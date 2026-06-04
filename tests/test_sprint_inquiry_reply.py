from pathlib import Path
import sys
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from sprint_inquiry_reply import approval_language_for_package, build_sprint_comment, checkbox_items  # noqa: E402


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

INVOICE_BODY = """### Organization / team

Example MSP

### Requester role

Operations lead

### Approximate document/template count

20 managed-services SOW and MSA variants

### Approval or procurement path

Invoice after approval; vendor setup may be required.

### Preferred start window

This week

### Delivery priorities

SLA credits, payment timing, renewal terms, and support scope.

### Approval readiness

- [X] I understand the Revenue Protection Sprint is $5,000 fixed scope.
- [X] I understand this is business-risk review, not legal advice.
- [X] I can approve, route, or introduce the correct person for invoice/procurement approval.
"""

SERVICE_PACKAGE_BODY = """### Organization / team

Example implementation partner

### Selected package

Audit + Negotiation Fallback Pack ($2,500)

### Requester role

Founder

### Approximate document/template count

8 SOWs and order-form excerpts

### Contract or template types

Implementation SOWs and renewal addenda.

### Top risk areas

Acceptance gates, scope creep, and reusable-IP language.

### Approval, payment, or procurement path

Written approval first, then platform-approved payment link.

### Target timeline

3-4 business days

### Intake readiness

- [X] I understand this is business-risk review, not legal advice.
- [X] I will not post confidential documents, personal data, private client details, tax IDs, or payment credentials in this public issue.
- [X] I can provide redacted templates or excerpts through a private intake path after approval.
"""


class SprintInquiryReplyTests(unittest.TestCase):
    def test_checkbox_items_keeps_checked_only(self):
        items = checkbox_items("- [X] One\n- [ ] Two\n- [x] Three")

        self.assertEqual(items, ["One", "Three"])

    def test_approval_language_for_package_uses_exact_price(self):
        approval = approval_language_for_package("Audit + Negotiation Fallback Pack ($2,500)")

        self.assertIn("$2,500 Audit + Negotiation Fallback Pack", approval)
        self.assertIn("business-risk review, not legal advice", approval)

    def test_build_sprint_comment_contains_scope_and_approval(self):
        comment = build_sprint_comment(ISSUE_BODY)

        self.assertIn("Revenue Protection Sprint Intake Response", comment)
        self.assertIn("$5,000 fixed scope", comment)
        self.assertIn("18 SOW variants", comment)
        self.assertIn("Approval packet", comment)
        self.assertIn("Approval Language", comment)
        self.assertIn("not legal advice", comment)

    def test_invoice_request_comment_contains_procurement_next_steps(self):
        comment = build_sprint_comment(INVOICE_BODY)

        self.assertIn("Invoice Path Response", comment)
        self.assertIn("Operations lead", comment)
        self.assertIn("This week", comment)
        self.assertIn("Invoice / Approval Path", comment)
        self.assertIn("Request invoice/approval path", comment)
        self.assertIn("$5,000 fixed scope", comment)

    def test_service_package_comment_contains_paid_package_next_steps(self):
        comment = build_sprint_comment(SERVICE_PACKAGE_BODY)

        self.assertIn("Paid Service Package Intake Response", comment)
        self.assertIn("Audit + Negotiation Fallback Pack - $2,500 fixed scope", comment)
        self.assertIn("Founder", comment)
        self.assertIn("8 SOWs", comment)
        self.assertIn("Payment / Approval Path", comment)
        self.assertIn("Close-Ready Approval Text", comment)
        self.assertIn("Approved. I authorize the $2,500 Audit + Negotiation Fallback Pack", comment)
        self.assertIn("authorized approver name and role", comment)
        self.assertIn("platform-approved payment path", comment)
        self.assertIn("Do **not** post private documents", comment)
        self.assertIn("Services and packages", comment)


if __name__ == "__main__":
    unittest.main()
