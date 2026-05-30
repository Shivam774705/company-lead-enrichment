import os
import json
import re
from groq import Groq
from .constants import PRIMARY_MODEL, FALLBACK_MODEL, DEFAULT_RESPONSE_SCHEMA

class GroqService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = None
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"Failed to initialize Groq client: {e}")

    def clean_and_parse_json(self, raw_response: str) -> dict:
        """Sanitize raw LLM response and parse it into the strict schema."""
        cleaned = raw_response.strip()
        
        # Remove markdown block symbols
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
            
        cleaned = cleaned.strip()
        
        # Try to find JSON object if mixed with conversational text
        if not (cleaned.startswith("{") and cleaned.endswith("}")):
            match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if match:
                cleaned = match.group(0)
                
        try:
            parsed_data = json.loads(cleaned)
            
            # Reconstruct response to guarantee strict adherence to schema
            final_data = DEFAULT_RESPONSE_SCHEMA.copy()
            for key in final_data.keys():
                if key in parsed_data:
                    # Coerce types if LLM output got them wrong
                    if isinstance(final_data[key], list):
                        if isinstance(parsed_data[key], list):
                            final_data[key] = [str(x).strip() for x in parsed_data[key] if x]
                        elif isinstance(parsed_data[key], str):
                            final_data[key] = [parsed_data[key].strip()] if parsed_data[key] else []
                    else:
                        if isinstance(parsed_data[key], list):
                            final_data[key] = ", ".join([str(x) for x in parsed_data[key]])
                        else:
                            final_data[key] = str(parsed_data[key]).strip()
            return final_data
        except Exception as e:
            print(f"Error parsing LLM response JSON: {e}. Raw response: {raw_response}")
            return DEFAULT_RESPONSE_SCHEMA.copy()

    def enrich_company(self, cleaned_text: str, emails: list, phones: list, custom_website_name: str = "") -> dict:
        """Call Groq API to analyze webpage content and extract company details."""
        # 1. Handle missing client / API key gracefully
        if not self.client:
            print("Groq client not initialized (missing API key). Returning regex-extracted contacts only.")
            fallback = DEFAULT_RESPONSE_SCHEMA.copy()
            fallback["website_name"] = custom_website_name or "Unknown Company"
            fallback["mail"] = emails
            fallback["mobile_number"] = phones[0] if phones else ""
            fallback["probable_pain_point"] = "Groq API key not configured. Enable key to extract deeper insights."
            return fallback

        # 2. Build anti-hallucination prompt
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

        if cleaned_text:
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
                f"Pre-extracted verified emails: {emails}\n"
                f"Pre-extracted verified phone numbers: {phones}\n"
                f"Optional Custom Website Name: {custom_website_name}\n\n"
                f"Website text content:\n{cleaned_text}\n"
            )
        else:
            user_content = (
                f"We were unable to scrape the website content for: {custom_website_name or 'the company'}.\n"
                "Using your general pre-trained business intelligence knowledge about this company, please populate the company profile details using the schema below.\n"
                "If the company or domain is unknown or invalid, return empty values for the fields.\n\n"
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
                "}\n"
            )

        # 3. Call API with fallback model in case of rate limits
        for model in [PRIMARY_MODEL, FALLBACK_MODEL]:
            try:
                print(f"Calling Groq API with model: {model}")
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_content}
                    ],
                    temperature=0.1,  # Low temperature for highly factual extraction
                    max_tokens=1000,
                    response_format={"type": "json_object"}  # Request JSON response format
                )
                
                raw_response = response.choices[0].message.content
                result = self.clean_and_parse_json(raw_response)
                
                # If custom website name was passed and LLM returned empty website_name, inject it
                if custom_website_name and not result.get("website_name"):
                    result["website_name"] = custom_website_name
                elif not result.get("website_name"):
                    result["website_name"] = result.get("company_name", "Unknown Company")
                    
                # Merge pre-extracted emails and phones if LLM missed them
                for email in emails:
                    if email not in result["mail"]:
                        result["mail"].append(email)
                if not result["mobile_number"] and phones:
                    result["mobile_number"] = phones[0]
                    
                return result
            except Exception as e:
                print(f"Groq API call failed with model {model}: {e}")
                
        # 4. If all models failed, return regex extraction fallback
        fallback = DEFAULT_RESPONSE_SCHEMA.copy()
        fallback["website_name"] = custom_website_name or "Unknown Company"
        fallback["mail"] = emails
        fallback["mobile_number"] = phones[0] if phones else ""
        fallback["probable_pain_point"] = "AI Analysis failed or timed out. Scraped info only."
        return fallback
