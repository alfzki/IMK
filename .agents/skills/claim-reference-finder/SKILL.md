---
name: claim-reference-finder
description: >-
  Search and retrieve scientific peer-reviewed literature for unverified research claims in Human-Computer
  Interaction (HCI), Usability, WebQual 4.0, and Information Systems papers using academic search CLI
  (arXiv, Crossref, OpenAlex, Semantic Scholar), download open-access PDFs, and automatically ingest them into
  Zotero and the local RAG repository. Use when an academic claim in a draft is ungrounded ([KLAIM_BELUM_TERVERIFIKASI])
  or when new empirical evidence is needed to substantiate assertions in HCI and Information Systems papers.
  NOTE: SIMPUS skripsi theses are strictly disallowed as scientific references.
---

# Claim Reference Finder & Academic Paper Ingestion Guide

Skill ini digunakan untuk mencari rujukan ilmiah resmi bagi klaim yang belum terbukti atau bertanda `[KLAIM_BELUM_TERVERIFIKASI]`, mengunduh berkas paper primer peer-reviewed (jurnal/konferensi/preprint bereputasi), serta memasukkannya secara otomatis ke dalam **Zotero** dan **Local RAG Engine**.

> [!CRITICAL] **ATURAN MUTLAK SUMBER REFERENSI**:
> Seluruh rujukan ilmiah **WAJIB** berasal dari jurnal ilmiah bereputasi (Scopus/SINTA), prosiding konferensi internasional (IEEE, ACM, Springer), buku akademik ber-ISBN, atau preprint terindeks (arXiv).
> **Skripsi alumni dan repositori SIMPUS STIS DILARANG KERAS dijadikan sitasi dalam artikel ilmiah.**

---

## 1. Alur Kerja Resolusi Klaim Tanpa Bukti (Evidence Gap Resolution)

```
[Draf Naskah Artikel Ilmiah]
      │
      ▼
audit_paper_draft.py  ───► Terdeteksi [KLAIM_BELUM_TERVERIFIKASI] / [SUMBER_TIDAK_TERDAFTAR]
      │
      ▼
Formulasi Query Akademik (Inggris/Indonesia: Domain HCI, UCD, WebQual 4.0, Usability, Evaluasi)
      │
      ▼
Pencarian Literatur Peer-Reviewed (OpenAlex, Crossref, arXiv, Semantic Scholar)
      │
      ▼
Unduh PDF Open Access Resmi (via download_with_fallback / Unpaywall / Penerbit)
      │
      ▼
ingest_new_reference.py  ───► Simpan ke references/papers/<citekey>.pdf
                               Ekstrak teks ke references/markdown/<citekey>/<citekey>.md
                               Daftarkan ke references/verified_papers.json
                               Perkaya literature/references.bib & references_zotero_import.bib
      │
      ▼
Revisi Draf Naskah  ───► Masukkan sitasi APA/IEEE yang valid & kutipan faktual
      │
      ▼
audit_paper_draft.py  ───► Verifikasi Ulang: Status Lolos (VERIFIED)!
```

---

## 2. Cara Mencari Paper Menggunakan CLI Proyek

Gunakan alat bantu pencarian multi-platform [`scripts/search_academic_papers.py`](file:///home/alfzki/Documents/IMK/scripts/search_academic_papers.py):

```bash
# 1. Pencarian di arXiv (Preprint CS / Human-Computer Interaction)
uv run python scripts/search_academic_papers.py --query "human-computer interaction usability evaluation government" --platform arxiv --limit 3

# 2. Pencarian di Crossref (Jurnal Penerbit Luas: Elsevier, Springer, IEEE, ACM)
uv run python scripts/search_academic_papers.py --query "WebQual 4.0 website quality user satisfaction" --platform crossref --limit 3

# 3. Pencarian di OpenAlex (Metadata Ilmiah Global Terlengkap)
uv run python scripts/search_academic_papers.py --query "user-centered design emergency public portal" --platform openalex --limit 3

# 4. Pencarian dan Langsung Ingesti Otomatis (misal paper hasil ke-1)
uv run python scripts/search_academic_papers.py --query "heuristic evaluation website redesign government portal" --platform openalex --auto-ingest 1
```

---

## 3. Pipeline Ingesti ke Zotero & Local RAG

Jalankan perintah ingesti untuk mendaftarkan paper baru:
```bash
uv run python scripts/ingest_new_reference.py \
  --pdf "https://example.org/path/to/paper.pdf" \
  --title "Evaluating Emergency Service Public Portals: A User-Centered Design and Usability Study" \
  --author "Falconi, A. and Martinez, R." \
  --year 2024 \
  --journal "International Journal of Human-Computer Studies" \
  --doi "10.1016/j.ijhcs.2024.103211" \
  --methods "User-Centered Design, Heuristic Evaluation, Usability Testing" \
  --relevance "Membahas perancangan antarmuka portal kebencanaan darurat dan mitigasi beban kognitif warga."
```

### Efek Otomatis dari Perintah Ingesti:
1. **Penyimpanan Berkas PDF:** Tersimpan di `references/papers/<citekey>.pdf`.
2. **Indeks RAG Lokal:** Teks diekstrak ke `references/markdown/<citekey>/<citekey>.md` sehingga langsung dapat ditelusuri oleh `scripts/query_references.py`.
3. **Pembaruan Database Terverifikasi:** Metadata resmi didaftarkan ke `references/verified_papers.json` sehingga paper otomatis menjadi sumber terdaftar yang sah (mencegah bendera `[SUMBER_TIDAK_TERDAFTAR]`).
4. **Sinkronisasi BibTeX & Zotero:** Entri BibTeX lengkap ditambahkan ke `literature/references.bib` dan `references/references_zotero_import.bib`.
5. **Validasi Anti-SIMPUS:** Skrip secara otomatis menolak ingesti jika sumber merupakan skripsi atau repositori SIMPUS.

---

## 4. Memperbarui Naskah & Verifikasi Akhir

Setelah paper di-ingest:
1. **Periksa Teks Asli untuk Kutipan:**
   ```bash
   uv run python scripts/query_references.py --citekey "<citekey>"
   ```
2. **Tuliskan Fakta Empiris:** Ganti klaim yang belum terbukti dengan kalimat yang memuat bukti riil dari paper tersebut dan cantumkan sitasi resmi:
   - Sitasi APA: `NamaPenulis dkk. (Tahun)` atau `(NamaPenulis dkk., Tahun)`
   - Sitasi IEEE: `[X]`
3. **Audit Ulang Draf:**
   ```bash
   uv run python scripts/audit_paper_draft.py --file drafts/<nama_file>.md --strict
   ```
   Pastikan klaim sekarang berstatus `VERIFIED` tanpa bendera ungrounded!
