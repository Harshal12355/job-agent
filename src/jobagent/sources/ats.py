"""Public job-board APIs. No login, no key: Greenhouse, Lever, Ashby."""

import html
import re
from datetime import UTC, datetime

import httpx

from jobagent.apply_links import classify
from jobagent.models import Job


def _strip_html(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(text or ""))).strip()


def greenhouse(client: httpx.Client, slug: str) -> list[Job]:
    r = client.get(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs", params={"content": "true"})
    r.raise_for_status()
    jobs = []
    for j in r.json().get("jobs", []):
        url = j["absolute_url"]
        jobs.append(Job(
            job_id=f"greenhouse_{slug}_{j['id']}",
            source="greenhouse",
            company=j.get("company_name") or slug,
            title=j["title"],
            location=(j.get("location") or {}).get("name", ""),
            remote=None,
            url=url,
            posted_at=j.get("first_published") or j.get("updated_at"),
            description=_strip_html(j.get("content", "")),
            apply_options=[classify(url, "Greenhouse")],
        ))
    return jobs


def lever(client: httpx.Client, slug: str) -> list[Job]:
    r = client.get(f"https://api.lever.co/v0/postings/{slug}", params={"mode": "json"})
    r.raise_for_status()
    jobs = []
    for j in r.json():
        cats = j.get("categories") or {}
        created = j.get("createdAt")
        jobs.append(Job(
            job_id=f"lever_{slug}_{j['id']}",
            source="lever",
            company=slug,
            title=j["text"],
            location=cats.get("location", ""),
            remote=(j.get("workplaceType") == "remote") if j.get("workplaceType") else None,
            url=j["hostedUrl"],
            posted_at=datetime.fromtimestamp(created / 1000, UTC).isoformat() if created else None,
            description=j.get("descriptionPlain", ""),
            apply_options=[classify(j.get("applyUrl") or j["hostedUrl"], "Lever")],
        ))
    return jobs


def ashby(client: httpx.Client, slug: str) -> list[Job]:
    r = client.get(
        f"https://api.ashbyhq.com/posting-api/job-board/{slug}", params={"includeCompensation": "true"}
    )
    r.raise_for_status()
    jobs = []
    for j in r.json().get("jobs", []):
        jobs.append(Job(
            job_id=f"ashby_{slug}_{j['id']}",
            source="ashby",
            company=slug,
            title=j["title"],
            location=j.get("location", ""),
            remote=j.get("isRemote"),
            url=j["jobUrl"],
            posted_at=j.get("publishedAt"),
            description=j.get("descriptionPlain", ""),
            apply_options=[classify(j.get("applyUrl") or j["jobUrl"], "Ashby")],
        ))
    return jobs


ADAPTERS = {"greenhouse": greenhouse, "lever": lever, "ashby": ashby}


def resolve_board(client: httpx.Client, slug: str) -> str | None:
    """Try each board and return the first that answers with at least one job."""
    for name, adapter in ADAPTERS.items():
        try:
            if adapter(client, slug):
                return name
        except httpx.HTTPError:
            continue
    return None
