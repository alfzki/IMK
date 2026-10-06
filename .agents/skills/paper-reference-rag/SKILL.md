---
name: paper-reference-rag
description: >-
  Retrieve, search, and synthesize citations and evidence from verified peer-reviewed research papers
  for human-computer interaction (HCI), usability evaluation, WebQual 4.0, and information systems.
  Use when writing research papers (Introduction, Methodology, Results & Discussion)
  to generate BibTeX citekeys, extract empirical benchmarks, or query literature via Zotero MCP and local RAG.
  NOTE: SIMPUS theses are strictly disabled. Only peer-reviewed publications are indexed.
---

# Paper Reference RAG & Zotero Citation Guide for HCI & Information Systems Research

Skill ini menyediakan prosedur temu-balik literatur, ekstraksi bukti empiris pembanding (*benchmarks*), serta sitasi dari pangkalan paper terverifikasi untuk artikel ilmiah Interaksi Manusia dan Komputer (HCI) dan Sistem Informasi.

---

## 1. Strategi Temu-Balik Literatur (Retrieval Strategies)

### Strategi A: Local Full-Text RAG Engine (`scripts/query_references.py`)
Tersedia offline secara cepat tanpa dependensi internet:
- **Pencarian teks lengkap & potongan seksi:**
  ```bash
  uv run python scripts/query_references.py --query "User-Centered Design WebQual" --limit 5
  ```
- **Filter berdasarkan judul seksi (Metodologi, Hasil, Diskusi):**
  ```bash
  uv run python scripts/query_references.py --query "heuristic evaluation" --section "method"
  ```
- **Rincian lengkap paper & format sitasi:**
  ```bash
  uv run python scripts/query_references.py --citekey "<citekey_or_id>"
  ```
- **Rekomendasi paper berdasarkan tema:**
  ```bash
  uv run python scripts/query_references.py --suggest webqual
  # Tema tersedia: ucd, webqual, heuristic, usability, government_portal, information_architecture, emotional_design
  ```
- **Tabel komparasi seluruh paper terverifikasi:**
  ```bash
  uv run python scripts/query_references.py --compare
  ```

### Strategi B: Zotero MCP Tools (Saat Zotero Desktop Aktif)
Ketika aplikasi Zotero desktop aktif pada localhost:
- `zotero_search_items(query, query_mode="everything")`: Menelusuri seluruh koleksi teks dan catatan.
- `zotero_item_metadata(item_key)`: Mengambil metadata sitasi lengkap dan DOI.
- `zotero_item_fulltext(item_key)`: Membaca teks utuh paper langsung dari repositori Zotero.

---

## 2. Pemetaan Literatur per Bagian Artikel Ilmiah

| Bagian Artikel | Tema Literatur Utama | Contoh Paper Rujukan & ID / Citekey |
| :--- | :--- | :--- |
| **Pendahuluan** | Kualitas portal e-government; Urgensi kanal darurat; Hambatan navigasi; Beban kognitif darurat | `Falconi2023Navigating`<br>`Jalil2023Quality`<br>`TejedoRomero2025Usability`<br>`Alexander2021Influence` |
| **Tinjauan Pustaka** | Kerangka kerja evaluasi usabilitas multi-metode; Dimensi WebQual 4.0; Standar ISO 9241 | `BarnesVidgen2002WebQual`<br>`Chairani2024WebQual`<br>`Raposo2026Multimethod`<br>`Wardhana2024ModelWebQual` |
| **Metodologi** | Alur User-Centered Design (UCD) 4 tahap; Heuristic Evaluation 10 prinsip Nielsen; Skala WebQual 4.0 & IPA | `Ramadhan2022UIUX`<br>`Adiwinata2024Penerapan`<br>`Bastardo2024Methodological`<br>`Burch2025CoDesigning` |
| **Hasil & Pembahasan** | Analisis Before vs After; Skor WebQual 4.0; Kepuasan pengguna; Evaluasi interaksi dinamis | `Maryani2023WebQual`<br>`Hafif2025WebQual`<br>`Safitri2024From`<br>`Pusnik2026Evaluating` |

---

## 3. Panduan Format Sitasi Baku

Ketika menyusun naskah artikel ilmiah:
1. **Format APA (Edisi ke-7)** (Sesuai `Template Makalah IMK.docx`):
   - Narasi Bahasa Indonesia: `Ramadhan dkk. (2022)` atau `Chairani dan Baroroh (2024)`
   - Narasi Bahasa Inggris: `Falconi et al. (2023)`
   - Di dalam kurung (*parenthetical*): `(Ramadhan dkk., 2022)` atau `(Falconi et al., 2023)`
2. **Format IEEE**:
   - Penomoran numerik berurutan di dalam tanda kurung siku: `[1]`, `[2]`, `[3]–[5]`
3. **Kaidah Grounding & Anti-Halusinasi**:
   - Pastikan setiap kalimat ber-sitasi didukung oleh fakta riil di `references/markdown/<citekey>/<citekey>.md`.
   - Dilarang mengarang metrik, angka sampel, atau kesimpulan yang tidak ada dalam paper sumber.
   - Jalankan `uv run python scripts/audit_paper_draft.py --file drafts/<naskah>.md --strict` sebelum menyerahkan draf.
