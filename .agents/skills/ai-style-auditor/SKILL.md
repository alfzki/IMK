---
name: ai-style-auditor
description: Mengaudit draf naskah artikel ilmiah IMK STIS dari tanda-tanda gaya penulisan AI (Wikipedia:Signs_of_AI_writing), mendeteksi klise kosakata dwibahasa, analisis semu gerund, negative parallelism, penggunaan em dash tidak baku, serta kebocoran artefak LLM.
---

# Panduan Keahlian: AI Writing Style Auditor (Wikipedia:Signs_of_AI_writing)

Keahlian ini membekali agen untuk mendeteksi, mengevaluasi, dan menyunting draf naskah artikel ilmiah IMK mahasiswa Politeknik Statistika STIS agar terbebas dari pola klise, gaya bahasa artifisial, dan kebocoran sistem model kecerdasan buatan (*Large Language Models*).

---

## 1. Taksonomi Tanda-Tanda Penulisan AI (Wikipedia Signs)

Pemeriksaan gaya mengacu pada taksonomi formal *WikiProject AI Cleanup* ([Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)):

1. **Chatbot Leaks & System Artifacts** (*Tingkat: FATAL*):
   - Token internal pencarian web ChatGPT: `:contentReference[oaicite:...]`, `[oai_citation:...]`, `turn0search0`, `attributableIndex`, `Wikipedia+1`.
   - Token kutipan Gemini: `[cite: 1]`, `[span_1](start_span)`.
   - Kurung lentikular DeepSeek: `【1†source】`, dagger symbol `†`.
   - Token Grok (`grok_card`) dan Perplexity (`ppl-ai-file-upload`).
2. **Conversational Filler & AI Salutations** (*Tingkat: FATAL*):
   - Sapaan korespondensi: *"Certainly!"*, *"Tentu saja!"*, *"I hope this helps"*, *"Semoga ini membantu"*, *"Here is a breakdown"*, *"Berikut adalah draf"*.
   - Deklarasi AI: *"Sebagai model bahasa AI..."*, *"As an AI..."*.
3. **Knowledge Cutoff Disclaimers** (*Tingkat: FATAL*):
   - *"As of my last knowledge update..."*, *"Hingga batas pembaruan pengetahuan saya..."*, *"Informasi terbatas dalam sumber yang tersedia"*.
4. **AI Vocabulary & Clichés** (*Tingkat: HIGH / MEDIUM*):
   - Bahasa Inggris: *delve, tapestry, beacon, testament, pivotal, intricate interplay, multifaceted, dynamic landscape, evolving realm, underscore, showcase, foster, meticulous, bolster*.
   - Bahasa Indonesia: *menyelami, rajutan/anyaman metaforis, bukti nyata, memainkan peran krusial/penting, dalam lanskap yang dinamis, ranah yang berkembang, di era modern/digital ini, tidak dapat dipungkiri bahwa, perlu dicatat bahwa, secara cermat*.
5. **Em Dash Overuse & Typographic Spacing** (*Tingkat: HIGH / MEDIUM*):
   - Berdasarkan **PUEBI / EYD V**: Tanda pisah (—) ditulis **rapat tanpa spasi** sebelum dan sesudah (`kata—kata`). Penulisan berspasi (`kata — kata` atau `kata -- kata`) adalah cacat tipografi khas keluaran chatbot.
   - Penggunaan lebih dari 1 tanda pisah dalam 1 kalimat atau >2 dalam satu paragraf merupakan dramatisasi gaya promosi yang dilarang dalam naskah ilmiah formal STIS.
6. **Copulative Avoidance** (*Tingkat: MEDIUM*):
   - Mengganti 'adalah/is' dengan konstruksi muluk: *serves as a, stands as a, functions as a, berperan sebagai wujud nyata*.
7. **Negative Parallelisms** (*Tingkat: MEDIUM*):
   - *Not only X, but also Y*, *tidak hanya X, tetapi juga Y* berulang untuk memompa kepentingan semu.
8. **Superficial Analysis Gerunds** (*Tingkat: HIGH*):
   - Menempelkan anak kalimat partisipel pemanis di akhir kalimat: *", highlighting..."*, *", thereby underscoring..."*, *", sehingga menegaskan pentingnya..."* tanpa data pendukung.
9. **Formulaic Conclusions & Outline Headers** (*Tingkat: HIGH*):
   - *"Despite these challenges..."*, *"Looking ahead..."*, *"Meskipun menghadapi berbagai tantangan..."*, *"Menatap masa depan..."*.
10. **Statistical Burstiness** (*Tingkat: INFO / LOW*):
    - Teks AI memiliki variansi panjang kalimat yang sangat rendah (panjang kalimat monoton ~18–22 kata).

---

## 2. Prosedur Eksekusi CLI Perkakas

Jalankan perkakas audit gaya bahasa melalui `uv run`:

### A. Mengaudit Berkas Draf Naskah Makalah IMK
```bash
uv run python scripts/check_ai_style.py --file drafts/MAKALAH_ILMIAH_IMK.md --suggest-fixes
```

### B. Mode Ketat (Strict Mode untuk CI / Verifikasi Akhir)
```bash
uv run python scripts/check_ai_style.py --file drafts/MAKALAH_ILMIAH_IMK.md --strict
```
*Catatan: Mode `--strict` menghasilkan exit code 1 jika ditemukan pelanggaran FATAL/HIGH atau jika skor risiko AI $\ge 35$.*

### C. Mengaudit Kutipan Kalimat Langsung
```bash
uv run python scripts/check_ai_style.py \
  --text "Redesain portal damkar memainkan peran penting dalam lanskap darurat modern — membuktikan komitmen dinas." \
  --suggest-fixes
```

### D. Mengekspor Laporan Evaluasi
```bash
uv run python scripts/check_ai_style.py --file drafts/MAKALAH_ILMIAH_IMK.md --export
```
Laporan Markdown dan JSON akan disimpan di `drafts/style_reports/`.

---

## 3. Protokol Penyuntingan Akademik (Rewriting Rules)

Ketika menemukan temuan pelanggaran gaya bahasa, AI Agent wajib menyunting teks dengan prinsip:
1. **Lugas dan Objektif**: Ganti konstruksi muluk (*serves as a testament*, *memainkan peran krusial*) dengan fungsi konkret (*"menyediakan tombol panggilan darurat 113 persisten"*, *"memvalidasi format isian form pelaporan"*).
2. **Kaidah Tanda Pisah (Em Dash PUEBI)**: Hapus spasi pada tanda pisah, atau gantikan dengan tanda koma (,), tanda kurung untuk keterangan tambahan, atau pisahkan menjadi dua kalimat deklaratif mandiri.
3. **Data-Grounded**: Setiap kali tergoda menambahkan anak kalimat pemanis (*", sehingga menegaskan pentingnya"*), ganti dengan data empiris atau rujukan sitasi ilmiah.
4. **Variasikan Ritme (Tingkatkan Burstiness)**: Padukan kalimat pendek tegas (8–12 kata) dengan kalimat majemuk bertingkat (20–30 kata) untuk menciptakan dinamika baca akademik alami.
