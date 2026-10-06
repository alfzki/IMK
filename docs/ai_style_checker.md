# Dokumentasi Teknis: Modul Audit Gaya Penulisan AI (AI Writing Style Checker)

Dokumen ini menjelaskan arsitektur, basis aturan, kaidah kebahasaan PUEBI/EYD V, serta panduan pengoperasian modul **AI Writing Style Checker** di lingkungan *calm-carson* Politeknik Statistika STIS.

---

## 1. Latar Belakang & Landasan Taksonomi

Seiring meluasnya penggunaan *Large Language Models* (LLM) seperti ChatGPT, Gemini, Grok, dan DeepSeek, banyak draf naskah ilmiah yang terjangkit pola penulisan artifisial, generalisasi hampa, dan pembesar-besaran signifikansi (*puffery*). 

Komunitas ensiklopedia global telah mengkodifikasi fenomena ini secara komprehensif dalam esai [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup). Modul `calm_carson.style` mengadopsi taksonomi tersebut dan memadukannya dengan kaidah bahasa Indonesia akademik resmi (**PUEBI / EYD V**) serta standar publikasi **IEEE STIS**.

---

## 2. Kategori Pelanggaran Gaya Bahasa

| Kategori | Tingkat Keparahan | Penjelasan & Indikator Pola | Rekomendasi Solusi Akademik |
| :--- | :--- | :--- | :--- |
| **`CHATBOT_LEAK`** | `FATAL` | Sisa artefak/token teknis LLM: `:contentReference[oaicite:...]`, `turn0search0`, `[cite: 1]`, `【1†source】`, `Wikipedia+1`. | Hapus token sistem; ganti dengan sitasi IEEE `[X]` yang terpetakan ke berkas BibTeX lokal. |
| **`CONVERSATIONAL_FILLER`** | `FATAL` | Sapaan ramah khas chatbot: *"Certainly!"*, *"Tentu saja!"*, *"I hope this helps"*, *"Berikut adalah draf..."*, *"Sebagai model AI..."*. | Hapus seluruh kalimat sapaan; mulai langsung dengan pokok masalah atau premis teknis. |
| **`KNOWLEDGE_CUTOFF`** | `FATAL` | Penafian batas waktu pelatihan: *"as of my last update"*, *"hingga batas pengetahuan saya"*, *"informasi terbatas dalam sumber"*. | Gunakan data primer riil atau hasil scraping resmi BPS/jurnal terakreditasi. |
| **`EM_DASH_OVERUSE`** | `HIGH` / `MEDIUM` | **1.** Tanda pisah berspasi (`kata — kata` atau `kata -- kata`).<br>**2.** Kepadatan $\ge 2$ tanda pisah dalam 1 kalimat / $\ge 3$ per paragraf (gaya jurnalisme dramatis/promosi). | **PUEBI/EYD V**: Tulis tanda pisah rapat tanpa spasi (`kata—kata`). Sederhanakan dengan koma (,), tanda kurung untuk aposisi, atau pecah kalimat. |
| **`AI_VOCABULARY`** | `HIGH` / `MEDIUM` | Kata klise berlonjakan statistik pasca-2022: *delve, tapestry, beacon, testament, pivotal, intricate interplay, dynamic landscape, menyelami, rajutan, bukti nyata, memainkan peran penting/krusial, di era modern ini, tidak dapat dipungkiri bahwa*. | Ganti dengan kata kerja operasional dan fungsi sistem yang dapat diukur (misal: *memvalidasi anomali koordinat*, *mengenkripsi data*). |
| **`SUPERFICIAL_ANALYSIS`** | `HIGH` | Buntut partisipel *-ing* / klausa pemanis di akhir kalimat: *", highlighting..."*, *", fostering..."*, *", sehingga menegaskan pentingnya..."* tanpa pembuktian. | Akhiri kalimat pada fakta teknis, atau sertakan data empiris dan metrik pengujian kuantitatif. |
| **`FORMULAIC_CONCLUSION`** | `HIGH` | Pola penutup formulaik: *"Despite these challenges..."*, *"Looking ahead..."*, *"Meskipun menghadapi tantangan..."*, *"Menatap masa depan..."*. | Tulis bab kesimpulan berbasis batasan penelitian dan hasil evaluasi nyata (ISO/IEC 25010, SUS). |
| **`COPULATIVE_AVOIDANCE`** | `MEDIUM` | Menghindari kata kerja kopula lugas (*is/are/adalah*) dengan konstruksi muluk: *serves as a, stands as a, berperan sebagai wujud nyata*. | Gunakan kalimat definisi langsung (*adalah*) atau langsung sebutkan aksi teknis komponennya. |
| **`NEGATIVE_PARALLELISM`** | `MEDIUM` | Kontras semu pengoreksi kesalahpahaman: *not only X, but also Y*, *tidak hanya X, tetapi juga Y* yang diulang-ulang. | Nyatakan karakteristik sistem secara afirmatif dan terukur. |
| **`INLINE_HEADER_LIST`** | `MEDIUM` | Ketergantungan berlebih pada daftar *bullet point* bertajuk tebal (`* **Header**: ...`) alih-alih paragraf analitik berkesinambungan. | Rangkai butir-butir menjadi paragraf narasi dengan konjungsi logika ilmiah yang runtut. |
| **`BURSTINESS_LOW`** | `LOW` / `INFO` | Variansi panjang kalimat sangat rendah (< 0.28). Panjang kalimat monoton ~18–22 kata tanpa dinamika ritme baca. | Padukan kalimat ringkas tegas (8–12 kata) dengan kalimat majemuk terstruktur (20–30 kata). |

---

## 3. Kaidah Tanda Pisah (Em Dash) Berdasarkan PUEBI & EYD V

Dalam bahasa Indonesia, tanda pisah (**—**, Unicode `U+2014`) memiliki kaidah baku:
1. **Tanpa Spasi**: Tanda pisah diapit langsung oleh kata tanpa diselingi spasi sebelum dan sesudahnya:
   - ✅ **Baku**: *Arsitektur microservices—yang dirancang berbasis gRPC—mampu menekan latensi.*
   - ❌ **Cacat AI**: *Arsitektur microservices — yang dirancang berbasis gRPC — mampu menekan latensi.*
   - ❌ **Cacat AI**: *Arsitektur microservices -- yang dirancang berbasis gRPC -- mampu menekan latensi.*
2. **Konteks Akademik**: Tanda pisah dalam karya ilmiah formal STIS hendaknya dibatasi penggunaannya hanya untuk keterangan aposisi khusus. Penggunaan lebih dari satu kali per kalimat mencerminkan gaya penulisan majalah santai atau sales-pitch LLM yang berusaha memaksakan intonasi dramatis.

---

## 4. Arsitektur Komponen Perangkat Lunak

```text
src/calm_carson/style/
├── __init__.py      # Antarmuka publik (AIStyleChecker, check_text_style, StyleReport)
├── models.py        # Data classes: StyleViolation, StyleMetrics, StyleReport, Enum keparahan
├── patterns.py      # Basis data ekspresi reguler dwibahasa (EN & ID) & pesan rekomendasi
├── checker.py       # Mesin utama deteksi, ekstraksi burstiness, & kalkulator skor risiko AI
└── exporter.py      # Visualisator terminal ANSI berwarna, eksportir Markdown & JSON
```

### Formula Skor Risiko AI (0 – 100)
- **Pelanggaran `FATAL`**: Langsung mengunci skor pada rentang $\ge 75$ hingga $100$.
- **Pelanggaran `HIGH`**: $+14$ poin per temuan.
- **Pelanggaran `MEDIUM`**: $+6$ poin per temuan.
- **Pelanggaran `LOW`**: $+2$ poin per temuan.
- **Penalti Kepadatan Klise**: $+15$ poin jika rasio klise $> 1.5\%$ dari total kata.
- **Penalti Em Dash Berspasi / Berlebih**: $+3$ poin per pelanggaran.
- **Penalti Burstiness Monoton**: $+10$ poin jika skor burstiness $< 0.25$.

---

## 5. Panduan Penggunaan CLI (`scripts/check_ai_style.py`)

### A. Mengaudit Berkas Draf Bab
```bash
uv run python scripts/check_ai_style.py --file drafts/topik_1/bab_1_pendahuluan.md --suggest-fixes
```

### B. Mode Verifikasi Ketat (Strict Mode untuk CI / Git Hook)
```bash
uv run python scripts/check_ai_style.py --file drafts/topik_1/bab_1_pendahuluan.md --strict
```
*Akan menghasilkan kode keluar `1` jika terdapat temuan FATAL/HIGH atau skor risiko $\ge 35$.*

### C. Mengaudit Kutipan Kalimat Tertentu
```bash
uv run python scripts/check_ai_style.py --text "Penerapan CAPI memainkan peran krusial dalam lanskap sensus digital — membuktikan komitmen nyata BPS." --suggest-fixes
```

### D. Mengekspor Laporan ke Disk
```bash
uv run python scripts/check_ai_style.py --file drafts/topik_1/bab_1_pendahuluan.md --export
```
Laporan lengkap disimpan ke:
- `drafts/style_reports/<nama_file>_style_report.md`
- `drafts/style_reports/<nama_file>_style_report.json`

---

## 6. Integrasi dengan Alur Kerja Utama (`orchestrate_drafting.py`)

Modul audit gaya penulisan ini telah diintegrasikan langsung pada tahap **Phase 4b** dari `ThesisDraftingPipeline`:
1. Setiap bab yang selesai disintesis oleh `SectionDrafter` dan diverifikasi klaimnya oleh `FactVerifier` akan langsung diaudit gaya bahasanya oleh `AIStyleChecker`.
2. Hasil evaluasi (Skor Risiko, jumlah temuan Fatal/Tinggi/Sedang, em dash, burstiness) ditampilkan langsung pada layar **Human Checkpoint**.
3. Penulis dapat menekan opsi `[5]` di terminal untuk menelaah tabel temuan detail dan draf beranotasi inline sebelum memutuskan menyetujui (`approve`) draf bab tersebut.

---

## 7. Contoh Kasus Perbaikan (Before & After)

### Contoh 1: Latar Belakang CAPI
- ❌ **Draf Terpapar Gaya AI (Skor Risiko: 82/100 - HIGH RISK)**:
  > *"Di era modern ini, pengumpulan data sensus memainkan peran krusial dalam lanskap statistik nasional. Penerapan CAPI berfungsi sebagai wujud nyata modernisasi BPS — sebuah pencapaian yang tidak hanya meningkatkan efisiensi, tetapi juga akuntabilitas, sehingga menegaskan pentingnya transformasi digital berkelanjutan. Meskipun menghadapi berbagai tantangan, masa depan digitalisasi sensus tetap cerah."*
- ✅ **Draf Disunting Akademik Objektif (Skor Risiko: 8/100 - CLEAN)**:
  > *"Berdasarkan evaluasi Sensus Pertanian 2023, pengumpulan data berbasis Computer-Assisted Personal Interviewing (CAPI) berhasil menurunkan durasi pengolahan data mentah dari 90 hari menjadi 21 hari [1]. BPS mengoperasikan sistem validasi aturan logika pada aplikasi CAPI guna memfilter anomali entri data secara waktu nyata. Namun demikian, galat sinkronisasi data offline di daerah 3T masih mencapai 14,2% akibat keterbatasan bandwidth seluler [2]."*
