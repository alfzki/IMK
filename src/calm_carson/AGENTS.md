# AGENTS.md — src/calm_carson

## OVERVIEW

Python automation engine backing all 19 `scripts/*.py` CLIs: brainstorm, retrieval, verification, drafting, publishing.

## STRUCTURE

- `archives/`: plugin registry + parallel fan-out. `base.py` (`BaseArchiveProvider`), `manager.py` (`CascadingPaperDownloader`, `ThreadPoolExecutor` fan-out, `resolve_source_names`, dedup via `get_normalized_title`), `models.py` (`PaperRecord`), `downloader.py`, `providers/` (9 files: `semantic_scholar`, `core`, `internet_archive`, `gutenberg`, `annas_archive`, `libgen`, `scihub`, `zlibrary`, `ipfs`).
- `brainstorm/`: `extractor.py` (`ResearchGapExtractor`), `synthesizer.py`, `exporter.py`, `models.py` (`ResearchGapItem`, `BrainstormClusterSummary`), pipeline via `run_brainstorm_pipeline`.
- `drafting/`: `collector.py` (`EvidenceCollector`), `outliner.py`, `drafter.py`, `reviser.py`, `checkpoint.py`, `pipeline.py`, `models.py`.
- `metadata.py`: single-module (no subpackage): `parse_pdf_document`, `parse_markdown_document`, `extract_paper_metadata`, `generate_citekey`, `clean_doi`, `compute_title_similarity`.
- `originality/`: `searcher.py` (`GlobalLiteratureSearcher`), `evaluator.py` (`OriginalityEvaluator`), `exporter.py`, `models.py` (`OriginalityReport`, `PublicationMatch`), entry `check_topic_originality`.
- `publisher/`: `engine.py` (`publish`), `converter.py`, `template_validator.py`, `citation_validator.py`, `bib_renderer.py`, `models.py`.
- `search/`: `hybrid.py` (`MarkdownHybridSearchEngine.search`, mode `hybrid|dense|sparse`, RRF `rrf_k=60`), `bm25.py`, `dense.py`, `chunker.py` (`HierarchicalMarkdownChunker`, `MarkdownChunk`).
- `style/`: `checker.py`, `patterns.py`, `models.py`, `exporter.py`.
- `verify/`: `decomposer.py` (`ClaimDecomposer`), `matcher.py` (`EvidenceMatcher`), `verifier.py` (`FactVerifier`, `verify_draft_text`), `annotator.py` (`DraftAnnotator`), `exporter.py`, `models.py` (`FactClaim`, `EvidenceMatch`).
- `__init__.py`: re-exports ~60 symbols; canonical import surface. Read it before adding new public API.

## WHERE TO LOOK

- New archive source: copy `archives/providers/core.py` (API-key pattern) or `annas_archive.py` (mirror-fallback pattern); register in `archives/manager.py` `SOURCE_GROUPS` + `archives/__init__.py`; tiers: TIER_1_ACADEMIC → TIER_4_DECENTRALIZED.
- Retrieval tuning: `search/hybrid.py:search` (`candidates_k = max(top_k*5, 40)`, `dense_weight/sparse_weight`); chunk shape in `search/chunker.py`; index lives `literature/search_index/`.
- Claim pipeline: `verify/decomposer.py` → `verify/matcher.py` → `verify/verifier.py` → `verify/annotator.py`.
- Draft pipeline: `drafting/collector.py` (`EvidenceCollector`, workspace-root-relative JSON loads) → `outliner` → `drafter` → `reviser.py` (`AutomatedReviser`).
- Entry point: `calm-carson` (pyproject) → same functions `scripts/*.py` import; fix here, not in scripts.

## CONVENTIONS

- Provider contract: `search(query, limit, min_year, max_year) -> List[PaperRecord]`; override `resolve_pdf` only when record lacks `pdf_url`; `enabled_by_default=False` for book-only providers (`gutenberg`).
- `EvidenceCollector(workspace_root=None)` resolves repo root via `Path(__file__)` parents; pass explicit root in tests.
- `MarkdownHybridSearchEngine(index_dir=.../literature/search_index)`; returns `[]` with console warning when index missing, never raises.
- Logging via module `logger`; HTML-scrape providers log mirror failures at `debug`, never raise per-mirror.

## ANTI-PATTERNS

- Never call providers directly from scripts; always go through `CascadingPaperDownloader.search` (parallel + dedup + `resolve_source_names`).
- Never add `requests.get` without `timeout=self.timeout` + try/except returning `[]`; one dead mirror must not kill fan-out.
- Never hardcode repo paths; use `EvidenceCollector.workspace_root` derivation or injected `index_dir`.
- Never bypass `PaperRecord` dataclass for dict records across provider boundary; `manager.py` dedup depends on it.
- Never put SIMPUS-thesis acceptance in this package; gating flag is `allow_simpus_theses=False` in `drafting/collector.py`, enforced by audit script, not here.
