import os
import sys
import json
import traceback

# Add backend to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

# Load dotenv to get Groq API key
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", ".env")))

from enrichment.scraper import SmartScraper
from enrichment.ai_service import GroqService
from enrichment.constants import DEFAULT_RESPONSE_SCHEMA

def run_validation_tests():
    # We will test 5 cases
    test_cases = [
        {"name": "Valid Company URL (Zoho)", "url": "https://www.zoho.com"},
        {"name": "Invalid URL (abc)", "url": "abc"},
        {"name": "Dead Website (randomfakewebsite1234.com)", "url": "https://randomfakewebsite1234.com"},
        {"name": "Website without sitemap (Google)", "url": "https://www.google.com"},
        {"name": "Website with limited contacts (Stripe)", "url": "https://www.stripe.com"},
        {"name": "Weird Company (Caterpillar)", "url": "https://www.caterpillar.com"},
        {"name": "Weird Company (Mahindra)", "url": "https://www.mahindra.com"}
    ]

    report = []
    report.append("# Validation Test Report\n")
    report.append("| Test Case | Input URL | Status | Crash Check | Schema Stable? | Mail is Array? | Insights Extracted? |")
    report.append("| --- | --- | --- | --- | --- | --- | --- |")

    ai_service = GroqService()

    for tc in test_cases:
        name = tc["name"]
        url = tc["url"]
        print(f"Running test: {name} (URL: {url})...")
        
        crash_free = True
        schema_stable = False
        mail_is_array = False
        insights_extracted = False
        outcome_status = "PASSED"
        
        try:
            # Run scraper
            scraper = SmartScraper(url)
            scraped = scraper.scrape()
            
            # Run AI service
            result = ai_service.enrich_company(
                cleaned_text=scraped.get("combined_text", ""),
                emails=scraped.get("emails", []),
                phones=scraped.get("phones", []),
                custom_website_name=""
            )
            
            # Check JSON schema stability (keys matches exactly)
            required_keys = set(DEFAULT_RESPONSE_SCHEMA.keys())
            result_keys = set(result.keys())
            schema_stable = (required_keys == result_keys)
            
            # Check mail is array
            mail_is_array = isinstance(result.get("mail"), list)
            
            # Check insights (core_service / target_customer not empty)
            insights_extracted = bool(result.get("core_service") or result.get("probable_pain_point"))
            
            # Print result summary
            print(f"Result for {url}: {json.dumps(result, indent=2)}")
            
        except Exception as e:
            crash_free = False
            outcome_status = "FAILED"
            print(f"Crash detected on {url}: {e}")
            traceback.print_exc()
            
        report.append(f"| {name} | `{url}` | {outcome_status} | {'Yes' if crash_free else 'No (Crash)'} | {'Yes' if schema_stable else 'No'} | {'Yes' if mail_is_array else 'No'} | {'Yes' if insights_extracted else 'No'} |")

    # Save report
    report_content = "\n".join(report)
    report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "artifacts", "validation_report.md"))
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"Validation report saved to: {report_path}")

if __name__ == "__main__":
    run_validation_tests()
