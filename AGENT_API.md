# Contract Revenue Radar Agent API

This is a no-framework local API for Google Cloud/Qwen-style demos.

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

This API is for redacted documents or templates. It is business-risk review, not legal advice.
