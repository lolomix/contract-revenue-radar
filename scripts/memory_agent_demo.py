#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from contract_radar.core import ContractRadar  # noqa: E402
from contract_radar.memory_agent import (  # noqa: E402
    build_memory_agent_result,
    load_memories,
    render_memory_agent_report,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a local MemoryAgent demo over Contract Revenue Radar findings."
    )
    parser.add_argument("contracts", nargs="+", type=Path, help="Text or Markdown contract files to audit.")
    parser.add_argument(
        "--memory",
        type=Path,
        default=REPO_ROOT / "samples" / "clause_memory.json",
        help="JSON file containing approved clause memories.",
    )
    parser.add_argument("--segment", default="", help="Optional business segment for memory matching.")
    parser.add_argument("--no-qdrant", action="store_true", help="Use deterministic fallback instead of Qdrant.")
    parser.add_argument("-o", "--output", type=Path, help="Write MemoryAgent report to this path.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    missing = [str(path) for path in [*args.contracts, args.memory] if not path.exists()]
    if missing:
        parser.error(f"Missing file(s): {', '.join(missing)}")

    radar = ContractRadar(prefer_qdrant=not args.no_qdrant)
    report = radar.audit_paths(args.contracts)
    memories = load_memories(args.memory)
    result = build_memory_agent_result(report, memories, segment=args.segment)
    markdown = render_memory_agent_report(result)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
    else:
        sys.stdout.write(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
