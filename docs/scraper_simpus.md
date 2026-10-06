# Dokumentasi Perkakas: SIMPus STIS Theses Scraper

Panduan teknis dan operasional untuk perkakas scraper portal perpustakaan [SIMPus Politeknik Statistika STIS](https://simpus.stis.ac.id/koleksi).

---

## 1. Ikhtisar & Arsitektur Sistem

Perkakas ini dikembangkan dalam skrip Python [`scripts/scrape_simpus.py`](../scripts/scrape_simpus.py). Perkakas ini berfungsi mengotomatisasi pengumpulan metadata skripsi alumni STIS, pembimbing, abstrak lengkap, kata kunci, serta pengunduhan dokumen skripsi PDF *full-text* terenkripsi secara on-demand.

### Alur Kerja (Workflow):
1. **Ekstraksi Token Otomatis**: Membaca JWT `access_token` langsung dari database cookies Firefox lokal (`cookies.sqlite`).
2. **Metadata Gathering**: Melakukan request terpaginasi ke REST API `https://api-simpus.stis.ac.id/v2/koleksi` dengan filter klasifikasi (Sistem Informasi, Sains Data, Komputasi Statistik) dan rentang tahun.
3. **Detail Enrichment**: Mengambil data detail per skripsi (abstrak, dosen pembimbing, kata kunci, NIM) dari `/v2/koleksi/{id}`.
4. **On-Demand PDF Decryption**: Mendekripsi proteksi AES-256-CBC dua lapis pada endpoint `/v2/koleksi/{id}/read` menggunakan kunci yang diekstrak dari header response `X-SBO-Random-Key` dan `X-SBO-IV`.

---

## 2. Cara Menjalankan Perkakas (Quick Start)

Perkakas telah dilengkapi mekanisme **Auto-Virtualenv Re-execution**. Anda dapat menjalankannya dengan salah satu dari dua cara berikut:

```bash
# Cara 1: Menggunakan uv (Sangat direkomendasikan)
uv run python scripts/scrape_simpus.py [OPSI]

# Cara 2: Menjalankan langsung via python (Otomatis beralih ke .venv lokal)
python scripts/scrape_simpus.py [OPSI]
```

### Opsi Perintah Utama

| Perintah | Deskripsi |
|---|---|
| `--check-auth` | Memeriksa apakah token autentikasi dari Firefox berhasil ditemukan |
| `--min-year <TAHUN>` | Batas tahun minimal (default: 2021) |
| `--max-year <TAHUN>` | Batas tahun maksimal (default: 2026) |
| `--limit <N>` | Batasi scraping hanya untuk N data (untuk pengujian) |
| `--pdf-id <UUID>` | Download dan dekripsi file PDF untuk 1 ID skripsi spesifik |
| `--pdf-query "<KEYWORD>"` | Download dan dekripsi PDF semua skripsi yang memuat kata kunci tertentu |
| `--token <JWT>` | Masukkan token manual jika tidak menggunakan sesi Firefox |

---

## 3. Contoh Penggunaan Praktis

### A. Memeriksa Autentikasi
```bash
uv run python scripts/scrape_simpus.py --check-auth
```
*Output yang diharapkan: `[+] Token ditemukan: eyJhbGciOi...`*

### B. Mengunduh PDF Berdasarkan Topik Riset
Jika Anda sedang meneliti topik tertentu, Anda dapat mengunduh seluruh PDF yang relevan dengan satu perintah:

```bash
# Topik Satu Data Indonesia / Interoperabilitas:
uv run python scripts/scrape_simpus.py --pdf-query "satu data"

# Topik WebGIS / Geospasial:
uv run python scripts/scrape_simpus.py --pdf-query "webgis"

# Topik Kuesioner CAPI / CAWI / Validasi:
uv run python scripts/scrape_simpus.py --pdf-query "capi"

# Topik Privasi Data / Diferensial Privasi:
uv run python scripts/scrape_simpus.py --pdf-query "privasi"
```
*File PDF hasil unduhan disimpan di `literature/pdfs/`.*

### D. Konversi Otomatis ke Markdown via Marker (NVIDIA GPU)
Secara default, setiap PDF yang diunduh (baik via `--pdf-id`, `--pdf-query`, atau `--download-pdf`) akan **langsung otomatis dikonversi menjadi file Markdown** (`.md`) dengan akselerasi GPU NVIDIA RTX 4050 menggunakan Marker.

Jika Anda ingin mendownload file biner PDF saja tanpa memicu konversi Markdown:
```bash
uv run python scripts/scrape_simpus.py --pdf-query "satu data" --no-convert-md
```

---

## 4. Struktur Output Data

| Berkas | Format | Deskripsi |
|---|---|---|
| `literature/theses_data.json` | JSON | Database lengkap 389 skripsi terstruktur |
| `literature/theses_data.csv` | CSV | Tabel spreadsheet untuk analisis kuantitatif dan filtering di Excel |
| `literature/previous_theses.md` | Markdown | Laporan ringkasan taksonomi skripsi terdahulu per pilar SIS |
| `literature/pdfs/*.pdf` | PDF Binary | Dokumen PDF skripsi lengkap (diabaikan oleh git) |
| `literature/markdowns/<judul>/` | Markdown + Images | Hasil konversi Markdown beresolusi tinggi beserta gambar/diagram |


---

## 5. Troubleshooting & FAQ

1. **Error: `Gagal mendapatkan token!`**
   - **Penyebab**: Sesi SIMPus di Firefox belum aktif atau cookies telah kedaluwarsa.
   - **Solusi**: Buka Firefox, akses [simpus.stis.ac.id](https://simpus.stis.ac.id), login menggunakan akun Google STIS, lalu jalankan kembali skrip.

2. **Error: `ModuleNotFoundError` saat menjalankan `python`**
   - Skrip telah diperbarui dengan auto-bootstrap ke `.venv/bin/python`. Jika dijalankan pada terminal baru tanpa venv aktif, cukup gunakan `uv run python scripts/scrape_simpus.py`.

3. **Rate Limiting & Server Politeness**
   - Skrip memiliki jeda waktu *polite delay* (120–300 ms) antar-request untuk menjaga stabilitas server API SIMPus STIS.
