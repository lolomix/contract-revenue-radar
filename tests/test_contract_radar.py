from pathlib import Path
import importlib.util
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from contract_radar.agent_workflow import build_agent_brief, render_agent_brief
from contract_radar.core import ContractRadar, render_markdown
from contract_radar.memory_agent import (
    load_memories,
    recall_memories,
    render_memory_agent_report,
    build_memory_agent_result,
)

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from mcp_contract_radar import handle_request  # noqa: E402


FIXTURES = Path(__file__).resolve().parents[1] / "samples"


class ContractRadarTests(unittest.TestCase):
    def test_audit_finds_revenue_risks_with_fallback_backend(self):
        radar = ContractRadar(prefer_qdrant=False)
        report = radar.audit_paths([FIXTURES / "acme_services_agreement.md"])

        risk_types = {finding.risk_type for finding in report.findings}
        self.assertIn("payment_delay", risk_types)
        self.assertIn("renewal_loss", risk_types)
        self.assertGreaterEqual(report.risk_score, 50)

    def test_new_risk_detectors_ip_and_renewal_fee_on_new_samples(self):
        radar = ContractRadar(prefer_qdrant=False)
        saas = radar.audit_paths([FIXTURES / "saas_msa_example.md"])
        msp = radar.audit_paths([FIXTURES / "msp_retainer_agreement.md"])

        saas_risks = {f.risk_type for f in saas.findings}
        msp_risks = {f.risk_type for f in msp.findings}
        # SaaS sample contains work-for-hire IP trap + auto renewal at then-current
        self.assertIn("ip_ownership", saas_risks)
        self.assertIn("renewal_fee_trap", saas_risks)
        # MSP sample contains similar plus audit over-reach
        self.assertIn("ip_ownership", msp_risks)
        self.assertIn("renewal_fee_trap", msp_risks)
        self.assertGreaterEqual(saas.risk_score, 60)
        self.assertGreaterEqual(msp.risk_score, 60)

    def test_cleaner_terms_score_lower_than_risky_terms(self):
        radar = ContractRadar(prefer_qdrant=False)
        risky = radar.audit_paths([FIXTURES / "acme_services_agreement.md"])
        cleaner = radar.audit_paths([FIXTURES / "better_terms_agreement.md"])

        self.assertGreater(risky.risk_score, cleaner.risk_score)


    def test_qdrant_backend_runs_when_dependency_available(self):
        if importlib.util.find_spec("qdrant_client") is None:
            self.skipTest("qdrant-client is not installed")

        radar = ContractRadar(prefer_qdrant=True)
        report = radar.audit_paths([FIXTURES / "acme_services_agreement.md"])

        self.assertEqual(report.backend, "qdrant-local-memory")
        self.assertGreaterEqual(report.risk_score, 50)

    def test_markdown_report_contains_actions_and_sources(self):
        radar = ContractRadar(prefer_qdrant=False)
        report = radar.audit_paths([FIXTURES / "acme_services_agreement.md"])
        markdown = render_markdown(report)

        self.assertIn("# Contract Revenue Radar Report", markdown)
        self.assertIn("Revenue risk score", markdown)
        self.assertIn("acme_services_agreement.md", markdown)
        self.assertIn("Priority Actions", markdown)

    def test_agent_brief_contains_fallback_positions(self):
        radar = ContractRadar(prefer_qdrant=False)
        report = radar.audit_paths([FIXTURES / "acme_services_agreement.md"])
        brief = build_agent_brief(report)
        markdown = render_agent_brief(brief)

        self.assertIn("Revenue Terms Agent Brief", markdown)
        self.assertIn("Fallback Positions", markdown)
        self.assertIn("Sales/Ops Checklist", markdown)
        self.assertGreater(len(brief.fallback_positions), 0)

    def test_memory_agent_recalls_active_segment_memories(self):
        radar = ContractRadar(prefer_qdrant=False)
        report = radar.audit_paths([FIXTURES / "saas_msa_example.md"])
        memories = load_memories(FIXTURES / "clause_memory.json")

        recalled = recall_memories(report, memories, segment="SaaS implementation")
        memory_ids = {memory.memory_id for memory in recalled}

        self.assertIn("payment_delay_saas_net15", memory_ids)
        self.assertIn("ip_ownership_background_ip", memory_ids)
        self.assertIn("renewal_fee_cap_3pct", memory_ids)
        self.assertNotIn("inactive_refund_full_credit", memory_ids)

    def test_memory_agent_report_contains_recalled_fallback(self):
        radar = ContractRadar(prefer_qdrant=False)
        report = radar.audit_paths([FIXTURES / "saas_msa_example.md"])
        memories = load_memories(FIXTURES / "clause_memory.json")
        result = build_memory_agent_result(report, memories, segment="SaaS implementation")
        markdown = render_memory_agent_report(result)

        self.assertIn("Revenue Terms Memory Agent Report", markdown)
        self.assertIn("payment_delay_saas_net15", markdown)
        self.assertIn("Net 15 from invoice date", markdown)
        self.assertIn("Revenue Terms Agent Brief", markdown)

    def test_mcp_tool_call_returns_structured_audit(self):
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "audit_contract_revenue_terms",
                "arguments": {
                    "text": "Payment is Net 90 after acceptance and may be withheld.",
                    "filename": "sample.md",
                    "no_qdrant": True,
                },
            },
        }
        response = handle_request(payload)

        self.assertEqual(response["id"], 2)
        self.assertFalse(response["result"]["isError"])
        structured = response["result"]["structuredContent"]
        self.assertIn("findings", structured)
        self.assertIn("agent_brief", structured)
        self.assertGreaterEqual(structured["risk_score"], 1)


if __name__ == "__main__":
    unittest.main()
