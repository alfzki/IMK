"""
Report Exporter & Terminal Renderer for AI Writing Style Checker.
Memformat hasil audit gaya penulisan ke tampilan terminal berwarna (ANSI), Markdown, dan JSON.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from calm_carson.style.models import StyleReport, StyleSeverity


class StyleExporter:
    """Eksportir dan visualisator hasil audit gaya penulisan AI."""

    @staticmethod
    def render_terminal(report: StyleReport, show_annotated: bool = True, suggest_fixes: bool = True) -> str:
        """Menghasilkan teks berformat terminal ANSI interaktif."""
        # Warna ANSI
        RESET = "\033[0m"
        BOLD = "\033[1m"
        RED = "\033[91m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        MAGENTA = "\033[95m"
        CYAN = "\033[96m"

        # Badge status
        badge_map = {
            "CLEAN_ACADEMIC": f"{GREEN}🟢 LOLOS (GAYA AKADEMIK ALAMI & OBJEKTIF){RESET}",
            "LOW_RISK": f"{YELLOW}🟡 RISIKO RENDAH (TERDAPAT BEBERAPA KLISE MINOR){RESET}",
            "SUSPICIOUS_AI_PATTERNS": f"{MAGENTA}🟠 TERINDIKASI POLA AI (PERLU PENYUNTINGAN SIGNIFIKAN){RESET}",
            "HIGH_RISK_AI_GENERATED": f"{RED}🔴 SANGAT TERINDIKASI AI (WAJIB DIREVISI TOTAL){RESET}",
        }
        badge = badge_map.get(report.risk_verdict, report.risk_verdict)

        # Risk score bar
        filled_bars = int(report.ai_risk_score / 5)
        bar_color = GREEN if report.ai_risk_score < 20 else (YELLOW if report.ai_risk_score < 40 else (MAGENTA if report.ai_risk_score < 70 else RED))
        meter = f"{bar_color}[{'█' * filled_bars}{'░' * (20 - filled_bars)}] {report.ai_risk_score}/100{RESET}"

        out = []
        out.append("=" * 85)
        out.append(f"{BOLD}📊 CALM-CARSON: AUDIT GAYA PENULISAN AI (WIKIPEDIA:SIGNS_OF_AI_WRITING){RESET}")
        out.append(f"   Objek Audit: {CYAN}{report.source_identifier}{RESET}")
        out.append("=" * 85)

        out.append(f"\n{BOLD}📋 STATUS DAN INDEKS RISIKO PENULISAN AI:{RESET}")
        out.append("-" * 85)
        out.append(f"Status Evaluasi    : {badge}")
        out.append(f"Indeks Risiko AI   : {meter}")
        out.append(
            f"Ringkasan Temuan   : {RED}{report.fatal_count} Fatal{RESET} | "
            f"{MAGENTA}{report.high_count} Tinggi{RESET} | "
            f"{YELLOW}{report.medium_count} Sedang{RESET} | "
            f"{CYAN}{report.low_count} Rendah{RESET} "
            f"(Total: {report.total_violations} anomali)"
        )
        out.append(
            f"Metrik Teks        : {report.metrics.total_words} Kata | {report.metrics.total_sentences} Kalimat | "
            f"Avg: {report.metrics.avg_sentence_length:.1f} k/kal | "
            f"Burstiness: {BOLD}{report.metrics.burstiness_score:.2f}{RESET} "
            f"({'Monoton/Robotik' if report.metrics.burstiness_score < 0.28 else 'Alami'})"
        )
        out.append(
            f"Tipografi & Format : {report.metrics.em_dash_count} Tanda Pisah (—) | "
            f"Rasio Daftar: {report.metrics.bullet_line_ratio*100:.1f}% baris berbutir"
        )
        out.append(f"\nKesimpulan Sistem  :\n> {report.summary_verdict}")
        out.append("-" * 85)

        # Tabel Temuan Detail
        if report.violations:
            out.append(f"\n{BOLD}🔍 TABEL RINCIAN POLA GAYA PENULISAN AI YANG DITEMUKAN:{RESET}")
            out.append("-" * 85)
            out.append(f"{'No':<3} | {'Baris':<5} | {'Tingkat':<9} | {'Tipe Pola':<22} | {'Teks Cocok':<24} | {'Saran Perbaikan'}")
            out.append("-" * 85)

            for idx, v in enumerate(report.violations, start=1):
                sev_color = {
                    StyleSeverity.FATAL: RED,
                    StyleSeverity.HIGH: MAGENTA,
                    StyleSeverity.MEDIUM: YELLOW,
                    StyleSeverity.LOW: CYAN,
                }.get(v.severity, RESET)

                sev_str = f"{sev_color}{v.severity.value:<7}{RESET}"
                type_str = v.violation_type.value[:20]
                matched_trunc = v.matched_text[:22] + ".." if len(v.matched_text) > 22 else v.matched_text
                fix_trunc = v.suggested_fix[:45] + "..." if len(v.suggested_fix) > 45 else v.suggested_fix

                out.append(f"{idx:<3} | L{v.line_number:<4} | {sev_str} | {type_str:<22} | {matched_trunc:<24} | {fix_trunc}")

            out.append("-" * 85)

        # Draf teranotasi inline
        if show_annotated and report.annotated_text:
            out.append(f"\n{BOLD}📝 DRAF TEKS DENGAN ANOTASI KOREKSI GAYA BAHASA INLINE:{RESET}")
            out.append("-" * 85)
            out.append(report.annotated_text)
            out.append("-" * 85)

        return "\n".join(out)

    @staticmethod
    def export_markdown(report: StyleReport, output_path: Path | str) -> Path:
        """Menyimpan laporan evaluasi gaya penulisan ke berkas Markdown."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        md = []
        md.append(f"# Laporan Evaluasi Gaya Penulisan AI (Signs of AI Writing)")
        md.append(f"\n- **Objek Audit**: `{report.source_identifier}`")
        md.append(f"- **Indeks Risiko AI**: `{report.ai_risk_score} / 100` ({report.risk_verdict})")
        md.append(f"- **Total Pelanggaran**: {report.total_violations} ({report.fatal_count} Fatal, {report.high_count} High, {report.medium_count} Medium, {report.low_count} Low)")
        md.append(f"- **Burstiness Score**: `{report.metrics.burstiness_score:.3f}` (std dev: {report.metrics.sentence_length_std_dev:.2f})")
        md.append(f"- **Total Em Dash**: {report.metrics.em_dash_count}")
        md.append(f"\n> **Kesimpulan**: {report.summary_verdict}\n")

        md.append("## Tabel Pelanggaran Gaya Penulisan\n")
        md.append("| No | Baris | Tingkat | Tipe Pola | Teks Terdeteksi | Penjelasan & Rekomendasi Perbaikan |")
        md.append("|---|---|---|---|---|---|")

        for idx, v in enumerate(report.violations, start=1):
            md.append(
                f"| {idx} | L{v.line_number} | `{v.severity.value}` | `{v.violation_type.value}` | "
                f"**{v.matched_text}** | {v.explanation} *Saran:* {v.suggested_fix} |"
            )

        md.append("\n## Draf Teranotasi Inline\n")
        md.append("```text")
        md.append(report.annotated_text)
        md.append("```\n")

        path.write_text("\n".join(md), encoding="utf-8")
        return path

    @staticmethod
    def export_json(report: StyleReport, output_path: Path | str) -> Path:
        """Menyimpan laporan evaluasi ke berkas JSON berstruktur."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = report.to_dict()
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return path
