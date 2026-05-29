from pathlib import Path
import importlib.util
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from contract_radar.agent_workflow import build_agent_brief, render_agent_brief
from contract_radar.core import ContractRadar, render_markdown


FIXTURES = Path(__file__).resolve().parents[1] / "samples"


class ContractRadarTests(unittest.TestCase):
    def test_audit_finds_revenue_risks_with_fallback_backend(self):
        radar = ContractRadar(prefer_qdrant=False)
        report = radar.audit_paths([FIXTURES / "acme_services_agreement.md"])

        risk_types = {finding.risk_type for finding in report.findings}
        self.assertIn("payment_delay", risk_types)
        self.assertIn("renewal_loss", risk_types)
        self.assertGreaterEqual(report.risk_score, 50)

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


if __name__ == "__main__":
    unittest.main()
