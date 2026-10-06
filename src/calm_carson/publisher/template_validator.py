"""Template compliance validator for thesis/proposal manuscripts."""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from calm_carson.publisher.models import (
    TemplateValidationReport,
    ValidationIssue,
    ValidationSeverity,
)


class TemplateValidator:
    """Validates markdown manuscripts against STIS IEEE proposal/thesis templates."""

    def __init__(self, template_path: Optional[str] = None):
        self.template_path = template_path or "proposals/Template Proposal Penelitian.docx"

    def validate(
        self,
        text: str,
        scope: Optional[str] = None,
        has_external_bib: bool = False,
    ) -> TemplateValidationReport:
        """Validates the markdown manuscript content against template requirements."""
        issues: List[ValidationIssue] = []
        metadata: Dict[str, Any] = {}
        section_status: Dict[str, bool] = {}

        # 1. Detect scope if not specified
        if not scope:
            if re.search(r"(?:#+\s*(?:BAB\s*IV|Bab\s*4|Hasil\s*dan\s*Pembahasan))", text, re.IGNORECASE):
                scope = "thesis"
            else:
                scope = "proposal"

        # 2. Extract and validate metadata / frontmatter
        meta_issues, extracted_meta = self._validate_metadata(text)
        issues.extend(meta_issues)
        metadata.update(extracted_meta)

        # 3. Validate structural sections according to scope
        sec_issues, sec_status = self._validate_sections(text, scope, has_external_bib=has_external_bib)
        issues.extend(sec_issues)
        section_status.update(sec_status)

        # 4. Validate STIS specific quality criteria (Latar Belakang 3 problems, figures, tables)
        quality_issues = self._validate_stis_criteria(text, scope)
        issues.extend(quality_issues)

        # 5. Calculate compliance score
        score = 100.0
        has_error = False
        for issue in issues:
            if issue.severity == ValidationSeverity.ERROR:
                score -= 15.0
                has_error = True
            elif issue.severity == ValidationSeverity.WARNING:
                score -= 5.0
            elif issue.severity == ValidationSeverity.INFO:
                score -= 1.0

        score = max(0.0, min(100.0, score))
        is_compliant = (not has_error) and (score >= 70.0)

        return TemplateValidationReport(
            target_template=str(self.template_path),
            scope=scope,
            is_compliant=is_compliant,
            compliance_score=score,
            issues=issues,
            metadata=metadata,
            section_status=section_status,
        )

    def validate_file(self, file_path: str, scope: Optional[str] = None) -> TemplateValidationReport:
        """Reads a markdown file and validates its content."""
        path = Path(file_path)
        if not path.exists():
            report = TemplateValidationReport(
                target_template=str(self.template_path),
                scope=scope or "proposal",
                is_compliant=False,
                compliance_score=0.0,
                issues=[
                    ValidationIssue(
                        code="FILE_NOT_FOUND",
                        category="template",
                        message=f"Berkas naskah tidak ditemukan: {file_path}",
                        severity=ValidationSeverity.ERROR,
                    )
                ],
            )
            return report

        text = path.read_text(encoding="utf-8")
        report = self.validate(text, scope)
        report.metadata["file_path"] = str(path.resolve())
        return report

    def _validate_metadata(self, text: str) -> Tuple[List[ValidationIssue], Dict[str, Any]]:
        """Extracts and validates frontmatter/title block metadata."""
        issues: List[ValidationIssue] = []
        meta: Dict[str, Any] = {}

        # Title extraction
        title_match = re.search(r"^#\s+(?:PROPOSAL\s+PENELITIAN:?\s*)?([^\n]+)", text, re.MULTILINE | re.IGNORECASE)
        if title_match:
            meta["title"] = title_match.group(1).strip()
        else:
            issues.append(
                ValidationIssue(
                    code="MISSING_TITLE",
                    category="metadata",
                    message="Judul proposal/skripsi (Heading level 1) tidak ditemukan pada awal naskah.",
                    severity=ValidationSeverity.ERROR,
                    suggestion="Tambahkan judul utama di awal berkas dengan format '# JUDUL PENELITIAN'",
                )
            )

        # Abstract / Ringkasan extraction & word count
        abstract_match = re.search(
            r"(?:##\s*(?:Ringkasan|Abstrak|Abstract)|> \*\*Ringkasan\*\*[:—]?|> \*\*Abstrak\*\*[:—]?)(.*?)(?=\n##|\Z)",
            text,
            re.DOTALL | re.IGNORECASE,
        )
        if abstract_match:
            abstract_text = abstract_match.group(1).strip()
            # clean markdown formatting
            clean_abstract = re.sub(r"[#>*_`\[\]]", " ", abstract_text)
            words = [w for w in clean_abstract.split() if w.strip()]
            meta["abstract_words"] = len(words)
            meta["has_abstract"] = True

            # IEEE guideline specifies maximum 160 words
            if len(words) > 160:
                issues.append(
                    ValidationIssue(
                        code="ABSTRACT_TOO_LONG",
                        category="metadata",
                        message=f"Ringkasan/Abstrak terdiri dari {len(words)} kata (maksimum template IEEE STIS adalah 160 kata).",
                        severity=ValidationSeverity.WARNING,
                        suggestion="Persingkat ringkasan agar padat dan berada dalam batas $\\le$ 160 kata.",
                    )
                )
            elif len(words) < 30:
                issues.append(
                    ValidationIssue(
                        code="ABSTRACT_TOO_SHORT",
                        category="metadata",
                        message=f"Ringkasan/Abstrak terlalu singkat ({len(words)} kata).",
                        severity=ValidationSeverity.WARNING,
                        suggestion="Uraikan latar belakang singkat, tujuan artefak, metode, dan estimasi kontribusi.",
                    )
                )
        else:
            meta["has_abstract"] = False
            issues.append(
                ValidationIssue(
                    code="MISSING_ABSTRACT",
                    category="metadata",
                    message="Bagian Ringkasan/Abstrak tidak ditemukan di awal dokumen.",
                    severity=ValidationSeverity.WARNING,
                    suggestion="Tambahkan bagian '## Ringkasan' sebelum Bab I (maksimum 160 kata).",
                )
            )

        # Keywords / Kata Kunci extraction
        kw_match = re.search(r"(?:Kata Kunci|Keywords)[:—]\s*([^\n]+)", text, re.IGNORECASE)
        if kw_match:
            raw_kws = kw_match.group(1).strip()
            keywords = [k.strip() for k in re.split(r"[,;]", raw_kws) if k.strip()]
            meta["keywords"] = keywords
            meta["keywords_count"] = len(keywords)
            if len(keywords) > 5:
                issues.append(
                    ValidationIssue(
                        code="TOO_MANY_KEYWORDS",
                        category="metadata",
                        message=f"Jumlah kata kunci ({len(keywords)}) melebihi batas template (maksimum 5 kata kunci).",
                        severity=ValidationSeverity.WARNING,
                        suggestion="Pilih 3 hingga 5 kata kunci paling esensial yang dipisahkan dengan koma.",
                    )
                )
            elif len(keywords) < 2:
                issues.append(
                    ValidationIssue(
                        code="TOO_FEW_KEYWORDS",
                        category="metadata",
                        message=f"Jumlah kata kunci ({len(keywords)}) kurang memadai.",
                        severity=ValidationSeverity.INFO,
                        suggestion="Sertakan minimal 3 kata kunci teknis.",
                    )
                )
        else:
            meta["keywords_count"] = 0
            issues.append(
                ValidationIssue(
                    code="MISSING_KEYWORDS",
                    category="metadata",
                    message="Bagian 'Kata Kunci' tidak ditemukan.",
                    severity=ValidationSeverity.WARNING,
                    suggestion="Tambahkan baris 'Kata Kunci: kata1, kata2, kata3, kata4, kata5' setelah ringkasan.",
                )
            )

        return issues, meta

    def _validate_sections(
        self,
        text: str,
        scope: str,
        has_external_bib: bool = False,
    ) -> Tuple[List[ValidationIssue], Dict[str, bool]]:
        """Validates presence and ordering of required chapters and subsections."""
        issues: List[ValidationIssue] = []
        status: Dict[str, bool] = {}

        # Required sections for STIS Proposal (Bab 1 s.d. 3)
        proposal_sections = [
            ("bab_1_pendahuluan", r"(?:BAB\s*I\b|Bab\s*1\b|PENDAHULUAN|I\.\s*Latar|Latar\s*Belakang)", "Bab I: Pendahuluan", True),
            ("latar_belakang", r"(?:1\.1\b|I\.\s*Latar|Latar\s*Belakang)", "Latar Belakang Masalah", True),
            ("rumusan_masalah", r"(?:1\.2\b|II\.\s*Rumusan|Rumusan\s*Masalah|Identifikasi\s*Masalah)", "Rumusan Masalah", True),
            ("tujuan_penelitian", r"(?:1\.3\b|III\.\s*Tujuan|Tujuan\s*Penelitian)", "Tujuan Penelitian", True),
            ("batasan_masalah", r"(?:1\.4\b|IV\.\s*Batasan|Batasan\s*Masalah|Ruang\s*Lingkup|Identifikasi\s*Masalah)", "Batasan Masalah", False),
            ("bab_2_tinjauan_pustaka", r"(?:BAB\s*II\b|Bab\s*2\b|IV\.\s*Tinjauan|TINJAUAN\s*PUSTAKA)", "Bab II: Tinjauan Pustaka", True),
            ("landasan_teori", r"(?:2\.1\b|Landasan\s*Teori|Tinjauan\s*Teori|Tinjauan\s*Pustaka)", "Landasan Teori / Konsep", True),
            ("penelitian_terdahulu", r"(?:2\.2\b|Penelitian\s*Terdahulu|Tabel\s*Kontribusi|Literature\s*Table)", "Penelitian Terdahulu & Kontribusi", False),
            ("kesenjangan_penelitian", r"(?:2\.3\b|Kesenjangan\s*Penelitian|Research\s*Gap|Dampak\s*dan\s*Urgensi)", "Kesenjangan Penelitian & Urgensi", False),
            ("bab_3_metodologi", r"(?:BAB\s*III\b|Bab\s*3\b|V\.\s*Metodologi|METODOLOGI\s*PENELITIAN)", "Bab III: Metodologi Penelitian", True),
            ("tahapan_penelitian", r"(?:3\.1\b|Tahapan\s*Penelitian|Metode\s*Pengembangan|DSRM|Metodologi\s*Penelitian)", "Tahapan / Desain Penelitian", True),
            ("lingkungan_arsitektur", r"(?:3\.2\b|Arsitektur\s*Sistem|Lingkungan\s*Komputasi|Metode\s*Analisis|Sumber\s*Data)", "Arsitektur Sistem & Komputasi", False),
            ("jadwal_penelitian", r"(?:3\.5\b|Jadwal\s*Penelitian|Rancangan\s*Jadwal|TABEL\s*II|Tabel\s*2)", "Jadwal Penelitian", False),
            ("daftar_pustaka", r"(?:DAFTAR\s*PUSTAKA|REFERENSI|REFERENCES)", "Daftar Pustaka", True),
        ]

        # Additional sections for Full Thesis (Bab 4 & 5)
        thesis_sections = [
            ("bab_4_hasil_pembahasan", r"(?:BAB\s*IV\b|Bab\s*4\b|HASIL\s*DAN\s*PEMBAHASAN)", "Bab IV: Hasil dan Pembahasan", True),
            ("bab_5_penutup", r"(?:BAB\s*V\b|Bab\s*5\b|PENUTUP|KESIMPULAN)", "Bab V: Penutup / Kesimpulan", True),
        ]

        sections_to_check = proposal_sections.copy()
        if scope == "thesis":
            sections_to_check.extend(thesis_sections)

        for sec_id, pattern, label, is_critical in sections_to_check:
            found = bool(re.search(pattern, text, re.IGNORECASE))
            if sec_id == "daftar_pustaka" and has_external_bib:
                found = True

            status[sec_id] = found

            if not found:
                severity = ValidationSeverity.ERROR if is_critical else ValidationSeverity.WARNING
                issues.append(
                    ValidationIssue(
                        code=f"MISSING_SECTION_{sec_id.upper()}",
                        category="template",
                        message=f"Bagian '{label}' tidak ditemukan dalam naskah.",
                        severity=severity,
                        suggestion=f"Tambahkan sub-bab atau bagian '{label}' sesuai dengan template resmi STIS.",
                    )
                )

        return issues, status

    def _validate_stis_criteria(self, text: str, scope: str) -> List[ValidationIssue]:
        """Validates specific STIS examination panel criteria."""
        issues: List[ValidationIssue] = []

        # 1. Check Latar Belakang for minimal 3 concrete empirical problems
        # Look for problem markers (1., 2., 3. or Masalah 1, Masalah 2, Masalah 3 or A., B., C.)
        latar_belakang_match = re.search(
            r"(?:\n##+\s*(?:1\.1|I\.\s*Latar|Latar\s*Belakang)[^\n]*\r?\n)(.*?)(?=\n##+\s*(?:1\.2|II\.|Rumusan)|\Z)",
            text,
            re.DOTALL | re.IGNORECASE,
        )
        if not latar_belakang_match:
            latar_belakang_match = re.search(
                r"(?:Latar\s*Belakang[^\n]*\n)(.*?)(?=Rumusan\s*Masalah|\n##\s*(?:1\.2|II\.)|\Z)",
                text,
                re.DOTALL | re.IGNORECASE,
            )
        if latar_belakang_match:
            lb_text = latar_belakang_match.group(1)
            # Find problem items
            problem_headers = re.findall(
                r"(?:###\s*(?:[A-Z]|\d+)\.|\bMasalah\s*\d+:|Permasalahan\s*\d+:|\b[A-C]\.\s+[^,\n]+)",
                lb_text,
                re.IGNORECASE,
            )
            # Find numbers and percentages in Latar Belakang
            quantitative_figures = re.findall(
                r"\b(?:\d{1,3}(?:\.\d{3})+|\d+[\.,]\d+|\d+%\b|\d+\s*(?:ribu|juta|persen|bulan|menit))\b",
                lb_text,
                re.IGNORECASE,
            )

            if len(problem_headers) < 3:
                issues.append(
                    ValidationIssue(
                        code="INSUFFICIENT_PROBLEMS",
                        category="content",
                        message=f"Latar Belakang hanya mendeteksi {len(problem_headers)} poin masalah konkret (Standar Pengujian STIS: minimal 3 masalah).",
                        severity=ValidationSeverity.WARNING,
                        location="Latar Belakang",
                        suggestion="Uraikan minimal 3 permasalahan operasional konkret dengan sub-heading jelas (e.g. '### 1. ...', '### 2. ...', '### 3. ...').",
                    )
                )

            if len(quantitative_figures) < 3:
                issues.append(
                    ValidationIssue(
                        code="LACK_OF_EMPIRICAL_FIGURES",
                        category="content",
                        message="Latar Belakang memiliki sedikit data kuantitatif riil (Standar STIS mewajibkan angka empiris konkret di setiap masalah).",
                        severity=ValidationSeverity.WARNING,
                        location="Latar Belakang",
                        suggestion="Sertakan angka statistik riil (e.g. jumlah petugas, durasi waktu pencacahan, persentase anomali, indeks SPBE/IPS).",
                    )
                )

        # 2. Check for Tabel I (Literature / Contribution Table)
        has_table_1 = bool(re.search(r"(?:TABEL\s*I\b|Tabel\s*1\b|Tabel\s*Kontribusi)", text, re.IGNORECASE))
        if not has_table_1:
            issues.append(
                ValidationIssue(
                    code="MISSING_CONTRIBUTION_TABLE",
                    category="template",
                    message="Tabel I (Tabel Kontribusi Penelitian / Literature Table) tidak terdeteksi pada Tinjauan Pustaka.",
                    severity=ValidationSeverity.WARNING,
                    location="Tinjauan Pustaka",
                    suggestion="Tambahkan 'TABEL I. TABEL KONTRIBUSI PENELITIAN' yang membandingkan penelitian ini dengan minimal 3-5 penelitian terdahulu.",
                )
            )

        # 3. Check for Tabel II (Research Schedule Table)
        has_table_2 = bool(re.search(r"(?:TABEL\s*II\b|Tabel\s*2\b|Jadwal\s*Penelitian|Bulan\s*10)", text, re.IGNORECASE))
        if not has_table_2:
            issues.append(
                ValidationIssue(
                    code="MISSING_SCHEDULE_TABLE",
                    category="template",
                    message="Tabel II (Rancangan Jadwal Penelitian 10 Bulan) tidak terdeteksi pada Metodologi Penelitian.",
                    severity=ValidationSeverity.WARNING,
                    location="Metodologi Penelitian",
                    suggestion="Tambahkan 'TABEL II. RANCANGAN JADWAL PENELITIAN' dengan timeline 10 bulan.",
                )
            )

        # 4. Check references count in text
        citations = re.findall(r"\[(\d+)\]", text)
        unique_cites = set(citations)
        if len(unique_cites) < 10:
            issues.append(
                ValidationIssue(
                    code="FEW_CITATIONS_IN_TEXT",
                    category="citation",
                    message=f"Hanya terdeteksi {len(unique_cites)} rujukan sitasi unik di dalam naskah (Standar STIS: minimal 20 referensi ilmiah).",
                    severity=ValidationSeverity.WARNING,
                    location="Daftar Pustaka / Sitasi",
                    suggestion="Perkaya sitasi naskah dengan mengutip paper jurnal/prosiding bereputasi (SINTA/Scopus).",
                )
            )

        return issues
