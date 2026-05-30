# Validation Test Report

| Test Case | Input URL | Status | Crash Check | Schema Stable? | Mail is Array? | Insights Extracted? |
| --- | --- | --- | --- | --- | --- | --- |
| Valid Company URL (Zoho) | `https://www.zoho.com` | PASSED | Yes | Yes | Yes | Yes |
| Invalid URL (abc) | `abc` | PASSED | Yes | Yes | Yes | No |
| Dead Website (randomfakewebsite1234.com) | `https://randomfakewebsite1234.com` | PASSED | Yes | Yes | Yes | No |
| Website without sitemap (Google) | `https://www.google.com` | PASSED | Yes | Yes | Yes | Yes |
| Website with limited contacts (Stripe) | `https://www.stripe.com` | PASSED | Yes | Yes | Yes | Yes |
| Weird Company (Caterpillar) | `https://www.caterpillar.com` | PASSED | Yes | Yes | Yes | No |
| Weird Company (Mahindra) | `https://www.mahindra.com` | PASSED | Yes | Yes | Yes | Yes |