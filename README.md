# Naskah Artikel Ilmiah Interaksi Manusia dan Komputer (IMK)

Repositori penelitian dan penyusunan naskah artikel ilmiah mata kuliah **Interaksi Manusia dan Komputer (IMK)**, Program Studi Diploma IV (D-IV) Komputasi Statistik, **Politeknik Statistika STIS**.

---

## 📌 Identitas Proyek Penelitian

- **Judul Artikel Ilmiah**:  
  *"Redesain Website Dinas Pemadam Kebakaran Kota Bandar Lampung dengan Pendekatan User-Centered Design"*  
  *(Interface Redesign of Bandar Lampung City Fire Emergency Information Portal Based on User-Centered Design)*
- **Objek Penelitian**: Portal Resmi Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung ([damkar.bandarlampungkota.go.id](https://damkar.bandarlampungkota.go.id))
- **Tim Penulis (Kelompok 8)**:
  1. **Alif Zakiansyah As Syauqi** (NIM: 222312958)
  2. **Andrian Fajar Fahmi** (NIM: 222312979)
  3. **Valentina Lasma Situmorang** (NIM: 222313413)
- **Template Resmi Acuan**: [`proposals/Template Makalah IMK.docx`](file:///home/alfzki/Documents/IMK/proposals/Template%20Makalah%20IMK.docx) (Format Makalah IMK STIS, sitasi gaya APA Edisi ke-7, bebas dari kutipan skripsi SIMPUS).

---

## 🎯 Fokus Metodologi & Temuan Utama

Penelitian ini memadukan audit inspeksi ahli dan perancangan terpusat pada pengguna untuk portal layanan darurat publik:

1. **Heuristic Evaluation (10 Prinsip Jakob Nielsen)**:
   - Evaluasi usabilitas awal menemukan kelemahan mayor pada seluruh 10 prinsip Heuristik Nielsen pada website eksisting (*Before*), mencakup ketiadaan tombol darurat 113 persisten, jargon birokrasi kaku, ketiadaan rekam navigasi (*breadcrumbs*), dan formulir tanpa validasi.
2. **User-Centered Design (ISO 9241-210:2019)**:
   - Perancangan solusi interaktif 4 tahapan UCD: penetapan konteks penggunaan, pemetaan kebutuhan pengguna (Persona & User Journey), perancangan purwarupa interaktif *high-fidelity* di Figma untuk 5 modul utama (Beranda, Berita, Galeri, Dokumen, dan Kontak/Pengaduan) dengan integrasi prinsip *Emotional Design* (Norman, 2004).
3. **Evaluasi Kuantitatif WebQual 4.0 (Before vs After)**:
   - Pengujian 22 indikator WebQual 4.0 pada 3 dimensi membuktikan lonjakan kualitas antarmuka yang sangat signifikan:
     - **Usability Quality**: Skor meningkat dari **2,64** menjadi **4,52** (+1,88)
     - **Information Quality**: Skor meningkat dari **2,81** menjadi **4,58** (+1,77)
     - **Service Interaction Quality**: Skor meningkat dari **2,45** menjadi **4,61** (+2,16)
     - **Rata-rata Keseluruhan**: Skor meningkat dari **2,63** (*Kurang Baik*) menjadi **4,57** (*Sangat Baik*)

---

## 📄 Berkas Kunci Naskah & Hasil Publikasi

- **Naskah Lengkap Lolos Audit**: [`drafts/MAKALAH_ILMIAH_IMK.md`](file:///home/alfzki/Documents/IMK/drafts/MAKALAH_ILMIAH_IMK.md)  
  *Naskah artikel ilmiah lengkap 364 baris yang telah diaudit ketat dan lolos 6 pilar mutu (0 klaim tanpa bukti, 0 sitasi SIMPUS, 0 klise AI, format APA 7th).*
- **Kerangka Naskah Komprehensif**: [`drafts/OUTLINE_PAPER_IMK.md`](file:///home/alfzki/Documents/IMK/drafts/OUTLINE_PAPER_IMK.md)  
  *Struktur outline artikel ilmiah, pemetaan sitasi per bagian, dan matriks kontribusi penelitian.*
- **Dokumen Word Resmi Siap Kumpul**: [`reports/Makalah_Ilmiah_IMK_Kelompok_8.docx`](file:///home/alfzki/Documents/IMK/reports/Makalah_Ilmiah_IMK_Kelompok_8.docx)  
  *Dokumen Microsoft Word resmi hasil konversi berstandar makalah IMK dengan rumus native OMML dan hanging indent APA.*
- **Laporan Komprehensif Bab per Bab**: [`drafts/laporan_proyek_imk/`](file:///home/alfzki/Documents/IMK/drafts/laporan_proyek_imk/)  
  *Draf kerja mendalam untuk masing-masing bab laporan proyek akhir IMK.*

---

## 📁 Struktur Direktori Workspace

- [`AGENTS.md`](file:///home/alfzki/Documents/IMK/AGENTS.md): Konfigurasi persona, aturan, dan pedoman kerja AI Agent untuk naskah IMK.
- [`INSTRUCTIONS.md`](file:///home/alfzki/Documents/IMK/INSTRUCTIONS.md): Konstitusi kerja sistem: aturan mutlak bebas halusinasi, kewajiban tool-first, dan integritas sitasi.
- [`ARCHITECTURE.md`](file:///home/alfzki/Documents/IMK/ARCHITECTURE.md): Peta sistem: topologi direktori data, katalog perkakas CLI, dan alur orkestrasi naskah.
- `proposals/`: Berkas template resmi makalah IMK (`Template Makalah IMK.docx`).
- `drafts/`: Draf naskah artikel ilmiah terorkestrasi, outline, dan draf bab per bab.
- `reports/`: Dokumen Microsoft Word resmi hasil publikasi (`Makalah_Ilmiah_IMK_Kelompok_8.docx`).
- `references/`: Koleksi referensi paper ilmiah peer-reviewed & template jurnal:
  - `verified_papers.json`: Basis data referensi peer-reviewed terverifikasi.
  - `markdown/`: Naskah Markdown teks utuh paper untuk RAG penelusuran bukti empiris.
  - `references_zotero_import.bib` & `.ris`: Berkas impor terstandarisasi untuk Zotero Desktop.
  - `template/`: Direktori template tambahan (referensi umum jurnal ilmiah).
- `results/`: Hasil evaluasi usabilitas dan WebQual 4.0.
- `literature/`: Pangkalan data referensi BibTeX (`references.bib`), arsip gap internal (`theses_data.json`), dan indeks pencarian.
- `scratchpad/`: Catatan log harian dan status milestone tim (`daily_notes.md`).
- `docs/`: Dokumentasi teknis lengkap setiap perkakas otomasi riset.
- `scripts/`: Perkakas otomasi riset dan pipeline publikasi ilmiah.
- `src/calm_carson/`: Paket Python internal modular (metadata, search, verify, publisher).
- `tests/`: Unit test suite otomatis (68 unit tests passing).

---

## 🛠️ Quick Start Perkakas Riset & Publikasi

### 1. Audit Kualitas & Uji Grounding Naskah (Strict Quality Gate)
```bash
# Audit 6 pilar artikel ilmiah (memblokir skripsi SIMPUS, grounding klaim, deteksi klise AI, keselarasan angka WebQual):
uv run python scripts/audit_paper_draft.py \
  --file drafts/MAKALAH_ILMIAH_IMK.md \
  --strict

# Audit dengan keluaran JSON terstruktur:
uv run python scripts/audit_paper_draft.py \
  --file drafts/MAKALAH_ILMIAH_IMK.md \
  --json
```

### 2. Ekspor Draf Markdown ke Dokumen DOCX Resmi Makalah IMK
```bash
# Mengonversi draf Markdown ke file Word berstandar format makalah IMK (OMML native):
uv run python scripts/export_to_docx.py \
  --input drafts/MAKALAH_ILMIAH_IMK.md \
  --output reports/Makalah_Ilmiah_IMK_Kelompok_8.docx
```

### 3. Temu-Balik Bukti Referensi Ilmiah RAG (HCI & WebQual 4.0)
```bash
# Menelusuri kutipan empiris dari paper peer-reviewed terverifikasi lokal:
uv run python scripts/query_references.py --query "User-Centered Design WebQual 4.0 evaluasi portal" --limit 3

# Menampilkan saran paper berdasarkan tema HCI (ucd, webqual, heuristic, usability):
uv run python scripts/query_references.py --suggest webqual

# Menampilkan detail sitasi dan teks lengkap dokumen rujukan spesifik:
uv run python scripts/query_references.py --citekey Chairani2024WebQual
```

### 4. Penelusuran & Ingesti Paper Peer-Reviewed Baru (Bebas SIMPUS)
```bash
# Mencari paper peer-reviewed global secara otomatis (OpenAlex, Crossref, arXiv):
uv run python scripts/search_academic_papers.py \
  --query "user-centered design emergency public portal" \
  --platform all \
  --auto-ingest 1

# Ingesti paper PDF baru ke koleksi referensi (skripsi SIMPUS otomatis ditolak):
uv run python scripts/ingest_new_reference.py \
  --pdf path/to/paper.pdf \
  --doi "10.1145/xxxx"
```

### 5. Audit Gaya Bahasa AI (Wikipedia: Signs of AI Writing)
```bash
# Mengaudit draf dari klise robotik, tanda pisah berspasi, dan kebocoran LLM:
uv run python scripts/check_ai_style.py \
  --file drafts/MAKALAH_ILMIAH_IMK.md \
  --suggest-fixes
```

### 6. Verifikasi Keabsahan Faktual & Validitas Sitasi
```bash
# Memverifikasi naskah draf secara ketat:
uv run python scripts/verify_claims.py \
  --file drafts/MAKALAH_ILMIAH_IMK.md \
  --strict
```

### 7. Menjalankan Seluruh Unit Test Suite
```bash
uv run python -m unittest discover tests
```
