"""
calm_carson.archives.manager
Central coordinator and parallel orchestrator for multi-archive search and retrieval.
"""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Set

from .base import BaseArchiveProvider
from .downloader import CascadingPaperDownloader
from .models import ArchiveTier, DownloadResult, ItemCategory, PaperRecord
from .providers.annas_archive import AnnasArchiveProvider
from .providers.core import CoreProvider
from .providers.gutenberg import GutenbergProvider
from .providers.internet_archive import InternetArchiveProvider
from .providers.ipfs import IPFSGatewayProvider
from .providers.libgen import LibGenProvider
from .providers.scihub import SciHubProvider
from .providers.semantic_scholar import SemanticScholarProvider
from .providers.zlibrary import ZLibraryProvider

logger = logging.getLogger(__name__)

# Category groups for convenient CLI selection
SOURCE_GROUPS = {
    "default": ["semanticscholar", "core", "internet_archive"],
    "academic": ["semanticscholar", "core"],
    "libraries": ["internet_archive"],
    "books": ["gutenberg", "internet_archive"],
    "shadow": ["scihub", "libgen", "annas_archive", "zlibrary"],
    "all": [
        "semanticscholar",
        "core",
        "internet_archive",
        "gutenberg",
        "scihub",
        "libgen",
        "annas_archive",
        "zlibrary",
    ],
}


class ArchiveManager:
    """Coordinates search across multiple open archives in parallel with deduplication."""

    def __init__(
        self,
        downloader_output_dir: str = "literature/pdfs",
        enable_fallback_download: bool = True,
        max_workers: int = 6,
    ):
        self.max_workers = max_workers
        self.downloader = CascadingPaperDownloader(
            output_dir=downloader_output_dir,
            enable_fallback=enable_fallback_download,
        )

        # Initialize provider registry
        self.providers: Dict[str, BaseArchiveProvider] = {
            "semanticscholar": SemanticScholarProvider(),
            "core": CoreProvider(),
            "internet_archive": InternetArchiveProvider(),
            "gutenberg": GutenbergProvider(),
            "scihub": SciHubProvider(),
            "libgen": LibGenProvider(),
            "annas_archive": AnnasArchiveProvider(),
            "ipfs": IPFSGatewayProvider(),
            "zlibrary": ZLibraryProvider(),
        }

    def resolve_source_names(
        self,
        sources_arg: Optional[str] = None,
        include_books: bool = False,
    ) -> List[str]:
        """Resolves user source string or presets into active provider keys."""
        if not sources_arg:
            active = list(SOURCE_GROUPS["default"])
            if include_books and "gutenberg" not in active:
                active.append("gutenberg")
            return active

        raw_tokens = [s.strip().lower() for s in sources_arg.split(",") if s.strip()]
        resolved: Set[str] = set()

        for token in raw_tokens:
            if token in SOURCE_GROUPS:
                resolved.update(SOURCE_GROUPS[token])
            elif token in self.providers:
                resolved.add(token)
            else:
                logger.warning("Sumber arsip tidak dikenal: '%s'. Dilewati.", token)

        if include_books:
            resolved.add("gutenberg")

        return list(resolved)

    def search(
        self,
        query: str,
        sources: Optional[str] = None,
        limit_per_source: int = 5,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
        include_books: bool = False,
    ) -> List[PaperRecord]:
        """
        Queries all resolved providers in parallel and returns deduplicated records.
        """
        active_keys = self.resolve_source_names(sources, include_books=include_books)
        selected_providers = [self.providers[k] for k in active_keys if k in self.providers]

        all_records: List[PaperRecord] = []

        with ThreadPoolExecutor(max_workers=min(self.max_workers, len(selected_providers) or 1)) as executor:
            future_to_provider = {
                executor.submit(
                    p.search,
                    query=query,
                    limit=limit_per_source,
                    min_year=min_year,
                    max_year=max_year,
                ): p
                for p in selected_providers
            }

            for future in as_completed(future_to_provider):
                p = future_to_provider[future]
                try:
                    results = future.result()
                    all_records.extend(results)
                    logger.info("[%s] Menghasilkan %d dokumen.", p.display_name, len(results))
                except Exception as e:
                    logger.warning("[%s] Terjadi kesalahan saat mencari: %s", p.display_name, e)

        return self.deduplicate_records(all_records)

    def deduplicate_records(self, records: List[PaperRecord]) -> List[PaperRecord]:
        """
        Deduplicates records based on DOI and normalized title similarity,
        merging open access PDF links and highest citation counts where possible.
        """
        seen_dois: Set[str] = set()
        seen_titles: Set[str] = set()
        deduped: List[PaperRecord] = []

        for rec in records:
            norm_doi = rec.doi.lower().strip() if rec.doi else None
            norm_title = rec.get_normalized_title()

            if norm_doi and norm_doi in seen_dois:
                # Merge into existing record if current record has OA PDF
                self._enrich_existing_record(deduped, norm_doi=norm_doi, candidate=rec)
                continue

            if norm_title and norm_title in seen_titles:
                self._enrich_existing_record(deduped, norm_title=norm_title, candidate=rec)
                continue

            if norm_doi:
                seen_dois.add(norm_doi)
            if norm_title:
                seen_titles.add(norm_title)

            deduped.append(rec)

        # Sort: items with PDF available first, then by citation count (if available)
        def sort_key(r: PaperRecord):
            has_pdf = 1 if r.pdf_url else 0
            citations = r.citation_count if r.citation_count is not None else 0
            tier_priority = 5 - r.source_tier
            return (has_pdf, tier_priority, citations)

        deduped.sort(key=sort_key, reverse=True)
        return deduped

    def _enrich_existing_record(
        self,
        records: List[PaperRecord],
        norm_doi: Optional[str] = None,
        norm_title: Optional[str] = None,
        candidate: Optional[PaperRecord] = None,
    ):
        """Enriches an existing record with additional links or higher citations."""
        if not candidate:
            return
        for r in records:
            match = False
            if norm_doi and r.doi and r.doi.lower().strip() == norm_doi:
                match = True
            elif norm_title and r.get_normalized_title() == norm_title:
                match = True

            if match:
                if not r.pdf_url and candidate.pdf_url:
                    r.pdf_url = candidate.pdf_url
                    r.is_oa = True
                if candidate.citation_count is not None:
                    if r.citation_count is None or candidate.citation_count > r.citation_count:
                        r.citation_count = candidate.citation_count
                if not r.doi and candidate.doi:
                    r.doi = candidate.doi
                break

    def download(self, record: PaperRecord) -> DownloadResult:
        """Downloads a record using the cascading downloader."""
        return self.downloader.download_paper(record)
