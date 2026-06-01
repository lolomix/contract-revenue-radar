from pathlib import Path
import sys
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from sprint_inquiry_reply import build_sprint_comment, checkbox_items  # noqa: E402


ISSUE_BODY = """### Organization / team

Example RevOps agency

### Approximate document/template count

18 SOW variants and 4 MSA/order-form templates

### Deal or delivery motion

HubSpot onboarding, RevOps managed services, and data migration work.

### Sprint fit

- [X] We have multiple recurring SOW/MSA/order-form variants.
- [X] Sales, delivery, finance, or ops need reusable fallback positions.
- [ ] We can provide redacted templates/excerpts.

### Desired output

Prioritized risk report, fallback positions, clause playbook, and sales/ops checklist.

### Acknowledgement

- [X] I understand this is business-risk review, not legal advice.
"""


class SprintInquiryReplyTests(unittest.TestCase):
    def test_checkbox_items_keeps_checked_only(self):
        items = checkbox_items("- [X] One\n- [ ] Two\n- [x] Three")

        self.assertEqual(items, ["One", "Three"])

    def test_build_sprint_comment_contains_scope_and_approval(self):
        comment = build_sprint_comment(ISSUE_BODY)

        self.assertIn("Revenue Protection Sprint Intake Response", comment)
        self.assertIn("$5,000 fixed scope", comment)
        self.assertIn("18 SOW variants", comment)
        self.assertIn("Approval packet", comment)
        self.assertIn("Approval Language", comment)
        self.assertIn("not legal advice", comment)


if __name__ == "__main__":
    unittest.main()
