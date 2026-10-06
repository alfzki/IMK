# Direktori Panduan & Template Makalah IMK

Direktori ini digunakan untuk menyimpan berkas template resmi naskah artikel ilmiah mata kuliah **Interaksi Manusia dan Komputer (IMK)** Politeknik Statistika STIS.

---

## 📄 Berkas dalam Direktori Ini

1. **[`Template Makalah IMK.docx`](file:///home/alfzki/Documents/IMK/proposals/Template%20Makalah%20IMK.docx)**:
   - Template resmi Microsoft Word untuk penulisan artikel ilmiah / makalah IMK Politeknik Statistika STIS.
   - Mengatur format judul bilingual, abstrak satu paragraf (maksimal 150–200 kata) dengan kata kunci, penomoran bagian utama (1. PENDAHULUAN, 2. METODOLOGI, 3. HASIL DAN PEMBAHASAN, 4. KESIMPULAN), tabel terbuka tanpa garis vertikal, serta daftar pustaka format APA Edisi ke-7.

---

## 📌 Ketentuan Penulisan Naskah Makalah IMK

Setiap naskah wajib memenuhi standar kualitas akademik:
- **Judul**: Maksimal 12 kata dalam Bahasa Indonesia sesuai template resmi, singkat, lugas, dilengkapi judul bahasa Inggris format miring (*italic*).
- **Abstrak**: Maksimal 150–200 kata, 1 paragraf utuh, memuat urgensi masalah, metodologi (Heuristik, UCD ISO 9241-210, Figma), hasil utama WebQual 4.0 Before vs After, dan kesimpulan. Dilarang memuat sitasi atau rumus. Kata kunci: 3–5 kata.
- **Pendahuluan**: Memuat minimal 3 permasalahan nyata yang didukung angka/data empiris riil (data insiden Damkarmat, SPM Permendagri 114/2018, isu usabilitas) dan sitasi literatur ilmiah yang valid.
- **Metodologi**: Uraian 4 tahapan UCD, 10 prinsip Heuristik Nielsen dengan severity rating, perancangan purwarupa Figma 5 modul utama, dan 22 butir indikator WebQual 4.0.
- **Hasil dan Pembahasan**: Analisis temuan evaluasi heuristik, visualisasi purwarupa hasil redesain, dan tabel komparasi kuantitatif WebQual 4.0 Before vs After.
- **Kesimpulan dan Saran**: Dapat ditulis dalam bentuk narasi/paragraf maupun penomoran (*pointer/numbering* terstruktur) sesuai ketentuan `Template Makalah IMK.docx`. Wajib menjawab tujuan penelitian, memuat kelebihan & keterbatasan hasil, serta menyertakan saran aplikatif.
- **Daftar Pustaka**: Format APA Edisi ke-7, minimal 20 referensi ilmiah (minimal 10 paper $\ge 2021$ terindeks SINTA/Scopus), serta **DILARANG MENGUTIP SKRIPSI SIMPUS STIS**.

---

## ⚙️ Validasi & Ekspor Naskah Makalah IMK

Setelah naskah Markdown selesai disusun atau disunting, jalankan audit ketat dan konversi ke Word:
```bash
# 1. Audit ketat 6 pilar naskah Markdown:
uv run python scripts/audit_paper_draft.py --file drafts/MAKALAH_ILMIAH_IMK.md --strict

# 2. Ekspor ke format Word resmi (.docx):
uv run python scripts/export_to_docx.py \
  --input drafts/MAKALAH_ILMIAH_IMK.md \
  --output reports/Makalah_Ilmiah_IMK_Kelompok_8.docx
```
