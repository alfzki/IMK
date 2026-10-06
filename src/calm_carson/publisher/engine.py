"""Unified Publishing Engine coordinating validation, bibliography rendering, and document conversion."""

import json
import re
from pathlib import Path
from typing import Optional

from calm_carson.publisher.bib_renderer import IEEEBibliographyRenderer
from calm_carson.publisher.citation_validator import CitationValidator
from calm_carson.publisher.converter import DocumentConverter
from calm_carson.publisher.models import (
    PublicationConfig,
    PublishResult,
    ValidationSeverity,
)
from calm_carson.publisher.template_validator import TemplateValidator


class DocumentPublisher:
    """End-to-end publishing pipeline from Markdown manuscripts to official IEEE documents."""

    def __init__(
        self,
        template_path: Optional[str] = None,
        bib_path: Optional[str] = None,
    ):
        self.template_path = template_path or "proposals/Template Proposal Penelitian.docx"
        self.bib_path = bib_path or "literature/references.bib"

        self.template_validator = TemplateValidator(self.template_path)
        self.citation_validator = CitationValidator(self.bib_path)
        self.bib_renderer = IEEEBibliographyRenderer()
        self.converter = DocumentConverter(self.template_path)

    def publish_file(
        self,
        input_markdown_path: str,
        config: Optional[PublicationConfig] = None,
    ) -> PublishResult:
        """Executes full publishing workflow for a markdown file."""
        cfg = config or PublicationConfig()
        in_path = Path(input_markdown_path)

        if not in_path.exists():
            return PublishResult(
                success=False,
                error_message=f"Berkas naskah sumber tidak ditemukan: {input_markdown_path}",
            )

        markdown_text = in_path.read_text(encoding="utf-8")
        return self.publish(markdown_text, in_path.stem, cfg)

    def publish(
        self,
        markdown_text: str,
        base_name: str,
        config: Optional[PublicationConfig] = None,
    ) -> PublishResult:
        """Executes full publishing workflow on raw markdown text."""
        cfg = config or PublicationConfig()

        # Determine output directory
        out_dir = Path(cfg.output_dir) if cfg.output_dir else Path("drafts/published")
        out_dir.mkdir(parents=True, exist_ok=True)

        target_name = cfg.base_filename or base_name
        bib_p = Path(self.bib_path)
        has_ext_bib = bib_p.exists() and bib_p.stat().st_size > 0

        # 1. Template Compliance Validation
        tpl_path = cfg.template_path or self.template_path
        template_report = self.template_validator.validate(markdown_text, has_external_bib=has_ext_bib)

        if cfg.strict_validation and template_report.error_count > 0:
            return PublishResult(
                success=False,
                template_report=template_report,
                error_message=f"Validasi template gagal: Ditemukan {template_report.error_count} kesalahan kritis pada naskah.",
            )

        # 2. Citation Integrity Validation
        citation_report = self.citation_validator.validate(markdown_text, str(bib_p))

        if cfg.strict_validation and citation_report.error_count > 0:
            return PublishResult(
                success=False,
                template_report=template_report,
                citation_report=citation_report,
                error_message=f"Validasi sitasi gagal: Ditemukan {citation_report.error_count} sitasi rusak / tidak ditemukan rujukan.",
            )

        # 3. Citation Renumbering & Bibliography Synthesis
        processed_text = markdown_text
        bib_entries = {}
        if bib_p.exists():
            bib_entries.update(self.citation_validator._parse_bibtex_file(bib_p))
        inline_entries = self.citation_validator._parse_inline_bibliography(markdown_text)
        bib_entries.update(inline_entries)

        has_bib_section = bool(
            re.search(
                r"(?:##\s*(?:DAFTAR\s*PUSTAKA|REFERENSI|REFERENCES)|\bDAFTAR\s*PUSTAKA\b)",
                processed_text,
                re.IGNORECASE,
            )
        )

        if cfg.auto_renumber_citations or not has_bib_section:
            if bib_entries:
                renumbered_text, _ = self.bib_renderer.renumber_manuscript_citations(
                    markdown_text, bib_entries
                )
                processed_text = renumbered_text

        # 4. Generate DOCX
        docx_path = out_dir / f"{target_name}.docx"
        pdf_path = out_dir / f"{target_name}.pdf"

        generated_docx = None
        generated_pdf = None

        if cfg.output_format in ("docx", "all"):
            try:
                generated_docx = self.converter.convert_to_docx(
                    markdown_text=processed_text,
                    output_docx_path=str(docx_path),
                    template_path=tpl_path,
                    config=cfg,
                )
            except Exception as e:
                return PublishResult(
                    success=False,
                    template_report=template_report,
                    citation_report=citation_report,
                    error_message=f"Gagal mengompilasi berkas DOCX: {str(e)}",
                )

        # 5. Generate PDF via LibreOffice headless
        if cfg.output_format in ("pdf", "all") and generated_docx:
            generated_pdf = self.converter.convert_to_pdf(generated_docx, str(pdf_path))

        # 6. Export publication summary metadata
        summary_path = out_dir / f"{target_name}_pub_report.json"
        pub_data = {
            "manuscript": target_name,
            "success": True,
            "docx_path": generated_docx,
            "pdf_path": generated_pdf,
            "template_compliance_score": template_report.compliance_score,
            "template_issues_count": len(template_report.issues),
            "citation_issues_count": len(citation_report.issues),
            "total_citations": citation_report.total_in_text_citations,
            "total_bib_entries": citation_report.total_bib_entries,
        }
        summary_path.write_text(json.dumps(pub_data, indent=2), encoding="utf-8")

        return PublishResult(
            success=True,
            docx_path=generated_docx,
            pdf_path=generated_pdf,
            template_report=template_report,
            citation_report=citation_report,
        )
