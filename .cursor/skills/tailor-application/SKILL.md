---
name: tailor-application
description: Writes a tailored resume packet and cover letter for one job from the fact bank, choosing lane A (Analytics Engineer) or B (Data/BI Analyst). Use when tailoring a resume, writing a cover letter, or preparing an application packet.
disable-model-invocation: true
---

# Tailor one application

Inputs: `data/jobs/<job_id>.json`, `out/<job_id>/score.json`, the fact bank in `profile/`.
Output: `out/<job_id>/tailored.yaml` (same shape as `profile/packets/base_lane_a.yaml`) and `out/<job_id>/cover.md`.

Follow `.cursor/skills/resume-principles/SKILL.md` for every bullet and the cover letter.

## Steps

0. If the posting asks applicants not to use AI, stop: write no text, mark the score record `manual_only: true`.
1. Read the posting's first paragraph. Name the grain they care about (a shipment, an order, an invoice line, a voyage) and the decision it feeds.
2. Start from the lane's base packet (`profile/packets/base_lane_<a|b>.yaml`).
3. Reorder OpenTug bullets so the first one matches the first paragraph. Keep 6 to 8.
4. Reword using their vocabulary where the fact allows it. "Freight" for "voyage" is fine. "Kafka" for "Django" is not.
5. Pick 1 to 2 projects whose `lanes` include this lane.
6. Skills: put their named tools first, but only tools that are already in the fact bank. A missing tool goes into `gaps`, never the resume.
7. Write the cover letter (template below).
8. Run `jobagent validate out/<job_id>/tailored.yaml` until it passes.

## Lane order

| Lane A: Analytics Engineer | Lane B: Data / BI Analyst |
|---|---|
| otug-voyage-table, otug-clocks, otug-money, otug-ci | otug-recon, otug-util, otug-money, otug-voyage-table |

## Cover letter (under 150 words, no customer names)

Follow section D of `resume-principles`. Shape:

```markdown
Para 1: The role + one reason specific to this company (referral name first, if any).
Para 2: One story from opentug_brief.md "Interview stories", 2 to 3 sentences, matched to their first paragraph.
Para 3: One detail only a close reader of their posting would know + a plain close.
```

9. Self-check against section C (AI tells) of `resume-principles`. Rewrite any line that fails.

## Same-family substitutions allowed

Sigma for Power BI, Looker, or Tableau. Snowflake for BigQuery, Redshift, or Azure SQL. Say the real tool name anyway, e.g. "semantic models in Sigma (similar to Looker)."
