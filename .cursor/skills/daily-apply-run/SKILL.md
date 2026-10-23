---
name: daily-apply-run
description: Runs the weekday job pipeline end to end (fetch, filter, score, tailor, validate, render, queue, log, notify) toward the 30-packet daily goal. Use when the 7am Automation fires or when Harshal asks to run today's batch.
disable-model-invocation: true
---

# Daily apply run

Goal: 30 validated packets in `queue/<today>.md`. Quality floor first, count second.

```
Progress:
- [ ] 1. jobagent fetch
- [ ] 2. jobagent filter
- [ ] 3. Score survivors (agent)
- [ ] 4. Tailor the top 30 scoring 70+ (tailor-application skill)
- [ ] 5. jobagent validate (loop until clean)
- [ ] 6. jobagent render
- [ ] 7. jobagent queue
- [ ] 8. jobagent notify --digest
```

## Steps

1. `jobagent fetch --run-id $RUN`: pulls every company in `companies.csv` and saves descriptions to `data/jobs/`.
2. `jobagent filter --run-id $RUN`: applies `profile/preferences.yaml`. Prints survivors as JSON.
3. For each survivor, write a score record to `out/<job_id>/score.json`:
   ```json
   {"job_id": "...", "score": 0, "lane": "A|B", "stretch": false,
    "reasons": ["max 3"], "gaps": ["max 3"]}
   ```
   Score on grain match (do they care about one trusted row of something?), stack overlap (SQL, dbt, warehouse, BI), level fit, domain (logistics, energy, marine score higher), and freshness (posted 0 to 4 days ago scores highest; early applicants are a large share of hires).
4. Sort by score. Tailor the top 30 that score 70 or higher. For any job scoring 85+, also run `referral-note`.
5. `jobagent validate out/<job_id>/tailored.yaml`. On errors, fix the packet and rerun. Never edit the fact bank to make a packet pass.
6. `jobagent render out/<job_id>/`: writes the resume and cover letter PDFs.
7. `jobagent queue --run-id $RUN`: writes `queue/<today>.md` and `queued` events.
8. If fewer than 30 were queued, `jobagent log supply_short --count N`. Then `jobagent notify --digest`.

## Stop conditions

- A board errors: log it, skip that company, continue.
- A job has an `ai_disclaimer` asking applicants not to use AI: queue it with the flag `manual_only`, no tailored text.
- Never submit in this run. Submitting is a separate step.
