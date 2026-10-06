"""Document converter from Markdown to publication-ready IEEE Word (.docx) and PDF."""

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import docx
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor

from calm_carson.publisher.models import PublicationConfig, PublishResult


class DocumentConverter:
    """Converts structured academic Markdown manuscripts to styled IEEE DOCX and PDF."""

    def __init__(self, template_path: Optional[str] = None):
        self.default_template = Path("proposals/Template Proposal Penelitian.docx")
        self.template_path = Path(template_path) if template_path else self.default_template

    def convert_to_docx(
        self,
        markdown_text: str,
        output_docx_path: str,
        template_path: Optional[str] = None,
        config: Optional[PublicationConfig] = None,
    ) -> str:
        """Converts Markdown manuscript into an IEEE formatted .docx file."""
        target_template = Path(template_path) if template_path else self.template_path
        out_path = Path(output_docx_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # 1. Initialize document from template or scratch
        if target_template.exists():
            doc = Document(str(target_template))
            self._prepare_template_document(doc, markdown_text)
        else:
            doc = Document()
            self._setup_scratch_ieee_layout(doc)
            self._render_scratch_title_block(doc, markdown_text)

        # 2. Parse and render manuscript body
        self._render_markdown_body(doc, markdown_text)

        # 3. Save document
        doc.save(str(out_path))
        return str(out_path.resolve())

    def convert_to_pdf(self, docx_path: str, output_pdf_path: Optional[str] = None) -> Optional[str]:
        """Converts .docx to .pdf using LibreOffice headless."""
        in_path = Path(docx_path)
        if not in_path.exists():
            return None

        out_dir = Path(output_pdf_path).parent if output_pdf_path else in_path.parent
        out_dir.mkdir(parents=True, exist_ok=True)

        # Check libreoffice
        lo_bin = shutil.which("libreoffice") or shutil.which("soffice")
        if not lo_bin:
            return None

        cmd = [
            lo_bin,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(out_dir.resolve()),
            str(in_path.resolve()),
        ]

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if res.returncode == 0:
                expected_pdf = out_dir / (in_path.stem + ".pdf")
                if expected_pdf.exists():
                    if output_pdf_path and str(expected_pdf.resolve()) != str(Path(output_pdf_path).resolve()):
                        shutil.move(str(expected_pdf), str(output_pdf_path))
                        return str(Path(output_pdf_path).resolve())
                    return str(expected_pdf.resolve())
        except Exception:
            return None

        return None

    def _prepare_template_document(self, doc: Document, markdown_text: str) -> None:
        """Prepares the base template by populating title block and clearing placeholders."""
        # Extract title and metadata
        meta = self._extract_frontmatter(markdown_text)

        # Update P0 (Title)
        if len(doc.paragraphs) > 0 and meta.get("title"):
            doc.paragraphs[0].text = meta["title"].upper()
            doc.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Update P1 (Subtitle)
        if len(doc.paragraphs) > 1 and meta.get("subtitle"):
            doc.paragraphs[1].text = meta["subtitle"]
            doc.paragraphs[1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif len(doc.paragraphs) > 1:
            doc.paragraphs[1].text = "Proposal Penelitian Skripsi D-IV Komputasi Statistik"
            doc.paragraphs[1].alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Update P2 (Author, NIM, Kelas)
        if len(doc.paragraphs) > 2:
            author = meta.get("author", "Nama Lengkap Mahasiswa")
            nim = meta.get("nim", "NIM: 2221xxxxx")
            kelas = meta.get("kelas", "Kelas: 4SI1")
            doc.paragraphs[2].text = f"{author} ({nim}, {kelas})"
            doc.paragraphs[2].alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Update P3 (Lecturer / Advisor)
        if len(doc.paragraphs) > 3:
            dosen = meta.get("dosen", "Dosen Pembimbing / Pengampu")
            doc.paragraphs[3].text = f"Dosen Pengampu: {dosen}"
            doc.paragraphs[3].alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Clear remaining body elements after index 6 (preserving final sectPr)
        body = doc._body._element
        # Elements to preserve: paragraphs 0..6 and the final sectPr
        for el in list(body)[7:]:
            if el.tag.endswith("sectPr"):
                continue
            body.remove(el)

        # Render Abstract & Keywords at the start of Section 1 (first column)
        if meta.get("abstract"):
            p_abs = doc.add_paragraph()
            p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            run_prefix = p_abs.add_run("Ringkasan— ")
            run_prefix.bold = True
            run_prefix.font.size = Pt(9)
            run_prefix.font.name = "Times New Roman"
            run_body = p_abs.add_run(meta["abstract"])
            run_body.italic = True
            run_body.font.size = Pt(9)
            run_body.font.name = "Times New Roman"

        if meta.get("keywords"):
            p_kw = doc.add_paragraph()
            p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            run_prefix = p_kw.add_run("Kata Kunci— ")
            run_prefix.bold = True
            run_prefix.font.size = Pt(9)
            run_prefix.font.name = "Times New Roman"
            run_body = p_kw.add_run(", ".join(meta["keywords"]))
            run_body.italic = True
            run_body.font.size = Pt(9)
            run_body.font.name = "Times New Roman"

        # Empty spacing paragraph
        doc.add_paragraph()

    def _setup_scratch_ieee_layout(self, doc: Document) -> None:
        """Sets up 2-column IEEE page layout from scratch if no template is used."""
        section = doc.sections[0]
        # A4 page size
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        # Margins: Top 19mm (0.75 in), Bottom 43mm (1.69 in), Left/Right 14.32mm (0.56 in)
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(1.69)
        section.left_margin = Inches(0.56)
        section.right_margin = Inches(0.56)

    def _render_scratch_title_block(self, doc: Document, markdown_text: str) -> None:
        """Renders title block on a scratch document."""
        meta = self._extract_frontmatter(markdown_text)
        title = meta.get("title", "PROPOSAL PENELITIAN SKRIPSI").upper()
        p_title = doc.add_paragraph()
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_title.add_run(title)
        r.font.name = "Times New Roman"
        r.font.size = Pt(24)
        r.bold = True

        p_author = doc.add_paragraph()
        p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
        author_str = f"{meta.get('author', 'Mahasiswa')} ({meta.get('nim', 'NIM')})"
        r_a = p_author.add_run(author_str)
        r_a.font.name = "Times New Roman"
        r_a.font.size = Pt(11)

        # Add section break for 2 columns
        sec2 = doc.add_section()
        sectPr = sec2._sectPr
        cols = sectPr.xpath("./w:cols")
        if cols:
            cols[0].set(qn("w:num"), "2")
            cols[0].set(qn("w:space"), "238")

    def _extract_frontmatter(self, text: str) -> Dict[str, Any]:
        """Extracts frontmatter metadata from markdown text."""
        meta: Dict[str, Any] = {}

        # Title
        t_match = re.search(r"^#\s+(?:PROPOSAL\s+PENELITIAN:?\s*)?([^\n]+)", text, re.MULTILINE | re.IGNORECASE)
        if t_match:
            meta["title"] = t_match.group(1).strip()

        # Author / Mahasiswa
        a_match = re.search(r"(?:Penulis|Mahasiswa|Nama)[:—]\s*([^\n\(]+)(?:\(([^,\)]+)(?:,\s*([^\)]+))?\))?", text, re.IGNORECASE)
        if a_match:
            meta["author"] = a_match.group(1).strip()
            if a_match.group(2):
                meta["nim"] = a_match.group(2).strip()
            if a_match.group(3):
                meta["kelas"] = a_match.group(3).strip()

        # Lecturer / Advisor
        d_match = re.search(r"(?:Dosen\s*Pengampu|Dosen\s*Pembimbing|Pembimbing)[:—]\s*([^\n]+)", text, re.IGNORECASE)
        if d_match:
            meta["dosen"] = d_match.group(1).strip()

        # Abstract
        abs_match = re.search(
            r"(?:##\s*(?:Ringkasan|Abstrak|Abstract)|> \*\*Ringkasan\*\*[:—]?|> \*\*Abstrak\*\*[:—]?)(.*?)(?=\n##|\Z)",
            text,
            re.DOTALL | re.IGNORECASE,
        )
        if abs_match:
            clean_abs = re.sub(r"[#>*_`\[\]]", " ", abs_match.group(1)).strip()
            clean_abs = " ".join(clean_abs.split())
            meta["abstract"] = clean_abs

        # Keywords
        kw_match = re.search(r"(?:Kata Kunci|Keywords)[:—]\s*([^\n]+)", text, re.IGNORECASE)
        if kw_match:
            kws = [k.strip() for k in re.split(r"[,;]", kw_match.group(1)) if k.strip()]
            meta["keywords"] = kws

        return meta

    def _render_markdown_body(self, doc: Document, markdown_text: str) -> None:
        """Parses Markdown body elements and renders them into Word paragraphs and tables."""
        # Strip frontmatter sections (Title, Ringkasan, Kata Kunci)
        clean_text = self._strip_frontmatter_for_body(markdown_text)

        lines = clean_text.splitlines()
        i = 0
        total_lines = len(lines)

        in_code_block = False
        code_lines: List[str] = []

        while i < total_lines:
            line = lines[i].rstrip()

            # Handle code blocks
            if line.startswith("```"):
                if in_code_block:
                    in_code_block = False
                    self._add_code_block(doc, "\n".join(code_lines))
                    code_lines = []
                else:
                    in_code_block = True
                    code_lines = []
                i += 1
                continue

            if in_code_block:
                code_lines.append(line)
                i += 1
                continue

            # Empty line
            if not line.strip():
                i += 1
                continue

            # Horizontal rule
            if re.match(r"^---+$", line.strip()):
                i += 1
                continue

            # Headings
            h_match = re.match(r"^(#{1,6})\s+(.+)", line)
            if h_match:
                level = len(h_match.group(1))
                h_text = h_match.group(2).strip()
                self._add_heading(doc, h_text, level)
                i += 1
                continue

            # Tables
            if line.strip().startswith("|") and line.strip().endswith("|"):
                # Collect all table lines
                table_lines = []
                while i < total_lines and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                    table_lines.append(lines[i].strip())
                    i += 1
                self._add_markdown_table(doc, table_lines)
                continue

            # Blockquotes
            if line.strip().startswith(">"):
                quote_text = re.sub(r"^>\s*", "", line.strip())
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.left_indent = Inches(0.2)
                p.paragraph_format.right_indent = Inches(0.2)
                run = p.add_run(quote_text)
                run.italic = True
                run.font.name = "Times New Roman"
                run.font.size = Pt(9.5)
                i += 1
                continue

            # Bulleted List
            if re.match(r"^[\*\-]\s+(.+)", line):
                bullet_text = re.match(r"^[\*\-]\s+(.+)", line).group(1)
                p = doc.add_paragraph(style="List Bullet") if "List Bullet" in [s.name for s in doc.styles] else doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.2)
                p.paragraph_format.first_line_indent = Inches(-0.1)
                self._render_formatted_runs(p, f"• {bullet_text}")
                i += 1
                continue

            # Numbered List
            if re.match(r"^\d+[\.\)]\s+(.+)", line):
                num_match = re.match(r"^(\d+[\.\)])\s+(.+)", line)
                num_prefix = num_match.group(1)
                num_text = num_match.group(2)
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.2)
                p.paragraph_format.first_line_indent = Inches(-0.1)
                self._render_formatted_runs(p, f"{num_prefix} {num_text}")
                i += 1
                continue

            # Math / Equation paragraph: e.g. (1) or $$ ... $$
            if re.search(r"\(\d+\)\s*$", line.strip()) or line.strip().startswith("$$"):
                self._add_equation(doc, line.strip())
                i += 1
                continue

            # Normal Paragraph
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Inches(0.15)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.05
            self._render_formatted_runs(p, line.strip())
            i += 1

    def _strip_frontmatter_for_body(self, text: str) -> str:
        """Removes title and abstract blocks from manuscript text to prevent duplicate rendering."""
        body = text
        # Remove initial title heading
        body = re.sub(r"^#\s+[^\n]+\n+", "", body)
        # Remove Abstract block
        body = re.sub(r"(?:##\s*(?:Ringkasan|Abstrak|Abstract)|> \*\*Ringkasan\*\*[:—]?|> \*\*Abstrak\*\*[:—]?)(.*?)(?=\n##\s*[^\n]+|\Z)", "", body, flags=re.DOTALL | re.IGNORECASE)
        # Remove Keywords line
        body = re.sub(r"(?:Kata Kunci|Keywords)[:—][^\n]+\n*", "", body, flags=re.IGNORECASE)
        return body.strip()

    def _add_heading(self, doc: Document, text: str, level: int) -> None:
        """Adds an IEEE styled heading."""
        # Clean text
        clean_text = re.sub(r"^#+\s*", "", text).strip()

        # Check if heading is major chapter (e.g. BAB I, BAB II, BAB III, DAFTAR PUSTAKA)
        is_major = bool(re.search(r"^(?:BAB\s*[I|V|X]+|Bab\s*\d+|DAFTAR\s*PUSTAKA|REFERENSI)", clean_text, re.IGNORECASE))

        if is_major or level == 1:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(clean_text.upper())
            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
        elif level == 2:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(clean_text)
            run.bold = True
            run.italic = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
        else:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.first_line_indent = Inches(0.15)
            run = p.add_run(clean_text)
            run.italic = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)

    def _add_markdown_table(self, doc: Document, table_lines: List[str]) -> None:
        """Converts Markdown table rows to an IEEE formatted Word table."""
        if len(table_lines) < 2:
            return

        # Parse rows
        parsed_rows: List[List[str]] = []
        for line in table_lines:
            # Skip delimiter line (|---|---|)
            if re.match(r"^\|?\s*[-:]+[-| :]*\|?$", line):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells:
                parsed_rows.append(cells)

        if not parsed_rows:
            return

        num_cols = max(len(r) for r in parsed_rows)
        num_rows = len(parsed_rows)

        table = doc.add_table(rows=num_rows, cols=num_cols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        for row_idx, row_data in enumerate(parsed_rows):
            row = table.rows[row_idx]
            is_header = (row_idx == 0)

            for col_idx in range(num_cols):
                cell_text = row_data[col_idx] if col_idx < len(row_data) else ""
                cell = row.cells[col_idx]
                cell.text = cell_text

                # Formatting cell runs
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if is_header else WD_ALIGN_PARAGRAPH.LEFT
                    for run in p.runs:
                        run.font.name = "Times New Roman"
                        run.font.size = Pt(8)
                        if is_header:
                            run.bold = True

                # Apply header shading
                if is_header:
                    shading_elm = parse_xml(r'<w:shd {} w:fill="F2F2F2"/>'.format(nsdecls('w')))
                    cell._tc.get_or_add_tcPr().append(shading_elm)

        # Spacing after table
        doc.add_paragraph()

    def _add_equation(self, doc: Document, eq_line: str) -> None:
        """Renders equation line with right-aligned number."""
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)

        clean_eq = eq_line.replace("$$", "").strip()
        run = p.add_run(clean_eq)
        run.italic = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(9.5)

    def _add_code_block(self, doc: Document, code: str) -> None:
        """Renders monospace code block."""
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(code)
        run.font.name = "Consolas"
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor(60, 60, 60)

    def _render_formatted_runs(self, paragraph, text: str) -> None:
        """Parses inline formatting (**bold**, *italic*, `code`, [1]) into runs."""
        # Regex tokens for bold, italic, code
        tokens = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)", text)
        for token in tokens:
            if not token:
                continue
            if token.startswith("**") and token.endswith("**"):
                r = paragraph.add_run(token[2:-2])
                r.bold = True
            elif token.startswith("*") and token.endswith("*"):
                r = paragraph.add_run(token[1:-1])
                r.italic = True
            elif token.startswith("`") and token.endswith("`"):
                r = paragraph.add_run(token[1:-1])
                r.font.name = "Consolas"
                r.font.size = Pt(9)
            else:
                r = paragraph.add_run(token)

            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
