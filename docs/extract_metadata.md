# Dokumentasi Perkakas: Automated Paper Metadata Extractor & BibTeX Generator

Panduan teknis dan operasional untuk modul ekstraksi metadata paper, artikel jurnal, preprint, dan dokumen skripsi lokal Politeknik Statistika STIS secara otomatis, terintegrasi dengan **Crossref REST API**, **Semantic Scholar Graph API**, **OpenAlex API**, dan basis data skripsi lokal STIS (`theses_data.json`).

---

## 1. Ikhtisar & Arsitektur Sistem

Perkakas ini dibangun untuk menjembatani dokumen riset lokal (berupa berkas biner PDF di `literature/pdfs/` maupun hasil konversi Markdown di `literature/markdowns/`) dengan pangkalan data literatur ilmiah bereputasi internasional dan nasional.

```text
[ Berkas Lokal: PDF / Markdown / Subfolder ]
                     │
                     ▼
  ┌────────────────────────────────────────────────────────┐
  │ 1. Document & Identifier Parser                        │
  │  - Ekstraksi DOI & arXiv ID dari metadata / teks PDF   │
  │  - Ekstraksi judul multi-baris dari halaman judul PDF  │
  │  - Ekstraksi heading level-1 & TOC dari Markdown/JSON  │
  │  - Normalisasi nama berkas (sanitized filename)        │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 2. Multi-Provider Academic Resolver                    │
  │  - Crossref API: Resolusi DOI, volume, isu, publisher  │
  │  - Semantic Scholar: Abstrak kaya & citation count     │
  │  - OpenAlex API: Validasi artikel jurnal & preprint    │
  │  - Local STIS Theses DB: Pencocokan 389 skripsi alumni │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 3. Citation & Structured Output Engine                 │
  │  - Official BibTeX via DOI Content Negotiation         │
  │  - Canonical BibTeX Synthesizer (@mastersthesis, dll.) │
  │  - Ekspor terstruktur JSON & CSV di `literature/`      │
  └────────────────────────────────────────────────────────┘
```

### Fitur Utama:
1. **Resolusi Otomatis Dua Arah**:
   - Mendeteksi DOI atau ID arXiv langsung dari metadata PDF atau teks awal halaman 1–3.
   - Jika DOI tidak ditemukan, melakukan pencarian berbasis kemiripan judul (*fuzzy title similarity* & *token overlap containment*).
2. **Local Fallback Skripsi Alumni STIS**:
   - Jika dokumen merupakan skripsi lokal Politeknik Statistika STIS (tanpa DOI komersial), sistem otomatis mencocokkannya ke database `theses_data.json` untuk menghasilkan entri sitasi `@mastersthesis` lengkap dengan nama mahasiswa, dosen pembimbing, peminatan, dan abstrak.
3. **Penyusunan BibTeX Standar**:
   - Mengambil BibTeX resmi langsung dari penerbit via *DOI Content Negotiation* (`Accept: application/x-bibtex`).
   - Membuat entri BibTeX kanonikal sintetis yang rapi untuk skripsi lokal atau paper tanpa BibTeX bawaan.
4. **Format Output Ganda**:
   - `literature/references.bib`: Koleksi referensi standar siap pakai untuk LaTeX/Overleaf/Typst.
   - `literature/extracted_metadata.json`: Skema data terstruktur untuk integrasi modul Python lain.
   - `literature/extracted_metadata.csv`: Spreadsheet ringkas untuk tinjauan literatur cepat.

---

## 2. Cara Menjalankan Perkakas (Quick Start)

Perkakas dapat dijalankan melalui CLI script maupun diimpor sebagai pustaka Python internal:

```bash
# Menjalankan via uv (Direkomendasikan):
uv run python scripts/extract_metadata.py [OPSI]

# Atau via Python lingkungan virtual:
python scripts/extract_metadata.py [OPSI]
```

### Opsi Perintah Utama (CLI Arguments)

| Argumen | Opsi Singkat | Tipe | Nilai Bawaan | Keterangan |
|---|---|---|---|---|
| `--input` | `-i` | String | `None` | Path ke berkas PDF, direktori PDF, berkas Markdown, atau folder Markdown |
| `--doi` | | String | `None` | Menarik metadata dan BibTeX langsung berdasarkan nomor DOI |
| `--title` | | String | `None` | Mencari metadata dan BibTeX langsung berdasarkan judul paper |
| `--output-dir` | `-o` | String | `literature` | Folder penyimpanan hasil (`references.bib`, JSON, CSV) |
| `--bibtex-file`| | String | `references.bib` | Nama berkas BibTeX output |
| `--api` | | Pilihan | `all` | API prioritas: `all`, `crossref`, `semanticscholar`, `openalex` |
| `--recursive`| `-r` | Flag | `False` | Memindai subdirektori secara rekursif (otomatis aktif jika direktori bersarang) |
| `--force` | | Flag | `False` | Memaksa ekstraksi ulang dan menimpa rekaman yang sudah ada di cache |

---

## 3. Contoh Penggunaan Praktis

### A. Ekstraksi Langsung Berdasarkan Nomor DOI
```bash
uv run python scripts/extract_metadata.py --doi 10.1145/3267323.3268949
```
*Mengambil paper ACM Differential Privacy oleh Garfinkel et al., menarik abstrak & citation count dari Semantic Scholar, serta menambahkan sitasi BibTeX resmi ke `literature/references.bib`.*

### B. Memproses Seluruh Koleksi PDF di Folder
```bash
uv run python scripts/extract_metadata.py --input literature/pdfs/
```
*Memproses seluruh berkas PDF (baik paper internasional maupun skripsi alumni STIS), mencocokkan metadata, dan memperbarui basis data JSON, CSV, serta BibTeX.*

### C. Memproses Hasil Konversi Markdown (Folder Bersarang)
```bash
uv run python scripts/extract_metadata.py --input literature/markdowns/
```
*Secara otomatis memindai seluruh folder turunan di `literature/markdowns/`, mengekstrak heading H1 / table of contents `_meta.json`, dan mencatat metadatanya.*

### D. Pencarian Berdasarkan Judul Paper Bebas
```bash
uv run python scripts/extract_metadata.py --title "Zero Trust Architecture NIST"
```

---

## 4. Penggunaan Sebagai Python Module (Programmatic API)

Modul ini telah terdaftar di paket `calm_carson` sehingga dapat diimpor langsung dalam skrip analisis lain:

```python
from calm_carson import extract_paper_metadata, batch_process_documents

# 1. Ekstraksi satu dokumen (PDF / Markdown / DOI):
metadata, bibtex = extract_paper_metadata("literature/pdfs/INTL_2026_trasgoDP_An_Open_Source_Framework_for_Releasing_Noised_Tabular_Microdata_under_L.pdf")

print("Judul   :", metadata["title"])
print("Penulis :", metadata["authors"])
print("Sitasi BibTeX:\n", bibtex)

# 2. Batch processing banyak berkas:
file_list = [
    "literature/pdfs/2024_Analisis_Penerimaan_Penggunaan_Aplikasi_Fasih_dengan_Penerapan_Konsep_Bring_Your.pdf",
    "doi:10.1145/3267323.3268949"
]
records = batch_process_documents(file_list, output_dir="literature")
```

---

## 5. Struktur Penyimpanan & Skema Data Output

### A. Berkas `literature/extracted_metadata.json`
```json
[
  {
    "title": "Issues Encountered Deploying Differential Privacy",
    "authors": "Simson L. Garfinkel, John M. Abowd, Sarah Powazek",
    "year": 2018,
    "venue": "Proceedings of the 2018 Workshop on Privacy in the Electronic Society",
    "doi": "10.1145/3267323.3268949",
    "url": "https://doi.org/10.1145/3267323.3268949",
    "abstract": "When differential privacy was created more than a decade ago...",
    "citation_count": 125,
    "publisher": "ACM",
    "api_source": "Crossref",
    "source_file": "doi:10.1145/3267323.3268949"
  }
]
```

### B. Berkas `literature/references.bib`
```bibtex
@inproceedings{Garfinkel_2018,
  title={Issues Encountered Deploying Differential Privacy},
  author={Garfinkel, Simson L. and Abowd, John M. and Powazek, Sarah},
  booktitle={Proceedings of the 2018 Workshop on Privacy in the Electronic Society},
  DOI={10.1145/3267323.3268949},
  year={2018},
  pages={133–137}
}

@mastersthesis{Desy2024Penerimaan,
  title = {Analisis Penerimaan Penggunaan Aplikasi Fasih dengan Penerapan Konsep Bring Your Own Device (BYOD) pada Kegiatan PL-KUMKM 2023},
  author = {DESY AHYU FITRIA},
  year = {2024},
  school = {Politeknik Statistika STIS},
  note = {Dosen Pembimbing: Yunarso Anang},
  type = {Skripsi Sarjana Terapan Komputasi Statistik, Peminatan Sistem Informasi},
  url = {https://simpus.stis.ac.id/repositori/a9d9f7cd-c926-443c-9034-6604c772c453}
}
```
