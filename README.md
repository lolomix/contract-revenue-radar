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
- Searches for risk classes: payment delay, renewal loss, scope creep, refunds/credits, and data/security blockers.
- Produces a Markdown report with source section, excerpt, why it matters, and negotiation action.

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

## Demo

```bash
./scripts/demo.sh
```

Or run the CLI directly:

```bash
PYTHONPATH=src python -m contract_radar.cli samples/acme_services_agreement.md -o report.md
```

Expected result: a report with high-risk findings around Net 90 terms, acceptance delay, termination for convenience, service credits, and data/security review blockers.

Append an agent-style business brief for Google Cloud/Qwen-style agent demos:

```bash
PYTHONPATH=src python -m contract_radar.cli samples/acme_services_agreement.md --agent-brief -o agent_report.md
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
