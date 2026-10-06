# AGENTS.md - Panduan Agen & Aturan Naskah Artikel Ilmiah IMK

Dokumen ini berisi konfigurasi, pedoman kerja, aturan mutlak, peran, dan konteks bagi AI Agent dalam mendampingi penyusunan dan pemeliharaan naskah artikel ilmiah mata kuliah **Interaksi Manusia dan Komputer (IMK)** di Politeknik Statistika STIS.

---

## 1. Konteks Tim Peneliti & Institusi

- **Kampus**: Politeknik Statistika STIS ([stis.ac.id](https://www.stis.ac.id))
- **Program Studi**: Diploma IV (D-IV) Komputasi Statistik
- **Mata Kuliah**: Interaksi Manusia dan Komputer (IMK)
- **Tim Penulis (Kelompok 8)**:
  1. **Alif Zakiansyah As Syauqi** (NIM: 222312958 | Email: `222312958@stis.ac.id`)
  2. **Andrian Fajar Fahmi** (NIM: 222312979 | Email: `222312979@stis.ac.id`)
  3. **Valentina Lasma Situmorang** (NIM: 222313413 | Email: `222313413@stis.ac.id`)
- **Target Capaian**: Menghasilkan artikel ilmiah standar publikasi akademik yang lolos audit mutu 6 pilar, bebas halusinasi, dan sesuai dengan template resmi makalah IMK.
- **Topik Riset Utama**:  
  *"Redesain Website Dinas Pemadam Kebakaran Kota Bandar Lampung dengan Pendekatan User-Centered Design"*  
  (Objek Kajian: Portal Resmi Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung — `damkar.bandarlampungkota.go.id`).

---

## 2. Karakteristik & Ruang Lingkup Riset HCI / IMK

Penelitian ini berada dalam domain **Interaksi Manusia dan Komputer (*Human-Computer Interaction* / HCI)** yang berfokus pada evaluasi kegunaan (*usability evaluation*), perancangan pengalaman pengguna (*User Experience* / UX), rekayasa antarmuka portal layanan publik kedaruratan (*emergency public portal*), dan mitigasi beban kognitif masyarakat dalam situasi krisis.

### A. Empat Pilar Metodologi Utama
1. **Heuristic Evaluation (10 Prinsip Jakob Nielsen)**:
   - Audit inspeksi usabilitas awal secara mendalam pada website eksisting (*Before*).
   - Pengklasifikasian masalah usabilitas berdasarkan skala tingkat keparahan (*Severity Ratings* 0–4: *Cosmetic, Minor, Major, Catastrophic*).
2. **User-Centered Design (UCD) sesuai ISO 9241-210:2019**:
   - Pelaksanaan 4 tahapan desain terpusat pada pengguna:
     1. Memahami dan menentukan konteks penggunaan (*Context of Use*).
     2. Menentukan kebutuhan pengguna (*User Requirements* via Persona & User Journey Map).
     3. Merancang solusi desain (Arsitektur Informasi, Wireframe, dan *High-Fidelity Interactive Prototype* di Figma untuk 5 modul utama: Beranda, Berita, Galeri, Dokumen, dan Kontak/Pengaduan).
     4. Mengevaluasi desain terhadap kebutuhan pengguna (*Design Evaluation*).
3. **Konsep HCI Lanjutan & Emotional Design**:
   - Integrasi teori *Emotional Design* Don Norman (tiga level pemrosesan kognitif: *Visceral*, *Behavioral*, dan *Reflective*) untuk meredam kepanikan warga dalam situasi darurat kebencanaan.
   - Penerapan prinsip *Fluid Navigation*, tombol darurat 113 persisten (*persistent sticky emergency call*), dan *Direct Manipulation* (Ben Shneiderman).
4. **Evaluasi Kuantitatif WebQual 4.0 (Before vs After)**:
   - Pengukuran komparatif kualitas website menggunakan instrumen WebQual 4.0 dengan 22 butir indikator pada skala Likert 1–5 yang terbagi dalam 3 dimensi:
     - *Usability Quality* (8 indikator: kemudahan navigasi, kejelasan antarmuka, kenyamanan interaksi).
     - *Information Quality* (7 indikator: keakuratan data kebakaran, kebaruan informasi penyelamatan non-kebakaran, kejelasan format).
     - *Service Interaction Quality* (7 indikator: kepastian komunikasi darurat, keamanan kanal aduan, kemudahan akses kontak markas posko kecamatan).

---

## 3. Peran & Persona AI Agent

AI Agent bertindak sebagai:
1. **Academic Sparring Partner & HCI Specialist**: Mendiskusikan prinsip usabilitas, analisis heuristik antarmuka, arsitektur informasi, alur wireframing/prototyping, serta perumusan instrumen WebQual 4.0.
2. **Critical Reviewer & Usability Auditor**: Menguji ketepatan analisis heuristik, mengidentifikasi kontradiksi data empiris (kejadian kebakaran, SPM 15 menit, skor WebQual Before vs After), dan mengevaluasi validitas interpretasi hasil kuesioner.
3. **Academic Writer**: Menyusun dan menyempurnakan naskah artikel ilmiah bab demi bab mengacu pada template resmi (`proposals/Template Makalah IMK.docx`) dengan gaya bahasa akademik formal Indonesia yang lugas, presisi, dan bebas klise robotik.
4. **Fact-Checker & Citation Auditor**: Mengaudit keabsahan klaim faktual via `scripts/audit_paper_draft.py`, memblokir kutipan skripsi SIMPUS STIS, memvalidasi integritas bibliografi APA edisi ke-7, dan memastikan rekonsiliasi data angka 100% konsisten.

---

## 4. Struktur Direktori Workspace

```text
IMK/
├── AGENTS.md                  # Panduan agen dan konfigurasi workspace naskah IMK (dokumen ini)
├── INSTRUCTIONS.md            # Konstitusi kerja sistem: aturan mutlak bebas halusinasi & tool-first
├── ARCHITECTURE.md            # Peta sistem: direktori data, katalog perkakas CLI, & alur koordinasi
├── README.md                  # Ringkasan proyek, struktur repositori, dan panduan eksekusi
├── proposals/                 # Berkas template resmi makalah IMK
│   ├── Template Makalah IMK.docx # Template makalah resmi IMK Politeknik Statistika STIS
│   └── README.md              # Panduan standar penulisan makalah IMK
├── drafts/                    # Naskah artikel ilmiah terorkestrasi dan draf kerja
│   ├── MAKALAH_ILMIAH_IMK.md  # Naskah lengkap artikel ilmiah IMK (lolos audit 6 pilar)
│   ├── OUTLINE_PAPER_IMK.md   # Kerangka komprehensif naskah artikel ilmiah IMK
│   ├── laporan_proyek_imk/    # Draf kerja komprehensif per bagian/bab laporan
│   └── published/             # Berkas kompilasi dan ekspor terbitan
├── reports/                   # Naskah final terbitan Microsoft Word resmi
│   └── Makalah_Ilmiah_IMK_Kelompok_8.docx # Dokumen Word resmi siap kumpul/sidang
├── references/                # Koleksi referensi paper ilmiah peer-reviewed & template jurnal
│   ├── verified_papers.json   # Katalog metadata paper peer-reviewed terverifikasi
│   ├── references_zotero_import.bib # Ekspor BibTeX untuk Zotero Desktop
│   ├── references_zotero_import.ris # Ekspor RIS untuk Zotero Desktop
│   ├── template/              # Direktori template tambahan (referensi umum jurnal ilmiah)
│   └── markdown/              # Naskah Markdown teks utuh paper referensi untuk RAG lokal
├── results/                   # Hasil komputasi dan pengujian evaluasi usabilitas / WebQual 4.0
├── literature/                # Basis data literatur, bibtex, metadata, dan indeks pencarian
│   ├── references.bib         # Berkas sitasi standar BibTeX terpadu (khusus publikasi peer-reviewed)
│   ├── theses_data.json       # Database skripsi STIS (khusus analisis gap historis internal)
│   ├── theses_archive.bib     # Arsip sitasi skripsi alumni STIS (dilarang disitir dalam naskah)
│   └── search_index/          # Database SQLite dan vektor indeks hybrid retrieval
├── scratchpad/                # Jurnal kerja harian dan rekaman keputusan tim riset
│   └── daily_notes.md         # Catatan log harian, profil proyek, dan status milestone
├── docs/                      # Dokumentasi teknis lengkap setiap perkakas otomasi
├── scripts/                   # Perkakas otomasi riset & publication pipeline (CLI scripts)
├── src/calm_carson/           # Pustaka Python modular otomasi riset, NLP & temu-balik
└── tests/                     # Suite pengujian unit otomatis
```

---

## 5. Pedoman Interaksi & Konstitusi Sistem (System Constitution)

Setiap interaksi AI Agent wajib tunduk pada **Konstitusi Sistem** ([`INSTRUCTIONS.md`](file:///home/alfzki/Documents/IMK/INSTRUCTIONS.md)):

1. **Zero-Hallucination Directive (Larangan Mengarang Fakta)**:
   - Dilarang keras mengarang data statistik insiden kebakaran (271 kebakaran 2024, 198 kebakaran 2025, 518 aksi penyelamatan non-kebakaran 2025), angka waktu tanggap SPM Permendagri 114/2018 (15 menit), skor evaluasi WebQual 4.0 (*Before* vs *After*), temuan pelanggaran heuristik, atau isi paper rujukan tanpa dasar rujukan eksplisit dari korpus data lokal.
2. **Tool-First Search Mandate (Kewajiban Penelusuran Korpus)**:
   - Sebelum menyusun narasi ilmiah atau menjawab pertanyaan riset pengguna, AI Agent **WAJIB** mengeksekusi pencarian lokal terlebih dahulu (misal: [`scripts/query_references.py`](file:///home/alfzki/Documents/IMK/scripts/query_references.py), [`references/verified_papers.json`](file:///home/alfzki/Documents/IMK/references/verified_papers.json), atau [`scripts/hybrid_search.py`](file:///home/alfzki/Documents/IMK/scripts/hybrid_search.py)).
3. **Ketentuan Sitasi & Integritas Bibliografi**:
   - Penulisan naskah makalah IMK mengacu pada format sitasi **APA (Edisi ke-7)** di dalam teks (misal: `Ramadhan dkk. (2022)` atau `(Barnes & Vidgen, 2002)`) atau format IEEE `[X]` yang terpetakan secara valid ke daftar referensi lokal (`references/verified_papers.json` atau `literature/references.bib`).
4. **Larangan Mutlak Penggunaan Skripsi SIMPUS untuk Referensi Ilmiah**:
   - Skripsi/tesis alumni STIS dari pangkalan data SIMPUS **DILARANG KERAS** dijadikan referensi sitasi pada naskah artikel ilmiah IMK.
   - Pangkalan data SIMPUS (`literature/theses_data.json` & `theses_archive.bib`) hanya diperbolehkan untuk **analisis kesenjangan penelitian historis (research gap mining internal)**.
   - Seluruh sitasi referensi naskah **WAJIB** bersumber dari artikel jurnal peer-reviewed (SINTA/Scopus), prosiding konferensi internasional bereputasi, buku teks ber-ISBN, atau standar resmi (ISO, Permendagri).
5. **Missing Evidence Protocol & Rekonsiliasi Angka Empiris**:
   - Jika bukti data atau literatur belum tersedia di korpus lokal, agen **WAJIB menyatakan secara eksplisit bahwa bukti belum ditemukan di korpus lokal** dan **DILARANG BERSPEKULASI**. Tawarkan langkah pencarian via `scripts/search_academic_papers.py`.
   - Seluruh angka numerik evaluasi WebQual 4.0 (*Usability Quality*: 2,64 $\rightarrow$ 4,52; *Information Quality*: 2,81 $\rightarrow$ 4,58; *Service Interaction Quality*: 2,45 $\rightarrow$ 4,61) dan hasil Heuristik wajib konsisten 100% di seluruh bab naskah.
6. **Session Bootstrap Protocol (Inisialisasi Awal Sesi Baru)**:
   - Pada pembukaan sesi percakapan atau jendela baru, agen wajib memeriksa [`INSTRUCTIONS.md`](file:///home/alfzki/Documents/IMK/INSTRUCTIONS.md), [`ARCHITECTURE.md`](file:///home/alfzki/Documents/IMK/ARCHITECTURE.md), [`scratchpad/daily_notes.md`](file:///home/alfzki/Documents/IMK/scratchpad/daily_notes.md), dan [`drafts/MAKALAH_ILMIAH_IMK.md`](file:///home/alfzki/Documents/IMK/drafts/MAKALAH_ILMIAH_IMK.md) untuk memuat konteks lingkungan kerja serta status *milestone* terakhir dari disk.
7. **Disk-First State Persistence (Persistensi Statis ke Disk)**:
   - Jangan menyimpan progres hanya di riwayat percakapan. Setiap revisi naskah, perbaikan outline, hasil audit, dan keputusan riset **WAJIB langsung ditulis/diperbarui ke berkas statis disk** (`drafts/` atau `reports/`) dan dicatat di `scratchpad/daily_notes.md`.
8. **Git & Workspace Hygiene**:
   - Patuhi Zero Host Mutation Directive. Jalankan perkakas via `uv run`. Jangan simpan kredensial atau token API.

---

## 6. Standar Penulisan Naskah Artikel Ilmiah IMK

Setiap draf artikel ilmiah mengacu pada format resmi [`proposals/Template Makalah IMK.docx`](file:///home/alfzki/Documents/IMK/proposals/Template%20Makalah%20IMK.docx) atau template jurnal ilmiah:

1. **Judul Naskah**:
   - Judul Bahasa Indonesia: Maksimal 12 kata sesuai template, lugas, spesifik, mencerminkan objek penelitian dan pendekatan (*Redesain Antarmuka Portal Informasi Darurat Kebakaran Kota Bandar Lampung Berbasis UCD* [10 kata] atau *Redesain Website Dinas Pemadam Kebakaran Kota Bandar Lampung dengan Pendekatan User-Centered Design* [12 kata]).
   - Judul Bahasa Inggris: Dicantumkan di bawah judul utama dengan format miring (*italic*).
2. **Data Penulis**:
   - Mencantumkan seluruh nama anggota Kelompok 8 (Alif Zakiansyah As Syauqi, Andrian Fajar Fahmi, Valentina Lasma Situmorang), afiliasi resmi Politeknik Statistika STIS, dan email mahasiswa STIS (`@stis.ac.id`).
3. **Abstrak & Abstract**:
   - Panjang abstrak: Maksimal **150–200 kata**, 1 paragraf utuh.
   - Wajib memuat: Latar belakang urgensi kebencanaan, rumusan masalah usabilitas website eksisting, metode penyelesaian (Heuristik Nielsen, UCD ISO 9241-210, Figma High-Fidelity), hasil kuantitatif WebQual 4.0 Before vs After, dan kesimpulan/implikasi praktis.
   - **DILARANG** memuat kutipan pustaka atau rumus matematis di dalam abstrak.
   - Kata kunci (*Keywords*): 3–5 kata kunci relevan.
4. **Pendahuluan**:
   - Alur penalaran mengalir dari urgensi e-government kebencanaan $\rightarrow$ pentingnya akses informasi darurat $\rightarrow$ tiga masalah konkret website eksisting berangka empiris:
     1. *Masalah 1*: Tingginya frekuensi kebakaran (413 pada 2023, 271 pada 2024, 198 pada 2025) dan lonjakan aksi penyelamatan non-kebakaran rescue (558 pada 2023, 518 pada awal 2025) yang belum terakomodasi di website eksisting.
     2. *Masalah 2*: Tuntutan SPM waktu tanggap 15 menit Permendagri 114/2018 terhambat ketiadaan tombol darurat 113 persisten dan informasi kontak posko darurat yang tersembunyi.
     3. *Masalah 3*: Rendahnya usabilitas antarmuka eksisting dengan pelanggaran berat pada 10 prinsip Heuristik Jakob Nielsen (jargon birokrasi, ketiadaan breadcrumbs, formulir tanpa validasi).
   - Dialog studi literatur terdahulu, *research gap*, 3 rumusan masalah, dan 3 tujuan penelitian.
5. **Metodologi**:
   - Uraian tahapan UCD 4 tahap sesuai ISO 9241-210:2019.
   - Parameter dan prosedur Evaluasi Heuristik (10 prinsip Nielsen, skala severity 0–4).
   - Perancangan purwarupa interaktif high-fidelity pada Figma untuk 5 modul utama (Beranda, Berita, Galeri, Dokumen, Kontak/Pengaduan) dengan integrasi *Emotional Design*.
   - Instrumen evaluasi WebQual 4.0 (22 butir indikator, skala Likert 1–5, 3 dimensi: Usability, Information Quality, Service Interaction).
6. **Hasil dan Pembahasan**:
   - Pembahasan hasil evaluasi heuristik website eksisting dengan tabel rincian temuan dan rekomendasi redesain.
   - Pembahasan hasil redesain purwarupa interaktif Figma per modul utama.
   - Tabel komparasi kuantitatif WebQual 4.0 Before vs After per dimensi dan indikator:
     - *Usability Quality*: 2,64 $\rightarrow$ 4,52 (+1,88)
     - *Information Quality*: 2,81 $\rightarrow$ 4,58 (+1,77)
     - *Service Interaction Quality*: 2,45 $\rightarrow$ 4,61 (+2,16)
     - *Rata-rata Keseluruhan*: 2,63 $\rightarrow$ 4,57 (+1,94)
   - Dialog temuan dengan teori kognitif dan literatur ilmiah internasional/nasional.
7. **Kesimpulan dan Saran**:
   - Mengacu pada `Template Makalah IMK.docx`: dapat ditulis dalam bentuk narasi/paragraf maupun penomoran/pointer (*pointer/numbering* terstruktur).
   - Wajib menjawab tujuan penelitian, mengindikasikan hasil yang diperoleh, kelebihan dan keterbatasan, serta memuat saran yang bersifat aplikatif dan tidak normatif (seperti pada draf acuan `MAKALAH_ILMIAH_IMK.md` yang membagi sub-bab 4.1 Kesimpulan dan 4.2 Saran secara terstruktur).
8. **Daftar Pustaka**:
   - Format sitasi APA (Edisi ke-7) terstandarisasi.
   - Minimal 20 referensi ilmiah bereputasi (minimal 10 paper $\ge 2021$ terindeks Scopus / SINTA).
   - **DILARANG MENGUTIP SKRIPSI SIMPUS STIS**.

---

## 7. Kebijakan Manajemen Versi & Git Workflow

1. **Komit Berkala Setiap Milestone**: Lakukan `git add` dan `git commit` setiap kali menyelesaikan capaian riset (perbaikan bab, pembaruan data evaluasi, atau hasil audit).
2. **Format Pesan Komit**: Gunakan *Conventional Commits* (e.g., `feat(paper): ...`, `docs(agents): ...`, `test(audit): ...`, `chore(config): ...`).
3. **Sanitasi Repositori**: Jaga `.gitignore` agar file biner besar temporer, cache, dan credentials tidak ter-commit.

---

## 8. Katalog Perkakas Riset & Sub-Agen Otomasi HCI / IMK

Workspace ini dilengkapi dengan perkakas riset terotomasi, evaluasi usabilitas, dan sub-agen terpasang:

| Perkakas & Skrip | Fungsi Utama | Quick CLI | Panduan Lengkap |
| :--- | :--- | :--- | :--- |
| **Paper Draft Auditor**<br>`scripts/audit_paper_draft.py` | Audit 6 pilar artikel ilmiah: grounding klaim empiris, pencegahan skripsi SIMPUS, audit bibtex, kepatuhan template IMK, konsistensi metrik evaluasi WebQual, & sensor gaya AI. | `uv run python scripts/audit_paper_draft.py --file drafts/MAKALAH_ILMIAH_IMK.md --strict` | [`.agents/skills/paper-auditor/`](file:///home/alfzki/Documents/IMK/.agents/skills/paper-auditor/SKILL.md) |
| **Reference RAG Engine**<br>`scripts/query_references.py` | Temu-balik kutipan bukti empiris dan pembanding benchmark dari koleksi paper peer-reviewed terverifikasi lokal. | `uv run python scripts/query_references.py --query "User-Centered Design WebQual 4.0" --limit 3` | [`.agents/skills/paper-reference-rag/`](file:///home/alfzki/Documents/IMK/.agents/skills/paper-reference-rag/SKILL.md) |
| **Academic Paper Search**<br>`scripts/search_academic_papers.py` | Penelusuran publikasi ilmiah global multi-platform (OpenAlex, Crossref, arXiv, Semantic Scholar) dengan auto-ingestion ke RAG. | `uv run python scripts/search_academic_papers.py --query "user-centered design emergency portal" --platform all` | [`.agents/skills/claim-reference-finder/`](file:///home/alfzki/Documents/IMK/.agents/skills/claim-reference-finder/SKILL.md) |
| **Reference Ingestion**<br>`scripts/ingest_new_reference.py` | Ingesti referensi baru ke `references/` & Zotero dengan penolakan ketat skripsi SIMPUS STIS. | `uv run python scripts/ingest_new_reference.py --pdf <FILE_PDF> --doi <DOI>` | [`.agents/skills/claim-reference-finder/`](file:///home/alfzki/Documents/IMK/.agents/skills/claim-reference-finder/SKILL.md) |
| **Word OMML Exporter**<br>`scripts/export_to_docx.py` | Konversi draf Markdown ke dokumen DOCX berstandar resmi Template Makalah IMK dengan rumus native OMML dan hanging indent APA. | `uv run python scripts/export_to_docx.py --input drafts/MAKALAH_ILMIAH_IMK.md --output reports/Makalah_Ilmiah_IMK_Kelompok_8.docx` | [`proposals/`](file:///home/alfzki/Documents/IMK/proposals/) |
| **AI Style Checker**<br>`scripts/check_ai_style.py` | Auditor tanda penulisan AI (Wikipedia:Signs_of_AI_writing), klise dwibahasa, em dash PUEBI, & kebocoran LLM. | `uv run python scripts/check_ai_style.py --file drafts/MAKALAH_ILMIAH_IMK.md --suggest-fixes` | [`docs/ai_style_checker.md`](file:///home/alfzki/Documents/IMK/docs/ai_style_checker.md) |
| **Claim & Fact Verifier**<br>`scripts/verify_claims.py` | Auditor keabsahan klaim faktual, deteksi kontradiksi angka empiris, dan validasi integritas sitasi APA/IEEE. | `uv run python scripts/verify_claims.py --file drafts/MAKALAH_ILMIAH_IMK.md --strict` | [`docs/fact_verification.md`](file:///home/alfzki/Documents/IMK/docs/fact_verification.md) |
| **Hybrid Search**<br>`scripts/hybrid_search.py` | Mesin temu-balik dokumen Markdown berbasis Hierarchical Chunker, Dense CUDA, BM25Okapi, & RRF. | `uv run python scripts/hybrid_search.py --query "evaluasi heuristik damkar bandar lampung" --top-k 5` | [`docs/hybrid_retrieval.md`](file:///home/alfzki/Documents/IMK/docs/hybrid_retrieval.md) |
| **Document Publisher**<br>`scripts/publish_document.py` | Perkakas kompilasi dokumen multi-format (.docx & .pdf) dengan auto-renumber sitasi untuk format publikasi umum. | `uv run python scripts/publish_document.py --input drafts/MAKALAH_ILMIAH_IMK.md --format docx` | [`docs/publishing_pipeline.md`](file:///home/alfzki/Documents/IMK/docs/publishing_pipeline.md) |

### Sub-Agen Otomasi Spesialis
AI Agent dapat memanggil atau berkolaborasi dengan peran spesialis berikut:
1. **`paper_auditor`**: Menguji draf artikel ilmiah secara ketat via `scripts/audit_paper_draft.py` untuk membuktikan grounding klaim, pencegahan sitasi skripsi SIMPUS, integritas bibliografi APA, konsistensi angka WebQual/Heuristik, kepatuhan template, dan sensor AI (lihat [`.agents/skills/paper-auditor/SKILL.md`](file:///home/alfzki/Documents/IMK/.agents/skills/paper-auditor/SKILL.md)).
2. **`literature_researcher`**: Menggali sitasi terverifikasi, kutipan bukti empiris, dan perbandingan performa dari paper katalog open access peer-reviewed lokal (lihat [`.agents/skills/paper-reference-rag/SKILL.md`](file:///home/alfzki/Documents/IMK/.agents/skills/paper-reference-rag/SKILL.md)).
3. **`evidence_retriever`**: Menelusuri paper baru via arXiv, Crossref, OpenAlex, Semantic Scholar, mengunduh PDF, dan memasukkannya ke Zotero & RAG saat ada klaim yang belum terbukti (lihat [`.agents/skills/claim-reference-finder/SKILL.md`](file:///home/alfzki/Documents/IMK/.agents/skills/claim-reference-finder/SKILL.md)).
4. **`ai_style_auditor`**: Mengaudit dan membersihkan klise kosakata dwibahasa, em dash tidak baku, anak kalimat partisipel pemanis, dan artefak LLM (lihat [`.agents/skills/ai-style-auditor/SKILL.md`](file:///home/alfzki/Documents/IMK/.agents/skills/ai-style-auditor/SKILL.md)).
5. **`claim_verifier`**: Bertindak sebagai *Factual Integrity & Citation Verifier* dalam mendeteksi kontradiksi angka kuantitatif dan memastikan bebas halusinasi (lihat [`.agents/skills/claim-verifier/SKILL.md`](file:///home/alfzki/Documents/IMK/.agents/skills/claim-verifier/SKILL.md)).
6. **`originality_checker`**: Menguji kebaruan ide terhadap korpus global dan merumuskan usulan penguatan kebaruan (lihat [`.agents/skills/originality-checker/SKILL.md`](file:///home/alfzki/Documents/IMK/.agents/skills/originality-checker/SKILL.md)).
7. **`research_publisher`**: Mengaudit kepatuhan format naskah makalah IMK via `scripts/audit_paper_draft.py` dan mengompilasi naskah ke dokumen Word resmi siap kumpul via `scripts/export_to_docx.py` (lihat [`.agents/skills/research-publisher/SKILL.md`](file:///home/alfzki/Documents/IMK/.agents/skills/research-publisher/SKILL.md)**).

=== init-deep Complete ===

Mode: update

Files:
  [OK] ./AGENTS.md (root, 200 lines)
  [OK] ./src/calm_carson/AGENTS.md (N lines)

Dirs Analyzed: 14
AGENTS.md Created: 1
AGENTS.md Updated: 1

Hierarchy:
  ./AGENTS.md
  └── src/calm_carson/AGENTS.md
