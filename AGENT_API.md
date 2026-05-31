# Contract Revenue Radar Agent API

This is a no-framework local API for Google Cloud/Qwen-style demos. The repo also includes a local MemoryAgent prototype for approved fallback recall.

## Run

```bash
.venv/bin/python scripts/serve_agent_api.py --port 8765
```

## Health Check

```bash
curl http://127.0.0.1:8765/health
```

## Audit Request

```bash
curl -s http://127.0.0.1:8765/audit \
  -H 'Content-Type: application/json' \
  -d @samples/api_request.json
```

## Response Shape

```json
{
  "backend": "qdrant-local-memory",
  "risk_score": 96,
  "searched_sections": 5,
  "findings": [],
  "agent_brief": {
    "executive_summary": "...",
    "priority_questions": [],
    "fallback_positions": [],
    "sales_ops_checklist": []
  },
  "markdown_report": "..."
}
```

Verified sample response:

```text
samples/api_response.json
```

## Hackathon Adaptation

- Google Cloud Rapid Agent: wrap `/audit` as the contract-audit tool in a Gemini/Agent Builder workflow.
- Qwen Cloud: use `/audit` as an Autopilot Agent tool, then let the model ask follow-up business questions and remember accepted fallback positions.
- MemoryAgent prototype: run `scripts/memory_agent_demo.py` with `samples/clause_memory.json` to show active memory recall by risk type and segment before wiring persistent cloud storage.

This API is for redacted documents or templates. It is business-risk review, not legal advice.

## MCP-Style Tool Server

For agent builders that prefer tool calling over HTTP, the repository includes a minimal JSON-RPC stdio server with an MCP-compatible shape:

```bash
.venv/bin/python scripts/mcp_contract_radar.py --call-once samples/mcp_tool_call.json
```

Tool name:

```text
audit_contract_revenue_terms
```

Supported methods:

- `initialize`
- `tools/list`
- `tools/call`

The tool returns structured audit data, an agent brief, and a Markdown report. This is intentionally dependency-light so it can be wrapped by Google Cloud Agent Builder, a partner MCP server flow, or a Qwen-style Autopilot Agent without changing the core audit engine.

## May 30 2026 Updates (Final Submission Session)
- Now exposes 7 risk classes (added IP ownership trap + auto-renewal fee escalation).
- New endpoints on the HTTP server: `/risk-classes` and `/capabilities` (see serve_agent_api.py).
- DOCX export available via CLI (and flagged in API responses).
- Enhanced scoring in fallback/Qdrant path.
- Fresh samples + docs. Full Session Notes in main README.

## May 31 2026 MemoryAgent Prototype

```bash
.venv/bin/python scripts/memory_agent_demo.py samples/saas_msa_example.md \
  --memory samples/clause_memory.json \
  --segment "SaaS implementation" \
  --no-qdrant \
  -o examples/reports/memory_agent_report.md
```

This produces a review packet that combines the audit findings, the agent brief, and approved memories such as Net 15 payment fallback, background-IP carveout, and renewal fee cap. Inactive memories are ignored.
