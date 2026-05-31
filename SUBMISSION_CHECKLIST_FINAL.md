# Qdrant Submission Checklist

Current status: build package is ready locally. The remaining work requires external account actions: GitHub repository upload, demo-video hosting, and final form submission.

Deadline: June 1, 2026 at 11:59 PM Pacific Time.

Official page: https://try.qdrant.tech/hackathon-vsd

## Prepared Assets

- Project directory: `/home/ubuntu/revenue_5000/qdrant-contract-radar`
- Submission archive: `/home/ubuntu/revenue_5000/contract-revenue-radar-submission.zip` (re-prep after May 30 changes)
- Canonical archive note: `/home/ubuntu/revenue_5000/CANONICAL_ARCHIVES.md`
- Demo video: `/home/ubuntu/revenue_5000/qdrant-contract-radar/demo_video/contract_revenue_radar_qdrant_demo.mp4`
- Form answers: `/home/ubuntu/revenue_5000/qdrant-contract-radar/SUBMISSION_FORM_ANSWERS.md`
- Hackathon brief: `/home/ubuntu/revenue_5000/qdrant-contract-radar/HACKATHON_SUBMISSION.md`
- API guide: `/home/ubuntu/revenue_5000/qdrant-contract-radar/AGENT_API.md`
- Sample report: `/home/ubuntu/revenue_5000/qdrant-contract-radar/agent_report.md`
- Sample DOCX note: `/home/ubuntu/revenue_5000/qdrant-contract-radar/SAMPLE_DOCX_NOTE.md`
- License: `/home/ubuntu/revenue_5000/qdrant-contract-radar/LICENSE`
- GitHub publishing checklist: `/home/ubuntu/revenue_5000/qdrant-contract-radar/GITHUB_PUBLISHING_CHECKLIST.md`
- **New May 30:** `hackathon_submission/` folder (Why This Wins + final assets), DOCX export, 2 new samples, 7 risk detectors.

## Before Submitting

1. Create a GitHub repository for the project.
2. Push the contents of `/home/ubuntu/revenue_5000/qdrant-contract-radar`.
3. Confirm the repository includes `README.md`, `LICENSE`, `AGENT_API.md`, `HACKATHON_SUBMISSION.md`, `src/`, `tests/`, `scripts/`, `samples/`, and the demo-video path or a hosted video link.
4. Upload `demo_video/contract_revenue_radar_qdrant_demo.mp4` to Loom, YouTube, Google Drive, Dropbox, or another shareable host.
5. Confirm the video link is publicly viewable or viewable by Qdrant organizers.
6. Open `SUBMISSION_FORM_ANSWERS.md` and paste the answers into the Qdrant submission form.
7. Submit before June 1, 2026 at 11:59 PM PT.

## Required Submission Fields

- Project name: Contract Revenue Radar
- Repository URL: paste the GitHub repo URL after upload.
- Demo video URL: paste the hosted video URL after upload.
- Project description: use the concise description from `SUBMISSION_FORM_ANSWERS.md`.
- Qdrant usage: explain that the app embeds contract clauses, stores them in a Qdrant local-memory collection, performs vector search over risk patterns, and returns business-risk findings plus an agent brief.

## Verification Commands

Run these from `/home/ubuntu/revenue_5000/qdrant-contract-radar` before pushing (May 30 final):

```bash
.venv/bin/python -m unittest discover -s tests   # now 7 tests, including new IP/renewal_fee on fresh samples
./scripts/demo.sh
.venv/bin/python scripts/serve_agent_api.py --port 8765
```

In a second terminal while the API server is running (new endpoints available):

```bash
curl -s http://127.0.0.1:8765/audit \
  -H 'Content-Type: application/json' \
  -d @samples/api_request.json

curl -s http://127.0.0.1:8765/risk-classes   # shows all 7 detectors + docx flag
curl -s http://127.0.0.1:8765/capabilities  # includes May 30 new-in-session note
```

Expected API result: `backend` should be `qdrant-local-memory`, the report should include findings (5+ on original), new detectors on saas_msp samples, and the agent brief should include fallback positions plus a contract-ops checklist. DOCX support flag visible.

## Session Notes (May 30 2026)
This checklist + all docs were updated live today with substantial new code. See README.md "Session Notes" and hackathon_submission/ for details proving work performed during the final window.
