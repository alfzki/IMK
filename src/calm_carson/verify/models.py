"""Data models for factual claim verification and citation validation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class FactClaim:
    """Represents an atomic factual proposition extracted from draft text."""

    id: str
    claim_text: str
    original_sentence: str
    start_char: int
    end_char: int
    extracted_numbers: List[str] = field(default_factory=list)
    embedded_citations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvidenceMatch:
    """Represents a text passage retrieved from the local corpus matching a claim."""

    file_path: str
    start_line: int
    end_line: int
    breadcrumb: str
    content: str
    similarity_score: float
    matched_numbers: List[str] = field(default_factory=list)
    extracted_citations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ClaimVerificationResult:
    """Verification assessment for a single factual claim."""

    claim: FactClaim
    status: str  # "SUPPORTED", "CONTRADICTED", "UNSUPPORTED"
    citation_status: str  # "VALID", "MISSING", "MISMATCH", "NOT_APPLICABLE"
    confidence_score: float
    best_evidence: Optional[EvidenceMatch]
    alternative_evidences: List[EvidenceMatch] = field(default_factory=list)
    explanation: str = ""
    correction_suggestion: Optional[str] = None
    annotated_claim: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim": self.claim.to_dict(),
            "status": self.status,
            "citation_status": self.citation_status,
            "confidence_score": round(self.confidence_score, 4),
            "best_evidence": self.best_evidence.to_dict() if self.best_evidence else None,
            "alternative_evidences": [e.to_dict() for e in self.alternative_evidences],
            "explanation": self.explanation,
            "correction_suggestion": self.correction_suggestion,
            "annotated_claim": self.annotated_claim,
        }


@dataclass
class VerificationReport:
    """Aggregate audit report for an entire verified draft text."""

    draft_text: str
    results: List[ClaimVerificationResult]
    overall_verdict: str  # "READY_FOR_SUBMISSION", "NEEDS_MINOR_CITATION", "FATAL_CONTRADICTIONS"
    verdict_summary: str
    supported_count: int
    contradicted_count: int
    unsupported_count: int
    missing_citation_count: int
    annotated_draft: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def total_claims(self) -> int:
        return len(self.results)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "draft_text": self.draft_text,
            "total_claims": self.total_claims,
            "supported_count": self.supported_count,
            "contradicted_count": self.contradicted_count,
            "unsupported_count": self.unsupported_count,
            "missing_citation_count": self.missing_citation_count,
            "overall_verdict": self.overall_verdict,
            "verdict_summary": self.verdict_summary,
            "results": [r.to_dict() for r in self.results],
            "annotated_draft": self.annotated_draft,
            "timestamp": self.timestamp,
        }
