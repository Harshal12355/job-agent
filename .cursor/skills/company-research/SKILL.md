---
name: company-research
description: >-
  Look up a company before tailoring, a referral note, or an interview: Glassdoor reviews and
  interview questions, salary ranges, recent news. Uses the OpenWeb Ninja MCP. Use for "what's it
  like at X", "what do they ask in interviews", "what does this role pay", the cover letter's
  why-this-company line, or building an interview kit.
---

# Company research (OpenWeb Ninja MCP)

The `openwebninja` MCP has 51 tools. This project uses **three**. Treat the rest as not there.

| Tool | Operation | Use it for |
|---|---|---|
| `realtime_glassdoor_data` | `company_search` → `company_reviews`, interviews | Interview kits: real questions people were asked, and red flags |
| `job_salary_data` | `job_salary` (title, location) | Telling Harshal the market range. **Never** fills a form answer |
| `realtime_news_data` | `search` (company name) | One recent, true fact for the cover letter's why-this-company line |

## Steps

1. Search with the **company name and job title only**. Nothing from `profile/` goes into a query.
2. Save what you used to `out/<job_id>/research.md` with the source URL of each fact.
3. Cover letter: at most one company fact, and it must be in `research.md`. It's a fact about them, never a claim about Harshal.
4. Interview kit: list the 5 most repeated Glassdoor interview questions, each mapped to a story from `profile/opentug_brief.md`.

## Credits

Each API has its own free tier on the same key. If a tool returns 401/403/429, it isn't subscribed yet: say so and ask before calling `subscribe`. It's free, but it's Harshal's account.

For **job search**, use `search_jobs` on the `jobagent` MCP, not `jsearch` here: ours counts credits against the monthly budget and resolves apply links. This server's `jsearch` spends the same 200 credits invisibly.

## Never

- `email_search`, `website_contacts_scraper`, `social_links_search`: scraping people's contact details for cold outreach. Referrals go through `referral-note`, with Harshal sending them himself.
- `chatgpt`, `gemini`, `copilot`, `google_ai_mode`: they relay text to another AI company.
- `web_unblocker`: gets around bot protection. Same rule as CAPTCHAs: never.
- Salary numbers into `answers.yaml` or a form. Harshal sets his own floor.
