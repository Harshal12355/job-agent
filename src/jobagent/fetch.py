import csv
import json
import sys
from datetime import UTC, datetime

import httpx
import yaml

from jobagent import ROOT
from jobagent.events import EVENTS_DIR, EventLog, save_job, seen_job_ids
from jobagent.http import client
from jobagent.models import Job
from jobagent.sources import ats, jsearch


def _config() -> dict:
    return yaml.safe_load((ROOT / "config" / "sources.yaml").read_text())


def jsearch_requests_this_month() -> int:
    month = f"{datetime.now(UTC):%Y-%m}"
    used = 0
    for path in EVENTS_DIR.glob(f"{month}-*.csv"):
        with path.open() as f:
            for row in csv.DictReader(f):
                if row["type"] == "jsearch_request":
                    used += json.loads(row["detail_json"]).get("pages", 1)
    return used


def _fetch_jsearch(http: httpx.Client, cfg: dict, log: EventLog) -> list[Job]:
    jobs: list[Job] = []
    for query in cfg["queries"]:
        if jsearch_requests_this_month() + cfg["num_pages"] > cfg["monthly_budget"]:
            log.log("-", "jsearch_budget_exhausted", budget=cfg["monthly_budget"])
            print("JSearch monthly budget reached; skipping remaining queries", file=sys.stderr)
            break
        try:
            found = jsearch.search(
                http, query, date_posted=cfg["date_posted"], num_pages=cfg["num_pages"],
                under_3_years=cfg.get("under_3_years", True),
            )
        except (httpx.HTTPError, RuntimeError) as err:
            log.log("-", "source_error", source="jsearch", query=query, error=str(err))
            continue
        log.log("-", "jsearch_request", query=query, pages=cfg["num_pages"], results=len(found))
        jobs.extend(found)
    return jobs


def _fetch_ats(http: httpx.Client, cfg: dict, log: EventLog) -> list[Job]:
    jobs: list[Job] = []
    with (ROOT / cfg["companies_file"]).open() as f:
        companies = list(csv.DictReader(f))
    for row in companies:
        slug, board = row["slug"].strip(), (row.get("board") or "").strip()
        board = board or ats.resolve_board(http, slug) or ""
        if board not in ats.ADAPTERS:
            log.log("-", "source_error", source="ats", slug=slug, error="no board found")
            continue
        try:
            jobs.extend(ats.ADAPTERS[board](http, slug))
        except httpx.HTTPError as err:
            log.log("-", "source_error", source=board, slug=slug, error=str(err))
    return jobs


def run(sources: list[str]) -> dict:
    cfg = _config()
    log = EventLog(f"{datetime.now(UTC):%Y-%m-%dT%H%M%S}_fetch")
    seen = seen_job_ids()
    fetched: list[Job] = []
    with client() as http:
        if "jsearch" in sources and cfg["jsearch"]["enabled"]:
            fetched += _fetch_jsearch(http, cfg["jsearch"], log)
        if "ats" in sources and cfg["ats"]["enabled"]:
            fetched += _fetch_ats(http, cfg["ats"], log)

    new = 0
    for job in fetched:
        if job.job_id in seen:
            continue
        seen.add(job.job_id)
        data = job.to_dict()
        save_job(data)
        best = data["best_apply"] or {}
        log.log(job.job_id, "found", source=job.source, company=job.company, title=job.title,
                board=best.get("board"), automatable=best.get("automatable"))
        new += 1
    return {"fetched": len(fetched), "new": new, "events": str(log.path.relative_to(ROOT))}
