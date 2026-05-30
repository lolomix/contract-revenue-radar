# Hackathon Submission Draft

## Project

Contract Revenue Radar

## Tagline

Vector search for clauses that delay cash, weaken renewals, and leak revenue.

## Problem

Small agencies, consultants, MSPs, and SaaS vendors often sign customer agreements that quietly damage cash flow: Net 90 terms, vague acceptance gates, broad termination rights, unlimited revision language, uncapped service credits, and security terms that stall signatures. Most teams do not have time to read every agreement deeply before a deadline.

## Solution

Contract Revenue Radar indexes contract sections in Qdrant local mode, searches for revenue-risk patterns, and produces a prioritized Markdown report with excerpts and negotiation actions. It is intentionally not a chatbot. The user gets a concrete audit trail instead of asking open-ended questions.

## Qdrant Usage

The app uses `qdrant-client` with `QdrantClient(":memory:")`, creates a collection, upserts embedded contract sections as points, and runs vector queries for each risk class. The same embedding path powers a fallback backend for offline tests, but Qdrant is the primary backend when installed.

## Judging Criteria Notes

- Functionality: runnable CLI + 7 detectors, 4 samples, Markdown + DOCX reports, full Agent API + MCP tool, 7/7 tests.
- Originality: revenue-focused contract risk retrieval (not generic RAG chat). 2 new detectors added May 30 (IP ownership trap + auto-renewal fee escalation) tailored for agencies/MSPs.
- User experience: one command → prioritized actions + excerpts + negotiation moves + professional DOCX. New API endpoints and enhanced hybrid scoring.

**May 30 2026 session added substantial new code** (see README Session Notes + hackathon_submission/WHY_THIS_WINS.md for proof of live work during the period).

## 3-Minute Demo Script

1. Open with the business problem: "This Net 90 clause can turn a profitable project into a cash crunch."
2. Show the sample risky agreement.
3. Run:

   ```bash
   PYTHONPATH=src python -m contract_radar.cli samples/acme_services_agreement.md -o report.md
   ```

4. Open `report.md` and show the risk score, payment delay finding, renewal finding, and action list.
5. Explain Qdrant local mode: contract sections are points; risk themes are vector queries.
6. Close with monetization: sell as a $1,500-$5,000 fixed-scope revenue terms audit for agencies, MSPs, and SaaS teams.

## Session Notes — May 30 2026 Final Prep (Live Work)
- Added IP ownership trap + auto-renewal fee escalation detectors (full integration).
- Shipped DOCX export module + CLI support.
- Added SaaS MSA + MSP retainer samples + test coverage.
- Enhanced vector fallback scoring + 2 new live API endpoints.
- Created hackathon_submission/ bundle + refreshed every doc with today's exact demo output.
- All committed with clear "May 30 2026 final submission prep" messages.

This directly satisfies the spirit of creating meaningful new code during the hackathon window.
