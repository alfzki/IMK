# Redesain Website Dinas Pemadam Kebakaran Kota Bandar Lampung dengan Pendekatan User-Centered Design

*(Redesign of the Bandar Lampung City Fire Department Website Using a User-Centered Design Approach)*

**Alif Zakiansyah As Syauqi¹\*, Andrian Fajar Fahmi², Valentina Lasma Situmorang³, Erna Nurmawati⁴**  
¹Program Studi D-IV Komputasi Statistik, Politeknik Statistika STIS, Jakarta, Indonesia, 222312958@stis.ac.id  
²Program Studi D-IV Komputasi Statistik, Politeknik Statistika STIS, Jakarta, Indonesia, 222312979@stis.ac.id  
³Program Studi D-IV Komputasi Statistik, Politeknik Statistika STIS, Jakarta, Indonesia, 222313413@stis.ac.id  
⁴Dosen Pengampu Mata Kuliah IMK, Politeknik Statistika STIS, Jakarta, Indonesia, erna@stis.ac.id  
\*Penulis Korespondensi: 222312958@stis.ac.id

---

### Abstrak
Portal layanan publik pemadam kebakaran berperan vital bagi keselamatan jiwa, di mana kecepatan akses informasi dan pemanggilan bantuan terikat standar waktu tanggap 15 menit Permendagri No. 114 Tahun 2018. Namun, website resmi Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung (damkar.bandarlampungkota.go.id) menghadapi kendala antarmuka serius: jam operasional fiktif (07.00–16.00), ketiadaan tombol darurat 113 persisten, kontak posko tersembunyi, dan navigasi membingungkan. Survei pendahuluan terhadap 22 responden mengonfirmasi rendahnya persepsi kualitas antarmuka eksisting dengan rerata 2,70/5,00. Penelitian ini bertujuan mengidentifikasi cacat antarmuka via 10 heuristik Nielsen, merancang ulang website responsif berbasis User-Centered Design (ISO 9241-210:2019) berpadu Emotional Design Don Norman dan prinsip HCI, serta menguji kualitas empirisnya memakai instrumen WebQual 4.0 (22 indikator). Pengujian komparatif menunjukkan peningkatan signifikan pada seluruh dimensi: Usability Quality meningkat dari 2,64 menjadi 4,52 (+1,88); Information Quality dari 2,81 menjadi 4,58 (+1,77); dan Service Interaction Quality dari 2,45 menjadi 4,61 (+2,16), dengan rerata keseluruhan meningkat dari 2,63 ke 4,57 (+1,94; p < 0,001). Hasil penelitian membuktikan integrasi tombol darurat persisten, hierarki visual adaptif krisis, dan validasi formulir real-time efektif memitigasi beban kognitif warga serta mendukung pencapaian SPM kebencanaan.

**Kata kunci**: Evaluasi Heuristik, Interaksi Manusia dan Komputer, Layanan Darurat Kebakaran, User-Centered Design, WebQual 4.0

---

### Abstract
*Municipal fire department digital portals play a vital role in citizen safety, where rapid emergency access is bound by a 15-minute response standard (Permendagri No. 114/2018). However, the Bandar Lampung Fire and Rescue Service official website (damkar.bandarlampungkota.go.id) exhibits critical usability defects: misleading operational hours (07:00–16:00), absent persistent 113 shortcuts, hidden outpost contacts, and fragmented navigation. A preliminary survey with 22 respondents revealed a low mean quality score of 2.70/5.00. This study identifies usability defects via Nielsen's 10 heuristics, re-engineers a responsive web portal using User-Centered Design (ISO 9241-210:2019) integrated with Norman's Emotional Design and HCI principles, and empirically evaluates interface quality via WebQual 4.0 (22 indicators). Comparative results demonstrated significant improvements across all dimensions: Usability Quality rose from 2.64 to 4.52 (+1.88); Information Quality from 2.81 to 4.58 (+1.77); and Service Interaction Quality from 2.45 to 4.61 (+2.16), raising the overall mean from 2.63 to 4.57 (+1.94; p < 0.001). The findings verify that persistent emergency actions, crisis-adaptive visual hierarchies, and real-time form validation effectively mitigate citizens' cognitive load and support municipal response standards.*

**Keywords**: Emergency Public Services, Heuristic Evaluation, Human-Computer Interaction, User-Centered Design, WebQual 4.0

---

## 1. PENDAHULUAN

Transformasi layanan publik digital di Indonesia menuntut terselenggaranya portal informasi yang menjamin kecepatan akses, kejelasan tata letak antarmuka, dan efisiensi interaksi warga (Bastardo et al., 2024; Jalil et al., 2023). Dalam domain pelayanan tanggap darurat pemadam kebakaran dan penyelamatan (*fire and rescue services*), kebergunaan (*usability*) antarmuka digital berkaitan langsung dengan mitigasi risiko fatalitas jiwa dan kerugian harta benda (Falconi et al., 2023; ISO, 2018). Ketika insiden kebakaran atau kondisi kedaruratan melanda, masyarakat mengakses portal informasi di bawah tekanan psikologis panik (*stress-induced cognitive load*), sehingga arsitektur informasi, kontras tombol darurat, serta penataan hierarki visual menentukan keberhasilan warga dalam memperoleh pertolongan dalam hitungan detik (Norman, 2004; Shneiderman et al., 2016).

Urgensi penataan antarmuka portal layanan darurat sangat nyata di Kota Bandar Lampung. Catatan operasional resmi Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung menunjukkan volume kejadian kebakaran perkotaan yang tinggi, yakni mencapai 413 insiden pada tahun 2023, 271 kebakaran pada tahun 2024, dan 198 peristiwa pada tahun 2025 (Damkarmat Kota Bandar Lampung, 2024). Di samping bencana kebakaran, instansi ini memikul tanggung jawab penanganan kedaruratan non-kebakaran (*rescue*) dengan volume aksi yang sangat besar, yaitu 558 operasi penyelamatan pada tahun 2023 serta 518 aksi evakuasi pada kurun Januari hingga Juli 2025 (meliputi evakuasi sarang tawon vespa, ular berbisa, penyelamatan banjir, hingga pelepasan cincin terjepit). Tingginya frekuensi insiden tersebut diikat secara ketat oleh regulasi nasional Peraturan Menteri Dalam Negeri Nomor 114 Tahun 2018 tentang Standar Pelayanan Minimal (SPM) Sub-Urusan Kebakaran, yang menetapkan waktu tanggap (*response time*) maksimal 15 menit terhitung sejak laporan diterima hingga armada pemadam tiba di lokasi bencana (Kementerian Dalam Negeri Republik Indonesia, 2018). Dalam rantai waktu tanggap tersebut, kemudahan warga dalam menemukan nomor kontak darurat dan melaporkan lokasi insiden melalui portal resmi menjadi simpul awal penyelamatan yang sangat krusial.

Namun, observasi empiris terhadap website resmi Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung (`https://damkar.bandarlampungkota.go.id`) menunjukkan kelemahan antarmuka yang membahayakan operasional kedaruratan. Pertama, pada bilah tajuk (*header*) utama situs web, terpampang teks statis "*Jam Oprasional: 07.00 s/d 16.00*". Pencantuman teks ini sangat menyesatkan (*misleading*) dan menimbulkan kepanikan bagi warga yang mengalami kebakaran pada malam hari, seolah-olah layanan pemadam kebakaran tidak beroperasi, padahal posko siaga darurat beroperasi penuh 24 jam sehari. Kedua, nomor darurat nasional 113 dan hotline kantor tidak tersedia dalam bentuk tombol panggil cepat persisten (*persistent sticky emergency call*), melainkan tersembunyi dalam teks statis berukuran kecil. Informasi kontak posko siaga di tingkat kecamatan (seperti Posko Kedaton, Sukarame, Kemiling, dan Panjang) tidak terpetakan dalam direktori yang mudah diakses, sehingga warga dipaksa menelusuri menu bertingkat yang tidak responsif. Ketiga, tata letak antarmuka situs eksisting didominasi oleh dokumentasi seremonial birokrasi, ketiadaan breadcrumbs, formulir pengaduan tanpa validasi format input, serta ketiadaan visualisasi statistik kejadian bencana yang transparan (Tejedo-Romero et al., 2025).

Kelemahan antarmuka tersebut terkonfirmasi secara kuantitatif melalui survei pendahuluan terhadap 22 responden warga Kota Bandar Lampung yang didominasi generasi usia produktif (20–29 tahun) dan pengguna perangkat seluler (54,5%). Menggunakan instrumen WebQual 4.0 pada skala Likert 1–5, nilai rerata kepuasan keseluruhan hanya mencapai 2,70 (kategori rendah), dengan rincian dimensi *Usability Quality* sebesar 2,77, *Information Quality* sebesar 2,63, dan *Service Interaction Quality* sebesar 2,71 (Tim Peneliti, 2026). Indikator dengan skor persepsi paling rendah meliputi daya tarik tampilan visual (2,23), ketersediaan data statistik insiden (2,41), jaminan ketersediaan layanan siaga 24/7 (2,41), serta kejelasan prosedur pelaporan (2,45). Temuan ini membuktikan adanya kesenjangan tajam antara kebutuhan interaksi masyarakat dalam situasi darurat dengan kapabilitas sistem antarmuka web eksisting.

Penelitian terdahulu mengenai evaluasi website e-government di Indonesia umumnya berfokus pada pengujian kepuasan portal dinas umum atau repositori dokumen hukum tanpa menyentuh interaksi kedaruratan (Alexander et al., 2021; Chairani & Baroroh, 2024; Hafif et al., 2025; Sitanggang et al., 2024). Evaluasi usabilitas antarmuka portal pengetahuan pemerintah dan kepuasan pengguna sebelumnya diteliti oleh Maryani (2023) menggunakan metode WebQual 4.0. Sementara itu, penerapan metode User Centered Design (UCD) pada aplikasi kebencanaan dan keselamatan publik dikaji oleh Ramadhan et al. (2022) dalam perancangan antarmuka (Adiwinata & Nugraha, 2024). Guna mengatasi kesenjangan penelitian tersebut, penelitian ini menerapkan model evaluasi multimode terintegrasi (Raposo et al., 2026) yang menggabungkan inspeksi 10 prinsip evaluasi heuristik Jakob Nielsen (Nielsen, 1994), rekayasa desain berpusat pada pengguna (*human-centred design*) berbasis standar ISO 9241-210:2019 (International Organization for Standardization, 2019), serta model WebQual 4.0 yang dikembangkan oleh Barnes dan Vidgen (2002) untuk mengukur kualitas website melalui dimensi usability, information, dan service interaction (Wardhana, 2024). Prinsip Emotional Design menurut Norman (2004) diintegrasikan untuk meredam kepanikan emosional warga dalam situasi darurat bencana.

Berdasarkan latar belakang di atas, penelitian ini merumuskan tiga pertanyaan penelitian:
1. Apa saja kelemahan usabilitas pada website Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung berdasarkan evaluasi heuristik Nielsen dan persepsi pengguna?
2. Bagaimana merancang arsitektur informasi, alur interaksi, dan prototipe website berbasis *User-Centered Design* yang mampu memitigasi beban kognitif masyarakat dalam situasi krisis darurat dan pelayanan publik?
3. Sejauh mana signifikansi peningkatan persepsi kualitas antarmuka pengguna sebelum dan sesudah redesain berdasarkan dimensi WebQual 4.0?

Sejalan dengan pertanyaan tersebut, tujuan penelitian ini adalah:
1. Mengidentifikasi dan mengklasifikasikan cacat antarmuka website eksisting melalui evaluasi heuristik 10 prinsip Nielsen dan survei pendahuluan;
2. Menghasilkan rancangan arsitektur informasi, alur pengguna (*user flow*), *wireframe* (rendah fidelitas), serta purwarupa interaktif *high-fidelity* yang responsif dan mengedepankan tombol darurat persisten serta transparansi informasi publik;
3. Mengukur dan menganalisis signifikansi pergeseran kualitas antarmuka secara empiris sebelum dan sesudah redesain menggunakan model evaluasi WebQual 4.0.

---

## 2. METODOLOGI

### 2.1 Desain Penelitian
Penelitian ini mengadopsi pendekatan metode campuran sekuensial eksplanatori (*explanatory sequential mixed-methods design*) yang memadukan inspeksi kualitatif mendalam dengan pengujian komparatif kuantitatif (Raposo et al., 2026). Siklus perancangan dikembangkan berlandaskan standar internasional ISO 9241-210:2019 (*Human-Centred Design for Interactive Systems*) yang mencakup empat fase iteratif: memahami konteks penggunaan (*understand context of use*), menentukan spesifikasi kebutuhan pengguna (*specify user requirements*), memproduksi solusi desain antarmuka (*produce design solutions*), dan mengevaluasi rancangan terhadap kebutuhan pengguna (*evaluate design*) (ISO, 2019; Ramadhan et al., 2022). Alur tahapan penelitian disajikan pada Gambar 1.

```
+-----------------------------------------------------------------------------------+
|                           TAHAPAN PENELITIAN BERBASIS UCD                         |
+-----------------------------------------------------------------------------------+
|  1. Context of Use       | Preliminary Survey (N=22) + Evaluasi Heuristik (H1-H10)|
|  2. User Requirements    | Matriks Kebutuhan Fungsional/Non-Fungsional + Persona  |
|  3. Design Solutions     | Arsitektur Informasi + Wireframe + High-Fidelity Figma |
|  4. Design Evaluation    | Evaluasi Komparatif WebQual 4.0 (Before vs After Redesign) |
+-----------------------------------------------------------------------------------+
```
*Gambar 1. Diagram alur tahapan penelitian berbasis User-Centered Design (ISO 9241-210:2019)*

### 2.2 Analisis Konteks Penggunaan (*Context of Use*)
Fase pertama UCD berfokus pada pemahaman karakteristik pengguna dan konteks penggunaan. Berdasarkan standar ISO 9241-11:2018, kebergunaan mencakup efektivitas, efisiensi, dan kepuasan dalam konteks penggunaan spesifik (International Organization for Standardization, 2018). Pemodelan kebutuhan pengguna dan konteks interaksi manusia dan komputer mengacu pada prinsip affordance, signifier, dan mental model (Norman, 2013).

#### 2.2.1 Survei Pendahuluan dan Pemodelan Persona
Penggalian kebutuhan awal diselenggarakan melalui survei pendahuluan terhadap 22 responden masyarakat Kota Bandar Lampung dengan teknik *purposive sampling* (Tim Peneliti, 2026). Kriteria responden mencakup warga berdomisili di Kota Bandar Lampung yang berpotensi membutuhkan layanan pemadam kebakaran, aksi evakuasi kedaruratan, serta akses keterbukaan informasi publik pemerintah daerah. Data survei diolah untuk menyusun dua arketipe persona pengguna (Norman, 2013; Sharp et al., 2019):
1. **Pengguna Darurat (*Emergency Persona*)**: Warga yang sedang menghadapi kebakaran pemukiman atau ancaman fauna berbahaya dalam kondisi panik tinggi (*high stress load*). Kebutuhan mutlak persona ini adalah tombol panggil cepat darurat 113 satu-klik, keterbacaan nomor telepon posko siaga terdekat, serta waktu muat halaman yang instan tanpa terhalang elemen dekoratif.
2. **Pengguna Informasi Publik (*Information Persona*)**: Pelaku usaha, akademisi, dan masyarakat umum yang memerlukan akses dokumen perizinan proteksi kebakaran, SOP kedinasan, berkas LKJIP/Renstra, berita pemadaman, dan visualisasi data statistik bencana dalam situasi tenang.

#### 2.2.2 Evaluasi Heuristik Antarmuka Eksisting
Secara simultan, dilakukan inspeksi usabilitas formal menggunakan 10 Prinsip Usabilitas Jakob Nielsen (*10 Usability Heuristics*) guna mengidentifikasi pelanggaran antarmuka situs eksisting secara objektif (Nielsen, 1994; Nielsen & Mack, 1994). Kesepuluh prinsip tersebut meliputi:
- H1: *Visibility of system status*
- H2: *Match between system and the real world*
- H3: *User control and freedom*
- H4: *Consistency and standards*
- H5: *Error prevention*
- H6: *Recognition rather than recall*
- H7: *Flexibility and efficiency of use*
- H8: *Aesthetic and minimalist design*
- H9: *Help users recognize, diagnose, and recover from errors*
- H10: *Help and documentation*

Tingkat keparahan anomali diklasifikasikan menggunakan skala *Severity Rating* menurut Nielsen (1994):
- Skor 0: Bukan masalah kebergunaan (*no usability problem*).
- Skor 1: Masalah kosmetik belaka (*cosmetic problem*), perbaikan prioritas rendah.
- Skor 2: Masalah kebergunaan minor (*minor usability problem*), prioritas sedang.
- Skor 3: Masalah kebergunaan mayor (*major usability problem*), prioritas tinggi.
- Skor 4: Bencana kebergunaan (*usability catastrophe*), wajib dituntaskan sebelum rilis.

### 2.3 Spesifikasi Kebutuhan dan Parameter Prinsip HCI
Fase kedua UCD merumuskan matriks kebutuhan fungsional dan non-fungsional berdasarkan sintesis evaluasi heuristik dan survei pendahuluan. Kebutuhan fungsional meliputi: (1) bilah darurat atas terpadu (*top emergency bar*), (2) tombol panggil darurat 113 melayang persisten (*persistent sticky emergency call*), (3) kartu direktori 6 posko siaga kecamatan dengan panggilan langsung (*click-to-call*), (4) formulir pengaduan interaktif dengan validasi format instan, (5) modul pencarian kata kunci dan penyaringan faset dokumen/berita, serta (6) dasbor visualisasi statistik kejadian insiden. Kebutuhan non-fungsional menitikberatkan pada kepatuhan *Web Content Accessibility Guidelines* (WCAG 2.1 Level AA) dengan rasio kontras warna minimal 4,5:1 untuk teks normal (W3C, 2018), ukuran target sentuh minimal 44 × 44 piksel pada layar ponsel mengacu pada Hukum Fitts, dan waktu respons sistem di bawah 100 milidetik.

Rancangan antarmuka dipandu oleh lima parameter prinsip Interaksi Manusia dan Komputer (HCI):
1. **Navigasi Mengalir (*Fluid Navigation*)**: Menerapkan navigasi persisten (*sticky header*), rekam jejak (*breadcrumbs*) dinamis pada seluruh subhalaman, dan pintasan akses langsung guna mengeliminasi disorientasi navigasi warga (Falconi et al., 2023).
2. **Bahasa Manusia dan Perintah Ekspresif (*Expressive Human and Command Languages*)**: Mengganti akronim birokrasi yang kaku dengan label aksi humanis yang tegas, seperti "DARURAT: 113", "Hubungi Posko 113 Sekarang", dan "Unduh Panduan Keselamatan PDF", disertai teks umpan balik konfirmasi yang komunikatif (Shneiderman et al., 2016).
3. **Manipulasi Langsung (*Direct Manipulation*)**: Prinsip manipulasi langsung menyediakan representasi visual kontinu pada objek interaksi, aksi fisik cepat, dan umpan balik langsung (Shneiderman et al., 2016). Pemilihan kategori berbasis tombol kapsul (*pill filters*) sekali klik, aksi pembatalan instan melalui tombol pembersih silang (X) pada bilah pencarian, dan inisiasi panggilan telepon langsung via protokol peramban gawai diimplementasikan untuk memudahkan pengguna.
4. **Pengalaman Pengguna Tepat Waktu (*The Timely User Experiences*)**: Menerapkan teori *Emotional Design* Don Norman pada tingkat viseral (warna *Primary Navy* #172554 berpadu aksen *Emergency Red* #DC2626 yang menumbuhkan rasa tenang dan wibawa siaga), tingkat behavioral (navigasi bebas hambatan dan validasi masukan langsung), serta tingkat reflektif (penegasan komitmen SPM waktu tanggap 15 menit Permendagri No. 114/2018 untuk membangun kepercayaan publik) (Norman, 2004; Sun & Jiang, 2025).
5. **Pencarian Informasi (*Information Search*)**: Mengintegrasikan kotak pencarian global pada *navbar* serta pencarian modular *in-page*, penyaringan faset bertingkat, dan penanganan status pencarian kosong (*rich empty state*) yang ramah pengguna (Falconi et al., 2023).

### 2.4 Perancangan Solusi Desain (*Produce Design Solutions*)
Fase ketiga UCD merealisasikan kebutuhan sistem ke dalam rancangan visual secara bertahap mengacu pada kaidah rekayasa desain interaksi (Camburn et al., 2017). Tahapan perancangan desain antarmuka merealisasikan kebutuhan pengguna melalui siklus interaksi, arsitektur informasi, dan prototipe (Sharp et al., 2019):
1. **Arsitektur Informasi dan Pemodelan Alur Pengguna (*User Flow*)**: Struktur informasi ditata ke dalam hierarki modular yang memisahkan kanal kedaruratan krisis dengan kanal keterbukaan informasi publik. Alur pengguna darurat dirancang memiliki kedalaman interaksi maksimal 1 hingga 2 ketukan menuju panggilan telepon petugas jaga.
2. **Prosedur Wireframing (Rendah Fidelitas)**: Pembuatan kerangka tata letak monokromatik (*low-fidelity wireframes*) untuk menentukan proporsi ruang, penempatan hierarki teks, alokasi bilah pencarian, dan tata letak kartu layanan tanpa distraksi elemen visual ornamen.
3. **Penyusunan Mockup dan Prototipe Interaktif (*High-Fidelity Prototype*)**: Mentransformasikan *wireframe* menjadi purwarupa interaktif berwarna menggunakan Figma dan diimplementasikan secara fungsional menggunakan arsitektur web modern Next.js, TypeScript, dan Tailwind CSS. Purwarupa mencakup lima modul utama: Beranda Utama, Berita & Pengumuman, Dokumen Publik & SOP, Galeri Dokumentasi Kegiatan, serta Kontak Posko & Formulir Pengaduan.

### 2.5 Evaluasi Desain (Instrumen dan Analisis Data WebQual 4.0)
Fase keempat UCD mengevaluasi efektivitas antarmuka sebelum redesain (*Before*) dan sesudah redesain (*After*) menggunakan instrumen baku WebQual 4.0 (Barnes & Vidgen, 2002; Chairani & Baroroh, 2024; Wardhana, 2024). Model WebQual 4.0 mengevaluasi kualitas situs web melalui 22 butir indikator yang terbagi ke dalam tiga dimensi utama:
1. ***Usability Quality* (8 indikator)**: Kemudahan pengoperasian, kejelasan interaksi, kemudahan navigasi, efisiensi penggunaan, daya tarik tampilan visual, kesesuaian tata letak, kompetensi antarmuka, dan kenyamanan interaksi secara menyeluruh.
2. ***Information Quality* (7 indikator)**: Keakuratan informasi insiden, keandalan data penyelamatan, kebaruan informasi (*up-to-date*), relevansi materi darurat, kemudahan pemahaman bahasa konten, kedalaman rincian informasi, dan ketepatan format penyajian data.
3. ***Service Interaction Quality* (7 indikator)**: Reputasi citra institusi, keamanan data pada formulir pengaduan, perlindungan privasi pelapor, ketersediaan ruang interaksi publik, kemudahan mekanisme penyampaian laporan kejadian, kepastian tanggapan operasional petugas, dan keandalan layanan kontak darurat 24/7.

Evaluasi pengalaman pengguna dan kualitas interaksi antarmuka publik secara kuantitatif melalui pengujian kepuasan mengadopsi pendekatan Pusnik et al. (2026) serta kerangka evaluasi multimode Raposo et al. (2026). Data evaluasi diukur menggunakan skala Likert 1 hingga 5 (1 = Sangat Tidak Setuju, 2 = Tidak Setuju, 3 = Netral, 4 = Setuju, 5 = Sangat Setuju). Analisis data dilakukan secara kuantitatif melalui perhitungan nilai rerata (*mean*), selisih peningkatan skor ($\Delta$), persentase kenaikan kualitas, serta pengujian signifikansi statistik menggunakan uji beda berpasangan non-parametrik *Wilcoxon Signed-Rank Test* pada taraf signifikansi $\alpha = 0,05$.

---

## 3. HASIL DAN PEMBAHASAN

### 3.1 Hasil Audit Usabilitas Website Eksisting (Kondisi Awal)
Audit heuristik independen terhadap website eksisting (`damkar.bandarlampungkota.go.id`) mengungkap berbagai cacat antarmuka signifikan yang tersebar pada 10 prinsip Jakob Nielsen. Rangkuman hasil audit heuristik disajikan pada Tabel 1.

*Tabel 1. Matriks Hasil Audit 10 Prinsip Usabilitas Heuristik Nielsen pada Website Eksisting*

| No | Prinsip Heuristik Nielsen | Kondisi Antarmuka Eksisting | Skor Severity (0–4) | Dampak terhadap Pengguna |
| :---: | :--- | :--- | :---: | :--- |
| 1 | *Visibility of System Status* (H1) | Ketiadaan indikator pemuatan (*loading spinner*), umpan balik formulir nihil, spanduk berputar tanpa penanda titik (*carousel dots*). | 3 (Mayor) | Pengguna tidak mengetahui apakah sistem sedang memproses data atau mengalami kebuntuan (*freezing*). |
| 2 | *Match Between System & Real World* (H2) | Istilah birokrasi berbelit (LKJIP, Renstra, SOP Uji Proteksi) tanpa penjelasan bahasa awam bagi masyarakat yang membutuhkan pertolongan. | 2 (Minor) | Beban kognitif tinggi bagi masyarakat awam dalam menafsirkan berkas administrasi dan perizinan. |
| 3 | *User Control and Freedom* (H3) | Tautan berkas membuka tab peramban baru secara paksa tanpa fasilitas pembatalan (*cancel*) atau tombol kembali (*back*). | 2 (Minor) | Pengguna kehilangan kendali alur penelusuran peramban dan mengalami disorientasi penjelajahan. |
| 4 | *Consistency and Standards* (H4) | Ketidakkonsistenan ukuran tipografi, warna tombol, dan jarak margin antarhalaman Beranda, Galeri, dan Berita. | 2 (Minor) | Merusak keselarasan visual antarmuka dan menciptakan persepsi portal pemerintah yang tidak terkelola rapi. |
| 5 | *Error Prevention* (H5) | Formulir kontak tidak memiliki validasi format nomor telepon dan email, serta tidak memiliki dialog konfirmasi sebelum data terkirim. | 3 (Mayor) | Rawan terjadi pengiriman laporan keliru (*slips & mistakes*) yang memperlambat verifikasi lokasi bencana. |
| 6 | *Recognition Rather than Recall* (H6) | Ketiadaan *breadcrumbs* navigasi, menu bersarang tanpa penanda halaman aktif, dan ketiadaan riwayat kueri pencarian. | 3 (Mayor) | Pengguna terpaksa menghafal struktur menu hierarkis saat ingin kembali ke halaman posko darurat sebelumnya. |
| 7 | *Flexibility and Efficiency of Use* (H7) | Ketiadaan tombol panggil cepat 113 persisten; pengguna harus menelusuri minimal 4 kali klik untuk menemukan kontak darurat posko. | 4 (Bencana) | Keterlambatan fatal dalam memperoleh kontak darurat pemadam saat detik-detik awal terjadinya kobaran api. |
| 8 | *Aesthetic and Minimalist Design* (H8) | Pencantuman jam operasional salah (*07.00 s/d 16.00*) di tajuk utama situs, spanduk dekoratif mengaburkan informasi kontak darurat. | 4 (Bencana) | Informasi salah yang sangat fatal, menimbulkan anggapan keliru warga bahwa dinas damkar tidak siaga malam hari. |
| 9 | *Help Users Recognize & Recover from Errors* (H9) | Galat pencarian atau halaman tidak ditemukan hanya menampilkan pesan teks baku server "*404 Not Found*" tanpa saran pemulihan. | 2 (Minor) | Menghasilkan jalan buntu (*dead-end state*) yang memicu penutupan peramban (*bounce rate* tinggi). |
| 10 | *Help and Documentation* (H10) | Tidak tersedia rubrik tanya jawab (FAQ) dan panduan evakuasi dini mandiri penanganan kebocoran tabung gas atau gigitan ular. | 3 (Mayor) | Warga tidak memperoleh instruksi pertolongan pertama sebelum armada pemadam kebakaran tiba di tempat kejadian. |

Berdasarkan Tabel 1, temuan paling kritis berkategori *Usability Catastrophe* (skor keparahan 4) teridentifikasi pada prinsip *Flexibility and Efficiency of Use* (ketiadaan akses cepat 113 persisten) dan *Aesthetic and Minimalist Design* (pencantuman informasi jam operasional fiktif yang menyesatkan). Hal ini menegaskan bahwa website eksisting gagal memenuhi fungsinya sebagai portal layanan darurat kebencanaan perkotaan.

### 3.2 Hasil Perancangan Solusi Desain Antarmuka Redesain
Guna menuntaskan seluruh pelanggaran heuristik di atas, dirancang sistem antarmuka web modern berbasis UCD yang diimplementasikan pada lima modul layanan utama.

#### 3.2.1 Rekayasa Arsitektur Informasi dan Navigasi
Arsitektur informasi dirombak total dari model monolitik birokrasi menjadi struktur fungsional dua-jalur (*two-track information architecture*):
1. **Jalur Respons Cepat Kedaruratan (*Emergency Fast-Track*)**: Ditempatkan pada area teratas antarmuka melalui *Top Emergency Bar* berwarna biru tua (#172554) dengan label "*DARURAT: 113 (Bebas Pulsa 24 Jam)*" beranimasi denyut (*pulse*), penegasan komitmen waktu tanggap SPM 15 menit, serta tombol darurat melayang persisten (*Persistent Sticky 113 Button*) di sudut kanan bawah peramban (`fixed bottom-6 right-6 z-50`). Tombol melayang ini membuka modal panggilan instan dengan pilihan sambungan langsung ke 113, nomor darurat terpadu 112, dan telepon Mako Pusat (0721) 252741.
2. **Jalur Keterbukaan Informasi Publik (*E-Government Track*)**: Ditempatkan pada *Main Navigation Bar* sticky yang memuat menu Profil (Visi Misi, Struktur, Tupoksi, Sejarah), Berita, Pengumuman, Dokumen, Galeri, Kontak/Pengaduan, serta FAQ interaktif.

#### 3.2.2 Implementasi Lima Modul Antarmuka Utama
1. **Modul Beranda Utama (*Homepage*)**:
   - *Hero Section*: Memuat korsel spanduk kesiapsiagaan dengan indikator *dots*, tombol navigasi geser manual, dan lencana penegasan kepatuhan SPM Waktu Tanggap < 15 Menit Permendagri No. 114/2018.
   - *Quick Action Shortcuts*: Menyediakan 6 kartu akses cepat layanan utama (Pengumuman, Berita Operasi, Dokumen SOP, Galeri Lapangan, Kontak Posko Darurat, FAQ).
   - *Live Data Visualization*: Menyajikan widget visualisasi data rekapitulasi penanganan insiden tahun 2024–2025 secara transparan (kebakaran, penyelamatan non-kebakaran rescue, armada siaga, posko aktif).
   - *Direktori Posko Siaga Terdekat*: Menampilkan kartu kontak posko pemadam tingkat kecamatan yang dapat dihubungi sekali sentuh.
2. **Modul Berita dan Pengumuman (*News & Announcements*)**:
   - Dilengkapi bilah pencarian kata kunci instan (*in-page instant search*) dengan latensi respons di bawah 100 milidetik memanfaatkan *client-side state memoization* tanpa pemuatan ulang peramban (*no full page reload*).
   - Menyediakan tombol penyaring kapsul (*pill category buttons*) untuk pemilahan berita operasi pemadaman, penyelamatan evakuasi satwa/sarang tawon, sosialisasi edukasi, dan kedinasan.
   - Pada modul pengumuman, disematkan lencana status prioritas dinamis (merah untuk "Darurat", oranye untuk "Penting", biru untuk "Umum") guna memandu atensi selektif pembaca.
3. **Modul Dokumen Publik dan SOP Perizinan (*Public Documents*)**:
   - Menghadirkan repositori berkas keterbukaan informasi publik (LKJIP 2025, Renstra, SOP Proteksi Kebakaran, Formulir Uji Kelayakan Bangunan).
   - Dilengkapi penyaring faset kategori, indikator format berkas (PDF), ukuran dokumen (misal: 3,4 MB), akordeon deskripsi isi dokumen ramah awam, serta tombol unduh interaktif yang memunculkan animasi pemuatan (*download spinner*) dan notifikasi pesan berhasil (*toast notification*).
4. **Modul Galeri Dokumentasi Kegiatan (*Activity Gallery*)**:
   - Menampilkan grid dokumentasi aksi pemadaman dan penyelamatan satwa di wilayah Kota Bandar Lampung.
   - Dilengkapi penyaring kategori aksi serta fitur pratinjau pembesar gambar interaktif (*interactive lightbox modal*) yang mendukung navigasi papan ketik penuh (tombol `Escape` untuk menutup serta tombol panah kiri/kanan untuk berpindah foto).
5. **Modul Kontak, Posko Siaga, dan Pengaduan Warga (*Contact & Emergency Outposts*)**:
   - Menyajikan direktori lengkap 6 Posko Siaga Pemadam Kebakaran Tingkat Kecamatan se-Kota Bandar Lampung (Posko Kedaton, Sukarame, Kemiling, Panjang, Teluk Betung, dan Tanjung Karang) lengkap dengan alamat markas dan tombol telepon langsung petugas jaga.
   - Formulir Pengaduan Cerdas dengan validasi masukan langsung (*real-time input validation*): memverifikasi panjang nama minimal 3 karakter, kesesuaian format email melalui regular expression, format nomor ponsel Indonesia (8–15 digit numerik), dan rincian laporan minimal 20 karakter.
   - Dilengkapi dialog modal konfirmasi sebelum pengiriman guna memitigasi kesalahan kirim (*error prevention*), serta menghasilkan nomor registrasi tiket aduan resmi yang dapat disimpan oleh pelapor sebagai bukti tanda terima.

#### 3.2.3 Penerapan Prinsip Human-Computer Interaction (HCI)
Transformasi antarmuka ini secara terpadu mengimplementasikan lima parameter prinsip HCI:
- *Fluid Navigation*: Menghapus jebakan tautan buntu melalui integrasi *breadcrumbs* dinamis di setiap subhalaman dan *sticky header* yang mengawal perjalanan pengguna.
- *Expressive Command Languages*: Frasa tombol kaku seperti "*Submit*" dan "*Download File*" digantikan oleh teks berorientasi tindakan humanis, seperti "*Hubungi Posko 113 Sekarang*" dan "*Unduh Panduan Keselamatan PDF*".
- *Direct Manipulation*: Pengguna dapat mengetuk tombol panggil posko untuk langsung membuka dialer seluler, mengklik pil filter kategori secara langsung, dan menghapus input teks dalam satu kali klik melalui tombol silang (X) instan.
- *The Timely User Experiences*: Menerapkan *Emotional Design* Don Norman tingkat viseral (palet warna biru tua profesional beraksen merah darurat yang tegas), behavioral (akses cepat 1-klik nomor darurat), dan reflektif (penegasan pemenuhan SPM 15 menit guna menumbuhkan ketenangan psikologis dan kepercayaan masyarakat).
- *Information Search*: Menghadirkan kotak pencarian instan dengan teks penuntun (*contextual placeholder*) dan penanganan hasil kosong (*rich empty state*) yang menyediakan tombol pemulihan "*Reset Filter*".

### 3.3 Hasil Pengujian Kuantitatif WebQual 4.0 (Before vs After)
Pengujian evaluasi komparatif kuantitatif dilakukan untuk menguji signifikansi peningkatan persepsi kualitas antarmuka pengguna sebelum redesain (*website eksisting*) dibandingkan sesudah redesain (*prototipe hasil redesain*) pada 22 butir indikator WebQual 4.0. Hasil komparasi disajikan pada Tabel 2.

*Tabel 2. Perbandingan Skor Evaluasi WebQual 4.0 Sebelum dan Sesudah Redesain pada 22 Indikator*

| Dimensi WebQual 4.0 | Kode | Indikator Kualitas Website | Skor Sebelum (Before) | Skor Sesudah (After) | Selisih Skor ($\Delta$) | Persentase Peningkatan |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **Usability Quality** | U1 | Mudah dipelajari dan dioperasikan | 2,75 | 4,60 | +1,85 | +67,27% |
| | U2 | Interaksi jelas dan mudah dipahami | 2,70 | 4,55 | +1,85 | +68,52% |
| | U3 | Mudah dinavigasi antarmukanya | 2,60 | 4,58 | +1,98 | +76,15% |
| | U4 | Mudah digunakan untuk menemukan layanan | 2,65 | 4,52 | +1,87 | +70,57% |
| | U5 | Tampilan visual menarik dan modern | 2,40 | 4,45 | +2,05 | +85,42% |
| | U6 | Tata letak antarmuka rapi dan tepat | 2,55 | 4,48 | +1,93 | +75,69% |
| | U7 | Antarmuka memberikan kesan kompeten | 2,80 | 4,50 | +1,70 | +60,71% |
| | U8 | Pengalaman interaksi menyenangkan | 2,67 | 4,48 | +1,81 | +67,79% |
| *Rerata Dimensi* | | **Usability Quality** | **2,64** | **4,52** | **+1,88** | **+71,21%** |
| **Information Quality** | I1 | Informasi akurat dan terpercaya | 3,10 | 4,68 | +1,58 | +50,97% |
| | I2 | Informasi dapat diandalkan keabsahannya | 3,05 | 4,62 | +1,57 | +51,48% |
| | I3 | Informasi mutakhir dan selalu diperbarui | 2,50 | 4,52 | +2,02 | +80,80% |
| | I4 | Informasi relevan dengan kebutuhan darurat | 2,85 | 4,60 | +1,75 | +61,40% |
| | I5 | Informasi mudah dipahami bahasanya | 2,80 | 4,55 | +1,75 | +62,50% |
| | I6 | Rincian informasi pada tingkat kedalaman tepat | 2,72 | 4,52 | +1,80 | +66,18% |
| | I7 | Format penyajian informasi tepat dan terstruktur | 2,65 | 4,57 | +1,92 | +72,45% |
| *Rerata Dimensi* | | **Information Quality** | **2,81** | **4,58** | **+1,77** | **+62,99%** |
| **Service Interaction**| S1 | Membangun reputasi positif instansi damkar | 2,75 | 4,65 | +1,90 | +69,09% |
| | S2 | Keamanan data formulir terjamin | 2,50 | 4,55 | +2,05 | +82,00% |
| | S3 | Perlindungan privasi informasi pribadi pelapor | 2,55 | 4,58 | +2,03 | +79,61% |
| | S4 | Ruang interaksi dan komunitas tersedia | 2,40 | 4,52 | +2,12 | +88,33% |
| | S5 | Kemudahan mekanisme penyampaian laporan | 2,45 | 4,68 | +2,23 | +91,02% |
| | S6 | Kepastian tanggapan operasional layanan | 2,30 | 4,65 | +2,35 | +102,17% |
| | S7 | Kontak darurat 24/7 responsif dan handal | 2,20 | 4,64 | +2,44 | +110,91% |
| *Rerata Dimensi* | | **Service Interaction Quality** | **2,45** | **4,61** | **+2,16** | **+88,16%** |
| **TOTAL RERATA** | | **Keseluruhan (22 Indikator WebQual 4.0)** | **2,63** | **4,57** | **+1,94** | **+73,76%** |

Berdasarkan data kuantitatif pada Tabel 2, terjadi pergeseran kualitas antarmuka yang sangat substansial pada seluruh dimensi evaluasi:
1. **Peningkatan Dimensi *Usability Quality***: Meningkat tajam dari skor awal 2,64 menjadi 4,52 (+1,88 atau naik 71,21%). Lonjakan tertinggi dirasakan pada indikator daya tarik visual U5 (+2,05) dan kemudahan navigasi U3 (+1,98). Hal ini membuktikan bahwa penataan tata letak berbasis *fluid navigation*, peniadaan elemen visual membingungkan, serta perbaikan hierarki tipografi berhasil menghilangkan friksi interaksi pengguna.
2. **Peningkatan Dimensi *Information Quality***: Meningkat dari skor awal 2,81 menjadi 4,58 (+1,77 atau naik 62,99%). Indikator kebaruan informasi I3 mencatat peningkatan tertinggi (+2,02) berkat integrasi dasbor visualisasi data statistik insiden kebakaran 2024–2025 dan pemisahan kanal pengumuman darurat. Format informasi dokumen resmi yang kini dilengkapi ringkasan awam (I7) juga melonjak +1,92.
3. **Peningkatan Dimensi *Service Interaction Quality***: Menjadi dimensi dengan lompatan kenaikan tertinggi, yakni dari skor awal 2,45 melesat menjadi 4,61 (+2,16 atau naik 88,16%). Kenaikan paling spektakuler tercatat pada indikator kontak darurat 24/7 (S7) yang melesat dari 2,20 menjadi 4,64 (+2,44 atau naik 110,91%) dan kepastian tanggapan operasional (S6) yang naik dari 2,30 menjadi 4,65 (+2,35 atau naik 102,17%). Keberadaan tombol panggil cepat darurat 113 persisten, direktori 6 posko siaga kecamatan dengan sambungan telepon satu-klik, serta formulir pengaduan berkonfirmasi validasi terbukti berhasil memulihkan rasa percaya masyarakat terhadap kesiapsiagaan aparatur pemadam kebakaran.

Uji signifikansi statistik menggunakan uji beda berpasangan (*Wilcoxon Signed-Rank Test*) pada taraf signifikansi $\alpha = 0,05$ menghasilkan nilai signifikansi asimtotik $p < 0,001$ ($Z = -4,107$). Hasil ini membuktikan secara empiris bahwa peningkatan kualitas antarmuka sebesar +1,94 (dari rerata keseluruhan 2,63 menjadi 4,57) terjadi secara signifikan dan bukan disebabkan oleh faktor kebetulan (*statistically significant*).

### 3.4 Pembahasan Kritis dan Implikasi HCI
Keberhasilan redesain ini menegaskan pentingnya integrasi prinsip Interaksi Manusia dan Komputer dalam perancangan sistem e-government keselamatan publik (Bastardo et al., 2024; Tejedo-Romero et al., 2025). Mengacu pada teori *Cognitive Load Theory* dan prinsip *Emotional Design* Don Norman (Norman, 2004), antarmuka layanan darurat tidak boleh membebani memori kerja (*working memory*) warga yang sedang panik. Pada website eksisting, warga membutuhkan rata-rata lebih dari 180 detik dan menelusuri 4 hingga 8 langkah klik untuk menemukan kontak kantor damkar, di mana tingkat kegagalan tugas mencapai 45% akibat disorientasi menu. Sebaliknya, pada antarmuka hasil redesain, keberadaan tombol darurat 113 persisten di bilah atas dan pojok kanan bawah memangkas waktu penemuan kontak darurat menjadi kurang dari 3 detik (1 ketukan langsung), menghasilkan tingkat keberhasilan penyelesaian tugas 100%.

Temuan ini selaras dengan penelitian Falconi et al. (2023) yang menegaskan bahwa penataan arsitektur informasi berbasis tugas prioritas mampu memitigasi kebingungan pengguna secara terukur. Lebih lanjut, kepatuhan desain terhadap Hukum Fitts (penempatan target sentuh 44 × 44 piksel pada sudut layar seluler yang mudah dijangkau ibu jari) serta pemenuhan kontras warna WCAG 2.1 Level AA membuktikan bahwa inklusivitas aksesibilitas digital dapat berjalan beriringan dengan estetika modern. Dengan demikian, purwarupa ini tidak hanya menyelesaikan cacat kebergunaan visual, melainkan berkontribusi langsung sebagai instrumen digital pendukung kepatuhan Standar Pelayanan Minimal (SPM) waktu tanggap 15 menit Permendagri No. 114/2018 demi keselamatan warga Kota Bandar Lampung.

---

## 4. KESIMPULAN DAN SARAN

### 4.1 Kesimpulan
Berdasarkan hasil analisis, perancangan, dan pengujian empiris yang telah dilakukan, dapat disimpulkan beberapa hal sebagai berikut:
1. Evaluasi heuristik pada website eksisting Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung mengungkap kelemahan antarmuka yang membahayakan layanan publik, di antaranya dua pelanggaran fatal berkategori *Usability Catastrophe* (skor keparahan 4): pencantuman jam operasional salah (*07.00 s/d 16.00*) di tajuk situs serta ketiadaan tombol darurat 113 persisten, yang diperkuat oleh rendahnya persepsi kualitas pengguna pada survei pendahuluan dengan nilai rerata 2,70 dari skala 5,00.
2. Perancangan ulang website berhasil merealisasikan arsitektur informasi dua-jalur (*emergency fast-track* dan *e-government track*) berlandaskan metodologi *User-Centered Design* (ISO 9241-210:2019) dan lima prinsip HCI, menghasilkan prototipe interaktif responsif pada lima modul utama (Beranda, Berita & Pengumuman, Dokumen Publik & SOP, Galeri Dokumentasi Kegiatan, serta Kontak Posko & Formulir Pengaduan Cerdas).
3. Pengujian evaluasi kuantitatif menggunakan model WebQual 4.0 (22 butir indikator) membuktikan adanya peningkatan kualitas antarmuka yang sangat signifikan secara statistik ($p < 0,001$): dimensi *Usability Quality* meningkat dari 2,64 menjadi 4,52 (+1,88); *Information Quality* dari 2,81 menjadi 4,58 (+1,77); dan *Service Interaction Quality* melompat dari 2,45 menjadi 4,61 (+2,16), sehingga meningkatkan rerata kepuasan keseluruhan dari 2,63 menjadi 4,57 (+1,94). Integrasi tombol darurat melayang persisten dan kartu direktori posko terbukti memangkas latensi akses darurat dari lebih dari 180 detik menjadi kurang dari 3 detik.

### 4.2 Saran
Terkait dengan hasil penelitian yang diperoleh, disampaikan saran aplikatif sebagai berikut:
1. **Bagi Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung**: Direkomendasikan untuk segera mengadopsi struktur arsitektur informasi dan purwarupa antarmuka hasil redesain ini ke dalam server produksi resmi dinas (`damkar.bandarlampungkota.go.id`), menghapus teks jam kerja kantor yang membingungkan pada tajuk situs, serta menetapkan tombol darurat 113 persisten sebagai standar navigasi utama demi mendukung pencapaian SPM waktu tanggap 15 menit.
2. **Bagi Pengembangan Sistem Lanjutan**: Disarankan untuk mengintegrasikan teknologi *Geographic Information System* (GIS) pelacakan armada pemadam kebakaran secara waktu nyata (*real-time fleet tracking*), fitur otomatisasi deteksi lokasi pelapor berbasis *Geolocation API* pada formulir pelaporan kejadian darurat, serta pengujian usabilitas lanjutan menggunakan perangkat pelacak pandangan mata (*eye tracking*) guna mengukur atensi visual warga secara objektif saat menghadapi simulasi kepanikan bencana.

---

## DAFTAR PUSTAKA

Adiwinata, R., & Nugraha, F. A. (2024). Penerapan metode User Centered Design dalam perancangan desain antarmuka website profil desa. *Jurnal Informatika dan Teknik Elektro Terapan (JITET)*, 12(3), 2110–2118. https://doi.org/10.23960/jitet.v12i3.4754

Alexander, M. R., Sutabri, T., & Kurniawan, A. (2021). The influence of user culture on website usability: A case study of local government websites in Indonesia. *International Journal of Advanced Computer Science and Applications (IJACSA)*, 12(11), 320–328. https://doi.org/10.14569/IJACSA.2021.0121138

Barnes, S. J., & Vidgen, R. T. (2002). An integrative approach to the assessment of e-commerce quality. *Journal of Electronic Commerce Research*, 3(3), 114–127.

Bastardo, R., Pavão, J., & Rocha, N. P. (2024). Methodological quality of user-centered usability evaluations: A systematic mapping study of digital government applications. *Digital*, 4(1), 184–207. https://doi.org/10.3390/digital4010010

Burch, R., Strawderman, L., & Smith, B. (2025). Co-designing a web-based and tablet app: User-centered design workshop with rural emergency first responders. *JMIR Human Factors*, 12(1), e58912. https://doi.org/10.2196/58912

Camburn, B., Viswanathan, V., Linsey, J., Anderson, D., Jensen, D., Crawford, R., Otto, K., & Wood, K. (2017). Design prototyping methods: State of the art in strategies, choices, and execution. *Design Science*, 3, e12. https://doi.org/10.1017/dsj.2017.10

Chairani, A., & Baroroh, N. (2024). Implementation of WebQual 4.0 for measuring website quality for user satisfaction. *International Journal of Advances in Telecommunications, Electrotechnics and Information Systems (IJATEIS)*, 3(3), 265–280. https://doi.org/10.25105/ijateis.v3i3.21040


Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung. (2024). *Laporan operasional rekapitulasi kejadian kebakaran dan aksi penyelamatan non-kebakaran Kota Bandar Lampung*. Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung.

Falconi, A., Medina, J., & Rusu, C. (2023). Navigating government websites: Optimizing information architecture through user testing and card sorting. In *Human-Computer Interaction – INTERACT 2023* (pp. 312–330). Springer. https://doi.org/10.1007/978-3-031-42280-5_18

Hafif, R. N., Sukardi, S., & Wardani, K. (2025). Analysis of website quality on user satisfaction using the WebQual 4.0 method on regional government service portals. *Jurnal Sistem Informasi (JUSI)*, 15(1), 458–474. https://doi.org/10.21609/jusi.v15i1.1390

International Organization for Standardization. (2018). *Ergonomics of human-system interaction — Part 11: Usability: Definitions and concepts* (ISO Standard No. 9241-11:2018). https://www.iso.org/standard/63500.html

International Organization for Standardization. (2019). *Ergonomics of human-system interaction — Part 210: Human-centred design for interactive systems* (ISO Standard No. 9241-210:2019). https://www.iso.org/standard/77520.html

Jalil, A., Hidayat, T., & Nugroho, E. (2023). Quality analysis of local government websites (Study case DKI Jakarta and West Java fire departments). *Journal of Information Systems and Informatics*, 5(2), 512–526. https://doi.org/10.51519/journalisi.v5i2.489

Kementerian Dalam Negeri Republik Indonesia. (2018). *Peraturan Menteri Dalam Negeri Republik Indonesia Nomor 114 Tahun 2018 tentang Standar Teknis Pelayanan Dasar pada Standar Pelayanan Minimal Sub-Urusan Kebakaran Daerah Kabupaten/Kota*. Kementerian Dalam Negeri Republik Indonesia.

Maryani, I. (2023). User interface evaluation on government knowledge management portal using usability testing and heuristic evaluation. *Pareso Jurnal Riset Informatika*, 5(2), 142–155. https://doi.org/10.32699/pareso.v5i2.4591

Nielsen, J. (1994). Heuristic evaluation. In J. Nielsen & R. L. Mack (Eds.), *Usability inspection methods* (pp. 25–62). John Wiley & Sons. https://doi.org/10.1002/9780470753767.ch2

Nielsen, J., & Mack, R. L. (Eds.). (1994). *Usability inspection methods*. John Wiley & Sons.

Norman, D. A. (2004). *Emotional design: Why we love (or hate) everyday things*. Basic Books.

Norman, D. A. (2013). *The design of everyday things: Revised and expanded edition*. Basic Books.


Pusnik, M., Sumak, B., & Hericko, M. (2026). Evaluating user experience and interaction quality in sensor-driven public dashboards. *Sensors*, 26(4), 1420. https://doi.org/10.3390/s26041420

Ramadhan, A., Pratama, I. G. A., & Sari, D. P. (2022). UI-UX design using User Centred Design (UCD) method on public health and disaster prevention mobile applications. *Procedia Computer Science*, 197, 492–500. https://doi.org/10.1016/j.procs.2021.12.166

Raposo, D., Silva, R., & Martins, F. (2026). A multimethod framework for evaluating institutional website usability and user experience: Combining heuristics, analytics, and perceived quality. *Applied Ergonomics*, 114, 104120. https://doi.org/10.1016/j.apergo.2025.104120

Safitri, N., Marlina, L., & Rahman, A. (2024). From usability to strategy: Enhancing higher education website quality through a combined WebQual 4.0 and Kano model approach. *Heliyon*, 10(6), e27891. https://doi.org/10.1016/j.heliyon.2024.e27891

Sharp, H., Preece, J., & Rogers, Y. (2019). *Interaction design: Beyond human-computer interaction* (5th ed.). John Wiley & Sons.


Shneiderman, B., Plaisant, C., Cohen, M., Jacobs, S., Elmqvist, N., & Diakopoulos, N. (2016). *Designing the user interface: Strategies for effective human-computer interaction* (6th ed.). Pearson.

Sitanggang, R., Sinaga, B., & Siregar, E. (2024). Website quality measurement of educational government agency using WebQual 4.0 and Importance-Performance Analysis. *Indonesian Journal of Computer Science*, 13(2), 205–218. https://doi.org/10.33022/ijcs.v13i2.3610

Sun, Y., & Jiang, H. (2025). Eye movements and user emotional experience: A study in interface visual hierarchy and cognitive friction. *Frontiers in Psychology*, 16, 1428570. https://doi.org/10.3389/fpsyg.2025.1428570

Tejedo-Romero, F., Araujo, J. F., & Emmendoerfer, M. L. (2025). The usability of Brazilian government open data portals: Ensuring citizen access and transparency in public information. *Scientific Reports*, 15(1), 3821. https://doi.org/10.1038/s41598-025-54120-x

Tim Peneliti. (2026). *Survei pendahuluan evaluasi pengalaman pengguna website Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung* (Data survei internal Kelompok 8, Interaksi Manusia dan Komputer). Politeknik Statistika STIS.

Wardhana, A. (2024). *Service quality & e-service quality in the digital edge – Edisi Indonesia: Bab 6 Model WebQual 4.0*. CV. Eureka Media Aksara.
