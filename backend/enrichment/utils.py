import re
import os
import json
import threading
from urllib.parse import urlparse, urlunparse

# Thread-safe in-memory results storage
class ResultsStorage:
    _lock = threading.Lock()
    _results = []
    _db_file = "in_memory_db.json"

    @classmethod
    def load(cls):
        with cls._lock:
            if os.path.exists(cls._db_file):
                try:
                    with open(cls._db_file, 'r', encoding='utf-8') as f:
                        cls._results = json.load(f)
                except Exception:
                    cls._results = []

    @classmethod
    def save(cls):
        with cls._lock:
            try:
                with open(cls._db_file, 'w', encoding='utf-8') as f:
                    json.dump(cls._results, f, indent=2, ensure_ascii=False)
            except Exception:
                pass

    @classmethod
    def add(cls, item):
        with cls._lock:
            # Check for duplicates by website URL
            existing = next((x for x in cls._results if x['website_name'].lower() == item['website_name'].lower() or x.get('website_url', '').lower() == item.get('website_url', '').lower()), None)
            if existing:
                # Update existing
                existing.update(item)
            else:
                cls._results.append(item)
        cls.save()

    @classmethod
    def get_all(cls):
        with cls._lock:
            return list(cls._results)

# Initial load
ResultsStorage.load()


def clean_url(url: str) -> str:
    """Ensure URL has a valid scheme and remove trailing slashes."""
    url = url.strip()
    if not url:
        return ""
    
    # Try parsing
    parsed = urlparse(url)
    
    # If no scheme, default to https
    if not parsed.scheme:
        # Check if it starts with domain-like text
        url = "https://" + url
        parsed = urlparse(url)
        
    # Rebuild URL
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path.rstrip('/'), '', '', ''))


def extract_emails(text: str) -> list:
    """Regex based email extraction, filtering common false positives."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    found = re.findall(email_pattern, text)
    
    # Clean and filter false positives like image extensions or standard template variables
    cleaned = []
    invalid_suffixes = ('.png', '.jpg', '.jpeg', '.gif', '.svg', 'email.com', 'example.com', 'domain.com', 'yourdomain.com')
    for email in found:
        email_lower = email.lower()
        if not any(email_lower.endswith(suffix) or suffix in email_lower for suffix in invalid_suffixes):
            if email not in cleaned:
                cleaned.append(email)
    return cleaned


def extract_phones(text: str) -> list:
    """Regex based phone number extraction supporting multiple formats."""
    # Matches formats like +1-555-555-5555, +91 99999 99999, (555) 555-5555, 555.555.5555, etc.
    phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\+?\d{10,12}'
    found = re.findall(phone_pattern, text)
    
    cleaned = []
    for phone in found:
        # Basic sanity: strip non-numeric or valid formatting characters and verify length
        digits = re.sub(r'[^\d+]', '', phone)
        if 9 <= len(digits) <= 15:
            # Format and add unique numbers
            formatted = phone.strip()
            if formatted not in cleaned:
                cleaned.append(formatted)
    return cleaned


def clean_html_text(soup) -> str:
    """Remove boilerplate elements and clean whitespace for token optimization."""
    if not soup:
        return ""
        
    # Remove tags that carry no useful content for business profile extraction
    for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'noscript', 'iframe', 'svg', 'form', 'button', 'input']):
        tag.decompose()
        
    # Get text
    text = soup.get_text(separator=' ')
    
    # Clean whitespace: replace tabs, newlines, and multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()
