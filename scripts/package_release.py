#!/usr/bin/env python3
"""
scripts/package_release.py
Skrip otomatis perakitan rilis GitHub (GitHub Release Packager)
Mengumpulkan seluruh perkakas, sub-agen, skills, pustaka, template, dan dokumentasi
menjadi arsip zip bersih siap distribusi untuk alur riset universal.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import zipfile
from pathlib import Path


def calculate_sha256(filepath: Path) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    version = "v0.1.0"
    pkg_name = f"agentic-research-workflow-{version}"
    dist_dir = repo_root / "dist"
    staging_dir = dist_dir / pkg_name
    zip_path = dist_dir / f"{pkg_name}.zip"
    downloads_dir = Path("/home/alfzki/Downloads")
    downloads_zip = downloads_dir / f"{pkg_name}.zip"

    print("=" * 80)
    print(f"📦 MERAKIT DISTRIBUSI GITHUB RELEASE: {pkg_name}")
    print("=" * 80)

    # 1. Bersihkan direktori dist sebelumnya
    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    if zip_path.exists():
        zip_path.unlink()
    staging_dir.mkdir(parents=True, exist_ok=True)

    # 2. Daftar file root yang wajib disertakan
    root_files = [
        "pyproject.toml",
        "uv.lock",
        ".python-version",
        ".gitignore",
        "LICENSE",
        "README.md",
        "ARCHITECTURE.md",
        "INSTRUCTIONS.md",
        "AGENTS.md",
        "QUICKSTART_UNIVERSAL.md",
        "RELEASE_NOTES.md",
    ]

    for rf in root_files:
        src = repo_root / rf
        if src.exists():
            shutil.copy2(src, staging_dir / rf)
            print(f"  [+] File root: {rf}")

    # 3. Salin .agents/skills/
    skills_src = repo_root / ".agents" / "skills"
    skills_dest = staging_dir / ".agents" / "skills"
    if skills_src.exists():
        shutil.copytree(skills_src, skills_dest)
        print(f"  [+] Skills terpasang: {len(list(skills_dest.iterdir()))} skills terdaftar")

    # 4. Salin src/calm_carson/ (abaikan __pycache__)
    src_dir = repo_root / "src"
    dest_src = staging_dir / "src"
    shutil.copytree(
        src_dir,
        dest_src,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )
    print("  [+] Core Engine: src/calm_carson/")

    # 5. Salin scripts/ (abaikan __pycache__ dan skrip spesifik lokal)
    scripts_src = repo_root / "scripts"
    scripts_dest = staging_dir / "scripts"
    shutil.copytree(
        scripts_src,
        scripts_dest,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "assemble_proposal_topik_1.py"),
    )
    print("  [+] CLI Scripts: scripts/ (11 tools + packager)")

    # 6. Salin docs/
    docs_src = repo_root / "docs"
    docs_dest = staging_dir / "docs"
    shutil.copytree(docs_src, docs_dest)
    print(f"  [+] Dokumentasi Teknis: docs/ ({len(list(docs_dest.iterdir()))} modul)")

    # 7. Salin tests/ (abaikan __pycache__)
    tests_src = repo_root / "tests"
    tests_dest = staging_dir / "tests"
    shutil.copytree(
        tests_src,
        tests_dest,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    print(f"  [+] Test Suite: tests/ ({len(list(tests_dest.glob('test_*.py')))} test files)")

    # 8. Siapkan template & folder kerja bersih
    # Proposals
    proposals_dest = staging_dir / "proposals"
    proposals_dest.mkdir(exist_ok=True)
    shutil.copy2(repo_root / "proposals" / "Template Proposal Penelitian.docx", proposals_dest)
    shutil.copy2(repo_root / "proposals" / "README.md", proposals_dest)
    print("  [+] Template Naskah: proposals/Template Proposal Penelitian.docx")

    # Literature (starter bersih)
    lit_dest = staging_dir / "literature"
    lit_dest.mkdir(exist_ok=True)
    (lit_dest / "pdfs").mkdir(exist_ok=True)
    (lit_dest / "markdowns").mkdir(exist_ok=True)
    (lit_dest / "pdfs" / ".gitkeep").touch()
    (lit_dest / "markdowns" / ".gitkeep").touch()
    shutil.copy2(repo_root / "literature" / "references.bib", lit_dest)

    # Buat literature/README.md yang bersih
    with open(lit_dest / "README.md", "w") as f:
        f.write(
            "# Literature Corpus Directory\n\n"
            "Direktori ini digunakan untuk menyimpan bahan literatur riset:\n"
            "- `pdfs/`: Letakkan berkas PDF jurnal/prosiding di sini.\n"
            "- `markdowns/`: Berkas Markdown hasil konversi dari PDF via `scripts/convert_pdf_to_md.py`.\n"
            "- `references.bib`: Berkas master sitasi BibTeX terpadu.\n"
        )
    print("  [+] Direktori Literatur: literature/ (bersih + template references.bib)")

    # Brainstorming (starter bersih)
    brainstorm_dest = staging_dir / "brainstorming"
    brainstorm_dest.mkdir(exist_ok=True)
    shutil.copy2(repo_root / "brainstorming" / "01_research_profile.md", brainstorm_dest)
    with open(brainstorm_dest / "README.md", "w") as f:
        f.write(
            "# Brainstorming & Research Exploration\n\n"
            "Gunakan direktori ini untuk eksplorasi topik dan pemetaan minat riset:\n"
            "- `01_research_profile.md`: Template kuesioner profil riset peneliti.\n"
        )
    print("  [+] Direktori Brainstorming: brainstorming/ (universal profile template)")

    # Drafts (starter bersih)
    drafts_dest = staging_dir / "drafts"
    drafts_dest.mkdir(exist_ok=True)
    (drafts_dest / "published").mkdir(exist_ok=True)
    (drafts_dest / "published" / ".gitkeep").touch()
    with open(drafts_dest / "README.md", "w") as f:
        f.write(
            "# Drafts & Output Directory\n\n"
            "Direktori ini digunakan untuk menyimpan draf naskah yang disusun bab demi bab:\n"
            "- Draf kerja akan dihasilkan oleh `scripts/orchestrate_drafting.py`.\n"
            "- Hasil penerbitan (.docx dan .pdf) akan disimpan di `published/`.\n"
        )
    print("  [+] Direktori Drafts: drafts/ (bersih)")

    # 9. Buat berkas zip rilis
    print("\n[*] Mengompresi seluruh berkas ke dalam arsip zip...")
    total_files = 0
    total_uncompressed_bytes = 0

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(staging_dir):
            for file in files:
                abs_file = Path(root) / file
                rel_path = abs_file.relative_to(staging_dir.parent)
                zf.write(abs_file, rel_path)
                total_files += 1
                total_uncompressed_bytes += abs_file.stat().st_size

    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    sha256_hash = calculate_sha256(zip_path)

    # 10. Salin ke direktori Downloads pengguna jika tersedia
    if downloads_dir.exists():
        shutil.copy2(zip_path, downloads_zip)
        print(f"  [✓] Salinan otomatis disimpan ke Downloads: {downloads_zip}")

    print("\n" + "=" * 80)
    print("🎉 GITHUB RELEASE BUNDLE BERHASIL DIBUAT!")
    print("=" * 80)
    print(f"Nama Berkas    : {zip_path.name}")
    print(f"Lokasi Dist    : {zip_path}")
    print(f"Ukuran Arsip   : {zip_size_mb:.2f} MB ({zip_path.stat().st_size:,} bytes)")
    print(f"Jumlah Berkas  : {total_files} berkas")
    print(f"Ukuran Mentah  : {total_uncompressed_bytes / (1024*1024):.2f} MB")
    print(f"SHA-256 Hash   : {sha256_hash}")
    print("=" * 80)

    # Catat ke berkas checksum
    checksum_file = dist_dir / f"{pkg_name}.sha256"
    with open(checksum_file, "w") as f:
        f.write(f"{sha256_hash}  {zip_path.name}\n")
    print(f"Checksum file  : {checksum_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
