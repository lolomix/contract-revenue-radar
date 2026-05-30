#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from contract_radar.agent_workflow import build_agent_brief  # noqa: E402
from contract_radar.core import AuditFinding, ContractRadar, render_markdown  # noqa: E402


TOOL_SCHEMA = {
    "name": "audit_contract_revenue_terms",
    "description": (
        "Audit a redacted contract, SOW, MSA, proposal, or order form for business "
        "terms that can delay cash, weaken renewals, expand scope, create refund "
        "exposure, or block signature through security/data obligations."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "Redacted contract text in plain text or Markdown.",
            },
            "filename": {
                "type": "string",
                "description": "Optional display filename for report citations.",
                "default": "submitted_contract.md",
            },
            "no_qdrant": {
                "type": "boolean",
                "description": "Use the built-in local fallback instead of Qdrant local-memory mode.",
                "default": False,
            },
        },
        "required": ["text"],
    },
}


def finding_to_dict(finding: AuditFinding) -> dict[str, Any]:
    return {
        "risk_type": finding.risk_type,
        "label": finding.label,
        "severity": finding.severity,
        "score": finding.score,
        "source": finding.source,
        "heading": finding.heading,
        "excerpt": finding.excerpt,
        "why": finding.why,
        "action": finding.action,
        "matched_terms": list(finding.matched_terms),
    }


def audit_contract_text(text: str, filename: str = "submitted_contract.md", no_qdrant: bool = False) -> dict[str, Any]:
    text = text.strip()
    if not text:
        raise ValueError("text is required")

    with tempfile.TemporaryDirectory() as tmpdir:
        safe_name = Path(filename).name or "submitted_contract.md"
        path = Path(tmpdir) / safe_name
        path.write_text(text, encoding="utf-8")

        radar = ContractRadar(prefer_qdrant=not no_qdrant)
        report = radar.audit_paths([path])
        brief = build_agent_brief(report)
        return {
            "backend": report.backend,
            "risk_score": report.risk_score,
            "searched_sections": report.searched_sections,
            "findings": [finding_to_dict(finding) for finding in report.findings],
            "agent_brief": {
                "executive_summary": brief.executive_summary,
                "priority_questions": list(brief.priority_questions),
                "fallback_positions": list(brief.fallback_positions),
                "sales_ops_checklist": list(brief.sales_ops_checklist),
            },
            "markdown_report": render_markdown(report),
        }


def handle_request(request: dict[str, Any]) -> dict[str, Any] | None:
    request_id = request.get("id")
    method = request.get("method")
    params = request.get("params") or {}

    try:
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {
                        "name": "contract-revenue-radar",
                        "version": "0.1.0",
                    },
                    "capabilities": {"tools": {}},
                },
            }

        if method == "notifications/initialized":
            return None

        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"tools": [TOOL_SCHEMA]},
            }

        if method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments") or {}
            if name != TOOL_SCHEMA["name"]:
                raise ValueError(f"unknown tool: {name}")
            result = audit_contract_text(
                text=str(arguments.get("text", "")),
                filename=str(arguments.get("filename", "submitted_contract.md")),
                no_qdrant=bool(arguments.get("no_qdrant", False)),
            )
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2),
                        }
                    ],
                    "structuredContent": result,
                    "isError": False,
                },
            }

        raise ValueError(f"unsupported method: {method}")
    except Exception as exc:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32000,
                "message": str(exc),
            },
        }


def serve_stdio() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        response = handle_request(json.loads(line))
        if response is not None:
            sys.stdout.write(json.dumps(response, separators=(",", ":")) + "\n")
            sys.stdout.flush()
    return 0


def call_once(payload: dict[str, Any]) -> int:
    response = handle_request(payload)
    if response is not None:
        print(json.dumps(response, indent=2))
    return 0 if "error" not in (response or {}) else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Contract Revenue Radar as a minimal MCP-style stdio tool server.")
    parser.add_argument(
        "--call-once",
        type=Path,
        help="Read one JSON-RPC request from a file and print the response, useful for demos/tests.",
    )
    args = parser.parse_args()

    if args.call_once:
        return call_once(json.loads(args.call_once.read_text(encoding="utf-8")))
    return serve_stdio()


if __name__ == "__main__":
    raise SystemExit(main())
