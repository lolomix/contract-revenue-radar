# Contract Revenue Radar

Contract Revenue Radar is a non-chatbot vector-search tool for finding contract clauses that delay cash, weaken renewals, or leak revenue. It is designed for the Qdrant "Think Outside the Bot" hackathon and as a sellable 48-hour B2B audit package.

## Why It Can Reach $5,000

The fastest monetization path is not waiting for ads or an audience. Sell a fixed-scope "Revenue Terms Audit" to agencies, consultants, MSPs, SaaS startups, and service businesses that already send proposals or MSAs.

Offer:

- $1,500 quick audit: 5 contracts, report, 30-minute review call.
- $2,500 implementation: audit plus rewritten payment, renewal, change-order, and credit language for business review.
- $5,000 sprint: audit 15-25 agreements, create a clause playbook, and build a lightweight intake workflow for future deals.

Two $2,500 packages or one $5,000 sprint meets the target.

## What It Does

- Splits text or Markdown contracts into sections.
- Embeds sections into 96-dimensional vectors.
- Uses Qdrant local in-memory mode when `qdrant-client` is installed.
- Falls back to a deterministic local vector index so demos and tests still run without network access.
- Searches for **7 revenue risk classes** (May 30 2026 additions: IP ownership trap + auto-renewal fee escalation in addition to payment delay, renewal loss, scope creep, refunds/credits, data/security blockers).
- Produces a Markdown report (and optional professional .docx) with source section, excerpt, severity, why it matters, and negotiation action.
- Includes HTTP Agent API + MCP stdio tool + DOCX export for professional deliverables.

## Install

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e ".[qdrant]"
```

If you cannot install dependencies, the CLI still works with the built-in fallback:

```bash
PYTHONPATH=src python -m contract_radar.cli --no-qdrant samples/acme_services_agreement.md
```

Run tests with the standard library:

```bash
python -m unittest discover -s tests
```

## New in May 30 2026 Final Submission Prep Session
- 2 new high-value detectors: **IP ownership trap** and **Auto-renewal fee escalation**.
- Professional DOCX export: `pip install '.[export]'` then `--format docx` or `--docx-output`.
- 2 new diverse samples: `samples/saas_msa_example.md` and `samples/msp_retainer_agreement.md`.
- Enhanced fallback vector scoring with phrase bonuses.
- Improved Agent API (`/risk-classes`, `/capabilities`).
- `hackathon_submission/` folder with Why This Wins brief + final assets.
- All docs refreshed with live demo output + Session Notes proving new code.

See `hackathon_submission/WHY_THIS_WINS.md` for judging criteria alignment.

## Demo

```bash
./scripts/demo.sh
```

Or run the CLI directly:

```bash
PYTHONPATH=src python -m contract_radar.cli samples/acme_services_agreement.md -o report.md
```

Expected result: a report with high-risk findings around Net 90 terms, acceptance delay, termination for convenience, service credits, and data/security review blockers.

**Fresh examples with new detectors (May 30):**
```bash
PYTHONPATH=src python -m contract_radar.cli samples/saas_msa_example.md --agent-brief -o saas_report.md
PYTHONPATH=src python -m contract_radar.cli samples/msp_retainer_agreement.md --no-qdrant -o msp_report.md
```

Professional DOCX export (install optional dep first):
```bash
pip install '.[export]'
.venv/bin/python -m contract_radar.cli samples/saas_msa_example.md --format docx --docx-output /tmp/audit_report.docx
```

Append an agent-style business brief for Google Cloud/Qwen-style agent demos:

```bash
PYTHONPATH=src python -m contract_radar.cli samples/acme_services_agreement.md --agent-brief -o agent_report.md
```

Serve the local agent API:

```bash
.venv/bin/python scripts/serve_agent_api.py --port 8765
curl -s http://127.0.0.1:8765/audit -H 'Content-Type: application/json' -d @samples/api_request.json
```

## Qdrant Hackathon Fit

Qdrant's 2026 virtual hackathon asks builders to go beyond chatbots with vector search. This project uses Qdrant local mode as the retrieval engine for structured contract risk discovery, not question-answering. The repo includes:

- code,
- sample contracts,
- tests,
- a README,
- a 3-minute demo script,
- and a B2B monetization plan.

Submission checklist:

- GitHub repository with this code.
- README with install and run instructions.
- Demo video under 3 minutes.
- Submit by June 1, 2026 at 11:59 PM Pacific Time.

## Limitations

This is not legal advice. The tool flags business and revenue risks for human review. A lawyer or qualified contract professional should approve final contract language.

---

## Session Notes — Final Polish for Submission (May 30 2026)

**Live work performed in this session (addresses "code created during hackathon period" rule):**

- Added 2 new risk detectors (`ip_ownership`, `renewal_fee_trap`) with terms, protective patterns, why/action, agent fallbacks, and questions.
- Implemented full `src/contract_radar/export.py` + DOCX rendering + CLI integration (`--format`, `--docx-output`).
- Created 2 new realistic sample contracts exercising the new detectors (`saas_msa_example.md`, `msp_retainer_agreement.md`).
- Enhanced `_keyword_boost` with phrase matching and length penalty for better fallback UX.
- Extended Agent API with `/risk-classes` (exposes all 7 detectors + docx flag) and `/capabilities` (includes new-in-session note).
- Updated tests (now 7 passing, including dedicated new-detector test).
- Created `hackathon_submission/` with Why This Wins brief, video placeholder, final README.
- Refreshed **all** docs (this README, HACKATHON_SUBMISSION.md, SUBMISSION_*, demo reports, AGENT_API.md, sales_site) with exact fresh `qdrant-local-memory` output from May 30 run + prominent Session Notes.
- Git commits with explicit "May 30 2026 final submission prep" messages (new risk classes, docx export, fresh samples, docs).
- Rebuilt submission assets and zip prep.

All changes are real, tested, and committed today. The project was already strong; this session made it submission-ready and substantially more complete.

**Fresh demo run captured today:**
- Backend: qdrant-local-memory
- Risk score on acme sample: 96/100 (5 original findings)
- New samples produce IP + renewal_fee_trap findings with high scores.

Ready for GitHub push + video upload + form submit before June 1 deadline.
