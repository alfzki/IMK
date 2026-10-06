"""
Script generator untuk menghasilkan wireframe ultra low-fidelity (Balsamiq / Sketch style)
sesuai contoh referensi visual: garis hitam tegas (2px), kotak abu-abu (#EAEAEA),
dummy text bars horizontal (#777777), image placeholder dengan silang 'X' diagonal,
dan browser window chrome retro.
"""

import os
import subprocess

OUT_DIR = "drafts/wireframes/low_fidelity"
os.makedirs(OUT_DIR, exist_ok=True)

STYLE_DEF = """
  <defs>
    <style>
      .sketch-bg { fill: #ffffff; }
      .sketch-border { stroke: #222222; stroke-width: 2; fill: none; }
      .sketch-window-top { fill: #cccccc; stroke: #222222; stroke-width: 2; }
      .sketch-window-nav { fill: #ffffff; stroke: #222222; stroke-width: 2; }
      .sketch-card { fill: #eaeaea; stroke: #222222; stroke-width: 2; }
      .sketch-card-white { fill: #ffffff; stroke: #222222; stroke-width: 2; }
      .sketch-line { stroke: #222222; stroke-width: 2; }
      .sketch-line-thin { stroke: #222222; stroke-width: 1.5; }
      .sketch-line-gray { stroke: #777777; stroke-width: 1.5; }
      .sketch-text-bar { fill: #777777; rx: 2; }
      .sketch-text-bar-light { fill: #aaaaaa; rx: 2; }
      
      .font-title { font-family: "Comic Sans MS", "Comic Neue", "Chalkboard SE", "Segoe Print", "Arial Rounded MT Bold", sans-serif; font-size: 20px; font-weight: bold; fill: #111111; }
      .font-subhead { font-family: "Comic Sans MS", "Comic Neue", "Chalkboard SE", "Segoe Print", sans-serif; font-size: 15px; font-weight: bold; fill: #222222; }
      .font-body { font-family: "Comic Sans MS", "Comic Neue", "Chalkboard SE", "Segoe Print", sans-serif; font-size: 12px; fill: #333333; }
      .font-body-bold { font-family: "Comic Sans MS", "Comic Neue", "Chalkboard SE", "Segoe Print", sans-serif; font-size: 12px; font-weight: bold; fill: #111111; }
      .font-small { font-family: "Comic Sans MS", "Comic Neue", "Chalkboard SE", "Segoe Print", sans-serif; font-size: 10px; fill: #555555; }
      .font-btn { font-family: "Comic Sans MS", "Comic Neue", "Chalkboard SE", "Segoe Print", sans-serif; font-size: 12px; font-weight: bold; fill: #111111; text-anchor: middle; }
      .font-btn-white { font-family: "Comic Sans MS", "Comic Neue", "Chalkboard SE", "Segoe Print", sans-serif; font-size: 12px; font-weight: bold; fill: #ffffff; text-anchor: middle; }
      
      .btn-sketch-white { fill: #ffffff; stroke: #222222; stroke-width: 2; rx: 4; }
      .btn-sketch-dark { fill: #222222; stroke: #222222; stroke-width: 2; rx: 4; }
      .btn-sketch-gray { fill: #dddddd; stroke: #222222; stroke-width: 2; rx: 4; }
    </style>
  </defs>
"""

def browser_chrome_lowfi(w, url="http://damkar.bandarlampungkota.go.id"):
    return f"""
    <!-- BROWSER WINDOW CHROME (BALSAMIQ RETRO STYLE) -->
    <!-- Outer Window Border -->
    <rect x="2" y="2" width="{w - 4}" height="68" class="sketch-window-top" />
    <text x="{w // 2}" y="19" class="font-body-bold" text-anchor="middle">Browser</text>
    <!-- Close Box X -->
    <rect x="{w - 26}" y="6" width="18" height="16" fill="#ffffff" stroke="#222222" stroke-width="1.5" />
    <text x="{w - 17}" y="19" class="font-body-bold" font-size="11" text-anchor="middle">✕</text>

    <!-- Nav Toolbar Strip -->
    <rect x="2" y="28" width="{w - 4}" height="42" class="sketch-window-nav" />
    
    <!-- Back / Forward Buttons -->
    <rect x="12" y="35" width="68" height="28" rx="4" fill="#ffffff" stroke="#222222" stroke-width="1.8" />
    <line x1="46" y1="35" x2="46" y2="63" stroke="#222222" stroke-width="1.5" />
    <text x="29" y="54" class="font-body-bold" text-anchor="middle">←</text>
    <text x="63" y="54" class="font-body-bold" text-anchor="middle">→</text>

    <!-- Refresh Button -->
    <rect x="86" y="35" width="30" height="28" rx="4" fill="#ffffff" stroke="#222222" stroke-width="1.8" />
    <text x="101" y="54" class="font-body-bold" text-anchor="middle">↻</text>

    <!-- URL Address Bar -->
    <rect x="124" y="35" width="{w - 140}" height="28" rx="4" fill="#ffffff" stroke="#222222" stroke-width="1.8" />
    <text x="136" y="53" class="font-body">{url}</text>
    """

def placeholder_image_lowfi(x, y, w, h, label="Image"):
    return f"""
    <!-- Placeholder Box with Diagonal X Lines -->
    <g transform="translate({x}, {y})">
      <rect x="0" y="0" width="{w}" height="{h}" class="sketch-card-white" />
      <line x1="0" y1="0" x2="{w}" y2="{h}" class="sketch-line" />
      <line x1="0" y1="{h}" x2="{w}" y2="0" class="sketch-line" />
      <!-- Label Backdrop -->
      <rect x="{w//2 - len(label)*4.5 - 12}" y="{h//2 - 12}" width="{len(label)*9 + 24}" height="24" fill="#ffffff" stroke="#222222" stroke-width="1.5" rx="3" />
      <text x="{w//2}" y="{h//2 + 5}" class="font-body-bold" text-anchor="middle">{label}</text>
    </g>
    """

def text_placeholder_bars(x, y, widths, h=10, gap=7):
    bars_xml = ""
    curr_y = y
    for w in widths:
        bars_xml += f'<rect x="{x}" y="{curr_y}" width="{w}" height="{h}" class="sketch-text-bar" />\n'
        curr_y += h + gap
    return bars_xml


# ==============================================================================
# 1. LOW-FI WIREFRAME 01: BERANDA & FRAMEWORK GLOBAL (1000 x 1180)
# ==============================================================================
def generate_lowfi_01():
    w, h = 1000, 1200
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {STYLE_DEF}
  <!-- Base Background -->
  <rect x="0" y="0" width="{w}" height="{h}" class="sketch-bg" />
  <rect x="2" y="2" width="{w-4}" height="{h-4}" class="sketch-border" />

  {browser_chrome_lowfi(w)}

  <!-- TOP EMERGENCY BAR -->
  <g transform="translate(15, 80)">
    <rect x="0" y="0" width="{w - 30}" height="30" class="sketch-card" />
    <rect x="10" y="5" width="110" height="20" fill="#222222" rx="3" />
    <text x="65" y="19" class="font-btn-white" font-size="10">SIAGA 24 JAM</text>
    <text x="135" y="20" class="font-body-bold">KOMITMEN SPM WAKTU TANGGAP &lt; 15 MENIT | CALL CENTER: 113 / 112</text>
    <rect x="{w - 180}" y="4" width="135" height="22" class="btn-sketch-dark" />
    <text x="{w - 112}" y="19" class="font-btn-white">HOTLINE 113</text>
  </g>

  <!-- NAVBAR -->
  <g transform="translate(15, 120)">
    <rect x="0" y="0" width="{w - 30}" height="55" class="sketch-card-white" />
    
    <!-- Logo -->
    <rect x="12" y="8" width="38" height="38" class="sketch-card" />
    <text x="31" y="32" class="font-body-bold" text-anchor="middle">LOGO</text>
    <text x="60" y="28" class="font-title" font-size="15">DAMKAR KOTA BANDAR LAMPUNG</text>
    <text x="60" y="44" class="font-small">Portal Kesiapsiagaan &amp; Tanggap Bencana</text>

    <!-- Links -->
    <text x="430" y="33" class="font-body-bold" text-decoration="underline">[ Beranda ]</text>
    <text x="525" y="33" class="font-body">[ Berita ]</text>
    <text x="600" y="33" class="font-body">[ Dokumen ]</text>
    <text x="690" y="33" class="font-body">[ Galeri ]</text>
    <text x="765" y="33" class="font-body">[ Kontak ]</text>

    <!-- Search Input -->
    <rect x="840" y="12" width="115" height="30" class="sketch-card-white" />
    <text x="850" y="31" class="font-small">Cari...</text>
  </g>

  <!-- HERO SECTION -->
  <g transform="translate(15, 185)">
    <rect x="0" y="0" width="{w - 30}" height="250" class="sketch-card" />
    
    <!-- Left Hero: Headline & CTAs -->
    <g transform="translate(25, 25)">
      <rect x="0" y="0" width="140" height="22" class="btn-sketch-white" />
      <text x="70" y="15" class="font-btn" font-size="10">SPM RESPON &lt; 15 MNT</text>

      <text x="0" y="55" class="font-title">RESPON CEPAT TANGGAP DARURAT</text>
      <text x="0" y="82" class="font-title">KEBAKARAN &amp; PENYELAMATAN</text>

      <!-- Dummy Text Bars -->
      {text_placeholder_bars(0, 102, [460, 420, 380], h=9, gap=6)}

      <!-- Primary Action Buttons -->
      <rect x="0" y="155" width="220" height="42" class="btn-sketch-dark" />
      <text x="110" y="181" class="font-btn-white">HUBUNGI DARURAT 113</text>

      <rect x="235" y="155" width="200" height="42" class="btn-sketch-white" />
      <text x="335" y="181" class="font-btn">Lapor Insiden Online</text>
    </g>

    <!-- Right Hero: Big Image Placeholder with X -->
    {placeholder_image_lowfi(560, 20, 385, 210, "Foto Armada Damkar &amp; Personil")}
  </g>

  <!-- EMERGENCY BROADCAST ALERT STRIP -->
  <g transform="translate(15, 445)">
    <rect x="0" y="0" width="{w - 30}" height="38" class="sketch-card-white" stroke-dasharray="6 3" />
    <text x="15" y="24" class="font-body-bold">[ ! ] PERINGATAN DINI KEBENCANAAN:</text>
    <rect x="250" y="14" width="580" height="10" class="sketch-text-bar" />
    <rect x="850" y="7" width="105" height="24" class="btn-sketch-white" />
    <text x="902" y="23" class="font-btn" font-size="10">Baca Himbauan</text>
  </g>

  <!-- 4 SERVICES CARDS (LAYANAN UTAMA) -->
  <g transform="translate(15, 495)">
    <text x="0" y="18" class="font-title" font-size="16">LAYANAN UTAMA KEDARURATAN</text>
    
    <!-- Card 1 -->
    <g transform="translate(0, 30)">
      <rect x="0" y="0" width="230" height="150" class="sketch-card" />
      {placeholder_image_lowfi(15, 12, 50, 40, "Api")}
      <text x="75" y="36" class="font-subhead" font-size="13">Pemadaman</text>
      {text_placeholder_bars(15, 65, [195, 180, 160], h=8, gap=5)}
      <rect x="15" y="105" width="110" height="28" class="btn-sketch-dark" />
      <text x="70" y="123" class="font-btn-white" font-size="10">Panggil 113</text>
    </g>

    <!-- Card 2 -->
    <g transform="translate(247, 30)">
      <rect x="0" y="0" width="230" height="150" class="sketch-card" />
      {placeholder_image_lowfi(15, 12, 50, 40, "Rescue")}
      <text x="75" y="36" class="font-subhead" font-size="13">Aksi Rescue</text>
      {text_placeholder_bars(15, 65, [195, 180, 160], h=8, gap=5)}
      <rect x="15" y="105" width="110" height="28" class="btn-sketch-white" />
      <text x="70" y="123" class="font-btn" font-size="10">Lapor Rescue</text>
    </g>

    <!-- Card 3 -->
    <g transform="translate(494, 30)">
      <rect x="0" y="0" width="230" height="150" class="sketch-card" />
      {placeholder_image_lowfi(15, 12, 50, 40, "Posko")}
      <text x="75" y="36" class="font-subhead" font-size="13">Posko Siaga</text>
      {text_placeholder_bars(15, 65, [195, 180, 160], h=8, gap=5)}
      <rect x="15" y="105" width="110" height="28" class="btn-sketch-white" />
      <text x="70" y="123" class="font-btn" font-size="10">Cari Posko</text>
    </g>

    <!-- Card 4 -->
    <g transform="translate(740, 30)">
      <rect x="0" y="0" width="230" height="150" class="sketch-card" />
      {placeholder_image_lowfi(15, 12, 50, 40, "SOP")}
      <text x="75" y="36" class="font-subhead" font-size="13">Dokumen SOP</text>
      {text_placeholder_bars(15, 65, [195, 180, 160], h=8, gap=5)}
      <rect x="15" y="105" width="110" height="28" class="btn-sketch-white" />
      <text x="70" y="123" class="font-btn" font-size="10">Unduh PDF</text>
    </g>
  </g>

  <!-- OPERATIONAL STATISTICS (4 STAT BOXES) -->
  <g transform="translate(15, 695)">
    <text x="0" y="18" class="font-title" font-size="16">STATISTIK OPERASIONAL &amp; SPM</text>

    <!-- Stat 1 -->
    <rect x="0" y="30" width="230" height="85" class="sketch-card-white" />
    <text x="20" y="65" class="font-title" font-size="28">271</text>
    <text x="20" y="85" class="font-body-bold">Kebakaran (2024)</text>
    <text x="20" y="100" class="font-small">Insiden tertangani</text>

    <!-- Stat 2 -->
    <rect x="247" y="30" width="230" height="85" class="sketch-card-white" />
    <text x="267" y="65" class="font-title" font-size="28">518</text>
    <text x="267" y="85" class="font-body-bold">Aksi Rescue (2025)</text>
    <text x="267" y="100" class="font-small">Penyelamatan warga</text>

    <!-- Stat 3 -->
    <rect x="494" y="30" width="230" height="85" class="sketch-card-white" />
    <text x="514" y="65" class="font-title" font-size="28">18</text>
    <text x="514" y="85" class="font-body-bold">Armada Mobil</text>
    <text x="514" y="100" class="font-small">Unit siaga aktif</text>

    <!-- Stat 4 -->
    <rect x="740" y="30" width="230" height="85" class="sketch-card-white" />
    <text x="760" y="65" class="font-title" font-size="28">&lt; 15 m</text>
    <text x="760" y="85" class="font-body-bold">Respon SPM</text>
    <text x="760" y="100" class="font-small">Permendagri 114/2018</text>
  </g>

  <!-- RECENT NEWS SECTION (3 CARDS) -->
  <g transform="translate(15, 830)">
    <text x="0" y="18" class="font-title" font-size="16">WARTA KEJADIAN &amp; EDUKASI MITIGASI</text>

    <!-- News 1 -->
    <g transform="translate(0, 30)">
      <rect x="0" y="0" width="310" height="195" class="sketch-card" />
      {placeholder_image_lowfi(10, 10, 290, 95, "Foto: Kebakaran Gudang")}
      <text x="15" y="125" class="font-body-bold">Kebakaran di Kedaton Tertangani</text>
      {text_placeholder_bars(15, 138, [270, 240], h=8, gap=5)}
      <text x="15" y="175" class="font-small">15 Sep 2025 • Baca selengkapnya &gt;</text>
    </g>

    <!-- News 2 -->
    <g transform="translate(330, 30)">
      <rect x="0" y="0" width="310" height="195" class="sketch-card" />
      {placeholder_image_lowfi(10, 10, 290, 95, "Foto: Animal Rescue")}
      <text x="15" y="125" class="font-body-bold">Evakuasi Ular Sanca di Pemukiman</text>
      {text_placeholder_bars(15, 138, [270, 240], h=8, gap=5)}
      <text x="15" y="175" class="font-small">12 Sep 2025 • Baca selengkapnya &gt;</text>
    </g>

    <!-- News 3 -->
    <g transform="translate(660, 30)">
      <rect x="0" y="0" width="310" height="195" class="sketch-card" />
      {placeholder_image_lowfi(10, 10, 290, 95, "Foto: Edukasi Sekolah")}
      <text x="15" y="125" class="font-body-bold">Pelatihan Proteksi Dini Siswa SD</text>
      {text_placeholder_bars(15, 138, [270, 240], h=8, gap=5)}
      <text x="15" y="175" class="font-small">08 Sep 2025 • Baca selengkapnya &gt;</text>
    </g>
  </g>

  <!-- PERSISTENT STICKY BUTTON (BOTTOM RIGHT) -->
  <g transform="translate({w - 180}, {h - 130})">
    <rect x="0" y="0" width="150" height="48" rx="24" class="btn-sketch-dark" />
    <text x="75" y="29" class="font-btn-white" font-size="13">🚨 DARURAT 113</text>
  </g>

  <!-- FOOTER -->
  <g transform="translate(15, {h - 70})">
    <rect x="0" y="0" width="{w - 30}" height="55" class="sketch-card" />
    <text x="15" y="24" class="font-body-bold">Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung</text>
    <text x="15" y="42" class="font-small">Markas Komando: Jl. Kapt. Piere Tendean No. 2 | Telp: (0721) 252741 | Hotline: 113</text>
    <text x="{w - 45}" y="32" class="font-small" text-anchor="end">Kelompok 8 IMK STIS © 2026</text>
  </g>
</svg>"""
    return svg


# ==============================================================================
# 2. LOW-FI WIREFRAME 02: MODUL BERITA (1000 x 1050)
# ==============================================================================
def generate_lowfi_02():
    w, h = 1000, 1080
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {STYLE_DEF}
  <rect x="0" y="0" width="{w}" height="{h}" class="sketch-bg" />
  <rect x="2" y="2" width="{w-4}" height="{h-4}" class="sketch-border" />

  {browser_chrome_lowfi(w, "http://damkar.bandarlampungkota.go.id/berita")}

  <!-- NAVBAR COMPACT -->
  <g transform="translate(15, 80)">
    <rect x="0" y="0" width="{w - 30}" height="45" class="sketch-card-white" />
    <text x="15" y="28" class="font-body-bold">DAMKAR BDL</text>
    <text x="380" y="28" class="font-body">[ Beranda ]</text>
    <text x="470" y="28" class="font-body-bold" text-decoration="underline">[ Berita ]</text>
    <text x="545" y="28" class="font-body">[ Dokumen ]</text>
    <text x="635" y="28" class="font-body">[ Galeri ]</text>
    <text x="710" y="28" class="font-body">[ Kontak ]</text>
    <rect x="{w - 170}" y="8" width="125" height="28" class="btn-sketch-dark" />
    <text x="{w - 107}" y="26" class="font-btn-white" font-size="11">DARURAT 113</text>
  </g>

  <!-- BREADCRUMBS & SECTION TITLE -->
  <g transform="translate(15, 140)">
    <text x="0" y="15" class="font-small">Beranda  /  Berita &amp; Catatan Operasi</text>
    <text x="0" y="45" class="font-title">WARTA KEJADIAN &amp; CATATAN OPERASIONAL</text>
    {text_placeholder_bars(0, 58, [550, 480], h=8, gap=5)}
  </g>

  <!-- SEARCH & PILL CATEGORY FILTERS -->
  <g transform="translate(15, 225)">
    <rect x="0" y="0" width="{w - 30}" height="50" class="sketch-card" />
    
    <rect x="15" y="10" width="300" height="30" class="sketch-card-white" />
    <text x="25" y="30" class="font-body">🔍 Cari peristiwa atau lokasi...</text>

    <!-- Pills -->
    <rect x="335" y="10" width="95" height="30" rx="15" class="btn-sketch-dark" />
    <text x="382" y="29" class="font-btn-white" font-size="11">Semua (48)</text>

    <rect x="440" y="10" width="125" height="30" rx="15" class="btn-sketch-white" />
    <text x="502" y="29" class="font-btn" font-size="11">Pemadaman (22)</text>

    <rect x="575" y="10" width="115" height="30" rx="15" class="btn-sketch-white" />
    <text x="632" y="29" class="font-btn" font-size="11">Rescue (16)</text>

    <rect x="700" y="10" width="115" height="30" rx="15" class="btn-sketch-white" />
    <text x="757" y="29" class="font-btn" font-size="11">Edukasi (7)</text>

    <rect x="825" y="10" width="115" height="30" rx="15" class="btn-sketch-white" />
    <text x="882" y="29" class="font-btn" font-size="11">Peringatan (3)</text>
  </g>

  <!-- FEATURED ARTICLE HEADLINE (2 COLUMNS) -->
  <g transform="translate(15, 290)">
    <rect x="0" y="0" width="{w - 30}" height="180" class="sketch-card-white" />
    {placeholder_image_lowfi(0, 0, 360, 180, "Foto Berita Utama")}

    <g transform="translate(385, 20)">
      <rect x="0" y="0" width="125" height="20" class="btn-sketch-dark" />
      <text x="62" y="14" class="font-btn-white" font-size="10">PEMADAMAN</text>
      <text x="140" y="14" class="font-small">18 September 2025 • Respon 11 Menit</text>

      <text x="0" y="48" class="font-title" font-size="17">Damkar Bandar Lampung Jinakkan Kebakaran Gudang</text>
      {text_placeholder_bars(0, 68, [540, 500, 460, 380], h=9, gap=6)}

      <rect x="0" y="125" width="160" height="32" class="btn-sketch-white" />
      <text x="80" y="146" class="font-btn">Baca Selengkapnya &gt;</text>
    </g>
  </g>

  <!-- 3x2 NEWS GRID -->
  <g transform="translate(15, 490)">
    <!-- Card 1 -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="310" height="210" class="sketch-card" />
      {placeholder_image_lowfi(10, 10, 290, 100, "Rescue Ular")}
      <text x="15" y="130" class="font-body-bold">Evakuasi Ular Sanca di Kemiling</text>
      {text_placeholder_bars(15, 142, [270, 230], h=8, gap=5)}
      <text x="15" y="185" class="font-small">14 Sep 2025 • Rincian &gt;</text>
    </g>

    <!-- Card 2 -->
    <g transform="translate(330, 0)">
      <rect x="0" y="0" width="310" height="210" class="sketch-card" />
      {placeholder_image_lowfi(10, 10, 290, 100, "Pelepasan Cincin")}
      <text x="15" y="130" class="font-body-bold">Aksi Cepat Damkar Lepas Cincin</text>
      {text_placeholder_bars(15, 142, [270, 230], h=8, gap=5)}
      <text x="15" y="185" class="font-small">10 Sep 2025 • Rincian &gt;</text>
    </g>

    <!-- Card 3 -->
    <g transform="translate(660, 0)">
      <rect x="0" y="0" width="310" height="210" class="sketch-card" />
      {placeholder_image_lowfi(10, 10, 290, 100, "Simulasi SD")}
      <text x="15" y="130" class="font-body-bold">Pelatihan Proteksi Dini Siswa SD</text>
      {text_placeholder_bars(15, 142, [270, 230], h=8, gap=5)}
      <text x="15" y="185" class="font-small">05 Sep 2025 • Rincian &gt;</text>
    </g>

    <!-- Card 4 -->
    <g transform="translate(0, 225)">
      <rect x="0" y="0" width="310" height="210" class="sketch-card" />
      {placeholder_image_lowfi(10, 10, 290, 100, "Uji Hidran")}
      <text x="15" y="130" class="font-body-bold">Inspeksi Kelayakan Hidran Kota</text>
      {text_placeholder_bars(15, 142, [270, 230], h=8, gap=5)}
      <text x="15" y="185" class="font-small">28 Agu 2025 • Rincian &gt;</text>
    </g>

    <!-- Card 5 -->
    <g transform="translate(330, 225)">
      <rect x="0" y="0" width="310" height="210" class="sketch-card" />
      {placeholder_image_lowfi(10, 10, 290, 100, "Cuaca Kemarau")}
      <text x="15" y="130" class="font-body-bold">Himbauan Pencegahan Api Terbuka</text>
      {text_placeholder_bars(15, 142, [270, 230], h=8, gap=5)}
      <text x="15" y="185" class="font-small">20 Agu 2025 • Rincian &gt;</text>
    </g>

    <!-- Card 6 -->
    <g transform="translate(660, 225)">
      <rect x="0" y="0" width="310" height="210" class="sketch-card" />
      {placeholder_image_lowfi(10, 10, 290, 100, "Simulasi Hotel")}
      <text x="15" y="130" class="font-body-bold">Uji Evakuasi Bencana Hotel</text>
      {text_placeholder_bars(15, 142, [270, 230], h=8, gap=5)}
      <text x="15" y="185" class="font-small">15 Agu 2025 • Rincian &gt;</text>
    </g>
  </g>

  <!-- PAGINATION -->
  <g transform="translate(380, 955)">
    <rect x="0" y="0" width="32" height="30" class="btn-sketch-white" />
    <text x="16" y="20" class="font-btn">&lt;</text>

    <rect x="40" y="0" width="30" height="30" class="btn-sketch-dark" />
    <text x="55" y="20" class="font-btn-white">1</text>

    <rect x="78" y="0" width="30" height="30" class="btn-sketch-white" />
    <text x="93" y="20" class="font-btn">2</text>

    <rect x="116" y="0" width="30" height="30" class="btn-sketch-white" />
    <text x="131" y="20" class="font-btn">3</text>

    <text x="160" y="20" class="font-body-bold">...</text>

    <rect x="180" y="0" width="30" height="30" class="btn-sketch-white" />
    <text x="195" y="20" class="font-btn">8</text>

    <rect x="218" y="0" width="32" height="30" class="btn-sketch-white" />
    <text x="234" y="20" class="font-btn">&gt;</text>
  </g>

  <!-- FOOTER -->
  <g transform="translate(15, {h - 60})">
    <rect x="0" y="0" width="{w - 30}" height="45" class="sketch-card" />
    <text x="15" y="28" class="font-small">Dinas Pemadam Kebakaran &amp; Penyelamatan Kota Bandar Lampung • Siaga 24 Jam Hotline: 113</text>
    <text x="{w - 45}" y="28" class="font-small" text-anchor="end">Kelompok 8 IMK STIS © 2026</text>
  </g>
</svg>"""
    return svg


# ==============================================================================
# 3. LOW-FI WIREFRAME 03: MODUL DOKUMEN & SOP (1000 x 1000)
# ==============================================================================
def generate_lowfi_03():
    w, h = 1000, 1020
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {STYLE_DEF}
  <rect x="0" y="0" width="{w}" height="{h}" class="sketch-bg" />
  <rect x="2" y="2" width="{w-4}" height="{h-4}" class="sketch-border" />

  {browser_chrome_lowfi(w, "http://damkar.bandarlampungkota.go.id/dokumen")}

  <!-- NAVBAR COMPACT -->
  <g transform="translate(15, 80)">
    <rect x="0" y="0" width="{w - 30}" height="45" class="sketch-card-white" />
    <text x="15" y="28" class="font-body-bold">DAMKAR BDL</text>
    <text x="380" y="28" class="font-body">[ Beranda ]</text>
    <text x="470" y="28" class="font-body">[ Berita ]</text>
    <text x="545" y="28" class="font-body-bold" text-decoration="underline">[ Dokumen ]</text>
    <text x="635" y="28" class="font-body">[ Galeri ]</text>
    <text x="710" y="28" class="font-body">[ Kontak ]</text>
    <rect x="{w - 170}" y="8" width="125" height="28" class="btn-sketch-dark" />
    <text x="{w - 107}" y="26" class="font-btn-white" font-size="11">DARURAT 113</text>
  </g>

  <!-- HEADER -->
  <g transform="translate(15, 140)">
    <text x="0" y="15" class="font-small">Beranda  /  Dokumen &amp; SOP</text>
    <text x="0" y="45" class="font-title">DOKUMEN KEDINASAN, SOP, &amp; REGULASI</text>
    {text_placeholder_bars(0, 58, [580, 490], h=8, gap=5)}
  </g>

  <!-- SEARCH & FILTER TOOLBAR -->
  <g transform="translate(15, 225)">
    <rect x="0" y="0" width="{w - 30}" height="50" class="sketch-card" />
    <rect x="15" y="10" width="420" height="30" class="sketch-card-white" />
    <text x="25" y="30" class="font-body">🔍 Cari dokumen (LKJIP, SOP Gedung, Renstra)...</text>

    <!-- Dropdown Filter Mock -->
    <rect x="450" y="10" width="220" height="30" class="sketch-card-white" />
    <text x="465" y="30" class="font-body">Semua Kategori Dokumen</text>
    <text x="645" y="30" class="font-body-bold">▼</text>

    <text x="{w - 50}" y="30" class="font-small" text-anchor="end">Menampilkan 5 dari 24 Dokumen</text>
  </g>

  <!-- DATA TABLE -->
  <g transform="translate(15, 290)">
    <!-- Table Header -->
    <rect x="0" y="0" width="{w - 30}" height="35" class="sketch-card" />
    <text x="15" y="22" class="font-body-bold">NAMA DOKUMEN &amp; DESKRIPSI</text>
    <text x="500" y="22" class="font-body-bold">KATEGORI</text>
    <text x="660" y="22" class="font-body-bold">FORMAT / UKURAN</text>
    <text x="810" y="22" class="font-body-bold">TANGGAL</text>
    <text x="910" y="22" class="font-body-bold">AKSI</text>

    <!-- Row 1 -->
    <g transform="translate(0, 35)">
      <rect x="0" y="0" width="{w - 30}" height="70" class="sketch-card-white" />
      <text x="15" y="25" class="font-body-bold">SOP Penanggulangan Kebakaran Gedung</text>
      {text_placeholder_bars(15, 35, [440, 380], h=7, gap=4)}
      <text x="500" y="32" class="font-body">SOP Kedaruratan</text>
      <text x="660" y="32" class="font-body">PDF (2,4 MB)</text>
      <text x="810" y="32" class="font-body">12 Jan 2025</text>
      <rect x="880" y="16" width="75" height="30" class="btn-sketch-dark" />
      <text x="917" y="35" class="font-btn-white" font-size="11">Unduh</text>
    </g>

    <!-- Row 2 -->
    <g transform="translate(0, 105)">
      <rect x="0" y="0" width="{w - 30}" height="70" class="sketch-card" />
      <text x="15" y="25" class="font-body-bold">Laporan Kinerja (LKJIP) Tahun 2024</text>
      {text_placeholder_bars(15, 35, [440, 380], h=7, gap=4)}
      <text x="500" y="32" class="font-body">Akuntabilitas</text>
      <text x="660" y="32" class="font-body">PDF (4,1 MB)</text>
      <text x="810" y="32" class="font-body">28 Feb 2025</text>
      <rect x="880" y="16" width="75" height="30" class="btn-sketch-dark" />
      <text x="917" y="35" class="font-btn-white" font-size="11">Unduh</text>
    </g>

    <!-- Row 3 -->
    <g transform="translate(0, 175)">
      <rect x="0" y="0" width="{w - 30}" height="70" class="sketch-card-white" />
      <text x="15" y="25" class="font-body-bold">SOP Evakuasi Satwa Liar (Ular / Tawon)</text>
      {text_placeholder_bars(15, 35, [440, 380], h=7, gap=4)}
      <text x="500" y="32" class="font-body">Layanan Rescue</text>
      <text x="660" y="32" class="font-body">PDF (1,8 MB)</text>
      <text x="810" y="32" class="font-body">05 Mei 2024</text>
      <rect x="880" y="16" width="75" height="30" class="btn-sketch-dark" />
      <text x="917" y="35" class="font-btn-white" font-size="11">Unduh</text>
    </g>

    <!-- Row 4 -->
    <g transform="translate(0, 245)">
      <rect x="0" y="0" width="{w - 30}" height="70" class="sketch-card" />
      <text x="15" y="25" class="font-body-bold">Perda No. 03/2021 Proteksi Kebakaran</text>
      {text_placeholder_bars(15, 35, [440, 380], h=7, gap=4)}
      <text x="500" y="32" class="font-body">Regulasi Daerah</text>
      <text x="660" y="32" class="font-body">PDF (3,5 MB)</text>
      <text x="810" y="32" class="font-body">14 Nov 2021</text>
      <rect x="880" y="16" width="75" height="30" class="btn-sketch-dark" />
      <text x="917" y="35" class="font-btn-white" font-size="11">Unduh</text>
    </g>

    <!-- Row 5 -->
    <g transform="translate(0, 315)">
      <rect x="0" y="0" width="{w - 30}" height="70" class="sketch-card-white" />
      <text x="15" y="25" class="font-body-bold">Formulir Permohonan Simulasi Pelatihan</text>
      {text_placeholder_bars(15, 35, [440, 380], h=7, gap=4)}
      <text x="500" y="32" class="font-body">Formulir Publik</text>
      <text x="660" y="32" class="font-body">PDF (820 KB)</text>
      <text x="810" y="32" class="font-body">10 Agu 2024</text>
      <rect x="880" y="16" width="75" height="30" class="btn-sketch-dark" />
      <text x="917" y="35" class="font-btn-white" font-size="11">Unduh</text>
    </g>
  </g>

  <!-- FEEDBACK TOAST NOTIFICATION -->
  <g transform="translate(15, 710)">
    <rect x="0" y="0" width="460" height="42" class="sketch-card-white" stroke-width="2" />
    <text x="15" y="26" class="font-body-bold">[ v ] Berkas "SOP Penanggulangan Kebakaran Gedung" berhasil diunduh.</text>
  </g>

  <!-- REQUEST BOX -->
  <g transform="translate(15, 775)">
    <rect x="0" y="0" width="{w - 30}" height="100" class="sketch-card" />
    <text x="25" y="35" class="font-title" font-size="16">TIDAK MENEMUKAN DOKUMEN YANG DICARI?</text>
    {text_placeholder_bars(25, 48, [620, 560], h=8, gap=5)}
    <rect x="{w - 240}" y="32" width="180" height="38" class="btn-sketch-white" />
    <text x="{w - 150}" y="56" class="font-btn">Ajukan Permohonan &gt;</text>
  </g>

  <!-- FOOTER -->
  <g transform="translate(15, {h - 60})">
    <rect x="0" y="0" width="{w - 30}" height="45" class="sketch-card" />
    <text x="15" y="28" class="font-small">Dinas Pemadam Kebakaran &amp; Penyelamatan Kota Bandar Lampung • Siaga 24 Jam Hotline: 113</text>
    <text x="{w - 45}" y="28" class="font-small" text-anchor="end">Kelompok 8 IMK STIS © 2026</text>
  </g>
</svg>"""
    return svg


# ==============================================================================
# 4. LOW-FI WIREFRAME 04: MODUL GALERI (1000 x 980)
# ==============================================================================
def generate_lowfi_04():
    w, h = 1000, 1000
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {STYLE_DEF}
  <rect x="0" y="0" width="{w}" height="{h}" class="sketch-bg" />
  <rect x="2" y="2" width="{w-4}" height="{h-4}" class="sketch-border" />

  {browser_chrome_lowfi(w, "http://damkar.bandarlampungkota.go.id/galeri")}

  <!-- NAVBAR COMPACT -->
  <g transform="translate(15, 80)">
    <rect x="0" y="0" width="{w - 30}" height="45" class="sketch-card-white" />
    <text x="15" y="28" class="font-body-bold">DAMKAR BDL</text>
    <text x="380" y="28" class="font-body">[ Beranda ]</text>
    <text x="470" y="28" class="font-body">[ Berita ]</text>
    <text x="545" y="28" class="font-body">[ Dokumen ]</text>
    <text x="635" y="28" class="font-body-bold" text-decoration="underline">[ Galeri ]</text>
    <text x="710" y="28" class="font-body">[ Kontak ]</text>
    <rect x="{w - 170}" y="8" width="125" height="28" class="btn-sketch-dark" />
    <text x="{w - 107}" y="26" class="font-btn-white" font-size="11">DARURAT 113</text>
  </g>

  <!-- HEADER -->
  <g transform="translate(15, 140)">
    <text x="0" y="15" class="font-small">Beranda  /  Galeri</text>
    <text x="0" y="45" class="font-title">GALERI DOKUMENTASI AKSI OPERASIONAL &amp; RESCUE</text>
    {text_placeholder_bars(0, 58, [580, 510], h=8, gap=5)}
  </g>

  <!-- FILTER TABS -->
  <g transform="translate(15, 220)">
    <rect x="0" y="0" width="{w - 30}" height="45" class="sketch-card" />
    
    <rect x="15" y="8" width="115" height="28" rx="14" class="btn-sketch-dark" />
    <text x="72" y="26" class="font-btn-white" font-size="11">Semua (36)</text>

    <rect x="140" y="8" width="140" height="28" rx="14" class="btn-sketch-white" />
    <text x="210" y="26" class="font-btn" font-size="11">Pemadaman (15)</text>

    <rect x="290" y="8" width="130" height="28" rx="14" class="btn-sketch-white" />
    <text x="355" y="26" class="font-btn" font-size="11">Aksi Rescue (12)</text>

    <rect x="430" y="8" width="140" height="28" rx="14" class="btn-sketch-white" />
    <text x="500" y="26" class="font-btn" font-size="11">Sosialisasi (6)</text>

    <rect x="580" y="8" width="125" height="28" rx="14" class="btn-sketch-white" />
    <text x="642" y="26" class="font-btn" font-size="11">Video Edukasi (3)</text>
  </g>

  <!-- 3x2 PHOTO GRID WITH X -->
  <g transform="translate(15, 280)">
    <!-- Photo 1 -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="310" height="235" class="sketch-card" />
      {placeholder_image_lowfi(10, 10, 290, 160, "Foto: Pemadaman Lahan")}
      <text x="15" y="195" class="font-body-bold">Pemadaman Lahan Sukarame</text>
      <text x="15" y="215" class="font-small">18 Sep 2025 • Durasi 45 Mnt</text>
    </g>

    <!-- Photo 2 -->
    <g transform="translate(330, 0)">
      <rect x="0" y="0" width="310" height="235" class="sketch-card" />
      {placeholder_image_lowfi(10, 10, 290, 160, "Foto: Rescue Sumur")}
      <text x="15" y="195" class="font-body-bold">Evakuasi Kucing di Sumur</text>
      <text x="15" y="215" class="font-small">14 Sep 2025 • Teluk Betung</text>
    </g>

    <!-- Photo 3 -->
    <g transform="translate(660, 0)">
      <rect x="0" y="0" width="310" height="235" class="sketch-card" />
      {placeholder_image_lowfi(10, 10, 290, 160, "Foto: Lepas Cincin")}
      <text x="15" y="195" class="font-body-bold">Pelepasan Cincin Macet di Jari</text>
      <text x="15" y="215" class="font-small">10 Sep 2025 • Mako Pusat</text>
    </g>

    <!-- Photo 4 -->
    <g transform="translate(0, 255)">
      <rect x="0" y="0" width="310" height="235" class="sketch-card" />
      {placeholder_image_lowfi(10, 10, 290, 160, "Foto: Sosialisasi SD")}
      <text x="15" y="195" class="font-body-bold">Simulasi APAR Siswa SD</text>
      <text x="15" y="215" class="font-small">02 Sep 2025 • Posko Kedaton</text>
    </g>

    <!-- Photo 5 -->
    <g transform="translate(330, 255)">
      <rect x="0" y="0" width="310" height="235" class="sketch-card" />
      {placeholder_image_lowfi(10, 10, 290, 160, "Foto: Cek Hidran")}
      <text x="15" y="195" class="font-body-bold">Uji Tekanan Hidran Pasar</text>
      <text x="15" y="215" class="font-small">25 Agu 2025 • Tj. Karang</text>
    </g>

    <!-- Photo 6 (Video Mock) -->
    <g transform="translate(660, 255)">
      <rect x="0" y="0" width="310" height="235" class="sketch-card" />
      {placeholder_image_lowfi(10, 10, 290, 160, "Video: Tabung Gas (▶)")}
      <text x="15" y="195" class="font-body-bold">Langkah Padamkan Api Gas LPG</text>
      <text x="15" y="215" class="font-small">18 Agu 2025 • Durasi 3:45 Mnt</text>
    </g>
  </g>

  <!-- LIGHTBOX CALLOUT -->
  <g transform="translate(15, 795)">
    <rect x="0" y="0" width="{w - 30}" height="70" class="sketch-card-white" stroke-dasharray="6 3" />
    <text x="20" y="30" class="font-body-bold">FITUR LIGHTBOX PREVIEW MODAL (DIRECT MANIPULATION):</text>
    <text x="20" y="50" class="font-body">Klik pada kartu gambar membuka pratinjau resolusi tinggi layar penuh lengkap dengan caption dan tombol unduh.</text>
  </g>

  <!-- FOOTER -->
  <g transform="translate(15, {h - 60})">
    <rect x="0" y="0" width="{w - 30}" height="45" class="sketch-card" />
    <text x="15" y="28" class="font-small">Dinas Pemadam Kebakaran &amp; Penyelamatan Kota Bandar Lampung • Siaga 24 Jam Hotline: 113</text>
    <text x="{w - 45}" y="28" class="font-small" text-anchor="end">Kelompok 8 IMK STIS © 2026</text>
  </g>
</svg>"""
    return svg


# ==============================================================================
# 5. LOW-FI WIREFRAME 05: MODUL KONTAK & PENGADUAN (1000 x 1150)
# ==============================================================================
def generate_lowfi_05():
    w, h = 1000, 1180
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {STYLE_DEF}
  <rect x="0" y="0" width="{w}" height="{h}" class="sketch-bg" />
  <rect x="2" y="2" width="{w-4}" height="{h-4}" class="sketch-border" />

  {browser_chrome_lowfi(w, "http://damkar.bandarlampungkota.go.id/kontak")}

  <!-- NAVBAR COMPACT -->
  <g transform="translate(15, 80)">
    <rect x="0" y="0" width="{w - 30}" height="45" class="sketch-card-white" />
    <text x="15" y="28" class="font-body-bold">DAMKAR BDL</text>
    <text x="380" y="28" class="font-body">[ Beranda ]</text>
    <text x="470" y="28" class="font-body">[ Berita ]</text>
    <text x="545" y="28" class="font-body">[ Dokumen ]</text>
    <text x="635" y="28" class="font-body">[ Galeri ]</text>
    <text x="710" y="28" class="font-body-bold" text-decoration="underline">[ Kontak ]</text>
    <rect x="{w - 170}" y="8" width="125" height="28" class="btn-sketch-dark" />
    <text x="{w - 107}" y="26" class="font-btn-white" font-size="11">DARURAT 113</text>
  </g>

  <!-- HEADER -->
  <g transform="translate(15, 140)">
    <text x="0" y="15" class="font-small">Beranda  /  Kontak &amp; Posko</text>
    <text x="0" y="45" class="font-title">KONTAK POSKO SIAGA &amp; FORMULIR LAPORAN KEJADIAN</text>
    {text_placeholder_bars(0, 58, [580, 510], h=8, gap=5)}
  </g>

  <!-- TWO-COLUMN ARCHITECTURE -->
  <g transform="translate(15, 220)">
    
    <!-- LEFT COLUMN: DIREKTORI 6 POSKO (w=420) -->
    <g transform="translate(0, 0)">
      <text x="0" y="20" class="font-title" font-size="16">DIREKTORI POSKO SIAGA</text>

      <!-- Mako Pusat Card -->
      <g transform="translate(0, 35)">
        <rect x="0" y="0" width="420" height="135" class="sketch-card" stroke-width="2.5" />
        <rect x="15" y="12" width="145" height="20" class="btn-sketch-dark" />
        <text x="87" y="26" class="font-btn-white" font-size="10">MARKAS PUSAT (24/7)</text>
        <text x="15" y="55" class="font-subhead">Mako Pemadam Kebakaran</text>
        <text x="15" y="73" class="font-body">Jl. Kapt. Piere Tendean No. 2, Tj. Karang</text>
        <text x="15" y="90" class="font-body-bold">Telp: (0721) 252741  |  Hotline: 113 / 112</text>
        <rect x="15" y="100" width="150" height="26" class="btn-sketch-white" />
        <text x="90" y="118" class="font-btn" font-size="10">📞 Panggil Mako</text>
      </g>

      <!-- Posko Kedaton -->
      <g transform="translate(0, 185)">
        <rect x="0" y="0" width="420" height="75" class="sketch-card-white" />
        <text x="15" y="25" class="font-body-bold">Posko Wilayah Kedaton</text>
        <text x="15" y="43" class="font-small">Jl. Teuku Umar No. 88 | Wilayah: Rajabasa, Kedaton</text>
        <text x="15" y="60" class="font-body-bold">Telp: (0721) 701113</text>
        <rect x="310" y="25" width="95" height="28" class="btn-sketch-dark" />
        <text x="357" y="44" class="font-btn-white" font-size="10">Telepon</text>
      </g>

      <!-- Posko Sukarame -->
      <g transform="translate(0, 275)">
        <rect x="0" y="0" width="420" height="75" class="sketch-card-white" />
        <text x="15" y="25" class="font-body-bold">Posko Wilayah Sukarame</text>
        <text x="15" y="43" class="font-small">Jl. Endro Suratmin | Wilayah: Sukarame, Way Halim</text>
        <text x="15" y="60" class="font-body-bold">Telp: (0721) 782113</text>
        <rect x="310" y="25" width="95" height="28" class="btn-sketch-dark" />
        <text x="357" y="44" class="font-btn-white" font-size="10">Telepon</text>
      </g>

      <!-- Posko Kemiling -->
      <g transform="translate(0, 365)">
        <rect x="0" y="0" width="420" height="75" class="sketch-card-white" />
        <text x="15" y="25" class="font-body-bold">Posko Wilayah Kemiling</text>
        <text x="15" y="43" class="font-small">Jl. Imam Bonjol | Wilayah: Kemiling, Langkapura</text>
        <text x="15" y="60" class="font-body-bold">Telp: (0721) 271113</text>
        <rect x="310" y="25" width="95" height="28" class="btn-sketch-dark" />
        <text x="357" y="44" class="font-btn-white" font-size="10">Telepon</text>
      </g>

      <!-- Posko Panjang -->
      <g transform="translate(0, 455)">
        <rect x="0" y="0" width="420" height="75" class="sketch-card-white" />
        <text x="15" y="25" class="font-body-bold">Posko Wilayah Panjang</text>
        <text x="15" y="43" class="font-small">Jl. Yos Sudarso No. 12 | Wilayah: Panjang, Bumi Waras</text>
        <text x="15" y="60" class="font-body-bold">Telp: (0721) 31113</text>
        <rect x="310" y="25" width="95" height="28" class="btn-sketch-dark" />
        <text x="357" y="44" class="font-btn-white" font-size="10">Telepon</text>
      </g>

      <!-- Posko Teluk Betung -->
      <g transform="translate(0, 545)">
        <rect x="0" y="0" width="420" height="75" class="sketch-card-white" />
        <text x="15" y="25" class="font-body-bold">Posko Wilayah Teluk Betung</text>
        <text x="15" y="43" class="font-small">Jl. Basuki Rahmat No. 4 | Wilayah: Teluk Betung</text>
        <text x="15" y="60" class="font-body-bold">Telp: (0721) 481113</text>
        <rect x="310" y="25" width="95" height="28" class="btn-sketch-dark" />
        <text x="357" y="44" class="font-btn-white" font-size="10">Telepon</text>
      </g>
    </g>

    <!-- RIGHT COLUMN: FORMULIR LAPORAN (w=520) -->
    <g transform="translate(450, 0)">
      <text x="0" y="20" class="font-title" font-size="16">FORMULIR LAPORAN INSIDEN</text>

      <rect x="0" y="35" width="520" height="660" class="sketch-card" />
      
      <g transform="translate(25, 20)">
        <!-- Input 1: Nama -->
        <text x="0" y="20" class="font-body-bold">Nama Pelapor *</text>
        <rect x="0" y="30" width="470" height="34" class="sketch-card-white" />
        <text x="15" y="52" class="font-body">Alif Zakiansyah</text>
        <text x="445" y="53" class="font-body-bold">[ v ]</text>

        <!-- Input 2: Kontak -->
        <text x="0" y="90" class="font-body-bold">Nomor Telepon / WhatsApp Aktif *</text>
        <rect x="0" y="100" width="470" height="34" class="sketch-card-white" />
        <text x="15" y="122" class="font-body">0812-9876-5432</text>
        <text x="445" y="123" class="font-body-bold">[ v ]</text>

        <!-- Input 3: Lokasi -->
        <text x="0" y="160" class="font-body-bold">Alamat &amp; Kecamatan Lokasi Kejadian *</text>
        <rect x="0" y="170" width="470" height="34" class="sketch-card-white" />
        <text x="15" y="192" class="font-body">Jl. Raden Intan No. 45, Kecamatan Enggal</text>
        <text x="445" y="193" class="font-body-bold">[ v ]</text>

        <!-- Input 4: Jenis Kejadian Dropdown -->
        <text x="0" y="230" class="font-body-bold">Jenis Kejadian Bencana / Rescue *</text>
        <rect x="0" y="240" width="470" height="34" class="sketch-card-white" />
        <text x="15" y="262" class="font-body">Kebakaran Bangunan Pemukiman / Ruko</text>
        <text x="445" y="262" class="font-body-bold">▼</text>

        <!-- Input 5: Keterangan -->
        <text x="0" y="300" class="font-body-bold">Keterangan Situasi &amp; Titik Api *</text>
        <rect x="0" y="310" width="470" height="80" class="sketch-card-white" />
        {text_placeholder_bars(15, 325, [430, 400, 360], h=8, gap=5)}
        <text x="460" y="380" class="font-small" text-anchor="end">128/500 karakter</text>

        <!-- Input 6: Upload Drag & Drop -->
        <text x="0" y="415" class="font-body-bold">Unggah Foto Bukti Kejadian (Opsional)</text>
        <rect x="0" y="425" width="470" height="60" class="sketch-card-white" stroke-dasharray="6 3" />
        <text x="235" y="455" class="font-small" text-anchor="middle">[ Seret &amp; Lepas Berkas Foto ke Sini ]</text>
        <text x="235" y="472" class="font-small" text-anchor="middle">(Maksimal 3 foto JPG/PNG)</text>

        <!-- Warning Anti-Prank -->
        <g transform="translate(0, 500)">
          <rect x="0" y="0" width="470" height="34" class="sketch-card-white" />
          <text x="15" y="22" class="font-small">Pencegahan galat: Petugas akan menelepon konfirmasi dalam &lt;60 detik.</text>
        </g>

        <!-- Submit Button -->
        <rect x="0" y="550" width="470" height="44" class="btn-sketch-dark" />
        <text x="235" y="578" class="font-btn-white" font-size="13">🚨 KIRIM LAPORAN KEJADIAN SEKARANG</text>
      </g>
    </g>
  </g>

  <!-- FOOTER -->
  <g transform="translate(15, {h - 60})">
    <rect x="0" y="0" width="{w - 30}" height="45" class="sketch-card" />
    <text x="15" y="28" class="font-small">Dinas Pemadam Kebakaran &amp; Penyelamatan Kota Bandar Lampung • Siaga 24 Jam Hotline: 113</text>
    <text x="{w - 45}" y="28" class="font-small" text-anchor="end">Kelompok 8 IMK STIS © 2026</text>
  </g>
</svg>"""
    return svg


# ==============================================================================
# 6. LOW-FI WIREFRAME 06: SMARTPHONE MOBILE VIEWPORT (420 x 950)
# ==============================================================================
def generate_lowfi_06():
    w, h = 440, 960
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {STYLE_DEF}
  <rect x="0" y="0" width="{w}" height="{h}" class="sketch-bg" />
  
  <!-- PHONE OUTER FRAME -->
  <rect x="15" y="10" width="410" height="940" rx="36" class="sketch-card" stroke-width="3" />
  <!-- Phone Screen Inner -->
  <rect x="25" y="20" width="390" height="920" rx="28" class="sketch-card-white" stroke-width="2" />
  
  <!-- Speaker / Notch Mock -->
  <rect x="160" y="30" width="120" height="16" rx="8" fill="#222222" />
  <circle cx="260" cy="38" r="3" fill="#666666" />

  <!-- TOP STATUS BAR -->
  <g transform="translate(35, 60)">
    <rect x="0" y="0" width="370" height="24" class="sketch-card" />
    <text x="185" y="16" class="font-body-bold" font-size="10" text-anchor="middle">🚨 SIAGA 24 JAM | SPM &lt; 15 MNT</text>
  </g>

  <!-- MOBILE NAVBAR -->
  <g transform="translate(35, 92)">
    <rect x="0" y="0" width="370" height="42" class="sketch-card-white" />
    <text x="12" y="27" class="font-body-bold" font-size="12">🚒 DAMKAR BDL</text>
    <text x="305" y="27" class="font-body-bold">🔍</text>
    <text x="340" y="27" class="font-body-bold">☰</text>
  </g>

  <!-- MOBILE HERO -->
  <g transform="translate(35, 142)">
    <rect x="0" y="0" width="370" height="225" class="sketch-card" />
    
    <rect x="12" y="12" width="145" height="18" class="btn-sketch-white" />
    <text x="84" y="25" class="font-btn" font-size="9">SPM RESPON &lt; 15 MNT</text>

    <text x="12" y="52" class="font-title" font-size="15">TANGGAP DARURAT 24 JAM</text>
    <text x="12" y="70" class="font-title" font-size="15">KOTA BANDAR LAMPUNG</text>

    {text_placeholder_bars(12, 85, [340, 310, 280], h=7, gap=5)}

    <!-- BIG EMERGENCY THUMB-ZONE CALL BUTTON -->
    <rect x="12" y="125" width="346" height="48" rx="24" class="btn-sketch-dark" />
    <text x="185" y="154" class="font-btn-white" font-size="14">📞 HUBUNGI DARURAT 113</text>
    <text x="185" y="168" class="font-small" fill="#ffffff" text-anchor="middle">Panggilan 1-Ketukan Bebas Pulsa</text>

    <rect x="12" y="180" width="346" height="34" class="btn-sketch-white" />
    <text x="185" y="202" class="font-btn" font-size="11">Lapor Insiden Online</text>
  </g>

  <!-- 2x2 SERVICES GRID -->
  <g transform="translate(35, 380)">
    <text x="0" y="15" class="font-body-bold" font-size="12">LAYANAN UTAMA</text>

    <!-- Svc 1 -->
    <rect x="0" y="25" width="180" height="75" class="sketch-card-white" />
    <text x="10" y="48" class="font-body-bold" font-size="11">🔥 Pemadaman</text>
    {text_placeholder_bars(10, 58, [155, 130], h=6, gap=4)}
    <text x="10" y="90" class="font-small">Panggil 113 &gt;</text>

    <!-- Svc 2 -->
    <rect x="190" y="25" width="180" height="75" class="sketch-card-white" />
    <text x="200" y="48" class="font-body-bold" font-size="11">🛡️ Aksi Rescue</text>
    {text_placeholder_bars(200, 58, [155, 130], h=6, gap=4)}
    <text x="200" y="90" class="font-small">Lapor Rescue &gt;</text>

    <!-- Svc 3 -->
    <rect x="0" y="108" width="180" height="75" class="sketch-card-white" />
    <text x="10" y="131" class="font-body-bold" font-size="11">📍 6 Posko Kec.</text>
    {text_placeholder_bars(10, 141, [155, 130], h=6, gap=4)}
    <text x="10" y="173" class="font-small">Lihat Posko &gt;</text>

    <!-- Svc 4 -->
    <rect x="190" y="108" width="180" height="75" class="sketch-card-white" />
    <text x="200" y="131" class="font-body-bold" font-size="11">📄 Dokumen SOP</text>
    {text_placeholder_bars(200, 141, [155, 130], h=6, gap=4)}
    <text x="200" y="173" class="font-small">Unduh PDF &gt;</text>
  </g>

  <!-- 2x2 STATS GRID -->
  <g transform="translate(35, 585)">
    <text x="0" y="15" class="font-body-bold" font-size="12">STATISTIK KINERJA</text>

    <rect x="0" y="25" width="180" height="60" class="sketch-card" />
    <text x="10" y="52" class="font-title" font-size="20">271</text>
    <text x="60" y="52" class="font-small">Kebakaran '24</text>

    <rect x="190" y="25" width="180" height="60" class="sketch-card" />
    <text x="200" y="52" class="font-title" font-size="20">518</text>
    <text x="250" y="52" class="font-small">Rescue '25</text>

    <rect x="0" y="92" width="180" height="60" class="sketch-card" />
    <text x="10" y="119" class="font-title" font-size="20">18</text>
    <text x="60" y="119" class="font-small">Armada Aktif</text>

    <rect x="190" y="92" width="180" height="60" class="sketch-card" />
    <text x="200" y="119" class="font-title" font-size="20">&lt;15m</text>
    <text x="250" y="119" class="font-small">Waktu SPM</text>
  </g>

  <!-- QUICK POSKO ACCORDION -->
  <g transform="translate(35, 760)">
    <text x="0" y="15" class="font-body-bold" font-size="12">DIREKTORI POSKO CEPAT</text>

    <rect x="0" y="25" width="370" height="42" class="sketch-card-white" />
    <text x="12" y="45" class="font-body-bold" font-size="11">Mako Pusat (Tj. Karang Pusat)</text>
    <rect x="290" y="32" width="70" height="26" class="btn-sketch-dark" />
    <text x="325" y="49" class="font-btn-white" font-size="10">Telp</text>

    <rect x="0" y="72" width="370" height="42" class="sketch-card-white" />
    <text x="12" y="92" class="font-body-bold" font-size="11">Posko Kedaton (Jl. Teuku Umar)</text>
    <rect x="290" y="79" width="70" height="26" class="btn-sketch-dark" />
    <text x="325" y="96" class="font-btn-white" font-size="10">Telp</text>
  </g>

  <!-- FIXED BOTTOM THUMB BAR -->
  <g transform="translate(25, 875)">
    <rect x="0" y="0" width="390" height="65" class="sketch-card" stroke-width="2" />
    
    <rect x="15" y="10" width="170" height="44" rx="22" class="btn-sketch-dark" />
    <text x="100" y="37" class="font-btn-white" font-size="12">🚨 113 DARURAT</text>

    <rect x="205" y="10" width="170" height="44" rx="22" class="btn-sketch-white" />
    <text x="290" y="37" class="font-btn" font-size="12">💬 WhatsApp</text>
  </g>
</svg>"""
    return svg


def main():
    generators = [
        ("lowfi_wireframe_01_beranda", generate_lowfi_01),
        ("lowfi_wireframe_02_berita", generate_lowfi_02),
        ("lowfi_wireframe_03_dokumen", generate_lowfi_03),
        ("lowfi_wireframe_04_galeri", generate_lowfi_04),
        ("lowfi_wireframe_05_kontak", generate_lowfi_05),
        ("lowfi_wireframe_06_mobile", generate_lowfi_06),
    ]

    print("=================================================================")
    print("MEMULAI GENERASI BALSAMIQ / ULTRA LOW-FIDELITY WIREFRAMES")
    print("=================================================================")

    for name, gen_fn in generators:
        svg_content = gen_fn()
        svg_path = os.path.join(OUT_DIR, f"{name}.svg")
        png_path = os.path.join(OUT_DIR, f"{name}.png")

        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"[*] Berhasil menulis SVG: {svg_path} ({os.path.getsize(svg_path):,} bytes)")

        # Convert to PNG using convert / magick
        res = subprocess.run(["convert", svg_path, png_path], capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(png_path):
            print(f"    -> Berhasil mengonversi ke PNG: {png_path} ({os.path.getsize(png_path):,} bytes)")
        else:
            print(f"    [!] Gagal konversi ke PNG: {res.stderr}")

    print("\n[OK] Seluruh berkas ultra low-fidelity wireframe berhasil dihasilkan!")

if __name__ == "__main__":
    main()
