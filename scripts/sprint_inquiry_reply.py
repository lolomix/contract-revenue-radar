#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from issue_sample_audit import INTAKE_URL, SPRINT_URL, parse_issue_form, truncate


SAMPLE_URL = "https://github.com/lolomix/contract-revenue-radar/issues/new?template=free-sample-audit.yml"
APPROVAL_PACKET_URL = "https://lolomix.github.io/contract-revenue-radar/approval-packet.html"
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


def build_sprint_comment(issue_body: str) -> str:
    fields = parse_issue_form(issue_body)
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
