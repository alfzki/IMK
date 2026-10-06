# Katalog Rancangan Wireframe & Low-Fidelity Mockup Redesain Website Damkar Kota Bandar Lampung

Dokumen ini berisi daftar dan dokumentasi lengkap berkas visual **Wireframe & Low-Fidelity Mockup** dalam format **vektor (`.svg`)** dan **raster resolusi tinggi (`.png`)** untuk proyek redesain portal resmi Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung (`damkar.bandarlampungkota.go.id` / `https://damkar-bandarlampung-redesign-5wxa.vercel.app`).

---

## 1. Daftar Berkas Gambar Wireframe & Mockup

| No. | Nama Berkas | Halaman / Komponen | Format & Resolusi | Prinsip HCI / IMK Utama |
| :---: | :--- | :--- | :--- | :--- |
| **01** | [`wireframe_01_beranda_desktop.svg`](file:///home/alfzki/Documents/IMK/drafts/wireframes/wireframe_01_beranda_desktop.svg)<br>[`wireframe_01_beranda_desktop.png`](file:///home/alfzki/Documents/IMK/drafts/wireframes/wireframe_01_beranda_desktop.png) | **Beranda & Framework Global (Desktop)** | SVG & PNG<br>(1200 × 1820 px) | *Visual Hierarchy, Hick's Law, Emotional Design (Visceral & Behavioral), Fitts's Law Sticky Button*. |
| **02** | [`wireframe_02_berita_desktop.svg`](file:///home/alfzki/Documents/IMK/drafts/wireframes/wireframe_02_berita_desktop.svg)<br>[`wireframe_02_berita_desktop.png`](file:///home/alfzki/Documents/IMK/drafts/wireframes/wireframe_02_berita_desktop.png) | **Modul Berita & Catatan Operasi (`/berita`)** | SVG & PNG<br>(1200 × 1450 px) | *Instant Search (<100ms), Recognition rather than Recall (Nielsen H6), Category Pill Filters, Pagination*. |
| **03** | [`wireframe_03_dokumen_desktop.svg`](file:///home/alfzki/Documents/IMK/drafts/wireframes/wireframe_03_dokumen_desktop.svg)<br>[`wireframe_03_dokumen_desktop.png`](file:///home/alfzki/Documents/IMK/drafts/wireframes/wireframe_03_dokumen_desktop.png) | **Modul Dokumen, SOP & Regulasi (`/dokumen`)** | SVG & PNG<br>(1200 × 1380 px) | *Match Real World (Nielsen H2 - Eliminasi Jargon), System Status Feedback Toast (H1), Akuntabilitas SPM*. |
| **04** | [`wireframe_04_galeri_desktop.svg`](file:///home/alfzki/Documents/IMK/drafts/wireframes/wireframe_04_galeri_desktop.svg)<br>[`wireframe_04_galeri_desktop.png`](file:///home/alfzki/Documents/IMK/drafts/wireframes/wireframe_04_galeri_desktop.png) | **Modul Galeri Edukasi & Penyelamatan (`/galeri`)** | SVG & PNG<br>(1200 × 1380 px) | *Direct Manipulation (Shneiderman), Modal Lightbox Preview, Emotional Design Reflective Level*. |
| **05** | [`wireframe_05_kontak_desktop.svg`](file:///home/alfzki/Documents/IMK/drafts/wireframes/wireframe_05_kontak_desktop.svg)<br>[`wireframe_05_kontak_desktop.png`](file:///home/alfzki/Documents/IMK/drafts/wireframes/wireframe_05_kontak_desktop.png) | **Modul Kontak & Pengaduan Cepat (`/kontak`)** | SVG & PNG<br>(1200 × 1480 px) | *Error Prevention (Nielsen H5), Real-time Regex Validation, Direktori 6 Posko Siaga Kecamatan (<15 Menit)*. |
| **06** | [`wireframe_06_mobile_responsive.svg`](file:///home/alfzki/Documents/IMK/drafts/wireframes/wireframe_06_mobile_responsive.svg)<br>[`wireframe_06_mobile_responsive.png`](file:///home/alfzki/Documents/IMK/drafts/wireframes/wireframe_06_mobile_responsive.png) | **Tampilan Responsif Mobile Smartphone** | SVG & PNG<br>(450 × 1500 px) | *Fitts's Law Mobile Thumb-Zone (Target Ukuran >48×48px), 1-Tap Call Hotline 113, Accordion Posko*. |
| **07** | [`wireframe_07_modals_interaction.svg`](file:///home/alfzki/Documents/IMK/drafts/wireframes/wireframe_07_modals_interaction.svg)<br>[`wireframe_07_modals_interaction.png`](file:///home/alfzki/Documents/IMK/drafts/wireframes/wireframe_07_modals_interaction.png) | **Dialog Interaktif & Pencegahan Galat** | SVG & PNG<br>(1200 × 920 px) | *Zero-Latency Quick Call Modal (113/112/Mako/WA) & Error Prevention Confirmation Modal with Ticket*. |

---

## 2. Penjelasan Rancangan Per Komponen & Alasan IMK

### A. Wireframe 01: Beranda & Framework Global
- **Top Emergency Bar (`#1E293B`)**: Penegasan status operasional 24 jam dan SPM waktu tanggap < 15 menit mengoreksi kesalahan fatal pada website eksisting yang menuliskan jam operasional kantor biasa (07.00 - 16.00).
- **Hero Section**: Memisahkan secara tegas dua aksi utama masyarakat: tombol darurat merah menyala (`Hubungi Darurat 113`) untuk kebutuhan krisis, dan tombol sekunder putih (`Lapor Insiden Online`) untuk laporan non-kritis.
- **Kartu 4 Layanan Utama**: Menerapkan *Hick's Law* dengan membatasi opsi awal ke 4 kartu terpenting: Pemadaman Api, Aksi Rescue, Posko Siaga Kecamatan, dan Dokumen Publik.
- **Dasbor Statistik Transparan**: Menampilkan metrik empiris (271 kebakaran 2024, 518 penyelamatan 2025, 18 armada aktif, SPM <15 menit) untuk membangun kepercayaan masyarakat (*Reflective Emotional Design*).
- **Persistent Sticky 113 Emergency Button**: Mengambang di sudut kanan bawah peramban (`fixed bottom-6 right-6`) dengan target klik besar dan animasi denyut (*pulse*) mematuhi kaidah *Fitts's Law* agar mudah dijangkau kapan pun tanpa perlu menggulir ke atas.

### B. Wireframe 02: Modul Berita & Catatan Operasi
- **Bilah Pencarian Instan (<100 ms)**: Pengguna dapat menemukan warta kejadian kebakaran atau rescue seketika di sisi klien (*client-side filtering*) tanpa muat ulang halaman.
- **Pill Category Buttons**: Tombol kapsul kategori multi-kategori (`Semua`, `Pemadaman`, `Rescue`, `Sosialisasi`, `Peringatan`) menerapkan prinsip *Recognition rather than Recall* (Nielsen H6).
- **Kartu Berita Utama (Featured Card)**: Memberikan titik fokus visual (*focal point*) pada penanganan insiden kebakaran berskala besar.

### C. Wireframe 03: Modul Dokumen, SOP & Regulasi
- **Deskripsi Bahasa Awam**: Mengeliminasi friksi pemahaman birokrasi (Nielsen H2 *Match between System and Real World*). Singkatan seperti LKJIP dan Renstra dijelaskan fungsi praktisnya bagi warga dan pemilik usaha.
- **Toast Feedback Notification**: Indikator visual seketika saat mengunduh berkas (*"SOP berhasil diunduh (2,4 MB)"*) memenuhi prinsip *Visibility of System Status* (Nielsen H1).

### D. Wireframe 04: Modul Galeri Edukasi & Penyelamatan
- **Tata Letak Grid Foto & Video**: Menampilkan bukti nyata kesiapsiagaan korps pemadam kebakaran dalam aksi pemadaman api, penyelamatan hewan berbahaya, evakuasi cincin, dan edukasi anak sekolah.
- **Lightbox Preview Modal**: Menerapkan *Direct Manipulation* (Ben Shneiderman) saat gambar diklik untuk memperbesar visual tanpa kehilangan konteks halaman.

### E. Wireframe 05: Modul Kontak & Pengaduan Cepat
- **Direktori 6 Posko Siaga Kecamatan**: Menyajikan alamat lengkap dan tombol panggil langsung (*click-to-call*) untuk Mako Pusat, Posko Kedaton, Sukarame, Kemiling, Panjang, dan Teluk Betung.
- **Validasi Formulir Seketika (*Real-time Validation*)**: Kotak input nama, nomor kontak regex, dan lokasi langsung memberikan tanda centang hijau atau peringatan galat seketika sebelum dikirim (Nielsen H5 *Error Prevention*).

### F. Wireframe 06: Responsive Mobile Viewport
- **Mobile Thumb Zone**: Tombol panggil 113 berukuran penuh (*full width*, tinggi 56 px) dirancang tepat di area jangkauan jempol tangan satu pengguna ponsel cerdas.
- **Sticky Bottom Action Bar**: Bilah aksi darurat tetap melekat di bagian bawah layar ponsel untuk panggilan telepon 113 dan chat WhatsApp siaga.

### G. Wireframe 07: Dialog Interaktif & Pencegahan Galat
- **Quick Call Modal**: Menghubungkan pengguna dalam 1 ketukan ke 4 opsi saluran: 113 (Damkar bebas pulsa), 112 (Call center pemkot), telepon PSTN Mako Pusat, dan pesan WhatsApp siaga dengan fitur *live location sharing*.
- **Confirmation Modal**: Mencegah kepanikan salah input dan laporan palsu (*prank calls*) dengan menampilkan ringkasan data, pernyataan kejujuran pelapor, dan penerbitan nomor tiket aduan resmi.
