# Panduan Konversi PDF ke Markdown (Marker dengan Akselerasi GPU NVIDIA RTX 4050)

Dokumen ini menjelaskan arsitektur, konfigurasi lingkungan CUDA, dan panduan penggunaan perkakas konversi dokumen PDF ke Markdown (`scripts/convert_pdf_to_md.py`) berbasis library [Marker](https://github.com/VikParuchuri/marker).

---

## 1. Arsitektur & Optimasi GPU NVIDIA RTX 4050

Perkakas ini dikonfigurasi secara khusus untuk memaksimalkan performa **NVIDIA GeForce RTX 4050 Laptop GPU (Ada Lovelace, 6GB VRAM)** yang berjalan di atas Linux Fedora pengguna secara terisolasi tanpa memodifikasi sistem operasi host (*Zero Host Mutation*).

### A. Konfigurasi Presisi FP16 & Pencegahan OOM (*Out-Of-Memory*)
Dengan batasan VRAM 6GB, memproses dokumen berukuran besar (misal skripsi 100+ halaman dengan banyak tabel kompleks) dapat memicu fragmentasi memori CUDA jika menggunakan nilai batch default server 24GB. Optimasi berikut telah diimplementasikan:

1. **Presisi Setengah (FP16)**:
   Model inferensi Marker (`layout_model`, `recognition_model`, `table_rec_model`, `detection_model`, `ocr_error_model`) dimuat dengan tipe data `torch.float16`, menghemat alokasi memori bobot model hingga 50% (~3.3 GB total VRAM).
2. **Segmentasi Dinamis PyTorch (`PYTORCH_CUDA_ALLOC_CONF`)**:
   Diatur ke `expandable_segments:True` untuk mencegah fragmentasi memori virtual CUDA saat pemrosesan gambar beresolusi tinggi.
3. **Adaptive Batch Sizing**:
   - `layout_batch_size = 4`
   - `recognition_batch_size = 8`
   - `encoder_chunk_sizes["cuda"] = 4096`
   - `table_rec_batch_size = 2`
   - `detection_batch_size = 4`
   - `ocr_error_batch_size = 8`
4. **Pembersihan Cache VRAM Otomatis**:
   Fungsi `torch.cuda.empty_cache()` dipanggil secara otomatis sebelum dan sesudah setiap dokumen diproses.

---

## 2. Struktur Penyimpanan Hasil Konversi

Setiap dokumen PDF dikonversi ke direktori terisolasi di `literature/markdowns/<NAMA_DOKUMEN>/`:

```text
literature/markdowns/
└── 2024_Analisis_Penerimaan_Penggunaan_Aplikasi_Fasih.../
    ├── 2024_Analisis_Penerimaan_Penggunaan_Aplikasi_Fasih....md  # Teks Markdown lengkap
    ├── 2024_Analisis_Penerimaan_Penggunaan_Aplikasi_Fasih..._meta.json # Metadata ekstraksi
    ├── _page_0_Picture_4.jpeg                                    # Gambar/diagram terekstraksi
    └── _page_1_Picture_4.jpeg
```

- Tautan gambar di dalam file `.md` menggunakan path relatif (`![](_page_x_Picture_y.jpeg)`) sehingga dokumen dapat langsung dirender dengan sempurna di previewer Markdown manapun (Obsidian, VS Code, GitHub).
- Rumus matematika diformat rapi dalam sintaks LaTeX KaTeX (`$...$` atau `$$...$$`).

---

## 3. Panduan Penggunaan CLI (`scripts/convert_pdf_to_md.py`)

### A. Memeriksa Status & Alokasi GPU
```bash
uv run python scripts/convert_pdf_to_md.py --check-gpu
```
*Output menampilkan nama kartu grafis, kapasitas VRAM total, dan versi CUDA runtime.*

### B. Konversi Satu File PDF Spesifik
```bash
uv run python scripts/convert_pdf_to_md.py --file literature/pdfs/nama_file.pdf
```

### C. Konversi dengan Rentang Halaman Tertentu
Sangat berguna untuk menguji halaman pembuka, bab tertentu, atau sampel abstrak:
```bash
# Rentang halaman (0-indexed)
uv run python scripts/convert_pdf_to_md.py --file literature/pdfs/nama_file.pdf --page-range 0-5
```

### D. Konversi Seluruh Folder PDF (Batch Processing)
Secara default membaca seluruh file `.pdf` di `literature/pdfs/`:
```bash
uv run python scripts/convert_pdf_to_md.py --dir literature/pdfs
```
- Flag `--force`: Memaksa konversi ulang meskipun file `.md` sudah ada sebelumnya.
- Flag `--limit 5`: Membatasi konversi hanya untuk 5 dokumen pertama.

---

## 4. Integrasi Otomatis ke Scraper SIMPus & Paper Internasional

Kedua script scraper telah dihubungkan secara modular ke engine konversi Marker:

### A. SIMPus STIS Scraper (`scripts/scrape_simpus.py`)
Setiap kali skripsi PDF diunduh dan didekripsi:
```bash
# Otomatis download PDF + dekripsi + langsung convert ke Markdown
uv run python scripts/scrape_simpus.py --pdf-query "VAPT"
uv run python scripts/scrape_simpus.py --pdf-id <UUID_SKRIPSI>
```
*Gunakan flag `--no-convert-md` jika hanya ingin menyimpan file PDF biner tanpa konversi Markdown.*

### B. International Literature Scraper (`scripts/scrape_international.py`)
Setiap kali paper Open Access terunduh dari OpenAlex atau arXiv:
```bash
# Otomatis download paper OA + langsung convert ke Markdown
uv run python scripts/scrape_international.py --topic 3 --source arxiv --limit 1 --download-pdf
```
*Gunakan flag `--no-convert-md` jika ingin menonaktifkan konversi otomatis.*

---

## 5. Penggunaan sebagai Modul Python (Programmatic API)

```python
from convert_pdf_to_md import convert_pdf_to_markdown, get_marker_models

# 1. Muat model sekali ke GPU
models = get_marker_models(device="cuda")

# 2. Konversi dokumen
md_path = convert_pdf_to_markdown(
    pdf_path="literature/pdfs/sample.pdf",
    output_base_dir="literature/markdowns",
    page_range=[0, 1, 2],
    models=models,
    skip_existing=True,
)
print("Markdown dihasilkan di:", md_path)
```
