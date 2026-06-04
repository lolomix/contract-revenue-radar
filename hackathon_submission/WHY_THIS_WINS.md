# Why Contract Revenue Radar Wins the Qdrant Hackathon

**Tagline:** Vector search for clauses that delay cash, weaken renewals, and leak revenue — built for real B2B sales velocity, not another chatbot.

## 1. Functionality (Judge Criteria)
- Fully working CLI + 7 risk detectors (2 added May 30 during final prep).
- Qdrant `:memory:` primary backend + rock-solid local hash-vector fallback (no network, tests pass offline).
- Structured Markdown + professional DOCX export (new in session).
- HTTP Agent API + MCP-style stdio tool server for local automation.
- 4 diverse samples (original + 2 new SaaS MSA + MSP retainer) + full test suite (9/9 passing).
- Real demo video + reproducible `./scripts/demo.sh`.

## 2. Originality (Beyond the Bot)
- **Not RAG chat.** Deliberately vector-search + deterministic scoring to surface recurring revenue-destroying patterns that sales teams actually negotiate.
- Domain-specific risk ontology (payment delay, renewal loss, scope creep, credit exposure, data blockers, **IP ownership trap**, **auto-renewal fee escalation**).
- Hybrid scoring: 96-dim hash embeddings + phrase-aware keyword boost (enhanced May 30).
- Practical workflow for agencies, MSPs, and RevOps teams that need fast pre-legal business-risk review.

## 3. UX & Polish (Ship-Ready)
- One-command audit → prioritized actions + excerpts + negotiation moves + agent brief.
- New DOCX export produces client-ready professional report (headings, severity color, excerpts).
- Live API surfaces new detectors + export capability flag (`/risk-classes`, `/capabilities`).
- Agent brief, MCP tool, full docs, fresh May 30 2026 demo outputs, and May 31 MemoryAgent prototype.

## 4. Hackathon Rule Compliance — "Code Created During Period"
- **Major new work added May 30 2026 in this session:**
  - 2 new high-value detectors (IP ownership trap, auto-renewal fee escalation) + protective patterns + agent fallbacks.
  - Full DOCX export module + CLI integration + optional dep.
  - 2 new realistic sample contracts (SaaS MSA, MSP retainer) exercising new detectors.
  - Enhanced fallback vector scoring (phrase bonuses, length penalty).
  - 2 new API endpoints + capabilities doc + docx flag.
  - Complete docs refresh + `hackathon_submission/` folder + "Session Notes" proving live work.
- All changes committed with "May 30 2026 final submission prep" messages.
- Tests updated and passing.
- May 31 MemoryAgent module, JSON memory fixture, demo runner, generated report, and tests added.

## 5. Business Impact
This is not a toy. Real agencies need fast, source-linked, negotiation-ready intelligence on clauses that quietly delay cash flow and leak implementation margin.

**Qdrant usage is core and visible:** every audit creates a collection, upserts 96-d vectors, queries per risk class. Fallback proves robustness.

**Ready to win:** Functionality ✓ Originality ✓ UX ✓ Live new work ✓ Business impact ✓

Video: See demo_video/ (or hosted link). Repo contains everything needed for judges to run in <60 seconds.
