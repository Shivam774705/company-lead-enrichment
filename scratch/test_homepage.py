import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from enrichment.scraper import SmartScraper

scraper = SmartScraper("https://www.zoho.com")
homepage_html = scraper.fetch_page(scraper.base_url)

from bs4 import BeautifulSoup
from enrichment.utils import clean_html_text

soup = BeautifulSoup(homepage_html, "lxml")
text = clean_html_text(soup)

print("Homepage text length:", len(text))
# Save text to file so we can view it without encoding crashes
with open("scratch/zoho_text.txt", "w", encoding="utf-8") as f:
    f.write(text)
print("Saved to scratch/zoho_text.txt")
