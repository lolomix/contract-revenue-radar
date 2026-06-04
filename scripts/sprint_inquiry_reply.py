#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from issue_sample_audit import INTAKE_URL, SPRINT_URL, parse_issue_form, truncate


SAMPLE_URL = "https://github.com/lolomix/contract-revenue-radar/issues/new?template=free-sample-audit.yml"
SERVICE_PACKAGE_URL = "https://github.com/lolomix/contract-revenue-radar/issues/new?template=service-package-request.yml"
B2B_PACKAGE_URL = "https://github.com/lolomix/contract-revenue-radar/issues/new?template=b2b-business-package.yml"
PAID_REVIEW_START_URL = "https://github.com/lolomix/contract-revenue-radar/issues/new?template=paid-review-start.yml"
APPROVAL_PACKET_URL = "https://lolomix.github.io/contract-revenue-radar/approval-packet.html"
SERVICES_URL = "https://lolomix.github.io/contract-revenue-radar/services.html"
REVIEW_ROOM_URL = "https://lolomix.github.io/contract-revenue-radar/review-room.html"
DEMO_URL = (
    "https://github.com/lolomix/contract-revenue-radar/releases/download/"
    "qdrant-submission-2026/contract_revenue_radar_qdrant_demo_final.mp4"
)
APPROVAL_LANGUAGE = (
    "Approved. I authorize the $5,000 Revenue Protection Sprint and understand "
    "this is business-risk review, not legal advice."
)
INVOICE_REQUEST_URL = "https://github.com/lolomix/contract-revenue-radar/issues/new?template=sprint-invoice-request.yml"


def checkbox_items(value: str) -> list[str]:
    items: list[str] = []
    for line in value.splitlines():
        stripped = line.strip()
        if stripped.startswith("- [X]") or stripped.startswith("- [x]"):
            items.append(stripped[5:].strip())
        elif stripped.startswith("- [ ]"):
            continue
    return items


PACKAGE_SCOPES = {
    "Revenue Terms Audit ($1,500)": [
        "**Revenue Terms Audit - $1,500 fixed scope**",
        "- Review up to 5 redacted documents or excerpts.",
        "- Return a revenue-risk report with exact excerpts, severity, business impact, and priority actions.",
        "- Check payment, acceptance, renewal, scope, credit/refund, security, and reusable-IP risk.",
        "- Target turnaround: 48 hours after payment, complete intake, and confirmed scope.",
    ],
    "Audit + Negotiation Fallback Pack ($2,500)": [
        "**Audit + Negotiation Fallback Pack - $2,500 fixed scope**",
        "- Review up to 10 redacted documents or excerpts.",
        "- Include everything in the audit package.",
        "- Add fallback positions for counsel review and a sales/ops checklist for recurring terms.",
        "- Target turnaround: 3-4 business days after payment, complete intake, and confirmed scope.",
    ],
    "B2B Business Package ($3,500)": [
        "**B2B Business Package - $3,500 fixed scope**",
        "- Review up to 15 redacted documents or recurring template excerpts.",
        "- Return a prioritized revenue-risk report plus reusable fallback positions.",
        "- Produce a buyer-safe summary for sales, delivery, finance, and counsel review.",
        "- Target turnaround: 4 business days after payment, complete intake, and confirmed scope.",
    ],
    "Revenue Protection Sprint ($5,000)": [
        "**Revenue Protection Sprint - $5,000 fixed scope**",
        "- Review 15-25 redacted recurring templates or excerpts.",
        "- Produce a reusable clause playbook and intake checklist.",
        "- Include a 60-minute review session for sales, ops, finance, and counsel coordination.",
        "- Target turnaround: 5 business days after payment/procurement approval and document intake.",
    ],
}

PACKAGE_PRICES = {
    "Revenue Terms Audit ($1,500)": "$1,500",
    "Audit + Negotiation Fallback Pack ($2,500)": "$2,500",
    "B2B Business Package ($3,500)": "$3,500",
    "Revenue Protection Sprint ($5,000)": "$5,000",
}

PACKAGE_NAMES = {
    "Revenue Terms Audit ($1,500)": "Revenue Terms Audit",
    "Audit + Negotiation Fallback Pack ($2,500)": "Audit + Negotiation Fallback Pack",
    "B2B Business Package ($3,500)": "B2B Business Package",
    "Revenue Protection Sprint ($5,000)": "Revenue Protection Sprint",
}


def approval_language_for_package(selected_package: str) -> str:
    price = PACKAGE_PRICES.get(selected_package, "selected")
    package_name = PACKAGE_NAMES.get(selected_package, "Contract Revenue Radar package")
    return (
        f"Approved. I authorize the {price} {package_name} and understand "
        "this is business-risk review, not legal advice."
    )


def build_service_package_comment(issue_body: str) -> str:
    fields = parse_issue_form(issue_body)
    organization = fields.get("Organization / team", "Requested organization").strip() or "Requested organization"
    selected_package = fields.get("Selected package", "Not sure yet").strip() or "Not sure yet"
    requester_role = fields.get("Requester role", "").strip()
    document_count = fields.get("Approximate document/template count", "").strip()
    contract_types = fields.get("Contract or template types", "").strip()
    top_risks = fields.get("Top risk areas", "").strip()
    approval_path = fields.get("Approval, payment, or procurement path", "").strip()
    timeline = fields.get("Target timeline", "").strip()
    readiness_items = checkbox_items(fields.get("Intake readiness", ""))
    public_notes = fields.get("Public-safe notes", "").strip()

    lines = [
        "## Paid Service Package Intake Response",
        "",
        "Thanks for the package request. This response confirms the public-safe intake and the next information needed before paid work can start.",
        "",
        f"- Organization/team: **{organization}**",
        f"- Selected package: **{truncate(selected_package, 120)}**",
    ]
    if requester_role:
        lines.append(f"- Requester role: **{truncate(requester_role, 120)}**")
    if document_count:
        lines.append(f"- Approximate document/template count: **{truncate(document_count, 180)}**")
    if contract_types:
        lines.append(f"- Contract/template types: {truncate(contract_types, 260)}")
    if top_risks:
        lines.append(f"- Top risk areas: {truncate(top_risks, 260)}")
    if approval_path:
        lines.append(f"- Approval/payment/procurement path: {truncate(approval_path, 260)}")
    if timeline:
        lines.append(f"- Target timeline: **{truncate(timeline, 80)}**")
    if public_notes:
        lines.append(f"- Public-safe notes: {truncate(public_notes, 260)}")

    if readiness_items:
        lines.extend(["", "### Intake Readiness"])
        lines.extend(f"- {item}" for item in readiness_items)

    lines.extend(["", "### Recommended Scope", ""])
    lines.extend(PACKAGE_SCOPES.get(selected_package, [
        "**Package fit to confirm**",
        "- $1,500 audit: up to 5 redacted documents or excerpts.",
        "- $2,500 audit + fallback pack: up to 10 redacted documents or excerpts plus fallback positions for counsel review.",
        "- $3,500 B2B Business Package: up to 15 recurring templates or excerpts plus prioritized fallback positions.",
        "- $5,000 Revenue Protection Sprint: 15-25 recurring templates or excerpts plus playbook, checklist, and review session.",
    ]))

    lines.extend([
        "",
        "### Payment / Approval Path",
        "",
        "Keep private billing, tax, contract, and payment details out of this public issue. The next private step is to confirm:",
        "",
        "- payer or company name for invoice/vendor setup,",
        "- role-based billing contact, platform-approved payment path, or confirmed private payment-link route,",
        "- whether W-9, vendor setup, purchase order, or written approval is required,",
        "- secure/private document intake path for redacted templates or excerpts,",
        "- business owner for priorities, acceptance of scope, and scheduling.",
        "",
        "### Close-Ready Approval Text",
        "",
        "An authorized business contact can approve the selected package privately, through procurement, or through a platform-approved order path with:",
        "",
        f"> {approval_language_for_package(selected_package)}",
        "",
        "Minimum private details needed to issue invoice/payment instructions:",
        "",
        "- authorized approver name and role,",
        "- payer or company name,",
        "- billing/procurement contact, approved marketplace path, or confirmed private payment-link route,",
        "- selected package and target start date,",
        "- document intake method for redacted files.",
        "",
        "### What To Send Next",
        "",
        "Do **not** post private documents in this public issue. Use a private transfer path for redacted files once the engagement is approved.",
        "",
        "Needed next:",
        "",
        "- confirm package selection and document count,",
        "- confirm payment/procurement path,",
        "- confirm target delivery date,",
        "- identify whether counsel, finance, delivery ops, RevOps, or founder owns final approval.",
        "",
        "### Useful Links",
        "",
        f"- Services and packages: {SERVICES_URL}",
        f"- Review Room: {REVIEW_ROOM_URL}",
        f"- Approval packet: {APPROVAL_PACKET_URL}",
        f"- $5,000 invoice/approval path: {INVOICE_REQUEST_URL}",
        f"- Optional 3-finding sample first: {SAMPLE_URL}",
        f"- Demo video: {DEMO_URL}",
        "",
        "### Boundary",
        "",
        "This is business-risk review for sales, finance, delivery, and operations teams. It is not legal advice, and counsel should approve final contract language.",
    ])
    return "\n".join(lines) + "\n"


def build_b2b_package_comment(issue_body: str) -> str:
    fields = parse_issue_form(issue_body)
    organization = fields.get("Organization / team", "Requested organization").strip() or "Requested organization"
    requester_role = fields.get("Requester role", "").strip()
    document_count = fields.get("Approximate document/template count", "").strip()
    contract_types = fields.get("Contract or template types", "").strip()
    top_risks = fields.get("Top risk areas", "").strip()
    approval_route = fields.get("Approval/payment route", "").strip()
    timeline = fields.get("Target timeline", "").strip()
    readiness_items = checkbox_items(fields.get("Intake readiness", ""))
    public_notes = fields.get("Public-safe notes", "").strip()

    lines = [
        "## B2B Business Package Intake Response",
        "",
        "Thanks for the $3,500 B2B Business Package request. This confirms the public-safe intake and the next steps before paid work can start.",
        "",
        f"- Organization/team: **{organization}**",
        "- Selected package: **B2B Business Package ($3,500)**",
    ]
    if requester_role:
        lines.append(f"- Requester role: **{truncate(requester_role, 120)}**")
    if document_count:
        lines.append(f"- Approximate document/template count: **{truncate(document_count, 180)}**")
    if contract_types:
        lines.append(f"- Contract/template types: {truncate(contract_types, 260)}")
    if top_risks:
        lines.append(f"- Top risk areas: {truncate(top_risks, 260)}")
    if approval_route:
        lines.append(f"- Approval/payment route: **{truncate(approval_route, 160)}**")
    if timeline:
        lines.append(f"- Target timeline: **{truncate(timeline, 80)}**")
    if public_notes:
        lines.append(f"- Public-safe notes: {truncate(public_notes, 260)}")

    if readiness_items:
        lines.extend(["", "### Intake Readiness"])
        lines.extend(f"- {item}" for item in readiness_items)

    lines.extend([
        "",
        "### Fixed Scope",
        "",
        "**B2B Business Package - $3,500 fixed scope**",
        "",
        "- Review up to 15 redacted documents or recurring template excerpts.",
        "- Flag payment timing, acceptance, customer dependency, support scope, renewal, credit/refund, data/security, and reusable-IP risks.",
        "- Return a prioritized revenue-risk report with exact excerpts and recommended fallback positions.",
        "- Produce a buyer-safe summary for sales, delivery, finance, and counsel review.",
        "- Target turnaround: 4 business days after payment, complete intake, and confirmed scope.",
        "",
        "### Approval / Payment Path",
        "",
        "Keep private billing, tax, contract, and payment details out of this public issue. The next private step is to confirm the authorized approver and payment/procurement route.",
        "",
        "Close-ready approval text:",
        "",
        "> Approved. I authorize the $3,500 B2B Business Package and understand this is business-risk review, not legal advice.",
        "",
        "Minimum private details needed after approval:",
        "",
        "- authorized approver name and role,",
        "- payer or company name,",
        "- billing/procurement contact, approved marketplace path, or confirmed private payment-link route,",
        "- target start date,",
        "- private intake method for redacted files.",
        "",
        "### What To Send Next",
        "",
        "Do **not** post private documents in this public issue. Once approved, use a private transfer path for redacted files.",
        "",
        "- confirm whether the selected route is payment link, procurement approval, vendor setup, or funded platform order,",
        "- confirm target delivery date,",
        "- identify whether counsel, finance, delivery ops, RevOps, or founder owns final approval.",
        "",
        "### Useful Links",
        "",
        f"- Services and packages: {SERVICES_URL}",
        f"- Buyer packet: https://lolomix.github.io/contract-revenue-radar/buyer-packet.html",
        f"- Review Room: {REVIEW_ROOM_URL}",
        f"- Optional 3-finding sample first: {SAMPLE_URL}",
        f"- Demo video: {DEMO_URL}",
        "",
        "### Boundary",
        "",
        "This is business-risk review for sales, finance, delivery, and operations teams. It is not legal advice, and counsel should approve final contract language.",
    ])
    return "\n".join(lines) + "\n"


def build_b2b_approval_comment(issue_body: str) -> str:
    fields = parse_issue_form(issue_body)
    organization = fields.get("Organization / team", "Requested organization").strip() or "Requested organization"
    approver_role = fields.get("Approver role", "").strip()
    payment_route = fields.get("Payment/procurement route", "").strip()
    submitted_approval = fields.get("Approval text", "").strip()
    acknowledgement_items = checkbox_items(fields.get("Acknowledgement", ""))

    lines = [
        "## B2B Business Package Approval Response",
        "",
        "Thanks for the public-safe written approval path. This issue can be used as an approval signal, but it is not payment evidence.",
        "",
        f"- Organization/team: **{organization}**",
        "- Approved package: **B2B Business Package ($3,500)**",
    ]
    if approver_role:
        lines.append(f"- Approver role: **{truncate(approver_role, 120)}**")
    if payment_route:
        lines.append(f"- Payment/procurement route: **{truncate(payment_route, 160)}**")
    if submitted_approval:
        lines.extend(["", "### Submitted Approval Text", "", f"> {truncate(submitted_approval, 500)}"])
    if acknowledgement_items:
        lines.extend(["", "### Acknowledgement"])
        lines.extend(f"- {item}" for item in acknowledgement_items)

    lines.extend([
        "",
        "### Next Private Step",
        "",
        "Keep payment links, billing details, tax IDs, private client names, credentials, and documents out of this public issue.",
        "",
        "The next private step is to confirm one of:",
        "",
        "- private payment-link routing,",
        "- procurement approval timing,",
        "- vendor setup / purchase-order route,",
        "- funded platform order.",
        "",
        "Close-ready approval text:",
        "",
        "> Approved. I authorize the $3,500 B2B Business Package and understand this is business-risk review, not legal advice.",
        "",
        "### Boundary",
        "",
        "This approval path is business-risk review for sales, finance, delivery, and operations teams. It is not legal advice, and counsel should approve final contract language.",
    ])
    return "\n".join(lines) + "\n"


def build_paid_review_start_comment(issue_body: str) -> str:
    fields = parse_issue_form(issue_body)
    organization = fields.get("Organization / team", "Requested organization").strip() or "Requested organization"
    selected_package = fields.get("Paid review package", "Not sure - recommend the right scope").strip()
    requester_role = fields.get("Requester / approver role", "").strip()
    document_count = fields.get("Approximate document/template count", "").strip()
    top_risks = fields.get("Top risk areas", "").strip()
    route = fields.get("Payment/procurement route", "").strip()
    target_start = fields.get("Target start window", "").strip()
    acknowledgement = checkbox_items(fields.get("Acknowledgement", ""))

    lines = [
        "## Paid Review Start Response",
        "",
        "Thanks for opening a paid review start request. This is the public-safe routing step before private payment/procurement and document intake.",
        "",
        f"- Organization/team: **{organization}**",
        f"- Requested package: **{truncate(selected_package, 120)}**",
    ]
    if requester_role:
        lines.append(f"- Requester/approver role: **{truncate(requester_role, 120)}**")
    if document_count:
        lines.append(f"- Approximate document/template count: **{truncate(document_count, 180)}**")
    if top_risks:
        lines.append(f"- Top risk areas: {truncate(top_risks, 260)}")
    if route:
        lines.append(f"- Payment/procurement route: **{truncate(route, 180)}**")
    if target_start:
        lines.append(f"- Target start window: **{truncate(target_start, 100)}**")
    if acknowledgement:
        lines.extend(["", "### Acknowledgement"])
        lines.extend(f"- {item}" for item in acknowledgement)

    lines.extend([
        "",
        "### Recommended Next Step",
        "",
        "Use a private route for payment/procurement and redacted document intake. Keep this public issue limited to scope, package, timeline, and role-based routing.",
        "",
        "Close-ready approval text for the selected package:",
        "",
        f"> {approval_language_for_package(selected_package)}",
        "",
        "Private details needed next:",
        "",
        "- authorized approver name and role,",
        "- payer or company name,",
        "- billing/procurement contact or approved payment route,",
        "- private intake method for redacted files,",
        "- target start date and delivery owner.",
        "",
        "### Useful Links",
        "",
        f"- Buyer packet: https://lolomix.github.io/contract-revenue-radar/buyer-packet.html",
        f"- Services: {SERVICES_URL}",
        f"- Sample deliverable: https://lolomix.github.io/contract-revenue-radar/b2b-package-sample.html",
        f"- Approval packet: {APPROVAL_PACKET_URL}",
        "",
        "### Boundary",
        "",
        "This is business-risk review for sales, finance, delivery, and operations teams. It is not legal advice, and counsel should approve final contract language.",
    ])
    return "\n".join(lines) + "\n"


def build_sprint_comment(issue_body: str) -> str:
    fields = parse_issue_form(issue_body)
    if "Paid review package" in fields:
        return build_paid_review_start_comment(issue_body)
    if "Approval text" in fields and "Payment/procurement route" in fields:
        return build_b2b_approval_comment(issue_body)
    if "Approval/payment route" in fields:
        return build_b2b_package_comment(issue_body)
    if "Selected package" in fields:
        return build_service_package_comment(issue_body)
    organization = fields.get("Organization / team", "Requested organization").strip() or "Requested organization"
    volume = fields.get("Approximate document/template count", "").strip()
    deal_motion = fields.get("Deal or delivery motion", "").strip()
    desired_output = fields.get("Desired output", "").strip()
    fit_items = checkbox_items(fields.get("Sprint fit", ""))
    requester_role = fields.get("Requester role", "").strip()
    procurement_path = fields.get("Approval or procurement path", "").strip()
    preferred_start = fields.get("Preferred start window", "").strip()
    delivery_priorities = fields.get("Delivery priorities", "").strip()
    approval_items = checkbox_items(fields.get("Approval readiness", ""))
    is_invoice_request = bool(procurement_path or preferred_start or delivery_priorities or approval_items)

    lines = [
        "## Revenue Protection Sprint Invoice Path Response" if is_invoice_request else "## Revenue Protection Sprint Intake Response",
        "",
        "Thanks for the sprint request. This response confirms the fixed-scope package and the information needed before work can start.",
        "",
        f"- Organization/team: **{organization}**",
    ]
    if requester_role:
        lines.append(f"- Requester role: **{truncate(requester_role, 120)}**")
    if volume:
        lines.append(f"- Approximate document/template count: **{truncate(volume, 180)}**")
    if deal_motion:
        lines.append(f"- Deal or delivery motion: {truncate(deal_motion, 260)}")
    if desired_output:
        lines.append(f"- Desired output: {truncate(desired_output, 260)}")
    if preferred_start:
        lines.append(f"- Preferred start window: **{truncate(preferred_start, 80)}**")
    if procurement_path:
        lines.append(f"- Approval/procurement path: {truncate(procurement_path, 260)}")
    if delivery_priorities:
        lines.append(f"- Delivery priorities: {truncate(delivery_priorities, 260)}")

    if fit_items:
        lines.extend(["", "### Fit Signals"])
        lines.extend(f"- {item}" for item in fit_items)
    if approval_items:
        lines.extend(["", "### Approval Readiness"])
        lines.extend(f"- {item}" for item in approval_items)

    lines.extend([
        "",
        "### Recommended Scope",
        "",
        "**Revenue Protection Sprint - $5,000 fixed scope**",
        "",
        "- Review 15-25 redacted SOWs, MSAs, order forms, retainers, addenda, or implementation-template excerpts.",
        "- Flag payment timing, acceptance, customer dependency, scope creep, renewal, credit/refund, data/security, and reusable-IP risks.",
        "- Return exact excerpts, severity, business impact, and recommended fallback positions.",
        "- Produce a reusable clause playbook and sales/ops intake checklist.",
        "- Include a 60-minute review session.",
        "- Target turnaround: 5 business days after document intake and payment/procurement approval.",
        "",
        "If the final scope is only one document or a small set, start with a smaller audit instead of the $5,000 sprint. The sprint is strongest when there are multiple recurring templates or variants.",
        "",
        "### Invoice / Approval Path",
        "",
        "If this request is ready for invoice or procurement routing, keep private billing details out of this public issue. The next private step is to confirm:",
        "",
        "- payer or company name for invoice/vendor setup,",
        "- role-based billing contact or procurement path,",
        "- payment method or purchase-order requirement,",
        "- private document intake path for redacted templates/excerpts,",
        "- business owner for priorities and review-call scheduling.",
        "",
        "### What To Send Next",
        "",
        "Do **not** post private documents in this public issue. Use a private transfer path for redacted files once the engagement is approved.",
        "",
        "Needed next:",
        "",
        "- billing contact and preferred payment/procurement path,",
        "- whether a W-9/vendor setup is required,",
        "- secure/private document intake method,",
        "- target delivery date,",
        "- whether counsel, finance, delivery ops, or RevOps owns final approval.",
        "",
        "### Approval Language",
        "",
        "To authorize the sprint, an authorized business contact can reply privately or in the chosen procurement path with:",
        "",
        f"> {APPROVAL_LANGUAGE}",
        "",
        "### Useful Links",
        "",
        f"- Sprint scope: {SPRINT_URL}",
        f"- Paid service package intake: {SERVICE_PACKAGE_URL}",
        f"- Approval packet: {APPROVAL_PACKET_URL}",
        f"- Request invoice/approval path: {INVOICE_REQUEST_URL}",
        f"- Public intake options: {INTAKE_URL}",
        f"- Optional 3-finding sample first: {SAMPLE_URL}",
        f"- Demo video: {DEMO_URL}",
        "",
        "### Boundary",
        "",
        "This is business-risk review for sales, finance, delivery, and operations teams. It is not legal advice, and counsel should approve final contract language.",
    ])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print("Usage: sprint_inquiry_reply.py GITHUB_EVENT_JSON", file=sys.stderr)
        return 2
    event = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    body = event.get("issue", {}).get("body", "")
    sys.stdout.write(build_sprint_comment(body))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
