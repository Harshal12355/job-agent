---
name: resume-principles
description: Evidence-based rules for resumes and cover letters that parse cleanly in Greenhouse, Lever, Ashby, and Workday and read well to recruiters. Use when writing, tailoring, reviewing, or rendering a resume or cover letter, or when changing profile/resume.typ.
---

# Resume principles

Ranked by evidence strength. The first five come from the ATS vendors' own documentation, so the validator enforces them. Sources: [sources.md](sources.md).

## A. Parsing rules (validator-enforced)

1. **One column.** No tables, text boxes, images, icons, or multi-column layouts. Name and contact sit in the body, never a page header or footer.
2. **Standard headings only:** Summary, Experience, Projects, Education, Skills.
3. **Each job is title, company, dates in a fixed order.** OpenTug title is always `Data Scientist` (from `work.yaml`).
4. **Text PDF under 2.5 MB.** After rendering, `pdftotext` must return every bullet in reading order. If a bullet is missing or out of order, the packet fails.
5. **Keywords exactly as the posting spells them, once in Skills and once in a bullet,** but only when a fact supports it. Greenhouse keyword search is exact-match: "dimensional modeling" ≠ "data modeling."
6. **No abbreviations a recruiter would search spelled out**, and no hyphenated line breaks inside a keyword.
7. **File name:** `Harshal_Shinoy_Thachapully_Resume.pdf`. Never the company name in the file name.

## B. Writing rules (agent-enforced)

8. **Bullet shape:** accomplished X, measured by Y, by doing Z. Lead with the outcome or the thing built. Tools go at the end.
   - ✅ "Cut dbt pull-request CI from about 32 minutes to about 6 with a nightly full build and slim rebuilds"
   - ❌ "Responsible for dbt CI optimization using GitHub Actions"
9. **Numbers only from the fact's `numbers` list.** No number? Describe the mechanism ("pairing events per barge so a two-barge tow is not double-counted"). A concrete mechanism beats a fake percentage.
10. **Show practice, not just tools:** grain, tests, CI, metric definitions, who used the output.
11. **Headline under 10 words, describing skills, not a title:** "Analytics Engineering · dbt · Snowflake · Sigma."
12. **One page.** Bold titles and companies; newest first. Recruiters' eyes go title → company → dates.
13. **Skills section lists only tools a bullet or project proves.** Group by type. Put the posting's tools first.
14. **Tailor by reordering and trimming the base packet,** not by rewriting from scratch.

## C. Signs of AI writing (never ship these)

- Stock phrases: "spearheaded," "leveraged," "cutting-edge," "passionate," "results-driven," "dynamic," "synergy," "proven track record."
- Em dashes in prose. Use a comma, a colon, or two sentences.
- Every bullet the same length and rhythm. Vary them: some short, some with a mechanism.
- A resume that repeats the posting's phrases sentence by sentence.
- Skills the experience does not back up.
- Any hidden text or instructions aimed at an AI screener. That reads as deception.

## D. Cover letter (under 150 words)

Tailored letters show a modest callback lift; generic ones show almost none. So either tailor it or skip it.

1. Line 1: the role, and one reason that is specific to this company. If there is a referral, name the person here.
2. One story from `opentug_brief.md`, in 2 to 3 sentences, matched to their first paragraph.
3. One detail that could only come from reading their posting or product closely.
4. Plain close. No "I am excited to apply."
5. Vary sentence openings: at most 2 sentences start with "I."
6. Same font as the resume. Address a named person when the posting gives one.

## E. Strategy (scoring and queue order)

- **Apply within 1 to 4 days of posting.** 41% of applicants arrive in the first 48 hours. Freshness is a top score input.
- **Referrals beat everything.** Lever data shows 1 in 16 referred candidates hired versus 1 in 152 from job boards. For scores 85+, run the `referral-note` skill.
- **Knockout questions reject more people than resume parsing does.** Never guess one. A `null` in `answers.yaml` sends the job to the manual queue.
- **If a posting asks applicants not to use AI,** queue it `manual_only` with no tailored text.
