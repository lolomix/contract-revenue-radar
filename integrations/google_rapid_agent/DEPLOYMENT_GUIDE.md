# Deployment Guide

This package turns Contract Revenue Radar into the hosted audit tool for Google Cloud Agent Builder.

## Local Smoke Test

From the repo root:

```bash
cd /home/ubuntu/revenue_5000/qdrant-contract-radar
.venv/bin/python scripts/serve_agent_api.py --host 127.0.0.1 --port 8765
```

In another terminal:

```bash
cd /home/ubuntu/revenue_5000
bash google_rapid_agent_submission/deploy/local_smoke_test.sh
```

## Cloud Run Deploy

Prerequisites:

- Google Cloud project.
- `gcloud` authenticated.
- Docker available.
- Billing enabled for Cloud Run.

Deploy:

```bash
cd /home/ubuntu/revenue_5000
PROJECT_ID=your-google-cloud-project-id \
REGION=us-central1 \
bash google_rapid_agent_submission/deploy/deploy_cloud_run.sh
```

The script prints the Cloud Run URL. Replace `https://YOUR_CLOUD_RUN_URL` in:

```text
google_rapid_agent_submission/openapi/revenue_terms_agent_openapi.yaml
```

Then import that OpenAPI file as an Agent Builder tool.

## Agent Builder Setup

1. Create a new Google Cloud Agent Builder agent.
2. Use Gemini as the reasoning model.
3. Import `openapi/revenue_terms_agent_openapi.yaml` as the contract-audit tool.
4. Add the instructions from `agent_builder/SYSTEM_INSTRUCTIONS.md`.
5. Configure selected partner MCP server, recommended MongoDB MCP.
6. Use `agent_builder/MONGODB_MCP_MEMORY_SCHEMA.md` for memory collections.
7. Test a redacted SOW sample.
8. Record a 3-minute demo showing:
   - audit tool call,
   - partner memory retrieval,
   - human approval,
   - saved fallback preference,
   - final review packet.

## Submission URLs To Fill Later

```text
Hosted URL:
Public repo URL:
Demo video URL:
Devpost URL:
```
