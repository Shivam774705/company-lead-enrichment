import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import xml.etree.ElementTree as ET
from rapidfuzz import fuzz
import random
import re
import warnings
from bs4 import XMLParsedAsHTMLWarning
from .constants import DEFAULT_HEADERS, USER_AGENTS, TARGET_KEYWORDS
from .utils import clean_html_text, clean_url, extract_emails, extract_phones

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

class SmartScraper:
    def __init__(self, base_url: str):
        self.base_url = clean_url(base_url)
        self.domain = urlparse(self.base_url).netloc
        self.session = requests.Session()
        
    def _get_headers(self):
        headers = DEFAULT_HEADERS.copy()
        headers["User-Agent"] = random.choice(USER_AGENTS)
        return headers

    def fetch_page(self, url: str) -> str:
        """Fetch a page with dynamic headers, timeout, and basic error handling."""
        try:
            response = self.session.get(
                url, 
                headers=self._get_headers(), 
                timeout=8, 
                allow_redirects=True
            )
            # Raise exception for bad responses
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching page {url}: {e}")
            return ""

    def get_sitemap_urls(self) -> list:
        """Attempt to fetch sitemap.xml and parse URLs."""
        sitemap_url = urljoin(self.base_url, "/sitemap.xml")
        try:
            response = self.session.get(
                sitemap_url, 
                headers=self._get_headers(), 
                timeout=5
            )
            if response.status_code == 200:
                # Basic XML parsing
                root = ET.fromstring(response.content)
                # Sitemaps use namespaces usually
                namespace = ""
                if root.tag.startswith("{"):
                    namespace = root.tag.split("}")[0] + "}"
                
                urls = []
                for loc in root.findall(f".//{namespace}loc"):
                    if loc.text:
                        urls.append(loc.text.strip())
                return urls
        except Exception as e:
            print(f"Sitemap parsing failed for {self.base_url}: {e}")
        return []

    def get_homepage_links(self, homepage_html: str) -> list:
        """Extract and score internal links from the homepage HTML."""
        if not homepage_html:
            return []
            
        soup = BeautifulSoup(homepage_html, "lxml")
        links = []
        
        for anchor in soup.find_all("a", href=True):
            href = anchor["href"].strip()
            text = anchor.get_text(separator=' ').strip()
            
            # Resolve relative URLs
            full_url = urljoin(self.base_url, href)
            parsed_full = urlparse(full_url)
            
            # Ensure it is same domain and is an http/https link
            if parsed_full.netloc == self.domain and parsed_full.scheme in ("http", "https"):
                # Clean URL (strip anchors/queries)
                cleaned = urlunparse((parsed_full.scheme, parsed_full.netloc, parsed_full.path, '', '', ''))
                
                # Check that it's not the homepage itself
                if cleaned.rstrip('/') != self.base_url.rstrip('/'):
                    links.append({
                        "url": cleaned,
                        "text": text,
                        "path": parsed_full.path
                    })
                    
        return links

    def score_links(self, links: list) -> list:
        """Score links using fuzzy matching on path/text against target keywords."""
        scored_links = []
        seen_urls = set()
        
        for link in links:
            url = link["url"]
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            path_lower = link["path"].lower()
            text_lower = link["text"].lower()
            
            max_score = 0
            # Compare against target keywords
            for kw in TARGET_KEYWORDS:
                # Keyword matching
                if kw in path_lower or kw in text_lower:
                    score = 80 + len(kw)  # High score for direct matches
                else:
                    # Fuzzy match ratio
                    score_path = fuzz.partial_ratio(kw, path_lower)
                    score_text = fuzz.partial_ratio(kw, text_lower)
                    score = max(score_path, score_text)
                
                if score > max_score:
                    max_score = score
            
            # Filter low relevance links
            if max_score > 40:
                scored_links.append((max_score, url))
                
        # Sort descending by score
        scored_links.sort(key=lambda x: x[0], reverse=True)
        return [url for _, url in scored_links]

    def scrape(self) -> dict:
        """Run the smart scraper pipeline and return collected text, emails, and phones."""
        print(f"Starting Smart Scraper for {self.base_url}")
        
        homepage_html = self.fetch_page(self.base_url)
        if not homepage_html:
            # Failed to fetch homepage entirely
            return {
                "combined_text": "",
                "emails": [],
                "phones": [],
                "status": "failed_homepage_fetch"
            }
            
        homepage_soup = BeautifulSoup(homepage_html, "lxml")
        homepage_text = clean_html_text(homepage_soup)
        
        # Primary Contact extraction from homepage text
        emails = extract_emails(homepage_html)
        phones = extract_phones(homepage_text)
        
        # Determine paths to fetch
        target_urls = []
        
        # APPROACH 1: Try sitemap
        sitemap_urls = self.get_sitemap_urls()
        if sitemap_urls:
            print(f"Found {len(sitemap_urls)} URLs in sitemap.xml. Scoring them...")
            # Form dummy links dict for scoring
            dummy_links = []
            for u in sitemap_urls:
                parsed = urlparse(u)
                dummy_links.append({
                    "url": u,
                    "text": "",
                    "path": parsed.path
                })
            target_urls = self.score_links(dummy_links)[:4] # Take top 4 sitemap pages
            
        # APPROACH 2: Try parsing homepage links
        if not target_urls:
            print("Sitemap empty or failed. Scrape homepage links...")
            homepage_links = self.get_homepage_links(homepage_html)
            target_urls = self.score_links(homepage_links)[:4] # Take top 4 fuzzy pages
            
        # Compile content
        pages_content = [f"=== Homepage URL: {self.base_url} ===\n{homepage_text}"]
        
        # Fetch target pages
        if target_urls:
            print(f"Top target pages to scrape: {target_urls}")
            for url in target_urls:
                page_html = self.fetch_page(url)
                if page_html:
                    page_soup = BeautifulSoup(page_html, "lxml")
                    page_text = clean_html_text(page_soup)
                    
                    # Extract any emails/phones on this subpage
                    emails.extend(extract_emails(page_html))
                    phones.extend(extract_phones(page_text))
                    
                    # Save page snippet
                    pages_content.append(f"=== Page URL: {url} ===\n{page_text}")
        else:
            print("No high-quality internal links discovered. Using homepage only (Approach 3).")

        # Clean lists (deduplicate)
        emails = list(set(emails))
        phones = list(set(phones))
        
        # Merge contents and optimize tokens (limit combined string length to 8500 chars)
        combined_text = "\n\n".join(pages_content)
        if len(combined_text) > 8500:
            combined_text = combined_text[:8500] + "... [Content truncated for token optimization]"
            
        return {
            "combined_text": combined_text,
            "emails": emails,
            "phones": phones,
            "status": "success"
        }

# Helper urlunparse import
from urllib.parse import urlunparse
