import argparse
import sys
from pathlib import Path

from jobagent import fetch
from jobagent.render import check_pdf, render_resume

NOT_BUILT = {
    "filter": 1, "validate": 2, "queue": 2, "log": 2,
    "dashboard": 3, "notify": 4, "run": 4,
}


def _render(args: argparse.Namespace) -> int:
    pdf = render_resume(Path(args.packet), Path(args.out))
    result = check_pdf(pdf, Path(args.packet))
    print(pdf)
    for err in result.errors:
        print(f"FAIL {err}", file=sys.stderr)
    return 0 if result.ok else 1


def _check_pdf(args: argparse.Namespace) -> int:
    result = check_pdf(Path(args.pdf), Path(args.packet))
    for err in result.errors:
        print(f"FAIL {err}", file=sys.stderr)
    if result.ok:
        print("OK: size under limit, every bullet extracts as text in order")
    return 0 if result.ok else 1


def _fetch(args: argparse.Namespace) -> int:
    print(fetch.run(args.source))
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(prog="jobagent")
    sub = parser.add_subparsers(dest="command", required=True)

    fetch_cmd = sub.add_parser("fetch", help="Pull new jobs from JSearch and company ATS boards")
    fetch_cmd.add_argument("--source", nargs="+", choices=["jsearch", "ats"], default=["jsearch", "ats"])
    fetch_cmd.set_defaults(func=_fetch)

    render = sub.add_parser("render", help="Render a resume packet to PDF and run the ATS text check")
    render.add_argument("packet")
    render.add_argument("--out", default="out/base")
    render.set_defaults(func=_render)

    check = sub.add_parser("check-pdf", help="ATS round-trip check on a rendered PDF")
    check.add_argument("pdf")
    check.add_argument("packet")
    check.set_defaults(func=_check_pdf)

    for name, phase in NOT_BUILT.items():
        stub = sub.add_parser(name, help=f"Built in phase {phase}")
        stub.add_argument("rest", nargs=argparse.REMAINDER)
        stub.set_defaults(func=lambda a, n=name, p=phase: _not_built(n, p))

    args = parser.parse_args()
    sys.exit(args.func(args))


def _not_built(name: str, phase: int) -> int:
    print(f"`jobagent {name}` is built in phase {phase} (see PLAN.md section 8).", file=sys.stderr)
    return 2


if __name__ == "__main__":
    main()
