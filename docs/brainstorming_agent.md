# Panduan Sistem: Kapabilitas Brainstorming & Sub-Agen Analisis Celah Riset

Dokumen ini memuat arsitektur teknis, panduan CLI, struktur data terstandar, dan panduan penggunaan sub-agen `topic_brainstormer` untuk menambang kesenjangan penelitian (*research gaps*), batasan metodologi (*limitations*), dan arahan riset lanjutan (*future work*) dari korpus lokal skripsi STIS dan paper internasional.

---

## 1. Arsitektur Pipeline Ekstraksi & Sintesis

Sistem mengintegrasikan korpus teks lokal (skripsi STIS, paper internasional, dan dokumen proposal) dengan mesin ekstraksi cerdas dan antarmuka sub-agen:

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             KORPUS DOKUMEN LOKAL                                 │
│  - 389 Skripsi Alumni STIS (literature/theses_data.json)                         │
│  - Berkas Markdown Hasil Konversi Marker GPU (literature/markdowns/)             │
│  - Katalog Review Paper Internasional (literature/topik_*_reviews.md)            │
│  - Proposal & Matriks Penelitian (proposals/ & brainstorming/)                   │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   RESEARCH GAP EXTRACTOR (extractor.py)                          │
│  1. Abstract Pattern Miner: Deteksi kalimat limitasi & saran via pola linguistik │
│  2. Markdown Section Extractor: Deteksi heading Limitations, Future Work, dll.   │
│  3. Hybrid Retrieval Hook: Pencarian celah konsep terarah via RRF & BM25        │
│  4. Cluster Classifier: Klasifikasi berbobot ke 5 Klaster Utama SIS STIS        │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   BRAINSTORM SYNTHESIZER (synthesizer.py)                        │
│  - Pengelompokan ke Taksonomi 3 Pilar:                                           │
│    1. Masalah Terbuka (Open Problems di BPS / Lapangan)                          │
│    2. Keterbatasan Metodologi (Methodological Bottlenecks sistem terdahulu)      │
│    3. Peluang Penelitian Baru (Novel Research Opportunities sesuai DSRM SIS)     │
│  - Matriks Komparasi Strategis (Pola Terdahulu vs Bottleneck vs Solusi Rekayasa) │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
┌──────────────────────────────────────┐  ┌────────────────────────────────────────┐
│     STRUKTUR DATA & LAPORAN EKSPOR   │  │       SUB-AGEN INTERAKTIF              │
│  - literature/brainstorming_gaps.json│  │   'topic_brainstormer'                 │
│  - literature/brainstorming_gaps.csv │  │  - Academic Sparring Partner           │
│  - brainstorming/peta_peluang_riset.md  │  - Dialog validasi ide DSRM STIS      │
│  - CLI: scripts/brainstorm_topics.py │  │  - Cek irisan skripsi kakak tingkat    │
└──────────────────────────────────────┘  └────────────────────────────────────────┘
```

---

## 2. Skema Data Terstruktur

Setiap temuan kesenjangan dimodelkan dalam dataclass `ResearchGapItem` dengan representasi JSON dan CSV berikut:

### Format JSON (`literature/brainstorming_gaps.json`)
```json
{
  "id": "gap_stis_cf939a3b_fw",
  "source_type": "stis_thesis",
  "source_title": "Pembangunan Sistem Informasi Survei Harga Konsumen BPS Provinsi DKI Jakarta",
  "year": "2024",
  "author": "Muhammad Rayyan Maulana",
  "cluster": "data_collection_capi",
  "gap_category": "future_work",
  "raw_excerpt": "Beberapa saran untuk penelitian selanjutnya termasuk perbaikan tampilan dan penambahan fitur untuk melihat detail per pencacah bagi pengawas.",
  "synthesized_summary": "Saran riset lanjutan dari skripsi alumni (Muhammad Rayyan Maulana, 2024): Beberapa saran untuk penelitian selanjutnya termasuk perbaikan tampilan...",
  "recommended_opportunity": "Mengintegrasikan enkripsi data mikro terisolasi pada database lokal SQLite perangkat pencacah CAPI serta automated integrity verification saat transmisi sinkronisasi.",
  "source_location": "literature/theses_data.json#cf939a3b-80ea-44be-a989-9477fe417272",
  "metadata": {
    "advisor": "Neli Agustina",
    "peminatan": "Sistem Informasi",
    "no_induk": "222011504/2023"
  }
}
```

### Kategori Kesenjangan (*Gap Category*):
- `open_problem`: Masalah nyata di instansi statistik (BPS/Kementerian/Lembaga) yang belum terselesaikan.
- `methodological_bottleneck`: Keterbatasan algoritma, arsitektur, atau keamanan sistem pada penelitian sebelumnya (misal: proses batch offline tanpa real-time, validasi manual tanpa AI, minimnya enkripsi data lokal).
- `future_work`: Saran atau rekomendasi eksplisit yang dituliskan oleh penulis skripsi/paper untuk dilanjutkan oleh peneliti berikutnya.

---

## 3. Penggunaan Antarmuka Baris Perintah (CLI Runner)

Skrip [`scripts/brainstorm_topics.py`](file:///home/alfzki/Documents/antigravity/calm-carson/scripts/brainstorm_topics.py) dapat dieksekusi langsung di terminal:

### A. Melihat Statistik Sebaran Gap Riset
```bash
uv run python scripts/brainstorm_topics.py --stats
```

### B. Menganalisis Klaster Tertentu
```bash
# Klaster Keamanan & Privasi Data Mikro
uv run python scripts/brainstorm_topics.py --cluster security_privacy

# Klaster Satu Data Indonesia & Interoperabilitas
uv run python scripts/brainstorm_topics.py --cluster sdi_interoperability

# Klaster Pengumpulan Data Cerdas (CAPI/CAWI)
uv run python scripts/brainstorm_topics.py --cluster data_collection_capi
```

### C. Penelusuran Kesenjangan Berdasarkan Konsep Spesifik (Hybrid Search)
```bash
uv run python scripts/brainstorm_topics.py --query "differential privacy SQL"
uv run python scripts/brainstorm_topics.py --query "VAPT API microservices"
```

### D. Ekspor Lengkap ke JSON, CSV, dan Markdown
```bash
uv run python scripts/brainstorm_topics.py --cluster all --export
```

Berkas keluaran otomatis disimpan di:
1. [`literature/brainstorming_gaps.json`](file:///home/alfzki/Documents/antigravity/calm-carson/literature/brainstorming_gaps.json)
2. [`literature/brainstorming_gaps.csv`](file:///home/alfzki/Documents/antigravity/calm-carson/literature/brainstorming_gaps.csv)
3. [`brainstorming/peta_peluang_riset.md`](file:///home/alfzki/Documents/antigravity/calm-carson/brainstorming/peta_peluang_riset.md)

---

## 4. Penggunaan Sub-Agen `topic_brainstormer`

Sub-agen `topic_brainstormer` dapat dipanggil kapan saja oleh agen utama menggunakan tool `invoke_subagent` untuk mendampingi sesi diskusi bersama mahasiswa:

### Contoh Pemanggilan Sub-Agen:
```python
invoke_subagent(
    Subagents=[{
        "TypeName": "topic_brainstormer",
        "Role": "Academic Sparring Partner",
        "Prompt": (
            "Saya tertarik pada topik keamanan API Satu Data Indonesia dan validasi metadata "
            "statistik otomatis. Bantu saya memeriksa apakah ada skripsi alumni STIS yang serupa, "
            "identifikasi celah riset yang ditinggalkan, dan rumuskan usulan novelty berbasis DSRM."
        )
    }]
)
```

### Kemampuan Respons Sub-Agen:
1. **Pengecekan Duplikasi**: Memeriksa pangkalan data 389 skripsi alumni STIS untuk memastikan ide mahasiswa tidak menduplikasi skripsi terdahulu.
2. **Kesesuaian Standar D-IV SIS**: Memastikan usulan berbobot rekayasa sistem informasi statistik (bukan CRUD biasa dan bukan Sains Data murni).
3. **Penyusunan Masalah Kuantitatif**: Membantu menyusun minimal 3 masalah riil berangka empiris untuk latar belakang proposal penelitian.

---

## 5. Penggunaan via Python API

Modul dapat diimpor langsung ke dalam skrip atau modul lain:

```python
from calm_carson.brainstorm import (
    ResearchGapExtractor,
    BrainstormSynthesizer,
    BrainstormExporter,
    run_brainstorm_pipeline,
)

# Menjalankan seluruh alur dalam satu baris
items, summaries = run_brainstorm_pipeline(cluster_filter="security_privacy", export_files=True)

for opp in summaries["security_privacy"].synthesized_opportunities:
    print(f"Peluang Baru: {opp}")
```

---

## 6. Pengujian Unit

Pengujian unit otomatis tersedia di [`tests/test_brainstormer.py`](file:///home/alfzki/Documents/antigravity/calm-carson/tests/test_brainstormer.py):

```bash
uv run python -m unittest tests/test_brainstormer.py
```
Seluruh 5 skenario uji memvalidasi ekstraksi heuristik kalimat abstrak, ekstraksi heading Markdown, klasifikasi klaster, serta integritas data ekspor JSON, CSV, dan Markdown.
