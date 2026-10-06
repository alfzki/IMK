#!/usr/bin/env python3
"""
scripts/publish_document.py
Perkakas Baris Perintah (CLI) untuk Memvalidasi dan Menerbitkan Naskah Markdown
menjadi Berkas Publikasi Standar IEEE (.docx dan .pdf) Politeknik Statistika STIS.
"""

import argparse
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from calm_carson.publisher import (
    DocumentPublisher,
    PublicationConfig,
    ValidationSeverity,
)


def print_banner():
    print("=" * 80)
    print("📄 CALM-CARSON: Document Publishing & Compilation Pipeline")
    print("   Politeknik Statistika STIS - Peminatan Sistem Informasi Statistik (SIS)")
    print("=" * 80)


def format_size(bytes_val: int) -> str:
    """Formats bytes into human-readable string."""
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024 * 1024:
        return f"{bytes_val / 1024:.1f} KB"
    else:
        return f"{bytes_val / (1024 * 1024):.1f} MB"


def main():
    parser = argparse.ArgumentParser(
        description="Kompilasi Naskah Markdown dan Bibliografi menjadi Berkas Publikasi IEEE (.docx & .pdf)"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path ke berkas naskah Markdown sumber (misal: drafts/topik_1/naskah_lengkap_skripsi.md)",
    )
    parser.add_argument(
        "--template", "-t",
        default="proposals/Template Proposal Penelitian.docx",
        help="Path ke berkas templat Microsoft Word (.docx) resmi atau kustom",
    )
    parser.add_argument(
        "--bib", "-b",
        default="literature/references.bib",
        help="Path ke berkas rujukan BibTeX (default: literature/references.bib)",
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="drafts/published",
        help="Direktori penyimpanan berkas publikasi (default: drafts/published)",
    )
    parser.add_argument(
        "--name", "-n",
        default=None,
        help="Nama dasar berkas luaran (default: mengikuti nama berkas naskah sumber)",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["docx", "pdf", "all"],
        default="all",
        help="Format dokumen luaran yang dihasilkan (default: all)",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Hanya jalankan validasi template dan sitasi tanpa mengompilasi berkas fisik",
    )
    parser.add_argument(
        "--auto-renumber",
        action="store_true",
        help="Otomatis urutkan dan beri nomor ulang sitasi teks secara kronologis (1..N)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Gagalkan proses dan kembalikan exit code 1 jika ditemukan kesalahan validasi kritis",
    )

    args = parser.parse_args()
    print_banner()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: Berkas naskah sumber tidak ditemukan: {args.input}")
        sys.exit(1)

    template_path = Path(args.template)
    if not template_path.exists():
        print(f"⚠️  Peringatan: Berkas templat tidak ditemukan: {args.template}. Menggunakan layout bawaan.")

    print(f"[*] Berkas Naskah   : {input_path}")
    print(f"[*] Berkas Templat  : {template_path}")
    print(f"[*] Berkas BibTeX   : {args.bib}")
    print(f"[*] Format Output   : {args.format.upper()}")
    print(f"[*] Direktori Target: {args.output_dir}")
    print("=" * 80)

    publisher = DocumentPublisher(
        template_path=str(template_path) if template_path.exists() else None,
        bib_path=args.bib,
    )

    # 1. Validasi Template
    print("\n🔍 [1/3] Memeriksa Kepatuhan Naskah terhadap Format Templat...")
    text_content = input_path.read_text(encoding="utf-8")
    has_ext_bib = Path(args.bib).exists() and Path(args.bib).stat().st_size > 0
    tpl_report = publisher.template_validator.validate(text_content, has_external_bib=has_ext_bib)

    status_icon = "🟢" if tpl_report.is_compliant else "🔴"
    print(f"{status_icon} Skor Kepatuhan Templat: {tpl_report.compliance_score:.1f}/100.0 (Status: {'PATUH' if tpl_report.is_compliant else 'PERLU PERBAIKAN'})")
    print(f"    - Kesalahan Kritis (Errors)  : {tpl_report.error_count}")
    print(f"    - Catatan Peringatan (Warns) : {tpl_report.warning_count}")

    if tpl_report.issues:
        print("\n    Rincian Temuan Struktur:")
        for idx, issue in enumerate(tpl_report.issues[:6], start=1):
            badge = "❌" if issue.severity == ValidationSeverity.ERROR else "⚠️"
            print(f"    {badge} [{issue.code}] {issue.message}")
            if issue.suggestion:
                print(f"       💡 Saran: {issue.suggestion}")
        if len(tpl_report.issues) > 6:
            print(f"       ... dan {len(tpl_report.issues) - 6} catatan lainnya.")

    # 2. Validasi Integritas Sitasi
    print("\n🔍 [2/3] Memeriksa Integritas dan Urutan Kunci Sitasi...")
    cit_report = publisher.citation_validator.validate(text_content, args.bib)

    cit_icon = "🟢" if cit_report.is_valid else "🔴"
    print(f"{cit_icon} Status Keutuhan Sitasi   : {'SAHIH' if cit_report.is_valid else 'TERDAPAT SITASI RUSAK'}")
    print(f"    - Total Sitasi di Teks       : {cit_report.total_in_text_citations} kemunculan ({cit_report.unique_in_text_citations} unik)")
    print(f"    - Entri Bibliografi Tersedia : {cit_report.total_bib_entries} rujukan")
    print(f"    - Sitasi Berhasil Dicocokkan : {len(cit_report.matched_citations)}")
    print(f"    - Sitasi Rusak/Hilang        : {len(cit_report.missing_citations)}")
    print(f"    - Rujukan Belum Dikutip      : {len(cit_report.orphan_references)}")

    if cit_report.missing_citations:
        print(f"\n    ❌ Sitasi Hilang Tanpa Rujukan: {', '.join(cit_report.missing_citations)}")
    if cit_report.out_of_order_citations:
        print(f"    ⚠️  Lompatan Urutan Sitasi IEEE : {len(cit_report.out_of_order_citations)} kali")

    if args.validate_only:
        print("\n" + "=" * 80)
        print("📋 MODE VALIDASI SELESAI (Tidak ada berkas yang diterbitkan).")
        print("=" * 80)
        if args.strict and (tpl_report.error_count > 0 or cit_report.error_count > 0):
            sys.exit(1)
        sys.exit(0)

    # Check strict mode before generating
    if args.strict:
        if tpl_report.error_count > 0 or cit_report.error_count > 0:
            print("\n❌ STRICT MODE: Penerbitan dihentikan karena terdeteksi kesalahan validasi kritis.")
            sys.exit(1)

    # 3. Kompilasi dan Penerbitan Dokumen
    print("\n🚀 [3/3] Mengompilasi Naskah Menjadi Format Dokumen Publikasi...")
    config = PublicationConfig(
        template_path=str(template_path) if template_path.exists() else None,
        output_format=args.format,
        auto_renumber_citations=args.auto_renumber,
        strict_validation=args.strict,
        output_dir=args.output_dir,
        base_filename=args.name,
    )

    result = publisher.publish_file(str(input_path), config)

    if not result.success:
        print(f"\n❌ Penerbitan Gagal: {result.error_message}")
        sys.exit(1)

    print("\n" + "=" * 80)
    print("🎉 PUBLIKASI BERHASIL DISUSUN!")
    print("=" * 80)

    if result.docx_path and Path(result.docx_path).exists():
        docx_file = Path(result.docx_path)
        size_str = format_size(docx_file.stat().st_size)
        print(f"[✓] Dokumen Word (.docx) : {docx_file.resolve()} ({size_str})")

    if result.pdf_path and Path(result.pdf_path).exists():
        pdf_file = Path(result.pdf_path)
        size_str = format_size(pdf_file.stat().st_size)
        print(f"[✓] Dokumen PDF (.pdf)   : {pdf_file.resolve()} ({size_str})")
    elif args.format in ("pdf", "all"):
        print("[⚠️] Konversi PDF dilewati (LibreOffice headless tidak tersedia atau gagal merender).")

    print(f"[✓] Metadata Laporan     : {Path(args.output_dir) / (input_path.stem + '_pub_report.json')}")
    print("=" * 80)


if __name__ == "__main__":
    main()
