from functools import lru_cache
from urllib.parse import urlparse

import yaml

from jobagent import ROOT
from jobagent.models import ApplyOption

BOARD_HOSTS = {
    "greenhouse.io": "greenhouse",
    "lever.co": "lever",
    "ashbyhq.com": "ashby",
    "myworkdayjobs.com": "workday",
    "linkedin.com": "linkedin",
    "indeed.com": "indeed",
    "icims.com": "icims",
    "taleo.net": "taleo",
    "successfactors.com": "successfactors",
    "jobvite.com": "jobvite",
    "glassdoor.com": "glassdoor",
    "ziprecruiter.com": "ziprecruiter",
}


@lru_cache(maxsize=1)
def _automatable_hosts() -> tuple[str, ...]:
    config = yaml.safe_load((ROOT / "config" / "manual_ats.yaml").read_text())
    return tuple(config["automatable"])


def _host(url: str) -> str:
    return (urlparse(url).hostname or "").lower().removeprefix("www.")


def classify(url: str, publisher: str = "", employer_domain: str | None = None) -> ApplyOption:
    """Name the board behind an apply link and whether the submitter may automate it."""
    host = _host(url)
    board = next((name for suffix, name in BOARD_HOSTS.items() if host == suffix or host.endswith("." + suffix)), None)
    if board is None:
        board = "employer" if employer_domain and host.endswith(employer_domain) else "other"
    automatable = any(host == h or host.endswith("." + h) for h in _automatable_hosts())
    return ApplyOption(url=url, publisher=publisher or host, board=board, automatable=automatable)
