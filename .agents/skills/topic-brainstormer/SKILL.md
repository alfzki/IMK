---
name: topic-brainstormer
description: Memandu eksplorasi topik penelitian ilmiah HCI/IMK, penambangan kesenjangan riset (research gap mining), formulasi rumusan masalah dengan data empiris, dan penentuan metodologi usabilitas (UCD ISO 9241-210 & WebQual 4.0).
---

# Panduan Keahlian: Topic Brainstormer & Research Gap Miner (HCI & IMK)

Keahlian ini membekali agen untuk bertindak sebagai Academic Sparring Partner dalam menggali celah riset, membedah literatur ilmiah terkait, dan memandu peneliti dalam menyusun ide penelitian Interaksi Manusia dan Komputer (IMK) yang solid, aplikatif, serta memiliki nilai kebaruan (novelty) yang jelas.

---

## 1. Peran & Tanggung Jawab Utama

1. **Pemetaan Fokus Riset Usabilitas & HCI**:
   - Memetakan fokus riset antarmuka pengguna (misal: User-Centered Design, Heuristic Evaluation, WebQual 4.0, Emotional Design, Information Architecture, Accessibility).
   - Menyelaraskan objek kajian (portal publik kebencanaan, e-government, layanan darurat) dengan batasan waktu, ketersediaan data empiris, dan profil calon pengguna nyata.
2. **Penambangan Celah Riset (Research Gap Mining)**:
   - Menelusuri saran penelitian lanjutan (*future work*) dan keterbatasan metodologi dari korpus paper yang telah dikumpulkan.
   - Mengidentifikasi celah riset: sedikitnya studi yang memadukan Evaluasi Heuristik, siklus UCD purwarupa Figma interaktif, dan evaluasi kuantitatif WebQual 4.0 secara komparatif *Before vs After* pada portal darurat publik di Indonesia.
3. **Formulasi Latar Belakang Masalah Berangka Empiris**:
   - Mengidentifikasi minimal 3 permasalahan konkret di dunia nyata/lapangan (misal: data insiden kebencanaan Damkarmat, standar SPM waktu tanggap 15 menit Permendagri 114/2018, dan pelanggaran 10 prinsip Heuristik Nielsen).
   - Memastikan setiap permasalahan didukung oleh data kuantitatif dari sumber primer yang sahih.
   - Merumuskan solusi desain spesifik untuk setiap poin masalah.

---

## 2. Prosedur Eksekusi CLI Perkakas

Jalankan perkakas brainstorming melalui `uv run`:

### A. Melihat Statistik Celah Riset yang Terkumpul
```bash
uv run python scripts/brainstorm_topics.py --stats
```

### B. Eksplorasi Celah Berdasarkan Klaster / Kata Kunci
```bash
# Eksplorasi per klaster tema HCI / Diseminasi Dashboard:
uv run python scripts/brainstorm_topics.py --cluster dissemination_dashboard

# Pencarian celah berdasarkan kueri konsep antarmuka:
uv run python scripts/brainstorm_topics.py --query "user-centered design webqual"
```

### C. Ekspor Data Celah Riset ke Format Analisis
```bash
uv run python scripts/brainstorm_topics.py --cluster all --export
```

---

## 3. Prinsip Formulasi Rumusan Masalah Akademik

1. **Evidence-Based (Berbasis Bukti)**: Hindari klaim asumtif tanpa rujukan. Gunakan data operasional riil atau temuan paper empiris sebelumnya.
2. **Definisi Ruang Lingkup yang Terukur**: Rumusan masalah harus dapat dijawab secara objektif melalui evaluasi empiris (misal: 10 prinsip Heuristik Nielsen dengan severity ratings, 22 butir indikator WebQual 4.0 dimensi Usability, Information Quality, dan Service Interaction Quality).
3. **Penyelarasan Metodologi**: Pendekatan penelitian wajib mengikuti standar baku (User-Centered Design ISO 9241-210:2019 dengan 4 tahapan operasional yang terverifikasi).
