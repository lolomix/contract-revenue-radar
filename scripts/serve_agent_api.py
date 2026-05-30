#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
import tempfile
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from contract_radar.agent_workflow import build_agent_brief  # noqa: E402
from contract_radar.core import RISK_PATTERNS, AuditFinding, ContractRadar, render_markdown  # noqa: E402
from contract_radar.export import has_docx_support  # noqa: E402


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


class AgentHandler(BaseHTTPRequestHandler):
    server_version = "ContractRevenueRadar/0.1"

    def do_GET(self) -> None:
        if self.path == "/health":
            self.write_json({"status": "ok", "service": "contract-revenue-radar", "version": "0.2.0-hackathon-may30"})
            return
        if self.path == "/risk-classes":
            classes = []
            for key, val in RISK_PATTERNS.items():
                classes.append({
                    "risk_type": key,
                    "label": val["label"],
                    "severity": val["severity"],
                    "example_terms": val["terms"][:3],
                    "why": val["why"][:120] + "...",
                })
            self.write_json({
                "risk_classes": classes,
                "total": len(classes),
                "docx_export_available": has_docx_support(),
                "note": "Use POST /audit for full structured audit + agent brief. Supports ?format=docx via CLI."
            })
            return
        if self.path == "/capabilities":
            self.write_json({
                "service": "Contract Revenue Radar Agent API (May 30 2026 final)",
                "features": [
                    "7 revenue risk detectors (payment, renewal, scope, credits, security, IP ownership, auto-renewal fees)",
                    "Qdrant local-memory + robust local-hash fallback with improved keyword+phrase boosting",
                    "Structured findings + Agent Brief with fallback positions and ops checklist",
                    "Markdown and professional DOCX export (optional python-docx)",
                    "MCP stdio tool compatible (scripts/mcp_contract_radar.py)"
                ],
                "endpoints": {
                    "GET /health": "liveness",
                    "GET /risk-classes": "list current detectors + export capability flag",
                    "GET /capabilities": "this document",
                    "POST /audit": "primary: {text, filename?, no_qdrant?} -> full report + brief"
                },
                "new_in_session": "IP ownership trap + auto-renewal fee escalation detectors; DOCX export; 2 new samples; enhanced vector scoring; hackathon_submission assets"
            })
            return
        self.write_json(
            {
                "service": "Contract Revenue Radar Agent API",
                "routes": {
                    "GET /health": "health check",
                    "GET /risk-classes": "current revenue risk detectors (new May 30)",
                    "GET /capabilities": "feature and endpoint summary",
                    "POST /audit": "JSON body with text, filename, no_qdrant. Returns findings, agent_brief, markdown_report.",
                },
                "hint": "See AGENT_API.md and samples/api_request.json. New risk classes added during final submission prep.",
            }
        )

    def do_POST(self) -> None:
        if self.path != "/audit":
            self.write_json({"error": "not found"}, status=404)
            return

        try:
            payload = self.read_json()
            text = str(payload.get("text", "")).strip()
            if not text:
                self.write_json({"error": "missing non-empty text"}, status=400)
                return
            filename = str(payload.get("filename", "submitted_contract.md"))
            no_qdrant = bool(payload.get("no_qdrant", False))
            response = audit_text(text, filename=filename, prefer_qdrant=not no_qdrant)
            self.write_json(response)
        except Exception as exc:  # pragma: no cover - defensive server boundary
            self.write_json({"error": str(exc)}, status=500)

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def write_json(self, payload: dict[str, Any], status: int = 200) -> None:
        data = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: Any) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), format % args))


def audit_text(text: str, filename: str, prefer_qdrant: bool = True) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmpdir:
        safe_name = Path(filename).name or "submitted_contract.md"
        path = Path(tmpdir) / safe_name
        path.write_text(text, encoding="utf-8")
        radar = ContractRadar(prefer_qdrant=prefer_qdrant)
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve Contract Revenue Radar Agent API.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), AgentHandler)
    print(f"serving http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

