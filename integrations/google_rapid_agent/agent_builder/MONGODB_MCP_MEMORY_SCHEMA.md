# MongoDB MCP Memory Schema

Recommended partner track: MongoDB MCP.

## Collections

### `audit_runs`

```json
{
  "audit_run_id": "audit_2026_06_01_001",
  "team": "implementation",
  "contract_type": "SOW",
  "risk_score": 92,
  "risk_types": ["payment_delay", "scope_creep", "ip_ownership"],
  "created_at": "2026-06-01T00:00:00Z",
  "source": "Revenue Terms Agent demo"
}
```

### `fallback_positions`

```json
{
  "memory_id": "payment_delay_saas_net15",
  "risk_type": "payment_delay",
  "applies_to_segment": "SaaS implementation",
  "approved_fallback": "Use Net 15 from invoice date with deemed acceptance after 5 business days.",
  "approver_role": "Finance Director",
  "active": true,
  "created_at": "2026-06-01T00:00:00Z",
  "expires_at": "2026-12-31",
  "source_decision": "Approved fallback from standard SaaS MSA markup"
}
```

### `reviewer_decisions`

```json
{
  "decision_id": "decision_001",
  "audit_run_id": "audit_2026_06_01_001",
  "risk_type": "scope_creep",
  "decision": "approved fallback with support-hour cap",
  "approved_by_role": "Delivery Operations",
  "created_at": "2026-06-01T00:00:00Z"
}
```

## Agent Retrieval Pattern

1. Use audit findings to identify risk types.
2. Query `fallback_positions` where:
   - `active` is true,
   - `risk_type` is in detected risk types,
   - `applies_to_segment` matches the user's business segment or is blank.
3. Include only the most relevant approved memories in the Gemini context.
4. Ask the user before inserting any new `reviewer_decisions` or fallback memory.

## Demo Evidence

The local prototype already proves this memory shape:

```text
qdrant-contract-radar/src/contract_radar/memory_agent.py
qdrant-contract-radar/samples/clause_memory.json
qdrant-contract-radar/scripts/memory_agent_demo.py
```
