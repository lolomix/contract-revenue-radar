# UiPath AgentHack Adaptation Plan

Objective: adapt Contract Revenue Radar into a UiPath-orchestrated enterprise agent for the UiPath AgentHack 2026.

Official page: https://uipath-agenthack.devpost.com/

Deadline: June 29, 2026 at 11:45 PM PDT.

Prize fit: $50,000 total cash pool; $8,000 grand prize; $5,000 best-of-track awards for Maestro Case, Maestro BPMN, and Test Cloud.

## Recommended Track

Track 1: UiPath Maestro Case.

Why: contract review is dynamic and exception-heavy. Different documents produce different issues, and the workflow needs human checkpoints before legal or finance approval.

Alternate track: UiPath Maestro BPMN if the demo is framed as a predictable order-to-cash or SOW approval process.

## Product Name

Revenue Terms Case Agent

## Business Problem

Implementation firms, RevOps teams, MSPs, and professional-services teams lose margin or delay cash when risky SOW/MSA terms are noticed too late. Common issues include payment after customer acceptance, vague customer dependencies, unlimited included work, broad refunds or credits, short termination windows, and unresolved security/data obligations.

## Agent Workflow

1. Intake
   - User uploads or pastes a redacted SOW, MSA, order form, or proposal.
   - Required fields: customer name, contract type, deal value band, expected signature date, business owner.

2. Triage agent
   - Calls `audit_contract_revenue_terms` through `scripts/mcp_contract_radar.py` or the HTTP `/audit` endpoint.
   - Scores the document and identifies revenue-risk findings.

3. Case orchestration
   - If risk score is below 35, route to normal approval.
   - If risk score is 35-69, create a sales/ops review task with fallback positions.
   - If risk score is 70+, create legal/finance review tasks and block signature until the business owner approves the fallback plan.

4. Human-in-the-loop
   - Business owner answers priority questions.
   - Legal or finance approves final fallback language.
   - Sales confirms whether the customer accepted, rejected, or escalated each fallback.

5. Closeout
   - Agent writes the final risk summary, fallback decisions, and reusable clause notes.
   - Approved fallback positions become the starting playbook for future deals.

## Local Assets Already Built

- CLI: `contract-radar`
- HTTP tool: `scripts/serve_agent_api.py`
- MCP-style stdio tool: `scripts/mcp_contract_radar.py`
- Sample JSON-RPC call: `samples/mcp_tool_call.json`
- Demo contract: `samples/acme_services_agreement.md`
- Agent brief/report: `agent_report.md`
- Sample sales packet generator: `/home/ubuntu/revenue_5000/tools/generate_sample_audit_packet.py`

## UiPath Components To Use

- UiPath Automation Cloud as the required orchestration layer.
- UiPath Maestro Case for stages, exceptions, business owner review, and approval gates.
- API Workflows or a robot activity to call the local/hosted Contract Revenue Radar endpoint.
- Agent Builder or an external coded agent for summarization, priority questions, and fallback explanation.
- Human tasks for business, legal, and finance review.

## Demo Script

1. Show a new case created from a redacted SOW.
2. Show the agent calling the Contract Revenue Radar tool.
3. Show a high risk score with payment, scope, renewal, and security findings.
4. Show Maestro routing to business/legal/finance tasks.
5. Show fallback positions attached to the case.
6. Show final approval summary and reusable clause playbook.

## Submission Requirements Checklist

- Public GitHub repository.
- MIT or Apache 2.0 license.
- README with setup, prerequisites, UiPath components, and whether coded agents/low-code agents are used.
- Working solution on UiPath Automation Cloud.
- Demo video of 5 minutes maximum showing the solution running, architecture, agents, orchestration, and human involvement.
- Presentation deck link.

## Build Order

1. Request UiPath Labs access from the Devpost page.
2. Create a Maestro Case flow with stages: Intake, Audit, Business Review, Legal/Finance Review, Final Decision.
3. Host or expose the existing `/audit` API endpoint.
4. Add API Workflow call from UiPath to `/audit`.
5. Map response fields into case data: risk score, findings, agent brief, fallback positions.
6. Record the 5-minute demo.
7. Submit on Devpost before June 29, 2026 at 11:45 PM PDT.

