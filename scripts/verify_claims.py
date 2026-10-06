#!/usr/bin/env python3
"""
CLI Runner for Factual Claim & Citation Verification.
Memeriksa keabsahan faktual, konsistensi data kuantitatif, dan validitas sitasi draf proposal terhadap korpus lokal.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Auto-bootstrap local .venv if run with system python
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
VENV_PYTHON = WORKSPACE_ROOT / ".venv" / "bin" / "python"
SRC_PATH = WORKSPACE_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

if VENV_PYTHON.exists() and sys.executable != str(VENV_PYTHON):
    if not os.environ.get("CALM_CARSON_BOOTSTRAPPED"):
        os.environ["CALM_CARSON_BOOTSTRAPPED"] = "1"
        os.environ["PYTHONPATH"] = f"{SRC_PATH}:{os.environ.get('PYTHONPATH', '')}"
        os.execv(str(VENV_PYTHON), [str(VENV_PYTHON)] + sys.argv)

from calm_carson.verify import (
    ClaimDecomposer,
    DraftAnnotator,
    EvidenceMatcher,
    FactVerifier,
    VerificationExporter,
    verify_draft_text,
)


def print_banner() -> None:
    print("=" * 80)
    print("🛡️  CALM-CARSON: Factual Claim & Citation Integrity Verifier")
    print("   Politeknik Statistika STIS - Peminatan Sistem Informasi Statistik (SIS)")
    print("=" * 80)


def display_report(report) -> None:
    verdict_colors = {
        "READY_FOR_SUBMISSION": "\033[92m🟢 LOLOS VERIFIKASI (SIAP DIAJUKAN)\033[0m",
        "NEEDS_MINOR_CITATION": "\033[93m🟡 PERLU PERBAIKAN SITASI MINOR\033[0m",
        "FATAL_CONTRADICTIONS": "\033[91m🔴 TERDAPAT KONTRADIKSI FAKTUAL / PERLU REVISI\033[0m",
    }
    badge = verdict_colors.get(report.overall_verdict, report.overall_verdict)

    print(f"\n📋 STATUS KELAYAKAN DRAF TULISAN:")
    print("-" * 80)
    print(f"Status Audit       : {badge}")
    print(f"Total Klaim Kalimat: {report.total_claims} Klaim")
    print(f"Distribusi Status  : {report.supported_count} Didukung | {report.contradicted_count} Kontradiksi | {report.unsupported_count} Tidak Berdasar")
    print(f"Perlu Nomor Sitasi : {report.missing_citation_count} Klaim")
    print(f"\nRingkasan Audit    :\n> {report.verdict_summary}")
    print("-" * 80)

    print("\n🔍 TABEL AUDIT DETAIL PER KLAIM:")
    print("-" * 80)
    print(f"{'No':<3} | {'Status':<12} | {'Sitasi':<8} | {'Klaim Draf':<32} | {'Bukti Korpus'}")
    print("-" * 80)

    for idx, r in enumerate(report.results, start=1):
        status_tag = {
            "SUPPORTED": "🟢 Didukung",
            "CONTRADICTED": "🔴 Kontradiksi",
            "UNSUPPORTED": "❓ Tdk Berdasar",
        }.get(r.status, r.status)

        cite_tag = {
            "VALID": "✓ Valid",
            "MISSING": "⚠️ Kurang",
            "MISMATCH": "❌ Salah",
            "DISALLOWED_THESIS": "🚫 Dilarang",
            "NOT_APPLICABLE": "-",
        }.get(r.citation_status, r.citation_status)

        claim_trunc = r.claim.claim_text[:30] + "..." if len(r.claim.claim_text) > 30 else r.claim.claim_text
        evidence_loc = f"{r.best_evidence.file_path.split('/')[-1]}:L{r.best_evidence.start_line}" if r.best_evidence else "Tidak ditemukan"

        print(f"{idx:<3} | {status_tag:<12} | {cite_tag:<8} | {claim_trunc:<32} | {evidence_loc}")

    print("-" * 80)
    print("\n📝 DRAF TEKS DENGAN ANOTASI KOREKSI INLINE:")
    print("-" * 80)
    print(report.annotated_draft)
    print("-" * 80)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit keabsahan faktual, konsistensi data kuantitatif, dan validitas sitasi draf skripsi."
    )
    parser.add_argument(
        "--text",
        "-t",
        type=str,
        help="Teks draf paragraf atau kalimat yang ingin diverifikasi keabsahannya",
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        help="Path ke berkas Markdown atau teks yang memuat draf proposal",
    )
    parser.add_argument(
        "--annotated-only",
        action="store_true",
        help="Tampilkan hanya draf teks dengan penanda anotasi inline",
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Ekspor laporan audit ke format JSON dan Markdown",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Keluar dengan exit code 1 jika terdapat kontradiksi data faktual",
    )

    args = parser.parse_args()
    print_banner()

    draft_text = ""
    if args.text:
        draft_text = args.text.strip()
    elif args.file:
        fpath = Path(args.file)
        if not fpath.exists():
            print(f"❌ Berkas tidak ditemukan: {fpath}")
            sys.exit(1)
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            draft_text = f.read().strip()
    else:
        print("\nSilakan masukkan teks draf paragraf yang ingin diaudit:")
        try:
            draft_text = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nOperasi dibatalkan.")
            sys.exit(0)

    if not draft_text:
        print("❌ Teks draf tidak boleh kosong.")
        sys.exit(1)

    print(f"\n[*] Membedah draf teks menjadi klaim-klaim individual...")
    report = verify_draft_text(
        draft_text=draft_text,
        workspace_root=WORKSPACE_ROOT,
        export_files=args.export,
    )

    if args.annotated_only:
        print("\n" + report.annotated_draft + "\n")
    else:
        display_report(report)

    if args.export:
        print("\n[✓] Laporan JSON     : literature/fact_check_*.json")
        print("[✓] Laporan Markdown : brainstorming/laporan_verifikasi_*.md")

    if args.strict and report.contradicted_count > 0:
        print("\n❌ GAGAL: Terdeteksi kontradiksi data empiris terhadap korpus.")
        sys.exit(1)


if __name__ == "__main__":
    main()
