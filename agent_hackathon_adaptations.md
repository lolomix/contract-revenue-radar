# Agent Hackathon Adaptations

The Qdrant submission is the immediate prize path. The same codebase can also be adapted for Google Cloud Rapid Agent Hackathon and Qwen Cloud Global AI Hackathon.

## Revenue Terms Agent

Agent objective:

1. Receive redacted SOWs, MSAs, proposals, order forms, or implementation agreements.
2. Run Contract Revenue Radar.
3. Produce a business-risk report.
4. Produce a Revenue Terms Agent Brief with:
   - executive summary,
   - priority questions,
   - fallback positions,
   - sales/ops checklist.
5. Route the brief to the right business owner before legal review.

## Current Local Demo

```bash
PYTHONPATH=src python -m contract_radar.cli samples/acme_services_agreement.md --agent-brief -o agent_report.md
```

## Google Cloud Rapid Agent Hackathon Fit

Build a hosted agent using Gemini and Google Cloud Agent Builder:

- Tool 1: upload or paste redacted contract text.
- Tool 2: call the Contract Revenue Radar audit engine.
- Tool 3: generate fallback positions and checklist.
- Tool 4: send the brief to a CRM, Drive folder, or partner MCP destination.

Submission angle:

"An agent that converts contract templates into a pre-legal revenue-risk workflow for SaaS implementers and RevOps teams."

## Qwen Cloud Hackathon Fit

Best tracks:

- Autopilot Agent: autonomously triages a SOW, asks missing business questions, and generates fallback positions.
- MemoryAgent: remembers approved fallback positions and flags deviations in future contracts.

Submission angle:

"A production-style agent for implementation teams that remembers clause preferences and routes risky SOW terms before signature."

## Minimal Hosted MVP

- HTTP endpoint: `/audit` from `scripts/serve_agent_api.py`
- Input: contract text or uploaded Markdown.
- Output: report plus agent brief.
- Persistence: store approved fallback preferences by buyer/team.
- Demo: use the included `samples/acme_services_agreement.md`.

Local run:

```bash
.venv/bin/python scripts/serve_agent_api.py --port 8765
curl -s http://127.0.0.1:8765/audit -H 'Content-Type: application/json' -d @samples/api_request.json
```
