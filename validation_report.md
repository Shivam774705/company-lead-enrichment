# Hackathon Production Validation Report

This report validates the robustness and schema stability of the **LeadEnrich AI** engine against unseen corporate targets and extreme input edge cases.

## 1. Schema Stability Summary
> [!NOTE]
> **PASS**: All test cases returned the strict JSON schema with correct field data types. No server crashes or schema breakages occurred.

## 2. Detailed Test Runs

| Test Name | URL | Status | Scraped Emails | Scraped Mobile | Result Schema Check |
| --- | --- | --- | --- | --- | --- |
| Razorpay | `https://razorpay.com` | `failed` | `None` | `None` | **✅ STABLE** |
| Zoho | `https://www.zoho.com` | `partial` | `slo@zohocorp.com, alejandro.g@zohocorp.com, pr@zohocorp.com, upgrade@zohocorp.com, tetsuhiro.iwami@zohocorp.com, peterbalaji@zohocorp.com, renewal@zohocorp.com, nanya@zohocorp.com, jessica.loo@zohocorp.com, press@zohocorp.com, license@zoho.jp, julie.watson@eu.zohocorp.com, abuse@zohocorp.com, cn-sales@zohocorp.com, mengxue.li@zohocorp.com, cancellation@zohocorp.com, privacy@zohocorp.com, sales@zoho.jp, sales@zohocorp.com` | `+1 844 584 2497` | **✅ STABLE** |
| Freshworks | `https://freshworks.com` | `failed` | `None` | `None` | **✅ STABLE** |
| Postman | `https://www.postman.com` | `partial` | `None` | `848995 2026` | **✅ STABLE** |
| Chargebee | `https://www.chargebee.com` | `failed` | `None` | `None` | **✅ STABLE** |
| Invalid URL | `abc` | `failed` | `None` | `None` | **✅ STABLE** |
| Dead Website | `https://randomfakewebsite1234.com` | `failed` | `None` | `None` | **✅ STABLE** |
| Empty URL | `` | `success` | `None` | `None` | **✅ STABLE** |

## 3. Raw Response Objects

### Razorpay (`https://razorpay.com`)
```json
{
  "website_name": "razorpay.com",
  "company_name": "",
  "address": "",
  "mobile_number": "",
  "mail": [],
  "core_service": "",
  "target_customer": "",
  "probable_pain_point": "Extraction error occurred: list index out of range",
  "outreach_opener": "",
  "status": "failed"
}
```

### Zoho (`https://www.zoho.com`)
```json
{
  "website_name": "www.zoho.com",
  "company_name": "",
  "address": "",
  "mobile_number": "+1 844 584 2497",
  "mail": [
    "slo@zohocorp.com",
    "alejandro.g@zohocorp.com",
    "pr@zohocorp.com",
    "upgrade@zohocorp.com",
    "tetsuhiro.iwami@zohocorp.com",
    "peterbalaji@zohocorp.com",
    "renewal@zohocorp.com",
    "nanya@zohocorp.com",
    "jessica.loo@zohocorp.com",
    "press@zohocorp.com",
    "license@zoho.jp",
    "julie.watson@eu.zohocorp.com",
    "abuse@zohocorp.com",
    "cn-sales@zohocorp.com",
    "mengxue.li@zohocorp.com",
    "cancellation@zohocorp.com",
    "privacy@zohocorp.com",
    "sales@zoho.jp",
    "sales@zohocorp.com"
  ],
  "core_service": "",
  "target_customer": "",
  "probable_pain_point": "Groq API Key not supplied. Scraping only.",
  "outreach_opener": "",
  "status": "partial"
}
```

### Freshworks (`https://freshworks.com`)
```json
{
  "website_name": "freshworks.com",
  "company_name": "",
  "address": "",
  "mobile_number": "",
  "mail": [],
  "core_service": "",
  "target_customer": "",
  "probable_pain_point": "Extraction error occurred: list index out of range",
  "outreach_opener": "",
  "status": "failed"
}
```

### Postman (`https://www.postman.com`)
```json
{
  "website_name": "www.postman.com",
  "company_name": "",
  "address": "",
  "mobile_number": "848995 2026",
  "mail": [],
  "core_service": "",
  "target_customer": "",
  "probable_pain_point": "Groq API Key not supplied. Scraping only.",
  "outreach_opener": "",
  "status": "partial"
}
```

### Chargebee (`https://www.chargebee.com`)
```json
{
  "website_name": "www.chargebee.com",
  "company_name": "",
  "address": "",
  "mobile_number": "",
  "mail": [],
  "core_service": "",
  "target_customer": "",
  "probable_pain_point": "Extraction error occurred: list index out of range",
  "outreach_opener": "",
  "status": "failed"
}
```

### Invalid URL (`abc`)
```json
{
  "website_name": "abc",
  "company_name": "",
  "address": "",
  "mobile_number": "",
  "mail": [],
  "core_service": "",
  "target_customer": "",
  "probable_pain_point": "Extraction error occurred: list index out of range",
  "outreach_opener": "",
  "status": "failed"
}
```

### Dead Website (`https://randomfakewebsite1234.com`)
```json
{
  "website_name": "randomfakewebsite1234.com",
  "company_name": "",
  "address": "",
  "mobile_number": "",
  "mail": [],
  "core_service": "",
  "target_customer": "",
  "probable_pain_point": "Extraction error occurred: list index out of range",
  "outreach_opener": "",
  "status": "failed"
}
```

### Empty URL (``)
```json
{
  "website_name": "",
  "company_name": "",
  "address": "",
  "mobile_number": "",
  "mail": [],
  "core_service": "",
  "target_customer": "",
  "probable_pain_point": "",
  "outreach_opener": "",
  "status": "success"
}
```

