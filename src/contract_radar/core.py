from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
import math
import re
from typing import Iterable, Sequence


RISK_PATTERNS = {
    "payment_delay": {
        "severity": 5,
        "label": "Payment delay",
        "terms": [
            "net 60",
            "net 90",
            "upon acceptance",
            "after acceptance",
            "after approval",
            "withhold",
            "retainage",
            "payment may be delayed",
            "sole discretion",
        ],
        "why": "Cash conversion risk: payment timing depends on buyer action or long terms.",
        "action": "Ask for Net 15/30, milestone billing, or acceptance deemed after a fixed review window.",
    },
    "renewal_loss": {
        "severity": 4,
        "label": "Renewal loss",
        "terms": [
            "non-renew",
            "non renew",
            "auto-renewal disabled",
            "terminate for convenience",
            "30 days notice",
            "without cause",
            "month-to-month",
        ],
        "why": "Retention risk: the customer can leave quickly or renewal is not protected.",
        "action": "Add annual renewal, longer notice, migration fee, or success review before termination.",
    },
    "scope_creep": {
        "severity": 4,
        "label": "Scope creep",
        "terms": [
            "reasonable requests",
            "as requested",
            "unlimited revisions",
            "all necessary",
            "additional support",
            "included at no charge",
        ],
        "why": "Margin risk: vague service language can expand work without expanding fees.",
        "action": "Define change orders, revision limits, support hours, and out-of-scope rates.",
    },
    "refund_credit": {
        "severity": 3,
        "label": "Refund or credit exposure",
        "terms": [
            "full refund",
            "service credits",
            "money back",
            "chargeback",
            "refund at customer",
            "credit against future invoices",
        ],
        "why": "Revenue leakage risk: broad refund or credit language can erase earned revenue.",
        "action": "Tie credits to measurable SLA misses and cap credits to monthly fees paid.",
    },
    "data_security": {
        "severity": 3,
        "label": "Data/security blocker",
        "terms": [
            "personal data",
            "hipaa",
            "confidential information",
            "security incident",
            "audit rights",
            "subprocessor",
            "delete all data",
        ],
        "why": "Sales cycle risk: security or data terms can block signature if not answered quickly.",
        "action": "Prepare a security appendix, DPA, incident process, and approved subprocessor list.",
    },
    "ip_ownership": {
        "severity": 4,
        "label": "IP ownership trap",
        "terms": [
            "work made for hire",
            "work for hire",
            "all intellectual property",
            "assigns to customer",
            "assigns all rights",
            "no rights retained",
            "perpetual license",
            "irrevocable assignment",
            "client owns all work product",
            "all deliverables become property",
        ],
        "why": "Revenue and reuse risk: broad IP assignment prevents the agency from reusing methodologies, code patterns, frameworks, or IP developed on the engagement in future client work, directly eroding future margins.",
        "action": "Carve out pre-existing IP, tools, methodologies, and generic components; grant a limited non-exclusive license instead of full assignment; retain ownership of reusable assets.",
    },
    "renewal_fee_trap": {
        "severity": 3,
        "label": "Auto-renewal fee escalation",
        "terms": [
            "auto renew",
            "automatically renews",
            "renewal term",
            "then-current rates",
            "price increase",
            "annual price adjustment",
            "unless terminated",
            "successive renewal periods",
            "renewal at then current",
        ],
        "why": "Hidden cost and retention risk: automatic renewal at escalated 'then-current' rates or without price caps locks clients into compounding fees and removes leverage for renegotiation.",
        "action": "Require explicit written renewal election, cap annual increases (e.g. CPI or 3%), provide easy 30-60 day opt-out, and keep renewal pricing fixed for initial term.",
    },
}


PROTECTIVE_PATTERNS = {
    "payment_delay": [
        "net 15",
        "50 percent at signature",
        "deemed accepted",
        "five business days",
    ],
    "renewal_loss": [
        "renews annually",
        "60 days notice",
        "termination for convenience is not available",
        "active annual term",
    ],
    "scope_creep": [
        "written change order",
        "outside exhibit",
        "requires a written change order",
    ],
    "refund_credit": [
        "sole remedy",
        "capped at",
        "verified sla misses",
    ],
    "data_security": [
        "approved subprocessor",
        "security appendix",
        "incident process",
    ],
    "ip_ownership": [
        "pre-existing ip",
        "retains all rights",
        "license only",
        "methodologies remain vendor",
        "vendor retains ownership",
        "background ip",
    ],
    "renewal_fee_trap": [
        "fixed pricing",
        "no automatic increase",
        "mutual renewal",
        "price cap on renewal",
        "renewal pricing fixed",
        "capped at",
    ],
}


@dataclass(frozen=True)
class ContractSection:
    """A chunk of contract text with stable metadata."""

    section_id: str
    source: str
    heading: str
    text: str


@dataclass(frozen=True)
class AuditFinding:
    risk_type: str
    label: str
    severity: int
    score: float
    source: str
    heading: str
    excerpt: str
    why: str
    action: str
    matched_terms: tuple[str, ...]


@dataclass(frozen=True)
class AuditReport:
    findings: tuple[AuditFinding, ...]
    searched_sections: int
    backend: str

    @property
    def risk_score(self) -> int:
        raw = sum(f.severity * max(f.score, 0.2) for f in self.findings)
        return min(100, round(raw * 8))

    @property
    def top_actions(self) -> tuple[str, ...]:
        seen: set[str] = set()
        actions: list[str] = []
        for finding in self.findings:
            if finding.action not in seen:
                actions.append(finding.action)
                seen.add(finding.action)
        return tuple(actions[:5])


class ContractRadar:
    """Finds contract clauses likely to affect revenue collection and retention."""

    def __init__(self, prefer_qdrant: bool = True) -> None:
        self._backend = _build_backend(prefer_qdrant)

    @property
    def backend_name(self) -> str:
        return self._backend.name

    def audit_paths(self, paths: Sequence[Path | str], limit_per_risk: int = 2) -> AuditReport:
        sections = []
        for path in paths:
            sections.extend(load_contract(Path(path)))
        return self.audit_sections(sections, limit_per_risk=limit_per_risk)

    def audit_sections(
        self,
        sections: Sequence[ContractSection],
        limit_per_risk: int = 2,
    ) -> AuditReport:
        self._backend.index(sections)
        findings: list[AuditFinding] = []

        for risk_type, definition in RISK_PATTERNS.items():
            query = f"{definition['label']} {' '.join(definition['terms'])}"
            candidates = self._backend.search(query, limit=limit_per_risk * 4)
            ranked = sorted(
                (
                    self._make_finding(risk_type, definition, section, score)
                    for section, score in candidates
                ),
                key=lambda f: (f.severity, f.score, len(f.matched_terms)),
                reverse=True,
            )
            findings.extend(
                finding
                for finding in ranked[: limit_per_risk * 2]
                if finding.matched_terms or finding.score >= 0.5
            )

        deduped = _dedupe_findings(findings)
        ordered = sorted(deduped, key=lambda f: (f.severity, f.score), reverse=True)
        return AuditReport(
            findings=tuple(ordered),
            searched_sections=len(sections),
            backend=self.backend_name,
        )

    def _make_finding(
        self,
        risk_type: str,
        definition: dict[str, object],
        section: ContractSection,
        score: float,
    ) -> AuditFinding:
        text_lower = section.text.lower()
        matched_terms = tuple(
            term for term in definition["terms"] if str(term).lower() in text_lower
        )
        protective_terms = PROTECTIVE_PATTERNS.get(risk_type, [])
        mitigation_hits = sum(1 for term in protective_terms if term in text_lower)
        adjusted_score = max(0.0, score - (mitigation_hits * 0.25))
        adjusted_severity = max(1, int(definition["severity"]) - mitigation_hits)
        excerpt = _best_excerpt(section.text, matched_terms)
        return AuditFinding(
            risk_type=risk_type,
            label=str(definition["label"]),
            severity=adjusted_severity,
            score=round(adjusted_score, 3),
            source=section.source,
            heading=section.heading,
            excerpt=excerpt,
            why=str(definition["why"]),
            action=str(definition["action"]),
            matched_terms=matched_terms,
        )


def load_contract(path: Path) -> list[ContractSection]:
    raw = path.read_text(encoding="utf-8")
    blocks = _split_sections(raw)
    sections = []
    for index, (heading, text) in enumerate(blocks, start=1):
        digest = hashlib.sha1(f"{path}:{index}:{heading}".encode("utf-8")).hexdigest()[:10]
        sections.append(
            ContractSection(
                section_id=digest,
                source=path.name,
                heading=heading or f"Section {index}",
                text=text.strip(),
            )
        )
    return sections


def render_markdown(report: AuditReport) -> str:
    lines = [
        "# Contract Revenue Radar Report",
        "",
        f"- Backend: {report.backend}",
        f"- Sections searched: {report.searched_sections}",
        f"- Revenue risk score: {report.risk_score}/100",
        "",
        "## Priority Actions",
    ]
    for action in report.top_actions:
        lines.append(f"- {action}")

    lines.extend(["", "## Findings"])
    for finding in report.findings:
        terms = ", ".join(finding.matched_terms) if finding.matched_terms else "semantic match"
        lines.extend(
            [
                "",
                f"### {finding.label} - severity {finding.severity}/5",
                f"- Source: {finding.source} / {finding.heading}",
                f"- Match score: {finding.score}",
                f"- Matched terms: {terms}",
                f"- Why it matters: {finding.why}",
                f"- Recommended move: {finding.action}",
                "",
                "> " + finding.excerpt.replace("\n", " "),
            ]
        )
    return "\n".join(lines).strip() + "\n"


def _split_sections(raw: str) -> list[tuple[str, str]]:
    cleaned = raw.replace("\r\n", "\n").strip()
    heading_pattern = re.compile(r"(?m)^(#{1,3}\s+.+|[0-9]+[.)]\s+.+)$")
    matches = list(heading_pattern.finditer(cleaned))
    if not matches:
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", cleaned) if p.strip()]
        return [(f"Paragraph {idx}", paragraph) for idx, paragraph in enumerate(paragraphs, 1)]

    sections: list[tuple[str, str]] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(cleaned)
        heading = match.group(0).lstrip("#").strip()
        body = cleaned[start:end].strip()
        if body:
            sections.append((heading, body))
    return sections or [("Document", cleaned)]


def _best_excerpt(text: str, matched_terms: Iterable[str], width: int = 280) -> str:
    lower = text.lower()
    positions = [lower.find(term.lower()) for term in matched_terms if lower.find(term.lower()) >= 0]
    if positions:
        center = min(positions)
        start = max(0, center - width // 3)
    else:
        start = 0
    excerpt = text[start : start + width].strip()
    if start > 0:
        excerpt = "... " + excerpt
    if start + width < len(text):
        excerpt += " ..."
    return re.sub(r"\s+", " ", excerpt)


def _dedupe_findings(findings: Sequence[AuditFinding]) -> list[AuditFinding]:
    best: dict[tuple[str, str, str], AuditFinding] = {}
    for finding in findings:
        key = (finding.risk_type, finding.source, finding.heading)
        current = best.get(key)
        if current is None or finding.score > current.score:
            best[key] = finding
    return list(best.values())


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]{2,}", text.lower())


def _hash_embedding(text: str, size: int = 96) -> list[float]:
    vector = [0.0] * size
    tokens = _tokenize(text)
    for token in tokens:
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
        bucket = int.from_bytes(digest[:4], "big") % size
        sign = 1 if digest[-1] % 2 == 0 else -1
        vector[bucket] += sign * (1.0 + math.log1p(len(token)))
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def _cosine(left: Sequence[float], right: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


class _MemoryBackend:
    name = "local-hash-vector-fallback"

    def __init__(self) -> None:
        self._rows: list[tuple[ContractSection, list[float]]] = []

    def index(self, sections: Sequence[ContractSection]) -> None:
        self._rows = [(section, _hash_embedding(section.text)) for section in sections]

    def search(self, query: str, limit: int) -> list[tuple[ContractSection, float]]:
        query_vector = _hash_embedding(query)
        scored = [
            (section, _cosine(query_vector, vector) + _keyword_boost(query, section.text))
            for section, vector in self._rows
        ]
        return sorted(scored, key=lambda row: row[1], reverse=True)[:limit]


class _QdrantBackend:
    name = "qdrant-local-memory"

    def __init__(self) -> None:
        from qdrant_client import QdrantClient, models

        self._client = QdrantClient(":memory:")
        self._models = models
        self._collection = "contract_revenue_radar"
        self._sections: dict[int, ContractSection] = {}

    def index(self, sections: Sequence[ContractSection]) -> None:
        models = self._models
        self._sections = {idx: section for idx, section in enumerate(sections)}
        if self._client.collection_exists(self._collection):
            self._client.delete_collection(self._collection)
        self._client.create_collection(
            collection_name=self._collection,
            vectors_config=models.VectorParams(size=96, distance=models.Distance.COSINE),
        )
        points = [
            models.PointStruct(
                id=idx,
                vector=_hash_embedding(section.text),
                payload={
                    "source": section.source,
                    "heading": section.heading,
                    "text": section.text,
                },
            )
            for idx, section in self._sections.items()
        ]
        if points:
            self._client.upsert(self._collection, points=points, wait=True)

    def search(self, query: str, limit: int) -> list[tuple[ContractSection, float]]:
        query_vector = _hash_embedding(query)
        result = self._client.query_points(
            collection_name=self._collection,
            query=query_vector,
            limit=limit,
            with_payload=True,
        ).points
        rows: list[tuple[ContractSection, float]] = []
        for point in result:
            section = self._sections[int(point.id)]
            rows.append((section, float(point.score) + _keyword_boost(query, section.text)))
        return rows


def _keyword_boost(query: str, text: str) -> float:
    """Improved keyword boost for better UX in fallback + Qdrant hybrid scoring.

    - Term overlap with length normalization
    - Bonus for exact multi-word phrase hits (e.g. "net 90", "work made for hire")
    - Slight saturation to avoid over-boosting very long sections
    """
    query_terms = set(_tokenize(query))
    text_terms = set(_tokenize(text))
    if not query_terms:
        return 0.0

    overlap = len(query_terms & text_terms) / len(query_terms)
    base = min(0.32, overlap * 0.38)

    # Phrase bonus: look for 2+ word contiguous phrases from query
    phrase_bonus = 0.0
    q_lower = query.lower()
    t_lower = text.lower()
    for phrase in [p for p in q_lower.split() if len(p) > 3]:
        # simple 2-gram style check on common risk phrases
        if phrase in t_lower:
            phrase_bonus += 0.04
    # exact famous phrases
    famous_phrases = ["net 90", "net 60", "work made for hire", "then-current", "auto renew", "sole discretion"]
    for ph in famous_phrases:
        if ph in q_lower and ph in t_lower:
            phrase_bonus += 0.08

    total = min(0.48, base + phrase_bonus)
    # gentle length penalty so very long sections don't dominate
    length_penalty = min(0.06, max(0.0, (len(text) - 1200) / 20000.0))
    return max(0.0, total - length_penalty)


def _build_backend(prefer_qdrant: bool):
    if prefer_qdrant:
        try:
            return _QdrantBackend()
        except Exception:
            pass
    return _MemoryBackend()

