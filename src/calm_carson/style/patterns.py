"""
Pattern definitions for AI Writing Style Checker.
Kompilasi ekspresi reguler dan basis data pola gaya penulisan AI dwibahasa (Inggris & Indonesia).
Mengacu pada taksonomi Wikipedia:Signs_of_AI_writing dan kaidah tata bahasa akademik (PUEBI/EYD V & IEEE).
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Pattern, Tuple
from calm_carson.style.models import StyleSeverity, StyleViolationType


# ==============================================================================
# 1. CHATBOT LEAKS & INTERNAL SYSTEM TOKENS (FATAL)
# ==============================================================================

CHATBOT_LEAK_PATTERNS: List[Tuple[str, Pattern, str, str]] = [
    (
        "chatgpt_oaicite_bracket",
        re.compile(r":contentReference\[oaicite:\d+\](?:\{index=\d+\})?", re.IGNORECASE),
        "Tag kebocoran kutipan internal ChatGPT (:contentReference[oaicite:...]). Teks disalin langsung dari antarmuka LLM.",
        "Hapus tag dan ganti dengan nomor sitasi resmi IEEE [X] atau rujukan primer.",
    ),
    (
        "chatgpt_oai_citation_link",
        re.compile(r"\[oai_citation:\d+[^\]]*\]\([^)]+\)", re.IGNORECASE),
        "Format tautan sitasi khas ChatGPT RAG web-search ([oai_citation:...](url)).",
        "Ganti tautan dengan format rujukan ilmiah IEEE [X] yang terdaftar di berkas BibTeX.",
    ),
    (
        "chatgpt_turn_search",
        re.compile(r"(?:cite)?turn\d+search\d+(?:)?", re.IGNORECASE),
        "Token pencarian web internal ChatGPT (turn0search0 / PUA Unicode).",
        "Hapus token internal dan masukkan sitasi literatur yang valid.",
    ),
    (
        "chatgpt_attributable_index",
        re.compile(r"attributableIndex", re.IGNORECASE),
        "Parameter internal penelusuran ChatGPT (attributableIndex).",
        "Hapus parameter dan periksa integritas teks draf.",
    ),
    (
        "chatgpt_plus_integer_citation",
        re.compile(r"\b[A-Z][a-zA-Z0-9\s]{2,20}\+\d+\b"),
        "Sisa artefak sitasi ChatGPT pencarian web (misal: 'Wikipedia+1', 'Google+3').",
        "Hapus token dan gunakan sitasi standar IEEE [X].",
    ),
    (
        "gemini_cite_token",
        re.compile(r"\[cite:\s*\d+\]", re.IGNORECASE),
        "Penanda kutipan internal antarmuka Google Gemini ([cite: 1]).",
        "Ganti penanda kutipan dengan sitasi IEEE [X] atau rujukan bibliografi lokal.",
    ),
    (
        "gemini_span_token",
        re.compile(r"\[span_\d+\]\(start_span\)", re.IGNORECASE),
        "Token penanda span sumber internal Google Gemini.",
        "Hapus token internal Gemini dari naskah.",
    ),
    (
        "deepseek_lenticular_brackets",
        re.compile(r"【\d+(?::\d+)?†[^】]*】"),
        "Tanda kurung lentikular penanda sitasi internal DeepSeek (【1†source】).",
        "Hapus kurung lentikular dan petakan ke referensi IEEE standar.",
    ),
    (
        "grok_card_leak",
        re.compile(r"grok_(?:card|render_citation_card_json)", re.IGNORECASE),
        "Artefak komponen UI sitasi Grok.",
        "Hapus artefak komponen UI dari teks draf.",
    ),
    (
        "perplexity_file_upload_leak",
        re.compile(r"(?:ppl-ai-file-upload|attached_file:\d+)", re.IGNORECASE),
        "Penanda berkas unggahan internal Perplexity AI.",
        "Hapus token internal Perplexity.",
    ),
]


# ==============================================================================
# 2. CONVERSATIONAL FILLER & AI GREETINGS (FATAL / HIGH)
# ==============================================================================

CONVERSATIONAL_PATTERNS: List[Tuple[str, Pattern, str, str, StyleSeverity]] = [
    (
        "conversational_salutation_id",
        re.compile(r"\b(?:Tentu saja!|Tentu,|Semoga ini membantu|Jangan ragu untuk bertanya|Berikut adalah draf|Draf ini menyajikan informasi yang Anda minta)\b", re.IGNORECASE),
        "Kalimat sapaan/korespondensi khas chatbot AI yang tidak boleh ada pada naskah ilmiah formal.",
        "Hapus sapaan chatbot dan mulai langsung dengan argumen ilmiah formal.",
        StyleSeverity.FATAL,
    ),
    (
        "conversational_salutation_en",
        re.compile(r"\b(?:Certainly!|Of course!|I hope this helps|Feel free to ask|Here is a breakdown|As requested,|In this response,)\b", re.IGNORECASE),
        "Chatbot conversational correspondence leak inappropriate for academic publishing.",
        "Remove conversational pleasantries and state technical facts directly.",
        StyleSeverity.FATAL,
    ),
    (
        "meta_ai_identity",
        re.compile(r"\b(?:sebagai model bahasa (?:ai|kecerdasan buatan)|as an ai language model|as an ai developed by)\b", re.IGNORECASE),
        "Deklarasi identitas LLM dalam teks tulisan.",
        "Hapus seluruh kalimat deklarasi AI.",
        StyleSeverity.FATAL,
    ),
    (
        "didactic_intro_clause",
        re.compile(r"\b(?:dalam bagian ini, (?:kita|penulis|kami) akan membahas secara komprehensif|in this section,? we will (?:delve into|explore|provide a comprehensive))\b", re.IGNORECASE),
        "Pengantar didaktis berlebihan khas penjelasan chatbot (mengumumkan apa yang akan ditulis alih-alih langsung menyajikan fakta).",
        "Hapus pengantar bertele-tele dan langsung kemukakan premis atau data penelitian.",
        StyleSeverity.HIGH,
    ),
]


# ==============================================================================
# 3. KNOWLEDGE-CUTOFF DISCLAIMERS & VAGUE SOURCE SPECULATION (FATAL / HIGH)
# ==============================================================================

KNOWLEDGE_CUTOFF_PATTERNS: List[Tuple[str, Pattern, str, str]] = [
    (
        "knowledge_cutoff_en",
        re.compile(r"\b(?:as of my (?:last )?(?:knowledge|training) (?:update|cutoff)|up to my last update)\b", re.IGNORECASE),
        "Penafian batas waktu data pelatihan chatbot (knowledge cutoff disclaimer).",
        "Hapus penafian dan gunakan rujukan data riil terkini dengan sitasi eksplisit.",
    ),
    (
        "knowledge_cutoff_id",
        re.compile(r"\b(?:hingga batas pembaruan pengetahuan saya|berdasarkan data yang tersedia hingga)\b", re.IGNORECASE),
        "Penafian batas data pengetahuan LLM.",
        "Gunakan data empiris riil bersumber literatur/statistik resmi.",
    ),
    (
        "unavailability_speculation",
        re.compile(r"\b(?:while specific details are (?:limited|scarce)|informasi spesifik mengenai hal ini terbatas dalam sumber yang tersedia|not widely documented in the provided sources)\b", re.IGNORECASE),
        "Spekulasi khas RAG saat tidak menemukan sumber, lalu berdalih bahwa informasi terbatas.",
        "Cari rujukan primer atau hapus klaim spekulatif jika data memang belum diverifikasi.",
    ),
]


# ==============================================================================
# 4. EM DASH OVERUSE & UNGRAMMATICAL SPACING (HIGH / MEDIUM)
# ==============================================================================

# Berdasarkan PUEBI / EYD V:
# Tanda pisah (—) ditulis TANPA SPASI sebelum dan sesudah (misal: "sistem—yang baru saja diluncurkan—beroperasi").
# Penggunaan berspasi ("sistem — yang baru saja — beroperasi") adalah kesalahan tipografi yang sering diproduksi LLM.
# Selain itu, penggunaan berulang dalam satu paragraf menciptakan efek dramatisasi gaya penjualan / pop-science.

SPACED_EM_DASH_PATTERN = re.compile(r"[^\s]+\s+[—–]\s+[^\s]+")
DOUBLE_HYPHEN_PATTERN = re.compile(r"[^\s]+\s+--\s+[^\s]+")


# ==============================================================================
# 5. AI VOCABULARY & TELLS (HIGH / MEDIUM)
# ==============================================================================

# Kata dan frasa klise yang terbukti secara statistik mengalami lonjakan tajam pasca-2022
AI_VOCABULARY_EN: Dict[str, Dict[str, str]] = {
    "delve": {
        "rule": "delve_into",
        "severity": "HIGH",
        "explanation": "Kata 'delve' merupakan penanda paling terkenal dari teks LLM pasca-2022.",
        "fix": "Ganti dengan 'examine', 'investigate', 'analyze', atau 'explore' yang lebih spesifik.",
    },
    "tapestry": {
        "rule": "abstract_tapestry",
        "severity": "HIGH",
        "explanation": "Penggunaan metaforis 'tapestry' (e.g. 'rich tapestry') adalah klise sastra khas LLM.",
        "fix": "Sebutkan komponen riil sistem atau fenomena secara harfiah dan spesifik.",
    },
    "beacon": {
        "rule": "beacon_of",
        "severity": "HIGH",
        "explanation": "Frasa kiasan 'beacon of...' berlebihan dan bernada promosi (puffery).",
        "fix": "Ganti dengan dampak teknis atau fungsi sistem yang dapat diukur.",
    },
    "testament": {
        "rule": "serves_as_testament",
        "severity": "HIGH",
        "explanation": "Frasa 'serves as a testament to' membesar-besarkan signifikansi secara subjektif.",
        "fix": "Sajikan data kuantitatif atau bukti empiris langsung yang mendukung klaim.",
    },
    "pivotal": {
        "rule": "pivotal_role",
        "severity": "MEDIUM",
        "explanation": "Kata 'pivotal' sering diobral LLM untuk memompa kepentingan tanpa bukti angka.",
        "fix": "Ganti dengan kontribusi teknis spesifik atau metrik terukur.",
    },
    "interplay": {
        "rule": "intricate_interplay",
        "severity": "MEDIUM",
        "explanation": "Frasa 'intricate interplay' merupakan filler abstrak yang menghindari penjelasan mekanisme.",
        "fix": "Jelaskan mekanisme interaksi atau alur data secara teknis antar-komponen.",
    },
    "multifaceted": {
        "rule": "multifaceted_nature",
        "severity": "MEDIUM",
        "explanation": "Kata 'multifaceted' sering dipakai LLM untuk tampak mendalam tanpa merinci aspeknya.",
        "fix": "Uraikan aspek-aspek teknis secara eksplisit dalam kalimat.",
    },
    "dynamic landscape": {
        "rule": "dynamic_landscape",
        "severity": "HIGH",
        "explanation": "Metafora 'in this dynamic landscape' adalah klise pengisi kalimat pembuka AI.",
        "fix": "Ganti dengan konteks lingkungan komputasi riil (e.g. 'dalam infrastruktur data BPS').",
    },
    "evolving realm": {
        "rule": "evolving_realm",
        "severity": "HIGH",
        "explanation": "Metafora 'in the evolving realm of' adalah klise pembuka paragraf AI.",
        "fix": "Sebutkan bidang keilmuan atau arsitektur sistem secara presisi.",
    },
    "underscore": {
        "rule": "underscore_importance",
        "severity": "MEDIUM",
        "explanation": "Penggunaan figuratif 'underscores the need/importance' sangat padat pada output GPT.",
        "fix": "Gunakan kata kerja lugas: 'menunjukkan', 'mengindikasikan', atau tampilkan datanya.",
    },
    "showcase": {
        "rule": "showcasing",
        "severity": "MEDIUM",
        "explanation": "Kata 'showcase' / 'showcasing' bernada presentasi pameran alih-alih evaluasi saintifik.",
        "fix": "Ganti dengan 'demonstrate', 'evaluate', atau 'measure'.",
    },
    "foster": {
        "rule": "fostering",
        "severity": "MEDIUM",
        "explanation": "Kata 'foster' / 'fostering' diobral untuk memberikan kesan positif tanpa kejelasan proses.",
        "fix": "Gunakan 'mengembangkan', 'membangun', atau jelaskan metode pembentukannya.",
    },
    "meticulous": {
        "rule": "meticulously",
        "severity": "MEDIUM",
        "explanation": "Pujian 'meticulous' / 'meticulously designed' bersifat subjektif dan klise.",
        "fix": "Jelaskan prosedur validasi atau pengujian yang dilakukan secara objektif.",
    },
    "bolster": {
        "rule": "bolstering",
        "severity": "MEDIUM",
        "explanation": "Kata 'bolster' adalah kata favorit LLM era GPT-4.",
        "fix": "Ganti dengan kata kerja teknis yang terukur (e.g. 'meningkatkan akurasi sebesar X%').",
    },
    "crucial": {
        "rule": "crucial_role",
        "severity": "LOW",
        "explanation": "Kata 'crucial' sering digunakan berulang kali sebagai kata sifat penguat emosional.",
        "fix": "Sebutkan konsekuensi teknis jika hal tersebut tidak dipenuhi.",
    },
}

AI_VOCABULARY_ID: Dict[str, Dict[str, str]] = {
    "menyelami": {
        "rule": "id_menyelami",
        "severity": "HIGH",
        "explanation": "Kata 'menyelami' adalah terjemahan harfiah klise dari 'delve into' dalam naskah akademik.",
        "fix": "Ganti dengan kata kerja penelitian lugas: 'mengkaji', 'menganalisis', atau 'menyelidiki'.",
    },
    "rajutan": {
        "rule": "id_rajutan_metafora",
        "severity": "HIGH",
        "explanation": "Metafora 'rajutan...' (terjemahan 'tapestry') adalah klise sastrawi yang tidak tepat di SIS.",
        "fix": "Ganti dengan penyebutan komponen arsitektur atau relasi data secara konkret.",
    },
    "anyaman": {
        "rule": "id_anyaman_metafora",
        "severity": "HIGH",
        "explanation": "Metafora 'anyaman kompleks...' merupakan variasi puitis khas terjemahan LLM.",
        "fix": "Sebutkan struktur hubungan antar-variabel atau entitas secara teknis.",
    },
    "bukti nyata": {
        "rule": "id_bukti_nyata",
        "severity": "HIGH",
        "explanation": "Frasa 'menjadi bukti nyata dari' (terjemahan 'serves as a testament to') hiperbolis.",
        "fix": "Sajikan data empiris atau hasil pengujian langsung tanpa klaim emosional.",
    },
    "memainkan peran krusial": {
        "rule": "id_peran_krusial",
        "severity": "HIGH",
        "explanation": "Frasa 'memainkan peran krusial/penting' adalah filler klise yang tidak memberikan informasi substansi.",
        "fix": "Jelaskan fungsi teknis spesifik komponen (misal: 'memvalidasi anomali koordinat GPS').",
    },
    "memainkan peran penting": {
        "rule": "id_peran_penting",
        "severity": "HIGH",
        "explanation": "Frasa 'memainkan peran penting' merupakan klise umum AI yang menghindari penjelasan fungsi.",
        "fix": "Ganti dengan fungsi sistem konkret (misal: 'memfilter galat entri data sensus').",
    },
    "dalam lanskap yang dinamis": {
        "rule": "id_lanskap_dinamis",
        "severity": "HIGH",
        "explanation": "Frasa 'dalam lanskap yang dinamis' adalah terjemahan klise dari 'in this dynamic landscape'.",
        "fix": "Ganti dengan konteks lingkungan penelitian riil (misal: 'dalam ekosistem SPBE nasional').",
    },
    "dalam lanskap": {
        "rule": "id_dalam_lanskap",
        "severity": "MEDIUM",
        "explanation": "Penggunaan abstrak kata 'lanskap' (seperti 'lanskap data', 'lanskap teknologi') sangat digemari LLM.",
        "fix": "Ganti dengan istilah yang lebih presisi seperti 'ekosistem', 'infrastruktur', atau 'lingkungan'.",
    },
    "ranah yang berkembang": {
        "rule": "id_ranah_berkembang",
        "severity": "HIGH",
        "explanation": "Frasa 'dalam ranah yang terus berkembang' adalah filler pembuka kalimat khas AI.",
        "fix": "Hapus filler dan langsung kemukakan permasalahan statistik atau kesenjangan teknis.",
    },
    "titik balik krusial": {
        "rule": "id_titik_balik",
        "severity": "MEDIUM",
        "explanation": "Klaim 'menandai titik balik krusial' membesar-besarkan signifikansi secara artifisial.",
        "fix": "Paparkan perubahan proses bisnis atau performa sistem dalam angka.",
    },
    "menggarisbawahi": {
        "rule": "id_menggarisbawahi",
        "severity": "MEDIUM",
        "explanation": "Kata 'menggarisbawahi' (terjemahan 'underscores') sering digunakan berlebihan sebagai filler.",
        "fix": "Ganti dengan 'menunjukkan', 'membuktikan', atau paparkan implikasi faktualnya.",
    },
    "tidak dapat dipungkiri bahwa": {
        "rule": "id_tidak_dapat_dipungkiri",
        "severity": "HIGH",
        "explanation": "Frasa 'tidak dapat dipungkiri bahwa' adalah retorika penegasan semu tanpa dasar rujukan.",
        "fix": "Hapus frasa tersebut; jika klaim itu fakta ilmiah, cukup sertakan angka dan sitasi rujukan.",
    },
    "tak terbantahkan bahwa": {
        "rule": "id_tak_terbantahkan",
        "severity": "HIGH",
        "explanation": "Retorika 'tak terbantahkan bahwa' menghindari beban pembuktian ilmiah.",
        "fix": "Hapus frasa dan sertakan bukti literatur atau data pendukung.",
    },
    "perlu dicatat bahwa": {
        "rule": "id_perlu_dicatat",
        "severity": "MEDIUM",
        "explanation": "Hedging preamble 'perlu dicatat bahwa' / 'penting untuk dicatat bahwa' memperpanjang kalimat tanpa menambah makna.",
        "fix": "Hapus frasa pembuka dan sampaikan fakta utamanya secara langsung.",
    },
    "penting untuk dicatat bahwa": {
        "rule": "id_penting_dicatat",
        "severity": "MEDIUM",
        "explanation": "Frasa pengisi 'penting untuk dicatat bahwa' lazim diproduksi LLM.",
        "fix": "Langsung sampaikan pokok pikiran tanpa embel-embel pengantar.",
    },
    "di era modern ini": {
        "rule": "id_era_modern",
        "severity": "HIGH",
        "explanation": "Frasa klise pembuka latar belakang 'di era modern ini' atau 'di era digital saat ini'.",
        "fix": "Mulai latar belakang dengan fenomena atau data statistik riil, bukan generalisasi waktu.",
    },
    "di era digital saat ini": {
        "rule": "id_era_digital",
        "severity": "HIGH",
        "explanation": "Klise klasik pengantar esai AI ('di era digital saat ini').",
        "fix": "Ganti dengan latar belakang kebijakan atau data kuantitatif BPS/pemerintah.",
    },
    "interaksi rumit": {
        "rule": "id_interaksi_rumit",
        "severity": "MEDIUM",
        "explanation": "Terjemahan dari 'intricate interplay'; klise penghindar penjelasan teknis sistem.",
        "fix": "Uraikan dependensi atau alur komunikasi antar-modul perangkat lunak.",
    },
}


# ==============================================================================
# 6. COPULATIVE AVOIDANCE (MEDIUM)
# ==============================================================================

# LLM cenderung menghindari kalimat lugas dengan 'is/are' atau 'adalah/ialah',
# dan menggantinya dengan konstruksi bertingkat seperti 'serves as a', 'stands as', 'berperan sebagai'.
COPULATIVE_AVOIDANCE_PATTERNS: List[Tuple[str, Pattern, str, str]] = [
    (
        "copula_serves_as",
        re.compile(r"\b(?:serves as (?:a|an|the)|stands as (?:a|an|the)|functions as (?:a|an|the)|operates as (?:a|an|the))\b", re.IGNORECASE),
        "Penghindaran kata kerja kopula sederhana ('is/are') dengan konstruksi muluk ('serves as a', 'stands as a').",
        "Gunakan kopula sederhana 'is' atau jelaskan tindakan teknisnya secara langsung.",
    ),
    (
        "copula_marks_the",
        re.compile(r"\b(?:marks (?:the|a) (?:pivotal|significant|crucial|turning))\b", re.IGNORECASE),
        "Pemberian predikat signifikansi semu ('marks the pivotal moment').",
        "Jelaskan peristiwa atau capaian arsitektur secara lugas dan faktual.",
    ),
    (
        "copula_id_berperan_sebagai_wujud",
        re.compile(r"\b(?:berperan sebagai (?:wujud nyata|salah satu pilar|fondasi utama)|berfungsi sebagai representasi)\b", re.IGNORECASE),
        "Penghindaran kopula langsung ('adalah'/'ialah') dengan konstruksi bertingkat ('berperan sebagai wujud nyata').",
        "Gunakan kalimat definisi langsung ('adalah') atau sebutkan fungsi sistem secara teknis.",
    ),
]


# ==============================================================================
# 7. NEGATIVE PARALLELISMS (MEDIUM)
# ==============================================================================

# LLM sering berpura-pura mengoreksi kesalahpahaman umum dengan pola kontras palsu
NEGATIVE_PARALLELISM_PATTERNS: List[Tuple[str, Pattern, str, str]] = [
    (
        "not_just_but_also_en",
        re.compile(r"\bnot (?:only|just) [^,]+,\s*but (?:also )?[^.]+\b", re.IGNORECASE),
        "Formula kontras semu 'Not only X, but also Y' berlebih untuk memompa signifikansi artifisial.",
        "Gunakan konjungsi biasa atau bagi menjadi dua kalimat deskriptif mandiri.",
    ),
    (
        "not_x_but_y_en",
        re.compile(r"\bnot [^,]+,\s*but rather [^.]+\b", re.IGNORECASE),
        "Struktur negative parallelism 'not X, but rather Y'.",
        "Nyatakan secara afirmatif apa karakteristik sistem yang sesungguhnya tanpa kontras retoris.",
    ),
    (
        "tidak_hanya_tetapi_juga_id",
        re.compile(r"\btidak hanya [^,]+,\s*(?:tetapi|melainkan) juga [^.]+\b", re.IGNORECASE),
        "Pola formulaik 'tidak hanya X, tetapi juga Y' yang berulang sebagai pemompa kepentingan.",
        "Nyatakan langsung kemampuan sistem secara afirmatif dan terukur.",
    ),
    (
        "bukan_sekadar_melainkan_id",
        re.compile(r"\bbukan (?:sekadar|hanya) [^,]+,\s*melainkan (?:sebuah )?[^.]+\b", re.IGNORECASE),
        "Gaya retorika sanggahan semu 'bukan sekadar X, melainkan Y'.",
        "Ubah menjadi pernyataan teknis lugas berbasis parameter rancang bangun artefak.",
    ),
]


# ==============================================================================
# 8. SUPERFICIAL ANALYSIS & GERUND TAILS (HIGH)
# ==============================================================================

# LLM gemar menempelkan anak kalimat partisipel (-ing) di akhir kalimat untuk
# mengklaim dampak/makna mendalam tanpa pembuktian.
SUPERFICIAL_ANALYSIS_PATTERNS: List[Tuple[str, Pattern, str, str]] = [
    (
        "superficial_gerund_en",
        re.compile(r",\s*(?:further )?(?:underscoring|highlighting|showcasing|fostering|emphasizing|creating a lively|paving the way for|solidifying its role)\b", re.IGNORECASE),
        "Buntut klausa partisipel (-ing) di ujung kalimat untuk mengklaim signifikansi semu tanpa data pendukung.",
        "Akhiri kalimat pada fakta teknis, atau buat kalimat baru yang menyajikan bukti kuantitatif atas dampak tersebut.",
    ),
    (
        "superficial_gerund_id",
        re.compile(r",\s*(?:sehingga|yang mana)\s+(?:menegaskan pentingnya|menggarisbawahi peran|membuktikan eksistensi|mencerminkan komitmen)\b", re.IGNORECASE),
        "Klausa penutup pemanis di akhir kalimat ('..., sehingga menegaskan pentingnya...') tanpa dasar data empiris.",
        "Hapus klausa pemanis dan ganti dengan data atau pengujian hasil riil.",
    ),
]


# ==============================================================================
# 9. FORMULAIC CONCLUSIONS & OUTLINE HEADERS (HIGH)
# ==============================================================================

FORMULAIC_CONCLUSION_PATTERNS: List[Tuple[str, Pattern, str, str]] = [
    (
        "conclusion_despite_challenges_en",
        re.compile(r"\b(?:Despite (?:these|its) challenges,? [^,]+ faces|Challenges and (?:Legacy|Future Prospects)|Looking ahead,?\b)", re.IGNORECASE),
        "Pola penutup artikel formulaik khas LLM ('Despite these challenges...', 'Looking ahead...').",
        "Tuliskan bab kesimpulan atau saran berdasarkan batasan penelitian dan hasil evaluasi nyata (misal: ISO 25010 / SUS).",
    ),
    (
        "conclusion_despite_challenges_id",
        re.compile(r"\b(?:Meskipun menghadapi (?:berbagai )?tantangan|Menatap masa depan,?\b|Tantangan dan Prospek Masa Depan|Seiring dengan terus berkembangnya)\b", re.IGNORECASE),
        "Pola penutup draf formulaik khas LLM ('Meskipun menghadapi tantangan...', 'Menatap masa depan...').",
        "Gunakan struktur kesimpulan formal DSRM yang merangkum capaian artefak dan rekomendasi pengembangan lanjutan.",
    ),
]
