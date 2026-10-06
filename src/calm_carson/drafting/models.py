"""Data models for thesis chapter drafting, outline hierarchy, evidence, and workflow state."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class SubSectionOutline:
    """Outline for a specific subsection within a thesis chapter."""

    id: str
    title: str
    focus_points: List[str]
    target_quantities: List[str] = field(default_factory=list)
    search_queries: List[str] = field(default_factory=list)
    estimated_paragraphs: int = 2

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ChapterOutline:
    """Outline for an entire thesis/proposal chapter."""

    id: str
    number: int
    title: str
    academic_goal: str
    subsections: List[SubSectionOutline] = field(default_factory=list)
    estimated_words: int = 1500

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvidenceItem:
    """A passage of evidence extracted from local corpus or theses database."""

    source: str
    content: str
    line_reference: str
    relevance_score: float
    extracted_citations: List[str] = field(default_factory=list)
    extracted_numbers: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SectionDraft:
    """Draft state for a chapter or section including verification and revision history."""

    chapter_id: str
    chapter_title: str
    raw_draft: str
    verified_draft: str
    final_draft: str
    status: str  # DRAFTED, VERIFIED, REVISED, APPROVED, EDITED
    evidences_used: List[EvidenceItem] = field(default_factory=list)
    verification_summary: Optional[Dict[str, Any]] = None
    style_summary: Optional[Dict[str, Any]] = None
    revision_count: int = 0
    user_notes: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class WorkflowState:
    """Persistent state tracking the multi-chapter drafting workflow."""

    session_id: str
    topic_id: str
    topic_title: str
    topic_cluster: str
    scope: str = "proposal"  # "proposal" (Bab 1-3) or "thesis" (Bab 1-5)
    current_chapter_idx: int = 0
    chapters_total: int = 3
    chapters_completed: List[str] = field(default_factory=list)
    chapter_drafts: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    output_dir: str = "drafts"
    last_updated: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    is_completed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def save(self, filepath: Path | str) -> None:
        """Saves workflow state to JSON file."""
        p = Path(filepath)
        p.parent.mkdir(parents=True, exist_ok=True)
        self.last_updated = datetime.now(timezone.utc).isoformat()
        with open(p, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, filepath: Path | str) -> WorkflowState:
        """Loads workflow state from JSON file."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)
