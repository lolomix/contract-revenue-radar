from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

from .agent_workflow import AgentBrief, build_agent_brief, render_agent_brief
from .core import AuditReport


@dataclass(frozen=True)
class ClauseMemory:
    memory_id: str
    risk_type: str
    approved_fallback: str
    approver_role: str
    applies_to_segment: str = ""
    active: bool = True
    created_at: str = ""
    expires_at: str = ""
    source_decision: str = ""


@dataclass(frozen=True)
class MemoryAgentResult:
    report: AuditReport
    brief: AgentBrief
    recalled_memories: tuple[ClauseMemory, ...]


def load_memories(path: Path | str) -> tuple[ClauseMemory, ...]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Memory file must contain a JSON list of memory records")
    return tuple(_memory_from_dict(item) for item in payload)


def recall_memories(
    report: AuditReport,
    memories: tuple[ClauseMemory, ...] | list[ClauseMemory],
    segment: str = "",
    limit: int = 5,
) -> tuple[ClauseMemory, ...]:
    risk_order = _risk_order(report)
    risk_types = set(risk_order)
    normalized_segment = _normalize(segment)

    candidates = [
        memory
        for memory in memories
        if memory.active
        and memory.risk_type in risk_types
        and _segment_matches(memory.applies_to_segment, normalized_segment)
    ]
    candidates.sort(
        key=lambda memory: (
            risk_order.get(memory.risk_type, 999),
            0 if memory.applies_to_segment else 1,
            memory.created_at,
            memory.memory_id,
        )
    )
    return tuple(candidates[:limit])


def build_memory_agent_result(
    report: AuditReport,
    memories: tuple[ClauseMemory, ...] | list[ClauseMemory],
    segment: str = "",
) -> MemoryAgentResult:
    return MemoryAgentResult(
        report=report,
        brief=build_agent_brief(report),
        recalled_memories=recall_memories(report, memories, segment=segment),
    )


def render_memory_agent_report(result: MemoryAgentResult) -> str:
    lines = [
        "# Revenue Terms Memory Agent Report",
        "",
        "## Audit Summary",
        "",
        f"- Backend: {result.report.backend}",
        f"- Revenue risk score: {result.report.risk_score}/100",
        f"- Sections searched: {result.report.searched_sections}",
        f"- Findings: {len(result.report.findings)}",
        "",
        "## Recalled Approved Memories",
    ]
    if result.recalled_memories:
        for memory in result.recalled_memories:
            segment = memory.applies_to_segment or "all segments"
            expiry = f"; expires {memory.expires_at}" if memory.expires_at else ""
            source = f"; source: {memory.source_decision}" if memory.source_decision else ""
            lines.append(
                "- "
                f"{memory.memory_id} ({memory.risk_type}, {segment}, approved by {memory.approver_role}{expiry}{source}): "
                f"{memory.approved_fallback}"
            )
    else:
        lines.append("- No active approved memory matched the detected risk types.")

    lines.extend(["", render_agent_brief(result.brief).strip(), ""])
    return "\n".join(lines)


def _memory_from_dict(item: object) -> ClauseMemory:
    if not isinstance(item, dict):
        raise ValueError("Each memory record must be a JSON object")
    required = ("memory_id", "risk_type", "approved_fallback", "approver_role")
    missing = [field for field in required if not item.get(field)]
    if missing:
        raise ValueError(f"Memory record missing required field(s): {', '.join(missing)}")
    return ClauseMemory(
        memory_id=str(item["memory_id"]),
        risk_type=str(item["risk_type"]),
        approved_fallback=str(item["approved_fallback"]),
        approver_role=str(item["approver_role"]),
        applies_to_segment=str(item.get("applies_to_segment", "")),
        active=bool(item.get("active", True)),
        created_at=str(item.get("created_at", "")),
        expires_at=str(item.get("expires_at", "")),
        source_decision=str(item.get("source_decision", "")),
    )


def _risk_order(report: AuditReport) -> dict[str, int]:
    order: dict[str, int] = {}
    for finding in report.findings:
        if finding.risk_type not in order:
            order[finding.risk_type] = len(order)
    return order


def _segment_matches(memory_segment: str, normalized_segment: str) -> bool:
    normalized_memory_segment = _normalize(memory_segment)
    if not normalized_memory_segment:
        return True
    if not normalized_segment:
        return False
    return (
        normalized_memory_segment in normalized_segment
        or normalized_segment in normalized_memory_segment
    )


def _normalize(value: str) -> str:
    return " ".join(value.lower().split())
