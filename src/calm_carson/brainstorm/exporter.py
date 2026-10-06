"""Exporter for research gaps, synthesis taxonomy, and markdown roadmap."""

from __future__ import annotations

import csv
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

from calm_carson.brainstorm.models import BrainstormClusterSummary, ResearchGapItem
from calm_carson.brainstorm.synthesizer import BrainstormSynthesizer

logger = logging.getLogger(__name__)


class BrainstormExporter:
    """Exports research gaps into JSON, CSV, and formatted Markdown reports."""

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
        items: List[ResearchGapItem],
        output_path: Optional[Path] = None,
    ) -> Path:
        """Export raw and categorized gap items to JSON."""
        target = output_path or (self.literature_dir / "brainstorming_gaps.json")
        data = [item.to_dict() for item in items]
        with open(target, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info("Exported %d gaps to %s", len(items), target)
        return target

    def export_csv(
        self,
        items: List[ResearchGapItem],
        output_path: Optional[Path] = None,
    ) -> Path:
        """Export gap items to spreadsheet-friendly CSV."""
        target = output_path or (self.literature_dir / "brainstorming_gaps.csv")
        headers = [
            "id",
            "cluster",
            "gap_category",
            "source_type",
            "year",
            "author",
            "source_title",
            "synthesized_summary",
            "recommended_opportunity",
            "source_location",
        ]

        with open(target, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
            writer.writeheader()
            for item in items:
                row = item.to_dict()
                # flatten or sanitize text
                row["synthesized_summary"] = (row.get("synthesized_summary") or "").replace("\n", " ")
                row["recommended_opportunity"] = (row.get("recommended_opportunity") or "").replace("\n", " ")
                writer.writerow(row)

        logger.info("Exported %d gaps to %s", len(items), target)
        return target

    def export_markdown_report(
        self,
        cluster_summaries: Dict[str, BrainstormClusterSummary],
        matrix: List[Dict[str, str]],
        output_path: Optional[Path] = None,
    ) -> Path:
        """Generate a comprehensive, beautiful Markdown synthesis report for brainstorming."""
        target = output_path or (self.brainstorming_dir / "peta_peluang_riset.md")

        total_gaps = sum(cs.total_items for cs in cluster_summaries.values())

        lines = [
            "# Peta Peluang Riset & Sintesis Kesenjangan Topik Skripsi SIS",
            "",
            "> Dokumen ini dihasilkan secara otomatis oleh **Research Gap Extractor & Brainstorm Synthesizer** dengan menambang keterbatasan metodologi (*limitations*), permasalahan terbuka (*open problems*), dan arahan penelitian lanjutan (*future work*) dari korpus dokumen lokal: **389 skripsi alumni STIS (2021–2026)**, artikel ilmiah internasional bereputasi, serta dokumen proposal penelitian.",
            "",
            "---",
            "",
            "## 1. Statistik Korpus Kesenjangan Penelitian",
            "",
            f"- **Total Kesenjangan & Rekomendasi Teridentifikasi**: {total_gaps} item",
            "",
            "| Klaster Topik SIS | Masalah Terbuka | Keterbatasan Metodologi | Saran Riset (Future Work) | Total |",
            "| :--- | :---: | :---: | :---: | :---: |",
        ]

        for cid, cs in cluster_summaries.items():
            lines.append(
                f"| **{cs.cluster_name.split(' (')[0]}** | {len(cs.open_problems)} | {len(cs.methodological_bottlenecks)} | {len(cs.future_works)} | **{cs.total_items}** |"
            )

        lines.extend([
            "",
            "---",
            "",
            "## 2. Matriks Komparasi Strategis: Skripsi Terdahulu vs Peluang Novelty",
            "",
            "Tabel ini memetakan pola tipikal skripsi alumni STIS sebelumnya dan bagaimana kesenjangan tersebut dapat diangkat menjadi topik skripsi baru yang berbobot rekayasa sistem informasi statistik:",
            "",
            "| Klaster Fokus | Pola Skripsi Terdahulu | Keterbatasan / Bottleneck | Peluang Novelty & Usulan Solusi | Kelayakan STIS |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ])

        for row in matrix:
            lines.append(
                f"| **{row['cluster']}** | {row['past_pattern']} | {row['methodological_bottleneck']} | {row['proposed_novelty']} | {row['stis_suitability']} |"
            )

        lines.extend([
            "",
            "---",
            "",
            "## 3. Rincian Temuan Kesenjangan & Peluang Riset per Klaster",
            "",
        ])

        for cid, cs in cluster_summaries.items():
            lines.extend([
                f"### A. Klaster: {cs.cluster_name}",
                "",
                "#### 💡 Rekomendasi Peluang Penelitian Baru Terpilih:",
            ])
            for opp in cs.synthesized_opportunities:
                lines.append(f"- **{opp}**")
            lines.append("")

            # Top Future Works
            if cs.future_works:
                lines.append("#### 📌 Saran Penelitian Selanjutnya (*Future Work*) dari Dokumen Terdahulu:")
                for item in cs.future_works[:5]:
                    lines.append(
                        f"- **[{item.year}] {item.source_title}** ({item.author}):\n"
                        f"  > *\"{item.raw_excerpt[:280]}...\"*\n"
                        f"  - **Arah Novelty**: {item.recommended_opportunity}\n"
                        f"  - *Sumber*: `{item.source_location}`"
                    )
                lines.append("")

            # Top Methodological Bottlenecks
            if cs.methodological_bottlenecks:
                lines.append("#### ⚠️ Keterbatasan Metodologi (*Methodological Bottlenecks*) yang Belum Terselesaikan:")
                for item in cs.methodological_bottlenecks[:5]:
                    lines.append(
                        f"- **[{item.year}] {item.source_title}** ({item.author}):\n"
                        f"  > *\"{item.raw_excerpt[:280]}...\"*\n"
                        f"  - **Solusi Rekayasa**: {item.recommended_opportunity}\n"
                        f"  - *Sumber*: `{item.source_location}`"
                    )
                lines.append("")

            lines.append("---")
            lines.append("")

        lines.extend([
            "## 4. Panduan Eksekusi bagi Mahasiswa SIS",
            "",
            "1. **Pilih Masalah, Bukan Alat**: Jangan memulai dari *'Saya ingin pakai FastAPI'* atau *'Saya ingin pakai LLM'*, melainkan dari masalah konkret (misal: *'Pencacahan lapangan masih rentan pemalsuan entri'* atau *'Diseminasi data mikro rentan melanggar UU PDP'*).",
            "2. **Pastikan Artefak Sistem Nyata (DSRM)**: Skripsi SIS wajib menghasilkan artefak perangkat lunak yang dapat didemonstrasikan saat sidang, bukan sekadar kajian model atau analitik notebook.",
            "3. **Uji Standar ISO/IEC 25010**: Selalu siapkan skenario pengujian Functional Suitability, Usability (SUS/UEQ), Security (VAPT/OWASP), dan Performance Efficiency (latensi/stress test).",
            "",
        ])

        content = "\n".join(lines)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info("Exported markdown report to %s", target)
        return target
