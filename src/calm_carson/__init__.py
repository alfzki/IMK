"""
calm_carson
Toolkit Brainstorming, Scraping, Retrieval, dan Perancangan Skripsi Politeknik Statistika STIS.
"""

from calm_carson.brainstorm import (
    BrainstormClusterSummary,
    BrainstormExporter,
    BrainstormSynthesizer,
    ResearchGapExtractor,
    ResearchGapItem,
    run_brainstorm_pipeline,
)
from calm_carson.metadata import (
    AcademicResolver,
    DocumentInfo,
    batch_process_documents,
    clean_doi,
    clean_filename_to_title,
    compute_title_similarity,
    extract_paper_metadata,
    generate_citekey,
    parse_markdown_document,
    parse_pdf_document,
)
from calm_carson.search import (
    BM25Index,
    DenseEmbeddingEngine,
    HierarchicalMarkdownChunker,
    MarkdownChunk,
    MarkdownHybridSearchEngine,
    SearchResult,
    tokenize_technical_text,
)

from calm_carson.originality import (
    DifferentiationFeedback,
    GlobalLiteratureSearcher,
    OriginalityEvaluator,
    OriginalityExporter,
    OriginalityReport,
    PublicationMatch,
    check_topic_originality,
)

from calm_carson.verify import (
    ClaimDecomposer,
    ClaimVerificationResult,
    DraftAnnotator,
    EvidenceMatch,
    EvidenceMatcher,
    FactClaim,
    FactVerifier,
    VerificationExporter,
    VerificationReport,
    verify_draft_text,
)

from calm_carson.drafting import (
    AutomatedReviser,
    ChapterOutline,
    DraftingCheckpoint,
    EvidenceCollector,
    EvidenceItem,
    SectionDraft,
    SubSectionOutline,
    ThesisDraftingPipeline,
    ThesisOutliner,
    WorkflowState,
)

from calm_carson.publisher import (
    BibliographyItem,
    CitationItem,
    CitationValidationReport,
    CitationValidator,
    DocumentConverter,
    DocumentPublisher,
    IEEEBibliographyRenderer,
    PublicationConfig,
    PublishResult,
    TemplateValidationReport,
    TemplateValidator,
    ValidationIssue,
    ValidationSeverity,
)

__all__ = [
    # Metadata & BibTeX
    "AcademicResolver",
    "DocumentInfo",
    "extract_paper_metadata",
    "batch_process_documents",
    "parse_pdf_document",
    "parse_markdown_document",
    "clean_doi",
    "clean_filename_to_title",
    "compute_title_similarity",
    "generate_citekey",
    # Hybrid Search & Retrieval
    "HierarchicalMarkdownChunker",
    "MarkdownChunk",
    "BM25Index",
    "tokenize_technical_text",
    "DenseEmbeddingEngine",
    "MarkdownHybridSearchEngine",
    "SearchResult",
    # Brainstorming & Research Gap Mining
    "ResearchGapItem",
    "BrainstormClusterSummary",
    "ResearchGapExtractor",
    "BrainstormSynthesizer",
    "BrainstormExporter",
    "run_brainstorm_pipeline",
    # Originality & Novelty Evaluation
    "PublicationMatch",
    "DifferentiationFeedback",
    "OriginalityReport",
    "GlobalLiteratureSearcher",
    "OriginalityEvaluator",
    "OriginalityExporter",
    "check_topic_originality",
    # Factual & Citation Verification
    "FactClaim",
    "EvidenceMatch",
    "ClaimVerificationResult",
    "VerificationReport",
    "ClaimDecomposer",
    "EvidenceMatcher",
    "FactVerifier",
    "DraftAnnotator",
    "VerificationExporter",
    "verify_draft_text",
    # Thesis Drafting Pipeline
    "SubSectionOutline",
    "ChapterOutline",
    "EvidenceItem",
    "SectionDraft",
    "WorkflowState",
    "ThesisOutliner",
    "EvidenceCollector",
    "SectionDrafter",
    "AutomatedReviser",
    "DraftingCheckpoint",
    "ThesisDraftingPipeline",
    # Publishing & Compilation Pipeline
    "ValidationSeverity",
    "ValidationIssue",
    "TemplateValidationReport",
    "CitationItem",
    "BibliographyItem",
    "CitationValidationReport",
    "PublicationConfig",
    "PublishResult",
    "TemplateValidator",
    "CitationValidator",
    "IEEEBibliographyRenderer",
    "DocumentConverter",
    "DocumentPublisher",
]


def main() -> None:
    print("calm-carson: Academic Research & Theses Toolkit for Polstat STIS.")
    print("Gunakan 'python scripts/extract_metadata.py --help' untuk ekstraksi metadata paper.")
    print("Gunakan 'python scripts/hybrid_search.py --help' untuk pencarian hybrid dokumen Markdown.")
    print("Gunakan 'python scripts/brainstorm_topics.py --help' untuk penambangan celah riset & brainstorming.")
    print("Gunakan 'python scripts/check_originality.py --help' untuk pengujian orisinalitas ide riset global.")
    print("Gunakan 'python scripts/verify_claims.py --help' untuk verifikasi keabsahan faktual dan sitasi draf.")
    print("Gunakan 'python scripts/orchestrate_drafting.py --help' untuk alur penyusunan naskah bab demi bab.")
    print("Gunakan 'python scripts/publish_document.py --help' untuk penerbitan dokumen DOCX & PDF siap pakai.")
