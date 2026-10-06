"""Data models for Calm-Carson Document Publishing & Compilation Pipeline."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class ValidationSeverity(str, Enum):
    """Severity level of a validation issue."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class ValidationIssue:
    """Represents a single issue found during template or citation validation."""
    code: str
    category: str  # 'template', 'citation', 'metadata', 'content'
    message: str
    severity: ValidationSeverity = ValidationSeverity.WARNING
    location: str = ""
    suggestion: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "category": self.category,
            "message": self.message,
            "severity": self.severity.value,
            "location": self.location,
            "suggestion": self.suggestion,
        }


@dataclass
class TemplateValidationReport:
    """Report detailing compliance against a thesis/proposal document template."""
    target_template: str
    scope: str  # 'proposal' (Bab 1-3) or 'thesis' (Bab 1-5)
    is_compliant: bool
    compliance_score: float  # 0.0 to 100.0
    issues: List[ValidationIssue] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    section_status: Dict[str, bool] = field(default_factory=dict)

    @property
    def error_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == ValidationSeverity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == ValidationSeverity.WARNING)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_template": self.target_template,
            "scope": self.scope,
            "is_compliant": self.is_compliant,
            "compliance_score": round(self.compliance_score, 1),
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "issues": [issue.to_dict() for issue in self.issues],
            "metadata": self.metadata,
            "section_status": self.section_status,
        }


@dataclass
class CitationItem:
    """Represents an in-text citation marker extracted from the manuscript."""
    key_or_number: str
    raw_marker: str
    occurrences: int = 1
    first_occurrence_line: int = 0
    context_snippets: List[str] = field(default_factory=list)


@dataclass
class BibliographyItem:
    """Represents a bibliographic entry from BibTeX or inline references."""
    key: str
    number: Optional[int] = None
    entry_type: str = "misc"  # 'article', 'inproceedings', 'book', 'mastersthesis', etc.
    title: str = ""
    authors: List[str] = field(default_factory=list)
    year: Optional[int] = None
    venue: Optional[str] = None
    volume: Optional[str] = None
    number_issue: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    publisher: Optional[str] = None
    school: Optional[str] = None
    note: Optional[str] = None
    raw_text: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "number": self.number,
            "entry_type": self.entry_type,
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "venue": self.venue,
            "volume": self.volume,
            "number_issue": self.number_issue,
            "pages": self.pages,
            "doi": self.doi,
            "url": self.url,
            "publisher": self.publisher,
            "school": self.school,
        }


@dataclass
class CitationValidationReport:
    """Report detailing integrity of citations against the available bibliography."""
    total_in_text_citations: int
    unique_in_text_citations: int
    total_bib_entries: int
    matched_citations: List[str] = field(default_factory=list)
    missing_citations: List[str] = field(default_factory=list)  # in text but not in bib
    orphan_references: List[str] = field(default_factory=list)  # in bib but never cited
    out_of_order_citations: List[Dict[str, Any]] = field(default_factory=list)
    is_valid: bool = True
    issues: List[ValidationIssue] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == ValidationSeverity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == ValidationSeverity.WARNING)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_in_text_citations": self.total_in_text_citations,
            "unique_in_text_citations": self.unique_in_text_citations,
            "total_bib_entries": self.total_bib_entries,
            "matched_citations_count": len(self.matched_citations),
            "missing_citations_count": len(self.missing_citations),
            "orphan_references_count": len(self.orphan_references),
            "missing_citations": self.missing_citations,
            "orphan_references": self.orphan_references,
            "out_of_order_citations": self.out_of_order_citations,
            "is_valid": self.is_valid,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "issues": [issue.to_dict() for issue in self.issues],
        }


@dataclass
class PublicationConfig:
    """Configuration options for the document publishing pipeline."""
    template_path: Optional[str] = None
    output_format: str = "all"  # 'docx', 'pdf', 'all'
    bib_style: str = "ieee"
    two_column: bool = True
    auto_renumber_citations: bool = False
    strict_validation: bool = False
    output_dir: Optional[str] = None
    base_filename: Optional[str] = None


@dataclass
class PublishResult:
    """Final outcome of the publication compilation process."""
    success: bool
    docx_path: Optional[str] = None
    pdf_path: Optional[str] = None
    template_report: Optional[TemplateValidationReport] = None
    citation_report: Optional[CitationValidationReport] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "docx_path": self.docx_path,
            "pdf_path": self.pdf_path,
            "template_report": self.template_report.to_dict() if self.template_report else None,
            "citation_report": self.citation_report.to_dict() if self.citation_report else None,
            "error_message": self.error_message,
        }
