# Panduan Sistem: Kapabilitas Penguji Orisinalitas Topik & Sub-Agen Originality Checker

Dokumen ini memuat arsitektur teknis, metodologi komputasi kemiripan semantik, panduan CLI, dan panduan penggunaan sub-agen `originality_checker` untuk menguji orisinalitas serta kebaruan (*novelty*) draf ide skripsi mahasiswa Sistem Informasi Statistik (SIS) Politeknik Statistika STIS terhadap lanskap literatur ilmiah global.

---

## 1. Arsitektur Pipeline Pengujian Orisinalitas

Sistem menggabungkan penelusuran publikasi ilmiah internasional terakreditasi, model representasi vektor multibahasa pada GPU NVIDIA RTX 4050, dan generator masukan kritis berbasis DSRM:

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   DRAF IDE SKRIPSI / RUMUSAN MASALAH MAHASISWA                  │
│  (Bahasa Indonesia atau Inggris, misal: "Rancang Bangun Secure Microdata Query   │
│   Engine dengan Penerapan Differential Privacy dan Cryptographic Audit Trail")   │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                    GLOBAL LITERATURE SEARCHER (searcher.py)                      │
│  1. Bilingual Concept Mapping: Penerjemahan istilah lokal ke terminologi global │
│  2. OpenAlex API Querying: Menelusuri publikasi Scopus/IEEE/ACM (>= 2021)       │
│  3. Local STIS Theses Cross-Check: Memeriksa database 389 skripsi alumni STIS   │
│  4. Abstract Inverted Index Reconstructor: Rekonstruksi teks abstrak utuh       │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                     ORIGINALITY EVALUATOR (evaluator.py)                         │
│  1. Multilingual Dense Embeddings: MiniLM-L12-v2 (FP16 PyTorch CUDA RTX 4050)   │
│  2. Cosine Similarity Computation: Operasi dot-product matriks L2-normalized    │
│  3. Overlap Risk Classification: High (>=70%), Moderate (45-69%), Low (<45%)    │
│  4. Differentiation Engine: Merumuskan 5 dimensi pembeda kebaruan               │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
┌──────────────────────────────────────┐  ┌────────────────────────────────────────┐
│     STRUKTUR DATA & LAPORAN EKSPOR   │  │       SUB-AGEN INTERAKTIF              │
│  - literature/originality_eval_*.json│  │   'originality_checker'                │
│  - brainstorming/laporan_orisinalitas│  │  - Critical Academic Reviewer          │
│  - CLI: scripts/check_originality.py │  │  - Evaluasi gap & reposisi ide riset   │
└──────────────────────────────────────┘  └────────────────────────────────────────┘
```

---

## 2. Metrik Kemiripan & Klasifikasi Risiko Tumpang Tindih

Tingkat kemiripan dihitung menggunakan kemiripan kosinus antara vektor embedding ide penelitian ($\vec{u}$) dan vektor representasi publikasi pembanding ($\vec{p}$):

$$\text{Similarity}(\vec{u}, \vec{p}) = \frac{\vec{u} \cdot \vec{p}}{\|\vec{u}\|_2 \|\vec{p}\|_2} = \vec{u} \cdot \vec{p} \quad (\text{vektor ternormalisasi } L_2)$$

### Tingkat Kemiripan per Publikasi (*Overlap Level*):
- 🔴 **HIGH OVERLAP** ($\text{Sim} \ge 70\%$): Tumpang tindih tema dan metode secara langsung; berisiko tinggi dianggap menduplikasi penelitian terdahulu jika tidak memiliki aspek pembeda yang kuat.
- 🟡 **MODERATE OVERLAP** ($45\% \le \text{Sim} < 70\%$): Irisan konsep dalam satu bidang minat; sangat baik dijadikan *paper benchmark* pada **Tabel I (Kontribusi Penelitian)** proposal skripsi.
- 🟢 **LOW OVERLAP** ($\text{Sim} < 45\%$): Kemiripan rendah; ide memiliki diferensiasi yang tinggi terhadap publikasi pembanding.

### Status Risiko Keseluruhan (*Overall Risk*):
- **HIGH_OVERLAP**: Ditetapkan jika kemiripan tertinggi $\ge 75\%$ atau terdapat minimal 2 paper dengan kemiripan $\ge 70\%$. Mahasiswa wajib mereposisi arsitektur atau fokus masalah.
- **MODERATE_OVERLAP**: Ditetapkan jika kemiripan tertinggi $\ge 50\%$. Mahasiswa disarankan mempertegas novelty pada karakteristik data BPS dan kepatuhan regulasi nasional.
- **DISTINCT_NOVEL**: Ditetapkan jika kemiripan tertinggi $< 50\%$. Ide dinilai memiliki orisinalitas tinggi.

---

## 3. Lima Dimensi Penguatan Kebaruan (*Differentiation Dimensions*)

Sistem merumuskan rekomendasi konkret pada 5 pilar strategis:

1. **Metodologi & Arsitektur Algoritma**:
   - Mentransformasi proses batch statis offline ke arsitektur *real-time streaming* atau *on-demand query*.
   - Menerapkan mekanisme privasi matematis formal (Laplace/Gaussian mechanism dengan dynamic privacy budget tracking) atau deteksi berbasis sekuens waktu (*dwell-time*).
2. **Spesifisitas & Kompleksitas Data Statistik Resmi (BPS)**:
   - Menyesuaikan arsitektur dengan hierarki bertingkat data survei/sensus BPS (blok sensus, rumah tangga, individu) dan kode standar klasifikasi nasional (KBLI/KBKI).
   - Memperhitungkan keterbatasan jaringan lapangan (*offline-first CAPI mobile*).
3. **Rekayasa Perangkat Lunak & Artefak Sistem (DSRM)**:
   - Memastikan terwujudnya artefak perangkat lunak utuh yang dapat didemonstrasikan saat sidang (bukan sekadar eksperimen notebook analitis).
   - Menambahkan fitur enterprise: *tamper-evident cryptographic audit trail* (hash chaining SHA-256), *zero-trust gateway*, dan *mTLS*.
4. **Kepatuhan Regulasi Nasional**:
   - Memetakan batasan sistem langsung ke klausul kewajiban UU No. 27 Tahun 2022 (UU PDP), Perpres No. 39 Tahun 2019 (Satu Data Indonesia), atau kerangka SPBE.
5. **Standar Pengujian Mutu Perangkat Lunak (ISO/IEC 25010)**:
   - Menyusun evaluasi multi-aspek: Functional Suitability, Usability (SUS/UEQ), Performance Efficiency, dan Security (VAPT OWASP API Top 10).

---

## 4. Penggunaan Antarmuka Baris Perintah (CLI Runner)

Skrip [`scripts/check_originality.py`](file:///home/alfzki/Documents/antigravity/calm-carson/scripts/check_originality.py) dapat dieksekusi langsung di terminal:

### A. Menguji Ide Langsung via Argumen String
```bash
uv run python scripts/check_originality.py \
  --idea "Rancang Bangun Secure On-Demand Microdata Query Engine dengan Penerapan Differential Privacy dan Cryptographic Audit Trail Berbasis API" \
  --export
```

### B. Menguji Ide dari Berkas Proposal Markdown
```bash
uv run python scripts/check_originality.py \
  --file proposals/proposal_topik_1_survey_fraud.md \
  --export
```

### C. Menentukan Batas Tahun Publikasi Global
```bash
uv run python scripts/check_originality.py \
  --idea "Deteksi Anomali Paradatak Entri Survei CAPI" \
  --min-year 2022 \
  --limit 8
```

---

## 5. Penggunaan Sub-Agen `originality_checker`

Sub-agen `originality_checker` dapat dipanggil kapan saja menggunakan tool `invoke_subagent` untuk melakukan review kritis:

### Contoh Pemanggilan Sub-Agen:
```python
invoke_subagent(
    Subagents=[{
        "TypeName": "originality_checker",
        "Role": "Critical Academic Reviewer",
        "Prompt": (
            "Saya memiliki ide skripsi: 'Pembangunan API Gateway Satu Data Indonesia dengan Zero-Trust "
            "Architecture dan Validasi Metadata SIMETRIS Otomatis'. "
            "Uji orisinalitas ide ini terhadap literatur global, identifikasi paper yang paling mirip, "
            "dan berikan masukan pembeda agar novelty penelitian saya kuat saat diajukan ke dosen pembimbing."
        )
    }]
)
```

---

## 6. Penggunaan via Python API

```python
from calm_carson.originality import check_topic_originality

report = check_topic_originality(
    idea_text="Penerapan differential privacy pada agregasi data mikro sensus",
    min_year=2021,
    export_files=True,
)

print(f"Status Risiko : {report.overall_risk}")
print(f"Max Kemiripan : {report.max_similarity * 100:.1f}%")
for fb in report.differentiation_feedbacks:
    print(f"- {fb.dimension_name}: {fb.recommended_differentiation}")
```

---

## 7. Pengujian Unit

Test suite otomatis tersedia di [`tests/test_originality.py`](file:///home/alfzki/Documents/antigravity/calm-carson/tests/test_originality.py):

```bash
uv run python -m unittest tests/test_originality.py
```
Memvalidasi fungsionalitas model dataclass, ekstraksi kueri dwibahasa, skoring kemiripan semantik, dan keabsahan luaran ekspor JSON/Markdown.
