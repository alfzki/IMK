# Release Notes: Agentic Research Workflow Toolkit v0.1.0

Selamat datang di rilis perdana **Agentic Research Workflow Toolkit (v0.1.0)**!

Rilis ini menyediakan kerangka kerja riset terotomasi berbasis kecerdasan buatan (AI Agent) dan perkakas baris perintah (CLI) untuk penyusunan naskah penelitian ilmiah universal (makalah konferensi IEEE/ACM, artikel jurnal Scopus/SINTA, proposal penelitian, tesis, dan disertasi). Seluruh arsitektur dibangun di atas prinsip **Zero-Hallucination Directive** dan **Evidence-Grounded Drafting**.

---

## 📦 Komponen yang Disertakan dalam Rilis v0.1.0

### 1. Perkakas CLI & Modul Internal Python (`scripts/` & `src/calm_carson/`)
- **`scrape_international.py`**: Scraper publikasi ilmiah Scopus & OpenAlex API + 9 Open Archives (Semantic Scholar, CORE, Internet Archive, Gutenberg, SciHub, LibGen, Anna's Archive, IPFS, Z-Library) dengan multi-tier downloader.
- **`convert_pdf_to_md.py`**: Konversi PDF artikel ilmiah berakselerasi GPU NVIDIA CUDA (Marker FP16) dengan ekstraksi rumus LaTeX dan tabel.
- **`extract_metadata.py`**: Ekstraksi metadata DOI/arXiv otomatis dan generator master `references.bib`.
- **`hybrid_search.py`**: Mesin temu-balik dokumen hibrida (Hierarchical Chunker, BM25Okapi, Dense CUDA Embeddings, & Reciprocal Rank Fusion).
- **`brainstorm_topics.py`**: Penambang celah penelitian (*research gap mining*) dan pengelompokan tema ilmiah.
- **`check_originality.py`**: Evaluasi orisinalitas dan kebaruan (*novelty score*) secara langsung terhadap ribuan publikasi global OpenAlex & arXiv.
- **`verify_claims.py`**: Auditor keabsahan klaim faktual, deteksi kontradiksi angka kuantitatif (*number-boosted retrieval*), dan validasi integritas sitasi IEEE.
- **`check_ai_style.py`**: Auditor tanda penulisan AI (*Wikipedia:Signs_of_AI_writing*), penertiban em dash PUEBI, klise dwibahasa, dan analisis *burstiness*.
- **`orchestrate_drafting.py`**: Orkestrator penyusunan draf bab demi bab berbasis bukti dengan titik kendali manusia (*human-in-the-loop checkpoint*).
- **`publish_document.py`**: Penerbit dokumen ilmiah format IEEE dua kolom (.docx) dan PDF siap submit (*headless* LibreOffice) dengan *auto-renumbering* sitasi berurutan.
- **`scrape_simpus.py`**: Contoh plugin repositori institusi terenkripsi AES-256.

### 2. Antigravity Skills & Sub-Agen (`.agents/skills/`)
- **`ai-style-auditor`**: Keahlian audit gaya penulisan AI dan penyuntingan akademik.
- **`topic-brainstormer`**: Keahlian perumusan masalah berangka empiris dan metodologi ilmiah.
- **`originality-checker`**: Keahlian telaah kebaruan dan perumusan matriks pembeda (*differentiation strategy*).
- **`claim-verifier`**: Keahlian verifikasi keabsahan data dan integritas sitasi.
- **`research-publisher`**: Keahlian format naskah dan kompilasi terbitan resmi.

### 3. Dokumentasi Teknis Lengkap (`docs/`)
- 11 berkas panduan teknis mendalam untuk setiap modul dan perkakas.
- `QUICKSTART_UNIVERSAL.md`: Panduan cepat 5 tahap penyusunan makalah penelitian universal.
- `INSTRUCTIONS.md`: Konstitusi kerja bebas halusinasi.
- `ARCHITECTURE.md`: Peta sistem, topologi data, dan alur orkestrasi agen.
- `AGENTS.md`: Panduan persona agen riset.

### 4. Jaminan Mutu & Unit Tests (`tests/`)
- 8 berkas test suite otomatis dengan 60 unit tests mencakup seluruh modul (`archives`, `brainstorm`, `drafting`, `originality`, `publisher`, `search`, `style`, `verifier`). Seluruh pengujian lulus 100%.

---

## ⚡ Petunjuk Instalasi Cepat

```bash
# 1. Ekstrak arsip zip rilis:
unzip agentic-research-workflow-v0.1.0.zip -d agentic-research-workflow
cd agentic-research-workflow

# 2. Pasang dependensi menggunakan uv (tanpa menyentuh host OS):
uv sync

# 3. Jalankan unit test untuk memvalidasi instalasi:
uv run python -m unittest discover tests

# 4. Mulai riset Anda mengikuti panduan QUICKSTART_UNIVERSAL.md!
```
