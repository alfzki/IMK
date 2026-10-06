#!/usr/bin/env python3
"""
CLI Runner for AI Writing Style Audit (Wikipedia:Signs_of_AI_writing).
Memeriksa tanda-tanda gaya penulisan AI, klise kosakata dwibahasa, kesimpulan formulaik,
penggunaan tanda pisah (em dash) yang tidak sesuai kaidah, serta kebocoran artefak LLM pada draf skripsi STIS.
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

from calm_carson.style import AIStyleChecker, StyleExporter


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit tanda-tanda gaya penulisan AI dan kebocoran artefak LLM berdasarkan Wikipedia:Signs_of_AI_writing."
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        help="Path ke berkas draf Markdown (.md) atau teks yang ingin diaudit.",
    )
    parser.add_argument(
        "--text",
        "-t",
        type=str,
        help="Teks kutipan draf kalimat atau paragraf yang ingin diaudit langsung.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Mode ketat: keluar dengan exit code 1 jika ditemukan pelanggaran FATAL/HIGH atau skor risiko AI >= 35.",
    )
    parser.add_argument(
        "--annotated-only",
        action="store_true",
        help="Tampilkan hanya draf teks dengan penanda anotasi perbaikan inline.",
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Simpan laporan audit ke berkas Markdown dan JSON di folder drafts/style_reports/.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Tampilkan hasil audit dalam format JSON mentah ke stdout.",
    )

    args = parser.parse_args()

    draft_text = ""
    source_id = "input_text"

    if args.file:
        fpath = Path(args.file)
        if not fpath.exists():
            print(f"❌ Berkas tidak ditemukan: {fpath}", file=sys.stderr)
            sys.exit(1)
        draft_text = fpath.read_text(encoding="utf-8", errors="ignore")
        source_id = str(fpath)
    elif args.text:
        draft_text = args.text.strip()
        source_id = "cli_arg_text"
    else:
        print("Silakan masukkan teks draf paragraf yang ingin diaudit (akhiri dengan Ctrl+D / EOF):")
        try:
            draft_text = sys.stdin.read().strip()
            source_id = "stdin_text"
        except (KeyboardInterrupt, EOFError):
            print("\nOperasi dibatalkan.")
            sys.exit(0)

    if not draft_text:
        print("❌ Teks draf tidak boleh kosong.", file=sys.stderr)
        sys.exit(1)

    # Jalankan audit
    checker = AIStyleChecker()
    report = checker.check_text(draft_text, source_id=source_id)

    # Keluaran format JSON jika diminta
    if args.json:
        import json
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
        if args.strict and not report.is_acceptable(strict=True):
            sys.exit(1)
        sys.exit(0)

    # Mode annotated-only
    if args.annotated_only:
        print(report.annotated_text)
        if args.strict and not report.is_acceptable(strict=True):
            sys.exit(1)
        sys.exit(0)

    # Render laporan terminal
    rendered_output = StyleExporter.render_terminal(report, show_annotated=True, suggest_fixes=True)
    print(rendered_output)

    # Ekspor berkas jika diminta
    if args.export:
        report_dir = WORKSPACE_ROOT / "drafts" / "style_reports"
        stem = Path(source_id).stem if args.file else "style_audit_report"
        md_file = report_dir / f"{stem}_style_report.md"
        json_file = report_dir / f"{stem}_style_report.json"

        StyleExporter.export_markdown(report, md_file)
        StyleExporter.export_json(report, json_file)

        print(f"\n💾 Laporan audit berhasil disimpan:")
        print(f"   - Markdown: {md_file}")
        print(f"   - JSON    : {json_file}")

    # Penentuan exit code pada mode strict
    if args.strict and not report.is_acceptable(strict=True):
        print("\n\033[91m❌ [STRICT MODE] Audit gagal: Terdeteksi pelanggaran gaya bahasa AI yang memerlukan revisi.\033[0m")
        sys.exit(1)


if __name__ == "__main__":
    main()
