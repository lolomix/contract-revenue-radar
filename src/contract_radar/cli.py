from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .core import ContractRadar, render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="contract-radar",
        description="Find contract clauses that delay cash, weaken renewals, or leak revenue.",
    )
    parser.add_argument("contracts", nargs="+", help="Text or Markdown contract files to audit.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write a Markdown report to this path. Defaults to stdout.",
    )
    parser.add_argument(
        "--no-qdrant",
        action="store_true",
        help="Use the built-in local vector fallback instead of Qdrant local mode.",
    )
    parser.add_argument(
        "--limit-per-risk",
        type=int,
        default=2,
        help="Maximum findings to show for each risk class.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    paths = [Path(path) for path in args.contracts]
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        parser.error(f"Missing contract file(s): {', '.join(missing)}")

    radar = ContractRadar(prefer_qdrant=not args.no_qdrant)
    report = radar.audit_paths(paths, limit_per_risk=args.limit_per_risk)
    markdown = render_markdown(report)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
    else:
        sys.stdout.write(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

