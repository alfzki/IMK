"""Data models for research originality evaluation against global literature."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class PublicationMatch:
    """Represents a retrieved global scientific publication with similarity metrics."""

    id: str
    title: str
    authors: List[str]
    year: int
    venue: str
    doi: Optional[str]
    url: Optional[str]
    abstract: str
    citation_count: int
    similarity_score: float  # 0.0 to 1.0
    overlap_level: str  # "HIGH" (>= 0.70), "MODERATE" (0.45-0.69), "LOW" (< 0.45)
    source_database: str = "openalex"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DifferentiationFeedback:
    """Actionable feedback along a specific research dimension to enhance novelty."""

    dimension: str  # e.g., "methodology_algorithm", "data_characteristics", "dsrm_system_engineering", "regulatory_compliance", "evaluation_metrics"
    dimension_name: str
    overlap_analysis: str
    recommended_differentiation: str
    actionable_guidance: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class OriginalityReport:
    """Comprehensive report summarizing originality evaluation, overlaps, and differentiation advice."""

    idea_text: str
    generated_queries: List[str]
    matches: List[PublicationMatch]
    max_similarity: float
    mean_similarity: float
    overall_risk: str  # "HIGH_OVERLAP", "MODERATE_OVERLAP", "DISTINCT_NOVEL"
    risk_summary: str
    differentiation_feedbacks: List[DifferentiationFeedback]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


    @property
    def high_overlap_count(self) -> int:
        return sum(1 for m in self.matches if m.overlap_level == "HIGH")

    @property
    def moderate_overlap_count(self) -> int:
        return sum(1 for m in self.matches if m.overlap_level == "MODERATE")

    @property
    def low_overlap_count(self) -> int:
        return sum(1 for m in self.matches if m.overlap_level == "LOW")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "idea_text": self.idea_text,
            "generated_queries": self.generated_queries,
            "max_similarity": round(self.max_similarity, 4),
            "mean_similarity": round(self.mean_similarity, 4),
            "overall_risk": self.overall_risk,
            "risk_summary": self.risk_summary,
            "high_overlap_count": self.high_overlap_count,
            "moderate_overlap_count": self.moderate_overlap_count,
            "low_overlap_count": self.low_overlap_count,
            "total_matches": len(self.matches),
            "matches": [m.to_dict() for m in self.matches],
            "differentiation_feedbacks": [df.to_dict() for df in self.differentiation_feedbacks],
            "timestamp": self.timestamp,
        }
