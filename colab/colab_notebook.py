# =====================================================================
# LeadEnrich AI - Google Colab Notebook Script
# AI & Automation Developer Hiring Hackathon - Subtask 1 & 2
# =====================================================================

# ---------------------------------------------------------------------
# 1. DEPENDENCY SETUP
# ---------------------------------------------------------------------
import sys
import subprocess

# Ensure necessary packages are installed
required_packages = ["groq", "requests", "beautifulsoup4", "lxml", "rapidfuzz"]
installed_packages = []

print("Validating dependencies...")
for pkg in required_packages:
    try:
        __import__(pkg)
    except ImportError:
        print(f"Installing {pkg}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

# ---------------------------------------------------------------------
# 2. CONFIGURATIONS & API KEY SETUP
# ---------------------------------------------------------------------
import os
import re
import json
import random
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urljoin, urlunparse
import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz
import warnings
from bs4 import XMLParsedAsHTMLWarning
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Try to get key from environment or Colab secrets, else prompt user
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    try:
        from google.colab import userdata
        GROQ_API_KEY = userdata.get('GROQ_API_KEY')
    except Exception:
        pass

if not GROQ_API_KEY:
    print("\n" + "="*60)
    print("GROQ API KEY IS REQUIRED")
    print("="*60)
    GROQ_API_KEY = input("Please enter your GROQ API Key: ").strip()

if not GROQ_API_KEY:
    print("[WARNING] No Groq API Key provided. AI enrichment will return mocked/scraped-only profiles.")

from groq import Groq

# Constants
PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-8b-instant"

DEFAULT_RESPONSE_SCHEMA = {
    "website_name": "",
    "company_name": "",
    "address": "",
    "mobile_number": "",
    "mail": [],
    "core_service": "",
    "target_customer": "",
    "probable_pain_point": "",
    "outreach_opener": ""
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
]

TARGET_KEYWORDS = [
    "about", "about-us", "contact", "contact-us", "services", 
    "solutions", "company", "who-we-are", "team", "industries"
]

# ---------------------------------------------------------------------
# 3. UTILITY HELPER FUNCTIONS
# ---------------------------------------------------------------------
def clean_url(url: str) -> str:
    url = url.strip()
    if not url:
        return ""
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
        parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path.rstrip('/'), '', '', ''))

def clean_html_text(soup) -> str:
    if not soup:
        return ""
    for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'noscript', 'iframe', 'svg', 'form', 'button', 'input']):
        tag.decompose()
    text = soup.get_text(separator=' ')
    return re.sub(r'\s+', ' ', text).strip()

def extract_emails(text: str) -> list:
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    found = re.findall(email_pattern, text)
    cleaned = []
    invalid_suffixes = ('.png', '.jpg', '.jpeg', '.gif', '.svg', 'email.com', 'example.com', 'domain.com', 'yourdomain.com')
    for email in found:
        email_lower = email.lower()
        if not any(email_lower.endswith(suffix) or suffix in email_lower for suffix in invalid_suffixes):
            if email not in cleaned:
                cleaned.append(email)
    return cleaned

def extract_phones(text: str) -> list:
    phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\+?\d{10,12}'
    found = re.findall(phone_pattern, text)
    cleaned = []
    for phone in found:
        digits = re.sub(r'[^\d+]', '', phone)
        if 9 <= len(digits) <= 15:
            formatted = phone.strip()
            if formatted not in cleaned:
                cleaned.append(formatted)
    return cleaned

# ---------------------------------------------------------------------
# 4. SMART SCRAPER CLASS
# ---------------------------------------------------------------------
class ColabSmartScraper:
    def __init__(self, base_url: str):
        self.base_url = clean_url(base_url)
        self.domain = urlparse(self.base_url).netloc
        self.session = requests.Session()
        
    def _headers(self):
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9"
        }

    def fetch_page(self, url: str) -> str:
        try:
            response = self.session.get(url, headers=self._headers(), timeout=8, allow_redirects=True)
            response.raise_for_status()
            return response.text
        except Exception as e:
            return ""

    def get_sitemap_urls(self) -> list:
        sitemap_url = urljoin(self.base_url, "/sitemap.xml")
        try:
            response = self.session.get(sitemap_url, headers=self._headers(), timeout=5)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                namespace = root.tag.split("}")[0] + "}" if root.tag.startswith("{") else ""
                return [loc.text.strip() for loc in root.findall(f".//{namespace}loc") if loc.text]
        except Exception:
            pass
        return []

    def get_homepage_links(self, html: str) -> list:
        if not html:
            return []
        soup = BeautifulSoup(html, "lxml")
        links = []
        for anchor in soup.find_all("a", href=True):
            href = anchor["href"].strip()
            text = anchor.get_text(separator=' ').strip()
            full_url = urljoin(self.base_url, href)
            parsed_full = urlparse(full_url)
            if parsed_full.netloc == self.domain and parsed_full.scheme in ("http", "https"):
                cleaned = urlunparse((parsed_full.scheme, parsed_full.netloc, parsed_full.path, '', '', ''))
                if cleaned.rstrip('/') != self.base_url.rstrip('/'):
                    links.append({"url": cleaned, "text": text, "path": parsed_full.path})
        return links

    def score_links(self, links: list) -> list:
        scored = []
        seen = set()
        for link in links:
            url = link["url"]
            if url in seen:
                continue
            seen.add(url)
            path_lower = link["path"].lower()
            text_lower = link["text"].lower()
            
            max_score = 0
            for kw in TARGET_KEYWORDS:
                if kw in path_lower or kw in text_lower:
                    score = 80 + len(kw)
                else:
                    score = max(fuzz.partial_ratio(kw, path_lower), fuzz.partial_ratio(kw, text_lower))
                if score > max_score:
                    max_score = score
            if max_score > 40:
                scored.append((max_score, url))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [url for _, url in scored]

    def scrape(self) -> dict:
        homepage_html = self.fetch_page(self.base_url)
        if not homepage_html:
            return {"combined_text": "", "emails": [], "phones": []}
            
        homepage_soup = BeautifulSoup(homepage_html, "lxml")
        homepage_text = clean_html_text(homepage_soup)
        
        emails = extract_emails(homepage_html)
        phones = extract_phones(homepage_text)
        
        target_urls = []
        sitemap_urls = self.get_sitemap_urls()
        if sitemap_urls:
            dummy_links = [{"url": u, "text": "", "path": urlparse(u).path} for u in sitemap_urls]
            target_urls = self.score_links(dummy_links)[:4]
            
        if not target_urls:
            homepage_links = self.get_homepage_links(homepage_html)
            target_urls = self.score_links(homepage_links)[:4]
            
        pages_content = [f"=== Homepage URL: {self.base_url} ===\n{homepage_text}"]
        
        for url in target_urls:
            page_html = self.fetch_page(url)
            if page_html:
                page_soup = BeautifulSoup(page_html, "lxml")
                page_text = clean_html_text(page_soup)
                emails.extend(extract_emails(page_html))
                phones.extend(extract_phones(page_text))
                pages_content.append(f"=== Page URL: {url} ===\n{page_text}")
                
        emails = list(set(emails))
        phones = list(set(phones))
        combined_text = "\n\n".join(pages_content)
        if len(combined_text) > 8500:
            combined_text = combined_text[:8500] + "... [Truncated]"
            
        return {
            "combined_text": combined_text,
            "emails": emails,
            "phones": phones
        }

# ---------------------------------------------------------------------
# 5. MANDATORY ENRICH COMPANY FUNCTION
# ---------------------------------------------------------------------
def enrich_company(url: str) -> dict:
    """
    Input: Company URL
    Output: Structured company profile [STRICT FORMAT]
    """
    cleaned_url = clean_url(url)
    if not cleaned_url:
        return DEFAULT_RESPONSE_SCHEMA.copy()
        
    try:
        # Step A: Scrape website intelligently
        scraper = ColabSmartScraper(cleaned_url)
        scraped = scraper.scrape()
        
        # Step B: Check API client key
        if not GROQ_API_KEY:
            fallback = DEFAULT_RESPONSE_SCHEMA.copy()
            fallback["website_name"] = urlparse(cleaned_url).netloc
            fallback["mail"] = scraped.get("emails", [])
            fallback["mobile_number"] = scraped.get("phones", [None])[0] or ""
            fallback["probable_pain_point"] = "Groq API Key not supplied. Scraping only."
            return fallback
            
        client = Groq(api_key=GROQ_API_KEY)
        
        # Step C: Prompt creation & Groq query
        system_instruction = (
            "You are a business intelligence extraction engine.\n"
            "Your task is to extract ONLY information explicitly present or strongly inferable from website content.\n\n"
            "CRITICAL RULES:\n"
            "* Never hallucinate phone numbers.\n"
            "* Never hallucinate emails.\n"
            "* Never invent addresses.\n"
            "* If data is missing return empty string \"\" or [].\n"
            "* Return STRICT VALID JSON ONLY. Do not wrap in markdown or commentary."
        )

        user_content = (
            "Extract company profile details using the schema below.\n\n"
            "Strict JSON Schema:\n"
            "{\n"
            "  \"website_name\": \"\",\n"
            "  \"company_name\": \"\",\n"
            "  \"address\": \"\",\n"
            "  \"mobile_number\": \"\",\n"
            "  \"mail\": [],\n"
            "  \"core_service\": \"\",\n"
            "  \"target_customer\": \"\",\n"
            "  \"probable_pain_point\": \"\",\n"
            "  \"outreach_opener\": \"\"\n"
            "}\n\n"
            f"Pre-extracted verified emails: {scraped.get('emails', [])}\n"
            f"Pre-extracted verified phone numbers: {scraped.get('phones', [])}\n\n"
            f"Website text content:\n{scraped.get('combined_text', '')}\n"
        )
        
        # Query primary model
        response = client.chat.completions.create(
            model=PRIMARY_MODEL,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_content}
            ],
            temperature=0.1,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        raw_text = response.choices[0].message.content.strip()
        
        # Sanitize code blocks
        if raw_text.startswith("```"):
            raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
            raw_text = re.sub(r"\s*```$", "", raw_text)
            
        parsed_data = json.loads(raw_text.strip())
        
        # Ensure schema structure and inject regex contacts
        final = DEFAULT_RESPONSE_SCHEMA.copy()
        for k in final.keys():
            if k in parsed_data:
                if isinstance(final[k], list):
                    if isinstance(parsed_data[k], list):
                        final[k] = [str(x).strip() for x in parsed_data[k] if x]
                    elif isinstance(parsed_data[k], str):
                        final[k] = [parsed_data[k].strip()] if parsed_data[k] else []
                else:
                    if isinstance(parsed_data[k], list):
                        final[k] = ", ".join([str(x) for x in parsed_data[k]])
                    else:
                        final[k] = str(parsed_data[k]).strip()
                        
        if not final.get("website_name"):
            final["website_name"] = final.get("company_name", urlparse(cleaned_url).netloc)
            
        # Guarantee pre-extracted arrays merge
        for email in scraped.get('emails', []):
            if email not in final["mail"]:
                final["mail"].append(email)
        if not final["mobile_number"] and scraped.get('phones'):
            final["mobile_number"] = scraped.get('phones')[0]
            
        return final
    except Exception as e:
        print(f"Failed enriching {url}: {e}")
        fallback = DEFAULT_RESPONSE_SCHEMA.copy()
        fallback["website_name"] = urlparse(cleaned_url).netloc
        fallback["probable_pain_point"] = f"Extraction error occurred: {e}"
        return fallback

# ========= 9. MAIN EXECUTION =========
if __name__ == "__main__":
    # The Golden Rule: Ask us for the array of URLs via input prompt
    urls_input = input("Enter URLs array (JSON format or comma-separated): ").strip()
    
    urls = []
    if urls_input:
        try:
            # Try parsing as JSON array e.g., ["https://razorpay.com", "https://zoho.com"]
            urls = json.loads(urls_input)
        except Exception:
            # Fallback to comma-separated list
            urls = [u.strip() for u in urls_input.split(",") if u.strip()]
            
    if not urls:
        # Fallback to defaults if input is empty
        urls = [
            "https://example1.com",
            "https://example2.com"
        ]
        
    results = []
    
    for url in urls:
        try:
            data = enrich_company(url)
            results.append(data)
        except Exception as e:
            print(f"Error processing {url}: {e}")
            
    # Save results to JSON file
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
    # Print results for evaluation
    print("\n=== FINAL OUTPUT ===\n")
    print(json.dumps(results, indent=2, ensure_ascii=False))
