from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .agent_workflow import build_agent_brief, render_agent_brief
from .core import ContractRadar, render_markdown
from .export import export_report, has_docx_support


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
    parser.add_argument(
        "--agent-brief",
        action="store_true",
        help="Append an agent-style business brief with fallback positions and checklist.",
    )
    parser.add_argument(
        "--format",
        choices=["md", "docx"],
        default="md",
        help="Output format for the report (md or docx). Requires python-docx for 'docx'.",
    )
    parser.add_argument(
        "--docx-output",
        type=Path,
        help="When set, also export a professional .docx version to this path (or derived from --output).",
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

    # Primary output (md always available)
    markdown = render_markdown(report)
    if args.agent_brief:
        markdown += "\n" + render_agent_brief(build_agent_brief(report))

    # Determine primary output path and write
    primary_path: Path | None = args.output
    if primary_path:
        primary_path.parent.mkdir(parents=True, exist_ok=True)
        primary_path.write_text(markdown, encoding="utf-8")
    else:
        sys.stdout.write(markdown)

    # Handle --format docx for primary output (overrides md if chosen and no separate --docx-output)
    if args.format == "docx":
        if primary_path is None:
            primary_path = Path("report.docx")
        try:
            export_path = export_report(report, primary_path, format="docx")
            if not args.output and not args.docx_output:
                print(f"\n[export] Wrote DOCX report to {export_path}", file=sys.stderr)
        except ImportError as e:
            parser.error(str(e))

    # Optional separate --docx-output (always produces a docx regardless of --format)
    if args.docx_output:
        try:
            docx_path = export_report(report, args.docx_output, format="docx")
            print(f"[export] Professional DOCX written to {docx_path}", file=sys.stderr)
        except ImportError as e:
            parser.error(str(e))

    # Helpful hint if docx requested but support missing (non-fatal for md path)
    if (args.format == "docx" or args.docx_output) and not has_docx_support() and args.format != "docx":
        print(
            "[hint] python-docx not installed. DOCX export unavailable. "
            "Install with: pip install '.[export]'",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
