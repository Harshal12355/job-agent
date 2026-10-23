import json

import yaml
from mcp.server.mcpserver import MCPServer

from jobagent import ROOT, fetch
from jobagent.apply_links import classify
from jobagent.http import client
from jobagent.render import check_pdf, render_resume
from jobagent.sources import jsearch

mcp = MCPServer("jobagent")


def _load(name: str) -> dict:
    return yaml.safe_load((ROOT / "profile" / name).read_text())


@mcp.tool()
def list_facts(lane: str = "A") -> dict:
    """Confirmed facts the agent may use for a lane (A or B). needs_review facts are excluded."""
    work = _load("work.yaml")
    projects = _load("projects.yaml")
    jobs = [
        {
            "company": job["company"],
            "title": job["title"],
            "start": job["start"],
            "end": job["end"],
            "bullets": [b for b in job["bullets"] if b.get("status") == "confirmed"],
        }
        for job in work["experience"]
    ]
    projs = [
        {**p, "bullets": [b for b in p["bullets"] if b.get("status") == "confirmed"]}
        for p in projects["projects"]
        if lane in p.get("lanes", [])
    ]
    return {"experience": jobs, "projects": projs, "education": _load("education.yaml")["education"]}


@mcp.tool()
def render_packet(packet_path: str, out_dir: str) -> dict:
    """Render a tailored packet to PDF and run the ATS text round-trip check."""
    packet = ROOT / packet_path
    pdf = render_resume(packet, ROOT / out_dir)
    result = check_pdf(pdf, packet)
    return {"pdf": str(pdf.relative_to(ROOT)), "ok": result.ok, "errors": result.errors}


@mcp.tool()
def check_rendered_pdf(pdf_path: str, packet_path: str) -> dict:
    """ATS round-trip check: under 2.5 MB and every bullet extracts as text in order."""
    result = check_pdf(ROOT / pdf_path, ROOT / packet_path)
    return {"ok": result.ok, "errors": result.errors}


@mcp.tool()
def search_jobs(query: str, date_posted: str = "3days", remote_only: bool = False) -> dict:
    """Ad-hoc JSearch query (one request credit). Returns jobs with their best apply link.
    Does not save or log; the scheduled `jobagent fetch` does that."""
    used = fetch.jsearch_requests_this_month()
    budget = fetch._config()["jsearch"]["monthly_budget"]
    if used >= budget:
        return {"error": f"JSearch budget used: {used}/{budget} this month"}
    try:
        with client() as http:
            jobs = jsearch.search(http, query, date_posted=date_posted, remote_only=remote_only)
    except RuntimeError as err:
        return {"error": str(err)}
    return {
        "credits_used_this_month": used + 1,
        "jobs": [
            {k: v for k, v in j.to_dict().items() if k != "description"} | {"description": j.description[:500]}
            for j in jobs
        ],
    }


@mcp.tool()
def resolve_apply_link(url: str) -> dict:
    """Which board an apply link belongs to and whether the submitter may automate it."""
    option = classify(url)
    return {"board": option.board, "automatable": option.automatable, "url": option.url}


@mcp.tool()
def list_found_jobs(limit: int = 50, automatable_only: bool = False) -> list[dict]:
    """Most recent saved jobs (title, company, best apply link), newest file first."""
    paths = sorted((ROOT / "data" / "jobs").glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    out = []
    for path in paths:
        job = json.loads(path.read_text())
        best = job.get("best_apply") or {}
        if automatable_only and not best.get("automatable"):
            continue
        out.append({
            "job_id": job["job_id"], "company": job["company"], "title": job["title"],
            "location": job["location"], "posted_at": job["posted_at"],
            "board": best.get("board"), "apply_url": best.get("url"),
        })
        if len(out) >= limit:
            break
    return out


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
