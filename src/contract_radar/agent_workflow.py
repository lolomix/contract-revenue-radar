from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .core import AuditFinding, AuditReport, ContractRadar


FALLBACK_POSITIONS = {
    "payment_delay": (
        "Replace open-ended acceptance with deemed acceptance after 5 business days. "
        "Use Net 15 or milestone billing for implementation work."
    ),
    "renewal_loss": (
        "Move month-to-month service terms to annual renewal where possible. "
        "Use at least 60 days notice before non-renewal."
    ),
    "scope_creep": (
        "Add a written change-order requirement for work outside the SOW. "
        "Define included support hours, revision limits, and out-of-scope rates."
    ),
    "refund_credit": (
        "Cap credits to fees paid for the affected month. "
        "Make credits the sole remedy for verified SLA misses."
    ),
    "data_security": (
        "Route security terms to a standard security appendix, DPA, incident process, "
        "and approved subprocessor list."
    ),
    "ip_ownership": (
        "Carve out pre-existing IP, tools, methodologies, and generic components. "
        "Grant limited license only; retain ownership of reusable IP and background assets."
    ),
    "renewal_fee_trap": (
        "Require explicit written renewal election. Cap annual price increases at CPI or 3%. "
        "Add easy 30-60 day opt-out without penalty and keep initial renewal pricing fixed."
    ),
}


@dataclass(frozen=True)
class AgentBrief:
    executive_summary: str
    priority_questions: tuple[str, ...]
    fallback_positions: tuple[str, ...]
    sales_ops_checklist: tuple[str, ...]


def build_agent_brief(report: AuditReport) -> AgentBrief:
    high_severity = [finding for finding in report.findings if finding.severity >= 4]
    top_labels = ", ".join(finding.label.lower() for finding in high_severity[:3])
    if top_labels:
        summary = (
            f"The reviewed documents show a {report.risk_score}/100 revenue risk score. "
            f"Highest-priority issues: {top_labels}. Route these clauses through business "
            "review before legal markup."
        )
    else:
        summary = (
            f"The reviewed documents show a {report.risk_score}/100 revenue risk score. "
            "No severe risk class dominated the review, but the checklist should still be used."
        )

    questions = tuple(_question_for(finding) for finding in report.findings[:5])
    fallbacks = []
    seen = set()
    for finding in report.findings:
        fallback = FALLBACK_POSITIONS.get(finding.risk_type)
        if fallback and fallback not in seen:
            fallbacks.append(fallback)
            seen.add(fallback)

    checklist = (
        "Confirm payment due date is not dependent on unilateral customer acceptance.",
        "Confirm change requests require written approval before work begins.",
        "Confirm renewals, non-renewals, and convenience termination have business owner approval.",
        "Confirm credits, refunds, or SLA remedies are capped.",
        "Confirm data/security obligations map to an approved appendix or review owner.",
        "Confirm IP clauses carve out pre-existing tools/methods and avoid full assignment of reusable work.",
        "Confirm auto-renewal terms include explicit election, price caps, and easy opt-out.",
    )
    return AgentBrief(
        executive_summary=summary,
        priority_questions=questions,
        fallback_positions=tuple(fallbacks[:5]),
        sales_ops_checklist=checklist,
    )


def render_agent_brief(brief: AgentBrief) -> str:
    lines = [
        "# Revenue Risk Agent Brief",
        "",
        "## Executive Summary",
        "",
        brief.executive_summary,
        "",
        "## Priority Questions",
    ]
    lines.extend(f"- {question}" for question in brief.priority_questions)
    lines.extend(["", "## Fallback Positions"])
    lines.extend(f"- {fallback}" for fallback in brief.fallback_positions)
    lines.extend(["", "## Sales/Ops Checklist"])
    lines.extend(f"- {item}" for item in brief.sales_ops_checklist)
    lines.extend(
        [
            "",
            "## Limit",
            "",
            "This is business-risk review, not legal advice. Counsel should approve final language.",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def run_agent_workflow(paths: list[Path], prefer_qdrant: bool = True) -> tuple[AuditReport, AgentBrief]:
    radar = ContractRadar(prefer_qdrant=prefer_qdrant)
    report = radar.audit_paths(paths)
    return report, build_agent_brief(report)


def _question_for(finding: AuditFinding) -> str:
    if finding.risk_type == "payment_delay":
        return f"Can {finding.source} / {finding.heading} be changed so payment is due on a fixed date or milestone?"
    if finding.risk_type == "renewal_loss":
        return f"Who approves the termination or non-renewal language in {finding.source} / {finding.heading}?"
    if finding.risk_type == "scope_creep":
        return f"Where is the change-order boundary for {finding.source} / {finding.heading}?"
    if finding.risk_type == "refund_credit":
        return f"Are credits or refunds capped in {finding.source} / {finding.heading}?"
    if finding.risk_type == "data_security":
        return f"Who owns the security and data obligations in {finding.source} / {finding.heading}?"
    if finding.risk_type == "ip_ownership":
        return f"Does {finding.source} / {finding.heading} carve out pre-existing IP and reusable methodologies for the vendor?"
    if finding.risk_type == "renewal_fee_trap":
        return f"Can {finding.source} / {finding.heading} add explicit renewal election and price caps instead of auto-escalation?"
    return f"Who owns the business decision for {finding.source} / {finding.heading}?"

