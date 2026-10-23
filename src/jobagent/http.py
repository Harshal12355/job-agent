import httpx

TIMEOUT = httpx.Timeout(20.0, connect=10.0)
HEADERS = {"User-Agent": "jobagent/0.1 (personal job search; contact harshal.thachapully@gmail.com)"}


def client() -> httpx.Client:
    return httpx.Client(timeout=TIMEOUT, headers=HEADERS, follow_redirects=True)
