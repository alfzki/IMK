"""Evidence matcher that retrieves supporting/contradicting corpus passages using hybrid search."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, List, Optional

from calm_carson.verify.decomposer import extract_citations, extract_quantities
from calm_carson.verify.models import EvidenceMatch, FactClaim

logger = logging.getLogger(__name__)


class EvidenceMatcher:
    """Matches factual claims against local corpus passages using MarkdownHybridSearchEngine."""

    def __init__(self, workspace_root: Optional[Path] = None, search_engine: Optional[Any] = None):
        if workspace_root is None:
            self.workspace_root = Path(__file__).resolve().parent.parent.parent.parent
        else:
            self.workspace_root = Path(workspace_root)

        if search_engine is not None:
            self.search_engine = search_engine
        else:
            try:
                from calm_carson.search.hybrid import MarkdownHybridSearchEngine
                index_dir = self.workspace_root / "literature" / "search_index"
                self.search_engine = MarkdownHybridSearchEngine(index_dir=str(index_dir))
            except Exception as e:
                logger.warning("Could not initialize hybrid search engine: %s", e)
                self.search_engine = None

    def match_claim(self, claim: FactClaim, top_k: int = 4) -> List[EvidenceMatch]:
        """Finds top candidate evidence text passages for a given claim."""
        if self.search_engine is None:
            return []

        # Construct query from claim text and numbers
        query = claim.claim_text
        if claim.extracted_numbers:
            # Append salient numbers to boost BM25 keyword matching on statistics
            num_tokens = " ".join(claim.extracted_numbers[:3])
            query = f"{claim.claim_text} {num_tokens}"

        try:
            results = self.search_engine.search(query, top_k=top_k, mode="hybrid")
        except Exception as e:
            logger.warning("Search query failed for claim '%s': %s", claim.id, e)
            return []

        matches: List[EvidenceMatch] = []
        for r in results:
            content = r.content
            evidence_numbers = extract_quantities(content)
            evidence_citations = extract_citations(content)

            # Check overlap between claim numbers and evidence numbers
            matched_nums = [n for n in claim.extracted_numbers if n in evidence_numbers]

            file_path = getattr(r, "doc_path", getattr(r, "file_path", ""))
            score = getattr(r, "rrf_score", getattr(r, "score", 0.0))

            matches.append(
                EvidenceMatch(
                    file_path=file_path,
                    start_line=r.start_line,
                    end_line=r.end_line,
                    breadcrumb=r.breadcrumb,
                    content=content,
                    similarity_score=score,
                    matched_numbers=matched_nums,
                    extracted_citations=evidence_citations,
                )
            )

        return matches
