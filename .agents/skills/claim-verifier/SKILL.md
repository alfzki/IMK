---
name: claim-verifier
description: Memverifikasi keabsahan klaim faktual, mendeteksi kontradiksi angka kuantitatif, dan memvalidasi kepatuhan sitasi standar APA/IEEE pada naskah artikel ilmiah IMK.
---

# Panduan Keahlian: Claim & Fact Verifier (Zero-Hallucination Gate)

Keahlian ini membekali agen untuk bertindak sebagai *Factual Integrity & Citation Verifier* dalam memastikan naskah penelitian terbebas dari angka fiktif, halusinasi model AI, dan klaim tanpa dasar literatur.

---

## 1. Peran & Tanggung Jawab Utama

1. **Dekomposisi Klaim Atomik**:
   - Membedah narasi latar belakang, landasan teori, metodologi, dan pembahasan menjadi proposisi-proposisi klaim individual yang dapat diverifikasi.
2. **Pencocokan Angka Empiris (Number Boosting Retrieval)**:
   - Mencocokkan angka-angka kuantitatif (frekuensi insiden kebakaran, waktu tanggap 15 menit Permendagri 114/2018, skor WebQual 4.0 Before vs After, tingkat keparahan Heuristik) terhadap korpus lokal menggunakan temu-balik hybrid.
   - Mengidentifikasi kontradiksi (*CONTRADICTED*), klaim yang didukung (*SUPPORTED*), atau klaim yang kekurangan sitasi (*CITATION_NEEDED*).
3. **Audit Integritas Bibliografi**:
   - Memastikan setiap penanda sitasi format APA atau IEEE terdaftar secara valid di berkas `references/verified_papers.json` atau `literature/references.bib`.

---

## 2. Prosedur Eksekusi CLI Perkakas

Jalankan verifikasi klaim melalui `uv run`:

### A. Memverifikasi Berkas Draf Naskah (Mode Ketat)
```bash
uv run python scripts/verify_claims.py --file drafts/MAKALAH_ILMIAH_IMK.md --strict --export
```

### B. Memverifikasi Teks / Paragraf Cepat
```bash
uv run python scripts/verify_claims.py \
  --text "Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung mendokumentasikan 271 kebakaran pada 2024 dan 198 pada 2025, dengan waktu tanggap SPM maksimal 15 menit." \
  --annotated-only
```
