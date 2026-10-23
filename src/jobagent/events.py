"""Append-only event log. One CSV per run; rows are never edited or deleted."""

import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from jobagent import ROOT

EVENTS_DIR = ROOT / "data" / "events"
FIELDS = ["at", "job_id", "type", "detail_json", "run_id"]


def new_run_id(kind: str) -> str:
    return f"{datetime.now(UTC):%Y-%m-%dT%H%M%S}_{kind}"


class EventLog:
    def __init__(self, run_id: str):
        self.run_id = run_id
        EVENTS_DIR.mkdir(parents=True, exist_ok=True)
        self.path = EVENTS_DIR / f"{run_id}.csv"

    def log(self, job_id: str, type_: str, **detail) -> None:
        new_file = not self.path.exists()
        with self.path.open("a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            if new_file:
                writer.writeheader()
            writer.writerow({
                "at": datetime.now(UTC).isoformat(timespec="seconds"),
                "job_id": job_id,
                "type": type_,
                "detail_json": json.dumps(detail, sort_keys=True),
                "run_id": self.run_id,
            })


def seen_job_ids() -> set[str]:
    ids: set[str] = set()
    for path in EVENTS_DIR.glob("*.csv"):
        with path.open() as f:
            ids.update(row["job_id"] for row in csv.DictReader(f) if row["type"] == "found")
    return ids


def save_job(job_dict: dict) -> Path:
    jobs_dir = ROOT / "data" / "jobs"
    jobs_dir.mkdir(parents=True, exist_ok=True)
    path = jobs_dir / f"{job_dict['job_id'].replace('/', '_')}.json"
    path.write_text(json.dumps(job_dict, indent=2))
    return path
