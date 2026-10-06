"""Citation integrity validator against bibliography files and inline references."""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from calm_carson.publisher.models import (
    BibliographyItem,
    CitationItem,
    CitationValidationReport,
    ValidationIssue,
    ValidationSeverity,
)


class CitationValidator:
    """Validates in-text citations against BibTeX files and inline bibliographies."""

    def __init__(self, bib_path: Optional[str] = None):
        self.bib_path = Path(bib_path) if bib_path else Path("literature/references.bib")

    def validate(self, text: str, bib_path: Optional[str] = None) -> CitationValidationReport:
        """Validates all citations in text against the specified or default bibliography."""
        target_bib = Path(bib_path) if bib_path else self.bib_path
        issues: List[ValidationIssue] = []

        # 1. Extract all in-text citations
        citation_items, citation_sequence = self._extract_citations(text)
        unique_cites = set(citation_items.keys())
        total_cites = sum(item.occurrences for item in citation_items.values())

        # 2. Parse bibliography entries (from BibTeX and from inline Markdown)
        bib_entries = {}
        if target_bib.exists():
            bib_entries.update(self._parse_bibtex_file(target_bib))
        inline_entries = self._parse_inline_bibliography(text)
        bib_entries.update(inline_entries)

        # 3. Check matched, missing, and orphan citations
        matched_citations: List[str] = []
        missing_citations: List[str] = []

        for cite_key, item in citation_items.items():
            # Check direct match by key or number
            if cite_key in bib_entries:
                matched_citations.append(cite_key)
            elif item.key_or_number in bib_entries:
                matched_citations.append(item.key_or_number)
            elif str(item.key_or_number) in [str(b.number) for b in bib_entries.values() if b.number is not None]:
                matched_citations.append(cite_key)
            else:
                missing_citations.append(cite_key)
                issues.append(
                    ValidationIssue(
                        code="BROKEN_CITATION",
                        category="citation",
                        message=f"Sitasi [{cite_key}] tercantum dalam naskah tetapi tidak ditemukan entri referensinya di bibliografi.",
                        severity=ValidationSeverity.ERROR,
                        location=f"Baris pertama: {item.first_occurrence_line}",
                        suggestion=f"Tambahkan entri referensi untuk [{cite_key}] ke 'literature/references.bib' atau daftar pustaka naskah.",
                    )
                )

        # 4. Check orphan references (in bib but never cited) and disallowed theses
        orphan_references: List[str] = []
        for bib_key, entry in bib_entries.items():
            is_cited = False
            # Check by key
            if bib_key in unique_cites:
                is_cited = True
            # Check by number
            elif entry.number is not None and str(entry.number) in unique_cites:
                is_cited = True

            if not is_cited:
                orphan_references.append(bib_key)
                issues.append(
                    ValidationIssue(
                        code="ORPHAN_REFERENCE",
                        category="citation",
                        message=f"Referensi '{entry.title[:50]}...' ({bib_key}) ada di bibliografi tetapi tidak pernah disitir dalam teks.",
                        severity=ValidationSeverity.INFO,
                        suggestion=f"Kutip referensi ini di bagian yang relevan atau hapus dari daftar pustaka jika tidak dipakai.",
                    )
                )

            # Check for disallowed university theses (SIMPUS / Skripsi)
            url_str = (getattr(entry, "url", None) or "").lower()
            title_str = (getattr(entry, "title", None) or "").lower()
            raw_str = (getattr(entry, "raw_text", None) or "").lower()
            is_thesis = (
                entry.entry_type in ["mastersthesis", "phdthesis", "thesis", "skripsi"]
                or "simpus.stis.ac.id" in url_str
                or "skripsi" in title_str
                or "skripsi" in raw_str
                or "sarjana terapan" in raw_str
                or "tugas akhir" in raw_str
            )
            if is_thesis:
                issues.append(
                    ValidationIssue(
                        code="DISALLOWED_THESIS",
                        category="citation",
                        message=f"Referensi '{entry.title[:50]}' ({bib_key}) merupakan skripsi alumni/SIMPUS yang dilarang untuk naskah ilmiah.",
                        severity=ValidationSeverity.ERROR,
                        suggestion="Ganti referensi skripsi alumni dengan artikel jurnal atau prosiding konferensi resmi.",
                    )
                )


        # 5. Check sequential citation ordering (IEEE numerical standard)
        out_of_order_cites: List[Dict[str, Any]] = []
        numeric_sequence = [int(k) for k in citation_sequence if k.isdigit()]
        max_seen = 0
        for idx, num in enumerate(numeric_sequence):
            if num > max_seen:
                if num > max_seen + 1 and max_seen > 0:
                    out_of_order_cites.append({
                        "citation": f"[{num}]",
                        "index": idx,
                        "expected_max": max_seen + 1,
                        "gap": num - max_seen - 1
                    })
                max_seen = num
            elif num < max_seen:
                # Earlier citation repeated, which is normal in IEEE
                pass

        if out_of_order_cites:
            issues.append(
                ValidationIssue(
                    code="CITATION_ORDER_GAP",
                    category="citation",
                    message=f"Terdapat {len(out_of_order_cites)} lompatan penomoran sitasi IEEE yang tidak berurutan pada naskah.",
                    severity=ValidationSeverity.WARNING,
                    suggestion="Gunakan opsi '--auto-renumber' untuk merapikan urutan sitasi numerik secara otomatis.",
                )
            )

        # 6. Validate STIS reference guidelines (minimal 20 refs, minimal 10 >= 2021)
        total_unique_bib = len(bib_entries)
        recent_refs = [
            b for b in bib_entries.values()
            if b.year is not None and b.year >= 2021
        ]

        if total_unique_bib < 20:
            issues.append(
                ValidationIssue(
                    code="INSUFFICIENT_REFERENCES_COUNT",
                    category="citation",
                    message=f"Total referensi ({total_unique_bib}) kurang dari batas minimum STIS (minimal 20 referensi).",
                    severity=ValidationSeverity.WARNING,
                    suggestion="Tambahkan rujukan ilmiah hingga mencapai minimal 20 entri referensi.",
                )
            )

        if len(recent_refs) < 10:
            issues.append(
                ValidationIssue(
                    code="INSUFFICIENT_RECENT_PAPERS",
                    category="citation",
                    message=f"Hanya {len(recent_refs)} referensi terbit >= 2021 (Standar Pengujian STIS: minimal 10 referensi mutakhir).",
                    severity=ValidationSeverity.WARNING,
                    suggestion="Sertakan lebih banyak paper jurnal atau skripsi mutakhir (rentang 2021–2026).",
                )
            )

        # 7. Check metadata completeness of matched references
        for key in matched_citations:
            entry = bib_entries.get(key)
            if not entry and key.isdigit():
                entry = next((b for b in bib_entries.values() if b.number == int(key)), None)
            if entry:
                if not entry.authors:
                    issues.append(
                        ValidationIssue(
                            code="INCOMPLETE_REF_AUTHOR",
                            category="metadata",
                            message=f"Entri referensi [{key}] tidak mencantumkan nama penulis.",
                            severity=ValidationSeverity.WARNING,
                            suggestion="Lengkapi field 'author' pada berkas BibTeX.",
                        )
                    )
                if not entry.year:
                    issues.append(
                        ValidationIssue(
                            code="INCOMPLETE_REF_YEAR",
                            category="metadata",
                            message=f"Entri referensi [{key}] tidak mencantumkan tahun terbit.",
                            severity=ValidationSeverity.WARNING,
                            suggestion="Lengkapi field 'year' pada berkas BibTeX.",
                        )
                    )

        has_errors = any(issue.severity == ValidationSeverity.ERROR for issue in issues)
        is_valid = not has_errors

        return CitationValidationReport(
            total_in_text_citations=total_cites,
            unique_in_text_citations=len(unique_cites),
            total_bib_entries=total_unique_bib,
            matched_citations=matched_citations,
            missing_citations=missing_citations,
            orphan_references=orphan_references,
            out_of_order_citations=out_of_order_cites,
            is_valid=is_valid,
            issues=issues,
        )

    def validate_file(self, file_path: str, bib_path: Optional[str] = None) -> CitationValidationReport:
        """Reads a manuscript file and validates its citations."""
        path = Path(file_path)
        if not path.exists():
            return CitationValidationReport(
                total_in_text_citations=0,
                unique_in_text_citations=0,
                total_bib_entries=0,
                is_valid=False,
                issues=[
                    ValidationIssue(
                        code="FILE_NOT_FOUND",
                        category="citation",
                        message=f"Berkas naskah tidak ditemukan: {file_path}",
                        severity=ValidationSeverity.ERROR,
                    )
                ],
            )
        text = path.read_text(encoding="utf-8")
        return self.validate(text, bib_path)

    def _extract_citations(self, text: str) -> Tuple[Dict[str, CitationItem], List[str]]:
        """Extracts citation markers from manuscript body (excluding bibliography section)."""
        # Exclude the bibliography / references section itself to avoid self-counting
        body_text = text
        bib_split = re.split(r"(?:##\s*(?:DAFTAR\s*PUSTAKA|REFERENSI|REFERENCES)|\bDAFTAR\s*PUSTAKA\b)", text, flags=re.IGNORECASE)
        if len(bib_split) > 1:
            body_text = bib_split[0]

        citation_items: Dict[str, CitationItem] = {}
        sequence: List[str] = []

        in_code_block = False
        lines = body_text.splitlines()
        for line_no, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                continue

            # Exclude box drawing / ASCII diagram lines
            if any(char in stripped for char in ("│", "┌", "└", "├", "─", "┼", "┬", "┴", "┐", "┘")):
                continue

            # Exclude lines that are markdown table delimiters
            if re.match(r"^\|?\s*[-:]+[-| :]*\|?$", stripped):
                continue

            # 1. Match numeric citations: [1], [2], [3], [1]-[3], [1, 2]
            # Negative lookbehind to avoid markdown links [text](url) or images ![alt](url)
            num_matches = re.finditer(r"(?<!\!)(?<!\[)\[(\d+(?:\s*[,-]\s*\d+)*)\](?!\()", line)
            for m in num_matches:
                raw = m.group(0)
                content = m.group(1).strip()

                # Check if preceded by 'in ' or '\in ' (mathematical range e.g. 'in [0, 1]')
                preceding_text = line[:m.start()]
                if re.search(r"(?:in|\\in|rentang|interval)\s*$", preceding_text, re.IGNORECASE):
                    continue

                # Parse range or comma
                keys = self._parse_compound_numeric_citation(content)
                for k in keys:
                    # Citations in academic writing are positive integers (1, 2, ...)
                    if k == "0":
                        continue
                    sequence.append(k)
                    if k not in citation_items:
                        citation_items[k] = CitationItem(
                            key_or_number=k,
                            raw_marker=raw,
                            occurrences=1,
                            first_occurrence_line=line_no,
                            context_snippets=[line.strip()[:100]],
                        )
                    else:
                        citation_items[k].occurrences += 1

            # 2. Match BibTeX key citations: [@key], @key, \cite{key}
            citekey_matches = re.finditer(r"(?:\[@([a-zA-Z0-9_\-:\.]+)|\\cite\{([a-zA-Z0-9_\-:\.]+)\})", line)
            for m in citekey_matches:
                key = m.group(1) or m.group(2)
                raw = m.group(0)
                sequence.append(key)
                if key not in citation_items:
                    citation_items[key] = CitationItem(
                        key_or_number=key,
                        raw_marker=raw,
                        occurrences=1,
                        first_occurrence_line=line_no,
                        context_snippets=[line.strip()[:100]],
                    )
                else:
                    citation_items[key].occurrences += 1

        return citation_items, sequence

    def _parse_compound_numeric_citation(self, content: str) -> List[str]:
        """Parses '1-3' or '1, 2, 3' into ['1', '2', '3']."""
        results: List[str] = []
        # Split by comma first
        parts = [p.strip() for p in content.split(",") if p.strip()]
        for p in parts:
            if "-" in p:
                dash_parts = p.split("-")
                if len(dash_parts) == 2 and dash_parts[0].strip().isdigit() and dash_parts[1].strip().isdigit():
                    start = int(dash_parts[0].strip())
                    end = int(dash_parts[1].strip())
                    if start <= end and (end - start) < 50:
                        for n in range(start, end + 1):
                            results.append(str(n))
                        continue
            if p.isdigit():
                results.append(p)
        return results

    def _parse_bibtex_file(self, bib_path: Path) -> Dict[str, BibliographyItem]:
        """Parses a .bib file into a dictionary of BibliographyItem objects."""
        items: Dict[str, BibliographyItem] = {}
        if not bib_path.exists():
            return items

        content = bib_path.read_text(encoding="utf-8", errors="replace")
        # Match @type{key, ...}
        entry_blocks = re.split(r"\n(?=@\w+\s*\{)", content)

        for block in entry_blocks:
            block = block.strip()
            if not block.startswith("@"):
                continue

            header_match = re.match(r"@(\w+)\s*\{\s*([^,]+),", block)
            if not header_match:
                continue

            entry_type = header_match.group(1).lower()
            cite_key = header_match.group(2).strip()

            item = BibliographyItem(
                key=cite_key,
                entry_type=entry_type,
                raw_text=block,
            )

            # Extract fields
            def get_field(field_name: str) -> Optional[str]:
                pat = r"(?:^|\n)\s*" + re.escape(field_name) + r"\s*=\s*[\{\"]?(.*?)[\}\"]?(?:,\s*(?:\n|\Z)|\s*\n\s*\}|\s*\Z)"
                m = re.search(pat, block, re.IGNORECASE | re.DOTALL)
                if m:
                    val = m.group(1).strip()
                    val = re.sub(r"[\{\}\"]", "", val).strip()
                    return val
                return None

            item.title = get_field("title") or ""
            author_str = get_field("author") or ""
            if author_str:
                item.authors = [a.strip() for a in author_str.split(" and ") if a.strip()]

            year_str = get_field("year")
            if year_str:
                m_year = re.search(r"\b(19\d\d|20\d\d)\b", year_str)
                if m_year:
                    item.year = int(m_year.group(1))

            item.venue = get_field("journal") or get_field("booktitle")
            item.volume = get_field("volume")
            item.number_issue = get_field("number")
            item.pages = get_field("pages")
            item.doi = get_field("doi")
            item.url = get_field("url")
            item.publisher = get_field("publisher")
            item.school = get_field("school")
            item.note = get_field("note")

            items[cite_key] = item

        return items

    def _parse_inline_bibliography(self, text: str) -> Dict[str, BibliographyItem]:
        """Parses inline markdown bibliography list (e.g. [1] Author, Title...)."""
        items: Dict[str, BibliographyItem] = {}
        bib_split = re.split(r"(?:##\s*(?:DAFTAR\s*PUSTAKA|REFERENSI|REFERENCES)|\bDAFTAR\s*PUSTAKA\b)", text, flags=re.IGNORECASE)
        if len(bib_split) < 2:
            return items

        bib_text = bib_split[1]
        lines = bib_text.splitlines()

        for line in lines:
            line = line.strip()
            m = re.match(r"^\[(\d+)\]\s*(.+)", line)
            if m:
                num = int(m.group(1))
                content = m.group(2).strip()

                # Extract year
                year_match = re.search(r"\b(19\d\d|20\d\d)\b", content)
                year = int(year_match.group(1)) if year_match else None

                # Extract title from quotation or italics
                title_match = re.search(r"\"([^\"]+)\"|“([^”]+)”|\*([^*]+)\*", content)
                title = ""
                if title_match:
                    title = title_match.group(1) or title_match.group(2) or title_match.group(3) or ""
                else:
                    title = content[:60]

                # Extract DOI or URL
                doi_match = re.search(r"\b(?:doi:\s*|https?://doi\.org/)(10\.\d{4,9}/[^\s,]+)", content)
                doi = doi_match.group(1) if doi_match else None

                url_match = re.search(r"(https?://[^\s,]+)", content)
                url = url_match.group(1) if url_match else None

                item = BibliographyItem(
                    key=str(num),
                    number=num,
                    title=title,
                    year=year,
                    doi=doi,
                    url=url,
                    raw_text=line,
                )
                items[str(num)] = item

        return items
