---
name: job-discovery
description: >-
  Find new job postings for lanes A and B: run `jobagent fetch`, spend JSearch credits on
  ad-hoc searches, add companies to companies.csv, and route each job to the board where it
  can be applied. Use for "find more jobs", "supply is short", "search for X roles", adding a
  company, or the Sunday discover run.
---

# Job discovery

## Where jobs come from

```text
JSearch (Google for Jobs) ──┐   LinkedIn, Indeed, Glassdoor listings, read through Google
Greenhouse / Lever / Ashby ─┼──► jobagent fetch ──► data/jobs/*.json + "found" events
companies.csv (you + agent) ┘   free public APIs, every posting at that company
```

Neither source logs into anything. The agent never opens linkedin.com or indeed.com.

## Steps

1. Scheduled run: `jobagent fetch` (both sources). It skips jobs already logged as `found`.
2. Ad-hoc search: `search_jobs(query)` on the `jobagent` MCP. **Each call costs 1 JSearch credit.**
   Company-first discovery (PLAN.md 3.1) is the main path; JSearch is for the week-1 gap check
   and for questions our registry can't answer yet. Prefer adding a company to `companies.csv`.
   Check `credits_used_this_month` in the reply. Stop at 80% of `monthly_budget` in
   `config/sources.yaml` and say so; don't burn the rest of the month on one session.
3. For every job, read `best_apply`:
   - `automatable: true` (Greenhouse, Lever, Ashby): goes to the normal tailor → approve → submit path.
   - `board: linkedin | indeed | workday | ...`: manual queue. The packet is still tailored; Harshal clicks submit.
   - Use `resolve_apply_link(url)` on any link you're unsure about.
4. When a JSearch job's apply link is on Greenhouse, Lever, or Ashby, add that company's slug to
   `companies.csv` (`slug,board`). Next fetch pulls *all* its postings for free.
5. Report: new jobs, how many are automatable, credits left, any `source_error` events.

## Good queries

Short, title-first, US-scoped. `config/sources.yaml` has the standing list.

| Lane | Query |
|---|---|
| A | `analytics engineer dbt snowflake`, `analytics engineer in United States` |
| B | `data analyst sql dbt in United States`, `business intelligence analyst` |
| Domain bonus | `analytics engineer logistics`, `bi analyst energy`, `data analyst freight` |

Leave `under_3_years: true` on. It is the cheapest filter there is: the API drops senior roles before they cost a credit.

## Never

- Turn on `jobspy` in `config/sources.yaml` without Harshal saying so in chat. It scrapes LinkedIn and Indeed from the Mac mini's home connection (his friend's IP).
- Use a LinkedIn MCP, AIHawk, or any tool that logs into his LinkedIn.
- Add a company only because it's famous. Big boards are mostly senior roles: a live test of 4 large companies returned 798 postings and 12 analytics titles, nearly all Staff or Principal.
