---
name: paper-auditor
description: >-
  Audit, fact-check, and polish scientific research paper drafts for Human-Computer Interaction (HCI) and Information Systems.
  Verifies that claims only come from verified downloaded peer-reviewed papers (references/markdown/),
  matches cited text to original paper markdowns, flags ungrounded claims ([KLAIM_BELUM_TERVERIFIKASI]),
  strictly blocks SIMPUS skripsi theses ([SIMPUS_THESIS_DISALLOWED]), validates bibliography to prevent hallucinated DOIs/titles,
  reconciles empirical numbers with evaluation metrics, enforces journal template rules, and eliminates stiff robotic AI writing styles.
---

# Scientific Paper Auditor & Fact-Checking Guide for HCI & Information Systems Research

Skill ini digunakan untuk mengaudit, memverifikasi keabsahan fakta/klaim ilmiah, memeriksa integritas daftar pustaka, menolak rujukan skripsi alumni, memastikan kepatuhan template penulisan (Template Makalah IMK), mencocokkan angka empiris dengan data evaluasi, dan membersihkan gaya bahasa kaku khas AI dari draf naskah paper HCI dan Sistem Informasi.

---

## 1. Prosedur Audit Otomatis Naskah

Jalankan perintah audit utama pada berkas draf Markdown:
```bash
# Audit standar dengan laporan ringkas
uv run python scripts/audit_paper_draft.py --file drafts/MAKALAH_ILMIAH_IMK.md

# Audit dengan laporan JSON terstruktur
uv run python scripts/audit_paper_draft.py --file drafts/MAKALAH_ILMIAH_IMK.md --json

# Audit mode ketat (gagal/exit 1 jika ada klaim belum terverifikasi, sitasi SIMPUS, atau pelanggaran fatal)
uv run python scripts/audit_paper_draft.py --file drafts/MAKALAH_ILMIAH_IMK.md --strict
```

---

## 2. Enam Pilar Kualitas Audit (Zero-Tolerance Quality Gates)

### 📌 Pilar 1: Verifikasi Klaim Berdasar Sumber (Claim Grounding)
1. **Aturan Mutlak:** Klaim literatur hanya boleh merujuk pada **paper peer-reviewed yang telah diunduh dan terverifikasi** di repositori proyek (`references/verified_papers.json` & `literature/references.bib`).
2. **Penanganan `[SUMBER_TIDAK_TERDAFTAR]`:**
   - Sitasi tersebut belum di-ingest ke dalam repositori resmi.
   - **Tindakan:** Cari paper aslinya via `scripts/search_academic_papers.py` dan lakukan ingesti via `scripts/ingest_new_reference.py`.
3. **Penanganan `[KLAIM_BELUM_TERVERIFIKASI]`:**
   - Kalimat memuat pernyataan, klaim angka, atau metodologi yang tidak didukung oleh teks asli di `references/markdown/<citekey>/`.
   - **Tindakan:** Buka teks asli paper rujukan via `scripts/query_references.py --citekey "<citekey>"`, lalu sesuaikan narasi agar 100% selaras dengan temuan penulis asli.

---

### 📌 Pilar 2: Larangan Mutlak Skripsi SIMPUS (`[SIMPUS_THESIS_DISALLOWED]`)
1. **Aturan Mutlak:** Naskah artikel ilmiah **TIDAK BOLEH** mengutip skripsi sarjana terapan / skripsi S1 dari repositori SIMPUS STIS (`simpus.stis.ac.id`) atau skripsi lokal lainnya sebagai referensi ilmiah.
2. **Jika Ditemukan Penanda `[SIMPUS_THESIS_DISALLOWED]`:**
   - Auditor akan menandai pelanggaran fatal dan memblokir persetujuan draf.
   - **Tindakan:** Ganti sitasi skripsi tersebut dengan paper jurnal internasional/nasional bereputasi (SINTA 1–4, Scopus Q1–Q4) atau prosiding konferensi yang membahas metode serupa.

---

### 📌 Pilar 3: Integritas Daftar Pustaka (Anti-Halusinasi & Format Baku APA 7th)
1. **Verifikasi Entri:** Setiap entri pada bagian `DAFTAR PUSTAKA` harus memiliki:
   - Nama penulis sesuai format APA (nama belakang diikuti inisial nama depan).
   - Tahun publikasi yang benar dalam tanda kurung `(202X)`.
   - Judul paper asli (tidak boleh disederhanakan/dikarang oleh AI).
   - Nama jurnal ilmiah atau prosiding resmi format miring (*italic*).
   - Tautan DOI asli yang valid (`https://doi.org/10.xxxx/...`) atau URL repositori terpercaya.
2. **Kesesuaian Dua Arah (Bidirectional Rule):**
   - Setiap referensi di Daftar Pustaka **wajib disitir** di dalam tubuh naskah.
   - Setiap sitasi di tubuh naskah **wajib tercantum** di Daftar Pustaka.

---

### 📌 Pilar 4: Rekonsiliasi Angka Empiris terhadap Data Evaluasi
1. **Kesesuaian 100% Data Evaluasi:**
   - Seluruh angka metrik kuantitatif (skor Heuristik Nielsen skala 0–4, skor rata-rata dimensi WebQual 4.0 Usability Quality, Information Quality, Service Interaction Quality, persentase peningkatan Sebelum vs Sesudah redesain, jumlah responden) di narasi abstrak, pembahasan, dan tabel **wajib identik dan konsisten 100%**:
     - *Usability Quality*: 2,64 $\rightarrow$ 4,52 (+1,88)
     - *Information Quality*: 2,81 $\rightarrow$ 4,58 (+1,77)
     - *Service Interaction Quality*: 2,45 $\rightarrow$ 4,61 (+2,16)
     - *Rata-rata Keseluruhan*: 2,63 $\rightarrow$ 4,57 (+1,94)
2. **Konsistensi Data Lapangan & Regulasi:**
   - Catatan insiden kebakaran dan penyelamatan (413 kebakaran 2023, 271 kebakaran 2024, 198 kebakaran 2025, 518 aksi rescue 2025) serta SPM waktu tanggap 15 menit Permendagri 114/2018 harus sinkron dan berdasar rujukan valid.

---

### 📌 Pilar 5: Kepatuhan Format Template Ilmiah (Template Makalah IMK)
Pastikan struktur dokumen mematuhi standar naskah ilmiah:

| Bagian | Ketentuan Template | Larangan / Kesalahan Umum |
| :--- | :--- | :--- |
| **Judul Naskah** | Judul Bahasa Indonesia (singkat, lugas, Title Case), dan Judul Bahasa Inggris di dalam kurung `(...)` miring (*italic*). | Menghilangkan judul bahasa Inggris. |
| **ABSTRAK** | Satu paragraf utuh, maksimal **150–200 kata**. Wajib memuat: Latar Belakang, Tujuan, Metode, Hasil Utama, dan Kesimpulan. Kata kunci 3–5 kata. | Melebihi 200 kata; memuat sitasi pustaka; memuat rumus matematika. |
| **PENDAHULUAN** | Masalah nyata berangka empiris (lonjakan kebakaran/penyelamatan, SPM 15 menit vs kontak tersembunyi, isu heuristik), studi literatur, kesenjangan riset, dan tujuan penelitian. | Mengawali dengan klise "Di era modern ini". |
| **METODE** | Alur UCD 4 tahap (ISO 9241-210), parameter Evaluasi Heuristik (10 prinsip Nielsen, skala severity 0–4), perancangan purwarupa Figma 5 modul utama, dan instrumen WebQual 4.0 (22 indikator). | Penjelasan metode tanpa tahapan operasional yang terukur. |
| **HASIL & PEMBAHASAN** | Temuan evaluasi heuristik, visualisasi perancangan Figma, dan tabel komparasi WebQual 4.0 Before vs After. Tabel berformat terbuka (hanya garis horizontal; **tanpa garis vertikal**). Ulas seluruh tabel/gambar dalam narasi (`Tabel 1`, `Gambar 1`). | Tabel berpembatas vertikal; screenshot tabel gambar; tabel tidak dibahas dalam teks. |
| **KESIMPULAN & SARAN** | Dapat ditulis dalam bentuk narasi/paragraf maupun penomoran (*pointer/numbering* terstruktur) sesuai `Template Makalah IMK.docx`. Wajib menjawab tujuan penelitian, memuat kelebihan & keterbatasan, serta menyertakan saran aplikatif. | Saran normatif tanpa kaitan hasil penelitian; kesimpulan yang tidak menjawab tujuan penelitian. |

---

### 📌 Pilar 6: Eliminasi Gaya Bahasa Robot, Klise AI, dan Puffery
1. **Hapus Seluruh Klise Kosakata AI:**
   - ❌ *menyelami* $\rightarrow$ ✅ *mengkaji / menganalisis / meneliti*
   - ❌ *rajutan / anyaman metaforis* $\rightarrow$ ✅ sebutkan variabel / faktor konkret
   - ❌ *memainkan peran penting / krusial* $\rightarrow$ ✅ jelaskan fungsi operasional konkret
   - ❌ *bukti nyata dari* $\rightarrow$ ✅ paparkan data angka / temuan kuesioner
   - ❌ *dalam lanskap yang dinamis* $\rightarrow$ ✅ sebutkan konteks lingkungan riset konkret
   - ❌ *tidak dapat dipungkiri bahwa / tak terbantahkan bahwa* $\rightarrow$ ✅ sajikan premis ilmiah langsung berlandaskan sitasi
   - ❌ *perlu dicatat bahwa / penting untuk dicatat bahwa* $\rightarrow$ ✅ langsung sampaikan pokok pikiran tanpa pembuka semu
   - ❌ *di era modern ini / di era digital saat ini* $\rightarrow$ ✅ mulai latar belakang dengan data empiris riil
2. **Hilangkan Bahasa Promotif / Puffery:**
   - ❌ *berhasil memangkas* $\rightarrow$ ✅ *meningkatkan skor usabilitas dari 2,64 menjadi 4,52*
   - ❌ *secara dramatis mereduksi* $\rightarrow$ ✅ *menurunkan hambatan navigasi dan beban kognitif*
   - ❌ *mendongkrak kepuasan* $\rightarrow$ ✅ *meningkatkan skor evaluasi WebQual 4.0*
   - ❌ *sangat direkomendasikan* $\rightarrow$ ✅ *dapat dipertimbangkan / berpotensi dimanfaatkan*
3. **Koreksi Tipografi Tanda Pisah (Em Dash):**
   - ❌ `portal ini — yang berbasis UCD — menghasilkan...` (berspasi salah)
   - ✅ `portal ini—yang berbasis UCD—menghasilkan...` (rapat sesuai EYD V) atau gunakan koma ganda.
4. **Cegah Kebocoran Prompt LLM:**
   - Bersihkan tag `[:contentReference]`, `[oai_citation]`, `[cite: X]`, serta sapaan chatbot (*"Tentu saja!"*, *"Berikut adalah draf..."*).
