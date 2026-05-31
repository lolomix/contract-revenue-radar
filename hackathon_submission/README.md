# Contract Revenue Radar — Qdrant Hackathon Submission (Final)

**Project:** Contract Revenue Radar  
**Date prepared:** May 30, 2026 (final polish session with substantial new code)  
**Deadline:** June 1, 2026 11:59 PM PT

## Assets in this folder
- `WHY_THIS_WINS.md` — one-page brief for judges (strongest summary of criteria fit + live work proof)
- `SUBMISSION_FORM_ANSWERS.md` — ready-to-paste answers
- `VIDEO_LINK.txt` — placeholder for hosted demo video URL
- `FINAL_SUMMARY_AND_CHECKLIST.md` — current public links, verification commands, and form checklist

## Quick Start (from repo root)
```bash
.venv/bin/python -m unittest discover -s tests
./scripts/demo.sh
.venv/bin/python -m contract_radar.cli samples/saas_msa_example.md --agent-brief --format docx --docx-output /tmp/demo_report.docx
```

New in this submission prep session (May 30):
- 7 risk detectors total (added IP ownership trap + auto-renewal fee escalation)
- Professional DOCX export via CLI
- 2 fresh diverse samples (SaaS MSA, MSP retainer)
- Enhanced vector fallback scoring
- Improved Agent API (new /risk-classes + /capabilities)
- Full docs refresh + this hackathon_submission/ bundle

## Repository Contents (all included)
src/, tests/, scripts/, samples/ (4 contracts), examples/reports/, demo_video/, AGENT_API.md, etc.

## Qdrant Usage
Primary: qdrant-client with :memory: mode. Collection per audit, 96-d vectors from hash embedding + hybrid keyword boost. Full source in core.py:_QdrantBackend.

This submission is 100% reproducible offline with fallback.

## Contact / Links
- Demo video: see VIDEO_LINK.txt (upload to Loom/YouTube before submit)
- Full repo to be pushed to GitHub (see `FINAL_SUMMARY_AND_CHECKLIST.md` and `../GITHUB_PUBLISHING_CHECKLIST.md`)
- Monetization: sell as $1.5k–$5k Revenue Terms Audits

**This wins because it is useful, original, complete, and ships with real revenue potential.**
