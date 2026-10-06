"""Originality and novelty verification module for thesis research topics."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from calm_carson.originality.evaluator import OriginalityEvaluator
from calm_carson.originality.exporter import OriginalityExporter
from calm_carson.originality.models import (
    DifferentiationFeedback,
    OriginalityReport,
    PublicationMatch,
)
from calm_carson.originality.searcher import GlobalLiteratureSearcher


def check_topic_originality(
    idea_text: str,
    workspace_root: Optional[Path] = None,
    min_year: int = 2021,
    max_year: int = 2026,
    limit: int = 10,
    export_files: bool = True,
) -> OriginalityReport:
    """End-to-end pipeline to check research topic originality against global academic literature."""
    searcher = GlobalLiteratureSearcher(workspace_root=workspace_root)
    queries = searcher.formulate_search_queries(idea_text)

    # Search global publications via OpenAlex
    global_pubs = searcher.search_openalex(
        queries=queries,
        min_year=min_year,
        max_year=max_year,
        limit_per_query=max(4, limit // len(queries) + 1) if queries else 6,
    )

    # Search academic archives (Semantic Scholar & CORE)
    academic_pubs = searcher.search_academic_archives(
        queries=queries,
        min_year=min_year,
        max_year=max_year,
        limit_per_query=2,
    )

    # Cross-reference with local STIS theses
    local_pubs = searcher.search_local_theses(idea_text, limit=3)
    all_pubs = global_pubs + academic_pubs + local_pubs

    # Evaluate similarities and overlap risks
    evaluator = OriginalityEvaluator()
    report = evaluator.evaluate(
        idea_text=idea_text,
        raw_publications=all_pubs,
        generated_queries=queries,
    )

    # Export if requested
    if export_files:
        exporter = OriginalityExporter(workspace_root=workspace_root)
        exporter.export_json(report)
        exporter.export_markdown(report)

    return report


__all__ = [
    "PublicationMatch",
    "DifferentiationFeedback",
    "OriginalityReport",
    "GlobalLiteratureSearcher",
    "OriginalityEvaluator",
    "OriginalityExporter",
    "check_topic_originality",
]
