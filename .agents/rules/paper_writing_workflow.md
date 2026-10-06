# Standar Operasional Prosedur (SOP) Penyusunan Artikel Ilmiah HCI & Sistem Informasi

Dokumen aturan ini memandu koordinasi antar-agen, pemanggilan sub-agen, dan eksekusi perkakas teknis dalam perancangan, eksperimentasi usabilitas, penulisan, dan audit artikel ilmiah untuk penelitian **Human-Computer Interaction (HCI / IMK) dan Sistem Informasi (IS)**.

---

## 1. Prinsip Utama & Kebijakan Rujukan Ilmiah

> [!CRITICAL] **LARANGAN PENGGUNAAN SKRIPSI / SIMPUS UNTUK REFERENSI ARTIKEL ILMIAH**:
> Seluruh rujukan ilmiah dalam artikel ilmiah **WAJIB** berasal dari:
> 1. Jurnal ilmiah bereputasi internasional (Scopus Q1–Q4, DOAJ) atau nasional terakreditasi (SINTA 1–4).
> 2. Prosiding konferensi internasional terindeks (IEEE, ACM, Springer, Elsevier).
> 3. Preprint ilmiah resmi bidang Computer Science / Information Systems (arXiv).
> 4. Buku teks ilmiah ber-ISBN dan standar regulasi resmi (ISO, Permen, UU).
>
> **Skripsi alumni dan pangkalan data SIMPUS STIS DILARANG KERAS dijadikan sitasi atau daftar pustaka dalam penulisan artikel ilmiah.**

---

## 2. Matriks Penugasan Sub-Agen & Skill (RACI)

| Peran Sub-Agen | Skill Terkait | Tugas Utama & Akuntabilitas |
| :--- | :--- | :--- |
| **`hci_evaluator`** | Evaluasi & Desain UI/UX | Melakukan audit Heuristik 10 Prinsip Nielsen, perancangan prototipe User-Centered Design (UCD ISO 9241-210), komparasi antarmuka Before & After, serta analisis dimensi WebQual 4.0 / SUS / UEQ. |
| **`literature_researcher`** | `paper-reference-rag` | Menggali sitasi terverifikasi, kutipan bukti empiris, dan perbandingan performa (*benchmark*) dari katalog paper peer-reviewed lokal (`references/markdown/`). |
| **`evidence_retriever`** | `claim-reference-finder` | Mencari paper peer-reviewed baru via OpenAlex, Crossref, arXiv, Semantic Scholar (`scripts/search_academic_papers.py`), mengunduh PDF open-access, dan melakukan ingesti otomatis ke local RAG & BibTeX. |
| **`academic_writer`** | Pedoman Template & Gaya Bahasa | Menyusun draf per seksi (Pendahuluan, Tinjauan Pustaka/Landasan Teori, Metodologi UCD & Evaluasi, Hasil & Pembahasan Before-After, Kesimpulan) dengan gaya bahasa ilmiah Indonesia/Inggris alami, presisi, dan bebas klise AI. |
| **`paper_auditor`** | `paper-auditor` | Menguji draf secara ketat via `scripts/audit_paper_draft.py` untuk membuktikan *grounding* klaim, integritas daftar pustaka, kepatuhan template, eliminasi diksi robotik AI, serta konsistensi angka temuan evaluasi. |

---

## 3. Alur Kerja 5 Tahapan Sistematis (*5-Stage Pipeline*)

```
[Tahap 1: Evidence Mining]
      │  Mencari telaah usabilitas, prinsip HCI, & instrumen WebQual dari paper peer-reviewed
      ▼
[Tahap 2: Empirical Evaluation & Prototyping]
      │  Audit Heuristik Nielsen (Kondisi Eksisting / Before)
      │  Perancangan ulang UCD (Wireframe & Prototipe High-Fidelity di Figma / After)
      │  Pengukuran kuantitatif kuesioner WebQual 4.0 / USE / SUS
      ▼
[Tahap 3: Compliant Scientific Drafting]
      │  academic_writer menyusun naskah sesuai Template Makalah IMK
      │  Integrasi angka evaluasi riil, komparasi Before-After, & sitasi resmi
      ▼
[Tahap 4: Multi-Pillar Quality Gate]
      │  paper_auditor mengeksekusi scripts/audit_paper_draft.py --strict
      │  Zero-tolerance: Ungrounded Claims = 0, SIMPUS Cites = 0, AI Cliches = 0
      ▼
[Tahap 5: Finalization, DOCX Export & Zotero Sync]
         Kompilasi ke Word (.docx) via scripts/export_to_docx.py
         Sinkronisasi referensi ke Zotero Desktop via prepare_zotero_import.py
```

---

## 4. Ketentuan Teknis Penulisan Draf

1. **Judul Artikel**: Maksimum 12 kata dalam bahasa Indonesia sesuai `Template Makalah IMK.docx`, lugas, spesifik, mencerminkan kontribusi evaluasi/redesain.
2. **Abstrak**: Maksimal 200 kata berbahasa Indonesia dan Inggris (cetak miring), memuat latar belakang masalah, metode (UCD & WebQual 4.0), ringkasan hasil sebelum vs sesudah, serta simpulan. Dilarang memuat sitasi dan rumus matematis. 3–5 kata kunci.
3. **Pendahuluan**: Menguraikan latar belakang permasalahan darurat/pelayanan publik, urgensi waktu tanggap (SPM), temuan awal kelemahan usabilitas heuristik, rumusan masalah, tujuan penelitian, dan telaah riset terdahulu yang relevan.
4. **Metodologi**: Memaparkan landasan teori (10 Prinsip Heuristik Nielsen, UCD ISO 9241-210, dimensi WebQual 4.0), subjek/responden penelitian, teknik pengumpulan data kuesioner, alur perancangan prototipe interaktif, dan metode analisis komparasi Before & After.
5. **Hasil dan Pembahasan**:
   - Memuat temuan rinci pelanggaran Heuristik pada sistem eksisting (Before).
   - Memaparkan solusi desain prototipe hasil redesain (After) untuk modul utama.
   - Menyajikan analisis Before & After sesuai format Sub-CPMK 8 dan 9 (Expressive Interface, Emotional Design, Information Search, Timely UX, Visualisasi).
   - Analisis kuantitatif peningkatan skor WebQual 4.0 (Usability, Information, Service Interaction Quality).
   - Dialog temuan terhadap riset usabilitas e-government internasional terkait.
6. **Kesimpulan dan Saran**: Ditulis dalam bentuk narasi atau pointer menjawab tujuan penelitian, memuat kelebihan dan keterbatasan prototipe, serta saran aplikatif untuk instansi terkait.
7. **Eliminasi Klise AI**:
   - Dilarang menggunakan pembuka klise (*"Di era modern ini", "Dalam lanskap yang dinamis", "Perlu dicatat bahwa"*).
   - Dilarang menggunakan frasa filler (*"memainkan peran penting", "interaksi rumit", "titik balik krusial", "menyelami"*).
   - Dilarang menggunakan bahasa promotif (*"berhasil memangkas", "mendongkrak", "secara dramatis", "sangat direkomendasikan"*).
   - Tanda pisah *em dash* (—) wajib rapat tanpa spasi sesuai EYD V.
