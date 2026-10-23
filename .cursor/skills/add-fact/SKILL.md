---
name: add-fact
description: Adds or corrects a fact in the fact bank (work.yaml, projects.yaml, education.yaml) with evidence and status. Use when Harshal shares new work, a new project, a corrected number, or confirms a needs_review item.
---

# Add or confirm a fact

1. Decide where it belongs: a job, a project, or education. Project skills never go into `work.yaml`.
2. Find evidence:
   - OpenTug work: `gh pr list --repo OpenTug/ATDS --author Harshal12355 --state merged --search "<words>"`. Cite `ATDS#<n>`.
   - Project: a file path in the repo that shows the skill.
   - Neither: `self-reported`.
3. Set `claim`: `shipped` (merged), `co_shipped` (merged with teammates), or `analyzed` (real work, not merged).
4. Set `status: confirmed` only when Harshal said it is true in this conversation. Otherwise use `needs_review`.
5. List every number in the text under `numbers`, exactly as written.
6. Show Harshal the new YAML block before saving it.

```yaml
- id: otug-<short-name>
  text: <verb-first, one line, no customer names>
  skills: [...]
  numbers: [...]
  claim: shipped
  status: confirmed
  evidence: [ATDS#12345]
```

Never delete a fact to make a packet pass validation. Fix the packet instead.
