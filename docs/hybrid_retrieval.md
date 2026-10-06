# Dokumentasi Perkakas: Hybrid Retrieval System (Dense Semantic + Sparse BM25)

Panduan teknis dan operasional untuk sistem penelusuran hibrida (*Hybrid Retrieval System*) pada korpus dokumen Markdown di workspace `calm-carson`. Sistem ini memadukan pencarian semantik vektor (*dense embedding*) dan pencarian kata kunci (*sparse BM25Okapi*) dengan algoritma fusi *Reciprocal Rank Fusion* (RRF).

---

## 1. Arsitektur & Prinsip Desain

```text
                 [ Korpus Dokumen Markdown (28 Berkas) ]
                (proposals/, literature/, brainstorming/, docs/)
                                    │
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │ 1. Hierarchical Markdown Chunker                       │
       │  - Heading stack tracker (# H1 > ## H2 > ### H3)       │
       │  - Contextual breadcrumbs injection per chunk          │
       │  - Boundary-aware splitting (paragraf, tabel, daftar)  │
       └────────────────────────────┬───────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
       ┌────────────────────────┐      ┌────────────────────────┐
       │ 2. Dense Vector Index  │      │ 3. Sparse BM25 Index   │
       │  - paraphrase-         │      │  - Custom Tokenizer    │
       │    multilingual-MiniLM │      │  - Technical terms     │
       │  - PyTorch CUDA (FP16) │      │  - Stopwords filtering │
       │  - L2-normalized 384d  │      │  - BM25Okapi scoring   │
       │  - Embeddings .npy     │      │  - JSON inverted index │
       └────────────┬───────────┘      └────────────┬───────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │ 4. Hybrid Fusion Engine                                │
       │  - Reciprocal Rank Fusion (RRF, k=60)                  │
       │  - Directory & metadata filtering                      │
       │  - SQLite Database (`literature/search_index/index.db`)│
       └────────────────────────────┬───────────────────────────┘
                                    ▼
       ┌────────────────────────────────────────────────────────┐
       │ 5. Antarmuka Pencarian & API                           │
       │  - CLI Runner: `scripts/hybrid_search.py`              │
       │  - Python Library: `calm_carson.search`                │
       └────────────────────────────────────────────────────────┘
```

### Keunggulan Utama:
1. **Hierarchical Breadcrumbs**:
   Setiap potongan teks (*chunk*) mempertahankan silsilah heading dari bab hingga sub-bab terdalam, contoh:
   `[Konteks: proposal_topik_2_sdi_gateway.md > Rancang Bangun Secure Ingestion Gateway... > V. Metodologi Penelitian > A. Desain dan Pendekatan Penelitian]`. Hal ini mencegah hilangnya konteks ketika model membaca potongan teks yang pendek.
2. **Dense Semantic Search (Multilingual CUDA)**:
   Menggunakan model `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (384 dimensi) yang dioptimasi untuk komputasi CUDA FP16 pada GPU NVIDIA RTX 4050. Mampu mengenali kesamaan makna dalam Bahasa Indonesia dan Bahasa Inggris secara konseptual.
3. **Sparse BM25Okapi Search**:
   Menangani akronim dan istilah teknis spesifik (*domain-specific terminology*) seperti `VAPT`, `SIPADU-NG`, `SIMWAS`, `CAPI`, `SDI`, `BYOD`, `AHP-TOPSIS`, `ISO-25010`, `SHA-256`, dan `trasgoDP`.
4. **Reciprocal Rank Fusion (RRF)**:
   Menggabungkan urutan peringkat kandidat dari pencarian padat (*dense*) dan jarang (*sparse*) menggunakan rumus kanonikal:
   $$RRF(d) = \frac{w_{dense}}{k + rank_{dense}(d)} + \frac{w_{sparse}}{k + rank_{sparse}(d)}$$
   dengan nilai standar $k=60$ dan bobot seimbang $w_{dense} = 0.5, w_{sparse} = 0.5$.

---

## 2. Penggunaan Melalui Baris Perintah (CLI)

Perkakas utama tersedia di [`scripts/hybrid_search.py`](../scripts/hybrid_search.py) dan telah dilengkapi mekanisme *auto-bootstrap virtual environment*:

```bash
# Menjalankan via uv (Sangat direkomendasikan):
uv run python scripts/hybrid_search.py [OPSI]
```

### Opsi Perintah Utama

| Argumen | Opsi Singkat | Tipe | Nilai Bawaan | Keterangan |
|---|---|---|---|---|
| `--query` | `-q` | String | `None` | Kueri pencarian bebas (pertanyaan/istilah) |
| `--top-k` | `-k` | Integer | `5` | Jumlah potongan teks teratas yang ditampilkan |
| `--mode` | `-m` | Pilihan | `hybrid` | Metode pencarian: `hybrid`, `dense`, `sparse` |
| `--filter-dir`| `-f` | String | `None` | Membatasi hasil ke folder tertentu (misal `proposals`) |
| `--index` / `--reindex` | | Flag | `False` | Membangun ulang indeks seluruh dokumen Markdown |
| `--stats` | | Flag | `False` | Menampilkan ringkasan statistik database indeks |

---

## 3. Contoh Skenario Pencarian Praktis

### A. Membangun / Memperbarui Indeks Korpus
```bash
uv run python scripts/hybrid_search.py --reindex
```
*Memindai 28 berkas Markdown di `proposals/`, `literature/`, `brainstorming/`, dan `docs/`, menghasilkan 699 chunks, dan menyimpannya di `literature/search_index/`.*

### B. Pencarian Istilah Teknis & Audit Keamanan
```bash
uv run python scripts/hybrid_search.py --query "celah keamanan VAPT RESTful API SIPADU-NG" --top-k 3
```

### C. Pencarian Metodologi dengan Filter Direktori
```bash
uv run python scripts/hybrid_search.py --query "tahapan metodologi DSRM Peffers" --filter-dir proposals --top-k 2
```

### D. Pencarian Konseptual Privasi Data
```bash
uv run python scripts/hybrid_search.py --query "dynamic privacy budgeting audit trail SHA-256 UU PDP" --top-k 2
```

### E. Memeriksa Status Indeks
```bash
uv run python scripts/hybrid_search.py --stats
```

---

## 4. Penggunaan Sebagai Python Module (Programmatic API)

Modul ini terdaftar pada pustaka internal `calm_carson.search` sehingga dapat langsung dimanfaatkan dalam modul analisis dan agen asisten:

```python
from calm_carson.search import MarkdownHybridSearchEngine

# Inisialisasi mesin pencari
engine = MarkdownHybridSearchEngine()

# Menjalankan kueri hybrid
results = engine.search(
    query="analisis celah OWASP API Top 10",
    top_k=3,
    mode="hybrid",
    filter_dir="literature",
)

for r in results:
    print(f"[{r.rrf_score:.4f}] {r.doc_path} ({r.breadcrumb})")
    print(r.raw_content[:200])
    print("-" * 50)
```

---

## 5. Menjalankan Automated Tests

Seluruh fungsionalitas diuji secara otomatis melalui test suite `tests/test_hybrid_search.py`:

```bash
uv run python -m unittest discover tests -v
```
Pengujian mencakup:
1. `TestHierarchicalMarkdownChunker`: Pemeliharaan tumpukan heading dan breadcrumbs kontekstual.
2. `TestBM25Index`: Tokenizer istilah teknis gabungan dan perangkingan kata kunci eksak.
3. `TestDenseEmbeddingEngine`: Vektorisasi semantik dan pencarian kosinus dot-product.
4. `TestHybridSearchEngine`: Pengujian end-to-end RRF fusion dan filter direktori.
