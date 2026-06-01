# Contract Revenue Radar

Contract Revenue Radar is a Qdrant-powered vector-search tool for finding contract clauses that delay cash, weaken renewals, or leak implementation margin.

It is built for the Qdrant **"Think Outside the Bot" Virtual Hackathon**. It is intentionally not a chatbot: the user runs a structured audit and receives source-linked findings, severity, business impact, and fallback positions.

## Demo Links

- Public repository: https://github.com/lolomix/contract-revenue-radar
- Demo video: https://github.com/lolomix/contract-revenue-radar/releases/download/qdrant-submission-2026/contract_revenue_radar_qdrant_demo_final.mp4
- Release assets: https://github.com/lolomix/contract-revenue-radar/releases/tag/qdrant-submission-2026
- Request a redacted sample audit: https://github.com/lolomix/contract-revenue-radar/issues/new/choose

## What It Does

- Splits Markdown/text contracts into sections.
- Embeds each section into a deterministic 96-dimensional vector.
- Uses Qdrant local in-memory mode (`QdrantClient(":memory:")`) as the primary vector-search backend.
- Searches for 7 revenue-risk classes:
  - payment delay,
  - renewal loss,
  - scope creep,
  - refund or credit exposure,
  - data/security blockers,
  - IP ownership traps,
  - auto-renewal fee escalation.
- Produces Markdown and optional DOCX reports.
- Generates an agent-style brief with priority questions and fallback positions.
- Includes an HTTP Agent API, an MCP-style stdio tool, and a local MemoryAgent prototype for approved fallback recall.

## Why This Uses Qdrant

Every audit indexes contract sections as Qdrant points and queries them by risk class. The tool creates a local in-memory Qdrant collection, upserts embedded sections, and retrieves the sections most relevant to each revenue-risk pattern.

The deterministic fallback backend exists only so tests and offline demos still run if `qdrant-client` is unavailable.

## Why It Is Not A Chatbot

The workflow is not open-ended Q&A. It is a deterministic audit:

1. Ingest contract files.
2. Chunk and vectorize sections.
3. Store/search sections in Qdrant.
4. Score and deduplicate findings.
5. Return a structured report and agent-ready brief.

The output is an operational review packet for sales, finance, delivery, and legal review.

## Quick Start

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e ".[qdrant]"
python -m unittest discover -s tests
./scripts/demo.sh
```

Fallback mode without Qdrant dependency:

```bash
PYTHONPATH=src python -m contract_radar.cli --no-qdrant samples/acme_services_agreement.md -o examples/reports/demo_report.md
```

## CLI Examples

Run a basic audit:

```bash
PYTHONPATH=src python -m contract_radar.cli samples/acme_services_agreement.md -o examples/reports/qdrant_demo_report.md
```

Append an agent brief:

```bash
PYTHONPATH=src python -m contract_radar.cli samples/saas_msa_example.md --agent-brief --no-qdrant -o examples/reports/agent_report.md
```

Export DOCX:

```bash
pip install -e ".[export]"
python -m contract_radar.cli samples/msp_retainer_agreement.md --format docx --docx-output examples/reports/report.docx --no-qdrant
```

Run the MemoryAgent prototype:

```bash
python scripts/memory_agent_demo.py samples/saas_msa_example.md \
  --memory samples/clause_memory.json \
  --segment "SaaS implementation" \
  --no-qdrant \
  -o examples/reports/memory_agent_report.md
```

Serve the local Agent API:

```bash
python scripts/serve_agent_api.py --port 8765
curl -s http://127.0.0.1:8765/audit -H 'Content-Type: application/json' -d @samples/api_request.json
```

Run the MCP-style tool call:

```bash
python scripts/mcp_contract_radar.py --call-once samples/mcp_tool_call.json
```

## Project Structure

```text
src/contract_radar/        Core audit engine, Qdrant backend, exports, agent workflow
scripts/                   CLI demo, HTTP API server, MCP-style tool, MemoryAgent demo
samples/                   Redacted/sample contracts and JSON requests
tests/                     Unit tests
examples/reports/          Generated example reports
demo_video/                MP4 demo and thumbnail
hackathon_submission/      Submission notes and judging brief
docs/                      Supporting docs
integrations/              Google Rapid Agent deployment and Agent Builder assets
```

## Business Review Requests

For a no-charge redacted sample audit or a fixed-scope Revenue Protection Sprint inquiry, use the GitHub issue templates:

```text
https://github.com/lolomix/contract-revenue-radar/issues/new/choose
```

Do not post confidential contracts, personal data, credentials, or private client documents in public issues. Use redacted excerpts or public-style samples only. See `docs/REVENUE_PROTECTION_SPRINT.md`.

## Google Rapid Agent Adaptation

This repo also includes deployable tool assets for a Google Cloud Rapid Agent submission:

```text
integrations/google_rapid_agent/
```

Contents:

- OpenAPI tool schema for Agent Builder.
- Cloud Run Dockerfile and deploy script.
- Agent Builder system instructions.
- MongoDB MCP memory schema for partner-track memory.
- Local smoke test.

The adaptation keeps Contract Revenue Radar as the audit tool, then lets Gemini/Agent Builder orchestrate audit, memory retrieval, human approval, and saved fallback preferences. See `integrations/google_rapid_agent/DEPLOYMENT_GUIDE.md`.

## Submission Compliance Review

| Requirement | Status | Evidence |
|---|---|---|
| Qdrant required | Met | `src/contract_radar/core.py` uses `qdrant-client` local memory mode when installed. |
| Not a chatbot | Met | CLI/API/MCP audit workflow returns structured findings, not chat responses. |
| GitHub repo | Met | https://github.com/lolomix/contract-revenue-radar |
| README | Met | This file. |
| Demo video <= 3 minutes | Met | `demo_video/contract_revenue_radar_qdrant_demo_final.mp4`; hosted in the release assets. |
| Code comments/basic docs | Met | Typed modules, README, API guide, sample requests, and tests. |
| Created during hackathon period | Evidence included | Git history in this repo starts May 29, 2026 and includes May 30-31 implementation commits. |
| Judging criteria | Addressed | Functionality, originality, and UX described in `hackathon_submission/WHY_THIS_WINS.md`. |

## Verification Snapshot

Latest verified local test run:

```text
Ran 9 tests in ~1.1s
OK
```

Latest publication commit before final cleanup:

```text
e9c7573 May 31 MemoryAgent prototype
```

Final cleanup commit keeps the repo focused on Qdrant submission essentials.

## Limitations

This is business-risk review, not legal advice. A qualified lawyer or contract professional should approve final contract language.
