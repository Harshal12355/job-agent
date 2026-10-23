---
name: inbox-triage
description: Reads recent job-related Gmail, classifies each reply, logs events, pushes alerts, and builds interview kits. Use when the inbox Automation fires or when Harshal asks what came back from applications.
disable-model-invocation: true
---

# Inbox triage

1. Search Gmail for the last 26 hours: senders from Greenhouse, Lever, Ashby, Workday, plus any company in `jobagent list --status applied`.
2. Skip any message whose Gmail id already has an event (`jobagent seen <gmail_id>`).
3. Classify each message as one of: `interview`, `assessment`, `rejection`, `offer`, `other`.
4. Match it to an application by company plus title. If nothing matches, log `email_unmatched` and continue.
5. `jobagent log email_<class> --job <job_id> --gmail-id <id>`.
6. `interview`, `assessment`, or `offer`: run `jobagent notify --high`, then write `out/<job_id>/interview_kit.md`:

```markdown
# <Company>: <Title>
Stage: <class>  |  Received: <date>  |  Link: <url>

## What they asked for (from the saved posting)
## What you sent (bullets with fact ids)
## Story to tell (one, from opentug_brief.md)
## Gaps they may probe, and the honest answer
```

Rejections are never pushed one at a time. They go into the evening digest.
