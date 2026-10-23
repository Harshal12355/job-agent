# Apply-agent brief: Harshal Thachapully (OpenTug)

This is the only source for OpenTug work history. If a fact is not here or in `work.yaml`, it does not go into an application. Customer names stay in this file and never reach a resume, cover letter, or form.

Git record (checked 2026-10-22): 64 merged pull requests in `OpenTug/ATDS`, first merge 2025-10-13 (#6445), latest merge 2026-10-13 (#11020).

```text
carrier file or email
        │
        ▼
   a voyage row in Snowflake
        │
        ▼
   a clock or a dollar a person can argue with
```

## Rules

1. Official title on record is **Data Scientist**. Every resume, form, and cover letter uses exactly that as the OpenTug title. The *target role* is Analytics Engineer; the work is analytics engineering. A headline or summary may describe the work ("analytics engineering in dbt and Snowflake") but never relabels the job title. Domain: voyage economics for inland petroleum barges. Warehouse is Snowflake. Transform layer is dbt. The BI page is Sigma (same job as Power BI or Looker).
2. Timezone is America/New_York. Open to relocation anywhere in the US. Do not claim he already lives in a city a posting requires.
3. Employer is OpenTug. Start date on the git record is 2025-10-13.
4. **Never put in an application:** customer or shipper names, voyage IDs, dollar gaps, invoice amounts, internal schema names, coworker names, or Snowflake account details. Say "a petroleum barge operator," "a commodity shipper," "a midstream customer," "a carrier's Excel update."
5. **Never claim at OpenTug:** Machine Learning Engineer, PyTorch or TensorFlow, reinforcement learning, vector databases, GCP, Kafka, Spark, Airflow ownership, ETA models, computer vision, satellite imagery, gas trading, demurrage claims negotiation.
6. **Do claim:** he directed the work and can explain the grain, the metric, and how the number lies. Many merges used AI coding tools (Cursor). Do not hide that if asked.
7. Some pipelines were co-authored. Say "shipped" or "built with the team" for those.
8. If a posting's main verb is "train a model," skip it. If it is "make a trusted table, a metric, or a freight/marine report," read it.

## Stack he can talk about

| Shipped | How it showed up |
|---|---|
| Python, Django | Inbound-email pipelines, Excel and HTML parsers, tests |
| BAML | PDF attachments sent to an extractor as documents, not images |
| SQL | Grains, windows, event pairing, deduping per-barge stamps, reconciliation |
| dbt Core on Snowflake | Staging, intermediate, marts, seeds, macros, unit tests, data tests, docs, semantic views |
| Sigma | Workbooks and data models on serving tables |
| GitHub Actions CI | Slim dbt builds, manifest defer, selective SQLFluff, nightly full build |
| AIS | Positions over time, H3 geofences, dwell, pickup and drop-off, vessel state |
| Snowflake Cortex | A semantic view plus a small chatbot API, with teammates |

No production ML training loop. The "prediction" work is scored rules and an inferred barge count.

## Domain he can speak

Inland tank-barge operations. A tow is a boat plus one or more barges. A voyage is an order to move cargo. Crews file timestamped events, often once per barge, so a naive min or max lies. Commercial desks split cargo into clean products, black oils, chemicals, and lubes. Money shows up as a quote or live estimate, then as an invoice. Those are different numbers. Cost can point inbound (paid to a vendor) or outbound (paid by the customer). Publishing the inbound number to a customer exposes markup.

Vocabulary used on real tickets: demurrage, deadfreight, laycan, time-charter utilization, on-hire and off-hire, NOR, fleeting, hose time, tankerman, inspector, ROB, pump rate, ancillary charges, standby, dock delay, lock delay, ballast or empty move, laden move, product desk, AIS, geofence, dwell.

## How a number is allowed to ship

1. What decision changes if the number moves?
2. What is one row? Voyage, barge, tow, stop, or month?
3. How could it lie? Double count, blank treated as zero, wrong desk, estimate standing in for a bill, per-barge event treated as a tow event, inbound cost shown outbound.
4. One real voyage that proves the rule, plus a test that fails if the rule breaks.

Failure modes he has hit and can explain:

- `min(end)` stops a tow when the first barge finishes. End stamps need the last completion, or an explicit barge grain.
- A barge can be released, shifted, and released again. `min(start)` throws away the second cycle.
- Events are filed per barge. Pairing without collapsing duplicates doubles hours on a two-barge tow.
- Partitioning an event pair by port can drop a wait whose start and end were tagged at different ports.
- A blank utilization on an empty voyage makes a fleet average look too good. Blank is not zero.
- A savings metric needs a named baseline. Quote minus billed is fake when "billed" falls back to the estimate.
- A contract-type key beat a name search. Matching "COA" inside a tow name mis-labeled tows.

## Chapter 1: Oct 2025 to Jan 2026. Make the carrier's file into rows

- Valero Excel parser (#6445, 2025-10-13) and follow-up debug (#6456).
- Welspun Excel parser (#6440).
- Reference-number format (#6551).
- ACBL TowWorks HTML parser (#6737).
- Barge events concatenated (#6783).
- Voyage completion from the inbound message, with a teammate (#6858).
- Duplicate-email guard, with a teammate (#6899).
- Ocean tank-barge completion (#6965).
- PDF sent to BAML as a document instead of images (#6976).
- Kirby/Valero Excel update parser (#6939) and origin plus destination (#7039).
- "None" to TBN (#7033).
- Upcoming jobs assigned the wrong barge and tug, fixed (#7002).
- Valero update completes jobs (#7233).
- Completed-voyage refactor (#7297).
- Bunker levels from a Buffalo/Valero file (#7034).

Proves: messy operational files, idempotency, IDs, tests around parsers, a document extractor used as a component.

## Chapter 2: Feb 2026 to Jun 2026. Where the boat actually was

Shared with other engineers. Claim participation and the dbt models, not sole ownership.

- Movements dbt (#7572).
- WS1 and WS2 movements and trade flows (#7855), bug fix (#7919).
- Parent geofences and carrier commodity filter (#8084).
- Carrier foreign key and carrier class (#8282).
- Terminal type (#8387).
- Dwell pipeline, with a teammate (#8289). Base unit changed from pings to dwells. 97% of dwells matched to known infrastructure. H3 pre-filter plus H3 neighbors for edge cases.
- AIS id on fact tables and key-pair auth for dbt (#8545). Never describe key material.
- Inferred barge count, with a teammate and a coding agent (#8343). Heuristic, not a trained model.
- dbt CI: nightly full build, manifest artifact, SQLFluff on changed files only (#8993).
- Slim dbt build: `state:modified+` with manifest defer (#9095). Slim build ~10 s vs ~22 min; total PR CI ~32 min to ~6 min.

Proves: geospatial dwell, grain of a movement, commodity inference with gates, warehouse cost and CI. AIS position and time are trusted; feed speed, status, and barge counts are not.

## Chapter 3: Jun 2026 to Aug 2026. One row a customer can read

Customer-facing voyage flat model: one row per voyage, clocks from crew events, dollars from estimates and invoices, served to Sigma and a semantic view.

- Repaired voyage history (#9209).
- Voyage confidence score, a point score with gates (#9210).
- Voyage flat staging and plan (#9349), mart tables (#9400).
- Customer-reporting fixes and known-issues doc (#9495).
- KPI event seed, events intermediate, and a test that every seeded code exists (#9539).
- KPI metrics first slice: event pivot, voyage-event fact, timeline (#9574).
- Time fields and initial estimated cost (#9642, #9704).
- MMSI on the flat model plus dbt warning cleanup (#9670).
- Voyage-flat logic bugs: "the first grain was wrong and I fixed it" (#9778).
- Total fleeting time (#9818).
- Hose time, with a teammate (#9871). Hose On/Off paired per barge, overlapping intervals merged so two barges hosing at once count as one period. Stint macro reused by later clocks.
- Tankerman time (#9980). Idle days (#9901). Waiting-for-ride fix (#9935).
- Customer-facing flat and mart restructure (#10000).
- Folder restructure: voyage, spines, kpi (#10148).
- Phase timeline, inspector stints, greater port area (#10093).
- Lanes and invoice dollars, row-access policy, Sigma flat and semantic view (#10329).
- Port wait: NOR to arrived dock (#10352).
- Chatbot API and Cortex semantic view, with teammates (#10328). He helped the data side.

Proves: grain, event-pair clocks, widening a serving model without breaking the page, customer row security, estimates versus invoices, documented known gaps.

## Chapter 4: Sep 2026 to Oct 2026. The row has to be true in dollars and days

**Merged:**

- Fuel trading dashboard (#10413).
- Refinery-lane costs page, four PRs (#10658, #10657, #10702, #10703).
- Outbound invoices sent (#10700).
- Late arrival hours: missing stamp stays null, early is zero (#10717).
- Product desk on the operator KPI table (#10790).
- Time-charter utilization: 9 models, 18 tests (#10741). Unscored voyages must not vanish from the average.
- Transit clocks: laden, empty, port, dock delay, tender, total delay (#10838).
- Outbound ancillary and pre-load standby (#10971).
- Pump rate, ROB, deadfreight (#10995, #10998). Zero rate stays blank, not a fake zero.
- Empty movement = deadfreight run (#11020).

**Analyzed, designed, or still in review. Say "analyzed" or "designed," never "shipped":**

- Midstream round trips: voyages broken into round trips, stops, and tow-level laps with tests. Not merged as of 2026-10-22.
- Open PRs: deadfreight clock and laden window (#11199, #11200, #11201), delay overlay for weather, locks, dock (#11205), voyage miles and trip times (#11232), load vs discharge side costs (#11169), net gallons on tank gauge (#10942), contract firm dates on Cortex flats (#10846), semantic-view leftovers (#10889).
- Reconciled an estimate chart against a billed chart for dollars per barrel. The gap traced to a desk label that classified term tows two ways, and to fuel and demurrage columns that were filled but excluded by a formula gate.
- Rebuilt a historical boat log into one row per voyage, separating what the diary can fill from what only an invoice can fill.
- Learned that summing AIS miles across voyages double-counts a boat on two voyages at once.
- Active-voyage page: quantity must be the latest update that has tons, not the latest row.
- River congestion, design only: stopped boats in a hex versus that hex's normal weekday hour.
- Plain-language column guides for non-SQL readers.

## Interview stories (tell one, then stop)

1. **Two charts, one leftover.** Listed every charge in each formula, found a desk rule that classified the same tows two ways plus charges stored but left out of the sum. Name the leftover dollars before writing SQL.
2. **The average lied by omission.** Utilization only existed when a laden clock existed. Empty voyages were blank, so the scored average looked busy. Blank versus zero, said out loud, before the chart ships.
3. **The clock fired once per barge.** Earliest end stops the tow when the first barge finishes. Collapse to the tow or declare barge grain before publishing hours.

## Gaps the agent must not paper over

- About 12 months at OpenTug, about 18 months of full-time work total. Never "3+ years" or "senior."
- Python is strong in parsers, tests, and data helpers. Not a production streaming stack.
- Shipped BI tool is Sigma. Power BI and Looker are adjacent. No years of DAX.
- Geospatial is dwell and geofences on AIS. Not a GIS career.
- Document AI means integrating BAML on PDFs. Not training an LLM.
- Confidence score and barge-count guess are rules.
- Not SnowPro certified.
