import json
from pathlib import Path

from jobagent.apply_links import classify
from jobagent.sources import jsearch

FIXTURES = Path(__file__).parent / "fixtures"


def _jobs():
    data = json.loads((FIXTURES / "jsearch_search.json").read_text())["data"]
    return [jsearch.parse(item) for item in data]


def test_jsearch_prefers_automatable_ats_over_linkedin():
    job = _jobs()[0]
    assert job.best_apply.board == "greenhouse"
    assert job.best_apply.automatable is True
    assert job.location == "Houston, TX"
    assert job.job_id == "jsearch_abc123=="


def test_jsearch_falls_back_to_employer_site_and_timestamp():
    job = _jobs()[1]
    assert job.best_apply.board == "employer"
    assert job.best_apply.automatable is False
    assert job.posted_at.startswith("2026-10-")


def test_linkedin_and_indeed_are_never_automatable():
    assert classify("https://www.linkedin.com/jobs/view/1").automatable is False
    assert classify("https://www.indeed.com/viewjob?jk=1").automatable is False
    assert classify("https://acme.wd5.myworkdayjobs.com/en-US/careers/job/1").board == "workday"


def test_ats_boards_are_automatable():
    for url in (
        "https://job-boards.greenhouse.io/acme/jobs/1",
        "https://jobs.lever.co/acme/abc",
        "https://jobs.ashbyhq.com/acme/abc",
    ):
        assert classify(url).automatable is True, url
