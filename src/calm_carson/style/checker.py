"""
AI Writing Style Checker Core Engine.
Mesin audit pendeteksi tanda-tanda penulisan AI berdasarkan taksonomi Wikipedia:Signs_of_AI_writing.
Mendukung naskah dwibahasa (Inggris & Indonesia), evaluasi kaidah PUEBI/EYD V, serta metrik statistik burstiness.
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from calm_carson.style.models import (
    StyleMetrics,
    StyleReport,
    StyleSeverity,
    StyleViolation,
    StyleViolationType,
)
from calm_carson.style.patterns import (
    AI_VOCABULARY_EN,
    AI_VOCABULARY_ID,
    CHATBOT_LEAK_PATTERNS,
    CONVERSATIONAL_PATTERNS,
    COPULATIVE_AVOIDANCE_PATTERNS,
    DOUBLE_HYPHEN_PATTERN,
    FORMULAIC_CONCLUSION_PATTERNS,
    KNOWLEDGE_CUTOFF_PATTERNS,
    NEGATIVE_PARALLELISM_PATTERNS,
    SPACED_EM_DASH_PATTERN,
    SUPERFICIAL_ANALYSIS_PATTERNS,
)


class AIStyleChecker:
    """Mesin audit gaya penulisan draf terhadap pola-pola kecerdasan buatan."""

    def __init__(self) -> None:
        # Regex rule of three (tiga kata terhubung koma dan konjungsi 'dan'/'and'/'serta')
        self._rule_of_three_re = re.compile(
            r"\b([a-zA-Z\-]{3,25}),\s+([a-zA-Z\-]{3,25}),?\s+(?:dan|and|serta)\s+([a-zA-Z\-]{3,25})\b",
            re.IGNORECASE,
        )
        # Regex inline-header bullet list: * **Header**: or - **Header**:
        self._inline_header_re = re.compile(r"^\s*[\*\-]\s+\*\*[^*:]+\*\*:\s+")
        # Regex bullet line umum
        self._bullet_line_re = re.compile(r"^\s*[\*\-]\s+|\s*\d+\.\s+")

    def check_file(self, file_path: Path | str) -> StyleReport:
        """Membaca berkas draf dan menjalankan audit gaya penulisan."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Berkas draf tidak ditemukan: {path}")

        text = path.read_text(encoding="utf-8", errors="ignore")
        return self.check_text(text, source_id=str(path))

    def check_text(self, text: str, source_id: str = "draft_text") -> StyleReport:
        """Mengaudit teks draf terhadap seluruh tanda penulisan AI."""
        if not text or not text.strip():
            return StyleReport(
                source_identifier=source_id,
                ai_risk_score=0,
                risk_verdict="CLEAN_ACADEMIC",
                total_violations=0,
                fatal_count=0,
                high_count=0,
                medium_count=0,
                low_count=0,
                summary_verdict="Teks draf kosong.",
            )

        lines = text.splitlines()
        violations: List[StyleViolation] = []

        # 1. Hitung metrik kuantitatif dan statistik burstiness
        metrics = self._calculate_metrics(lines, text)

        # 2. Audit baris demi baris dan kalimat demi kalimat
        violations.extend(self._scan_chatbot_leaks(lines))
        violations.extend(self._scan_conversational_and_cutoffs(lines))
        violations.extend(self._scan_em_dash_violations(lines))
        violations.extend(self._scan_ai_vocabulary(lines))
        violations.extend(self._scan_copulatives_and_parallelisms(lines))
        violations.extend(self._scan_superficial_and_conclusions(lines))
        violations.extend(self._scan_rule_of_three(lines))
        violations.extend(self._scan_structural_lists(lines, metrics))

        # 3. Periksa anomali variansi panjang kalimat (burstiness)
        if metrics.total_sentences >= 5 and metrics.burstiness_score < 0.28:
            violations.append(
                StyleViolation(
                    violation_type=StyleViolationType.BURSTINESS_LOW,
                    severity=StyleSeverity.LOW,
                    rule_name="monotonous_sentence_burstiness",
                    matched_text=f"Burstiness index: {metrics.burstiness_score:.2f} (std_dev: {metrics.sentence_length_std_dev:.1f})",
                    line_number=1,
                    sentence="Keseragaman panjang kalimat di seluruh naskah.",
                    explanation=(
                        "Variansi panjang kalimat sangat rendah (ritme monoton). "
                        "Teks yang dihasilkan LLM cenderung memiliki panjang kalimat yang sangat seragam (~18-22 kata) tanpa variasi ritmis."
                    ),
                    suggested_fix="Campurkan kalimat ringkas tegas dengan kalimat majemuk terstruktur untuk menciptakan ritme akademik alami.",
                )
            )

        # 4. Agregasi statistik keparahan
        fatal_count = sum(1 for v in violations if v.severity == StyleSeverity.FATAL)
        high_count = sum(1 for v in violations if v.severity == StyleSeverity.HIGH)
        medium_count = sum(1 for v in violations if v.severity == StyleSeverity.MEDIUM)
        low_count = sum(1 for v in violations if v.severity == StyleSeverity.LOW)
        total_violations = len(violations)

        # 5. Hitung skor risiko AI (0 s.d. 100)
        ai_risk_score = self._compute_risk_score(
            fatal_count=fatal_count,
            high_count=high_count,
            medium_count=medium_count,
            low_count=low_count,
            metrics=metrics,
        )

        # 6. Tentukan klasifikasi verdict
        if fatal_count > 0 or ai_risk_score >= 70:
            risk_verdict = "HIGH_RISK_AI_GENERATED"
            summary_verdict = (
                "🔴 SANGAT TERINDIKASI GAYA PENULISAN AI (Wajib Direvisi Total). "
                f"Ditemukan {fatal_count} kebocoran fatal dan {high_count} pola klise berat khas model AI."
            )
        elif ai_risk_score >= 40:
            risk_verdict = "SUSPICIOUS_AI_PATTERNS"
            summary_verdict = (
                "🟠 TERINDIKASI POLA PENULISAN AI (Perlu Penyuntingan Signifikan). "
                f"Terdeteksi {high_count} pola bernilai tinggi dan {medium_count} konstruksi kalimat artifisial."
            )
        elif ai_risk_score >= 20:
            risk_verdict = "LOW_RISK"
            summary_verdict = (
                "🟡 RISIKO RENDAH (Perbaikan Minor). Teks secara umum wajar, namun mengandung beberapa "
                f"frasa klise umum ({medium_count + low_count} temuan minor)."
            )
        else:
            risk_verdict = "CLEAN_ACADEMIC"
            summary_verdict = (
                "🟢 LOLOS AUDIT GAYA PENULISAN (Naskah Alami & Bebas Pola AI). "
                "Gaya bahasa objektif, presisi, dan terbebas dari klise artifisial."
            )

        # 7. Bentuk draf teranotasi inline
        annotated_text = self._build_annotated_text(text, violations)

        return StyleReport(
            source_identifier=source_id,
            ai_risk_score=ai_risk_score,
            risk_verdict=risk_verdict,
            total_violations=total_violations,
            fatal_count=fatal_count,
            high_count=high_count,
            medium_count=medium_count,
            low_count=low_count,
            violations=violations,
            metrics=metrics,
            annotated_text=annotated_text,
            summary_verdict=summary_verdict,
        )

    def _calculate_metrics(self, lines: List[str], full_text: str) -> StyleMetrics:
        """Menghitung metrik kuantitatif draf teks."""
        words = re.findall(r"\b[a-zA-Z0-9_\-]+\b", full_text)
        total_words = len(words)

        # Pisahkan kalimat berdasarkan tanda titik, tanya, seru
        raw_sentences = re.split(r"[.!?]+", full_text)
        sentences = [s.strip() for s in raw_sentences if len(s.strip().split()) >= 3]
        total_sentences = len(sentences)

        # Hitung panjang kata per kalimat
        sentence_lengths = [len(s.split()) for s in sentences]
        avg_sentence_length = sum(sentence_lengths) / total_sentences if total_sentences > 0 else 0.0

        # Standar deviasi panjang kalimat
        if total_sentences > 1:
            variance = sum((x - avg_sentence_length) ** 2 for x in sentence_lengths) / (total_sentences - 1)
            sentence_length_std_dev = math.sqrt(variance)
        else:
            sentence_length_std_dev = 0.0

        burstiness_score = (
            sentence_length_std_dev / avg_sentence_length if avg_sentence_length > 0 else 0.0
        )

        # Hitung paragraf dan baris ber-bullet
        paragraphs = [p for p in full_text.split("\n\n") if p.strip()]
        total_paragraphs = len(paragraphs)

        non_empty_lines = [line for line in lines if line.strip()]
        bullet_lines = [line for line in non_empty_lines if self._bullet_line_re.match(line)]
        bullet_line_ratio = (
            len(bullet_lines) / len(non_empty_lines) if non_empty_lines else 0.0
        )

        # Hitung em dash
        em_dash_count = full_text.count("—") + full_text.count(" – ") + len(DOUBLE_HYPHEN_PATTERN.findall(full_text))

        # Vocabulary richness (Type-Token Ratio)
        unique_words = set(w.lower() for w in words)
        ttr = len(unique_words) / total_words if total_words > 0 else 0.0

        return StyleMetrics(
            total_words=total_words,
            total_sentences=total_sentences,
            total_paragraphs=total_paragraphs,
            avg_sentence_length=avg_sentence_length,
            sentence_length_std_dev=sentence_length_std_dev,
            burstiness_score=burstiness_score,
            bullet_line_ratio=bullet_line_ratio,
            em_dash_count=em_dash_count,
            vocabulary_richness=ttr,
        )

    def _scan_chatbot_leaks(self, lines: List[str]) -> List[StyleViolation]:
        """Memindai token sistem dan artefak antarmuka LLM (FATAL)."""
        violations: List[StyleViolation] = []
        for line_idx, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            for rule_name, pattern, explanation, fix in CHATBOT_LEAK_PATTERNS:
                for match in pattern.finditer(line):
                    violations.append(
                        StyleViolation(
                            violation_type=StyleViolationType.CHATBOT_LEAK,
                            severity=StyleSeverity.FATAL,
                            rule_name=rule_name,
                            matched_text=match.group(0),
                            line_number=line_idx,
                            sentence=line.strip(),
                            explanation=explanation,
                            suggested_fix=fix,
                        )
                    )
        return violations

    def _scan_conversational_and_cutoffs(self, lines: List[str]) -> List[StyleViolation]:
        """Memindai sapaan percakapan dan penafian batas pengetahuan LLM."""
        violations: List[StyleViolation] = []
        for line_idx, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            # Conversational fillers
            for rule_name, pattern, explanation, fix, severity in CONVERSATIONAL_PATTERNS:
                for match in pattern.finditer(line):
                    violations.append(
                        StyleViolation(
                            violation_type=StyleViolationType.CONVERSATIONAL_FILLER,
                            severity=severity,
                            rule_name=rule_name,
                            matched_text=match.group(0),
                            line_number=line_idx,
                            sentence=line.strip(),
                            explanation=explanation,
                            suggested_fix=fix,
                        )
                    )
            # Knowledge cutoff disclaimers
            for rule_name, pattern, explanation, fix in KNOWLEDGE_CUTOFF_PATTERNS:
                for match in pattern.finditer(line):
                    violations.append(
                        StyleViolation(
                            violation_type=StyleViolationType.KNOWLEDGE_CUTOFF,
                            severity=StyleSeverity.FATAL,
                            rule_name=rule_name,
                            matched_text=match.group(0),
                            line_number=line_idx,
                            sentence=line.strip(),
                            explanation=explanation,
                            suggested_fix=fix,
                        )
                    )
        return violations

    def _scan_em_dash_violations(self, lines: List[str]) -> List[StyleViolation]:
        """
        Memindai penggunaan tanda pisah (em dash '—') yang berlebihan dan tidak sesuai kaidah kebahasaan.
        Kaidah PUEBI / EYD V:
        - Tanda pisah (—) TIDAK menggunakan spasi sebelum dan sesudahnya (misal: 'fitur—yang dirilis kemarin—berfungsi').
        - Tanda pisah berspasi ('fitur — yang dirilis kemarin — berfungsi') adalah kesalahan tipografi khas LLM.
        - Penggunaan lebih dari satu tanda pisah dalam satu kalimat merupakan dramatisasi gaya promosi/jurnalisme santai.
        """
        violations: List[StyleViolation] = []
        for line_idx, line in enumerate(lines, start=1):
            if not line.strip():
                continue

            # Abaikan baris bibliografi / daftar pustaka ([X] Penulis, "Judul...") yang memuat judul verbatim paper
            if re.match(r"^\s*\[\d+\]", line):
                continue

            # 1. Deteksi tanda pisah berspasi (Spaced Em Dash / En Dash)
            for match in SPACED_EM_DASH_PATTERN.finditer(line):
                violations.append(
                    StyleViolation(
                        violation_type=StyleViolationType.EM_DASH_OVERUSE,
                        severity=StyleSeverity.MEDIUM,
                        rule_name="spaced_em_dash_typography",
                        matched_text=match.group(0),
                        line_number=line_idx,
                        sentence=line.strip(),
                        explanation=(
                            "Tanda pisah (—) ditulis dengan spasi sebelum dan/atau sesudahnya. "
                            "Kaidah PUEBI/EYD V dan IEEE Style mewajibkan tanda pisah ditulis rapat tanpa spasi. "
                            "Spasi pada tanda pisah adalah kesalahan tipografi khas output LLM."
                        ),
                        suggested_fix="Hapus spasi di sekitar tanda pisah (contoh: 'kata—kata' bukan 'kata — kata'), atau gunakan tanda koma/kurung.",
                    )
                )

            # 2. Deteksi double hyphen berspasi (' -- ')
            for match in DOUBLE_HYPHEN_PATTERN.finditer(line):
                violations.append(
                    StyleViolation(
                        violation_type=StyleViolationType.EM_DASH_OVERUSE,
                        severity=StyleSeverity.MEDIUM,
                        rule_name="double_hyphen_surrogate",
                        matched_text=match.group(0),
                        line_number=line_idx,
                        sentence=line.strip(),
                        explanation="Penggunaan tanda hubung ganda berspasi (' -- ') sebagai pengganti em dash.",
                        suggested_fix="Gunakan tanda pisah Unicode tanpa spasi (—) atau gunakan koma pembatas klausul.",
                    )
                )

            # 3. Deteksi kepadatan em dash dalam satu baris/kalimat (>1 em dash)
            em_dash_occurrences = line.count("—")
            if em_dash_occurrences >= 3:
                violations.append(
                    StyleViolation(
                        violation_type=StyleViolationType.EM_DASH_OVERUSE,
                        severity=StyleSeverity.HIGH,
                        rule_name="excessive_em_dash_density",
                        matched_text=f"{em_dash_occurrences}x '—' dalam satu baris",
                        line_number=line_idx,
                        sentence=line.strip(),
                        explanation=(
                            f"Ditemukan {em_dash_occurrences} tanda pisah (em dash) dalam satu baris/kalimat. "
                            "LLM sering menggunakan tanda pisah secara berulang untuk memberi penekanan dramatis semu (punchy sales style)."
                        ),
                        suggested_fix="Sederhanakan kalimat dengan tanda koma (,), tanda kurung untuk aposisi, atau pecah menjadi dua kalimat terpisah.",
                    )
                )
            elif em_dash_occurrences == 2:
                # Periksa apakah 2 em dash membentuk sepasang aposisi tanpa spasi (word—clause—word)
                is_clean_pair = bool(re.search(r"[^\s—]+—[^\s—].*?[^\s—]—[^\s—]+", line))
                sev = StyleSeverity.LOW if is_clean_pair else StyleSeverity.MEDIUM
                rule = "parenthetical_em_dash_pair" if is_clean_pair else "excessive_em_dash_density"
                violations.append(
                    StyleViolation(
                        violation_type=StyleViolationType.EM_DASH_OVERUSE,
                        severity=sev,
                        rule_name=rule,
                        matched_text="Sepasang tanda pisah (—...—)",
                        line_number=line_idx,
                        sentence=line.strip(),
                        explanation=(
                            "Penggunaan sepasang tanda pisah sebagai klausa sisipan (aposisi). "
                            "Meskipun secara kaidah PUEBI diperbolehkan jika tanpa spasi, dalam naskah akademik formal STIS "
                            "tanda kurung (...) atau tanda koma lebih disukai untuk menjaga formalitas."
                        ),
                        suggested_fix="Pertimbangkan mengganti sepasang tanda pisah dengan tanda kurung (...) atau tanda koma (,).",
                    )
                )

        return violations

    def _scan_ai_vocabulary(self, lines: List[str]) -> List[StyleViolation]:
        """Memindai kata dan frasa klise over-represented pasca-2022 (Inggris & Indonesia)."""
        violations: List[StyleViolation] = []

        # Kompilasi pola kata tunggal dan frasa dwibahasa
        for line_idx, line in enumerate(lines, start=1):
            if not line.strip():
                continue

            # Periksa kosakata Bahasa Indonesia
            for phrase, meta in AI_VOCABULARY_ID.items():
                pattern = re.compile(rf"\b{re.escape(phrase)}\b", re.IGNORECASE)
                for match in pattern.finditer(line):
                    sev = StyleSeverity(meta["severity"])
                    violations.append(
                        StyleViolation(
                            violation_type=StyleViolationType.AI_VOCABULARY,
                            severity=sev,
                            rule_name=meta["rule"],
                            matched_text=match.group(0),
                            line_number=line_idx,
                            sentence=line.strip(),
                            explanation=meta["explanation"],
                            suggested_fix=meta["fix"],
                        )
                    )

            # Periksa kosakata Bahasa Inggris
            for word, meta in AI_VOCABULARY_EN.items():
                pattern = re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE)
                for match in pattern.finditer(line):
                    sev = StyleSeverity(meta["severity"])
                    violations.append(
                        StyleViolation(
                            violation_type=StyleViolationType.AI_VOCABULARY,
                            severity=sev,
                            rule_name=meta["rule"],
                            matched_text=match.group(0),
                            line_number=line_idx,
                            sentence=line.strip(),
                            explanation=meta["explanation"],
                            suggested_fix=meta["fix"],
                        )
                    )

        return violations

    def _scan_copulatives_and_parallelisms(self, lines: List[str]) -> List[StyleViolation]:
        """Memindai penghindaran kata kopula langsung dan negative parallelisms."""
        violations: List[StyleViolation] = []
        for line_idx, line in enumerate(lines, start=1):
            if not line.strip():
                continue

            # Copulative Avoidance
            for rule_name, pattern, explanation, fix in COPULATIVE_AVOIDANCE_PATTERNS:
                for match in pattern.finditer(line):
                    violations.append(
                        StyleViolation(
                            violation_type=StyleViolationType.COPULATIVE_AVOIDANCE,
                            severity=StyleSeverity.MEDIUM,
                            rule_name=rule_name,
                            matched_text=match.group(0),
                            line_number=line_idx,
                            sentence=line.strip(),
                            explanation=explanation,
                            suggested_fix=fix,
                        )
                    )

            # Negative Parallelisms
            for rule_name, pattern, explanation, fix in NEGATIVE_PARALLELISM_PATTERNS:
                for match in pattern.finditer(line):
                    violations.append(
                        StyleViolation(
                            violation_type=StyleViolationType.NEGATIVE_PARALLELISM,
                            severity=StyleSeverity.MEDIUM,
                            rule_name=rule_name,
                            matched_text=match.group(0),
                            line_number=line_idx,
                            sentence=line.strip(),
                            explanation=explanation,
                            suggested_fix=fix,
                        )
                    )
        return violations

    def _scan_superficial_and_conclusions(self, lines: List[str]) -> List[StyleViolation]:
        """Memindai buntut partisipel pemanis (-ing) dan penutup draf formulaik."""
        violations: List[StyleViolation] = []
        for line_idx, line in enumerate(lines, start=1):
            if not line.strip():
                continue

            # Superficial Participles
            for rule_name, pattern, explanation, fix in SUPERFICIAL_ANALYSIS_PATTERNS:
                for match in pattern.finditer(line):
                    violations.append(
                        StyleViolation(
                            violation_type=StyleViolationType.SUPERFICIAL_ANALYSIS,
                            severity=StyleSeverity.HIGH,
                            rule_name=rule_name,
                            matched_text=match.group(0),
                            line_number=line_idx,
                            sentence=line.strip(),
                            explanation=explanation,
                            suggested_fix=fix,
                        )
                    )

            # Formulaic Conclusions
            for rule_name, pattern, explanation, fix in FORMULAIC_CONCLUSION_PATTERNS:
                for match in pattern.finditer(line):
                    violations.append(
                        StyleViolation(
                            violation_type=StyleViolationType.FORMULAIC_CONCLUSION,
                            severity=StyleSeverity.HIGH,
                            rule_name=rule_name,
                            matched_text=match.group(0),
                            line_number=line_idx,
                            sentence=line.strip(),
                            explanation=explanation,
                            suggested_fix=fix,
                        )
                    )
        return violations

    def _scan_rule_of_three(self, lines: List[str]) -> List[StyleViolation]:
        """Memindai penggunaan berulang formula rule of three (trio kata sifat/frasa)."""
        violations: List[StyleViolation] = []
        for line_idx, line in enumerate(lines, start=1):
            if not line.strip():
                continue

            matches = list(self._rule_of_three_re.finditer(line))
            if matches:
                for match in matches:
                    w1, w2, w3 = match.group(1), match.group(2), match.group(3)
                    # Filter: hindari flag jika ketiga kata sangat pendek (e.g. data, teks, dan kode)
                    if len(w1) < 4 and len(w2) < 4 and len(w3) < 4:
                        continue

                    violations.append(
                        StyleViolation(
                            violation_type=StyleViolationType.RULE_OF_THREE,
                            severity=StyleSeverity.LOW,
                            rule_name="rule_of_three_adjectives",
                            matched_text=match.group(0),
                            line_number=line_idx,
                            sentence=line.strip(),
                            explanation=(
                                "Struktur 'rule of three' (tiga kata sifat/frasa beruntun). "
                                "LLM sering mengandalkan pola ritmis tiga kata untuk menciptakan kesan kelengkapan semu."
                            ),
                            suggested_fix="Fokuskan pada atribut teknis yang paling krusial disertai parameter pembuktiannya.",
                        )
                    )
        return violations

    def _scan_structural_lists(self, lines: List[str], metrics: StyleMetrics) -> List[StyleViolation]:
        """Memindai dominasi berlebihan daftar bertajuk tebal (inline-header vertical lists)."""
        violations: List[StyleViolation] = []

        inline_header_count = sum(1 for line in lines if self._inline_header_re.match(line))
        # Jika terdapat lebih dari 4 daftar bertajuk tebal dan rasio daftar > 35%
        if inline_header_count >= 4 and metrics.bullet_line_ratio > 0.35:
            first_line = next(i for i, line in enumerate(lines, 1) if self._inline_header_re.match(line))
            violations.append(
                StyleViolation(
                    violation_type=StyleViolationType.INLINE_HEADER_LIST,
                    severity=StyleSeverity.MEDIUM,
                    rule_name="inline_header_vertical_list_overuse",
                    matched_text=f"{inline_header_count} baris daftar bertajuk tebal ({metrics.bullet_line_ratio*100:.1f}% teks)",
                    line_number=first_line,
                    sentence="Ketergantungan berlebihan pada daftar vertikal berbutir (* **Header**: Deskripsi).",
                    explanation=(
                        "Ketergantungan pada format daftar bertajuk tebal alih-alih narasi analitik berkesinambungan. "
                        "Format ini merupakan tanda khas ringkasan cepat AI yang menghindari pertautan logika antar-paragraf."
                    ),
                    suggested_fix="Ubah butir-butir daftar menjadi paragraf analitik terpadu dengan konjungsi logis yang mengalir.",
                )
            )

        return violations

    def _compute_risk_score(
        self,
        fatal_count: int,
        high_count: int,
        medium_count: int,
        low_count: int,
        metrics: StyleMetrics,
    ) -> int:
        """Menghitung skor risiko gaya penulisan AI secara komposit (skala 0 s.d. 100)."""
        if fatal_count > 0:
            score = 75 + (fatal_count * 10) + (high_count * 5)
            return min(score, 100)

        # Bobot per tingkat keparahan
        score = (high_count * 14) + (medium_count * 6) + (low_count * 2)

        # Penalti kepadatan kata klise per 100 kata
        if metrics.total_words > 0:
            vocab_density = (high_count + medium_count) / (metrics.total_words / 100)
            if vocab_density > 1.5:
                score += 15
            elif vocab_density > 0.8:
                score += 8

        # Penalti em dash berlebih
        if metrics.em_dash_count >= 3:
            score += min(metrics.em_dash_count * 3, 15)

        # Penalti burstiness monoton
        if metrics.total_sentences >= 5 and metrics.burstiness_score < 0.25:
            score += 10

        return max(0, min(score, 100))

    def _build_annotated_text(self, original_text: str, violations: List[StyleViolation]) -> str:
        """Menyisipkan anotasi inline pada teks asli untuk memudahkan peninjauan pengguna."""
        lines = original_text.splitlines()

        # Kelompokkan pelanggaran berdasarkan nomor baris
        v_by_line: Dict[int, List[StyleViolation]] = {}
        for v in violations:
            v_by_line.setdefault(v.line_number, []).append(v)

        annotated_lines: List[str] = []
        for idx, line in enumerate(lines, start=1):
            annotated_lines.append(line)
            if idx in v_by_line:
                for v in v_by_line[idx]:
                    tag = f"  >>> [⚠️ AI_STYLE ({v.severity.value}): '{v.matched_text}' -> Saran: {v.suggested_fix}]"
                    annotated_lines.append(tag)

        return "\n".join(annotated_lines)


# Helper function instan
def check_text_style(text: str, source_id: str = "text") -> StyleReport:
    """Fungsi helper cepat untuk mengaudit teks."""
    checker = AIStyleChecker()
    return checker.check_text(text, source_id=source_id)


def check_file_style(file_path: Path | str) -> StyleReport:
    """Fungsi helper cepat untuk mengaudit berkas draf."""
    checker = AIStyleChecker()
    return checker.check_file(file_path)
