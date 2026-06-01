from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from issue_sample_audit import build_sample_comment, parse_issue_form  # noqa: E402


ISSUE_BODY = """### Organization / team

Example RevOps team

### Contract type

Statement of Work (SOW)

### Business context

HubSpot implementation and managed services.

### Main concerns

- [X] Payment timing or acceptance gates
- [X] Scope creep or change orders

### Redacted excerpt or public-style sample

Vendor will provide implementation support and additional support as requested by Customer. Customer will pay invoices on Net 90 terms after acceptance by the Customer project owner. Customer may terminate for convenience with 30 days notice.

### Acknowledgement

- [X] I understand this is business-risk review, not legal advice.
"""


class IssueSampleAuditTests(unittest.TestCase):
    def test_parse_issue_form_extracts_fields(self):
        fields = parse_issue_form(ISSUE_BODY)

        self.assertEqual(fields["Organization / team"], "Example RevOps team")
        self.assertEqual(fields["Contract type"], "Statement of Work (SOW)")
        self.assertIn("Net 90", fields["Redacted excerpt or public-style sample"])

    def test_build_sample_comment_contains_findings_and_cta(self):
        comment = build_sample_comment(ISSUE_BODY)

        self.assertIn("Automated 3-Finding Sample Audit", comment)
        self.assertIn("Payment delay", comment)
        self.assertIn("Revenue risk score", comment)
        self.assertIn("Revenue Protection Sprint", comment)
        self.assertIn("not legal advice", comment)


if __name__ == "__main__":
    unittest.main()
