# Job agent

Finds Analytics Engineer and Data/BI Analyst jobs, tailors a truthful resume and cover letter for each, queues them for Harshal, and tracks every reply.

## Read first

- `PLAN.md`: the whole design.
- `profile/opentug_brief.md`: the only source for OpenTug work.
- `.cursor/rules/truth-first.mdc`: what can never be claimed.

## Skills

| Skill | When |
|---|---|
| `resume-principles` | Any resume or cover letter writing or review |
| `daily-apply-run` | 7am weekday run, or "run today's batch" |
| `job-discovery` | Find more jobs, ad-hoc JSearch searches, add a company, route apply links |
| `company-research` | Glassdoor interviews, salary ranges, company news (OpenWeb Ninja MCP, 3 tools only) |
| `tailor-application` | One job's resume and cover letter |
| `submit-application` | Fill a form with Playwright MCP, wait for approval, submit |
| `referral-note` | Jobs scoring 85+, or "who can I ask at X?" |
| `inbox-triage` | Inbox run every 2 hours, or "what came back?" |
| `add-fact` | Harshal shares or confirms a fact |

## Commands

Everything runs in Docker. Render there, so every PDF uses the same font.

```bash
docker compose build
docker compose up -d playwright                       # browser MCP on localhost:8931
docker compose run --rm worker jobagent render profile/packets/base_lane_a.yaml --out out/lane_a
docker compose run --rm worker jobagent check-pdf <pdf> <packet>
docker compose run --rm worker jobagent fetch         # JSearch + company boards -> data/jobs/
docker compose up -d worker                           # cron: daily, inbox, discover, backup
```

Production runs on the Mac mini (PLAN.md section 3.11). Deploy: `ssh mini '~/job-agent/scripts/deploy.sh'`.

MCP servers are in `.cursor/mcp.json`: `jobagent` (our tools, stdio via Docker), `playwright`, and `openwebninja` (research only; see the `company-research` skill).
`jobagent` tools: `list_facts`, `render_packet`, `check_rendered_pdf`, `search_jobs` (costs 1 JSearch credit), `resolve_apply_link`, `list_found_jobs`.

## Hard rules

1. No invented facts. The validator blocks the packet.
2. No guessed form answers. `null` in `answers.yaml` sends the job to the manual queue.
3. No CAPTCHA bypass. LinkedIn, Indeed, and Workday are always manual.
4. At most 2 open applications per company.
5. Append-only event log.
