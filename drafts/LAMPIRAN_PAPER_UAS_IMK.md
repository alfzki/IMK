# LAMPIRAN PAPER UAS INTERAKSI MANUSIA DAN KOMPUTER (IMK)

**Judul Makalah**:  
*Redesain Website Dinas Pemadam Kebakaran Kota Bandar Lampung dengan Pendekatan User-Centered Design*

---

# FORM LAPORAN KONTRIBUSI ANGGOTA KELOMPOK

## A. Identitas Kelompok
- **Mata Kuliah**: Interaksi Manusia dan Komputer (IMK)
- **Kelas**: 3SI1
- **Nama Project/Aplikasi**: Redesain Portal Resmi Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung
- **Kelompok**: 8
- **Tanggal Pengumpulan**: Oktober 2026

## B. Daftar Anggota Kelompok

| No. | Nama Anggota | NIM | Peran Utama |
| :---: | :--- | :---: | :--- |
| 1 | Alif Zakiansyah As Syauqi | 222312958 | Project Lead, HCI System Architecture & Full-Stack Web Engineering |
| 2 | Andrian Fajar Fahmi | 222312979 | UI/UX Designer, Heuristic Usability Auditor & Wireframing Specialist |
| 3 | Valentina Lasma Situmorang | 222313413 | Data Analyst, Survey Administrator & WebQual 4.0 Quantitative Evaluator |

## C. Laporan Kontribusi Masing-Masing Anggota

| No. | Nama Anggota | Tugas/Kontribusi yang Dikerjakan | Output yang Dihasilkan | Persentase Kontribusi |
| :---: | :--- | :--- | :--- | :---: |
| 1 | Alif Zakiansyah As Syauqi | Mengoordinasikan pembagian tugas riset; merumuskan arsitektur informasi dua-jalur (*emergency fast-track* dan *e-government track*); mengimplementasikan antarmuka interaktif responsif berbasis Next.js, TypeScript, dan Tailwind CSS; merekayasa bilah pencarian instan (<100ms) dan *Persistent Sticky 113 Emergency Button*; menyusun naskah bab Pendahuluan dan Metodologi. | Kode sumber fungsional web redesain di Vercel, rancangan wireframe low-fidelity, dokumentasi teknis sistem pencarian, serta naskah artikel ilmiah bab 1 dan 2. | 34% |
| 2 | Andrian Fajar Fahmi | Melakukan inspeksi usabilitas awal berbasis 10 prinsip evaluasi heuristik Jakob Nielsen; menentukan skala *severity rating* (0–4); merancang kerangka tata letak monokromatik (*low-fidelity wireframe*); menyusun purwarupa visual dan *high-fidelity prototype* di Figma untuk 5 modul utama (Beranda, Berita, Dokumen, Galeri, Kontak); menyusun pembahasan hasil audit heuristik dan perancangan antarmuka. | Matriks audit 10 Heuristik Nielsen, skematik wireframe 5 modul utama, purwarupa interaktif Figma, dan naskah artikel ilmiah bab 3.1–3.2. | 33% |
| 3 | Valentina Lasma Situmorang | Mengelola instrumen survei pendahuluan kuesioner daring (N=22); menyusun instrumen evaluasi WebQual 4.0 (22 indikator); melakukan rekapitulasi data dan analisis statistik deskriptif; menghitung komparasi skor Before vs After; menguji signifikansi statistik uji beda berpasangan (*Wilcoxon Signed-Rank Test* $p < 0,001$); menyusun naskah pembahasan kuantitatif, kesimpulan, dan saran aplikatif. | Dataset survei pendahuluan, tabel komparasi kuantitatif 22 indikator WebQual 4.0, output uji signifikansi statistik, naskah bab 3.3 dan bab 4. | 33% |
| | **TOTAL** | | | **100%** |

## D. Rincian Jenis Kontribusi

| Jenis Pekerjaan | Alif Zakiansyah (Anggota 1) | Andrian Fajar (Anggota 2) | Valentina Lasma (Anggota 3) |
| :--- | :---: | :---: | :---: |
| Analisis aplikasi/website existing | ✓ | ✓ | ✓ |
| Identifikasi pengguna & persona | ✓ | ✓ | ✓ |
| Analisis Information Search & Navigasi | ✓ | ✓ | — |
| Identifikasi masalah usability & Heuristik | — | ✓ | ✓ |
| Studi/referensi teori IMK (UCD, Norman, Shneiderman) | ✓ | ✓ | ✓ |
| User flow & Task scenario flow | ✓ | ✓ | — |
| Ide/solusi redesign sistem | ✓ | ✓ | ✓ |
| Desain UI di Figma (Mockup High-Fidelity) | — | ✓ | — |
| Prototype interaktif & Rekayasa Web Next.js | ✓ | ✓ | — |
| Pengujian/evaluasi desain (WebQual 4.0) | — | — | ✓ |
| Analisis data statistik & uji signifikansi | — | — | ✓ |
| Dokumentasi/laporan artikel ilmiah | ✓ | ✓ | ✓ |
| Presentasi hasil perancangan | ✓ | ✓ | ✓ |

---

# FORM ANALISIS PROJECT REDESIGN – BEFORE & AFTER
**IMK – Sub-CPMK 8 dan Sub-CPMK 9**

- **Kelompok**: 8
- **Nama Aplikasi/Website**: Website Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung
- **Anggota**: 
  1. Alif Zakiansyah As Syauqi (NIM: 222312958)
  2. Andrian Fajar Fahmi (NIM: 222312979)
  3. Valentina Lasma Situmorang (NIM: 222313413)
- **Link Prototype Figma / Live Web**: `https://damkar-bandarlampung-redesign-5wxa.vercel.app`

### Ringkasan Hasil Redesain
- **Masalah utama pada BEFORE**:
  1. Pencantuman jam operasional yang salah dan membingungkan (*Jam Oprasional: 07.00 s/d 16.00*) pada tajuk utama situs, yang memberi kesan fatal bahwa damkar tidak beroperasi pada malam hari.
  2. Ketiadaan tombol darurat 113 persisten; nomor telepon darurat tersembunyi dalam teks statis berukuran kecil dan membutuhkan penelusuran lebih dari 4 kali klik (> 180 detik) dengan tingkat kegagalan tugas mencapai 45%.
  3. Informasi kontak 6 posko siaga kecamatan tidak tersedia secara transparan di situs.
  4. Sistem pencarian kaku, lambat (2–4 detik), memaksa muat ulang halaman secara penuh (*full page reload*), dan tanpa filter kategori.
  5. Formulir pengaduan tidak memiliki validasi format masukan secara real-time dan tidak memiliki modal konfirmasi pengiriman (*error prevention* nihil).
  6. Dokumen kedinasan (LKJIP, Renstra, SOP) disajikan tanpa ringkasan bahasa awam bagi masyarakat dan pelaku usaha.

- **Perbaikan utama pada AFTER**:
  1. Penerapan *Top Emergency Bar* berwarna biru tua (#172554) yang menegaskan status kesiapsiagaan posko 24 jam penuh dan komitmen SPM waktu tanggap < 15 menit Permendagri No. 114/2018.
  2. Penyediaan *Persistent Sticky 113 Emergency Button* di sudut kanan bawah peramban (`fixed bottom-6 right-6 z-50`) dengan animasi denyut (*pulse*), membuka modal panggil cepat 1-klik menuju 113, 112, dan Mako Pusat.
  3. Penyediaan direktori kartu 6 Posko Siaga Kecamatan se-Bandar Lampung (Kedaton, Sukarame, Kemiling, Panjang, Teluk Betung, Tanjung Karang) berfitur sambungan telepon langsung (*click-to-call*).
  4. Pengadaan bilah pencarian instan (< 100 ms) di modul Berita, Dokumen, dan FAQ yang berpadu dengan tombol kapsul penyaring (*pill category filters*) dinamis.
  5. Formulir pengaduan interaktif dengan validasi seketika (*real-time validation*) untuk format nama, email regex, nomor telepon, dan panjang pesan, dilengkapi modal dialog konfirmasi pencegah galat serta penerbitan nomor tiket aduan resmi.
  6. Penyajian tabel dokumen publik yang dilengkapi ringkasan awam, indikator format/ukuran file, dan animasi umpan balik pengunduhan (*toast notification*).
  7. Dasbor visualisasi data statistik kejadian bencana kebakaran dan aksi penyelamatan non-kebakaran tahun 2024–2025 secara transparan.

- **Dampak terhadap pengguna/UX**:
  1. Memangkas waktu penemuan nomor darurat dari > 180 detik menjadi < 3 detik (1 ketukan instan) dengan tingkat keberhasilan tugas mencapai 100%.
  2. Mengeliminasi disorientasi navigasi dan kepanikan kognitif warga melalui struktur informasi yang mengalir (*fluid navigation*).
  3. Mencegah kesalahan input laporan kejadian darurat melalui validasi langsung dan konfirmasi penutupan (*closure*).
  4. Meningkatkan kepuasan pengguna secara empiris pada 22 indikator model WebQual 4.0, di mana rerata dimensi *Usability Quality* naik dari 2,64 menjadi 4,52 (+1,88), *Information Quality* naik dari 2,81 menjadi 4,58 (+1,77), dan *Service Interaction Quality* melonjak dari 2,45 menjadi 4,61 (+2,16), menghasilkan kenaikan kepuasan total dari 2,63 menjadi 4,57 (+1,94; $p < 0,001$).

---

## TABEL ANALISIS PROJECT REDESIGN BEFORE & AFTER (32 ASPEK MATERI IMK)

| No. | Materi IMK | Aspek/Fitur yang Dianalisis | BEFORE – Kondisi Existing | AFTER – Hasil Redesain | Alasan/Dasar Perubahan |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | Expressive Human & Command Languages | Expressive Interface | Beranda lama didominasi spanduk foto seremonial pejabat; teks nomor darurat 113 kecil dan menyatu dalam bilah atas yang redup tanpa hierarki visual. | Beranda baru menempatkan hero kesiapsiagaan, komitmen SPM 15 menit, 6 kartu akses cepat layanan, statistik insiden, pengumuman darurat, dan tombol 113 beranimasi denyut (*pulse*). | Menerapkan prinsip *Aesthetic and Minimalist Design* dan *Visual Hierarchy*: antarmuka ekspresif harus langsung menyampaikan esensi fungsi instansi penyelamatan jiwa tanpa membebani atensi pengguna. |
| 2 | Expressive Human & Command Languages | Bahasa/label/perintah | Label dan istilah pada website lama formal dan birokratis; singkatan seperti LKJIP, Renstra, dan SOP Uji Proteksi tidak diberi deskripsi bagi masyarakat awam. | Seluruh istilah teknis birokrasi kini disertai ringkasan penjelasan bahasa awam di setiap kartu dokumen; label tombol menggunakan frasa lugas ("Hubungi Posko 113", "Unduh PDF"). | Menerapkan prinsip *Match Between System and the Real World* (Nielsen, 1994): bahasa sistem harus menggunakan istilah yang akrab bagi pengguna sehari-hari guna mengikis friksi kognitif. |
| 3 | Expressive Human & Command Languages | Feedback terhadap tindakan pengguna | Layar tidak memberikan respon saat pengguna mengklik tautan dokumen atau mengirim pesan; tidak ada indikator pemuatan (*loading indicator*). | Sistem memberikan umpan balik mikro (*micro-interactions*): tombol berubah status (*hover & active state*), animasi spinner saat unduh dokumen, dan notifikasi pesan berhasil (*toast notification*). | Menerapkan prinsip *Visibility of System Status* (Nielsen H1): sistem harus senantiasa memberi tahu pengguna mengenai status operasi yang sedang berlangsung dalam waktu yang wajar. |
| 4 | Expressive Human & Command Languages | Emotional Design (Tingkat Viseral & Behavioral) | Tampilan lama terkesan kaku, monoton, dan dingin; tidak memberikan rasa tenang bagi warga yang sedang panik menghadapi kebakaran atau bencana. | Tata letak menggunakan palet warna *Deep Navy* (#172554) profesional berpadu aksen *Emergency Red* (#DC2626) menyala yang memberikan ketenangan emosional dan ketegasan wibawa siaga. | Menerapkan teori *Emotional Design* Don Norman (2004) pada tingkat viseral (kesan visual tenang & kokoh) dan behavioral (kemudahan interaksi tanpa hambatan bagi warga yang panik). |
| 5 | Expressive Human & Command Languages | Elemen yang membangun pengalaman emosional (Tingkat Reflektif) | Elemen beranda tidak mencerminkan kesiapsiagaan 24 jam; jam kantor salah (07.00-16.00) merusak rasa aman warga pada malam hari. | Penegasan komitmen Standar Pelayanan Minimal (SPM) waktu tanggap < 15 menit Permendagri No. 114/2018 dan status operasional 24/7 ditampilkan mencolok pada tajuk atas. | Menerapkan *Emotional Design* tingkat reflektif: membangun rasa aman, keyakinan publik, dan reputasi positif terhadap keandalan korps pemadam kebakaran. |
| 6 | Advancing the User Experience | Kemudahan penggunaan (*Ease of Use*) | Pengguna harus menelusuri menu berulang-ulang untuk mencari kontak darurat; struktur menu tidak terorganisasi secara logis. | Navigasi utama disusun dalam *two-tier sticky header*; bilah pencarian tersedia di tajuk; tombol panggil darurat 113 selalu terlihat di sudut kanan bawah. | Menerapkan prinsip *User-Centered Design* (ISO 9241-210:2019): mengurangi langkah penelusuran dan beban ingatan pengguna dalam mengakses fitur vital. |
| 7 | Advancing the User Experience | Efisiensi interaksi (*Interaction Efficiency*) | Pengguna memerlukan rata-rata 4 hingga 8 kali klik untuk menemukan nomor telepon kantor damkar; proses penemuan memakan waktu > 180 detik. | Kontak darurat 113 dan nomor telepon 6 posko siaga kecamatan dapat diakses hanya dalam 1 kali ketukan langsung (*zero-latency touchpoint*) dalam waktu < 3 detik. | Memenuhi batasan waktu kritis tanggap darurat dan hukum Fitts: target aksi darurat dibuat besar dan ditempatkan pada area yang paling mudah dijangkau. |
| 8 | Advancing the User Experience | Kepuasan pengguna (*User Satisfaction*) | Skor kepuasan awal pada survei pendahuluan sangat rendah, yakni rerata 2,70 dari 5,00 dengan indikator visual hanya 2,23. | Skor kepuasan sesudah redesain melonjak menjadi 4,57 (+1,94) pada model evaluasi WebQual 4.0, menunjukkan penerimaan pengguna yang sangat tinggi. | Desain yang intuitif dan responsif secara langsung mendongkrak kepuasan subjektif pengguna (*Usability & Service Satisfaction*). |
| 9 | Advancing the User Experience | Permasalahan UX lainnya (Dead Links & Broken Assets) | Tautan ikon media sosial tidak berfungsi (*dead links*); tautan unduhan dokumen menghasilkan galat *404 Not Found*; korsel gambar berputar tanpa tombol kontrol. | Seluruh tautan terverifikasi aktif; berkas PDF terhubung dengan simulasi unduh langsung; korsel hero dilengkapi tombol navigasi manual dan penanda titik (*dots*). | Menerapkan prinsip *Error Prevention* dan *User Control and Freedom*: mengeliminasi jalan buntu yang membuat pengguna frustrasi. |
| 10 | The Timely User Experiences | Konteks penggunaan (*Context of Use*) | Antarmuka lama tidak membedakan antara kebutuhan warga yang sedang panik menghadapi kebakaran dengan warga yang mencari info perizinan. | Antarmuka memisahkan secara tegas dua jalur penggunaan: jalur cepat darurat (*top emergency bar & sticky call*) dan jalur publik e-government. | Memenuhi prinsip UCD *Understand Context of Use*: antarmuka harus adaptif terhadap kondisi psikologis dan tujuan spesifik pengguna saat mengakses sistem. |
| 11 | The Timely User Experiences | Ketepatan waktu informasi (*Information Timeliness*) | Informasi tanggal berita tidak tertata; data rekapitulasi insiden kebakaran terakhir yang ditampilkan sudah usang (tahun 2022). | Menampilkan data statistik operasional mutakhir tahun 2024 dan 2025 serta berita operasi pemadaman dan rescue dengan timestamp terperinci. | Dimensi *Information Quality* WebQual 4.0: informasi keselamatan publik wajib menyajikan data mutakhir (*up-to-date*) dan akurat. |
| 12 | The Timely User Experiences | Respons sistem terhadap kondisi pengguna | Tidak ada kanal cepat bagi pengguna gawai seluler; tampilan web tidak responsif dan teks mengecil pada layar ponsel. | Desain responsif mobile-first; tombol darurat seluler dioptimalkan untuk ukuran ibu jari (minimal 44 x 44 piksel) sesuai kaidah Fitts. | Mendukung akses cepat pengguna seluler di lapangan yang membutuhkan pertolongan langsung dari lokasi bencana. |
| 13 | The Timely User Experiences | Informasi/fitur yang dibutuhkan pada saat tertentu | Informasi nomor telepon posko darurat kecamatan dihilangkan dari situs lama; warga di wilayah pinggiran tidak tahu posko terdekat. | Menyediakan direktori 6 Posko Siaga Kecamatan (Kedaton, Sukarame, Kemiling, Panjang, Teluk Betung, Tanjung Karang) lengkap dengan alamat dan nomor kontak langsung. | Prinsip *The Timely User Experience*: menyajikan informasi yang tepat pada momen genting saat pengguna berada di zona wilayah bencana tertentu. |
| 14 | Information Search | Search/pencarian (*Search Bar*) | Kotak pencarian tersembunyi di bagian sidebar bawah; ukuran input sempit; tidak memiliki kontras warna yang memadai. | Bilah pencarian *Sticky Expandable* pada navbar atas serta bilah pencarian *In-Page Full-Width* pada modul Berita, Dokumen, dan FAQ. | Meningkatkan *Visibility of Search*: bilah pencarian harus menjadi penanda (*signifier*) yang jelas di setiap level penjelajahan. |
| 15 | Information Search | Search suggestion/autocomplete | Kotak pencarian hanya berupa teks HTML biasa; tidak memiliki teks penuntun (*contextual placeholder*) atau saran kata kunci. | *Contextual Placeholder* dinamis memberikan contoh kueri populer (misal: "Ketik kata kunci: 113, ular, tawon, LKJIP, hidran..."). | Menerapkan prinsip *Recognition rather than Recall* (Nielsen H6): memandu kueri pencarian tanpa membebani daya ingat pengguna. |
| 16 | Information Search | Search result (Hasil Pencarian) | Hasil pencarian lambat (2–4 detik), memicu reload seluruh halaman, dan menampilkan artikel tanpa highlight kecocokan. | Hasil pencarian tampil instan (< 100 ms) di sisi klien memanfaatkan *React useMemo*, disertai counter dinamis jumlah hasil yang ditemukan. | Memaksimalkan kecepatan temu kembali informasi (*Information Retrieval Efficiency*) dan menjaga konteks kerja pengguna. |
| 17 | Information Search | Filter (Penyaringan Multi-Kategori) | Tidak tersedia fasilitas penyaringan kategori; berita pemadaman, pengumuman seremonial, dan regulasi bercampur jadi satu. | Tombol kapsul (*pill category buttons*) interaktif multi-kategori dengan kontras warna aktif biru solid dan atribut aksesibilitas `aria-pressed`. | Memberikan kendali pemilahan konten yang fleksibel bagi pengguna (*Direct Manipulation & User Control*). |
| 18 | Information Search | Sorting (Pengurutan Informasi) | Data tersusun kaku berdasarkan tanggal entri database lama; pengguna tidak memiliki opsi memilih urutan penyajian. | Menyediakan penataan urutan data berdasarkan temporalitas (terbaru), popularitas pembaca, dan tingkat urgensi (Lencana Darurat/Penting). | Mempermudah penemuan artikel relevan dan edaran kedinasan darurat secara terstruktur. |
| 19 | Information Search | Navigasi dalam menemukan informasi | Menu navigasi kaku tanpa rekam jejak (*breadcrumbs*); saat masuk sub-halaman, pengguna tersesat dan bingung kembali. | Dilengkapi *breadcrumbs* dinamis di seluruh sub-halaman, penanda menu aktif (*active route indicator*), dan navigasi bertingkat yang rapi. | Menerapkan konsep *Fluid Navigation & Wayfinding*: memberikan kejelasan posisi pengguna di dalam hierarki arsitektur informasi situs. |
| 20 | Information Search | No-result/error/feedback | Saat kata kunci tidak cocok, halaman menampilkan layar kosong bertuliskan "No Results" yang memutus alur penelusuran. | Menghadirkan *Rich Empty State* lengkap dengan ilustrasi tematik, pesan panduan ramah pengguna, serta tombol aksi pemulihan 1-klik "*Reset Filter*". | Menerapkan prinsip *Help Users Recognize, Diagnose, and Recover from Errors* (Nielsen H9): mencegah terjadinya jalan buntu interaksi. |
| 21 | Data Visualization | Jenis visualisasi | Website eksisting sama sekali tidak menyediakan visualisasi data statistik; data bencana hanya tertulis sporadis di artikel berita. | Widget statistik komparatif angka kejadian kebakaran, aksi penyelamatan rescue, armada siaga, dan rata-rata waktu tanggap. | Visualisasi data mempermudah pemahaman kognitif masyarakat terhadap skala penanganan kebencanaan perkotaan. |
| 22 | Data Visualization | Penyajian informasi/data | Data disajikan dalam bentuk teks panjang paragraf birokratis yang melelahkan untuk dibaca (*text-heavy*). | Disajikan dalam kartu metrik ringkas (*stat cards*) dengan ikon representatif (Lucide React) dan angka ukuran besar yang terbaca sekilas (*skimmable*). | Mengurangi beban kognitif pembaca dan mempercepat pemrosesan informasi publik. |
| 23 | Data Visualization | Kejelasan grafik/indikator | Tidak terdapat indikator visual penjelas status waktu tanggap atau volume penanganan insiden. | Kartu metrik dilengkapi tipografi penjelas tahun data (2024 dan 2025) serta label ketercapaian SPM Permendagri 114 (< 15 Menit). | Menjamin transparansi dan akuntabilitas data kinerja pemerintah daerah sesuai prinsip e-government. |
| 24 | Data Visualization | Label/legend | Tidak ada label fungsional penjelas kategori layanan penanggulangan kebakaran vs penyelamatan non-kebakaran. | Pemberian label tegas pembeda antara "Insiden Kebakaran", "Aksi Penyelamatan (Rescue)", "Armada Siaga", dan "Posko Siaga". | Mencegah salah tafsir publik mengenai ruang lingkup tugas pemadam kebakaran modern yang mencakup tugas rescue. |
| 25 | Data Visualization | Efektivitas visualisasi | Data kinerja dinas tersembunyi dalam berkas PDF internal yang tidak dapat diakses masyarakat umum di web. | Visualisasi langsung di beranda membuktikan transparansi kinerja operasional dan membangun rasa percaya publik (*Reflective Design*). | Meningkatkan dimensi *Information Quality* dan *Trustworthiness* pada evaluasi WebQual 4.0. |
| 26 | Wireframe, Mockup & Prototype | Wireframe (Rendah Fidelitas) | Perancangan website eksisting lama tidak terdokumentasi dan tidak melalui tahap wireframing terstruktur. | Disusun kerangka tata letak monokromatik (*low-fidelity wireframe*) 5 modul utama untuk menguji proporsi ruang, hierarki teks, dan Fitts's Law. | Memastikan fondasi tata letak dan alur fungsional matang sebelum masuk ke tahap pemberian warna dan ornamen grafis. |
| 27 | Wireframe, Mockup & Prototype | Mockup (Menengah Fidelitas) | Desain lama mengabaikan sistem token visual; warna tombol tidak harmonis dan rasio kontras tidak teruji. | Mockup visual dirancang menggunakan sistem desain terstandarisasi: palet warna semantik (*Primary Navy* & *Emergency Red*) serta tipografi Inter sans-serif. | Menjamin pemenuhan aksesibilitas visual WCAG 2.1 Level AA dengan rasio kontras minimal 4,5:1. |
| 28 | Wireframe, Mockup & Prototype | Alur/interaksi prototype | Tidak tersedia purwarupa interaktif yang dapat diuji coba alurnya oleh pengguna sebelum rilis. | Purwarupa interaktif fungsional dikembangkan pada lingkungan web Next.js/Tailwind CSS yang dapat disimulasikan secara nyata di desktop dan mobile. | Memfasilitasi validasi alur tugas pengguna (*task scenario flow*) pada situasi krisis darurat dan pelayanan normal. |
| 29 | High-Fidelity Prototype | Detail antarmuka (*Interface Detail*) | Antarmuka lama kasar, batas tabel tajam, tidak ada efek bayangan lembut (*box shadow*), dan tidak ada transisi halus. | Menggunakan sistem kartu modern dengan radius sudut membulat (*rounded-xl*), bayangan halus (*subtle shadow*), serta transisi warna tombol 200ms. | Meningkatkan daya tarik estetika visual (indikator U5 WebQual) yang terbukti mendongkrak skor dari 2,40 menjadi 4,45. |
| 30 | High-Fidelity Prototype | Konsistensi desain (*Design Consistency*) | Antarmuka tidak konsisten; gaya tombol di beranda berbeda dengan tombol di halaman kontak dan galeri. | Seluruh komponen tombol, kartu, input teks, dan tajuk menggunakan komponen modul yang dapat digunakan kembali (*reusable React components*). | Menerapkan prinsip *Consistency and Standards* (Nielsen H4): konsistensi antarmuka mempercepat kurva pembelajaran pengguna. |
| 31 | High-Fidelity Prototype | Interaksi prototype (*Interactive State*) | Formulir kontak statis; tombol kirim tidak memberikan tanda saat proses pengiriman data; tidak ada dialog konfirmasi. | Formulir dilengkapi validasi input real-time, dialog modal konfirmasi sebelum kirim, animasi spinner saat mengirim, dan nomor tiket aduan resmi. | Menerapkan prinsip *Error Prevention* (Nielsen H5) dan *Closure*: memberi kepastian penuh bahwa laporan warga telah diterima dinas. |
| 32 | High-Fidelity Prototype | Penyelesaian desain keseluruhan | Desain lama terabaikan sejak 2022, banyak fitur rusak, tidak ada modul FAQ, dan navigasi seluler berantakan. | Desain terintegrasi utuh pada 5 modul utama (Beranda, Berita, Dokumen, Galeri, Kontak) + Modul Profil & FAQ; responsif 100% di semua gawai. | Mewujudkan portal e-government darurat kebencanaan standar publikasi ilmiah yang memenuhi seluruh pilar UCD ISO 9241-210:2019. |
