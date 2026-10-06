# Panduan Sistem: Kapabilitas Verifikasi Keabsahan Faktual & Sub-Agen Claim Verifier

Dokumen ini memuat arsitektur teknis, metodologi verifikasi keabsahan data kuantitatif, aturan validasi sitasi, panduan antarmuka perintah CLI, dan panduan penggunaan sub-agen `claim_verifier` untuk mengaudit setiap draf tulisan sebelum teks disetujui masuk ke dalam dokumen proposal maupun skripsi akhir mahasiswa Sistem Informasi Statistik (SIS) Politeknik Statistika STIS.

---

## 1. Arsitektur Pipeline Verifikasi Faktual

Sistem mengintegrasikan pembedahan klaim berbasis linguistik, penelusuran bukti pada korpus lokal menggunakan hybrid retrieval (Dense CUDA MiniLM + Sparse BM25Okapi), evaluasi keselarasan logika, dan penandaan anotasi inline:

```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                     DRAF PARAGRAF / TEKS USULAN PROPOSAL                         │
│  (Contoh: "Pada Sensus Pertanian 2023, BPS merekrut sekitar 190.000 petugas      │
│   lapangan [1]. Namun hanya 50.000 petugas yang aktif. Nilai IPS adalah 1,48.") │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                      CLAIM DECOMPOSER (decomposer.py)                            │
│  1. Sentence Boundary Detection: Pembagi kalimat kebal singkatan (dkk., et al.) │
│  2. Numerical Quantity Extractor: Ekstraksi angka ribuan, desimal, persentase    │
│  3. Citation Marker Extractor: Ekstraksi penanda sitasi standar IEEE [1], [2]    │
│  4. Claim Normalization: Pembersihan tanda kurung & sitasi untuk pencarian teks │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                      EVIDENCE MATCHER (matcher.py)                               │
│  1. Hybrid Search Retrieval: Mengkueri MarkdownHybridSearchEngine (BM25 + Dense) │
│  2. Number Token Boosting: Menyuntikkan token angka ke kueri penelusuran         │
│  3. Candidate Passage Ranking: Mengambil top-k potongan teks bukti korpus        │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                       FACT VERIFIER (verifier.py)                                │
│  1. Semantic Similarity: Cosine similarity via SentenceTransformer (GPU FP16)   │
│  2. Numeric Contradiction Engine: Pembedaan tahun kalender vs angka statistik   │
│  3. Alignment Classification: SUPPORTED, CONTRADICTED, atau UNSUPPORTED          │
│  4. Citation Audit: Memvalidasi kecocokan nomor sitasi (VALID/MISSING/MISMATCH)  │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
┌──────────────────────────────────────┐  ┌────────────────────────────────────────┐
│     INLINE ANNOTATOR (annotator.py)  │  │     EXPORTER & SUB-AGEN                │
│  - [✓ TERVERIFIKASI: file:line]      │  │  - JSON: literature/fact_check_*.json  │
│  - [⚠️ KONTRADIKSI: alasan]          │  │  - MD: brainstorming/laporan_verifikasi│
│  - [💡 PERLU SITASI: tambahkan [X]] │  │  - CLI: scripts/verify_claims.py      │
│  - [❓ TIDAK BERDASAR: kemiripan %]  │  │  - Sub-agen: 'claim_verifier'          │
└──────────────────────────────────────┘  └────────────────────────────────────────┘
```

---

## 2. Taksonomi Status Verifikasi & Logika Penilaian

Sistem menetapkan status keabsahan secara deterministik dan transparan untuk setiap klaim individual:

### A. Status Keselarasan Logika (*Factual Alignment*)
1. 🟢 **SUPPORTED (Didukung Penuh)**:
   - Skor kemiripan semantik terhadap bukti korpus $\ge 0,40$.
   - Tidak ada pertentangan angka statistik.
   - Fakta divalidasi oleh dokumen resmi di korpus (misalnya: `proposals/bank_data_masalah_proposal.md` atau `proposals/proposal_topik_*.md`).
2. 🔴 **CONTRADICTED (Bertentangan)**:
   - Teks klaim berbagi konteks entitas yang kuat (irisan kata kunci $\ge 3$), namun menyajikan angka statistik yang berbeda langsung dengan angka pada bukti korpus (misalnya: draf menulis *50.000 petugas*, korpus mencatat *190.000 petugas*).
   - Kalender tahun (1950–2050) dibedakan secara terpisah dari metrik kuantitas agar tahun kegiatan tidak membatalkan deteksi konflik angka.
3. ❓ **UNSUPPORTED (Tidak Berdasar / Kurang Rujukan)**:
   - Skor kemiripan semantik $< 0,40$ atau tidak ditemukan bagian teks yang relevan di seluruh korpus lokal.
   - Menandakan klaim berupa spekulasi pribadi, opini tanpa dasar, atau data yang belum terdokumentasi di repositori.

### B. Status Validitas Sitasi (*Citation Integrity*)
1. ✓ **VALID**:
   - Kalimat klaim menyertakan penanda sitasi IEEE (misal `[1]`), dan penanda tersebut sesuai dengan nomor sitasi pada bukti korpus.
2. 💡 **MISSING**:
   - Kalimat klaim didukung penuh oleh bukti di korpus, namun belum memiliki penanda sitasi. Sistem memberikan rekomendasi nomor sitasi yang wajib ditambahkan (misal `[1]`).
3. ⚠️ **MISMATCH**:
   - Klaim menyertakan penanda sitasi, tetapi nomor sitasi berbeda dari rujukan resmi yang tercatat pada bagian bukti korpus.

---

## 3. Format Penanda Anotasi Inline

Setelah proses audit selesai, draf tulisan akan diperkaya dengan tag penanda inline:

| Tag Anotasi | Kondisi Pemicu | Contoh Visual |
| :--- | :--- | :--- |
| `[✓ TERVERIFIKASI: file:line]` | Klaim didukung penuh dan memiliki sitasi valid | `BPS merekrut sekitar 190.000 petugas lapangan [1]. [✓ TERVERIFIKASI: proposals/proposal_topik_1_survey_fraud.md:L26]` |
| `[⚠️ KONTRADIKSI: alasan]` | Terjadi pertentangan angka atau data kuantitatif | `Hanya 50.000 petugas yang tercatat aktif. [⚠️ KONTRADIKSI: klaim menyebut 50.000, sedangkan korpus mencatat 190.000 (lihat proposal_topik_1_survey_fraud.md:L26)]` |
| `[💡 PERLU SITASI: tambahkan [X]]` | Fakta didukung bukti, namun belum diberi nomor rujukan | `Nilai rata-rata IPS nasional adalah 1,48. [💡 PERLU SITASI: didukung di bank_data_masalah_proposal.md:L47, tambahkan [1]]` |
| `[❓ TIDAK BERDASAR]` | Klaim tidak ditemukan rujukannya di korpus lokal | `Alien mendarat di kantor BPS pada 2023. [❓ TIDAK BERDASAR: belum ada rujukan di korpus]` |

---

## 4. Panduan CLI (`scripts/verify_claims.py`)

Perkakas CLI `scripts/verify_claims.py` dapat dijalankan secara langsung untuk memverifikasi teks string ataupun berkas Markdown:

### A. Memverifikasi Teks Langsung
```bash
uv run python scripts/verify_claims.py --text "Pada Sensus Pertanian 2023, BPS merekrut sekitar 190.000 petugas lapangan [1]. Namun hanya 50.000 petugas yang tercatat aktif. Nilai indeks pembangunan statistik nasional tergolong rendah." --export
```

### B. Memverifikasi Berkas Proposal Markdown
```bash
uv run python scripts/verify_claims.py --file proposals/proposal_topik_1_survey_fraud.md
```

### C. Menampilkan Hanya Draf Beranotasi Inline
Opsi ini sangat berguna saat menyalin teks yang sudah diberi catatan koreksi langsung ke editor draf:
```bash
uv run python scripts/verify_claims.py --text "..." --annotated-only
```

### D. Mode Proteksi Ketat (Strict CI/CD Gate)
Flag `--strict` menyebabkan CLI mengembalikan exit code `1` apabila ditemukan kontradiksi data faktual. Opsi ini dapat digunakan sebagai gate otomatis sebelum draf naskah digabungkan ke dokumen final:
```bash
uv run python scripts/verify_claims.py --file proposals/proposal_topik_2_sdi_gateway.md --strict
```

---

## 5. Sub-Agen Interaktif: `claim_verifier`

Sub-agen `claim_verifier` bertindak sebagai editor akademik independen (*Academic Fact-Checking Sparring Partner*) yang bertugas menjaga integritas naskah skripsi:

### Mandat & Tanggung Jawab Sub-Agen:
1. **Pembedahan Klaim**: Membedah setiap paragraf draf menjadi proposisi faktual atomik.
2. **Pencarian Bukti Mandiri**: Menelusuri potongan teks bukti di `literature/markdowns/`, `proposals/`, dan `brainstorming/` melalui hybrid search.
3. **Pengujian Kuantitatif**: Mengecek angka riil (persentase, populasi sampel, skor indeks, nilai $p$-value).
4. **Verifikasi Sitasi**: Memastikan setiap angka kuantitatif memiliki nomor sitasi IEEE yang terhubung ke dokumen referensi resmi.
5. **Pencegahan Halusinasi**: Menolak tegas kalimat klaim yang tidak berdasar atau bertentangan sebelum disetujui masuk ke dalam dokumen proposal.

---

## 6. Lokasi Berkas & Struktur Output

- **Pustaka Logika Verifikasi**: `src/calm_carson/verify/`
  - `models.py`: Data model (`FactClaim`, `EvidenceMatch`, `ClaimVerificationResult`, `VerificationReport`).
  - `decomposer.py`: Pembedah kalimat, ekstraktor angka kuantitatif, dan sitasi.
  - `matcher.py`: Pengambil bukti korpus via `MarkdownHybridSearchEngine`.
  - `verifier.py`: Evaluator keselarasan logika, pendeteksi kontradiksi angka, dan validator sitasi.
  - `annotator.py`: Penyusun draf teks beranotasi inline.
  - `exporter.py`: Generator laporan JSON dan Markdown.
- **Skrip CLI**: `scripts/verify_claims.py`
- **Unit Test Suite**: `tests/test_verifier.py` (6 tes unit terotomasi)
- **Laporan Audit Terstruktur**:
  - Format JSON: `literature/fact_check_<slug>.json`
  - Format Markdown: `brainstorming/laporan_verifikasi_<slug>.md`
