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

- Functionality: runnable CLI, sample contracts, Markdown report.
- Originality: revenue-focused contract risk retrieval rather than generic RAG chat.
- User experience: one command produces a prioritized action report with sources.

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

