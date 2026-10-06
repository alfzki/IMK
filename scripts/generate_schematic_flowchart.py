"""
scripts/generate_schematic_flowchart.py

Menghasilkan representasi skematik Diagram Alir Penelitian (Research Methodology Flowchart)
sesuai spesifikasi visual rancangan pengguna dalam format:
1. Draw.io XML (.drawio) -> drafts/figures/gambar_01_diagram_alir_skematik.drawio
2. Vector SVG (.svg)     -> drafts/figures/gambar_01_diagram_alir_skematik.svg
3. High-Res PNG (.png)   -> drafts/figures/gambar_01_diagram_alir_skematik.png
"""

import os
import subprocess
import xml.etree.ElementTree as ET

OUT_DIR = "drafts/figures"
os.makedirs(OUT_DIR, exist_ok=True)

DRAWIO_FILE = os.path.join(OUT_DIR, "gambar_01_diagram_alir_skematik.drawio")
SVG_FILE = os.path.join(OUT_DIR, "gambar_01_diagram_alir_skematik.svg")
PNG_FILE = os.path.join(OUT_DIR, "gambar_01_diagram_alir_skematik.png")


def build_drawio_xml() -> str:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-10-01T16:30:00.000Z" agent="Antigravity/1.0" version="24.0.0">
  <diagram id="schematic-research-flowchart-kelompok-8" name="Diagram Alir Skematik Penelitian">
    <mxGraphModel dx="1400" dy="1600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1240" pageHeight="1480" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- ========================================== -->
        <!-- TAHAP 1: INISIASI RISET & MASALAH EMPIRIS -->
        <!-- ========================================== -->
        <mxCell id="c_tahap1" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="30" width="1160" height="165" as="geometry" />
        </mxCell>
        <mxCell id="lbl_tahap1" value="&lt;b&gt;TAHAP 1: INISIASI RISET &amp;amp; MASALAH EMPIRIS&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;fontColor=#1E293B;" vertex="1" parent="1">
          <mxGeometry x="50" y="36" width="350" height="20" as="geometry" />
        </mxCell>

        <!-- 3 Kotak Input Tahap 1 -->
        <mxCell id="b_1a" value="&lt;b&gt;Audit Awal Website Eksisting &amp;amp; Survei Pendahuluan (N=22)&lt;/b&gt;&lt;br/&gt;(Rerata kepuasan rendah: 2,70 / 5,00)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=10;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="70" y="65" width="350" height="46" as="geometry" />
        </mxCell>
        <mxCell id="b_1b" value="&lt;b&gt;Tuntutan Regulasi SPM Permendagri No. 114/2018&lt;/b&gt;&lt;br/&gt;(Standar response time &amp;lt; 15 menit)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=10;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="445" y="65" width="350" height="46" as="geometry" />
        </mxCell>
        <mxCell id="b_1c" value="&lt;b&gt;Analisis Data Frekuensi Bencana Kebakaran &amp;amp; Rescue&lt;/b&gt;&lt;br/&gt;(413 insiden &#39;23; 271 &#39;24; 198 &#39;25; 518 aksi rescue &#39;25)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=10;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="820" y="65" width="350" height="46" as="geometry" />
        </mxCell>

        <!-- Kotak Konvergensi Masalah -->
        <mxCell id="b_1d" value="&lt;b&gt;Identifikasi Masalah &amp;amp; Perumusan Kesenjangan Riset&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=10.5;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="370" y="138" width="500" height="38" as="geometry" />
        </mxCell>

        <!-- Panah dari 1a, 1b, 1c ke 1d -->
        <mxCell id="a_1a_1d" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.2;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_1a" target="b_1d">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="a_1b_1d" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_1b" target="b_1d">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="a_1c_1d" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.8;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_1c" target="b_1d">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>


        <!-- ================================================================= -->
        <!-- CONTAINER UTAMA: SIKLUS ITERASI USER-CENTERED DESIGN (ISO 9241-210) -->
        <!-- ================================================================= -->
        <mxCell id="c_ucd" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="215" width="1160" height="1065" as="geometry" />
        </mxCell>
        <mxCell id="lbl_ucd" value="&lt;b&gt;SIKLUS ITERASI USER-CENTERED DESIGN (ISO 9241-210:2019)&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;fontColor=#1E293B;" vertex="1" parent="1">
          <mxGeometry x="50" y="221" width="450" height="20" as="geometry" />
        </mxCell>

        <!-- Panah dari 1d ke Siklus UCD (Fase 1) -->
        <mxCell id="a_1d_f1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_1d" target="c_fase1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- FASE 1 -->
        <mxCell id="c_fase1" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;" vertex="1" parent="1">
          <mxGeometry x="55" y="250" width="1130" height="145" as="geometry" />
        </mxCell>
        <mxCell id="lbl_fase1" value="&lt;b&gt;FASE 1: Memahami Konteks Penggunaan (Context of Use)&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=9.5;fontColor=#1E293B;" vertex="1" parent="1">
          <mxGeometry x="65" y="255" width="400" height="18" as="geometry" />
        </mxCell>

        <mxCell id="b_f1_1" value="Analisis Kondisi Psikologis (Kepanikan saat Krisis) &amp;amp; Akses Seluler" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=10;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="70" y="280" width="350" height="42" as="geometry" />
        </mxCell>
        <mxCell id="b_f1_2" value="Perumusan User Persona (Emergency Persona vs Public Persona)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=10;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="445" y="280" width="350" height="42" as="geometry" />
        </mxCell>
        <mxCell id="b_f1_3" value="Identifikasi Karakteristik &amp;amp; Kebutuhan Pengguna" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=10;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="820" y="280" width="350" height="42" as="geometry" />
        </mxCell>

        <mxCell id="b_f1_out" value="&lt;b&gt;Luaran: Peta Konteks Penggunaan &amp;amp; Task Scenarios&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#333333;strokeWidth=1;fontSize=10;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="390" y="345" width="460" height="34" as="geometry" />
        </mxCell>

        <mxCell id="a_f1_1_out" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.2;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f1_1" target="b_f1_out">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="a_f1_2_out" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f1_2" target="b_f1_out">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="a_f1_3_out" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.8;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f1_3" target="b_f1_out">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Panah dari Fase 1 ke Fase 2 -->
        <mxCell id="a_f1_f2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f1_out" target="c_fase2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>


        <!-- FASE 2 -->
        <mxCell id="c_fase2" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;" vertex="1" parent="1">
          <mxGeometry x="55" y="415" width="1130" height="145" as="geometry" />
        </mxCell>
        <mxCell id="lbl_fase2" value="&lt;b&gt;FASE 2: Menentukan Kebutuhan Pengguna (Specify User Requirements)&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=9.5;fontColor=#1E293B;" vertex="1" parent="1">
          <mxGeometry x="65" y="420" width="480" height="18" as="geometry" />
        </mxCell>

        <mxCell id="b_f2_1" value="Perumusan Parameter HCI: Emotional Design, Fitts&#39;s Law, Fluid Navigation" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=10;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="70" y="445" width="350" height="42" as="geometry" />
        </mxCell>
        <mxCell id="b_f2_2" value="Klasifikasi Severity Rating Masalah Usabilitas (Skala 0-4)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=10;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="445" y="445" width="350" height="42" as="geometry" />
        </mxCell>
        <mxCell id="b_f2_3" value="Audit Inspeksi 10 Prinsip Heuristik Nielsen pada Website Eksisting" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=10;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="820" y="445" width="350" height="42" as="geometry" />
        </mxCell>

        <mxCell id="b_f2_out" value="&lt;b&gt;Luaran: Matriks Kebutuhan Pengguna &amp;amp; Dokumen Spesifikasi Desain&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#333333;strokeWidth=1;fontSize=10;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="370" y="510" width="500" height="34" as="geometry" />
        </mxCell>

        <mxCell id="a_f2_1_out" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.2;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f2_1" target="b_f2_out">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="a_f2_2_out" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f2_2" target="b_f2_out">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="a_f2_3_out" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.8;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f2_3" target="b_f2_out">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Panah dari Fase 2 ke Fase 3 -->
        <mxCell id="a_f2_f3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f2_out" target="c_fase3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>


        <!-- FASE 3 -->
        <mxCell id="c_fase3" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;" vertex="1" parent="1">
          <mxGeometry x="55" y="580" width="1130" height="150" as="geometry" />
        </mxCell>
        <mxCell id="lbl_fase3" value="&lt;b&gt;FASE 3: Merancang Solusi Desain (Produce Design Solutions)&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=9.5;fontColor=#1E293B;" vertex="1" parent="1">
          <mxGeometry x="65" y="585" width="450" height="18" as="geometry" />
        </mxCell>

        <mxCell id="b_f3_1" value="Purwarupa Interaktif Tinggi Fidelitas (Figma &amp;amp; Full-Stack Next.js/Tailwind)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=9.5;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="70" y="610" width="260" height="46" as="geometry" />
        </mxCell>
        <mxCell id="b_f3_2" value="Arsitektur Informasi (IA) Dua-Jalur &amp;amp; Skematik User Flow" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=9.5;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="350" y="610" width="260" height="46" as="geometry" />
        </mxCell>
        <mxCell id="b_f3_3" value="Perancangan Rendah Fidelitas: Low-Fidelity Wireframe (Sketsa Balsamiq)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=9.5;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="630" y="610" width="260" height="46" as="geometry" />
        </mxCell>
        <mxCell id="b_f3_4" value="Sistem Desain &amp;amp; Aksesibilitas WCAG 2.1 AA (Primary Navy &amp;amp; Emergency Red)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=9.5;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="910" y="610" width="260" height="46" as="geometry" />
        </mxCell>

        <mxCell id="b_f3_out" value="&lt;b&gt;Luaran: Live Interactive Prototype Web &amp;amp; Cetak Biru Wireframe&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#333333;strokeWidth=1;fontSize=10;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="370" y="680" width="500" height="34" as="geometry" />
        </mxCell>

        <mxCell id="a_f3_1_out" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.15;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f3_1" target="b_f3_out">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="a_f3_2_out" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.38;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f3_2" target="b_f3_out">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="a_f3_3_out" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.62;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f3_3" target="b_f3_out">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="a_f3_4_out" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.85;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f3_4" target="b_f3_out">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Panah dari Fase 3 ke Fase 4 -->
        <mxCell id="a_f3_f4" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f3_out" target="c_fase4">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>


        <!-- FASE 4 -->
        <mxCell id="c_fase4" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;" vertex="1" parent="1">
          <mxGeometry x="55" y="750" width="1130" height="150" as="geometry" />
        </mxCell>
        <mxCell id="lbl_fase4" value="&lt;b&gt;FASE 4: Evaluasi Desain terhadap Kebutuhan (Evaluate Against Requirements)&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=9.5;fontColor=#1E293B;" vertex="1" parent="1">
          <mxGeometry x="65" y="755" width="520" height="18" as="geometry" />
        </mxCell>

        <mxCell id="b_f4_1" value="Pengukuran Task Completion Time Penemuan Kontak Darurat (&amp;lt; 3 Detik)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=9.5;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="70" y="780" width="260" height="46" as="geometry" />
        </mxCell>
        <mxCell id="b_f4_2" value="Pengujian Kuantitatif WebQual 4.0 Komparatif Before vs After (22 Indikator)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=9.5;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="350" y="780" width="260" height="46" as="geometry" />
        </mxCell>
        <mxCell id="b_f4_3" value="Uji Beda Berpasangan Wilcoxon Signed-Rank Test (Signifikansi p &amp;lt; 0,001)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=9.5;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="630" y="780" width="260" height="46" as="geometry" />
        </mxCell>
        <mxCell id="b_f4_4" value="Audit Aksesibilitas WCAG 2.1 Level AA (Uji WAVE &amp;amp; Rasio Kontras)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=9.5;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="910" y="780" width="260" height="46" as="geometry" />
        </mxCell>

        <mxCell id="b_f4_out" value="&lt;b&gt;Luaran: Skor WebQual 4.0, Output Wilcoxon, &amp;amp; Bukti Bebas Galat WAVE&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#333333;strokeWidth=1;fontSize=10;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="350" y="850" width="540" height="34" as="geometry" />
        </mxCell>

        <mxCell id="a_f4_1_out" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.15;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f4_1" target="b_f4_out">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="a_f4_2_out" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.38;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f4_2" target="b_f4_out">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="a_f4_3_out" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.62;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f4_3" target="b_f4_out">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="a_f4_4_out" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.85;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f4_4" target="b_f4_out">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Panah dari Fase 4 ke Decision Diamond -->
        <mxCell id="a_f4_decision" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_f4_out" target="decision_diamond">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>


        <!-- DECISION DIAMOND -->
        <mxCell id="decision_diamond" value="&lt;b&gt;Apakah Kriteria Usabilitas &amp;amp; Standar SPM Terpenuhi?&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size: 8.5px;&quot;&gt;(Skor WebQual &amp;#8805; 4,00 | p &amp;lt; 0,05 | Akses &amp;lt; 3 detik | WCAG 0 Error)&lt;/span&gt;" style="rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1.2;fontSize=9.5;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="410" y="920" width="420" height="110" as="geometry" />
        </mxCell>

        <!-- Cabang TIDAK: Kotak Iterasi UCD -->
        <mxCell id="b_iterasi" value="Iterasi UCD: Penyesuaian Desain &amp;amp; Fitur" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=9.5;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="840" y="1120" width="240" height="38" as="geometry" />
        </mxCell>

        <!-- Panah dari Diamond ke Iterasi UCD (TIDAK) -->
        <mxCell id="a_decision_tidak" value="TIDAK (Perlu Perbaikan)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=9;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="decision_diamond" target="b_iterasi">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="620" y="1080" />
              <mxPoint x="960" y="1080" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- Feedback Loop Panah dari Iterasi UCD kembali ke FASE 3 -->
        <mxCell id="a_feedback_loop" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;dashPattern=4 2;strokeColor=#333333;strokeWidth=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="b_iterasi" target="c_fase3">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1150" y="1139" />
              <mxPoint x="1150" y="655" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- Cabang YA: Panah dari Diamond ke Container Tahap Akhir -->
        <mxCell id="a_decision_ya" value="YA (Memenuhi Kriteria)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=9;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="decision_diamond" target="c_tahap_akhir">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="620" y="1290" />
              <mxPoint x="620" y="1290" />
            </Array>
          </mxGeometry>
        </mxCell>


        <!-- ========================================== -->
        <!-- TAHAP AKHIR: LUARAN RISET & PUBLIKASI     -->
        <!-- ========================================== -->
        <mxCell id="c_tahap_akhir" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="1310" width="1160" height="110" as="geometry" />
        </mxCell>
        <mxCell id="lbl_tahap_akhir" value="&lt;b&gt;TAHAP AKHIR: LUARAN RISET &amp;amp; PUBLIKASI&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;fontColor=#1E293B;" vertex="1" parent="1">
          <mxGeometry x="50" y="1316" width="350" height="20" as="geometry" />
        </mxCell>

        <!-- 4 Kotak Luaran Akhir -->
        <mxCell id="b_fin_1" value="Matriks Analisis 32 Aspek IMK Before &amp;amp; After Terisi Lengkap 100%" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=9.5;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="70" y="1345" width="260" height="46" as="geometry" />
        </mxCell>
        <mxCell id="b_fin_2" value="Portal Web Redesain Siap Pakai (Production Ready di Vercel)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=9.5;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="350" y="1345" width="260" height="46" as="geometry" />
        </mxCell>
        <mxCell id="b_fin_3" value="Peningkatan Mutu Terbukti Signifikan (+1,94; p &amp;lt; 0,001)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=9.5;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="630" y="1345" width="260" height="46" as="geometry" />
        </mxCell>
        <mxCell id="b_fin_4" value="Naskah Makalah Ilmiah Standar Publikasi Bebas Halusinasi (31 Rujukan APA 7th)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#333333;strokeWidth=1;fontSize=9.5;align=center;verticalAlign=middle;" vertex="1" parent="1">
          <mxGeometry x="910" y="1345" width="260" height="46" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    return xml.strip()


def build_schematic_svg() -> str:
    w, h = 1240, 1460
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <style>
      .bg {{ fill: #ffffff; }}
      .container-box {{ fill: #ffffff; stroke: #333333; stroke-width: 1; }}
      .sub-container {{ fill: #ffffff; stroke: #333333; stroke-width: 1; }}
      .node-box {{ fill: #ffffff; stroke: #333333; stroke-width: 1; }}
      .output-box {{ fill: #f8fafc; stroke: #333333; stroke-width: 1; }}
      .diamond {{ fill: #ffffff; stroke: #333333; stroke-width: 1.2; }}
      .title-text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; font-size: 11px; font-weight: bold; fill: #1e293b; }}
      .node-title {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; font-size: 10px; font-weight: bold; fill: #0f172a; text-anchor: middle; }}
      .node-sub {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; font-size: 9px; fill: #334155; text-anchor: middle; }}
      .node-desc {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; font-size: 9.5px; fill: #0f172a; text-anchor: middle; }}
      .label-text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; font-size: 9px; fill: #475569; text-anchor: middle; }}
      .arrow-line {{ stroke: #333333; stroke-width: 1; fill: none; }}
      .arrow-loop {{ stroke: #333333; stroke-width: 1; stroke-dasharray: 4 2; fill: none; }}
    </style>
    <marker id="arr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#333333" />
    </marker>
  </defs>

  <rect width="{w}" height="{h}" class="bg" />

  <!-- ================= TAHAP 1 ================= -->
  <rect x="40" y="30" width="1160" height="165" class="container-box" />
  <text x="50" y="50" class="title-text">TAHAP 1: INISIASI RISET &amp; MASALAH EMPIRIS</text>

  <!-- Box 1A -->
  <rect x="70" y="65" width="350" height="46" class="node-box" />
  <text x="245" y="83" class="node-title">Audit Awal Website Eksisting &amp; Survei Pendahuluan (N=22)</text>
  <text x="245" y="99" class="node-sub">(Rerata kepuasan rendah: 2,70 / 5,00)</text>

  <!-- Box 1B -->
  <rect x="445" y="65" width="350" height="46" class="node-box" />
  <text x="620" y="83" class="node-title">Tuntutan Regulasi SPM Permendagri No. 114/2018</text>
  <text x="620" y="99" class="node-sub">(Standar response time &lt; 15 menit)</text>

  <!-- Box 1C -->
  <rect x="820" y="65" width="350" height="46" class="node-box" />
  <text x="995" y="83" class="node-title">Analisis Data Frekuensi Bencana Kebakaran &amp; Rescue</text>
  <text x="995" y="99" class="node-sub">(413 insiden &#39;23; 271 &#39;24; 198 &#39;25; 518 aksi rescue &#39;25)</text>

  <!-- Box 1D -->
  <rect x="370" y="138" width="500" height="38" class="node-box" />
  <text x="620" y="162" class="node-title">Identifikasi Masalah &amp; Perumusan Kesenjangan Riset</text>

  <!-- Panah Tahap 1 -->
  <path d="M 245 111 L 245 125 L 470 125 L 470 138" class="arrow-line" marker-end="url(#arr)" />
  <path d="M 620 111 L 620 138" class="arrow-line" marker-end="url(#arr)" />
  <path d="M 995 111 L 995 125 L 770 125 L 770 138" class="arrow-line" marker-end="url(#arr)" />

  <!-- ================= UCD CONTAINER ================= -->
  <rect x="40" y="215" width="1160" height="1065" class="container-box" />
  <text x="50" y="235" class="title-text">SIKLUS ITERASI USER-CENTERED DESIGN (ISO 9241-210:2019)</text>

  <!-- Panah dari 1D ke UCD -->
  <path d="M 620 176 L 620 250" class="arrow-line" marker-end="url(#arr)" />

  <!-- FASE 1 -->
  <rect x="55" y="250" width="1130" height="145" class="sub-container" />
  <text x="65" y="269" class="title-text" font-size="10">FASE 1: Memahami Konteks Penggunaan (Context of Use)</text>

  <rect x="70" y="280" width="350" height="42" class="node-box" />
  <text x="245" y="306" class="node-desc">Analisis Kondisi Psikologis (Kepanikan saat Krisis) &amp; Akses Seluler</text>

  <rect x="445" y="280" width="350" height="42" class="node-box" />
  <text x="620" y="306" class="node-desc">Perumusan User Persona (Emergency Persona vs Public Persona)</text>

  <rect x="820" y="280" width="350" height="42" class="node-box" />
  <text x="995" y="306" class="node-desc">Identifikasi Karakteristik &amp; Kebutuhan Pengguna</text>

  <rect x="390" y="345" width="460" height="34" class="output-box" />
  <text x="620" y="366" class="node-title">Luaran: Peta Konteks Penggunaan &amp; Task Scenarios</text>

  <path d="M 245 322 L 245 334 L 480 334 L 480 345" class="arrow-line" marker-end="url(#arr)" />
  <path d="M 620 322 L 620 345" class="arrow-line" marker-end="url(#arr)" />
  <path d="M 995 322 L 995 334 L 760 334 L 760 345" class="arrow-line" marker-end="url(#arr)" />

  <!-- Panah Fase 1 ke Fase 2 -->
  <path d="M 620 379 L 620 415" class="arrow-line" marker-end="url(#arr)" />

  <!-- FASE 2 -->
  <rect x="55" y="415" width="1130" height="145" class="sub-container" />
  <text x="65" y="434" class="title-text" font-size="10">FASE 2: Menentukan Kebutuhan Pengguna (Specify User Requirements)</text>

  <rect x="70" y="445" width="350" height="42" class="node-box" />
  <text x="245" y="471" class="node-desc">Perumusan Parameter HCI: Emotional Design, Fitts&#39;s Law, Fluid Navigation</text>

  <rect x="445" y="445" width="350" height="42" class="node-box" />
  <text x="620" y="471" class="node-desc">Klasifikasi Severity Rating Masalah Usabilitas (Skala 0-4)</text>

  <rect x="820" y="445" width="350" height="42" class="node-box" />
  <text x="995" y="471" class="node-desc">Audit Inspeksi 10 Prinsip Heuristik Nielsen pada Website Eksisting</text>

  <rect x="370" y="510" width="500" height="34" class="output-box" />
  <text x="620" y="531" class="node-title">Luaran: Matriks Kebutuhan Pengguna &amp; Dokumen Spesifikasi Desain</text>

  <path d="M 245 487 L 245 499 L 470 499 L 470 510" class="arrow-line" marker-end="url(#arr)" />
  <path d="M 620 487 L 620 510" class="arrow-line" marker-end="url(#arr)" />
  <path d="M 995 487 L 995 499 L 770 499 L 770 510" class="arrow-line" marker-end="url(#arr)" />

  <!-- Panah Fase 2 ke Fase 3 -->
  <path d="M 620 544 L 620 580" class="arrow-line" marker-end="url(#arr)" />

  <!-- FASE 3 -->
  <rect x="55" y="580" width="1130" height="150" class="sub-container" />
  <text x="65" y="599" class="title-text" font-size="10">FASE 3: Merancang Solusi Desain (Produce Design Solutions)</text>

  <rect x="70" y="610" width="260" height="46" class="node-box" />
  <text x="200" y="629" class="node-desc">Purwarupa Interaktif Tinggi Fidelitas</text>
  <text x="200" y="644" class="node-sub">(Figma &amp; Full-Stack Next.js/Tailwind)</text>

  <rect x="350" y="610" width="260" height="46" class="node-box" />
  <text x="480" y="629" class="node-desc">Arsitektur Informasi (IA) Dua-Jalur</text>
  <text x="480" y="644" class="node-sub">&amp; Skematik User Flow</text>

  <rect x="630" y="610" width="260" height="46" class="node-box" />
  <text x="760" y="629" class="node-desc">Perancangan Rendah Fidelitas</text>
  <text x="760" y="644" class="node-sub">Low-Fidelity Wireframe (Sketsa Balsamiq)</text>

  <rect x="910" y="610" width="260" height="46" class="node-box" />
  <text x="1040" y="629" class="node-desc">Sistem Desain &amp; Aksesibilitas WCAG 2.1 AA</text>
  <text x="1040" y="644" class="node-sub">(Primary Navy &amp; Emergency Red)</text>

  <rect x="370" y="680" width="500" height="34" class="output-box" />
  <text x="620" y="701" class="node-title">Luaran: Live Interactive Prototype Web &amp; Cetak Biru Wireframe</text>

  <path d="M 200 656 L 200 668 L 440 668 L 440 680" class="arrow-line" marker-end="url(#arr)" />
  <path d="M 480 656 L 480 668 L 560 668 L 560 680" class="arrow-line" marker-end="url(#arr)" />
  <path d="M 760 656 L 760 668 L 680 668 L 680 680" class="arrow-line" marker-end="url(#arr)" />
  <path d="M 1040 656 L 1040 668 L 800 668 L 800 680" class="arrow-line" marker-end="url(#arr)" />

  <!-- Panah Fase 3 ke Fase 4 -->
  <path d="M 620 714 L 620 750" class="arrow-line" marker-end="url(#arr)" />

  <!-- FASE 4 -->
  <rect x="55" y="750" width="1130" height="150" class="sub-container" />
  <text x="65" y="769" class="title-text" font-size="10">FASE 4: Evaluasi Desain terhadap Kebutuhan (Evaluate Against Requirements)</text>

  <rect x="70" y="780" width="260" height="46" class="node-box" />
  <text x="200" y="799" class="node-desc">Pengukuran Task Completion Time</text>
  <text x="200" y="814" class="node-sub">Penemuan Kontak Darurat (&lt; 3 Detik)</text>

  <rect x="350" y="780" width="260" height="46" class="node-box" />
  <text x="480" y="799" class="node-desc">Pengujian Kuantitatif WebQual 4.0</text>
  <text x="480" y="814" class="node-sub">Komparatif Before vs After (22 Indikator)</text>

  <rect x="630" y="780" width="260" height="46" class="node-box" />
  <text x="760" y="799" class="node-desc">Uji Beda Berpasangan Wilcoxon</text>
  <text x="760" y="814" class="node-sub">Signed-Rank Test (Signifikansi p &lt; 0,001)</text>

  <rect x="910" y="780" width="260" height="46" class="node-box" />
  <text x="1040" y="799" class="node-desc">Audit Aksesibilitas WCAG 2.1 Level AA</text>
  <text x="1040" y="814" class="node-sub">(Uji WAVE &amp; Rasio Kontras)</text>

  <rect x="350" y="850" width="540" height="34" class="output-box" />
  <text x="620" y="871" class="node-title">Luaran: Skor WebQual 4.0, Output Wilcoxon, &amp; Bukti Bebas Galat WAVE</text>

  <path d="M 200 826 L 200 838 L 430 838 L 430 850" class="arrow-line" marker-end="url(#arr)" />
  <path d="M 480 826 L 480 838 L 550 838 L 550 850" class="arrow-line" marker-end="url(#arr)" />
  <path d="M 760 826 L 760 838 L 690 838 L 690 850" class="arrow-line" marker-end="url(#arr)" />
  <path d="M 1040 826 L 1040 838 L 810 838 L 810 850" class="arrow-line" marker-end="url(#arr)" />

  <!-- Panah Fase 4 ke Decision Diamond -->
  <path d="M 620 884 L 620 920" class="arrow-line" marker-end="url(#arr)" />

  <!-- DECISION DIAMOND -->
  <polygon points="620,920 830,975 620,1030 410,975" class="diamond" />
  <text x="620" y="971" class="node-title">Apakah Kriteria Usabilitas &amp; Standar SPM Terpenuhi?</text>
  <text x="620" y="987" class="node-sub">(Skor WebQual &#8805; 4,00 | p &lt; 0,05 | Akses &lt; 3 detik | WCAG 0 Error)</text>

  <!-- Cabang TIDAK -->
  <rect x="840" y="1120" width="240" height="38" class="node-box" />
  <text x="960" y="1144" class="node-desc">Iterasi UCD: Penyesuaian Desain &amp; Fitur</text>

  <path d="M 620 1030 L 620 1075 L 960 1075 L 960 1120" class="arrow-line" marker-end="url(#arr)" />
  <rect x="670" y="1063" width="130" height="18" fill="#ffffff" stroke="#e2e8f0" rx="3" />
  <text x="735" y="1076" class="label-text">TIDAK (Perlu Perbaikan)</text>

  <!-- Feedback Loop ke Fase 3 -->
  <path d="M 1080 1139 L 1150 1139 L 1150 655 L 1185 655" class="arrow-loop" marker-end="url(#arr)" />

  <!-- Cabang YA -->
  <path d="M 620 1030 L 620 1310" class="arrow-line" marker-end="url(#arr)" />
  <rect x="545" y="1235" width="150" height="20" fill="#ffffff" stroke="#e2e8f0" rx="3" />
  <text x="620" y="1249" class="label-text">YA (Memenuhi Kriteria)</text>


  <!-- ================= TAHAP AKHIR ================= -->
  <rect x="40" y="1310" width="1160" height="110" class="container-box" />
  <text x="50" y="1330" class="title-text">TAHAP AKHIR: LUARAN RISET &amp; PUBLIKASI</text>

  <rect x="70" y="1345" width="260" height="46" class="node-box" />
  <text x="200" y="1364" class="node-desc">Matriks Analisis 32 Aspek IMK</text>
  <text x="200" y="1379" class="node-sub">Before &amp; After Terisi Lengkap 100%</text>

  <rect x="350" y="1345" width="260" height="46" class="node-box" />
  <text x="480" y="1364" class="node-desc">Portal Web Redesain Siap Pakai</text>
  <text x="480" y="1379" class="node-sub">(Production Ready di Vercel)</text>

  <rect x="630" y="1345" width="260" height="46" class="node-box" />
  <text x="760" y="1364" class="node-desc">Peningkatan Mutu Terbukti Signifikan</text>
  <text x="760" y="1379" class="node-sub">(+1,94; p &lt; 0,001)</text>

  <rect x="910" y="1345" width="260" height="46" class="node-box" />
  <text x="1040" y="1364" class="node-desc">Naskah Makalah Ilmiah Standar Publikasi</text>
  <text x="1040" y="1379" class="node-sub">Bebas Halusinasi (31 Rujukan APA 7th)</text>

</svg>"""
    return svg


def main():
    # 1. Tulis Draw.io
    drawio_content = build_drawio_xml()
    with open(DRAWIO_FILE, "w", encoding="utf-8") as f:
        f.write(drawio_content)
    print(f"[*] Berhasil menulis berkas Draw.io: {DRAWIO_FILE} ({os.path.getsize(DRAWIO_FILE):,} bytes)")

    # Validasi XML
    try:
        ET.fromstring(drawio_content)
        print("[OK] Validasi XML Draw.io: BERHASIL (Well-formed XML)")
    except ET.ParseError as e:
        print(f"[!] Validasi XML Draw.io GAGAL: {e}")

    # 2. Tulis SVG
    svg_content = build_schematic_svg()
    with open(SVG_FILE, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[*] Berhasil membuat berkas SVG: {SVG_FILE} ({os.path.getsize(SVG_FILE):,} bytes)")

    # 3. Konversi ke PNG
    res = subprocess.run(["convert", SVG_FILE, PNG_FILE], capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(PNG_FILE):
        print(f"[OK] Berhasil mengonversi ke PNG: {PNG_FILE} ({os.path.getsize(PNG_FILE):,} bytes)")
    else:
        print(f"[!] Gagal konversi ke PNG via ImageMagick: {res.stderr}")


if __name__ == "__main__":
    main()
