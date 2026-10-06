#!/usr/bin/env python3
"""
scripts/export_to_docx.py

Converts scientific research Markdown drafts into fully styled Microsoft Word (.docx) documents
strictly adhering to academic research paper specifications:
- A4 Paper: Width 21.0 cm, Height 29.7 cm; Margins: Top 2.0 cm, Bottom 2.0 cm, Left 2.0 cm, Right 1.5 cm
- Times New Roman throughout
- Judul: 16pt Bold Center
- Subjudul/English Title: 12pt Italic Center
- Abstrak/Abstract: 10pt Justified, 1 paragraph, 1 column
- Bab: 12pt Bold Uppercase
- Sub-bab: 11pt Bold Titlecase
- Body: 11pt Justified, Line spacing 1.0, First line indent 0.75cm
- Rumus: Native Word Equation (OMML via Insert Equation)
- Tabel: Border terbuka (hanya horizontal atas, bawah, header; tanpa garis vertikal), font TNR 10 pt
- Daftar Pustaka: 11pt, hanging indent 0.75cm
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import docx
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

import latex2mathml.converter
import mathml2omml

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent


def convert_latex_to_omml(tex_str: str) -> Optional[OxmlElement]:
    clean_tex = tex_str.strip()
    if not clean_tex:
        return None
    try:
        mml = latex2mathml.converter.convert(clean_tex)
        omml = mathml2omml.convert(mml)
        if "xmlns:m=" not in omml:
            omml = omml.replace(
                "<m:oMath",
                '<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"',
                1,
            )
        return parse_xml(omml)
    except Exception:
        return None


def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="{top or "none"}" w:sz="6" w:space="0" w:color="auto"/>\n'
        f'  <w:left w:val="{left or "none"}" w:sz="6" w:space="0" w:color="auto"/>\n'
        f'  <w:bottom w:val="{bottom or "none"}" w:sz="6" w:space="0" w:color="auto"/>\n'
        f'  <w:right w:val="{right or "none"}" w:sz="6" w:space="0" w:color="auto"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)


def parse_and_add_runs(
    paragraph,
    text: str,
    font_size=Pt(11),
    base_bold=False,
    base_italic=False,
    font_name="Times New Roman",
    font_color=RGBColor(0, 0, 0),
):
    """
    Parse inline formatting with recursive support:
    - ***bold italic***
    - **bold**
    - *italic*
    - `code` (clean font without backticks)
    - $math$ (native inline OMML equation)
    - \\n (line break)
    """
    pattern = re.compile(
        r"(\n|\*\*\*.*?\*\*\*|\*\*.*?\*\*|\*[^*\n]+?\*|`[^`\n]+?`|\$[^\$\n]+?\$)"
    )
    parts = pattern.split(text)

    for part in parts:
        if not part:
            continue

        if part == "\n":
            r = paragraph.add_run()
            r.add_break()
            continue

        if part.startswith("***") and part.endswith("***") and len(part) >= 6:
            inner = part[3:-3]
            parse_and_add_runs(
                paragraph, inner,
                font_size=font_size, base_bold=True, base_italic=True,
                font_name=font_name, font_color=font_color
            )
            continue

        if part.startswith("**") and part.endswith("**") and len(part) >= 4:
            inner = part[2:-2]
            parse_and_add_runs(
                paragraph, inner,
                font_size=font_size, base_bold=True, base_italic=base_italic,
                font_name=font_name, font_color=font_color
            )
            continue

        if part.startswith("*") and part.endswith("*") and len(part) >= 2:
            inner = part[1:-1]
            parse_and_add_runs(
                paragraph, inner,
                font_size=font_size, base_bold=base_bold, base_italic=True,
                font_name=font_name, font_color=font_color
            )
            continue

        if part.startswith("`") and part.endswith("`") and len(part) >= 2:
            inner = part[1:-1]
            r = paragraph.add_run(inner)
            r.font.name = font_name
            r.font.size = font_size
            r.font.bold = base_bold
            r.font.italic = base_italic
            r.font.color.rgb = font_color
            continue

        if part.startswith("$") and part.endswith("$") and len(part) >= 2:
            inner = part[1:-1].strip()
            omml = convert_latex_to_omml(inner)
            if omml is not None:
                paragraph._p.append(omml)
            else:
                r = paragraph.add_run(inner)
                r.font.name = font_name
                r.font.size = font_size
                r.font.italic = True
            continue

        r = paragraph.add_run(part)
        r.font.name = font_name
        r.font.size = font_size
        r.font.bold = base_bold
        r.font.italic = base_italic
        r.font.color.rgb = font_color


def convert_markdown_to_docx(md_path: Path, docx_out: Path, template_path: Optional[Path] = None) -> Path:
    if template_path and template_path.exists():
        doc = Document(str(template_path))
        # Clear existing placeholder paragraphs and tables from template so only paper content is written
        for p in list(doc.paragraphs):
            p._element.getparent().remove(p._element)
        for t in list(doc.tables):
            t._element.getparent().remove(t._element)
    else:
        doc = Document()

    # Configure Margins
    for sec in doc.sections:
        sec.top_margin = Cm(2.0)
        sec.bottom_margin = Cm(2.0)
        sec.left_margin = Cm(2.0)
        sec.right_margin = Cm(1.5)
        sec.page_width = Cm(21.0)
        sec.page_height = Cm(29.7)

    text = md_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.split("\n")

    in_references = False
    in_table = False
    table_lines = []

    def flush_table(lines_to_parse):
        if not lines_to_parse:
            return
        rows = [l.strip().strip("|").split("|") for l in lines_to_parse if not re.match(r"^\s*\|?[-:| ]+\|?\s*$", l)]
        if not rows:
            return
        num_cols = max(len(r) for r in rows)
        table = doc.add_table(rows=len(rows), cols=num_cols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        table_font_size = Pt(9.5) if num_cols > 6 else Pt(10)

        for r_idx, row_data in enumerate(rows):
            is_header = (r_idx == 0)
            is_last = (r_idx == len(rows) - 1)
            row_elem = table.rows[r_idx]
            row_elem.height = Cm(0.5)

            for c_idx, cell_value in enumerate(row_data):
                if c_idx >= num_cols:
                    break
                cell = table.cell(r_idx, c_idx)
                p = cell.paragraphs[0]
                p.text = ""
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                parse_and_add_runs(p, cell_value.strip(), font_size=table_font_size, base_bold=is_header)

                top_b = "single" if is_header else None
                bot_b = "single" if (is_header or is_last) else None
                set_cell_borders(cell, top=top_b, bottom=bot_b, left=None, right=None)

    for line in lines:
        stripped = line.strip()

        # Handle Markdown Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            in_table = True
            table_lines.append(stripped)
            continue
        else:
            if in_table:
                flush_table(table_lines)
                table_lines = []
                in_table = False

        if not stripped:
            continue

        # Images: ![alt](path)
        img_match = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)", stripped)
        if img_match:
            alt_text = img_match.group(1).strip()
            img_rel_path = img_match.group(2).strip()
            resolved_img = None
            for cand in [md_path.parent / img_rel_path, WORKSPACE_ROOT / img_rel_path, Path(img_rel_path)]:
                if cand.exists():
                    resolved_img = cand
                    break

            if resolved_img:
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(6)
                p_img.paragraph_format.space_after = Pt(3)
                p_img.add_run().add_picture(str(resolved_img), width=Inches(5.5))

                if alt_text:
                    p_cap = doc.add_paragraph()
                    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_cap.paragraph_format.space_after = Pt(6)
                    parse_and_add_runs(p_cap, alt_text, font_size=Pt(10), font_name="Times New Roman")
            continue

        # Check Headings
        if stripped.startswith("# "):
            title_text = stripped.lstrip("# ").strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
            parse_and_add_runs(p, title_text, font_size=Pt(16), base_bold=True)
            continue

        if stripped.startswith("## "):
            h_text = stripped.lstrip("# ").strip()
            if "DAFTAR PUSTAKA" in h_text.upper() or "REFERENCES" in h_text.upper():
                in_references = True

            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            parse_and_add_runs(p, h_text.upper(), font_size=Pt(12), base_bold=True)
            continue

        if stripped.startswith("### "):
            h_text = stripped.lstrip("# ").strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = True
            parse_and_add_runs(p, h_text, font_size=Pt(11), base_bold=True)
            continue

        # Display Math equations: $$ ... $$
        if stripped.startswith("$$") and stripped.endswith("$$") and len(stripped) > 4:
            math_content = stripped[2:-2].strip()
            omml_elem = convert_latex_to_omml(math_content)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            if omml_elem is not None:
                p._p.append(omml_elem)
            else:
                parse_and_add_runs(p, math_content, font_size=Pt(11), base_italic=True)
            continue

        # Table or Figure caption
        is_table_caption = stripped.startswith("Tabel ") or stripped.startswith("Table ")
        is_source_line = stripped.startswith("Sumber:") or stripped.startswith("Source:")

        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.0

        if is_table_caption:
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = True
            parse_and_add_runs(p, stripped, font_size=Pt(11), base_bold=True)
            continue

        if is_source_line:
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(8)
            p.paragraph_format.left_indent = Cm(0.75)
            parse_and_add_runs(p, stripped, font_size=Pt(9), base_italic=True)
            continue

        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if in_references:
            p.paragraph_format.left_indent = Cm(0.75)
            p.paragraph_format.first_line_indent = Cm(-0.75)
            p.paragraph_format.space_after = Pt(4)
        else:
            p.paragraph_format.first_line_indent = Cm(0.75)
            p.paragraph_format.space_after = Pt(4)

        parse_and_add_runs(p, stripped, font_size=Pt(11))

    if in_table and table_lines:
        flush_table(table_lines)

    docx_out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(docx_out))
    print(f"✅ Dokumen Word berhasil diekspor ke: {docx_out}")
    return docx_out



def main():
    parser = argparse.ArgumentParser(description="Export scientific Markdown paper to formatted Microsoft Word (.docx)")
    parser.add_argument("--input", "-i", required=True, help="Input markdown file")
    parser.add_argument("--output", "-o", help="Output .docx file path")
    parser.add_argument("--template", "-t", help="Optional Word template path")

    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    out_path = Path(args.output) if args.output else in_path.with_suffix(".docx")
    if args.template:
        template_path = Path(args.template)
    else:
        imk_template = WORKSPACE_ROOT / "proposals" / "Template Makalah IMK.docx"
        template_path = imk_template if imk_template.exists() else (WORKSPACE_ROOT / "references" / "template" / "Template_Penelitian.docx")

    convert_markdown_to_docx(in_path, out_path, template_path if template_path.exists() else None)


if __name__ == "__main__":
    main()
