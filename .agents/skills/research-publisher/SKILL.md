---
name: research-publisher
description: Memvalidasi kepatuhan format naskah artikel ilmiah IMK (Template Makalah IMK), merapikan sitasi, dan mengompilasi naskah ke format DOCX & PDF siap kumpul.
---

# Panduan Keahlian: Scientific Research Publisher

Keahlian ini membekali agen untuk memvalidasi struktur dokumen makalah IMK, memastikan kelengkapan elemen sesuai `Template Makalah IMK.docx`, dan mengompilasi naskah Markdown menjadi berkas Microsoft Word (.docx) siap kumpul dengan styling akademik, persamaan OMML native, dan hanging indent APA.

---

## 1. Peran & Tanggung Jawab Utama

1. **Validasi Kepatuhan Format Naskah**:
   - Memastikan kelengkapan elemen naskah: Judul bilingual (Indonesia & Inggris), Penulis & Afiliasi STIS, Abstrak (<= 200 kata) & Kata Kunci, Bagian Utama (1. Pendahuluan, 2. Metodologi, 3. Hasil dan Pembahasan, 4. Kesimpulan), serta Daftar Pustaka APA 7th.
   - Memverifikasi jumlah referensi minimum dan larangan mutlak sitasi skripsi SIMPUS STIS.
2. **Kompilasi DOCX Makalah Resmi**:
   - Mengonversi berkas Markdown naskah ke Microsoft Word berstandar jurnal/makalah menggunakan `scripts/export_to_docx.py`.
   - Menghasilkan dokumen Word akhir di `reports/Makalah_Ilmiah_IMK_Kelompok_8.docx`.
3. **Pipeline Validasi Dokumen & Audit 6 Pilar**:
   - Menjalankan audit kepatuhan template makalah IMK, grounding klaim, anti-SIMPUS, dan integritas sitasi via `scripts/audit_paper_draft.py`.

---

## 2. Prosedur Eksekusi CLI Perkakas

Jalankan penerbitan dan konversi dokumen melalui `uv run`:

### A. Ekspor Naskah Markdown ke Format Word Resmi Makalah IMK
```bash
uv run python scripts/export_to_docx.py \
  --input drafts/MAKALAH_ILMIAH_IMK.md \
  --output reports/Makalah_Ilmiah_IMK_Kelompok_8.docx
```

### B. Validasi Kepatuhan Naskah dan Template (Audit 6 Pilar)
```bash
uv run python scripts/audit_paper_draft.py \
  --file drafts/MAKALAH_ILMIAH_IMK.md \
  --strict
```
