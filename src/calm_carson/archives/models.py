"""
calm_carson.archives.models
Standard data models for multi-archive academic literature search and paper downloading.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any, Dict, List, Optional


class ArchiveTier(IntEnum):
    """Priority tiers for open archives."""
    TIER_1_ACADEMIC = 1       # Official open academic APIs (OpenAlex, arXiv, Semantic Scholar, CORE)
    TIER_2_PUBLIC_LIB = 2     # Public digital libraries (Internet Archive, Open Library, Gutenberg)
    TIER_3_SHADOW_RESOLVER = 3# Paywall resolvers & shadow repositories (Sci-Hub, LibGen, Anna's Archive)
    TIER_4_DECENTRALIZED = 4  # Decentralized transport & account-proxied (IPFS, Z-Library proxy)


class ItemCategory:
    """Category classification for academic artifacts."""
    PAPER = "paper"
    BOOK = "book"
    PREPRINT = "preprint"
    DISSERTATION = "dissertation"
    DATASET = "dataset"


@dataclass
class PaperRecord:
    """Standardized representation of a scientific publication or book across all archives."""
    id: str
    title: str
    authors: List[str] = field(default_factory=list)
    year: Optional[int] = None
    venue: str = ""
    doi: Optional[str] = None
    url: Optional[str] = None
    pdf_url: Optional[str] = None
    abstract: str = ""
    citation_count: Optional[int] = None
    source: str = ""
    source_tier: int = ArchiveTier.TIER_1_ACADEMIC
    category: str = ItemCategory.PAPER
    is_oa: bool = False
    ipfs_cid: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def get_authors_string(self, max_authors: int = 5) -> str:
        """Formats the author list into a clean readable string."""
        if not self.authors:
            return "Unknown"
        if len(self.authors) <= max_authors:
            return ", ".join(self.authors)
        return ", ".join(self.authors[:max_authors]) + " et al."

    def get_normalized_title(self) -> str:
        """Normalizes the title string for deduplication."""
        clean = re.sub(r"[^a-zA-Z0-9\s]", " ", self.title.lower())
        return " ".join(clean.split())

    def to_dict(self) -> Dict[str, Any]:
        """Converts record to JSON-serializable dictionary."""
        return {
            "id": self.id,
            "source": self.source,
            "source_tier": self.source_tier,
            "category": self.category,
            "title": self.title,
            "authors": self.get_authors_string(),
            "authors_list": self.authors,
            "year": self.year,
            "venue": self.venue,
            "doi": self.doi or "",
            "url": self.url or "",
            "pdf_url": self.pdf_url or "",
            "abstract": self.abstract,
            "citations": self.citation_count if self.citation_count is not None else "-",
            "is_oa": self.is_oa,
            "ipfs_cid": self.ipfs_cid or "",
            "extra": self.extra,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PaperRecord:
        """Constructs PaperRecord from a dictionary."""
        authors = data.get("authors_list")
        if not authors:
            raw_authors = data.get("authors", "")
            if isinstance(raw_authors, str):
                authors = [a.strip() for a in raw_authors.replace(" et al.", "").split(",") if a.strip()]
            else:
                authors = []

        citations = data.get("citations")
        if citations == "-" or citations is None:
            c_count = None
        else:
            try:
                c_count = int(citations)
            except (ValueError, TypeError):
                c_count = None

        return cls(
            id=str(data.get("id", "")),
            title=str(data.get("title", "Untitled")),
            authors=authors,
            year=data.get("year"),
            venue=str(data.get("venue", "")),
            doi=data.get("doi") or None,
            url=data.get("url") or None,
            pdf_url=data.get("pdf_url") or None,
            abstract=str(data.get("abstract", "")),
            citation_count=c_count,
            source=str(data.get("source", "Unknown")),
            source_tier=int(data.get("source_tier", ArchiveTier.TIER_1_ACADEMIC)),
            category=str(data.get("category", ItemCategory.PAPER)),
            is_oa=bool(data.get("is_oa", False)),
            ipfs_cid=data.get("ipfs_cid") or None,
            extra=data.get("extra") or {},
        )


@dataclass
class DownloadResult:
    """Encapsulates the result of a paper PDF download attempt."""
    success: bool
    filepath: Optional[str] = None
    source_used: Optional[str] = None
    filesize_bytes: int = 0
    error: Optional[str] = None
    was_fallback: bool = False
