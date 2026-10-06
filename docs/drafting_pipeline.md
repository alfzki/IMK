# Panduan Sistem: Pipeline Semi-Otomatis Penyusunan Naskah Skripsi Bab demi Bab

Dokumen ini memuat arsitektur teknis, metodologi alur kerja terpadu (*integrated workflow*), panduan antarmuka perintah CLI, dan mekanisme titik kendali pengguna (*human-in-the-loop checkpoint*) untuk menyusun naskah penelitian proposal maupun skripsi tingkat akhir mahasiswa Diploma IV Komputasi Statistik (Peminatan Sistem Informasi Statistik) Politeknik Statistika STIS.

---

## 1. Arsitektur Alur Kerja Terpadu (Pipeline Workflow)

Sistem mengintegrasikan seluruh kapabilitas data lokal, penelusuran semantik hybrid, penulisan berbasis bukti, verifikasi keabsahan klaim faktual, dan iterasi revisi otomatis ke dalam 6 fase terstruktur:

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│              PEMILIHAN TOPIK & INISIALISASI WORKFLOW STATE                       │
│  - Preset: Topik 1 (CAPI Fraud), Topik 2 (SDI Gateway), Topik 3 (Diff Privacy)   │
│  - Mendukung Judul Topik Kustom Mahasiswa & Penelusuran Korpus Dinamis          │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                      FASE 1: THESIS OUTLINER (outliner.py)                       │
│  - Menyusun hierarki Bab & Sub-bab standar STIS D-IV SIS (IEEE Format)          │
│  - Menetapkan fokus kajian, target data kuantitatif, dan kata kunci kueri        │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                    FASE 2: EVIDENCE COLLECTOR (collector.py)                     │
│  - Hybrid Search Korpus (Dense CUDA MiniLM + Sparse BM25Okapi)                  │
│  - Database 389 Skripsi Alumni STIS (theses_data.json) untuk Benchmarking       │
│  - Database Kesenjangan Riset (brainstorming_gaps.json) untuk Future Work        │
│  - Bank Data Masalah Empiris BPS (bank_data_masalah_proposal.md)                │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                     FASE 3: SECTION DRAFTER (drafter.py)                         │
│  - Sintesis teks narasi akademik formal Bahasa Indonesia ilmiah baku            │
│  - Penyematan bukti angka riil (persentase, petugas, durasi, skor IPS)           │
│  - Integrasi penanda sitasi resmi standar IEEE [1], [2]                          │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│              FASE 4: AUDIT VERIFIKASI & AUTOMATED REVISER (reviser.py)           │
│  - Pembedahan klaim atomik & pencocokan bukti korpus (calm_carson.verify)        │
│  - Loop Revisi Otomatis (hingga 3 iterasi):                                     │
│    * Koreksi angka bertentangan (CONTRADICTED -> Angka Sahih Bukti Korpus)      │
│    * Penyisipan nomor rujukan IEEE yang hilang (MISSING -> Rekomendasi Sitasi)  │
│    * Pelunakan klaim spekulatif tanpa rujukan (UNSUPPORTED)                      │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│               FASE 5: HUMAN-IN-THE-LOOP CHECKPOINT (checkpoint.py)               │
│  - Menampilkan ringkasan status bab, audit keabsahan, dan pratinjau naskah      │
│  - Titik Kendali Terminal:                                                       │
│    [1] Setujui & Lanjut (Approve)   [2] Masukkan Catatan Suntingan (Edit)        │
│    [3] Tulis Ulang Bab (Regenerate) [4] Simpan Status & Jeda (Save & Pause)      │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│               FASE 6: PERAKITAN NASKAH LENGKAP & EXPORT (pipeline.py)            │
│  - Menyimpan berkas bab individual: drafts/bab_1_*.md, bab_2_*.md, dst.          │
│  - Mengompilasi Naskah Terpadu dengan Daftar Isi: drafts/naskah_lengkap_skripsi.md│
│  - Menyimpan riwayat workflow_state.json untuk resume sewaktu-waktu              │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Struktur Bab & Standar Akademik STIS D-IV SIS

Pipeline mendukung dua lingkup naskah:
1. **Mode Proposal Penelitian (`--scope proposal`)**:
   - **BAB I: PENDAHULUAN**:
     - 1.1 Latar Belakang Masalah (wajib memuat 3 masalah riil berangka kuantitatif BPS & sitasi resmi, diakhiri solusi terpadu).
     - 1.2 Rumusan Masalah.
     - 1.3 Tujuan Penelitian.
     - 1.4 Batasan Masalah.
     - 1.5 Manfaat Penelitian (Teoritis & Praktis bagi BPS).
   - **BAB II: TINJAUAN PUSTAKA**:
     - 2.1 Landasan Teori & Konsep Dasar (GSBPM, arsitektur sistem, keamanan).
     - 2.2 Kajian Penelitian Terdahulu (State-of-the-Art & skripsi alumni STIS).
     - 2.3 Tabel I Kontribusi Penelitian & Benchmarking Literatur.
     - 2.4 Kesenjangan Penelitian (*Research Gap*), Dampak, & Urgensi.
   - **BAB III: METODOLOGI PENELITIAN**:
     - 3.1 Desain Penelitian (*Design Science Research Methodology* / DSRM 6 Fase).
     - 3.2 Karakteristik & Sumber Data Penelitian (kepatuhan UU PDP No. 27/2022).
     - 3.3 Perancangan Arsitektur Sistem & Spesifikasi Artefak.
     - 3.4 Lingkungan Komputasi & Perkakas Pengembangan (GPU CUDA, Docker).
     - 3.5 Metrik Pengujian & Evaluasi Kualitas Perangkat Lunak (ISO/IEC 25010 & F1-Score).
     - 3.6 Kerangka Pikir Penelitian & Tabel II Jadwal Pelaksanaan (10 Bulan).
2. **Mode Skripsi Lengkap (`--scope thesis`)**:
   - Menambahkan **BAB IV** (Analisis Kebutuhan, Perancangan UML/Basis Data, Implementasi Algoritma, dan Hasil Evaluasi ISO 25010) serta **BAB V** (Kesimpulan dan Saran Masa Depan / *Future Work*).

---

## 3. Panduan Penggunaan CLI (`scripts/orchestrate_drafting.py`)

Perkakas CLI `scripts/orchestrate_drafting.py` menyediakan antarmuka terpadu untuk mengeksekusi pipeline:

### A. Melihat Daftar Topik Unggulan
```bash
uv run python scripts/orchestrate_drafting.py --list-topics
```

### B. Menjalankan Penyusunan Interaktif (Rekomendasi Utama)
Pengguna akan diajak meninjau draf dan audit keabsahan pada setiap akhir bab sebelum melanjutkan:
```bash
uv run python scripts/orchestrate_drafting.py --topic 1 --scope proposal
```

### C. Melanjutkan Progres yang Dijeda (*Resume Capability*)
Jika sesi sebelumnya dijeda menggunakan opsi `[4] Save & Pause`, alur kerja dapat dilanjutkan langsung dari bab terakhir:
```bash
uv run python scripts/orchestrate_drafting.py --resume
```

### D. Menyusun Bab Tertentu Saja
Untuk merevisi atau menyusun ulang satu bab tertentu tanpa memproses bab lain:
```bash
uv run python scripts/orchestrate_drafting.py --topic 1 --chapter 2
```

### E. Mode Otomatis Penuh (Auto-Approve / CI Batch Mode)
Untuk menghasilkan draf seluruh bab secara instan tanpa menunggu interaksi terminal:
```bash
uv run python scripts/orchestrate_drafting.py --topic 1 --scope proposal --auto-approve --output-dir drafts/topik_1
```

---

## 4. Mekanisme Titik Kendali Manusia (*Human Checkpoint*)

Pada setiap akhir fase drafting bab, sistem menampilkan ringkasan visual audit dan terminal prompt interaktif:

```text
================================================================================
📋 TITIK KENDALI PENGGUNA (HUMAN CHECKPOINT): PENDAHULUAN
================================================================================
ID Bab         : bab_1 (Bab 1)
Status Draf    : VERIFIED
Jumlah Revisi  : 0 iterasi otomatis
Audit Keabsahan: 🟢 19 Didukung | 🔴 0 Kontradiksi | 💡 0 Perlu Sitasi | ❓ 0 Kurang Bukti
Status Mutu    : READY_FOR_SUBMISSION
--------------------------------------------------------------------------------
📄 PRATINJAU DRAF NASKAH (15 Baris Pertama):
...
--------------------------------------------------------------------------------

PILIHAN TINDAKAN:
  [1] Setujui & Lanjutkan ke Bab Berikutnya (Approve)
  [2] Masukkan Catatan Suntingan / Koreksi Manual (Edit)
  [3] Tulis Ulang Draf Bab Ini (Regenerate)
  [4] Simpan Status & Jeda Progres (Save & Pause)
```

- **Opsi 1 (Approve)**: Menyetujui naskah bab saat ini, menyimpannya ke berkas Markdown, memperbarui state, dan melangkah ke bab berikutnya.
- **Opsi 2 (Edit)**: Memberikan catatan instruksi atau paragraf tambahan dari pengguna. Sistem akan menyematkan masukan tersebut ke draf sebelum melanjutkan.
- **Opsi 3 (Regenerate)**: Menjalankan ulang penelusuran bukti dan drafting untuk bab tersebut.
- **Opsi 4 (Save & Pause)**: Menyimpan snapshot `WorkflowState` ke berkas `workflow_state.json` dan keluar secara aman.

---

## 5. Struktur Berkas dan Output

- **Modul Inti**: `src/calm_carson/drafting/`
  - `models.py`: Data model (`ChapterOutline`, `SubSectionOutline`, `EvidenceItem`, `SectionDraft`, `WorkflowState`).
  - `outliner.py`: Generator kerangka naskah bab/sub-bab.
  - `collector.py`: Pengumpul bukti multi-sumber dari korpus lokal.
  - `drafter.py`: Generator teks narasi akademik berbasis bukti.
  - `reviser.py`: Mesin iterasi revisi otomatis berbasis audit klaim.
  - `checkpoint.py`: Manajer titik kendali interaktif pengguna.
  - `pipeline.py`: Orkestrator alur kerja multi-bab dan perakitan naskah lengkap.
- **Skrip CLI**: `scripts/orchestrate_drafting.py`
- **Unit Test Suite**: `tests/test_drafting_pipeline.py` (6 tes unit terotomasi)
- **Keluaran Draf Naskah**:
  - `drafts/<topik>/bab_1_pendahuluan.md`
  - `drafts/<topik>/bab_2_tinjauan_pustaka.md`
  - `drafts/<topik>/bab_3_metodologi_penelitian.md`
  - `drafts/<topik>/naskah_lengkap_skripsi.md` (naskah terpadu lengkap dengan Daftar Isi)
  - `drafts/<topik>/workflow_state.json` (rekam status workflow)
