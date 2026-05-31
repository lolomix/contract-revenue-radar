# GitHub Publishing Checklist

Use this before any hackathon or marketplace submission that requires a public repository.

## Required External Actions

1. Create a new public GitHub repository named `contract-revenue-radar`.
2. Push this project directory to the new repository.
3. Upload `demo_video/contract_revenue_radar_qdrant_demo.mp4` to Loom, YouTube unlisted, Google Drive, or Dropbox.
4. Replace `hackathon_submission/VIDEO_LINK.txt` with the hosted video URL.
5. Submit the Qdrant form at https://try.qdrant.tech/hackathon-vsd before June 1, 2026 at 11:59 PM PT.

## Local Verification

Run from `/home/ubuntu/revenue_5000/qdrant-contract-radar`:

```bash
.venv/bin/python -m unittest discover -s tests
./scripts/demo.sh
.venv/bin/python -m contract_radar.cli samples/saas_msa_example.md --agent-brief --format docx --docx-output /tmp/verify_report.docx
.venv/bin/python scripts/mcp_contract_radar.py --call-once samples/mcp_tool_call.json
```

Expected state:

- Tests pass.
- Demo report uses `qdrant-local-memory` when the optional Qdrant dependency is installed.
- DOCX output is generated.
- MCP-style tool call returns structured audit content.
- `LICENSE` is present and uses MIT terms.

## Repository Contents To Confirm

- `README.md`
- `LICENSE`
- `src/`
- `tests/`
- `scripts/`
- `samples/`
- `AGENT_API.md`
- `HACKATHON_SUBMISSION.md`
- `SUBMISSION_FORM_ANSWERS.md`
- `SUBMISSION_CHECKLIST_FINAL.md`
- `hackathon_submission/`
- `demo_video/contract_revenue_radar_qdrant_demo.mp4` or a hosted video URL

## Git Commands

```bash
cd /home/ubuntu/revenue_5000/qdrant-contract-radar
git status --short
git remote add origin https://github.com/YOUR_USERNAME/contract-revenue-radar.git
git branch -M main
git push -u origin main
```

If `origin` already exists, replace it intentionally:

```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/contract-revenue-radar.git
```

Do not push credentials, `.venv`, local scratch files, or private client documents.
