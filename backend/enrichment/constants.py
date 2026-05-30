# Groq AI Models
PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-8b-instant"

# Strict response schema structure
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

# Browser Headers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

DEFAULT_HEADERS = {
    "User-Agent": USER_AGENTS[0],
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0"
}

# Smart Scraping keywords for fuzzy matching
TARGET_KEYWORDS = [
    "about",
    "about-us",
    "contact",
    "contact-us",
    "services",
    "solutions",
    "company",
    "who-we-are",
    "team",
    "industries"
]
