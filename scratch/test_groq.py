import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", ".env")))

from enrichment.scraper import SmartScraper
from enrichment.ai_service import GroqService

scraper = SmartScraper("https://www.zoho.com")
data = scraper.scrape()

# print("Scraped Text Snippet (first 400 chars):")
# print(data["combined_text"][:400])
# print("="*60)

ai = GroqService()
# We will query directly and print raw LLM output
system_instruction = (
    "You are a business intelligence extraction engine.\n"
    "Your task is to extract ONLY information explicitly present or strongly inferable from website content.\n\n"
    "CRITICAL RULES:\n"
    "* Never hallucinate phone numbers. If none are present in the text or the pre-extracted list, return empty string \"\".\n"
    "* Never hallucinate emails. If none are present in the text or the pre-extracted list, return empty array [].\n"
    "* Never invent addresses.\n"
    "* If data is missing return empty string \"\" or [].\n"
    "* Return STRICT VALID JSON ONLY. Do not wrap in markdown or include conversational text."
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
    f"Pre-extracted verified emails: {data['emails']}\n"
    f"Pre-extracted verified phone numbers: {data['phones']}\n\n"
    f"Website text content:\n{data['combined_text']}\n"
)

response = ai.client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_content}
    ],
    temperature=0.1,
    max_tokens=1000,
    response_format={"type": "json_object"}
)

raw_output = response.choices[0].message.content
print("RAW LLM OUTPUT:")
print(raw_output)
