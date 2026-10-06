"""Brainstorming and research gap analysis module for STIS thesis topics."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Tuple

from calm_carson.brainstorm.exporter import BrainstormExporter
from calm_carson.brainstorm.extractor import ResearchGapExtractor
from calm_carson.brainstorm.models import BrainstormClusterSummary, ResearchGapItem
from calm_carson.brainstorm.synthesizer import (
    CLUSTER_NAMES,
    CLUSTER_STRATEGIC_OPPORTUNITIES,
    BrainstormSynthesizer,
)


def run_brainstorm_pipeline(
    workspace_root: Optional[Path] = None,
    cluster_filter: Optional[str] = None,
    min_year: Optional[int] = 2021,
    export_files: bool = True,
) -> Tuple[List[ResearchGapItem], Dict[str, BrainstormClusterSummary]]:
    """Run full gap extraction, synthesis, and export pipeline."""
    extractor = ResearchGapExtractor(workspace_root=workspace_root)
    items = extractor.extract_all(cluster_filter=cluster_filter, min_year=min_year)

    synthesizer = BrainstormSynthesizer(items)
    summaries = synthesizer.synthesize_by_cluster()
    matrix = synthesizer.generate_research_matrix()

    if export_files:
        exporter = BrainstormExporter(workspace_root=workspace_root)
        exporter.export_json(items)
        exporter.export_csv(items)
        exporter.export_markdown_report(summaries, matrix)

    return items, summaries


__all__ = [
    "ResearchGapItem",
    "BrainstormClusterSummary",
    "ResearchGapExtractor",
    "BrainstormSynthesizer",
    "BrainstormExporter",
    "CLUSTER_NAMES",
    "CLUSTER_STRATEGIC_OPPORTUNITIES",
    "run_brainstorm_pipeline",
]
