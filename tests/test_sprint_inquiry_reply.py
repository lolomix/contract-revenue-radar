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

B2B_PACKAGE_BODY = """### Organization / team

Example RevOps MSP

### Selected package

B2B Business Package ($3,500)

### Requester role

Delivery lead

### Approximate document/template count

12 MSA, SOW, and renewal excerpts

### Contract or template types

Managed-services SOWs, implementation addenda, and renewal terms.

### Top risk areas

Payment timing, SLA credits, support scope, and renewal leakage.

### Approval, payment, or procurement path

Private payment-link route after written approval.

### Target timeline

3-4 business days

### Intake readiness

- [X] I understand this is business-risk review, not legal advice.
- [X] I will not post confidential documents, personal data, private client details, tax IDs, or payment credentials in this public issue.
"""

B2B_DEDICATED_BODY = """### Organization / team

Example B2B services team

### Requester role

Finance owner

### Approximate document/template count

14 SOW and renewal excerpts

### Contract or template types

Recurring services SOWs and order forms.

### Top risk areas

Payment timing, acceptance gates, and scope boundaries.

### Approval/payment route

I need a private payment-link route after written approval

### Target timeline

4 business days after payment/intake

### Intake readiness

- [X] I understand this is business-risk review, not legal advice.
- [X] I understand the B2B Business Package is $3,500 fixed scope.
- [X] I will not post confidential documents, personal data, private client details, tax IDs, or payment credentials in this public issue.
"""

B2B_APPROVAL_BODY = """### Organization / team

Northstar RevOps

### Approver role

Finance owner

### Payment/procurement route

Private payment link after approval

### Approval text

Approved. I authorize the $3,500 B2B Business Package and understand this is business-risk review, not legal advice.

### Acknowledgement

- [X] I understand the B2B Business Package is $3,500 fixed scope.
- [X] I understand this is business-risk review, not legal advice.
- [X] I will not post confidential documents, personal data, private client details, tax IDs, or payment credentials in this public issue.
"""

PAID_REVIEW_START_BODY = """### Organization / team

Northstar Services

### Paid review package

B2B Business Package ($3,500)

### Requester / approver role

Founder

### Approximate document/template count

11 SOW and renewal templates

### Top risk areas

Payment timing and support scope.

### Payment/procurement route

Private payment link after written approval

### Target start window

This week

### Acknowledgement

- [X] I understand this is business-risk review, not legal advice.
- [X] I will not post confidential documents, payment credentials, private client details, personal data, or tax IDs in this public issue.
- [X] I can approve, route, or introduce the correct person for payment/procurement approval.
"""


class SprintInquiryReplyTests(unittest.TestCase):
    def test_checkbox_items_keeps_checked_only(self):
        items = checkbox_items("- [X] One\n- [ ] Two\n- [x] Three")

        self.assertEqual(items, ["One", "Three"])

    def test_approval_language_for_package_uses_exact_price(self):
        approval = approval_language_for_package("Audit + Negotiation Fallback Pack ($2,500)")

        self.assertIn("$2,500 Audit + Negotiation Fallback Pack", approval)
        self.assertIn("business-risk review, not legal advice", approval)

    def test_approval_language_for_b2b_package_uses_exact_price(self):
        approval = approval_language_for_package("B2B Business Package ($3,500)")

        self.assertIn("$3,500 B2B Business Package", approval)
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

    def test_b2b_service_package_comment_contains_3500_scope(self):
        comment = build_sprint_comment(B2B_PACKAGE_BODY)

        self.assertIn("B2B Business Package - $3,500 fixed scope", comment)
        self.assertIn("12 MSA, SOW", comment)
        self.assertIn("Private payment-link route", comment)
        self.assertIn("Approved. I authorize the $3,500 B2B Business Package", comment)
        self.assertIn("confirmed private payment-link route", comment)

    def test_dedicated_b2b_package_comment_closes_to_private_payment_route(self):
        comment = build_sprint_comment(B2B_DEDICATED_BODY)

        self.assertIn("B2B Business Package Intake Response", comment)
        self.assertIn("$3,500 B2B Business Package request", comment)
        self.assertIn("14 SOW", comment)
        self.assertIn("Close-ready approval text", comment)
        self.assertIn("Approved. I authorize the $3,500 B2B Business Package", comment)
        self.assertIn("confirmed private payment-link route", comment)
        self.assertIn("Do **not** post private documents", comment)

    def test_b2b_approval_comment_does_not_route_to_revenue_protection_sprint(self):
        comment = build_sprint_comment(B2B_APPROVAL_BODY)

        self.assertIn("B2B Business Package Approval Response", comment)
        self.assertIn("approval signal", comment)
        self.assertIn("B2B Business Package ($3,500)", comment)
        self.assertIn("Private payment link after approval", comment)
        self.assertIn("Approved. I authorize the $3,500 B2B Business Package", comment)
        self.assertNotIn("Revenue Protection Sprint - $5,000 fixed scope", comment)

    def test_paid_review_start_comment_routes_to_private_close_path(self):
        comment = build_sprint_comment(PAID_REVIEW_START_BODY)

        self.assertIn("Paid Review Start Response", comment)
        self.assertIn("Northstar Services", comment)
        self.assertIn("B2B Business Package ($3,500)", comment)
        self.assertIn("Private payment link after written approval", comment)
        self.assertIn("Approved. I authorize the $3,500 B2B Business Package", comment)
        self.assertIn("private payment/procurement and document intake", comment)
        self.assertNotIn("Revenue Protection Sprint - $5,000 fixed scope", comment)


if __name__ == "__main__":
    unittest.main()
