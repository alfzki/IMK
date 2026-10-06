#!/usr/bin/env python3
"""
SIMPus STIS Theses Scraper
Scrapes skripsi metadata (title, author, NIM, abstract, supervisor, keywords) 
from https://simpus.stis.ac.id/koleksi and provides on-demand encrypted PDF downloading.
"""

import argparse
import csv
import glob
import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import time
from datetime import datetime
from typing import Dict, List, Optional

# Auto-reexec into project .venv if run with system python
try:
    import requests
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from tqdm import tqdm
except ImportError:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    venv_python = os.path.join(project_root, ".venv", "bin", "python")
    if os.path.exists(venv_python) and sys.executable != venv_python:
        os.execv(venv_python, [venv_python] + sys.argv)
    uv_bin = shutil.which("uv")
    if uv_bin:
        os.execv(uv_bin, ["uv", "run", "python"] + sys.argv)
    print("Error: Missing required packages (requests, cryptography, tqdm).")
    print("Please run using: uv run python " + " ".join(sys.argv))
    sys.exit(1)


# Ensure scripts directory is in sys.path for internal modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_API_URL = "https://api-simpus.stis.ac.id"
KLASIFIKASI_MAP = {
    263: "Sistem Informasi",
    264: "Sains Data",
    300: "Komputasi Statistik",
}
SECRET_SALT_1 = "MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAt2dCskTnNf7Fz+5sbj9rbJQrej+h"
SECRET_SALT_2 = "MIIJrTBXBgkqhkiG9w0BBQ0wSjApBgkqhkiG9w0BBQwwHAQIp49kwfeaRJkCAggAMAwGCCq"


def trigger_md_conversion(pdf_path: str, output_base_dir: str = "literature/markdowns"):
    """Converts a downloaded PDF to Markdown using convert_pdf_to_md module (Marker GPU)."""
    try:
        from convert_pdf_to_md import convert_pdf_to_markdown
        print(f"        [*] Mengonversi PDF ke Markdown via Marker (GPU RTX 4050)...")
        md_file = convert_pdf_to_markdown(pdf_path, output_base_dir=output_base_dir)
        if md_file:
            print(f"        [+] Markdown tersimpan: {md_file}")
    except Exception as e:
        print(f"        [!] Konversi Markdown dilewati: {e}")



def get_firefox_token() -> Optional[str]:
    """Find and extract the access_token JWT from local Firefox cookies.sqlite."""
    search_patterns = [
        os.path.expanduser("~/.config/mozilla/firefox/*/cookies.sqlite"),
        os.path.expanduser("~/.mozilla/firefox/*/cookies.sqlite"),
        os.path.expanduser("~/.var/app/org.mozilla.firefox/.mozilla/firefox/*/cookies.sqlite"),
    ]

    cookie_files = []
    for pat in search_patterns:
        cookie_files.extend(glob.glob(pat))

    for db_path in cookie_files:
        if not os.path.exists(db_path):
            continue
        try:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp_path = tmp.name
            shutil.copyfile(db_path, tmp_path)
            conn = sqlite3.connect(tmp_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT value FROM moz_cookies WHERE host LIKE '%api-simpus.stis.ac.id%' AND name = 'access_token'"
            )
            row = cursor.fetchone()
            conn.close()
            os.unlink(tmp_path)
            if row and row[0]:
                return row[0]
        except Exception:
            continue
    return None


def decrypt_vb(t: str, i: str) -> str:
    """Decrypts session key token (AES-256-CBC) used by SIMPus frontend."""
    r, n = t.split(":")
    iv = bytes.fromhex(r)
    ciphertext = bytes.fromhex(n)
    key = hashlib.sha256(i.encode("utf-8")).digest()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode("utf-8")


def decrypt_vo(ciphertext: bytes, i: str, r: str) -> bytes:
    """Decrypts the actual binary PDF stream (AES-256-CBC)."""
    key = hashlib.sha256(i.encode("utf-8")).digest()
    iv = bytes.fromhex(r)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    try:
        data = unpadder.update(padded_data) + unpadder.finalize()
    except Exception:
        data = padded_data
    return data


def download_and_decrypt_pdf(token: str, thesis_id: str, output_path: str) -> bool:
    """Fetches encrypted PDF stream from SIMPus API and decrypts it into a valid PDF file."""
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)",
        "Authorization": f"Bearer {token}",
    }
    url = f"{BASE_API_URL}/v2/koleksi/{thesis_id}/read"
    try:
        resp = requests.get(url, headers=headers, timeout=60)
        if resp.status_code != 200:
            print(f"[-] Gagal mengunduh PDF untuk {thesis_id}: Status {resp.status_code}")
            return False

        r = resp.headers.get("X-SBO-Random-Key")
        n = resp.headers.get("X-SBO-IV")
        if not r or not n:
            print(f"[-] Header enkripsi tidak ditemukan pada response {thesis_id}")
            return False

        a = decrypt_vb(r, SECRET_SALT_1)
        a = decrypt_vb(a, SECRET_SALT_2)
        pdf_bytes = decrypt_vo(resp.content, a, n)

        if not pdf_bytes.startswith(b"%PDF-"):
            print(f"[-] Header PDF tidak valid setelah didekripsi untuk {thesis_id}")
            return False

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

        return True
    except Exception as e:
        print(f"[-] Terjadi kesalahan saat mendownload PDF {thesis_id}: {e}")
        return False


def fetch_theses_list(
    token: str,
    min_year: int,
    max_year: int,
    klasifikasi_ids: List[int],
    limit: Optional[int] = None,
) -> List[Dict]:
    """Fetches paginated list of theses matching criteria."""
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)",
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    filters = [
        {"id": "klasifikasiId", "value": klasifikasi_ids},
        {
            "id": "tahunTerbit",
            "value": [f"{min_year}-01-01T00:00:00Z", f"{max_year}-12-31T23:59:59Z"],
        },
    ]
    sorting = [{"id": "createdAt", "desc": True}]

    items = []
    page_size = 50
    start = 0

    print(f"[*] Mengambil daftar skripsi dari SIMPus (Rentang {min_year}-{max_year})...")

    while True:
        params = {
            "start": str(start),
            "size": str(page_size),
            "jenis-pustaka": "Skripsi",
            "filters": json.dumps(filters),
            "sorting": json.dumps(sorting),
        }
        url = f"{BASE_API_URL}/v2/koleksi"
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        if resp.status_code != 200:
            print(f"[-] Gagal mengambil data halaman (start={start}): HTTP {resp.status_code}")
            break

        data = resp.json()
        total_count = data.get("count", 0)
        rows = data.get("rows", [])
        if not rows:
            break

        items.extend(rows)
        print(f"    -> Terambil {len(items)} dari total {total_count} skripsi...")

        if limit and len(items) >= limit:
            items = items[:limit]
            break

        start += len(rows)
        if start >= total_count:
            break

        time.sleep(0.3)

    return items


def fetch_thesis_detail(token: str, item_id: str) -> Optional[Dict]:
    """Fetches full metadata for a specific thesis (abstract, supervisor, keywords, etc.)."""
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)",
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    url = f"{BASE_API_URL}/v2/koleksi/{item_id}"
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"[-] Gagal mengambil detail {item_id}: {e}")
    return None


def clean_text(text: Optional[str]) -> str:
    """Normalize and strip whitespace in strings."""
    if not text:
        return ""
    text = text.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def sanitize_filename(title: str, max_len: int = 80) -> str:
    """Clean filename for saving PDFs."""
    clean = re.sub(r'[\\/*?:"<>|]', "", title)
    clean = re.sub(r"\s+", "_", clean).strip("_")
    return clean[:max_len]


def generate_markdown_summary(theses: List[Dict], md_path: str):
    """Generates an academic literature benchmarking document in Markdown."""
    total = len(theses)
    by_peminatan = {}
    by_year = {}
    for t in theses:
        p = t.get("peminatan", "Lainnya")
        y = t.get("tahun", "Unknown")
        by_peminatan[p] = by_peminatan.get(p, 0) + 1
        by_year[y] = by_year.get(y, 0) + 1

    lines = []
    lines.append("# Rekapitulasi & Benchmarking Skripsi Alumni STIS (2021–2026)\n")
    lines.append(f"*Total Skripsi Terekam*: **{total} judul** (Sumber: SIMPus Politeknik Statistika STIS)\n")
    lines.append("## 1. Distribusi Peminatan & Tahun Terbit\n")
    lines.append("| Peminatan / Jurusan | Jumlah Skripsi | Persentase |")
    lines.append("|---|---|---|")
    for p, c in sorted(by_peminatan.items(), key=lambda x: x[1], reverse=True):
        pct = (c / total) * 100 if total else 0
        lines.append(f"| **{p}** | {c} | {pct:.1f}% |")

    lines.append("\n| Tahun Terbit | Jumlah Skripsi |")
    lines.append("|---|---|")
    for y, c in sorted(by_year.items(), key=lambda x: str(x[0]), reverse=True):
        lines.append(f"| {y} | {c} |")

    lines.append("\n---\n")
    lines.append("## 2. Taksonomi Tematik Skripsi Peminatan Sistem Informasi Statistik\n")
    lines.append("Berdasarkan telaah terhadap judul dan abstrak, tema skripsi Sistem Informasi dan Komputasi Statistik terbagi ke dalam beberapa pilar utama:\n")

    clusters = {
        "1. Pengumpulan Data Cerdas, CAPI/CAWI & Validasi Survei": ["capi", "cawi", "kuesioner", "validasi", "survei", "entri", "monitoring survei"],
        "2. WebGIS, Sistem Spasial & Pemetaan Statistik": ["gis", "webgis", "spasial", "pemetaan", "geospasial", "wilayah", "citra"],
        "3. Tata Kelola Data, Satu Data Indonesia (SDI) & Interoperabilitas/SPBE": ["satu data", "sdi", "interoperabilitas", "metadata", "api", "pipeline", "etl", "integrasi", "spbe"],
        "4. Visualisasi Data, Dashboard Analitik & Diseminasi Statistik": ["dashboard", "visualisasi", "diseminasi", "portal", "grafik", "indikator"],
        "5. Keamanan Sistem, Privasi Data & SDC (Statistical Disclosure Control)": ["privasi", "privacy", "disclosure", "keamanan", "audit", "enkripsi", "anonimitas"],
    }

    for cluster_name, keywords in clusters.items():
        matched = []
        for t in theses:
            text = (t.get("judul", "") + " " + t.get("abstrak", "") + " " + t.get("kata_kunci", "")).lower()
            if any(kw in text for kw in keywords):
                matched.append(t)

        lines.append(f"### {cluster_name} ({len(matched)} Skripsi)\n")
        lines.append("| Tahun | Judul Skripsi | Penulis | Peminatan | Pembimbing | Link SIMPus |")
        lines.append("|---|---|---|---|---|---|")
        matched.sort(key=lambda x: (x.get("tahun", ""), x.get("jumlah_dibaca", 0)), reverse=True)
        for m in matched[:15]:
            judul = m.get("judul", "").replace("|", "-")
            penulis = m.get("penulis", "").replace("|", "-")
            pemb = m.get("pembimbing", "-") or "-"
            pemb = pemb.replace("|", "-")
            peminatan = m.get("peminatan", "")
            y = m.get("tahun", "")
            url = m.get("url_simpus", "#")
            lines.append(f"| {y} | **{judul}** | {penulis} | {peminatan} | {pemb} | [Buka di SIMPus]({url}) |")
        lines.append("\n")

    lines.append("---\n")
    lines.append("## 3. Daftar Lengkap Skripsi Berdasarkan Peminatan\n")
    for pem in ["Sistem Informasi", "Komputasi Statistik", "Sains Data"]:
        sub_list = [t for t in theses if t.get("peminatan") == pem]
        lines.append(f"### {pem} ({len(sub_list)} Judul)\n")
        lines.append("| No | Tahun | Judul Skripsi | Penulis | Dosen Pembimbing | Kata Kunci |")
        lines.append("|---|---|---|---|---|---|")
        sub_list.sort(key=lambda x: (x.get("tahun", ""), x.get("judul", "")), reverse=True)
        for i, item in enumerate(sub_list, 1):
            j = item.get("judul", "").replace("|", "-")
            pen = item.get("penulis", "").replace("|", "-")
            pem_name = (item.get("pembimbing") or "-").replace("|", "-")
            kw = (item.get("kata_kunci") or "-").replace("|", "-")
            y = item.get("tahun", "")
            url = item.get("url_simpus", "")
            lines.append(f"| {i} | {y} | [{j}]({url}) | {pen} | {pem_name} | {kw} |")
        lines.append("\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))



def main():
    parser = argparse.ArgumentParser(description="Scraper Skripsi SIMPus Politeknik Statistika STIS")
    parser.add_argument("--min-year", type=int, default=2021, help="Tahun terbit minimal (default: 2021)")
    parser.add_argument("--max-year", type=int, default=2026, help="Tahun terbit maksimal (default: 2026)")
    parser.add_argument("--limit", type=int, default=None, help="Batas jumlah data yang diambil (untuk testing)")
    parser.add_argument("--token", type=str, default=None, help="Manual JWT access_token")
    parser.add_argument("--output-dir", type=str, default="literature", help="Direktori penyimpanan data (default: literature)")
    parser.add_argument("--download-pdf", action="store_true", help="Download seluruh file PDF skripsi yang discrap")
    parser.add_argument("--pdf-id", type=str, default=None, help="Download PDF on-demand untuk 1 ID skripsi spesifik")
    parser.add_argument("--pdf-query", type=str, default=None, help="Download PDF on-demand untuk judul yang mengandung kata kunci tertentu")
    parser.add_argument("--no-convert-md", action="store_true", help="Jangan otomatis mengonversi PDF terunduh ke Markdown")
    parser.add_argument("--check-auth", action="store_true", help="Cek status token autentikasi")
    parser.add_argument("--download-year", type=int, default=None, help="Download seluruh PDF skripsi untuk tahun tertentu dari database lokal")
    parser.add_argument("--peminatan", type=str, default=None, help="Filter peminatan saat download (misal: 'Sistem Informasi', 'Sains Data')")

    args = parser.parse_args()

    token = args.token or os.environ.get("SIMPUS_TOKEN") or get_firefox_token()
    if not token:
        print("[-] Gagal mendapatkan token! Pastikan Firefox telah login ke SIMPus STIS atau masukkan via --token")
        sys.exit(1)

    if args.check_auth:
        print("[+] Token ditemukan:", token[:20] + "...")
        sys.exit(0)

    if args.pdf_id:
        print(f"[*] Mengunduh PDF on-demand untuk ID: {args.pdf_id}")
        det = fetch_thesis_detail(token, args.pdf_id)
        title = det.get("judul", args.pdf_id) if det else args.pdf_id
        year = (det.get("tahunTerbit") or "unknown")[:4] if det else "unknown"
        filename = f"{year}_{sanitize_filename(title)}.pdf"
        out_path = os.path.join(args.output_dir, "pdfs", filename)
        ok = download_and_decrypt_pdf(token, args.pdf_id, out_path)
        if ok:
            print(f"[+] Berhasil disimpan: {out_path}")
            if not args.no_convert_md:
                trigger_md_conversion(out_path, os.path.join(args.output_dir, "markdowns"))
        sys.exit(0 if ok else 1)

    if args.pdf_query:
        json_path = os.path.join(args.output_dir, "theses_data.json")
        if not os.path.exists(json_path):
            print(f"[-] File {json_path} tidak ditemukan. Jalankan scraping metadata terlebih dahulu!")
            sys.exit(1)
        with open(json_path, "r", encoding="utf-8") as f:
            theses = json.load(f)

        query = args.pdf_query.lower()
        matched = [
            t for t in theses 
            if query in t.get("judul", "").lower() 
            or query in t.get("abstrak", "").lower() 
            or query in t.get("kata_kunci", "").lower()
        ]
        print(f"[*] Ditemukan {len(matched)} skripsi dengan kata kunci '{args.pdf_query}':")
        for item in matched:
            title = item.get("judul", "")
            year = item.get("tahun", "")
            item_id = item.get("id")
            filename = f"{year}_{sanitize_filename(title)}.pdf"
            out_path = os.path.join(args.output_dir, "pdfs", filename)
            if os.path.exists(out_path):
                print(f"    [=] Sudah ada: {filename}")
                if not args.no_convert_md:
                    trigger_md_conversion(out_path, os.path.join(args.output_dir, "markdowns"))
                continue
            print(f"    [*] Mendownload: {title[:70]}...")
            ok = download_and_decrypt_pdf(token, item_id, out_path)
            if ok:
                print(f"        [+] Sukses: {filename}")
                if not args.no_convert_md:
                    trigger_md_conversion(out_path, os.path.join(args.output_dir, "markdowns"))
            time.sleep(1)
        sys.exit(0)

    if args.download_year:
        json_path = os.path.join(args.output_dir, "theses_data.json")
        if not os.path.exists(json_path):
            print(f"[-] File {json_path} tidak ditemukan. Jalankan scraping metadata terlebih dahulu!")
            sys.exit(1)
        with open(json_path, "r", encoding="utf-8") as f:
            theses = json.load(f)

        target_year = str(args.download_year)
        matched = [t for t in theses if str(t.get("tahun")) == target_year and t.get("is_dapat_dibaca")]
        if args.peminatan:
            pem_filter = args.peminatan.lower()
            matched = [t for t in matched if pem_filter in str(t.get("peminatan", "")).lower()]

        print(f"[*] Ditemukan {len(matched)} skripsi tahun {target_year}" + (f" (peminatan: {args.peminatan})" if args.peminatan else "") + " untuk diunduh:")
        success_count = 0
        skipped_count = 0
        failed_count = 0

        for idx, item in enumerate(matched, 1):
            title = item.get("judul", "")
            year = item.get("tahun", "")
            item_id = item.get("id")
            filename = f"{year}_{sanitize_filename(title)}.pdf"
            out_path = os.path.join(args.output_dir, "pdfs", filename)

            if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
                print(f"[{idx}/{len(matched)}] [=] Sudah ada: {filename[:70]}...")
                skipped_count += 1
                if not args.no_convert_md:
                    trigger_md_conversion(out_path, os.path.join(args.output_dir, "markdowns"))
                continue

            print(f"[{idx}/{len(matched)}] [*] Mendownload ({item.get('peminatan', '')}): {title[:65]}...")
            ok = download_and_decrypt_pdf(token, item_id, out_path)
            if ok:
                success_count += 1
                print(f"    [+] Sukses: {filename[:70]}...")
                if not args.no_convert_md:
                    trigger_md_conversion(out_path, os.path.join(args.output_dir, "markdowns"))
            else:
                failed_count += 1
            time.sleep(0.3)

        print(f"\n[+] Selesai! Berhasil diunduh: {success_count}, Sudah ada: {skipped_count}, Gagal: {failed_count}")
        sys.exit(0)

    klasifikasi_ids = list(KLASIFIKASI_MAP.keys())
    theses_summary_list = fetch_theses_list(
        token=token,
        min_year=args.min_year,
        max_year=args.max_year,
        klasifikasi_ids=klasifikasi_ids,
        limit=args.limit,
    )

    print(f"[+] Berhasil mengambil daftar dasar {len(theses_summary_list)} skripsi.")
    print("[*] Memulai pengambilan detail (abstrak, dosen pembimbing, kata kunci)...")

    os.makedirs(args.output_dir, exist_ok=True)
    json_path = os.path.join(args.output_dir, "theses_data.json")
    existing_records = {}
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                for item in json.load(f):
                    existing_records[item["id"]] = item
            print(f"[i] Terdeteksi cache sebelumnya dengan {len(existing_records)} skripsi.")
        except Exception:
            pass

    enriched_data = []
    for item in tqdm(theses_summary_list, desc="Enriching metadata"):
        item_id = item["id"]
        if item_id in existing_records and existing_records[item_id].get("abstrak"):
            enriched_data.append(existing_records[item_id])
            continue

        det = fetch_thesis_detail(token, item_id)
        if not det:
            det = item

        info_tambahan = det.get("infoTambahan") or {}
        year_val = det.get("tahunTerbit") or ""
        year_str = year_val[:4] if len(year_val) >= 4 else ""

        record = {
            "id": item_id,
            "no_induk": clean_text(det.get("noInduk")),
            "judul": clean_text(det.get("judul")),
            "penulis": clean_text(det.get("penulis")),
            "tahun": year_str,
            "tahun_terbit_raw": year_val,
            "klasifikasi_id": det.get("klasifikasiId"),
            "peminatan": KLASIFIKASI_MAP.get(det.get("klasifikasiId"), det.get("klasifikasi", "Lainnya")),
            "pembimbing": clean_text(info_tambahan.get("pembimbing")),
            "abstrak": clean_text(info_tambahan.get("abstrak")),
            "kata_kunci": clean_text(info_tambahan.get("keyword")),
            "jumlah_dibaca": det.get("jumlahDibaca", 0),
            "jumlah_disimpan": det.get("jumlahDisimpan", 0),
            "is_dapat_dibaca": det.get("isDapatDibaca", False),
            "url_simpus": f"https://simpus.stis.ac.id/koleksi/{item_id}",
            "created_at": det.get("createdAt"),
        }
        enriched_data.append(record)

        if args.download_pdf and record["is_dapat_dibaca"]:
            pdf_name = f"{record['tahun']}_{sanitize_filename(record['judul'])}.pdf"
            pdf_path = os.path.join(args.output_dir, "pdfs", pdf_name)
            if not os.path.exists(pdf_path):
                ok = download_and_decrypt_pdf(token, item_id, pdf_path)
                if ok and not args.no_convert_md:
                    trigger_md_conversion(pdf_path, os.path.join(args.output_dir, "markdowns"))

        time.sleep(0.12)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(enriched_data, f, ensure_ascii=False, indent=2)
    print(f"\n[+] Data berhasil disimpan ke JSON: {json_path}")


    csv_path = os.path.join(args.output_dir, "theses_data.csv")
    if enriched_data:
        fieldnames = list(enriched_data[0].keys())
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(enriched_data)
    print(f"[+] Data berhasil disimpan ke CSV: {csv_path}")


    md_path = os.path.join(args.output_dir, "previous_theses.md")
    generate_markdown_summary(enriched_data, md_path)
    print(f"[+] Ringkasan analisis skripsi disimpan ke: {md_path}")


if __name__ == "__main__":
    main()
