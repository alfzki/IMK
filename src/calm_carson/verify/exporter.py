"""Exporter for factual verification audit reports in JSON and Markdown formats."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Optional

from calm_carson.verify.models import VerificationReport

logger = logging.getLogger(__name__)


def slugify(text: str, max_len: int = 35) -> str:
    """Creates a filesystem-safe slug from text."""
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[\s_-]+", "_", slug).strip("_")
    return slug[:max_len] or "draf_verifikasi"


class VerificationExporter:
    """Exports verification reports into structured JSON and user-friendly Markdown audit reports."""

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
        report: VerificationReport,
        output_path: Optional[Path] = None,
    ) -> Path:
        """Saves verification report to JSON file."""
        if output_path is None:
            slug = slugify(report.draft_text)
            target = self.literature_dir / f"fact_check_{slug}.json"
        else:
            target = output_path

        with open(target, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)

        logger.info("Saved verification JSON to %s", target)
        return target

    def export_markdown(
        self,
        report: VerificationReport,
        output_path: Optional[Path] = None,
    ) -> Path:
        """Generates a detailed factual verification report in Markdown."""
        if output_path is None:
            slug = slugify(report.draft_text)
            target = self.brainstorming_dir / f"laporan_verifikasi_{slug}.md"
        else:
            target = output_path

        verdict_badge = {
            "READY_FOR_SUBMISSION": "🟢 **LOLOS VERIFIKASI (SIAP DIAJUKAN)**",
            "NEEDS_MINOR_CITATION": "🟡 **PERLU PERBAIKAN SITASI MINOR**",
            "FATAL_CONTRADICTIONS": "🔴 **TERDAPAT KONTRADIKSI FAKTUAL / PERLU REVISI TOTAL**",
        }.get(report.overall_verdict, report.overall_verdict)

        lines = [
            "# Laporan Audit Keabsahan Faktual & Validitas Sitasi Draf Tulisan",
            "",
            f"> Tanggal Audit: `{report.timestamp}` | Engine: **Corpus Hybrid Search + Dense Multilingual MiniLM (RTX 4050 CUDA)**",
            "",
            "---",
            "",
            "## 1. Status Kelayakan Dokumen",
            "",
            f"- **Status Verifikasi Keseluruhan**: {verdict_badge}",
            f"- **Ringkasan Audit**: {report.verdict_summary}",
            f"- **Statistik Klaim ({report.total_claims} Klaim)**:",
            f"  - Didukung Penuh (*Supported*): **{report.supported_count}** klaim",
            f"  - Bertentangan (*Contradicted*): **{report.contradicted_count}** klaim",
            f"  - Kurang Rujukan / Tidak Berdasar (*Unsupported*): **{report.unsupported_count}** klaim",
            f"  - Perlu Penambahan Sitasi (*Missing Citation*): **{report.missing_citation_count}** klaim",
            "",
            "---",
            "",
            "## 2. Tabel Rincian Verifikasi per Klaim Kalimat",
            "",
            "| No | Status Faktual | Status Sitasi | Klaim Kalimat Draf | Bukti Rujukan Korpus | Penjelasan / Tindakan |",
            "| :---: | :---: | :---: | :--- | :--- | :--- |",
        ]

        for idx, res in enumerate(report.results, start=1):
            status_icon = {
                "SUPPORTED": "🟢 Didukung",
                "CONTRADICTED": "🔴 Kontradiksi",
                "UNSUPPORTED": "❓ Tidak Berdasar",
            }.get(res.status, res.status)

            cite_icon = {
                "VALID": "✓ Valid",
                "MISSING": "⚠️ Belum Ada",
                "MISMATCH": "❌ Salah",
                "NOT_APPLICABLE": "-",
            }.get(res.citation_status, res.citation_status)

            evidence_desc = "-"
            if res.best_evidence:
                evidence_desc = f"`{res.best_evidence.file_path}:L{res.best_evidence.start_line}`"

            lines.append(
                f"| {idx} | {status_icon} | {cite_icon} | {res.claim.original_sentence[:80]}... | {evidence_desc} | {res.explanation[:90]}... |"
            )

        lines.extend([
            "",
            "---",
            "",
            "## 3. Teks Draf dengan Anotasi Koreksi Inline",
            "",
            "Berikut adalah draf tulisan yang telah dilengkapi catatan verifikasi inline untuk mempermudah perbaikan langsung:",
            "",
            "> " + report.annotated_draft,
            "",
            "---",
            "",
            "## 4. Rekomendasi Tindak Lanjut untuk Penulis",
            "",
            "1. **Perbaiki Kontradiksi Data Segera**: Klaim bertentangan berisiko langsung digugurkan penguji saat sidang karena ketidakakuratan data empiris BPS.",
            "2. **Lengkapi Nomor Sitasi Hilang**: Kalimat yang didukung korpus wajib disematkan penanda rujukan resmi IEEE `[X]`.",
            "3. **Hapus atau Perkuat Klaim Tanpa Dasar**: Jangan memasukkan generalisasi atau asumsi pribadi tanpa didasari dokumen resmi atau artikel ilmiah terakreditasi.",
            "",
        ])

        content = "\n".join(lines)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info("Saved verification Markdown report to %s", target)
        return target
