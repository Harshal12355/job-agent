---
name: submit-application
description: Fills one application form in a headless browser through the Playwright MCP, screenshots it, and waits for Harshal's approval before clicking submit. Use when submitting a queued job, doing a dry run of a form, or when Harshal approves a submit from the dashboard.
disable-model-invocation: true
---

# Submit one application (supervised)

Input: a `queued` job with `out/<job_id>/resume.pdf`, `cover.pdf`, `tailored.yaml`.

## Gate: check before opening the browser

1. Board is Greenhouse, Lever, or Ashby. Anything in `config/manual_ats.yaml` (LinkedIn, Indeed, Workday, iCIMS, Taleo, SuccessFactors) stops here: `jobagent log manual_required --job <id>`.
2. `jobagent seen-apply <job_id>` returns false. Never apply twice.
3. Company has fewer than 2 open applications.

## Fill

1. `browser_navigate` to the posting's apply URL.
2. `browser_snapshot`. List every field with its label and whether it is required.
3. Map each field:
   - Contact, links: `answers.yaml` `contact`.
   - Resume / cover upload: the rendered PDFs.
   - Work authorization, sponsorship, salary, location, start date, EEO: `answers.yaml` only.
   - Free-text "why us" questions: write at most 80 words from the cover letter. Never new facts.
4. **Any required field with no source → stop.** `jobagent log manual_required --job <id> --reason "<field label>"`. Do not guess, do not pick a default option.
5. Fill with `browser_fill` / `browser_select_option` / file upload.
6. `browser_take_screenshot` of the full form. Save to `out/<job_id>/before_submit.png`.

## Approve, then submit

7. `jobagent log awaiting_approval --job <id>`. The dashboard shows the screenshot with **Approve** / **Reject**.
8. Only after an `approved` event exists for this job: click submit, wait for the confirmation page, screenshot to `out/<job_id>/after_submit.png`, then `jobagent log applied --job <id>`.
9. In `--dry-run` mode, stop after step 6 and log `dry_run_ok`.

## Never

- Solve or bypass a CAPTCHA. Log `manual_required --reason captcha`.
- Create accounts or log in to job sites on Harshal's behalf.
- Check boxes that certify something (background check consent, "I certify the above is true") without an `approved` event.
