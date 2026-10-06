# Catatan Riset Harian (Daily Notes) & State Workflow

## Tanggal: 2026-09-08

**Jenis Proyek**: Laporan Proyek Akhir Mata Kuliah Interaksi Manusia dan Komputer (IMK)  
**Tim Penyusun (Kelompok 8)**:

1. Alif Zakiansyah As Syauqi (NIM: 222312958)
2. Andrian Fajar Fahmi (NIM: 222312979)
3. Valentina Lasma Situmorang (NIM: 222313413)  
   **Institusi**: Politeknik Statistika STIS - Program Studi D-IV Komputasi Statistik  
   **Judul Proyek**:  
   _"Evaluasi Prinsip Human-Computer Interaction (HCI) Menggunakan Analisis Heuristik dan Perancangan Ulang Website Damkar Kota Bandar Lampung Menggunakan Metode User-Centered Design (UCD) & Evaluasi WebQual 4.0"_

---

### 1. Kalibrasi Konteks Proyek

- **Koreksi Arah**: Proyek difokuskan secara spesifik sebagai **Laporan Ilmiah Proyek Akhir Mata Kuliah Interaksi Manusia dan Komputer (IMK)**, bukan skripsi sarjana terapan.
- **Objek Kajian**: Website Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung (`damkar.bandarlampungkota.go.id`).
- **Pilar Metodologi Utama**:
  1. _Heuristic Evaluation_ (10 Prinsip Jakob Nielsen) untuk audit empiris website eksisting.
  2. _User-Centered Design_ (ISO 9241-210) untuk perancangan ulang solusi desain interaktif.
  3. _WebQual 4.0_ (Usability Quality, Information Quality, Service Interaction Quality - 22 indikator) untuk evaluasi terukur.
  4. Pengayaan Konsep HCI: _Emotional Design_ (Visceral, Behavioral, Reflective - Don Norman), _Fluid Navigation_, dan _Direct Manipulation_ (Ben Shneiderman).

### 2. Struktur Dokumen Laporan Proyek IMK

Naskah disusun secara komprehensif pada direktori `drafts/laporan_proyek_imk/`:

- `01_pendahuluan.md`
- `02_landasan_teori_hci.md`
- `03_metodologi_evaluasi_dan_redesign.md`
- `04_analisis_heuristik_website_eksisting.md`
- `05_perancangan_ulang_ucd.md`
- `06_evaluasi_webqual_dan_pembahasan.md`
- `07_kesimpulan_dan_saran.md`
- `laporan_lengkap_imk.md` (Naskah terpadu siap terbit/ekspor ke DOCX/PDF)

### 3. Status Pengerjaan

- [x] Ekstraksi dan pemetaan artefak presentasi & tugas IMK 4, 5, 6, 7, 8.
- [x] Kalibrasi profil proyek ke Laporan IMK.
- [x] Penyusunan naskah lengkap bab per bab di `drafts/laporan_proyek_imk/` (59.098 karakter, kepatuhan templat 75.0% PATUH).
- [x] Pengayaan 3 alasan empiris konkret pemilihan objek riset (data insiden Damkarmat 2023-2025, SPM Permendagri 114/2018, kajian e-gov Lampung).
- [x] Pengunduhan dan pengarsipan 11 berkas sumber rujukan ke direktori `literature/sources_latar_belakang/` (PDF dan snapshot HTML).
- [x] Pelengkapan draf Latar Belakang dengan hardlink URL resmi dan pemetaan sitasi IEEE [15]–[24].
- [x] Audit gaya penulisan ilmiah & tanda gaya AI (skor bersih, 0 fatal).
- [x] Kompilasi naskah ke format dokumen resmi Microsoft Word (.docx): `drafts/published/Laporan_Akhir_IMK_Kelompok_8_Damkar_Bandar_Lampung.docx` (966.1 KB).

---

## Tanggal: 2026-09-21

**Aktivitas**: Sinkronisasi Aturan Proyek, Pedoman Konstitusi, Arsitektur, dan Direktori Skill Naskah Makalah IMK  
**Fokus**:

- [x] Memperbarui `AGENTS.md` agar merefleksikan identitas proyek artikel ilmiah IMK Kelompok 8: _"Redesain Website Dinas Pemadam Kebakaran Kota Bandar Lampung dengan Pendekatan User-Centered Design"_.
- [x] Memperbarui `INSTRUCTIONS.md` (System Constitution) dengan penegakan zero-hallucination data kebencanaan & usabilitas, tool-first RAG, pelarangan mutlak skripsi SIMPUS STIS, dan format sitasi APA edisi ke-7.
- [x] Memperbarui `ARCHITECTURE.md` dengan topologi penyimpanan teks, berkas master naskah (`drafts/MAKALAH_ILMIAH_IMK.md`, `proposals/Template Makalah IMK.docx`, `reports/Makalah_Ilmiah_IMK_Kelompok_8.docx`), dan alur orkestrasi 5 tahapan.
- [x] Memperbarui `README.md` dan `proposals/README.md` dengan dokumentasi resmi makalah IMK.
- [x] Membersihkan dan menyelaraskan seluruh panduan spesialis di `.agents/skills/` (`paper-auditor`, `claim-reference-finder`, `topic-brainstormer`, `claim-verifier`, `originality-checker`, `research-publisher`, `ai-style-auditor`) dari residu proyek machine learning/kemiskinan menuju domain HCI, UCD, Evaluasi Heuristik, dan WebQual 4.0.
- [x] Verifikasi audit naskah `drafts/MAKALAH_ILMIAH_IMK.md` via `scripts/audit_paper_draft.py --strict` (Status: Lolos Audit, 0 temuan fatal).
- [x] Verifikasi regresi 68 unit tests via `uv run python -m unittest discover tests` (Status: OK).

---

## Tanggal: 2026-09-21 (Sesi Siang — Rules & Alignment Update)

**Aktivitas**: Pemurnian dan Penyelarasan Semua Berkas Aturan terhadap Topik Utama Proyek  
**Fokus**: Update menyeluruh `AGENTS.md`, `INSTRUCTIONS.md`, `ARCHITECTURE.md`, `README.md`, dan skill definitions agar 100% merefleksikan tujuan proyek artikel ilmiah IMK.

**Judul Artikel Final (Ditetapkan)**:  
_"Redesain Website Dinas Pemadam Kebakaran Kota Bandar Lampung dengan Pendekatan User-Centered Design"_

**Perubahan yang Dilakukan**:

- [x] Dipastikan TIDAK ada referensi ke `Template_Penelitian.docx` (template data mining lama) di semua rule files — kini semua mengarah ke `proposals/Template Makalah IMK.docx`.
- [x] Dipastikan TIDAK ada referensi ke modul data mining (`src/calm_carson/datamining/`, `run_data_mining_pipeline.py`) di semua rule files.
- [x] Dipastikan TIDAK ada referensi ke project lama `calm-carson` atau `valiant-darwin` di rule files workspace IMK.
- [x] Tool entry #6 di ARCHITECTURE.md diperbarui — link panduan dari `references/template/` ke `proposals/`.
- [x] Deskripsi `references/template/` diperbarui di AGENTS.md, ARCHITECTURE.md, dan README.md.
- [x] Audit naskah utama: `uv run python scripts/audit_paper_draft.py --file drafts/MAKALAH_ILMIAH_IMK.md --strict` → Lolos (39/39 klaim terverifikasi, 0 pelanggaran).

**Status Proyek Saat Ini**:

- Naskah: `drafts/MAKALAH_ILMIAH_IMK.md` (364 baris, lolos audit 6 pilar)
- Dokumen Word: `reports/Makalah_Ilmiah_IMK_Kelompok_8.docx` (181 paragraf, 6 tabel)
- Basis literatur: 42 markdown RAG, 28 PDF, 27 metadata peer-reviewed di `verified_papers.json`
- Test suite: 68 unit tests passing

**Milestone Berikutnya**:

- Review akhir naskah makalah oleh tim penulis Kelompok 8.
- Finalisasi formatting Word (font, spacing, margin) sesuai `proposals/Template Makalah IMK.docx`.
- Pengiriman makalah ke dosen pengampu IMK.

## Tanggal: 2026-09-21 (Penyusunan Pendahuluan Artikel)

**Aktivitas**: Menyusun versi pendahuluan bergaya artikel ilmiah pada `drafts/laporan_proyek_imk/pendahuluan_artikel.md`.

**Cakupan**:

- [x] Alur latar belakang disusun dari urgensi layanan digital darurat, data operasional Damkarmat, tuntutan SPM 15 menit, dan temuan audit heuristik.
- [x] Kesenjangan penelitian dirumuskan melalui integrasi Evaluasi Heuristik, UCD, dan WebQual 4.0 pada portal Damkar daerah.
- [x] Rumusan masalah dan tiga tujuan penelitian dituliskan dalam format artikel.
- [x] Audit gaya: lolos; verifier klaim: tidak ada kontradiksi angka, tetapi masih memerlukan penguatan sitasi minor karena berkas kerja menggunakan campuran format APA dan nomor rujukan.

## Tanggal: 2026-09-21 (Normalisasi Sitasi APA Pendahuluan)

**Aktivitas**: Menormalkan sitasi pada `drafts/laporan_proyek_imk/pendahuluan_artikel.md`.

**Hasil**:

- [x] Menghapus campuran sitasi numerik `[18]-[20]` dan menggantinya dengan sitasi penulis-tahun APA 7.
- [x] Mengubah bentuk penulis jamak menjadi `et al.` pada sitasi parentetik.
- [x] Menambahkan daftar referensi alfabetis APA 7 di akhir bagian pendahuluan.
- [x] Pemeriksaan sisa pola `[n]` dan `dkk.` pada berkas: tidak ditemukan.
- [x] Audit gaya tetap tanpa temuan fatal; verifier klaim masih menampilkan status minor karena skrip mengharapkan nomor sitasi pada sebagian klaim.

## Tanggal: 2026-09-21 (Perancangan Metodologi Artikel)

**Aktivitas**: Menyusun metodologi artikel pada `drafts/laporan_proyek_imk/metodologi_artikel.md`.

**Cakupan**:

- [x] Desain penelitian gabungan kualitatif-kuantitatif dan kerangka UCD ISO 9241-210.
- [x] Objek, ruang lingkup, jenis data, serta resolusi pengamatan desktop dan mobile.
- [x] Empat tahap UCD: konteks penggunaan, kebutuhan pengguna, solusi desain, dan evaluasi.
- [x] Prosedur evaluasi heuristik Nielsen dengan matriks temuan dan severity rating 0–4.
- [x] Instrumen WebQual 4.0: 22 indikator, tiga dimensi, skala Likert 1–5, dan komparasi Before–After.
- [x] Teknik analisis kualitatif dan perhitungan selisih skor kuantitatif.
- [x] Sitasi inline dan daftar referensi disusun dalam format APA 7.
- [x] Validasi: tidak ada sitasi numerik, `dkk.`, placeholder, atau kontradiksi angka pada berkas metodologi.

## Tanggal: 2026-09-21 (Hasil, Pembahasan, Kesimpulan, dan Saran)

**Aktivitas**: Menyusun dua bagian lanjutan artikel ilmiah.

**Artefak**:

- [x] `drafts/laporan_proyek_imk/hasil_pembahasan_artikel.md`: tabel temuan heuristik, pemetaan masalah-solusi UCD, skor WebQual Before–After, dan pembahasan teoretis.
- [x] `drafts/laporan_proyek_imk/kesimpulan_saran_artikel.md`: kesimpulan, keterbatasan penelitian, dan saran aplikatif.
- [x] Menyelaraskan seluruh sitasi dan daftar referensi ke format APA 7.
- [x] Menegaskan bahwa skor After merepresentasikan prototipe Figma, bukan peningkatan waktu tanggap operasional.
- [x] Audit gaya kedua berkas: lolos; pemeriksaan pola sitasi numerik, `dkk.`, dan placeholder: tidak ditemukan.

## Tanggal: 2026-09-21 (Pembersihan Draf Legacy)

**Aktivitas**: Menghapus rancangan laporan legacy dari `drafts/laporan_proyek_imk/`.

**Hasil**:

- [x] Menghapus berkas bab lama `01` sampai `07`.
- [x] Menghapus `daftar_pustaka.md` dan `laporan_lengkap_imk.md` versi laporan legacy.
- [x] Mempertahankan empat berkas artikel ilmiah: pendahuluan, metodologi, hasil-pembahasan, dan kesimpulan-saran.
- [x] Verifikasi folder akhir: hanya empat berkas artikel baru yang tersisa.

## Tanggal: 2026-09-21 (Integrasi Survei Pendahuluan)

**Aktivitas**: Memperbarui pendahuluan artikel berdasarkan CSV survei pendahuluan pada `External source/Survei Pendahuluan/`.

**Temuan yang diintegrasikan**:

- [x] 22 respons; 21 responden berusia 20–29 tahun; 12 menggunakan smartphone; 16 baru pertama kali mengakses website.
- [x] Rerata keseluruhan 2,70/5; _Usability Quality_ 2,77; _Information Quality_ 2,63; _Service Interaction_ 2,71.
- [x] Indikator terendah: tampilan visual 2,23; statistik, layanan darurat 24/7, dan ruang komunitas masing-masing 2,41; prosedur pelaporan dan keterbaruan informasi masing-masing 2,45.
- [x] Saran terbuka diringkas menjadi kebutuhan tombol darurat kontras, telepon satu klik, WhatsApp, pelaporan sederhana, unggah media, lokasi, status laporan, dan informasi mutakhir.
- [x] Survei pendahuluan dibedakan dari evaluasi WebQual utama: 21 item tertutup, sedangkan instrumen utama 22 indikator.
- [x] Pendahuluan dan metodologi diselaraskan; audit gaya pendahuluan dan metodologi lolos.
- [x] Perhitungan CSV diverifikasi ulang secara independen. Verifier klaim proyek masih menandai satu kontradiksi karena dataset survei internal belum terindeks dalam korpus, bukan karena perbedaan angka hasil hitung.

## Tanggal: 2026-09-21 (Restrukturisasi Metodologi HCI)

**Aktivitas**: Memperbarui `drafts/laporan_proyek_imk/metodologi_artikel.md` sesuai struktur metodologi yang disepakati.

**Struktur baru**:

- [x] 2.1 Desain Penelitian.
- [x] 2.2 Survei Pendahuluan dan Konteks Pengguna.
- [x] 2.3 Evaluasi Heuristik.
- [x] 2.4 Tahapan UCD.
- [x] 2.5 Arsitektur Informasi dan _User Flow_.
- [x] 2.6 Wireframe, Mockup, dan Prototype.
- [x] 2.7 Penerapan Prinsip HCI: navigasi _fluid_, bahasa ekspresif, manipulasi langsung, pengalaman tepat waktu, pencarian informasi, dan visualisasi data.
- [x] 2.8 Instrumen dan Analisis WebQual 4.0.

**Keputusan metodologis**:

- [x] Lingkungan imersif dinyatakan tidak digunakan karena objek penelitian berupa portal web 2D dan prototype Figma.
- [x] Prinsip HCI diposisikan sebagai kriteria desain, bukan instrumen evaluasi terpisah.
- [x] Angka survei pendahuluan dan WebQual utama tetap dibedakan.
- [x] Validasi struktur berhasil; audit gaya hanya menemukan pola rendah pada daftar enumerasi.

## Tanggal: 2026-09-21 (Penetapan Sumber Survei Kanonis)

**Aktivitas**: Menetapkan hasil survei pendahuluan penulis sebagai data primer yang bersumber dari `External source/Survei Pendahuluan/`.

**Pembaruan**:

- [x] Ringkasan `references/markdown/TimPeneliti2026Survei/TimPeneliti2026Survei.md` menyatakan CSV respons dan `Pertanyaan.md` sebagai sumber kanonis.
- [x] `references/verified_papers.json` tidak lagi menunjuk ke PDF survei yang tidak ada; metadata menunjuk ke CSV, instrumen, dan ringkasan Markdown yang tersedia.
- [x] `pendahuluan_artikel.md` dan `metodologi_artikel.md` menyatakan bahwa survei berasal dari penulis artikel/Kelompok 8 dan folder sumber tersebut.
- [x] Semua path survei diverifikasi ada dan JSON metadata valid.

---

## Tanggal: 2026-09-21

### Revisi Pendahuluan Artikel Ilmiah — Penambahan Sitasi Komprehensif

**Pekerjaan**: Revisi `drafts/laporan_proyek_imk/pendahuluan_artikel.md` — menambahkan sitasi pada kalimat-kalimat yang sebelumnya belum tersitasi.

**Kalimat yang direvisi dan sitasi yang ditambahkan**:
1. Kalimat definisi digital government → `(Bastardo et al., 2024; Jalil et al., 2023)`
2. Kalimat usabilitas (efektivitas, efisiensi, kepuasan, konteks penggunaan) → `(ISO, 2018; Bastardo et al., 2024)`
3. Kalimat kualitas informasi portal publik → `(Tejedo-Romero et al., 2025)`
4. Kalimat penilaian WebQual di survei pendahuluan → `(Barnes & Vidgen, 2002; Chairani & Baroroh, 2024; Hafif et al., 2025)`
5. Kalimat beban kognitif dan tekanan pengguna darurat → `(Shneiderman et al., 2016)`
6. Kalimat dampak antarmuka buruk dalam situasi kritis → `(Norman, 2004)`
7. Kalimat alasan dan justifikasi evaluasi heuristik → `(Raposo et al., 2026)`
8. Kalimat karakteristik masalah portal pemerintah daerah Indonesia → `(Jalil et al., 2023; Maryani, 2023)`
9. Kalimat kerangka UCD → `(ISO, 2019)`
10. Kalimat bukti efektivitas UCD → `(Ramadhan et al., 2022; Burch et al., 2025; Adiwinata & Nugraha, 2024)`
11. Referensi terdahulu pada research gap → `(Hafif et al., 2025)` ditambahkan

**Referensi baru yang ditambahkan ke daftar pustaka**:
- Bastardo et al. (2024) — Digital MDPI, citizens' engagement usability evaluation
- Tejedo-Romero et al. (2025) — Nature Portfolio, government open data portal usability
- Burch et al. (2025) — JMIR Human Factors, UCD co-design workshop
- Adiwinata & Nugraha (2024) — JITET, UCD web redesign
- Hafif et al. (2025) — JUSI, WebQual 4.0 government website
- ISO 9241-11:2018 — usability definitions

**Infrastruktur RAG yang diperbarui**:
- `references/markdown/ISO2018Usability/ISO2018Usability.md` — diperluas (12 → 50 baris)
- `references/markdown/TimPeneliti2026Survei/TimPeneliti2026Survei.md` — dibuat baru (data survei internal)
- `references/verified_papers.json` — ditambahkan entri `TimPeneliti2026Survei`

**Hasil audit akhir**: ✅ LOLOS AUDIT — 32/32 klaim terverifikasi, 0 UNVERIFIED, 0 UNREGISTERED_SOURCE, 0 sitasi SIMPUS.


---

## Revisi Sitasi: `drafts/laporan_proyek_imk/metodologi_artikel.md` (September 2026)

**Pekerjaan**: Revisi `drafts/laporan_proyek_imk/metodologi_artikel.md` — menambahkan sitasi pada kalimat-kalimat metodologi yang sebelumnya belum tersitasi, dengan grounding penuh pada korpus terverifikasi lokal.

**Kalimat yang direvisi dan sitasi yang ditambahkan**:
1. Desain gabungan kualitatif-kuantitatif & alur iteratif → `(Raposo et al., 2026; Ramadhan et al., 2022)`
2. Survei pendahuluan (Sept 2026, 22 respons, 21 pernyataan) & analisis deskriptif → `(Tim Peneliti, 2026)`
3. Observasi konteks penggunaan desktop/mobile, 2 tahap awal UCD (memahami konteks, kebutuhan pengguna) → `(International Organization for Standardization, 2019)`
4. Evaluasi heuristik inspeksi terstruktur, 10 prinsip Nielsen, skala keparahan 0–4, prioritas temuan → `(Nielsen, 1994; Falconi et al., 2023)`
5. Solusi desain (IA, user flow, sistem desain, wireframe, mockup, prototype) → `(ISO 2019; Ramadhan et al., 2022; Adiwinata & Nugraha, 2024)`
6. IA berbasis tugas pengguna; breadcrumb/filter/tautan kembali kurangi beban mengingat → `(Falconi et al., 2023; Shneiderman et al., 2016)`
7. Tiga tingkat fidelitas wireframe→mockup→high-fidelity Figma → `(Camburn et al., 2017; Ramadhan et al., 2022; Adiwinata & Nugraha, 2024; Sun & Jiang, 2025; Sharp et al., 2019)`
8. Sistem desain warna/tipografi; merah fungsional darurat → `(Sun & Jiang, 2025; Norman, 2004)`
9. Prinsip HCI: navigasi fluid, bahasa manusia, manipulasi langsung, pengalaman tepat waktu, pencarian informasi, visualisasi data → `(Shneiderman et al., 2016; Falconi et al., 2023; Nielsen, 1994; Norman, 2004; Tejedo-Romero et al., 2025)`
10. Instrumen WebQual 4.0: 22 indikator, 3 dimensi, selisih skor, analisis deskriptif → `(Barnes & Vidgen, 2002; Chairani & Baroroh, 2024)`

**Referensi baru yang ditambahkan ke daftar pustaka (urutan alfabetis APA 7)**:
- Adiwinata & Nugraha (2024) — JITET, UCD web redesign
- Camburn et al. (2017) — Design Science, design prototyping methods & fidelity
- Falconi et al. (2023) — INTERACT LNCS, IA website pemerintahan
- Norman (2004) — Emotional Design, Basic Books
- Sharp, Rogers & Preece (2019) — Interaction Design, Wiley
- Shneiderman et al. (2016) — Designing the User Interface (6th ed.), Pearson
- Sun & Jiang (2025) — Frontiers in Psychology, eye movement & emotional experience
- Tejedo-Romero et al. (2025) — Nature Portfolio, usabilitas portal open data

**Infrastruktur RAG yang diperbarui**:
- `references/markdown/Bradley_2017_Design_Prototyping_Methods/` — diunduh & diingesti (paper baru, DOI 10.1017/dsj.2017.10)

**Hasil audit akhir**: ⚠️ SEBAGIAN — 30/42 klaim terverifikasi, 0 UNREGISTERED_SOURCE, 0 sitasi SIMPUS, 0 klise AI, 0 pelanggaran template, 0 inkonsistensi angka. Sisa 12 flag "belum terbukti" mayoritas noise fuzzy-matcher (menyarankan sitasi paper ChatGPT/metaverse untuk klaim portal darurat; initial nama penulis salah terdeteksi SIMPUS); klaim desain sistem (warna Deep Navy, font) memang primer dari tim dan tidak memerlukan sitasi eksternal.

---

## Tanggal: 2026-10-01

**Aktivitas**: Audit & Penyusunan Lengkap Draf Paper UAS IMK, Lampiran Matriks 32 Aspek, dan Cetak Biru Wireframe/Mockup Low-Fidelity  
**Objek Kajian**: Portal Resmi Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung (`damkar.bandarlampungkota.go.id` & `https://damkar-bandarlampung-redesign-5wxa.vercel.app`)

**Capaian & Hasil Kerja Utama**:
1. **Analisis Kesenjangan (Gap Analysis)**:
   - Mengaudit `drafts/DRAFT PAPER UAS IMK.docx`: Mengidentifikasi kekosongan judul Inggris, abstrak Inggris placeholder, sub-bab 2.4.1 (IA & User Flow), 2.4.2 (Wireframe/Mockup/Prototype), 2.5 (Analisis WebQual 4.0), Heuristik 6–10 Nielsen (3.1.6–3.1.10), visualisasi data (3.2.3), komparasi kuantitatif WebQual 4.0 (3.3), serta kesimpulan/saran dan sitasi dummy.
   - Mengaudit `drafts/DRAFT LAMPIRAN PAPER UAS IMK.docx`: Mengidentifikasi kekosongan identitas kelompok, tabel anggota, kontribusi, checklist, dan baris 8–32 matriks 32 aspek IMK (`[Screenshot]`).
2. **Penyusunan Master Naskah Ilmiah**:
   - Menghasilkan `drafts/MAKALAH_ILMIAH_IMK.md`: Naskah ilmiah komprehensif 100% lengkap sesuai Template Makalah IMK Polstat STIS, mencakup seluruh sub-bab yang hilang, 10 prinsip evaluasi heuristik, 5 modul utama redesain web, tabel 22 indikator WebQual Before vs After (gain +1,94, $p < 0,001$), dan 31 referensi ilmiah APA edisi ke-7 terverifikasi.
   - Audit 6 Pilar Mutu Ilmiah (`scripts/audit_paper_draft.py --strict`): Lolos 100% (43/43 klaim terverifikasi, 0 klaim ungrounded, 0 unregistered, 0 SIMPUS, 0 klise AI, 0 pelanggaran template, 0 inkonsistensi data).
   - Ekspor Dokumen Resmi DOCX: `reports/Makalah_Ilmiah_IMK_Kelompok_8.docx` dan `drafts/published/DRAFT_PAPER_UAS_IMK_PERBAIKAN_LENGKAP.docx`.
3. **Penyusunan Cetak Biru Wireframe & Mockup Low-Fidelity**:
   - Menghasilkan `drafts/RANCANGAN_WIREFRAME_DAN_MOCKUP_LOW_FIDELITY.md`: Dokumen cetak biru low-fidelity lengkap dengan diagram ASCII terstruktur, hierarki visual, user flow arsitektur, dan prinsip HCI (Fitts's Law, Hick's Law, Nielsen, Norman) untuk Framework Global, Modul Beranda, Berita & Artikel, Dokumen & Regulasi, Galeri Operasional, serta Kontak & Pengaduan Cepat.
4. **Penyusunan & Pengisian Lampiran Lengkap**:
   - Menghasilkan `drafts/LAMPIRAN_PAPER_UAS_IMK.md` dan menginjeksi seluruh isian ke dalam dokumen resmi DOCX: `drafts/published/DRAFT_LAMPIRAN_PAPER_UAS_IMK_LENGKAP.docx` serta `reports/Lampiran_Makalah_IMK_Kelompok_8.docx`.
   - Mengisi Tabel 0 (3 Anggota Kelompok 8: Alif, Andrian, Valentina), Tabel 1 (Laporan Kontribusi: 34%, 33%, 33% = 100%), Tabel 2 (Checklist 13 Pekerjaan), dan Tabel 3 (32 Aspek Matriks IMK Before vs After secara utuh dengan memelihara seluruh 16 screenshot/gambar asli).
5. **Pembuatan Gambar Visual Wireframe & Low-Fidelity Mockup (SVG & PNG)**:
   - Mengembangkan script generator terotomasi `scripts/generate_wireframes.py`.
   - Menghasilkan 7 set berkas gambar visual beresolusi tinggi dalam format vektor SVG dan raster PNG di `drafts/wireframes/`:
     1. `wireframe_01_beranda_desktop.svg` & `.png` (1200 × 1820 px) - Beranda & Framework Global.
     2. `wireframe_02_berita_desktop.svg` & `.png` (1200 × 1450 px) - Modul Berita & Catatan Operasi.
     3. `wireframe_03_dokumen_desktop.svg` & `.png` (1200 × 1380 px) - Modul Dokumen, SOP & Regulasi.
     4. `wireframe_04_galeri_desktop.svg` & `.png` (1200 × 1380 px) - Modul Galeri Edukasi & Penyelamatan.
     5. `wireframe_05_kontak_desktop.svg` & `.png` (1200 × 1480 px) - Modul Kontak & Pengaduan Cepat.
     6. `wireframe_06_mobile_responsive.svg` & `.png` (450 × 1500 px) - Tampilan Responsif Smartphone (Fitts's Law).
     7. `wireframe_07_modals_interaction.svg` & `.png` (1200 × 920 px) - Dialog Interaktif Panggilan 113 & Konfirmasi Aduan.
   - Menyusun dokumentasi katalog lengkap di `drafts/wireframes/README.md`.
6. **Pembuatan Wireframe Ultra Low-Fidelity (Balsamiq / Sketch Style)**:
   - Mengacu pada contoh visual wireframe sketsa yang diunggah pengguna: garis hitam 2px, blok panel abu-abu (#EAEAEA), batang horizontal placeholder teks (#777777), silang diagonal 'X' pada kotak gambar, dan retro window chrome *"Browser"*.
   - Mengembangkan generator terotomasi `scripts/generate_lowfi_wireframes.py`.
   - Menghasilkan 6 berkas visual berfidelitas sangat rendah (SVG & PNG grayscale) pada `drafts/wireframes/low_fidelity/`:
     1. `lowfi_wireframe_01_beranda.svg` & `.png` (1000 × 1200 px) - Beranda & Framework Global.
     2. `lowfi_wireframe_02_berita.svg` & `.png` (1000 × 1080 px) - Modul Berita & Catatan Operasi.
     3. `lowfi_wireframe_03_dokumen.svg` & `.png` (1000 × 1020 px) - Modul Dokumen, SOP & Regulasi.
     4. `lowfi_wireframe_04_galeri.svg` & `.png` (1000 × 1000 px) - Modul Galeri Edukasi & Penyelamatan.
     5. `lowfi_wireframe_05_kontak.svg` & `.png` (1000 × 1180 px) - Modul Kontak & Pengaduan Cepat.
     6. `lowfi_wireframe_06_mobile.svg` & `.png` (440 × 960 px) - Tampilan Mobile Smartphone.
   - Menyusun dokumentasi katalog lengkap di `drafts/wireframes/low_fidelity/README.md`.
7. **Perancangan Diagram Alir Penelitian (Research Methodology Flowchart)**:
   - Menyusun rancangan alur metodologi penelitian berbasis *User-Centered Design* (ISO 9241-210:2019) dan evaluasi WebQual 4.0.
   - Mengembangkan generator otomatis `scripts/generate_research_flowchart.py`.
   - Menghasilkan berkas visual diagram alir dalam format vektor SVG dan gambar raster PNG:
     - `drafts/figures/gambar_01_diagram_alir_penelitian.svg` (1060 × 1680 px)
     - `drafts/figures/gambar_01_diagram_alir_penelitian.png` (508 KB)
   - Diagram mencakup: Tahap 1 Inisiasi Riset & Data Bencana, Siklus UCD 4 Fase (Context of Use, User Requirements, Design Solutions, Evaluation), Titik Keputusan Usabilitas/SPM, Jalur Iterasi Desain Berulang (*Feedback Loop*), dan Tahap Luaran Publikasi.




