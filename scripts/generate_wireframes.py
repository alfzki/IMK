"""
Script generator untuk menghasilkan rancangan wireframe dan low-fidelity mockup
dalam format SVG dan PNG untuk 5 modul utama dan framework global website
Dinas Pemadam Kebakaran dan Penyelamatan Kota Bandar Lampung.
"""

import os
import subprocess

OUT_DIR = "drafts/wireframes"
os.makedirs(OUT_DIR, exist_ok=True)

# Helper styles
STYLE_DEF = """
  <defs>
    <style>
      .bg-canvas { fill: #f8fafc; }
      .browser-chrome { fill: #f1f5f9; stroke: #cbd5e1; stroke-width: 1; }
      .browser-dot-red { fill: #ef4444; }
      .browser-dot-yellow { fill: #f59e0b; }
      .browser-dot-green { fill: #10b981; }
      .browser-url-bar { fill: #ffffff; stroke: #cbd5e1; stroke-width: 1; rx: 6; }
      .text-url { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 12px; fill: #475569; }
      
      .top-bar-bg { fill: #1e293b; }
      .top-bar-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 11px; font-weight: 600; fill: #f8fafc; }
      .top-bar-badge { fill: #dc2626; rx: 4; }
      
      .navbar-bg { fill: #ffffff; stroke: #e2e8f0; stroke-width: 1; }
      .nav-title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 15px; font-weight: 700; fill: #0f172a; }
      .nav-subtitle { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 10px; fill: #64748b; }
      .nav-link { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 13px; font-weight: 500; fill: #475569; }
      .nav-link-active { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 13px; font-weight: 700; fill: #1e40af; }
      
      .hero-bg { fill: #f1f5f9; stroke: #e2e8f0; stroke-width: 1; }
      .heading-xl { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 24px; font-weight: 800; fill: #0f172a; }
      .heading-lg { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 18px; font-weight: 700; fill: #0f172a; }
      .heading-md { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 15px; font-weight: 700; fill: #1e293b; }
      .text-body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 13px; fill: #475569; }
      .text-sm { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 11px; fill: #64748b; }
      
      .card-bg { fill: #ffffff; stroke: #cbd5e1; stroke-width: 1; rx: 8; }
      .placeholder-box { fill: #e2e8f0; stroke: #94a3b8; stroke-width: 1; stroke-dasharray: 4 4; }
      .placeholder-line { stroke: #cbd5e1; stroke-width: 1.5; }
      .placeholder-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 12px; fill: #64748b; font-weight: 600; text-anchor: middle; }
      
      .btn-primary { fill: #dc2626; rx: 6; }
      .btn-primary-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 13px; font-weight: 700; fill: #ffffff; text-anchor: middle; }
      .btn-secondary { fill: #ffffff; stroke: #94a3b8; stroke-width: 1.5; rx: 6; }
      .btn-secondary-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 13px; font-weight: 600; fill: #1e293b; text-anchor: middle; }
      .btn-navy { fill: #1e3a8a; rx: 6; }
      .btn-navy-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 13px; font-weight: 600; fill: #ffffff; text-anchor: middle; }

      .badge-bg { fill: #e2e8f0; rx: 4; }
      .badge-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 10px; font-weight: 600; fill: #334155; }
      .badge-red-bg { fill: #fee2e2; stroke: #fca5a5; stroke-width: 1; rx: 4; }
      .badge-red-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 10px; font-weight: 700; fill: #991b1b; }
      .badge-blue-bg { fill: #dbeafe; stroke: #93c5fd; stroke-width: 1; rx: 4; }
      .badge-blue-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 10px; font-weight: 700; fill: #1e40af; }
      
      .annotation-box { fill: #fef3c7; stroke: #f59e0b; stroke-width: 1.5; rx: 4; }
      .annotation-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 10px; font-weight: 700; fill: #92400e; }
      
      .sticky-btn-pulse { fill: #fee2e2; stroke: #ef4444; stroke-width: 2; stroke-dasharray: 4 2; }
      .sticky-btn-body { fill: #dc2626; rx: 28; filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.25)); }
      .sticky-btn-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 13px; font-weight: 800; fill: #ffffff; text-anchor: middle; }

      .table-hdr { fill: #f1f5f9; stroke: #cbd5e1; stroke-width: 1; }
      .table-cell { fill: #ffffff; stroke: #e2e8f0; stroke-width: 1; }
      .table-cell-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 12px; fill: #1e293b; }
      .table-hdr-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 12px; font-weight: 700; fill: #0f172a; }
    </style>
  </defs>
"""

def browser_chrome(w, title, url):
    clean_url = url.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""
    <!-- Browser Window Header -->
    <rect x="0" y="0" width="{w}" height="46" class="browser-chrome" />
    <circle cx="20" cy="23" r="6" class="browser-dot-red" />
    <circle cx="38" cy="23" r="6" class="browser-dot-yellow" />
    <circle cx="56" cy="23" r="6" class="browser-dot-green" />
    <rect x="180" y="9" width="{w - 360}" height="28" class="browser-url-bar" />
    <text x="{w // 2}" y="28" class="text-url" text-anchor="middle">🔒 {clean_url}</text>
    """

def top_emergency_bar(w, y):
    return f"""
    <!-- Top Emergency Bar -->
    <g transform="translate(0, {y})">
      <rect x="0" y="0" width="{w}" height="34" class="top-bar-bg" />
      <rect x="40" y="7" width="115" height="20" class="top-bar-badge" />
      <text x="97" y="21" class="top-bar-text" text-anchor="middle">SIAGA 24 JAM</text>
      <text x="170" y="21" class="top-bar-text">KOMITMEN SPM WAKTU TANGGAP &lt; 15 MENIT | POSKO UTAMA: (0721) 252741</text>
      <rect x="{w - 180}" y="5" width="140" height="24" fill="#dc2626" rx="4" />
      <text x="{w - 110}" y="21" class="top-bar-text" text-anchor="middle" font-weight="bold">📞 HOTLINE 113</text>
    </g>
    """

def navbar(w, y, active="Beranda"):
    tabs = [
        ("Beranda", "Beranda"),
        ("Berita &amp; Operasi", "Berita"),
        ("Dokumen &amp; SOP", "Dokumen"),
        ("Galeri Edukasi", "Galeri"),
        ("Kontak &amp; Posko", "Kontak")
    ]
    items_xml = ""
    start_x = 420
    for label, key in tabs:
        is_active = (active == key or key in active)
        cls = "nav-link-active" if is_active else "nav-link"
        clean_len = len(label.replace("&amp;", "&"))
        border = f'<line x1="{start_x}" y1="46" x2="{start_x + clean_len*7.5}" y2="46" stroke="#1e40af" stroke-width="2.5" />' if is_active else ""
        items_xml += f'<text x="{start_x}" y="36" class="{cls}">{label}</text>{border}'
        start_x += clean_len * 9.5 + 28

    return f"""
    <!-- Main Navbar -->
    <g transform="translate(0, {y})">
      <rect x="0" y="0" width="{w}" height="66" class="navbar-bg" />
      <!-- Logo wireframe -->
      <rect x="40" y="13" width="40" height="40" fill="#e2e8f0" stroke="#94a3b8" rx="6" />
      <text x="60" y="38" font-family="sans-serif" font-size="18" text-anchor="middle" fill="#64748b">🚒</text>
      <text x="92" y="30" class="nav-title">Dinas Pemadam Kebakaran &amp; Penyelamatan</text>
      <text x="92" y="47" class="nav-subtitle">Portal Informasi &amp; Kesiapsiagaan Publik Kota Bandar Lampung</text>
      
      {items_xml}

      <!-- Search input mock -->
      <rect x="{w - 240}" y="17" width="190" height="32" fill="#f8fafc" stroke="#cbd5e1" rx="6" />
      <text x="{w - 225}" y="38" font-family="sans-serif" font-size="11" fill="#94a3b8">🔍 Cari informasi...</text>
    </g>
    """

def sticky_emergency_button(x, y):
    return f"""
    <!-- Persistent Sticky Emergency Call Button (Fitts's Law Target) -->
    <g transform="translate({x}, {y})">
      <circle cx="36" cy="36" r="42" class="sticky-btn-pulse" />
      <rect x="0" y="8" width="165" height="56" rx="28" class="sticky-btn-body" />
      <text x="28" y="43" font-size="22" fill="#ffffff">🚨</text>
      <text x="56" y="34" class="sticky-btn-text" text-anchor="start">DARURAT 113</text>
      <text x="56" y="48" font-family="sans-serif" font-size="9" fill="#fee2e2" text-anchor="start">Panggil Cepat 1-Ketukan</text>

      <!-- HCI Callout Badge -->
      <rect x="20" y="-22" width="125" height="18" class="annotation-box" />
      <text x="82" y="-10" class="annotation-text" text-anchor="middle">HCI: Fitts's Law Target</text>
    </g>
    """

def footer(w, y):
    return f"""
    <!-- Footer Global Wireframe -->
    <g transform="translate(0, {y})">
      <rect x="0" y="0" width="{w}" height="170" fill="#0f172a" />
      
      <text x="40" y="35" font-family="sans-serif" font-size="15" font-weight="bold" fill="#f8fafc">Dinas Pemadam Kebakaran &amp; Penyelamatan Kota Bandar Lampung</text>
      <text x="40" y="58" font-family="sans-serif" font-size="11" fill="#94a3b8">Markas Komando Pusat: Jl. Kapten Piere Tendean No. 2, Durian Payung, Tj. Karang Pusat</text>
      <text x="40" y="76" font-family="sans-serif" font-size="11" fill="#94a3b8">Telepon: (0721) 252741 | Hotline Darurat: 113 / 112 (Bebas Pulsa)</text>
      <text x="40" y="94" font-family="sans-serif" font-size="11" fill="#94a3b8">Posko Siaga: Kedaton | Sukarame | Kemiling | Panjang | Teluk Betung | Tanjung Karang</text>
      
      <text x="{w - 400}" y="35" font-family="sans-serif" font-size="13" font-weight="bold" fill="#f8fafc">Prinsip Desain &amp; Aksesibilitas IMK</text>
      <text x="{w - 400}" y="56" font-family="sans-serif" font-size="11" fill="#cbd5e1">• Standar UCD ISO 9241-210:2019 &amp; Evaluasi WebQual 4.0</text>
      <text x="{w - 400}" y="74" font-family="sans-serif" font-size="11" fill="#cbd5e1">• Aksesibilitas WCAG 2.1 Level AA (Kontras Rasio &gt; 4,5:1)</text>
      <text x="{w - 400}" y="92" font-family="sans-serif" font-size="11" fill="#cbd5e1">• 10 Heuristik Jakob Nielsen &amp; Teori Kognitif Don Norman</text>

      <line x1="40" y1="120" x2="{w - 40}" y2="120" stroke="#334155" stroke-width="1" />
      <text x="40" y="145" font-family="sans-serif" font-size="11" fill="#64748b">© 2026 Redesain IMK Kelompok 8 (Alif Zakiansyah, Andrian Fajar, Valentina Lasma) - Politeknik Statistika STIS</text>
      <text x="{w - 40}" y="145" font-family="sans-serif" font-size="11" fill="#64748b" text-anchor="end">Live Deployment: damkar-bandarlampung-redesign-5wxa.vercel.app</text>
    </g>
    """

def placeholder_image(x, y, w, h, label="Placeholder Gambar"):
    clean_label = label.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""
    <g transform="translate({x}, {y})">
      <rect x="0" y="0" width="{w}" height="{h}" class="placeholder-box" />
      <line x1="0" y1="0" x2="{w}" y2="{h}" class="placeholder-line" />
      <line x1="0" y1="{h}" x2="{w}" y2="0" class="placeholder-line" />
      <rect x="{w//2 - 90}" y="{h//2 - 14}" width="180" height="28" fill="#f8fafc" rx="4" stroke="#cbd5e1" />
      <text x="{w//2}" y="{h//2 + 4}" class="placeholder-text">{clean_label}</text>
    </g>
    """


# ==============================================================================
# 1. WIREFRAME 01: BERANDA & FRAMEWORK GLOBAL DESKTOP (1200 x 1850)
# ==============================================================================
def generate_wireframe_01():
    w, h = 1200, 1820
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {STYLE_DEF}
  <rect width="{w}" height="{h}" class="bg-canvas" />

  {browser_chrome(w, "Beranda Damkar", "https://damkar.bandarlampungkota.go.id/")}
  {top_emergency_bar(w, 46)}
  {navbar(w, 80, "Beranda")}

  <!-- HERO SECTION -->
  <g transform="translate(40, 165)">
    <rect x="0" y="0" width="1120" height="300" class="hero-bg" rx="12" />
    
    <!-- Hero Badges -->
    <rect x="30" y="25" width="180" height="24" class="badge-red-bg" />
    <text x="120" y="41" class="badge-red-text" text-anchor="middle">🚨 KESIAPSIAGAAN 24/7</text>
    
    <rect x="220" y="25" width="220" height="24" class="badge-blue-bg" />
    <text x="330" y="41" class="badge-blue-text" text-anchor="middle">⏱️ SPM WAKTU TANGGAP &lt; 15 MENIT</text>

    <!-- Headline & Subhead -->
    <text x="30" y="85" class="heading-xl">Respon Cepat Tanggap Darurat Kebakaran &amp;</text>
    <text x="30" y="115" class="heading-xl">Penyelamatan Kota Bandar Lampung</text>
    <text x="30" y="150" class="text-body" fill="#334155">Pelayanan terpadu penanggulangan bencana kebakaran dan aksi penyelamatan (rescue) warga</text>
    <text x="30" y="170" class="text-body" fill="#334155">siaga penuh 24 jam bebas biaya di seluruh wilayah kecamatan Kota Bandar Lampung.</text>

    <!-- CTAs -->
    <rect x="30" y="205" width="230" height="48" class="btn-primary" />
    <text x="145" y="235" class="btn-primary-text">📞 HUBUNGI DARURAT 113</text>

    <rect x="275" y="205" width="220" height="48" class="btn-secondary" />
    <text x="385" y="235" class="btn-secondary-text">📝 Lapor Insiden Online</text>

    <!-- Hero Image Placeholder -->
    {placeholder_image(680, 25, 410, 250, "Foto Armada Damkarmat & Personil")}
  </g>

  <!-- EMERGENCY BROADCAST ALERT BANNER -->
  <g transform="translate(40, 485)">
    <rect x="0" y="0" width="1120" height="50" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.5" rx="8" />
    <text x="25" y="31" font-size="16">⚠️</text>
    <text x="55" y="31" font-family="sans-serif" font-size="12" font-weight="bold" fill="#92400e">[PERINGATAN DINI KEBENCANAAN]:</text>
    <text x="270" y="31" font-family="sans-serif" font-size="12" fill="#78350f">Waspada Potensi Kebakaran Lahan di Musim Kemarau. Segera hubungi 113 jika menemukan titik api.</text>
    <rect x="1000" y="12" width="95" height="26" fill="#fef3c7" stroke="#d97706" rx="4" />
    <text x="1047" y="29" font-family="sans-serif" font-size="11" font-weight="bold" fill="#92400e" text-anchor="middle">Baca Panduan</text>
  </g>

  <!-- QUICK ACCESS SERVICES SECTION (4 CARDS) -->
  <g transform="translate(40, 560)">
    <text x="0" y="20" class="heading-lg">Layanan Utama Kedaruratan &amp; Penyelamatan</text>
    <text x="0" y="38" class="text-sm">Akses cepat penanganan insiden darurat dan administrasi layanan proteksi kebakaran</text>

    <!-- Card 1: Pemadaman -->
    <rect x="0" y="55" width="265" height="180" class="card-bg" />
    <rect x="20" y="75" width="36" height="36" fill="#fee2e2" rx="6" />
    <text x="38" y="98" font-size="18" text-anchor="middle">🔥</text>
    <text x="20" y="135" class="heading-md">Pemadaman Kebakaran</text>
    <text x="20" y="155" class="text-sm">Penanganan kebakaran ruko,</text>
    <text x="20" y="170" class="text-sm">perumahan, gudang, &amp; lahan.</text>
    <rect x="20" y="188" width="130" height="28" fill="#dc2626" rx="4" />
    <text x="85" y="206" class="btn-primary-text" font-size="11">Panggil 113 &gt;</text>

    <!-- Card 2: Rescue -->
    <rect x="285" y="55" width="265" height="180" class="card-bg" />
    <rect x="305" y="75" width="36" height="36" fill="#e0f2fe" rx="6" />
    <text x="323" y="98" font-size="18" text-anchor="middle">🛡️</text>
    <text x="305" y="135" class="heading-md">Aksi Penyelamatan</text>
    <text x="305" y="155" class="text-sm">Evakuasi satwa liar (ular/tawon),</text>
    <text x="305" y="170" class="text-sm">pelepasan cincin, &amp; banjir.</text>
    <rect x="305" y="188" width="130" height="28" fill="#0284c7" rx="4" />
    <text x="370" y="206" class="btn-primary-text" font-size="11">Lapor Rescue &gt;</text>

    <!-- Card 3: Posko Siaga -->
    <rect x="570" y="55" width="265" height="180" class="card-bg" />
    <rect x="590" y="75" width="36" height="36" fill="#fef3c7" rx="6" />
    <text x="608" y="98" font-size="18" text-anchor="middle">📍</text>
    <text x="590" y="135" class="heading-md">Posko Siaga Kecamatan</text>
    <text x="590" y="155" class="text-sm">Direktori 6 posko siaga terdekat</text>
    <text x="590" y="170" class="text-sm">dengan respon langsung &lt;15 mnt.</text>
    <rect x="590" y="188" width="130" height="28" fill="#d97706" rx="4" />
    <text x="655" y="206" class="btn-primary-text" font-size="11">Lihat Posko &gt;</text>

    <!-- Card 4: Dokumen & SOP -->
    <rect x="855" y="55" width="265" height="180" class="card-bg" />
    <rect x="875" y="75" width="36" height="36" fill="#f1f5f9" rx="6" />
    <text x="893" y="98" font-size="18" text-anchor="middle">📄</text>
    <text x="875" y="135" class="heading-md">Dokumen &amp; SOP Publik</text>
    <text x="875" y="155" class="text-sm">Unduh SOP proteksi kebakaran,</text>
    <text x="875" y="170" class="text-sm">LKJIP 2024, regulasi, &amp; formulir.</text>
    <rect x="875" y="188" width="130" height="28" fill="#475569" rx="4" />
    <text x="940" y="206" class="btn-primary-text" font-size="11">Unduh SOP &gt;</text>
  </g>

  <!-- OPERATIONAL STATISTICS DASHBOARD -->
  <g transform="translate(40, 825)">
    <text x="0" y="20" class="heading-lg">Transparansi Kinerja &amp; Statistik Operasional</text>
    <text x="0" y="38" class="text-sm">Data riil volume penanganan bencana dan pemenuhan Standar Pelayanan Minimal (SPM)</text>

    <!-- Stat 1 -->
    <rect x="0" y="55" width="265" height="110" class="card-bg" />
    <text x="25" y="98" font-family="sans-serif" font-size="32" font-weight="800" fill="#dc2626">271</text>
    <text x="25" y="122" class="heading-md" font-size="13">Insiden Kebakaran</text>
    <text x="25" y="142" class="text-sm">Total kejadian tertangani 2024</text>

    <!-- Stat 2 -->
    <rect x="285" y="55" width="265" height="110" class="card-bg" />
    <text x="310" y="98" font-family="sans-serif" font-size="32" font-weight="800" fill="#0284c7">518</text>
    <text x="310" y="122" class="heading-md" font-size="13">Aksi Penyelamatan</text>
    <text x="310" y="142" class="text-sm">Rescue non-kebakaran (Jan-Jul 2025)</text>

    <!-- Stat 3 -->
    <rect x="570" y="55" width="265" height="110" class="card-bg" />
    <text x="595" y="98" font-family="sans-serif" font-size="32" font-weight="800" fill="#059669">18</text>
    <text x="595" y="122" class="heading-md" font-size="13">Armada Mobil Siaga</text>
    <text x="595" y="142" class="text-sm">Unit pancar, tangki, &amp; rescue aktif</text>

    <!-- Stat 4 -->
    <rect x="855" y="55" width="265" height="110" class="card-bg" />
    <text x="880" y="98" font-family="sans-serif" font-size="32" font-weight="800" fill="#7c3aed">&lt; 15 mnt</text>
    <text x="880" y="122" class="heading-md" font-size="13">Waktu Tanggap SPM</text>
    <text x="880" y="142" class="text-sm">Standar Permendagri No. 114/2018</text>
  </g>

  <!-- KECAMATAN STATIONS DIRECTORY (3x2 GRID) -->
  <g transform="translate(40, 1025)">
    <text x="0" y="20" class="heading-lg">Direktori 6 Posko Siaga Kecamatan se-Bandar Lampung</text>
    <text x="0" y="38" class="text-sm">Penyebaran posko siaga untuk menjamin waktu respon di bawah 15 menit ke lokasi warga</text>

    <!-- Posko 1 -->
    <rect x="0" y="55" width="360" height="95" class="card-bg" />
    <text x="20" y="80" class="heading-md">Mako Pusat (Tanjung Karang Pusat)</text>
    <text x="20" y="100" class="text-sm">Jl. Kapten Piere Tendean No. 2 | Telp: (0721) 252741</text>
    <rect x="20" y="112" width="105" height="24" fill="#dc2626" rx="4" />
    <text x="72" y="128" class="btn-primary-text" font-size="10">Hubungi Mako</text>

    <!-- Posko 2 -->
    <rect x="380" y="55" width="360" height="95" class="card-bg" />
    <text x="400" y="80" class="heading-md">Posko Wilayah Kedaton</text>
    <text x="400" y="100" class="text-sm">Jl. Teuku Umar No. 88 | Telp: (0721) 701113</text>
    <rect x="400" y="112" width="105" height="24" fill="#1e3a8a" rx="4" />
    <text x="452" y="128" class="btn-primary-text" font-size="10">Hubungi Posko</text>

    <!-- Posko 3 -->
    <rect x="760" y="55" width="360" height="95" class="card-bg" />
    <text x="780" y="80" class="heading-md">Posko Wilayah Sukarame</text>
    <text x="780" y="100" class="text-sm">Jl. Endro Suratmin | Telp: (0721) 782113</text>
    <rect x="780" y="112" width="105" height="24" fill="#1e3a8a" rx="4" />
    <text x="832" y="128" class="btn-primary-text" font-size="10">Hubungi Posko</text>

    <!-- Posko 4 -->
    <rect x="0" y="165" width="360" height="95" class="card-bg" />
    <text x="20" y="190" class="heading-md">Posko Wilayah Kemiling</text>
    <text x="20" y="210" class="text-sm">Jl. Imam Bonjol | Telp: (0721) 271113</text>
    <rect x="20" y="222" width="105" height="24" fill="#1e3a8a" rx="4" />
    <text x="72" y="238" class="btn-primary-text" font-size="10">Hubungi Posko</text>

    <!-- Posko 5 -->
    <rect x="380" y="165" width="360" height="95" class="card-bg" />
    <text x="400" y="190" class="heading-md">Posko Wilayah Panjang</text>
    <text x="400" y="210" class="text-sm">Jl. Yos Sudarso No. 12 | Telp: (0721) 31113</text>
    <rect x="400" y="222" width="105" height="24" fill="#1e3a8a" rx="4" />
    <text x="452" y="238" class="btn-primary-text" font-size="10">Hubungi Posko</text>

    <!-- Posko 6 -->
    <rect x="760" y="165" width="360" height="95" class="card-bg" />
    <text x="780" y="190" class="heading-md">Posko Wilayah Teluk Betung</text>
    <text x="780" y="210" class="text-sm">Jl. Basuki Rahmat No. 4 | Telp: (0721) 481113</text>
    <rect x="780" y="222" width="105" height="24" fill="#1e3a8a" rx="4" />
    <text x="832" y="238" class="btn-primary-text" font-size="10">Hubungi Posko</text>
  </g>

  <!-- BERITA TERKINI & EDUKASI -->
  <g transform="translate(40, 1335)">
    <text x="0" y="20" class="heading-lg">Berita Operasi Pemadaman &amp; Edukasi Terkini</text>
    <text x="{1120}" y="20" class="nav-link-active" text-anchor="end">Lihat Seluruh Berita &gt;</text>

    <!-- News 1 -->
    <rect x="0" y="45" width="360" height="240" class="card-bg" />
    {placeholder_image(0, 45, 360, 130, "Foto: Operasi Kebakaran")}
    <rect x="15" y="185" width="110" height="20" class="badge-red-bg" />
    <text x="70" y="199" class="badge-red-text" text-anchor="middle">PEMADAMAN</text>
    <text x="15" y="225" class="heading-md" font-size="13">Kebakaran Gudang di Kedaton Berhasil Padam</text>
    <text x="15" y="245" class="text-sm">15 Sep 2025 • Waktu tanggap 11 menit</text>

    <!-- News 2 -->
    <rect x="380" y="45" width="360" height="240" class="card-bg" />
    {placeholder_image(380, 45, 360, 130, "Foto: Evakuasi Satwa")}
    <rect x="395" y="185" width="110" height="20" class="badge-blue-bg" />
    <text x="450" y="199" class="badge-blue-text" text-anchor="middle">ANIMAL RESCUE</text>
    <text x="395" y="225" class="heading-md" font-size="13">Tim Rescue Evakuasi Ular Sanca di Sukarame</text>
    <text x="395" y="245" class="text-sm">12 Sep 2025 • Evakuasi aman tanpa korban</text>

    <!-- News 3 -->
    <rect x="760" y="45" width="360" height="240" class="card-bg" />
    {placeholder_image(760, 45, 360, 130, "Foto: Edukasi Sekolah")}
    <rect x="775" y="185" width="110" height="20" class="badge-bg" />
    <text x="830" y="199" class="badge-text" text-anchor="middle">SOSIALISASI</text>
    <text x="775" y="225" class="heading-md" font-size="13">Simulasi Mitigasi Kebakaran Siswa Sekolah</text>
    <text x="775" y="245" class="text-sm">08 Sep 2025 • Edukasi APAR sejak dini</text>
  </g>

  {footer(w, 1650)}
  {sticky_emergency_button(980, 1530)}
</svg>"""
    return svg


# ==============================================================================
# 2. WIREFRAME 02: MODUL BERITA & CATATAN OPERASIONAL DESKTOP (1200 x 1450)
# ==============================================================================
def generate_wireframe_02():
    w, h = 1200, 1450
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {STYLE_DEF}
  <rect width="{w}" height="{h}" class="bg-canvas" />

  {browser_chrome(w, "Berita & Operasi Damkar", "https://damkar.bandarlampungkota.go.id/berita")}
  {top_emergency_bar(w, 46)}
  {navbar(w, 80, "Berita")}

  <!-- BREADCRUMBS & HEADER -->
  <g transform="translate(40, 165)">
    <text x="0" y="15" class="text-sm">Beranda  /  <tspan fill="#1e40af" font-weight="bold">Berita &amp; Informasi Operasional</tspan></text>
    <text x="0" y="50" class="heading-xl">Warta Kebencanaan &amp; Catatan Operasi Lapangan</text>
    <text x="0" y="72" class="text-body">Dokumentasi transparan penanganan kebakaran, aksi penyelamatan, dan panduan mitigasi warga.</text>
  </g>

  <!-- SEARCH & FILTER TOOLBAR -->
  <g transform="translate(40, 260)">
    <rect x="0" y="0" width="1120" height="60" class="card-bg" />
    
    <!-- Instant Search Input -->
    <rect x="20" y="12" width="380" height="36" fill="#f8fafc" stroke="#cbd5e1" rx="6" />
    <text x="35" y="35" class="text-body" fill="#94a3b8">🔍 Cari judul, lokasi, atau kata kunci... (&lt;100ms)</text>

    <!-- Pill Category Buttons -->
    <rect x="420" y="14" width="115" height="32" fill="#1e40af" rx="16" />
    <text x="477" y="34" class="btn-primary-text" font-size="11">Semua (48)</text>

    <rect x="545" y="14" width="145" height="32" fill="#f1f5f9" stroke="#cbd5e1" rx="16" />
    <text x="617" y="34" class="nav-link" font-size="11" text-anchor="middle">Pemadaman (22)</text>

    <rect x="700" y="14" width="135" height="32" fill="#f1f5f9" stroke="#cbd5e1" rx="16" />
    <text x="767" y="34" class="nav-link" font-size="11" text-anchor="middle">Aksi Rescue (16)</text>

    <rect x="845" y="14" width="135" height="32" fill="#f1f5f9" stroke="#cbd5e1" rx="16" />
    <text x="912" y="34" class="nav-link" font-size="11" text-anchor="middle">Sosialisasi (7)</text>

    <rect x="990" y="14" width="110" height="32" fill="#f1f5f9" stroke="#cbd5e1" rx="16" />
    <text x="1045" y="34" class="nav-link" font-size="11" text-anchor="middle">Peringatan (3)</text>
  </g>

  <!-- FEATURED ARTICLE CARD (HEADLINE) -->
  <g transform="translate(40, 345)">
    <rect x="0" y="0" width="1120" height="210" class="card-bg" />
    {placeholder_image(0, 0, 420, 210, "Foto Utama Headline")}

    <g transform="translate(450, 25)">
      <rect x="0" y="0" width="135" height="22" class="badge-red-bg" />
      <text x="67" y="15" class="badge-red-text" text-anchor="middle">OPERASI PEMADAMAN</text>
      <text x="150" y="15" class="text-sm">18 September 2025 • Durasi Respon 12 Menit</text>

      <text x="0" y="50" class="heading-lg">Damkar Bandar Lampung Jinakkan Kebakaran Gudang di Kedaton</text>
      <text x="0" y="80" class="text-body">Sebanyak 6 unit mobil pemadam dan 35 personel dikerahkan ke lokasi kebakaran gudang logistik.</text>
      <text x="0" y="100" class="text-body">Tidak ada korban jiwa berkat kesigapan warga menghubungi 113 dan respon posko &lt; 15 menit.</text>

      <rect x="0" y="130" width="160" height="34" class="btn-navy" />
      <text x="80" y="152" class="btn-navy-text">Baca Selengkapnya &gt;</text>
    </g>
  </g>

  <!-- NEWS GRID (3 x 2) -->
  <g transform="translate(40, 580)">
    <!-- Card 1 -->
    <rect x="0" y="0" width="360" height="290" class="card-bg" />
    {placeholder_image(0, 0, 360, 140, "Foto: Rescue Ular")}
    <rect x="15" y="155" width="110" height="20" class="badge-blue-bg" />
    <text x="70" y="169" class="badge-blue-text" text-anchor="middle">ANIMAL RESCUE</text>
    <text x="15" y="195" class="heading-md" font-size="13">Evakuasi Ular Sanca 3 Meter di Pemukiman Kemiling</text>
    <text x="15" y="215" class="text-sm">Warga melaporkan keberadaan ular di atas plafon rumah...</text>
    <text x="15" y="245" class="text-sm" fill="#94a3b8">14 Sep 2025 • Petugas Posko Kemiling</text>
    <text x="15" y="270" class="nav-link-active" font-size="11">Baca rincian &gt;</text>

    <!-- Card 2 -->
    <rect x="380" y="0" width="360" height="290" class="card-bg" />
    {placeholder_image(380, 0, 360, 140, "Foto: Pelepasan Cincin")}
    <rect x="395" y="155" width="110" height="20" class="badge-blue-bg" />
    <text x="450" y="169" class="badge-blue-text" text-anchor="middle">RESCUE NON-API</text>
    <text x="395" y="195" class="heading-md" font-size="13">Aksi Cepat Damkar Lepaskan Cincin Macet di Jari</text>
    <text x="395" y="215" class="text-sm">Petugas menggunakan alat pemotong mini dengan presisi...</text>
    <text x="395" y="245" class="text-sm" fill="#94a3b8">10 Sep 2025 • Mako Pusat Durian Payung</text>
    <text x="395" y="270" class="nav-link-active" font-size="11">Baca rincian &gt;</text>

    <!-- Card 3 -->
    <rect x="760" y="0" width="360" height="290" class="card-bg" />
    {placeholder_image(760, 0, 360, 140, "Foto: Edukasi TK/SD")}
    <rect x="775" y="155" width="110" height="20" class="badge-bg" />
    <text x="830" y="169" class="badge-text" text-anchor="middle">SOSIALISASI</text>
    <text x="775" y="195" class="heading-md" font-size="13">Pelatihan Proteksi Dini bagi Siswa SD se-Kecamatan</text>
    <text x="775" y="215" class="text-sm">Pengenalan APAR dan tata cara penyelamatan diri saat darurat...</text>
    <text x="775" y="245" class="text-sm" fill="#94a3b8">05 Sep 2025 • Posko Sukarame</text>
    <text x="775" y="270" class="nav-link-active" font-size="11">Baca rincian &gt;</text>

    <!-- Card 4 -->
    <rect x="0" y="310" width="360" height="290" class="card-bg" />
    {placeholder_image(0, 310, 360, 140, "Foto: Inspeksi Hidran")}
    <rect x="15" y="465" width="110" height="20" class="badge-bg" />
    <text x="70" y="479" class="badge-text" text-anchor="middle">INSPEKSI</text>
    <text x="15" y="505" class="heading-md" font-size="13">Pengecekan Kelaikan Hidran Kota di Kawasan Bisnis</text>
    <text x="15" y="525" class="text-sm">Memastikan suplai debit air hidran aktif untuk proteksi gedung...</text>
    <text x="15" y="555" class="text-sm" fill="#94a3b8">28 Agu 2025 • Bidang Pencegahan Damkar</text>
    <text x="15" y="580" class="nav-link-active" font-size="11">Baca rincian &gt;</text>

    <!-- Card 5 -->
    <rect x="380" y="310" width="360" height="290" class="card-bg" />
    {placeholder_image(380, 310, 360, 140, "Foto: Cuaca Panas")}
    <rect x="395" y="465" width="110" height="20" class="badge-red-bg" />
    <text x="450" y="479" class="badge-red-text" text-anchor="middle">PERINGATAN</text>
    <text x="395" y="505" class="heading-md" font-size="13">Himbauan Pencegahan Pembakaran Sampah Terbuka</text>
    <text x="395" y="525" class="text-sm">Potensi penjalaran api tinggi pada musim kemarau berangin...</text>
    <text x="395" y="555" class="text-sm" fill="#94a3b8">20 Agu 2025 • Siaga Komando</text>
    <text x="395" y="580" class="nav-link-active" font-size="11">Baca rincian &gt;</text>

    <!-- Card 6 -->
    <rect x="760" y="310" width="360" height="290" class="card-bg" />
    {placeholder_image(760, 310, 360, 140, "Foto: Simulasi Hotel")}
    <rect x="775" y="465" width="110" height="20" class="badge-bg" />
    <text x="830" y="479" class="badge-text" text-anchor="middle">SIMULASI</text>
    <text x="775" y="505" class="heading-md" font-size="13">Uji Evakuasi Tanggap Bencana Hotel Bertingkat</text>
    <text x="775" y="525" class="text-sm">Pengujian alarm smoke detector dan rute tangga darurat...</text>
    <text x="775" y="555" class="text-sm" fill="#94a3b8">15 Agu 2025 • Tim Proteksi Damkar</text>
    <text x="775" y="580" class="nav-link-active" font-size="11">Baca rincian &gt;</text>
  </g>

  <!-- PAGINATION CONTROLS -->
  <g transform="translate(460, 1205)">
    <rect x="0" y="0" width="40" height="34" fill="#ffffff" stroke="#cbd5e1" rx="4" />
    <text x="20" y="22" class="table-hdr-text" text-anchor="middle">&lt;</text>
    
    <rect x="50" y="0" width="36" height="34" fill="#1e40af" rx="4" />
    <text x="68" y="22" class="btn-primary-text" font-size="12">1</text>
    
    <rect x="96" y="0" width="36" height="34" fill="#ffffff" stroke="#cbd5e1" rx="4" />
    <text x="114" y="22" class="table-hdr-text" text-anchor="middle">2</text>
    
    <rect x="142" y="0" width="36" height="34" fill="#ffffff" stroke="#cbd5e1" rx="4" />
    <text x="160" y="22" class="table-hdr-text" text-anchor="middle">3</text>

    <text x="195" y="22" class="table-hdr-text" text-anchor="middle">...</text>

    <rect x="220" y="0" width="36" height="34" fill="#ffffff" stroke="#cbd5e1" rx="4" />
    <text x="238" y="22" class="table-hdr-text" text-anchor="middle">8</text>

    <rect x="266" y="0" width="40" height="34" fill="#ffffff" stroke="#cbd5e1" rx="4" />
    <text x="286" y="22" class="table-hdr-text" text-anchor="middle">&gt;</text>
  </g>

  {footer(w, 1280)}
  {sticky_emergency_button(980, 1160)}
</svg>"""
    return svg


# ==============================================================================
# 3. WIREFRAME 03: MODUL DOKUMEN & REGULASI DESKTOP (1200 x 1400)
# ==============================================================================
def generate_wireframe_03():
    w, h = 1200, 1380
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {STYLE_DEF}
  <rect width="{w}" height="{h}" class="bg-canvas" />

  {browser_chrome(w, "Dokumen & SOP Damkar", "https://damkar.bandarlampungkota.go.id/dokumen")}
  {top_emergency_bar(w, 46)}
  {navbar(w, 80, "Dokumen")}

  <!-- BREADCRUMBS & HEADER -->
  <g transform="translate(40, 165)">
    <text x="0" y="15" class="text-sm">Beranda  /  <tspan fill="#1e40af" font-weight="bold">Dokumen Kedinasan &amp; SOP Publik</tspan></text>
    <text x="0" y="50" class="heading-xl">Dokumen Publik, SOP, dan Regulasi Penyelamatan</text>
    <text x="0" y="72" class="text-body">Akses transparan standar operasional prosedur, laporan akuntabilitas, dan berkas perizinan.</text>
  </g>

  <!-- FILTER & SEARCH BAR -->
  <g transform="translate(40, 260)">
    <rect x="0" y="0" width="1120" height="60" class="card-bg" />
    
    <rect x="20" y="12" width="480" height="36" fill="#f8fafc" stroke="#cbd5e1" rx="6" />
    <text x="35" y="35" class="text-body" fill="#94a3b8">🔍 Cari nama dokumen (misal: LKJIP, SOP Gedung, Renstra)...</text>

    <!-- Dropdown Mock -->
    <rect x="520" y="12" width="260" height="36" fill="#ffffff" stroke="#cbd5e1" rx="6" />
    <text x="535" y="35" class="text-body">Semua Kategori Dokumen</text>
    <text x="755" y="35" class="text-body">▼</text>

    <!-- Total badge -->
    <text x="1090" y="35" class="text-sm" text-anchor="end">Menampilkan 5 dari 24 Dokumen</text>
  </g>

  <!-- INTERACTIVE DOCUMENT TABLE -->
  <g transform="translate(40, 345)">
    <!-- Table Header -->
    <rect x="0" y="0" width="1120" height="42" class="table-hdr" />
    <text x="20" y="26" class="table-hdr-text">NAMA DOKUMEN &amp; DESKRIPSI LENGKAP</text>
    <text x="560" y="26" class="table-hdr-text">KATEGORI</text>
    <text x="730" y="26" class="table-hdr-text">FORMAT / UKURAN</text>
    <text x="890" y="26" class="table-hdr-text">TANGGAL TERBIT</text>
    <text x="1050" y="26" class="table-hdr-text" text-anchor="middle">AKSI</text>

    <!-- Row 1 -->
    <rect x="0" y="42" width="1120" height="80" class="table-cell" />
    <text x="20" y="70" class="heading-md" font-size="13">SOP Penanggulangan Kebakaran Gedung Bertingkat</text>
    <text x="20" y="92" class="text-sm">Panduan teknis pencegahan, evakuasi, dan pemadaman bagi pengelola gedung perkantoran &amp; usaha.</text>
    <rect x="560" y="65" width="120" height="22" class="badge-red-bg" />
    <text x="620" y="80" class="badge-red-text" text-anchor="middle">SOP Kedaruratan</text>
    <text x="730" y="82" class="table-cell-text">📄 PDF (2,4 MB)</text>
    <text x="890" y="82" class="table-cell-text">12 Jan 2025</text>
    <rect x="1000" y="62" width="100" height="34" class="btn-navy" />
    <text x="1050" y="83" class="btn-navy-text" font-size="11">Unduh PDF</text>

    <!-- Row 2 -->
    <rect x="0" y="122" width="1120" height="80" class="table-cell" fill="#f8fafc" />
    <text x="20" y="150" class="heading-md" font-size="13">Laporan Kinerja Instansi Pemerintah (LKJIP) Tahun 2024</text>
    <text x="20" y="172" class="text-sm">Laporan akuntabilitas tahunan capaian operasional, anggaran, dan pemenuhan SPM waktu tanggap.</text>
    <rect x="560" y="145" width="120" height="22" class="badge-blue-bg" />
    <text x="620" y="160" class="badge-blue-text" text-anchor="middle">Akuntabilitas</text>
    <text x="730" y="162" class="table-cell-text">📄 PDF (4,1 MB)</text>
    <text x="890" y="162" class="table-cell-text">28 Feb 2025</text>
    <rect x="1000" y="142" width="100" height="34" class="btn-navy" />
    <text x="1050" y="163" class="btn-navy-text" font-size="11">Unduh PDF</text>

    <!-- Row 3 -->
    <rect x="0" y="202" width="1120" height="80" class="table-cell" />
    <text x="20" y="230" class="heading-md" font-size="13">SOP Permohonan Evakuasi Satwa Liar (Ular &amp; Tawon Vespa)</text>
    <text x="20" y="252" class="text-sm">Tata cara masyarakat melaporkan ancaman fauna berbahaya ke markas rescue tanpa dipungut biaya.</text>
    <rect x="560" y="225" width="120" height="22" class="badge-blue-bg" />
    <text x="620" y="240" class="badge-blue-text" text-anchor="middle">Layanan Rescue</text>
    <text x="730" y="242" class="table-cell-text">📄 PDF (1,8 MB)</text>
    <text x="890" y="242" class="table-cell-text">05 Mei 2024</text>
    <rect x="1000" y="222" width="100" height="34" class="btn-navy" />
    <text x="1050" y="243" class="btn-navy-text" font-size="11">Unduh PDF</text>

    <!-- Row 4 -->
    <rect x="0" y="282" width="1120" height="80" class="table-cell" fill="#f8fafc" />
    <text x="20" y="310" class="heading-md" font-size="13">Perda No. 03 Tahun 2021 tentang Sistem Proteksi Kebakaran</text>
    <text x="20" y="332" class="text-sm">Dasar hukum regulasi kewajiban ketersediaan APAR, hidran, pipa air, dan izin kelayakan proteksi gedung.</text>
    <rect x="560" y="305" width="120" height="22" class="badge-bg" />
    <text x="620" y="320" class="badge-text" text-anchor="middle">Regulasi Daerah</text>
    <text x="730" y="322" class="table-cell-text">📄 PDF (3,5 MB)</text>
    <text x="890" y="322" class="table-cell-text">14 Nov 2021</text>
    <rect x="1000" y="302" width="100" height="34" class="btn-navy" />
    <text x="1050" y="323" class="btn-navy-text" font-size="11">Unduh PDF</text>

    <!-- Row 5 -->
    <rect x="0" y="362" width="1120" height="80" class="table-cell" />
    <text x="20" y="390" class="heading-md" font-size="13">Formulir Permohonan Simulasi Mitigasi Kebakaran Lembaga / Sekolah</text>
    <text x="20" y="412" class="text-sm">Blangko pengajuan resmi pelatihan penanggulangan bencana kebakaran gratis bagi lembaga pendidikan.</text>
    <rect x="560" y="385" width="120" height="22" class="badge-bg" />
    <text x="620" y="400" class="badge-text" text-anchor="middle">Formulir Publik</text>
    <text x="730" y="402" class="table-cell-text">📄 PDF (820 KB)</text>
    <text x="890" y="402" class="table-cell-text">10 Agu 2024</text>
    <rect x="1000" y="382" width="100" height="34" class="btn-navy" />
    <text x="1050" y="403" class="btn-navy-text" font-size="11">Unduh PDF</text>
  </g>

  <!-- TOAST FEEDBACK NOTIFICATION SIMULATION -->
  <g transform="translate(40, 810)">
    <rect x="0" y="0" width="550" height="48" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5" rx="8" />
    <text x="20" y="30" font-size="18">✅</text>
    <text x="50" y="30" font-family="sans-serif" font-size="12" font-weight="bold" fill="#065f46">Umpan Balik Sistem (Feedback):</text>
    <text x="235" y="30" font-family="sans-serif" font-size="12" fill="#047857">Berkas "SOP Penanggulangan Kebakaran Gedung" berhasil diunduh (2,4 MB).</text>

    <!-- Callout Box -->
    <rect x="570" y="10" width="220" height="26" class="annotation-box" />
    <text x="680" y="27" class="annotation-text" text-anchor="middle">HCI: Nielsen H1 System Status Visibility</text>
  </g>

  <!-- PUBLIC REQUEST INFORMATION BOX -->
  <g transform="translate(40, 885)">
    <rect x="0" y="0" width="1120" height="120" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1" rx="8" />
    <text x="30" y="40" class="heading-lg">Tidak Menemukan Dokumen yang Anda Cari?</text>
    <text x="30" y="65" class="text-body">Ajukan permohonan informasi publik secara daring atau hubungi bagian Pejabat Pengelola Informasi (PPID) Damkar.</text>
    <text x="30" y="85" class="text-sm">Layanan pemenuhan permohonan dokumen diproses maksimal 3 hari kerja sesuai UU KIP.</text>

    <rect x="880" y="38" width="210" height="42" class="btn-secondary" />
    <text x="985" y="64" class="btn-secondary-text">Ajukan Permohonan &gt;</text>
  </g>

  {footer(w, 1050)}
  {sticky_emergency_button(980, 930)}
</svg>"""
    return svg


# ==============================================================================
# 4. WIREFRAME 04: MODUL GALERI EDUKASI & PENYELAMATAN DESKTOP (1200 x 1350)
# ==============================================================================
def generate_wireframe_04():
    w, h = 1200, 1380
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {STYLE_DEF}
  <rect width="{w}" height="{h}" class="bg-canvas" />

  {browser_chrome(w, "Galeri Edukasi Damkar", "https://damkar.bandarlampungkota.go.id/galeri")}
  {top_emergency_bar(w, 46)}
  {navbar(w, 80, "Galeri")}

  <!-- BREADCRUMBS & HEADER -->
  <g transform="translate(40, 165)">
    <text x="0" y="15" class="text-sm">Beranda  /  <tspan fill="#1e40af" font-weight="bold">Galeri Dokumentasi &amp; Edukasi</tspan></text>
    <text x="0" y="50" class="heading-xl">Galeri Operasi Penyelamatan &amp; Edukasi Mitigasi</text>
    <text x="0" y="72" class="text-body">Rekaman visual perjuangan petugas pemadam kebakaran dan aksi rescue penyelamatan masyarakat se-Bandar Lampung.</text>
  </g>

  <!-- FILTER TABS -->
  <g transform="translate(40, 260)">
    <rect x="0" y="0" width="1120" height="52" class="card-bg" />
    
    <rect x="15" y="10" width="140" height="32" fill="#1e40af" rx="16" />
    <text x="85" y="30" class="btn-primary-text" font-size="11">Semua Media (36)</text>

    <rect x="165" y="10" width="165" height="32" fill="#f1f5f9" stroke="#cbd5e1" rx="16" />
    <text x="247" y="30" class="nav-link" font-size="11" text-anchor="middle">Operasi Kebakaran (15)</text>

    <rect x="340" y="10" width="155" height="32" fill="#f1f5f9" stroke="#cbd5e1" rx="16" />
    <text x="417" y="30" class="nav-link" font-size="11" text-anchor="middle">Aksi Rescue (12)</text>

    <rect x="505" y="10" width="165" height="32" fill="#f1f5f9" stroke="#cbd5e1" rx="16" />
    <text x="587" y="30" class="nav-link" font-size="11" text-anchor="middle">Simulasi Sekolah (6)</text>

    <rect x="680" y="10" width="140" height="32" fill="#f1f5f9" stroke="#cbd5e1" rx="16" />
    <text x="750" y="30" class="nav-link" font-size="11" text-anchor="middle">Video Edukasi (3)</text>
  </g>

  <!-- 3x2 GALLERY GRID -->
  <g transform="translate(40, 335)">
    <!-- Photo 1 -->
    <rect x="0" y="0" width="360" height="270" class="card-bg" />
    {placeholder_image(0, 0, 360, 190, "Foto: Pemadaman Sukarame")}
    <rect x="15" y="200" width="85" height="20" class="badge-red-bg" />
    <text x="57" y="214" class="badge-red-text" text-anchor="middle">PEMADAMAN</text>
    <text x="15" y="238" class="heading-md" font-size="13">Pemadaman Lahan Kering Sukarame</text>
    <text x="15" y="255" class="text-sm">18 Sep 2025 • Durasi Operasi 45 Menit</text>

    <!-- Photo 2 -->
    <rect x="380" y="0" width="360" height="270" class="card-bg" />
    {placeholder_image(380, 0, 360, 190, "Foto: Rescue Sumur")}
    <rect x="395" y="200" width="105" height="20" class="badge-blue-bg" />
    <text x="447" y="214" class="badge-blue-text" text-anchor="middle">ANIMAL RESCUE</text>
    <text x="395" y="238" class="heading-md" font-size="13">Penyelamatan Kucing di Sumur 12 Meter</text>
    <text x="395" y="255" class="text-sm">14 Sep 2025 • Lokasi Teluk Betung</text>

    <!-- Photo 3 -->
    <rect x="760" y="0" width="360" height="270" class="card-bg" />
    {placeholder_image(760, 0, 360, 190, "Foto: Pelepasan Cincin")}
    <rect x="775" y="200" width="105" height="20" class="badge-blue-bg" />
    <text x="827" y="214" class="badge-blue-text" text-anchor="middle">MEDIS RESCUE</text>
    <text x="775" y="238" class="heading-md" font-size="13">Pelepasan Cincin Macet di Jari Lansia</text>
    <text x="775" y="255" class="text-sm">10 Sep 2025 • Mako Pusat Durian Payung</text>

    <!-- Photo 4 -->
    <rect x="0" y="295" width="360" height="270" class="card-bg" />
    {placeholder_image(0, 295, 360, 190, "Foto: Edukasi APAR TK")}
    <rect x="15" y="495" width="85" height="20" class="badge-bg" />
    <text x="57" y="509" class="badge-text" text-anchor="middle">SOSIALISASI</text>
    <text x="15" y="533" class="heading-md" font-size="13">Pengenalan Bahaya Api Siswa SD/TK</text>
    <text x="15" y="550" class="text-sm">02 Sep 2025 • Posko Kedaton</text>

    <!-- Photo 5 -->
    <rect x="380" y="295" width="360" height="270" class="card-bg" />
    {placeholder_image(380, 295, 360, 190, "Foto: Pengecekan Hidran")}
    <rect x="395" y="495" width="85" height="20" class="badge-bg" />
    <text x="437" y="509" class="badge-text" text-anchor="middle">INSPEKSI</text>
    <text x="395" y="533" class="heading-md" font-size="13">Uji Tekanan Hidran Pasar Bambu Kuning</text>
    <text x="395" y="550" class="text-sm">25 Agu 2025 • Tanjung Karang Pusat</text>

    <!-- Photo 6 (Video Mock) -->
    <rect x="760" y="295" width="360" height="270" class="card-bg" />
    {placeholder_image(760, 295, 360, 190, "Video: Tutorial APAR (▶ 03:45)")}
    <rect x="775" y="495" width="105" height="20" class="badge-red-bg" />
    <text x="827" y="509" class="badge-red-text" text-anchor="middle">VIDEO EDUKASI</text>
    <text x="775" y="533" class="heading-md" font-size="13">Langkah Padamkan Api Tabung Gas LPG</text>
    <text x="775" y="550" class="text-sm">18 Agu 2025 • Durasi 3 Menit 45 Detik</text>
  </g>

  <!-- LIGHTBOX MODAL PREVIEW MOCKUP CALLOUT -->
  <g transform="translate(40, 930)">
    <rect x="0" y="0" width="1120" height="110" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="6 4" rx="8" />
    <text x="25" y="35" class="heading-md">Fitur Interaksi Lightbox Preview (Direct Manipulation):</text>
    <text x="25" y="60" class="text-body">Setiap kartu foto/video dapat diklik untuk membuka pratinjau resolusi tinggi layar penuh (*modal lightbox*)</text>
    <text x="25" y="80" class="text-body">lengkap dengan informasi lokasi, tanggal insiden, nama posko penanggung jawab, serta tombol unduh dokumentasi.</text>

    <rect x="880" y="32" width="210" height="42" class="btn-navy" />
    <text x="985" y="58" class="btn-navy-text">Simulasikan Lightbox &gt;</text>
  </g>

  {footer(w, 1080)}
  {sticky_emergency_button(980, 960)}
</svg>"""
    return svg


# ==============================================================================
# 5. WIREFRAME 05: MODUL KONTAK & PENGADUAN CEPAT DESKTOP (1200 x 1450)
# ==============================================================================
def generate_wireframe_05():
    w, h = 1200, 1480
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {STYLE_DEF}
  <rect width="{w}" height="{h}" class="bg-canvas" />

  {browser_chrome(w, "Kontak & Posko Damkar", "https://damkar.bandarlampungkota.go.id/kontak")}
  {top_emergency_bar(w, 46)}
  {navbar(w, 80, "Kontak")}

  <!-- BREADCRUMBS & HEADER -->
  <g transform="translate(40, 165)">
    <text x="0" y="15" class="text-sm">Beranda  /  <tspan fill="#1e40af" font-weight="bold">Kontak Markas &amp; Pengaduan Cepat</tspan></text>
    <text x="0" y="50" class="heading-xl">Kontak Posko Siaga &amp; Formulir Laporan Kejadian</text>
    <text x="0" y="72" class="text-body">Hubungi saluran darurat 24 jam bebas biaya atau laporkan insiden melalui formulir dengan validasi langsung.</text>
  </g>

  <!-- TWO-COLUMN ARCHITECTURE -->
  <g transform="translate(40, 260)">
    
    <!-- LEFT COLUMN: DIREKTORI POSKO (w=480) -->
    <g transform="translate(0, 0)">
      <text x="0" y="20" class="heading-lg">Direktori Posko Siaga Kecamatan</text>
      <text x="0" y="38" class="text-sm">Terhubung langsung dengan operator siaga posko terdekat</text>

      <!-- Mako Pusat High-Priority Card -->
      <rect x="0" y="55" width="480" height="150" fill="#fee2e2" stroke="#ef4444" stroke-width="1.5" rx="8" />
      <rect x="20" y="72" width="130" height="22" class="badge-red-bg" />
      <text x="85" y="87" class="badge-red-text" text-anchor="middle">MARKAS PUSAT (24/7)</text>
      <text x="20" y="115" class="heading-md" font-size="15">Mako Pusat Dinas Pemadam Kebakaran</text>
      <text x="20" y="135" class="text-sm">Jl. Kapten Piere Tendean No. 2, Tj. Karang Pusat</text>
      <text x="20" y="152" class="text-sm" font-weight="bold">Telp: (0721) 252741  |  Hotline: 113 / 112</text>
      <rect x="20" y="165" width="160" height="28" fill="#dc2626" rx="4" />
      <text x="100" y="183" class="btn-primary-text" font-size="11">📞 Panggil Mako Pusat</text>

      <!-- Posko Kedaton -->
      <rect x="0" y="220" width="480" height="95" class="card-bg" />
      <text x="20" y="245" class="heading-md">Posko Wilayah Kedaton</text>
      <text x="20" y="265" class="text-sm">Jl. Teuku Umar No. 88 | Wilayah: Kedaton, Rajabasa, Labuhan Ratu</text>
      <text x="20" y="282" class="text-sm" font-weight="bold">Telepon Siaga: (0721) 701113</text>
      <rect x="340" y="245" width="120" height="30" fill="#1e3a8a" rx="4" />
      <text x="400" y="264" class="btn-primary-text" font-size="11">Hubungi Posko</text>

      <!-- Posko Sukarame -->
      <rect x="0" y="330" width="480" height="95" class="card-bg" />
      <text x="20" y="355" class="heading-md">Posko Wilayah Sukarame</text>
      <text x="20" y="375" class="text-sm">Jl. Endro Suratmin | Wilayah: Sukarame, Way Halim, Sukabumi</text>
      <text x="20" y="392" class="text-sm" font-weight="bold">Telepon Siaga: (0721) 782113</text>
      <rect x="340" y="355" width="120" height="30" fill="#1e3a8a" rx="4" />
      <text x="400" y="374" class="btn-primary-text" font-size="11">Hubungi Posko</text>

      <!-- Posko Kemiling -->
      <rect x="0" y="440" width="480" height="95" class="card-bg" />
      <text x="20" y="465" class="heading-md">Posko Wilayah Kemiling</text>
      <text x="20" y="485" class="text-sm">Jl. Imam Bonjol | Wilayah: Kemiling, Langkapura, TBT</text>
      <text x="20" y="502" class="text-sm" font-weight="bold">Telepon Siaga: (0721) 271113</text>
      <rect x="340" y="465" width="120" height="30" fill="#1e3a8a" rx="4" />
      <text x="400" y="484" class="btn-primary-text" font-size="11">Hubungi Posko</text>

      <!-- Posko Panjang -->
      <rect x="0" y="550" width="480" height="95" class="card-bg" />
      <text x="20" y="575" class="heading-md">Posko Wilayah Panjang</text>
      <text x="20" y="595" class="text-sm">Jl. Yos Sudarso No. 12 | Wilayah: Panjang, Bumi Waras</text>
      <text x="20" y="612" class="text-sm" font-weight="bold">Telepon Siaga: (0721) 31113</text>
      <rect x="340" y="575" width="120" height="30" fill="#1e3a8a" rx="4" />
      <text x="400" y="594" class="btn-primary-text" font-size="11">Hubungi Posko</text>

      <!-- Posko Teluk Betung -->
      <rect x="0" y="660" width="480" height="95" class="card-bg" />
      <text x="20" y="685" class="heading-md">Posko Wilayah Teluk Betung</text>
      <text x="20" y="705" class="text-sm">Jl. Basuki Rahmat No. 4 | Wilayah: TB Selatan, TB Barat, TB Timur</text>
      <text x="20" y="722" class="text-sm" font-weight="bold">Telepon Siaga: (0721) 481113</text>
      <rect x="340" y="685" width="120" height="30" fill="#1e3a8a" rx="4" />
      <text x="400" y="704" class="btn-primary-text" font-size="11">Hubungi Posko</text>
    </g>

    <!-- RIGHT COLUMN: INTERACTIVE REPORT FORM (w=600) -->
    <g transform="translate(520, 0)">
      <rect x="0" y="0" width="600" height="755" class="card-bg" />

      <g transform="translate(30, 25)">
        <text x="0" y="20" class="heading-lg">Formulir Laporan Insiden Online</text>
        <text x="0" y="40" class="text-sm">Validasi masukan seketika untuk mencegah galat data dalam kondisi panik</text>

        <!-- Field 1: Nama -->
        <text x="0" y="75" class="table-hdr-text">Nama Lengkap Pelapor *</text>
        <rect x="0" y="85" width="540" height="38" fill="#f8fafc" stroke="#10b981" stroke-width="1.5" rx="6" />
        <text x="15" y="109" class="table-cell-text">Alif Zakiansyah</text>
        <text x="515" y="109" font-size="14" fill="#10b981">✓</text>
        <text x="0" y="135" class="text-sm" fill="#10b981">Format nama valid</text>

        <!-- Field 2: Telepon/WA -->
        <text x="0" y="160" class="table-hdr-text">Nomor Telepon / WhatsApp Aktif *</text>
        <rect x="0" y="170" width="540" height="38" fill="#f8fafc" stroke="#10b981" stroke-width="1.5" rx="6" />
        <text x="15" y="194" class="table-cell-text">0812-9876-5432</text>
        <text x="515" y="194" font-size="14" fill="#10b981">✓</text>
        <text x="0" y="220" class="text-sm" fill="#10b981">Nomor dapat dihubungi untuk konfirmasi verifikasi</text>

        <!-- Field 3: Lokasi -->
        <text x="0" y="245" class="table-hdr-text">Lokasi Lengkap &amp; Kecamatan Kejadian *</text>
        <rect x="0" y="255" width="540" height="38" fill="#f8fafc" stroke="#10b981" stroke-width="1.5" rx="6" />
        <text x="15" y="279" class="table-cell-text">Jl. Raden Intan No. 45, Kecamatan Enggal (dekat simpang posko)</text>
        <text x="515" y="279" font-size="14" fill="#10b981">✓</text>

        <!-- Field 4: Jenis Kejadian Dropdown -->
        <text x="0" y="325" class="table-hdr-text">Jenis Kejadian Bencana / Rescue *</text>
        <rect x="0" y="335" width="540" height="38" fill="#ffffff" stroke="#cbd5e1" rx="6" />
        <text x="15" y="359" class="table-cell-text">Kebakaran Bangunan Pemukiman / Ruko</text>
        <text x="515" y="359" class="text-sm">▼</text>

        <!-- Field 5: Keterangan -->
        <text x="0" y="405" class="table-hdr-text">Keterangan Situasi &amp; Titik Api *</text>
        <rect x="0" y="415" width="540" height="85" fill="#f8fafc" stroke="#cbd5e1" rx="6" />
        <text x="15" y="440" class="text-sm" fill="#334155">Terlihat asap tebal dan kobaran api dari lantai dua ruko. Akses jalan selebar</text>
        <text x="15" y="458" class="text-sm" fill="#334155">6 meter dan sumber air dapat diambil dari parit sekitar 50 meter.</text>
        <text x="535" y="490" class="text-sm" text-anchor="end" fill="#94a3b8">128/500 karakter</text>

        <!-- Field 6: Upload Drag & Drop Mock -->
        <text x="0" y="525" class="table-hdr-text">Unggah Foto Kejadian (Opsional)</text>
        <rect x="0" y="535" width="540" height="65" fill="#f1f5f9" stroke="#94a3b8" stroke-dasharray="4 4" rx="6" />
        <text x="270" y="565" class="text-sm" text-anchor="middle" fill="#64748b">📷 Seret &amp; lepas foto kejadian ke sini atau <tspan fill="#1e40af" font-weight="bold">pilih berkas</tspan></text>
        <text x="270" y="583" class="text-sm" text-anchor="middle" fill="#94a3b8">(Maksimal 3 foto format JPG/PNG, maks 5 MB)</text>

        <!-- Error Prevention Box -->
        <g transform="translate(0, 615)">
          <rect x="0" y="0" width="540" height="36" fill="#fffbeb" stroke="#f59e0b" rx="6" />
          <text x="12" y="23" font-size="14">⚠️</text>
          <text x="35" y="23" class="text-sm" fill="#92400e"><tspan font-weight="bold">Pencegahan Galat:</tspan> Petugas akan menelepon pelapor dalam &lt;60 detik untuk verifikasi.</text>
        </g>

        <!-- Submit Button -->
        <rect x="0" y="665" width="540" height="46" class="btn-primary" />
        <text x="270" y="694" class="btn-primary-text" font-size="14">🚨 KIRIM LAPORAN KEJADIAN SEKARANG</text>
      </g>
    </g>
  </g>

  {footer(w, 1140)}
  {sticky_emergency_button(980, 1020)}
</svg>"""
    return svg


# ==============================================================================
# 6. WIREFRAME 06: RESPONSIVE MOBILE VIEWPORT (SMARTPHONE) (450 x 1500)
# ==============================================================================
def generate_wireframe_06():
    w, h = 450, 1500
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {STYLE_DEF}
  <rect width="{w}" height="{h}" fill="#e2e8f0" />

  <!-- SMARTPHONE DEVICE FRAME (iPhone/Pixel Mockup) -->
  <rect x="15" y="15" width="420" height="1470" rx="44" fill="#0f172a" stroke="#334155" stroke-width="4" />
  <!-- Screen Inner Display -->
  <rect x="25" y="25" width="400" height="1450" rx="34" class="bg-canvas" />

  <!-- Dynamic Island / Speaker Notch -->
  <rect x="160" y="34" width="130" height="24" rx="12" fill="#000000" />
  <circle cx="270" cy="46" r="4.5" fill="#1e293b" />

  <!-- MOBILE TOP STATUS BAR -->
  <g transform="translate(40, 70)">
    <rect x="0" y="0" width="370" height="26" class="top-bar-bg" rx="4" />
    <text x="185" y="17" class="top-bar-text" text-anchor="middle" font-size="10">🚨 POSKO SIAGA 24 JAM | SPM &lt; 15 MNT</text>
  </g>

  <!-- MOBILE APP HEADER / NAVBAR -->
  <g transform="translate(40, 105)">
    <rect x="0" y="0" width="370" height="52" class="navbar-bg" rx="6" />
    <text x="15" y="32" font-size="20">🚒</text>
    <text x="45" y="26" class="heading-md" font-size="12">Damkarmat</text>
    <text x="45" y="40" class="nav-subtitle">Bandar Lampung</text>

    <!-- Search & Menu Icons -->
    <text x="300" y="32" font-size="16">🔍</text>
    <text x="335" y="32" font-size="20" font-weight="bold">☰</text>
  </g>

  <!-- MOBILE HERO SECTION (FITTS'S LAW THUMB ZONE OPTIMIZED) -->
  <g transform="translate(40, 170)">
    <rect x="0" y="0" width="370" height="270" class="hero-bg" rx="10" />

    <rect x="15" y="15" width="160" height="20" class="badge-red-bg" />
    <text x="95" y="29" class="badge-red-text" text-anchor="middle">SPM WAKTU TANGGAP &lt; 15 MNT</text>

    <text x="15" y="60" class="heading-md" font-size="16">Tanggap Darurat 24 Jam</text>
    <text x="15" y="82" class="heading-md" font-size="16">Kota Bandar Lampung</text>
    <text x="15" y="108" class="text-sm">Layanan pemadaman dan rescue warga gratis</text>
    <text x="15" y="124" class="text-sm">didukung 6 posko siaga kecamatan.</text>

    <!-- BIG THUMB-FRIENDLY EMERGENCY CALL BUTTON (Hukum Fitts) -->
    <rect x="15" y="145" width="340" height="56" rx="28" class="btn-primary" />
    <text x="185" y="174" class="btn-primary-text" font-size="15">📞 HUBUNGI DARURAT 113</text>
    <text x="185" y="191" font-family="sans-serif" font-size="10" fill="#fee2e2" text-anchor="middle">Panggilan Cepat 1-Sentuhan (Bebas Pulsa)</text>

    <!-- Secondary Action -->
    <rect x="15" y="212" width="340" height="42" class="btn-secondary" />
    <text x="185" y="238" class="btn-secondary-text" font-size="12">📝 Lapor Insiden Online</text>
  </g>

  <!-- MOBILE EMERGENCY WARNING STRIP -->
  <g transform="translate(40, 455)">
    <rect x="0" y="0" width="370" height="42" fill="#fffbeb" stroke="#f59e0b" rx="6" />
    <text x="12" y="26" font-size="14">⚠️</text>
    <text x="35" y="25" class="text-sm" fill="#92400e" font-weight="bold">Siaga Kemarau: Waspada Kebakaran Lahan</text>
  </g>

  <!-- MOBILE 2x2 SERVICES GRID -->
  <g transform="translate(40, 510)">
    <text x="0" y="18" class="heading-md" font-size="14">Layanan Utama Kedaruratan</text>

    <!-- Service 1 -->
    <rect x="0" y="30" width="180" height="100" class="card-bg" />
    <text x="15" y="58" font-size="20">🔥</text>
    <text x="15" y="80" class="heading-md" font-size="12">Pemadaman</text>
    <text x="15" y="96" class="text-sm" font-size="9">Respon Cepat &lt;15 Mnt</text>
    <text x="15" y="116" class="nav-link-active" font-size="10">Panggil 113 &gt;</text>

    <!-- Service 2 -->
    <rect x="190" y="30" width="180" height="100" class="card-bg" />
    <text x="205" y="58" font-size="20">🛡️</text>
    <text x="205" y="80" class="heading-md" font-size="12">Aksi Rescue</text>
    <text x="205" y="96" class="text-sm" font-size="9">Satwa &amp; Evakuasi</text>
    <text x="205" y="116" class="nav-link-active" font-size="10">Lapor Rescue &gt;</text>

    <!-- Service 3 -->
    <rect x="0" y="140" width="180" height="100" class="card-bg" />
    <text x="15" y="168" font-size="20">📍</text>
    <text x="15" y="190" class="heading-md" font-size="12">Posko Siaga</text>
    <text x="15" y="206" class="text-sm" font-size="9">6 Posko Wilayah</text>
    <text x="15" y="226" class="nav-link-active" font-size="10">Cari Posko &gt;</text>

    <!-- Service 4 -->
    <rect x="190" y="140" width="180" height="100" class="card-bg" />
    <text x="205" y="168" font-size="20">📄</text>
    <text x="205" y="190" class="heading-md" font-size="12">Dokumen SOP</text>
    <text x="205" y="206" class="text-sm" font-size="9">Unduh Berkas</text>
    <text x="205" y="226" class="nav-link-active" font-size="10">Unduh PDF &gt;</text>
  </g>

  <!-- MOBILE 2x2 OPERATIONAL STATS -->
  <g transform="translate(40, 770)">
    <text x="0" y="18" class="heading-md" font-size="14">Capaian Kinerja Operasional</text>

    <rect x="0" y="30" width="180" height="75" class="card-bg" />
    <text x="15" y="62" font-family="sans-serif" font-size="24" font-weight="800" fill="#dc2626">271</text>
    <text x="15" y="82" class="table-hdr-text" font-size="11">Kebakaran (2024)</text>

    <rect x="190" y="30" width="180" height="75" class="card-bg" />
    <text x="205" y="62" font-family="sans-serif" font-size="24" font-weight="800" fill="#0284c7">518</text>
    <text x="205" y="82" class="table-hdr-text" font-size="11">Rescue (2025)</text>

    <rect x="0" y="115" width="180" height="75" class="card-bg" />
    <text x="15" y="147" font-family="sans-serif" font-size="24" font-weight="800" fill="#059669">18</text>
    <text x="15" y="167" class="table-hdr-text" font-size="11">Armada Siaga</text>

    <rect x="190" y="115" width="180" height="75" class="card-bg" />
    <text x="205" y="147" font-family="sans-serif" font-size="24" font-weight="800" fill="#7c3aed">&lt; 15 m</text>
    <text x="205" y="167" class="table-hdr-text" font-size="11">Waktu SPM</text>
  </g>

  <!-- MOBILE QUICK POSKO ACCORDION -->
  <g transform="translate(40, 990)">
    <text x="0" y="18" class="heading-md" font-size="14">Direktori Kontak Posko Siaga</text>

    <!-- Posko Item 1 -->
    <rect x="0" y="30" width="370" height="56" class="card-bg" />
    <text x="15" y="55" class="heading-md" font-size="11">Mako Pusat (Tj. Karang Pusat)</text>
    <text x="15" y="72" class="text-sm" font-size="9">Jl. Kapt. P. Tendean | Telp: (0721) 252741</text>
    <rect x="270" y="42" width="85" height="30" fill="#dc2626" rx="4" />
    <text x="312" y="61" class="btn-primary-text" font-size="10">Telepon</text>

    <!-- Posko Item 2 -->
    <rect x="0" y="94" width="370" height="56" class="card-bg" />
    <text x="15" y="119" class="heading-md" font-size="11">Posko Kedaton</text>
    <text x="15" y="136" class="text-sm" font-size="9">Jl. Teuku Umar | Telp: (0721) 701113</text>
    <rect x="270" y="106" width="85" height="30" fill="#1e3a8a" rx="4" />
    <text x="312" y="125" class="btn-primary-text" font-size="10">Telepon</text>

    <!-- Posko Item 3 -->
    <rect x="0" y="158" width="370" height="56" class="card-bg" />
    <text x="15" y="183" class="heading-md" font-size="11">Posko Sukarame</text>
    <text x="15" y="200" class="text-sm" font-size="9">Jl. Endro Suratmin | Telp: (0721) 782113</text>
    <rect x="270" y="170" width="85" height="30" fill="#1e3a8a" rx="4" />
    <text x="312" y="189" class="btn-primary-text" font-size="10">Telepon</text>
  </g>

  <!-- MOBILE NEWS LIST -->
  <g transform="translate(40, 1235)">
    <text x="0" y="18" class="heading-md" font-size="14">Warta Operasional Terbaru</text>
    <rect x="0" y="28" width="370" height="65" class="card-bg" />
    <text x="15" y="52" class="heading-md" font-size="11">Kebakaran Gudang Kedaton Berhasil Dipadamkan</text>
    <text x="15" y="70" class="text-sm" font-size="9">15 Sep 2025 • Respon 11 menit • 6 Unit mobil</text>
    <text x="345" y="62" class="table-hdr-text">&gt;</text>
  </g>

  <!-- FIXED BOTTOM THUMB NAVIGATION BAR -->
  <g transform="translate(25, 1375)">
    <rect x="0" y="0" width="400" height="80" fill="#1e293b" rx="20" />
    
    <rect x="20" y="14" width="170" height="50" rx="25" class="btn-primary" />
    <text x="105" y="44" class="btn-primary-text" font-size="12">🚨 PANGGIL 113</text>

    <rect x="210" y="14" width="170" height="50" rx="25" fill="#059669" />
    <text x="295" y="44" class="btn-primary-text" font-size="12">💬 WhatsApp Siaga</text>
  </g>
</svg>"""
    return svg


# ==============================================================================
# 7. WIREFRAME 07: MODAL INTERAKTIF & PENCEGAHAN GALAT (1200 x 900)
# ==============================================================================
def generate_wireframe_07():
    w, h = 1200, 920
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {STYLE_DEF}
  <rect width="{w}" height="{h}" fill="#334155" />

  <!-- TITLE HEADER -->
  <g transform="translate(60, 40)">
    <text x="0" y="0" font-family="sans-serif" font-size="22" font-weight="bold" fill="#f8fafc">Cetak Biru Komponen Dialog Interaktif &amp; Pencegahan Galat (HCI)</text>
    <text x="0" y="24" font-family="sans-serif" font-size="13" fill="#cbd5e1">Perancangan modal panggil cepat kedaruratan (Zero-Latency) dan dialog modal konfirmasi aduan (Nielsen H5 Error Prevention).</text>
  </g>

  <!-- MODAL 1 (KIRI): PANGGILAN CEPAT KEDARURATAN (w=500, h=680) -->
  <g transform="translate(60, 90)">
    <!-- Modal Card Container -->
    <rect x="0" y="0" width="510" height="740" rx="16" fill="#ffffff" filter="drop-shadow(0px 10px 25px rgba(0,0,0,0.5))" />

    <!-- Modal Header Red -->
    <rect x="0" y="0" width="510" height="100" rx="16" fill="#dc2626" />
    <rect x="0" y="80" width="510" height="20" fill="#dc2626" /> <!-- Square bottom corners -->
    <text x="35" y="45" font-size="28">🚨</text>
    <text x="80" y="42" font-family="sans-serif" font-size="18" font-weight="bold" fill="#ffffff">Panggilan Cepat Kedaruratan</text>
    <text x="80" y="65" font-family="sans-serif" font-size="12" fill="#fee2e2">Kota Bandar Lampung — Layanan Siaga 24 Jam</text>
    <text x="475" y="40" font-family="sans-serif" font-size="18" font-weight="bold" fill="#ffffff">✕</text>

    <!-- Modal Body -->
    <g transform="translate(30, 125)">
      <text x="0" y="15" class="text-body" fill="#334155">Pilih kanal panggilan darurat di bawah ini untuk tersambung</text>
      <text x="0" y="33" class="text-body" fill="#334155">seketika dengan petugas operator damkar terdekat:</text>

      <!-- Option 1: 113 -->
      <g transform="translate(0, 55)">
        <rect x="0" y="0" width="450" height="85" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5" rx="10" />
        <rect x="15" y="18" width="50" height="50" fill="#dc2626" rx="25" />
        <text x="40" y="50" font-size="22" fill="#ffffff" text-anchor="middle">📞</text>
        <text x="80" y="38" class="heading-md" font-size="16">Hotline 113 (Bebas Pulsa)</text>
        <text x="80" y="58" class="text-sm">Sambungan langsung pemadam kebakaran seluruh operator seluler.</text>
        <text x="420" y="48" font-size="20" fill="#dc2626">&gt;</text>
      </g>

      <!-- Option 2: 112 -->
      <g transform="translate(0, 155)">
        <rect x="0" y="0" width="450" height="85" class="card-bg" />
        <rect x="15" y="18" width="50" height="50" fill="#1e3a8a" rx="25" />
        <text x="40" y="50" font-size="22" fill="#ffffff" text-anchor="middle">🏛️</text>
        <text x="80" y="38" class="heading-md" font-size="16">Call Center Terpadu 112</text>
        <text x="80" y="58" class="text-sm">Layanan tanggap darurat terintegrasi Pemerintah Kota.</text>
        <text x="420" y="48" font-size="20" fill="#1e3a8a">&gt;</text>
      </g>

      <!-- Option 3: Mako Pusat -->
      <g transform="translate(0, 255)">
        <rect x="0" y="0" width="450" height="85" class="card-bg" />
        <rect x="15" y="18" width="50" height="50" fill="#0284c7" rx="25" />
        <text x="40" y="50" font-size="22" fill="#ffffff" text-anchor="middle">🏢</text>
        <text x="80" y="38" class="heading-md" font-size="16">Mako Pusat (0721) 252741</text>
        <text x="80" y="58" class="text-sm">Jalur PSTN langsung ruang siaga komando Durian Payung.</text>
        <text x="420" y="48" font-size="20" fill="#0284c7">&gt;</text>
      </g>

      <!-- Option 4: WhatsApp Siaga -->
      <g transform="translate(0, 355)">
        <rect x="0" y="0" width="450" height="85" class="card-bg" />
        <rect x="15" y="18" width="50" height="50" fill="#059669" rx="25" />
        <text x="40" y="50" font-size="22" fill="#ffffff" text-anchor="middle">💬</text>
        <text x="80" y="38" class="heading-md" font-size="16">WhatsApp Siaga Petugas</text>
        <text x="80" y="58" class="text-sm">Kirim koordinat lokasi share-live dan foto situasi kebakaran.</text>
        <text x="420" y="48" font-size="20" fill="#059669">&gt;</text>
      </g>

      <!-- Cancel Button -->
      <rect x="0" y="470" width="450" height="42" class="btn-secondary" />
      <text x="225" y="496" class="btn-secondary-text">Tutup Jendela Panggilan</text>

      <!-- Callout Badge -->
      <rect x="100" y="535" width="250" height="24" class="annotation-box" />
      <text x="225" y="551" class="annotation-text" text-anchor="middle">HCI: Zero-Latency Emergency Touchpoint</text>
    </g>
  </g>

  <!-- MODAL 2 (KANAN): KONFIRMASI PENCEGAHAN GALAT (w=530, h=680) -->
  <g transform="translate(610, 90)">
    <!-- Modal Card Container -->
    <rect x="0" y="0" width="530" height="740" rx="16" fill="#ffffff" filter="drop-shadow(0px 10px 25px rgba(0,0,0,0.5))" />

    <!-- Modal Header Navy -->
    <rect x="0" y="0" width="530" height="100" rx="16" fill="#1e293b" />
    <rect x="0" y="80" width="530" height="20" fill="#1e293b" />
    <text x="35" y="45" font-size="28">⚠️</text>
    <text x="80" y="42" font-family="sans-serif" font-size="18" font-weight="bold" fill="#ffffff">Konfirmasi Pengiriman Laporan</text>
    <text x="80" y="65" font-family="sans-serif" font-size="12" fill="#94a3b8">Pencegahan Kesalahan Informasi &amp; Laporan Palsu</text>
    <text x="495" y="40" font-family="sans-serif" font-size="18" font-weight="bold" fill="#ffffff">✕</text>

    <!-- Modal Body -->
    <g transform="translate(30, 125)">
      <text x="0" y="15" class="text-body" fill="#334155">Harap periksa kembali kebenaran data laporan kejadian berikut</text>
      <text x="0" y="33" class="text-body" fill="#334155">sebelum dikirimkan ke Markas Komando Pemadam Kebakaran:</text>

      <!-- Review Summary Box -->
      <rect x="0" y="55" width="470" height="225" fill="#f8fafc" stroke="#cbd5e1" rx="8" />
      
      <g transform="translate(20, 75)">
        <text x="0" y="15" class="text-sm" fill="#64748b">Nama Pelapor:</text>
        <text x="170" y="15" class="heading-md" font-size="13">Alif Zakiansyah</text>

        <text x="0" y="45" class="text-sm" fill="#64748b">Nomor Telepon / WA:</text>
        <text x="170" y="45" class="heading-md" font-size="13">0812-9876-5432</text>

        <text x="0" y="75" class="text-sm" fill="#64748b">Jenis Insiden:</text>
        <text x="170" y="75" class="badge-red-text" font-size="13">🔥 Kebakaran Ruko Pemukiman</text>

        <text x="0" y="105" class="text-sm" fill="#64748b">Lokasi Kejadian:</text>
        <text x="170" y="105" class="heading-md" font-size="12">Jl. Raden Intan No. 45, Kec. Enggal</text>

        <text x="0" y="135" class="text-sm" fill="#64748b">Estimasi Respon Posko:</text>
        <text x="170" y="135" class="badge-blue-text" font-size="13">⏱️ &lt; 10 Menit (Posko Tj. Karang)</text>
      </g>

      <!-- Verification Checkbox -->
      <g transform="translate(0, 305)">
        <rect x="0" y="0" width="22" height="22" rx="4" fill="#1e40af" />
        <text x="6" y="16" fill="#ffffff" font-size="14" font-weight="bold">✓</text>
        <text x="32" y="16" class="table-cell-text" font-size="12">Saya menyatakan bahwa laporan ini benar, terjadi di lokasi,</text>
        <text x="32" y="32" class="table-cell-text" font-size="12">dan saya siap menerima telepon konfirmasi dalam 60 detik.</text>
      </g>

      <!-- Warning Box -->
      <g transform="translate(0, 360)">
        <rect x="0" y="0" width="470" height="40" fill="#fffbeb" stroke="#f59e0b" rx="6" />
        <text x="12" y="25" font-size="14">⚖️</text>
        <text x="35" y="24" class="text-sm" fill="#92400e">Laporan palsu / main-main dapat dipidana sesuai Pasal 220 KUHP.</text>
      </g>

      <!-- Action Buttons -->
      <g transform="translate(0, 425)">
        <rect x="0" y="0" width="220" height="46" class="btn-secondary" />
        <text x="110" y="28" class="btn-secondary-text">Periksa Ulang Data</text>

        <rect x="240" y="0" width="230" height="46" class="btn-primary" />
        <text x="355" y="28" class="btn-primary-text">Kirim &amp; Terbitkan Tiket</text>
      </g>

      <!-- Callout Badge -->
      <rect x="100" y="535" width="270" height="24" class="annotation-box" />
      <text x="235" y="551" class="annotation-text" text-anchor="middle">HCI: Nielsen H5 Error Prevention &amp; Closure</text>
    </g>
  </g>
</svg>"""
    return svg


def main():
    generators = [
        ("wireframe_01_beranda_desktop", generate_wireframe_01),
        ("wireframe_02_berita_desktop", generate_wireframe_02),
        ("wireframe_03_dokumen_desktop", generate_wireframe_03),
        ("wireframe_04_galeri_desktop", generate_wireframe_04),
        ("wireframe_05_kontak_desktop", generate_wireframe_05),
        ("wireframe_06_mobile_responsive", generate_wireframe_06),
        ("wireframe_07_modals_interaction", generate_wireframe_07),
    ]

    print("=================================================================")
    print("MEMULAI GENERASI WIREFRAME DAN LOW-FIDELITY MOCKUP (SVG & PNG)")
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

    print("\n[OK] Seluruh berkas wireframe dan low-fidelity mockup berhasil dihasilkan!")

if __name__ == "__main__":
    main()
