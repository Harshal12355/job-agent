"""JSearch (OpenWeb Ninja): Google for Jobs listings, including postings that originate on
LinkedIn, Indeed, Glassdoor, and ZipRecruiter. Each returned page (10 jobs) costs one request credit."""

import os
from datetime import UTC, datetime
from urllib.parse import urlparse

import httpx

from jobagent.apply_links import classify
from jobagent.models import Job

OPENWEBNINJA_URL = "https://api.openwebninja.com/jsearch/search"
RAPIDAPI_URL = "https://jsearch.p.rapidapi.com/search"
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"


def _request_target() -> tuple[str, dict[str, str]]:
    if key := os.environ.get("OPENWEBNINJA_API_KEY"):
        return OPENWEBNINJA_URL, {"x-api-key": key}
    if key := os.environ.get("RAPIDAPI_KEY"):
        return RAPIDAPI_URL, {"X-RapidAPI-Key": key, "X-RapidAPI-Host": RAPIDAPI_HOST}
    raise RuntimeError("Set OPENWEBNINJA_API_KEY or RAPIDAPI_KEY in .env")


def search(
    client: httpx.Client,
    query: str,
    *,
    date_posted: str = "3days",
    num_pages: int = 1,
    remote_only: bool = False,
    under_3_years: bool = True,
) -> list[Job]:
    url, headers = _request_target()
    params: dict[str, str | int] = {
        "query": query,
        "country": "us",
        "date_posted": date_posted,
        "num_pages": num_pages,
        "employment_types": "FULLTIME",
    }
    if remote_only:
        params["work_from_home"] = "true"
    if under_3_years:
        params["job_requirements"] = "under_3_years_experience,no_experience"
    response = client.get(url, params=params, headers=headers)
    response.raise_for_status()
    return [parse(item) for item in response.json().get("data", [])]


def parse(item: dict) -> Job:
    employer_domain = (urlparse(item.get("employer_website") or "").hostname or "").removeprefix("www.") or None
    options = [
        classify(o["apply_link"], o.get("publisher", ""), employer_domain)
        for o in item.get("apply_options") or []
        if o.get("apply_link")
    ]
    if not options and item.get("job_apply_link"):
        options = [classify(item["job_apply_link"], item.get("job_publisher", ""), employer_domain)]

    posted = item.get("job_posted_at_datetime_utc")
    if not posted and item.get("job_posted_at_timestamp"):
        posted = datetime.fromtimestamp(item["job_posted_at_timestamp"], UTC).isoformat()

    location = ", ".join(p for p in (item.get("job_city"), item.get("job_state")) if p) or item.get(
        "job_location", ""
    )
    return Job(
        job_id=f"jsearch_{item['job_id']}",
        source="jsearch",
        company=item.get("employer_name", ""),
        title=item.get("job_title", ""),
        location=location,
        remote=item.get("job_is_remote"),
        url=item.get("job_google_link") or item.get("job_apply_link", ""),
        posted_at=posted,
        description=item.get("job_description", ""),
        apply_options=options,
        salary_min=item.get("job_min_salary"),
        salary_max=item.get("job_max_salary"),
    )
