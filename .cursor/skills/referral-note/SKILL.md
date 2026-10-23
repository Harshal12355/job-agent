---
name: referral-note
description: Drafts a short referral request and a list of people to ask for a high-scoring job, for Harshal to send by hand. Use for jobs scoring 85+, or when Harshal asks who he could reach out to at a company.
disable-model-invocation: true
---

# Referral note

Referred candidates were hired at about 10× the rate of job-board applicants (Lever data). One good referral beats twenty cold applications.

The agent never logs in to LinkedIn or messages anyone. It writes `out/<job_id>/referral.md` and Harshal sends it.

## Steps

1. List who to look for (Harshal searches LinkedIn himself):
   - Northeastern University or Heriot-Watt alumni at the company.
   - People with "analytics engineer," "data," or "BI" in their title on the hiring team.
   - Anyone who has worked at OpenTug or a marine/energy company.
2. Draft the message (under 80 words):

```text
Hi <name>, I'm a data scientist at OpenTug doing analytics engineering in dbt and Snowflake
(one row per barge voyage, with clocks and dollars customers argue about). I'm applying for
<role> on <team> and <one specific reason>. Would you be open to a 10-minute chat, or to
referring me if it seems like a fit? Resume attached. Thanks either way.
```

3. Add a line to the dashboard: `jobagent log referral_drafted --job <id>`.
4. When Harshal says he sent it: `jobagent log referral_sent --job <id>`. If someone refers him, `referral_given`. The Learn tab compares reply rates with and without one.
