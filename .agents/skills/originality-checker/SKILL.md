---
name: originality-checker
description: Menguji dan mengevaluasi kebaruan (novelty) serta orisinalitas ide penelitian ilmiah terhadap publikasi global (OpenAlex, arXiv, Crossref) dan korpus lokal.
---

# Panduan Keahlian: Originality & Novelty Checker

Keahlian ini membekali agen untuk bertindak sebagai *Critical Reviewer & Novelty Evaluator* dalam menguji kemiripan ide, memindai publikasi global, dan merumuskan usulan penguatan kebaruan (*differentiation matrix*).

---

## 1. Peran & Tanggung Jawab Utama

1. **Pemindaian Literatur Global**:
   - Menghubungkan kueri ide riset ke ribuan publikasi Scopus/OpenAlex dan preprint arXiv (Human-Computer Interaction / CS).
   - Menghitung kemiripan leksikal dan semantik antara ide usulan dan publikasi yang ada.
2. **Penentuan Skor Kemiripan (Overlap Score)**:
   - Mengkategorikan tingkat irisan ide: *Low Overlap* (orisinalitas kuat), *Moderate Overlap* (perlu penguatan sudut pembeda), atau *High Overlap* (risiko duplikasi tinggi).
3. **Penyusunan Matriks Pembeda (Differentiation Strategy)**:
   - Merumuskan rekomendasi pembeda: konteks portal layanan darurat kebencanaan di Indonesia, integrasi Heuristic Evaluation dengan siklus UCD 4 tahap, dan evaluasi kuantitatif komparatif Before vs After berbasis WebQual 4.0.

---

## 2. Prosedur Eksekusi CLI Perkakas

Jalankan pengujian orisinalitas melalui `uv run`:

### A. Menguji Rumusan Ide Secara Langsung
```bash
uv run python scripts/check_originality.py \
  --idea "Redesain Antarmuka Portal Informasi Darurat Kebakaran Kota Bandar Lampung Berbasis User-Centered Design dan Evaluasi WebQual 4.0" \
  --export
```

### B. Menguji Draf Naskah Berkas Markdown
```bash
uv run python scripts/check_originality.py \
  --file drafts/MAKALAH_ILMIAH_IMK.md \
  --export
```

Laporan evaluasi orisinalitas (JSON & Markdown) akan disimpan di folder analisis terkait.
