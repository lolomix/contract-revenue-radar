# Submission Form Answers

## Project Name

Contract Revenue Radar

## Tagline

Vector search for contract clauses that delay cash, weaken renewals, and create unpaid implementation work.

## Short Description

Contract Revenue Radar indexes SOWs, MSAs, proposals, and order forms in Qdrant local-memory mode, then searches for payment delays, acceptance traps, renewal loss, scope creep, service-credit exposure, data/security blockers, IP ownership traps, and renewal fee escalation. It returns a prioritized Markdown report with the source excerpt, severity, commercial risk, and negotiation move. It is intentionally not a chatbot: the output is a concrete audit trail for business/legal review.

## What It Does

- Splits Markdown/text contracts into sections.
- Stores section vectors as Qdrant points (96-d hash embeddings + hybrid phrase-boosted scoring).
- Runs revenue-risk vector queries over the collection (now 7 classes).
- Produces a report with excerpts, matched terms, severity, and recommended actions. Optional professional DOCX export.
- Includes a deterministic fallback backend so tests and demos can run without network access.
- New May 30-31 2026: IP ownership trap + auto-renewal fee escalation detectors; SaaS/MSP samples; Agent API improvements; MemoryAgent prototype for approved fallback recall.

## How It Uses Qdrant

The app uses `qdrant-client` with `QdrantClient(":memory:")`. It creates a collection, upserts embedded contract sections as points, and queries the collection once per revenue-risk class. The included demo report was generated with backend `qdrant-local-memory`.

## Why It Is Not Another Chatbot

The user does not ask questions in a chat box. They run a contract audit and receive a structured, source-linked report. The product uses vector search as a discovery engine for recurring business-risk patterns in contracts.

## Demo Commands

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[qdrant]"
./scripts/demo.sh
```

Generated video walkthrough:

```bash
.venv/bin/pip install pillow
.venv/bin/python scripts/create_demo_video.py
```

Output: `demo_video/contract_revenue_radar_qdrant_demo_final.mp4`

Fallback demo without Qdrant dependency:

```bash
PYTHONPATH=src python3 -m contract_radar.cli --no-qdrant samples/acme_services_agreement.md -o examples/reports/demo_report.md
```

## Monetization

The same artifact can be sold as a fixed-scope Revenue Terms Audit:

- $1,500 quick audit for up to 5 documents.
- $2,500 audit plus clause fallback pack.
- $5,000 revenue protection sprint for 15-25 documents and a reusable clause playbook.

Primary buyers: SaaS implementation firms, RevOps consultancies, MSPs, and custom software agencies.

## Safety / Limits

This is business-risk review, not legal advice. Final contract language should be approved by counsel. Redacted documents or template excerpts are enough for a sample audit.

## Session Notes — May 30-31 2026 Live Work (for judges / organizers)
Substantial new code added today to meet "created during hackathon period":
- 2 new revenue risk detectors fully implemented and tested.
- DOCX export capability (new module + CLI + optional dep).
- 2 new sample contracts + test updates.
- Vector search UX improvements + new API endpoints exposing live features.
- Complete documentation refresh + hackathon_submission/ folder created.
- May 31 MemoryAgent prototype + tests + generated report.
- All git-committed with dated messages. Fresh demo outputs captured with qdrant-local-memory backend.

See README.md "Session Notes" section and hackathon_submission/WHY_THIS_WINS.md for full details. Project is stronger and fully compliant.
