"""Exporter for originality evaluation reports in JSON and Markdown formats."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Optional

from calm_carson.originality.models import OriginalityReport

logger = logging.getLogger(__name__)


def slugify(text: str, max_len: int = 40) -> str:
    """Creates a filesystem-safe slug from text."""
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[\s_-]+", "_", slug).strip("_")
    return slug[:max_len] or "ide_riset"


class OriginalityExporter:
    """Exports originality reports into structured JSON and user-friendly Markdown reports."""

    def __init__(self, workspace_root: Optional[Path] = None):
        if workspace_root is None:
            self.workspace_root = Path(__file__).resolve().parent.parent.parent.parent
        else:
            self.workspace_root = Path(workspace_root)

        self.literature_dir = self.workspace_root / "literature"
        self.brainstorming_dir = self.workspace_root / "brainstorming"

        self.literature_dir.mkdir(parents=True, exist_ok=True)
        self.brainstorming_dir.mkdir(parents=True, exist_ok=True)

    def export_json(
        self,
        report: OriginalityReport,
        output_path: Optional[Path] = None,
    ) -> Path:
        """Saves report to structured JSON file."""
        if output_path is None:
            slug = slugify(report.idea_text)
            target = self.literature_dir / f"originality_eval_{slug}.json"
        else:
            target = output_path

        with open(target, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)

        logger.info("Saved originality JSON report to %s", target)
        return target

    def export_markdown(
        self,
        report: OriginalityReport,
        output_path: Optional[Path] = None,
    ) -> Path:
        """Generates an academic-grade Markdown evaluation report with similarity matrices."""
        if output_path is None:
            slug = slugify(report.idea_text)
            target = self.brainstorming_dir / f"laporan_orisinalitas_{slug}.md"
        else:
            target = output_path

        risk_badge = {
            "HIGH_OVERLAP": "🔴 **RISIKO TINGGI (HIGH OVERLAP)**",
            "MODERATE_OVERLAP": "🟡 **RISIKO SEDANG (MODERATE OVERLAP)**",
            "DISTINCT_NOVEL": "🟢 **KEBARUAN TINGGI (DISTINCT NOVELTY)**",
        }.get(report.overall_risk, report.overall_risk)

        lines = [
            f"# Laporan Uji Orisinalitas & Kebaruan Topik Penelitian",
            "",
            f"> Tanggal Evaluasi: `{report.timestamp}` | Engine: **Dense Multilingual Embedding (RTX 4050 CUDA) + OpenAlex Global Literature**",
            "",
            "---",
            "",
            "## 1. Draf Ide / Rumusan Masalah yang Diuji",
            "",
            f"**\"{report.idea_text}\"**",
            "",
            f"**Kueri Akademis Terstruktur yang Dihasilkan**:",
            "",
        ]

        for q in report.generated_queries:
            lines.append(f"- `{q}`")

        lines.extend([
            "",
            "---",
            "",
            "## 2. Ringkasan Tingkat Kemiripan & Risiko Tumpang Tindih",
            "",
            f"- **Status Evaluasi Orisinalitas**: {risk_badge}",
            f"- **Kemiripan Semantik Tertinggi (*Max Similarity*)**: `{report.max_similarity * 100:.1f}%`",
            f"- **Rata-Rata Kemiripan Top Publikasi (*Mean Similarity*)**: `{report.mean_similarity * 100:.1f}%`",
            f"- **Distribusi Temuan Publikasi**: {report.high_overlap_count} High Overlap (≥70%), {report.moderate_overlap_count} Moderate Overlap (45–69%), {report.low_overlap_count} Low Overlap (<45%)",
            "",
            "> [!NOTE]",
            f"> {report.risk_summary}",
            "",
            "---",
            "",
            "## 3. Publikasi Ilmiah Global Paling Serupa (Tabel Benchmark Literatur)",
            "",
            "| No | Skor Kemiripan | Tingkat Irisan | Judul Publikasi Ilmiah | Penulis & Tahun | Sumber / Jurnal | Sitasi |",
            "| :---: | :---: | :---: | :--- | :--- | :--- | :---: |",
        ])

        for idx, m in enumerate(report.matches[:10], start=1):
            badge = {
                "HIGH": "🔴 Tinggi",
                "MODERATE": "🟡 Sedang",
                "LOW": "🟢 Rendah",
            }.get(m.overlap_level, m.overlap_level)

            authors_short = m.authors[0] if len(m.authors) == 1 else f"{m.authors[0]} et al."
            url_part = f"[{m.title[:85]}...]({m.url})" if m.url else m.title[:85]

            lines.append(
                f"| {idx} | **`{m.similarity_score * 100:.1f}%`** | {badge} | {url_part} | {authors_short} ({m.year}) | {m.venue[:30]} | {m.citation_count} |"
            )

        lines.extend([
            "",
            "---",
            "",
            "## 4. Masukan Kritis & Aspek Pembeda (*Novelty Reinforcement Strategies*)",
            "",
            "Untuk memastikan topik skripsi mahasiswa memiliki kebaruan yang diakui penguji sidang dan tidak sekadar menduplikasi publikasi internasional di atas, terapkan rekomendasi penguatan berikut:",
            "",
        ])

        for idx, fb in enumerate(report.differentiation_feedbacks, start=1):
            lines.extend([
                f"### {idx}. Dimensi: {fb.dimension_name}",
                f"- **Analisis Irisan Literatur**: {fb.overlap_analysis}",
                f"- **Rekomendasi Pembeda (Novelty)**: {fb.recommended_differentiation}",
                f"- **Panduan Implementasi Teknis**: *{fb.actionable_guidance}*",
                "",
            ])

        lines.extend([
            "---",
            "",
            "## 5. Kesimpulan & Rekomendasi Langkah Lanjutan",
            "",
            "1. **Jadikan Publikasi Teratas sebagai Baseline**: Masukkan paper dengan skor kemiripan tertinggi di atas ke dalam **Tabel I (Kontribusi Penelitian)** proposal penelitian untuk menunjukkan penguasaan *state-of-the-art*.",
            "2. **Tegaskan Ruang Lingkup Sistem (SIS)**: Hindari hanya mengulang pemodelan statistik; tekankan pada rekayasa perangkat lunak dan otomasi proses bisnis statistik (DSRM).",
            "3. **Gunakan Metrik Pengujian Multi-Dimensi**: Lengkapi proposal dengan rencana evaluasi standar ISO/IEC 25010 (keamanan, fungsionalitas, performa, dan kegunaan).",
            "",
        ])

        content = "\n".join(lines)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info("Saved originality Markdown report to %s", target)
        return target
