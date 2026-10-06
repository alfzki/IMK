"""Data models for research gap analysis and thesis brainstorming."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ResearchGapItem:
    """Represents an extracted research gap, limitation, or future work recommendation."""

    id: str
    source_type: str  # "stis_thesis", "intl_paper", "proposal_note"
    source_title: str
    year: str
    author: str
    cluster: str  # "security_privacy", "sdi_interoperability", "data_collection_capi", "geospatial", "dissemination_dashboard", "other"
    gap_category: str  # "open_problem", "methodological_bottleneck", "future_work"
    raw_excerpt: str
    synthesized_summary: str
    recommended_opportunity: str
    source_location: str  # filepath:line or thesis_id / url
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert dataclass to dictionary."""
        return asdict(self)


@dataclass
class BrainstormClusterSummary:
    """Aggregated summary of research gaps and opportunities per topic cluster."""

    cluster_id: str
    cluster_name: str
    open_problems: List[ResearchGapItem] = field(default_factory=list)
    methodological_bottlenecks: List[ResearchGapItem] = field(default_factory=list)
    future_works: List[ResearchGapItem] = field(default_factory=list)
    synthesized_opportunities: List[str] = field(default_factory=list)

    @property
    def total_items(self) -> int:
        return len(self.open_problems) + len(self.methodological_bottlenecks) + len(self.future_works)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cluster_id": self.cluster_id,
            "cluster_name": self.cluster_name,
            "total_items": self.total_items,
            "open_problems": [item.to_dict() for item in self.open_problems],
            "methodological_bottlenecks": [item.to_dict() for item in self.methodological_bottlenecks],
            "future_works": [item.to_dict() for item in self.future_works],
            "synthesized_opportunities": self.synthesized_opportunities,
        }
