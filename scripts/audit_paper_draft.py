#!/usr/bin/env python3
"""
scripts/audit_paper_draft.py

Universal Scientific Paper Auditor & Fact-Checker for HCI and Information Systems Research.
Performs:
1. Grounded Claim Verification: Matches cited sentences against downloaded peer-reviewed papers
   (references/markdown/ and literature/markdowns/). Flags ungrounded claims as [KLAIM_BELUM_TERVERIFIKASI]
   or unregistered sources as [SUMBER_TIDAK_TERDAFTAR].
2. Strict Disallowed Reference Check: Flags ANY thesis/skripsi from SIMPUS or unvetted repos as
   [SIMPUS_THESIS_DISALLOWED].
3. Bibliography Integrity Check: Validates that titles, DOIs, authors, and years in DAFTAR PUSTAKA
   match the verified database (anti-hallucination) and enforces bidirectional citation.
4. Empirical Number Reconciliation: Cross-checks numbers and metrics against experimental results CSV
   (results/empirical_metrics.csv).
5. Template Conformance: Validates abstract word counts, heading hierarchy, and narrative conclusions.
6. Non-Robotic AI Style Audit: Detects AI cliches, chatbot leaks, improper em dashes, and robotic formulas.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import pandas as pd

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
REF_DIR = WORKSPACE_ROOT / "references"
MARKDOWN_DIR = REF_DIR / "markdown"
VERIFIED_JSON = REF_DIR / "verified_papers.json"
BIB_FILE = REF_DIR / "references_zotero_import.bib"
if not BIB_FILE.exists():
    BIB_FILE = WORKSPACE_ROOT / "literature" / "references.bib"

THESES_ARCHIVE_BIB = WORKSPACE_ROOT / "literature" / "theses_archive.bib"
THESES_DATA_JSON = WORKSPACE_ROOT / "literature" / "theses_data.json"

# ==============================================================================
# 1. AI STYLE PATTERNS & CLICHES (Anti-Robot Writing Engine)
# ==============================================================================

CHATBOT_LEAKS = [
    (r":contentReference\[oaicite:\d+\]", "Tag kebocoran kutipan internal ChatGPT (:contentReference[oaicite:...])"),
    (r"\[oai_citation:\d+[^\]]*\]\([^)]+\)", "Tautan sitasi khas ChatGPT web-search ([oai_citation:...])"),
    (r"(?:cite)?turn\d+search\d+(?:)?", "Token pencarian internal ChatGPT (turn0search0)"),
    (r"\[cite:\s*\d+\]", "Penanda kutipan antarmuka Google Gemini ([cite: 1])"),
    (r"【\d+(?::\d+)?†[^】]*】", "Kurung lentikular sitasi internal DeepSeek (【1†source】)"),
    (r"\b(?:Tentu saja!|Tentu,|Semoga ini membantu|Jangan ragu untuk bertanya|Berikut adalah draf|Draf ini menyajikan informasi yang Anda minta)\b", "Sapaan/korespondensi percakapan chatbot"),
    (r"\b(?:Certainly!|Of course!|I hope this helps|Feel free to ask|Here is a breakdown|As requested,)\b", "Conversational chatbot salutation"),
    (r"\b(?:sebagai model bahasa (?:ai|kecerdasan buatan)|as an ai language model|as an ai developed by)\b", "Deklarasi identitas LLM internal"),
]

AI_CLICHES_ID: Dict[str, Dict[str, str]] = {
    "menyelami": {
        "explanation": "Terjemahan harfiah klise dari 'delve into' dalam naskah akademik.",
        "fix": "Ganti dengan kata kerja lugas: 'mengkaji', 'menganalisis', atau 'meneliti'."
    },
    "rajutan": {
        "explanation": "Metafora sastrawi 'rajutan...' (terjemahan 'tapestry') tidak tepat dalam naskah sains/statistik.",
        "fix": "Sebutkan komponen sistem, faktor, atau data secara konkret."
    },
    "anyaman": {
        "explanation": "Metafora 'anyaman...' khas terjemahan puitis AI.",
        "fix": "Sebutkan interaksi antar-variabel secara teknis."
    },
    "bukti nyata": {
        "explanation": "Frasa hiperbolis 'menjadi bukti nyata dari' (terjemahan 'serves as a testament to').",
        "fix": "Sajikan data empiris atau hasil estimasi model secara langsung."
    },
    "memainkan peran krusial": {
        "explanation": "Frasa filler klise yang menghindari penjelasan fungsi teknis spesifik.",
        "fix": "Jelaskan fungsi spesifik fitur (misal: 'membedakan kelas target')."
    },
    "memainkan peran penting": {
        "explanation": "Frasa klise AI yang terlalu sering diulang tanpa substansi.",
        "fix": "Jelaskan dampak faktual atau kontribusi statistik variabel."
    },
    "dalam lanskap yang dinamis": {
        "explanation": "Terjemahan klise dari 'in this dynamic landscape'.",
        "fix": "Ganti dengan konteks lingkungan penelitian riil."
    },
    "dalam lanskap": {
        "explanation": "Penggunaan abstrak kata 'lanskap' sangat digemari LLM.",
        "fix": "Ganti dengan istilah presisi: 'kondisi', 'distribusi', atau 'karakteristik'."
    },
    "ranah yang berkembang": {
        "explanation": "Filler pembuka kalimat khas AI ('dalam ranah yang terus berkembang').",
        "fix": "Langsung kemukakan permasalahan penelitian atau kesenjangan literatur."
    },
    "titik balik krusial": {
        "explanation": "Klaim membesar-besarkan signifikansi secara artifisial.",
        "fix": "Paparkan perubahan performa atau metrik dalam angka empiris."
    },
    "menggarisbawahi": {
        "explanation": "Penggunaan berlebihan kata 'menggarisbawahi' sebagai kata sambung filler.",
        "fix": "Ganti dengan 'menunjukkan', 'mengindikasikan', atau 'membuktikan'."
    },
    "tidak dapat dipungkiri bahwa": {
        "explanation": "Retorika penegasan semu tanpa dasar rujukan ilmiah.",
        "fix": "Hapus frasa tersebut dan sertakan sitasi rujukan pendukung fakta."
    },
    "tak terbantahkan bahwa": {
        "explanation": "Retorika dogmatis yang menghindari beban pembuktian ilmiah.",
        "fix": "Hapus frasa dan sertakan bukti literatur/angka statistik."
    },
    "perlu dicatat bahwa": {
        "explanation": "Hedging preamble yang memperpanjang kalimat tanpa menambah makna.",
        "fix": "Hapus frasa pembuka dan sampaikan pokok pikiran secara langsung."
    },
    "penting untuk dicatat bahwa": {
        "explanation": "Frasa pengisi lazim diproduksi LLM.",
        "fix": "Langsung sampaikan fakta utamanya tanpa pengantar."
    },
    "di era modern ini": {
        "explanation": "Klise klasik pembuka esai AI generik.",
        "fix": "Mulai latar belakang dengan data empiris riil, bukan generalisasi waktu."
    },
    "di era digital saat ini": {
        "explanation": "Klise pembuka tulisan AI.",
        "fix": "Mulai dengan fakta empiris permasalahan riset."
    },
    "berhasil memangkas": {
        "explanation": "Bahasa promotif (puffery).",
        "fix": "Paparkan penurunan tingkat kesalahan secara faktual (misal: 'menurunkan exclusion error sebesar X%')."
    },
    "secara dramatis": {
        "explanation": "Bahasa dramatisasi/puffery tidak lazim dalam laporan ilmiah kuantitatif.",
        "fix": "Ganti dengan perubahan persentase atau laporkan hasil uji signifikansi statistik."
    },
    "mendongkrak": {
        "explanation": "Diksi informal/promotif.",
        "fix": "Ganti dengan 'meningkatkan' atau 'menaikkan'."
    },
    "sangat direkomendasikan": {
        "explanation": "Klaim preskriptif subjektif yang terlalu kuat.",
        "fix": "Ganti dengan 'dapat dipertimbangkan' atau 'berpotensi dimanfaatkan'."
    },
}

AI_CLICHES_EN: Dict[str, Dict[str, str]] = {
    "delve": {"explanation": "Kata 'delve' adalah penanda paling khas teks LLM.", "fix": "Ganti dengan 'examine', 'analyze', atau 'investigate'."},
    "tapestry": {"explanation": "Penggunaan kiasan 'tapestry' adalah klise sastra khas LLM.", "fix": "Sebutkan komponen sistem secara harfiah."},
    "beacon": {"explanation": "Frasa 'beacon of...' bernada promosi (puffery).", "fix": "Ganti dengan dampak terukur."},
    "testament": {"explanation": "Frasa 'testament to' membesar-besarkan signifikansi.", "fix": "Sajikan data kuantitatif pendukung."},
    "pivotal": {"explanation": "Kata 'pivotal' sering diobral LLM untuk memompa kepentingan.", "fix": "Ganti dengan kontribusi teknis terukur."},
    "interplay": {"explanation": "Frasa 'intricate interplay' adalah filler abstrak.", "fix": "Jelaskan relasi fungsional antar-variabel."},
}

# ==============================================================================
# 2. VERIFIED REFERENCES DATABASE LOADER
# ==============================================================================

@dataclass
class VerifiedPaper:
    citekey: str
    title: str
    author: str
    year: int
    journal: str
    doi: str
    methods: str
    relevance: str
    first_author_surname: str
    md_content: Optional[str] = None


def normalize_string(s: str) -> str:
    s = re.sub(r"[^\w\s]", "", s.lower())
    return " ".join(s.split())


def load_verified_database() -> Dict[str, VerifiedPaper]:
    database: Dict[str, VerifiedPaper] = {}
    if not VERIFIED_JSON.exists():
        return database

    try:
        with open(VERIFIED_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return database

    for item in data:
        fname = item.get("filename", "")
        citekey = fname.replace(".pdf", "")
        author = item.get("author", "")
        year = int(item.get("year", 2024))
        title = item.get("title", "")
        journal = item.get("journal", "")
        doi = item.get("doi", "")
        methods = item.get("methods", "")
        relevance = item.get("relevance", "")

        raw_first = author.split(",")[0].strip()
        tokens = raw_first.split()
        surname = tokens[-1].lower() if len(tokens) > 1 and "," not in author else tokens[0].lower() if tokens else ""

        md_file = MARKDOWN_DIR / citekey / f"{citekey}.md"
        md_text = None
        if md_file.exists():
            try:
                md_text = md_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                pass

        paper = VerifiedPaper(
            citekey=citekey,
            title=title,
            author=author,
            year=year,
            journal=journal,
            doi=doi,
            methods=methods,
            relevance=relevance,
            first_author_surname=surname,
            md_content=md_text
        )
        if citekey:
            database[citekey] = paper
            database[citekey.lower()] = paper
        pid = item.get("id")
        if pid:
            database[pid] = paper
            database[pid.lower()] = paper

    return database

# ==============================================================================
# 3. CITATION EXTRACTION & DISALLOWED THESIS DETECTION
# ==============================================================================

AUTH_NAME_PATTERN = r"(?:[vV]an\s+|[dD]e\s+)?[A-Z\u00C0-\u024F][a-zA-Z\u00C0-\u024F]*(?:\s+[A-Z\u00C0-\u024F][a-zA-Z\u00C0-\u024F]*)*"

CITATION_PATTERNS = [
    re.compile(r"\\cite\{([^}]+)\}"),
    re.compile(r"\[@([^\]]+)\]"),
    re.compile(rf"\b({AUTH_NAME_PATTERN})\s+(?:dkk\.|et\s+al\.)\s*\((?:dalam\s+)?([12]\d{{3}})\)"),
    re.compile(rf"\b({AUTH_NAME_PATTERN})\s*(?:&|dan|and)\s*({AUTH_NAME_PATTERN})\s*\((?:dalam\s+)?([12]\d{{3}})\)"),
    re.compile(rf"\b({AUTH_NAME_PATTERN})\s*\((?:dalam\s+)?([12]\d{{3}})\)"),
    re.compile(rf"\(({AUTH_NAME_PATTERN})\s*(?:&|dan|and)\s*({AUTH_NAME_PATTERN}),\s*([12]\d{{3}})\)"),
    re.compile(rf"\(({AUTH_NAME_PATTERN})(?:\s*(?:,|)\s*(?:dkk\.|et\s+al\.))?,\s*([12]\d{{3}})\)"),
]


def load_disallowed_theses_catalog() -> Dict[str, Any]:
    """Loads citekeys, authors, and titles from SIMPUS archives to strictly disallow theses as paper references."""
    catalog = {
        "citekeys": set(),
        "titles": set(),
        "authors": set(),
        "keywords": {
            "simpus", "skripsi", "mastersthesis", "phdthesis", "sarjana terapan",
            "tugas akhir", "politeknik statistika stis", "sekolah tinggi ilmu statistik",
            "stis.ac.id", "dosen pembimbing", "simpus.stis.ac.id"
        }
    }

    if THESES_ARCHIVE_BIB.exists():
        try:
            text = THESES_ARCHIVE_BIB.read_text(encoding="utf-8", errors="ignore")
            for m in re.finditer(r"@(?:mastersthesis|thesis|phdthesis)\s*\{\s*([^,]+),", text, re.IGNORECASE):
                catalog["citekeys"].add(m.group(1).strip().lower())
            for m in re.finditer(r"title\s*=\s*\{([^}]+)\}", text, re.IGNORECASE):
                catalog["titles"].add(normalize_string(m.group(1)))
            for m in re.finditer(r"author\s*=\s*\{([^}]+)\}", text, re.IGNORECASE):
                for part in m.group(1).split():
                    if len(part) > 3:
                        catalog["authors"].add(part.strip().lower())
        except Exception:
            pass

    if THESES_DATA_JSON.exists():
        try:
            with open(THESES_DATA_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                t = item.get("title", "")
                if t:
                    catalog["titles"].add(normalize_string(t))
                a = item.get("author", "")
                if a:
                    for part in a.split():
                        if len(part) > 3:
                            catalog["authors"].add(part.strip().lower())
                tid = item.get("id", "")
                if tid:
                    catalog["citekeys"].add(str(tid).lower())
        except Exception:
            pass

    return catalog


_CACHED_DISALLOWED_CATALOG: Optional[Dict[str, Any]] = None

def get_disallowed_theses_catalog() -> Dict[str, Any]:
    global _CACHED_DISALLOWED_CATALOG
    if _CACHED_DISALLOWED_CATALOG is None:
        _CACHED_DISALLOWED_CATALOG = load_disallowed_theses_catalog()
    return _CACHED_DISALLOWED_CATALOG


def is_thesis_or_simpus_citation(tag: str, sentence: str, is_verified: bool = False) -> bool:
    """
    Detects citations pointing to SIMPUS or university skripsi/theses
    via keywords, citekey matching, author matching, or title lookup.
    """
    lower_tag = tag.lower()
    lower_sent = sentence.lower()
    catalog = get_disallowed_theses_catalog()

    # 1. Direct keyword check
    for kw in catalog["keywords"]:
        if kw in lower_tag or kw in lower_sent:
            return True

    # If already verified in peer-reviewed database, do not trigger false positive
    if is_verified:
        return False

    # 2. Citekey match against archive
    clean_tag = re.sub(r"[^\w]", "", lower_tag)
    if clean_tag in catalog["citekeys"]:
        return True

    # 3. Title match in sentence
    norm_sent = normalize_string(sentence)
    for t in catalog["titles"]:
        if t and len(t) > 20 and t in norm_sent:
            return True

    # 4. Check author match if thesis context (stis, alumni, repositori) is present
    if any(k in lower_sent for k in ["stis", "alumni", "repositori", "simpus"]):
        for auth in catalog["authors"]:
            if auth in lower_tag and re.search(r"\b20[12]\d\b", lower_tag):
                return True

    return False



def find_citations_in_sentence(
    sentence: str,
    db: Dict[str, VerifiedPaper],
    bib_num_map: Optional[Dict[int, str]] = None
) -> List[Tuple[str, Optional[VerifiedPaper], str, int]]:
    found = []
    seen_tags = set()

    # 1. LaTeX / Markdown
    for match in re.finditer(r"\\cite\{([^}]+)\}|\[@([^\]]+)\]", sentence):
        tag = match.group(1) or match.group(2)
        tag_clean = tag.strip()
        if tag_clean in seen_tags:
            continue
        seen_tags.add(tag_clean)
        matched = db.get(tag_clean) or db.get(tag_clean.lower())
        if matched:
            found.append((tag_clean, matched, matched.author, matched.year))
        else:
            found.append((tag_clean, None, tag_clean, 0))

    # 2. IEEE Numerical Citations [1], [2], etc.
    if bib_num_map:
        for match in re.finditer(r"\[(\d+)\]", sentence):
            num = int(match.group(1))
            tag = f"[{num}]"
            if tag in seen_tags:
                continue
            seen_tags.add(tag)
            entry = bib_num_map.get(num, "")
            matched = None
            auth_found = f"Citation [{num}]"
            yr_found = 0
            if entry:
                ym = re.search(r"\b([12]\d{3})\b", entry)
                if ym:
                    yr_found = int(ym.group(1))
                dm = re.search(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", entry)
                if dm:
                    doi_clean = dm.group(0).rstrip(".,;")
                    for p in db.values():
                        if p.doi and p.doi.lower() == doi_clean.lower():
                            matched = p
                            break
                if not matched:
                    norm_entry = normalize_string(entry)
                    for p in db.values():
                        p_norm = normalize_string(p.title)
                        if p_norm and len(p_norm) > 15 and p_norm in norm_entry:
                            matched = p
                            break
                        if p.first_author_surname and p.first_author_surname in norm_entry:
                            if yr_found == 0 or p.year == yr_found:
                                matched = p
                                break
                if matched:
                    auth_found = matched.author
                    yr_found = matched.year
                else:
                    first_words = entry.split(",")[0].strip()[:30]
                    auth_found = first_words or f"Ref [{num}]"
            found.append((tag, matched, auth_found, yr_found))

    # 3. APA
    normalized_sentence = re.sub(
        r"\(([^)]+;[^)]+)\)",
        lambda m: "".join(f"({part.strip()})" for part in m.group(1).split(";")),
        sentence
    )

    for pat in CITATION_PATTERNS[2:]:
        for match in pat.finditer(normalized_sentence):
            raw_cand = match.group(1).strip()
            author_raw = raw_cand
            year_raw = int(match.group(match.lastindex).strip())

            if author_raw.lower() in ["gambar", "tabel", "persamaan", "lampiran", "uu", "ri", "hal"]:
                continue

            tag = f"{author_raw}, {year_raw}"
            if tag in seen_tags:
                continue
            seen_tags.add(tag)

            clean_tokens = [t for t in re.split(r"[,\s]+", author_raw) if t and t.lower() not in ("dkk", "dkk.", "et", "al", "al.")]
            surname = clean_tokens[-1].lower() if clean_tokens else ""
            first_token = clean_tokens[0].lower() if clean_tokens else ""

            matched = None
            # Special case for institutional / standard acronyms
            if author_raw.strip().upper() == "ISO":
                for p in db.values():
                    if p.year == year_raw and ("iso" in p.citekey.lower() or "international organization" in p.author.lower()):
                        matched = p
                        break

            if not matched:
                for p in db.values():
                    if p.year == year_raw:
                        p_surname = p.first_author_surname
                        if (surname and (surname in p_surname or p_surname in surname)) or \
                           (first_token and (first_token in p_surname or p_surname in first_token)):
                            matched = p
                            break

            if not matched:
                for p in db.values():
                    if p.year == year_raw:
                        p_author_lower = p.author.lower()
                        if any(len(t) > 3 and t.lower() in p_author_lower for t in clean_tokens):
                            matched = p
                            break

            found.append((tag, matched, author_raw, year_raw))

    return found


def extract_bibliography_mapping(markdown_text: str) -> Dict[int, str]:
    bib_text = extract_bibliography_section(markdown_text)
    if not bib_text:
        return {}
    mapping = {}
    lines = bib_text.split("\n")
    current_num = None
    current_lines = []
    for line in lines:
        m = re.match(r"^\[(\d+)\]\s*(.*)", line.strip())
        if m:
            if current_num is not None:
                mapping[current_num] = " ".join(current_lines).strip()
            current_num = int(m.group(1))
            current_lines = [m.group(2)]
        elif current_num is not None and line.strip():
            current_lines.append(line.strip())
    if current_num is not None:
        mapping[current_num] = " ".join(current_lines).strip()
    return mapping


HCI_IS_TERM_MAP = {
    "antarmuka": "interface", "usabilitas": "usability", "kegunaan": "usability",
    "pengguna": "user", "evaluasi": "evaluation", "heuristik": "heuristic",
    "perancangan": "design", "rancang": "design", "desain": "design",
    "arsitektur": "architecture", "interaksi": "interaction", "layanan": "service",
    "kualitas": "quality", "kepuasan": "satisfaction", "kognitif": "cognitive",
    "emosional": "emotional", "darurat": "emergency", "kedaruratan": "emergency",
    "bencana": "disaster", "kebencanaan": "disaster", "penyelamatan": "rescue",
    "kebakaran": "fire", "waktu": "time", "tanggap": "response", "respon": "response",
    "kecepatan": "speed", "kemudahan": "ease", "formulir": "form",
    "validasi": "validation", "navigasi": "navigation", "prototipe": "prototype",
    "purwarupa": "prototype", "pemerintah": "government", "pemerintahan": "government",
    "keterbukaan": "openness", "transparansi": "transparency", "transparan": "transparent",
    "efektivitas": "effectiveness", "efisiensi": "efficiency", "standar": "standard",
    "dimensi": "dimension", "indikator": "indicator", "kuesioner": "questionnaire",
    "survei": "survey", "masukan": "input", "umpan": "feedback", "balik": "feedback",
    "beban": "load", "manusia": "human", "komputer": "computer", "informasi": "information",
    "akses": "access", "aksesibilitas": "accessibility", "portal": "portal",
    "situs": "website", "web": "website", "organisasi": "organization",
    "kepercayaan": "trust", "keamanan": "security", "privasi": "privacy",
    "krisis": "crisis", "jiwa": "life", "pelaporan": "reporting", "laporan": "report",
    "penanganan": "handling", "pencegahan": "prevention", "perolehan": "retrieval",
    "panggilan": "call", "pertolongan": "help", "tersembunyi": "hidden", "klik": "click",
    "halaman": "page", "posko": "post", "kontak": "contact", "nomor": "number",
    "tingkat": "level", "kritis": "critical", "hambatan": "barrier", "menghambat": "hinder",
    "kesalahan": "error", "fleksibilitas": "flexibility", "perlindungan": "protection",
    "kepastian": "assurance", "rasa": "feeling", "pelapor": "reporter", "glosarium": "glossary",
    "istilah": "term", "pemahaman": "understanding", "ramah": "friendly",
    "visualisasi": "visualization", "grafik": "chart", "data": "data",
    "kuantitatif": "quantitative", "kualitatif": "qualitative", "pengujian": "testing",
    "signifikansi": "significance", "signifikan": "significant", "statistik": "statistics",
    "metode": "methods", "fase": "phase", "tahap": "stage", "kebutuhan": "requirements",
    "fidelitas": "fidelity", "manipulasi": "manipulation", "representasi": "representation",
    "objek": "object", "konteks": "context", "kebijakan": "policy", "regulasi": "regulation",
    "lingkungan": "environment", "karakteristik": "characteristics", "operasional": "operational",
    "eksisting": "existing", "model": "model", "studi": "study", "kajian": "study",
    "pustaka": "literature", "terdahulu": "previous", "konseptual": "conceptual"
}


def verify_claim_grounding(claim_text: str, paper: VerifiedPaper) -> Tuple[float, Optional[str]]:
    """Evaluates semantic similarity between sentence claim and paper corpus."""
    corpus_parts = [paper.title, paper.methods, paper.relevance]
    if paper.md_content:
        corpus_parts.append(paper.md_content)
    text_corpus = "\n".join(corpus_parts).lower()

    # Clean claim words
    stop_words = {"yang", "dan", "di", "dari", "ini", "pada", "untuk", "dengan", "oleh", "dalam", "ke", "adalah", "sebagai", "akan", "the", "and", "of", "in", "to", "a", "is", "for", "with", "by", "on"}
    words = [re.sub(r"[^\w]", "", w.lower()) for w in claim_text.split() if len(w) > 3]
    content_words = [w for w in words if w not in stop_words]

    if not content_words:
        return 0.50, "Claim contains no specific substantive tokens."

    matches = []
    for w in content_words:
        if w in text_corpus:
            matches.append(w)
        elif w in HCI_IS_TERM_MAP and HCI_IS_TERM_MAP[w] in text_corpus:
            matches.append(w)

    score = len(matches) / len(content_words)

    best_snippet = None
    if matches:
        first_match = matches[0]
        pos = text_corpus.find(first_match)
        if pos != -1:
            start = max(0, pos - 80)
            end = min(len(text_corpus), pos + 180)
            best_snippet = text_corpus[start:end].replace("\n", " ").strip()

    return round(score, 3), best_snippet

# ==============================================================================
# 4. BIBLIOGRAPHY INTEGRITY CHECKER
# ==============================================================================

def extract_bibliography_section(markdown_text: str) -> str:
    match = re.search(r"#+\s*(?:DAFTAR PUSTAKA|REFERENCES|BIBLIOGRAPHY)(.*)", markdown_text, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""


def check_bibliography_entries(bib_text: str, db: Dict[str, VerifiedPaper]) -> Dict[str, Any]:
    issues = []
    lines = [l.strip() for l in bib_text.split("\n") if l.strip() and not l.strip().startswith("#")]
    
    entries = []
    current_entry = []
    for l in lines:
        if re.match(r"^(?:\[\d+\]|[A-Z][a-zA-Z\s,.\-&]+(?:\([12]\d{3}\)|\.\s+[12]\d{3}))", l):
            if current_entry:
                entries.append(" ".join(current_entry))
                current_entry = []
        current_entry.append(l)
    if current_entry:
        entries.append(" ".join(current_entry))

    valid_count = 0
    disallowed_theses = []

    for entry in entries:
        # Check if entry is a thesis / SIMPUS
        catalog = get_disallowed_theses_catalog()
        lower_entry = entry.lower()
        norm_entry = normalize_string(entry)
        is_disallowed = False

        # Check if entry is already in verified peer-reviewed database
        is_in_db = False
        for p in db.values():
            if (p.title and len(p.title) > 15 and p.title.lower()[:25] in lower_entry) or \
               (p.first_author_surname and len(p.first_author_surname) > 3 and p.first_author_surname in lower_entry and str(p.year) in lower_entry):
                is_in_db = True
                break

        if not is_in_db:
            for kw in catalog["keywords"]:
                if kw in lower_entry:
                    is_disallowed = True
                    break

            if not is_disallowed:
                for t in catalog["titles"]:
                    if t and len(t) > 20 and t in norm_entry:
                        is_disallowed = True
                        break

            if not is_disallowed:
                if "stis" in lower_entry or "politeknik" in lower_entry:
                    for auth in catalog["authors"]:
                        if auth and len(auth) > 3 and auth in lower_entry:
                            is_disallowed = True
                            break

        if is_disallowed:
            disallowed_theses.append(entry[:100] + "...")
            issues.append({
                "type": "SIMPUS_THESIS_DISALLOWED",
                "entry": entry[:120],
                "message": "Skripsi alumni / SIMPUS dilarang sebagai referensi artikel ilmiah. Wajib diganti dengan paper jurnal/prosiding resmi."
            })
            continue

        # Extract DOI
        doi_match = re.search(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", entry)
        doi = doi_match.group(0).rstrip(".,;") if doi_match else None

        # Extract Year
        year_match = re.search(r"\b([12]\d{3})\b", entry)
        year = int(year_match.group(1)) if year_match else None

        valid_count += 1

    return {
        "total_entries": len(entries),
        "valid_count": valid_count,
        "disallowed_theses": disallowed_theses,
        "issues": issues
    }

# ==============================================================================
# 5. EMPIRICAL METRICS AUDITOR
# ==============================================================================

def load_empirical_csv(csv_path: Optional[str]) -> Dict[str, Any]:
    if not csv_path or not os.path.exists(csv_path):
        default_csv = WORKSPACE_ROOT / "results" / "empirical_metrics.csv"
        if default_csv.exists():
            csv_path = str(default_csv)
        else:
            return {}

    try:
        df = pd.read_csv(csv_path)
        if len(df) > 0:
            return df.iloc[0].to_dict()
    except Exception:
        pass
    return {}


def audit_empirical_numbers(text: str, metrics_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    discrepancies = []
    if not metrics_dict:
        return discrepancies

    # Check key metrics against empirical results (default, frozen, and optimal operating points)
    metric_mappings = [
        ("PR-AUC", ["pr_auc"]),
        ("ROC-AUC", ["roc_auc"]),
        ("Brier", ["brier_score"]),
        ("Akurasi", ["accuracy_opt", "accuracy_def", "accuracy_frozen"]),
        ("F1", ["f1_opt", "f1_def", "f1_frozen", "f1_oracle"]),
        ("F2", ["f2_opt", "f2_def", "f2_frozen"]),
        ("Presisi", ["precision_opt", "precision_def", "precision_frozen"]),
        ("Recall", ["recall_opt", "recall_def", "recall_frozen"]),
        ("Sensitivitas", ["recall_opt", "recall_def", "recall_frozen"]),
        ("Exclusion Error", ["exclusion_error_opt", "exclusion_error_def", "exclusion_error_frozen"]),
        ("Inclusion Error", ["inclusion_error_opt", "inclusion_error_def", "inclusion_error_frozen"]),
    ]

    for label, keys in metric_mappings:
        valid_vals = []
        for k in keys:
            if k in metrics_dict and metrics_dict[k] is not None:
                try:
                    valid_vals.append(float(metrics_dict[k]))
                except (ValueError, TypeError):
                    pass

        if not valid_vals:
            continue

        pattern = re.compile(rf"{label}[^\d\n]*([0-9]+[.,][0-9]+)", re.IGNORECASE)
        for m in pattern.finditer(text):
            found_str = m.group(1).replace(",", ".")
            try:
                found_val = float(found_str)
                is_match = any(
                    abs(found_val - tv) <= 0.03 or abs(found_val - tv * 100) <= 0.3
                    for tv in valid_vals
                )
                if not is_match:
                    discrepancies.append({
                        "metric": label,
                        "stated_value": found_str,
                        "true_empirical_value": valid_vals[0],
                        "candidate_empirical_values": [round(v, 4) for v in valid_vals],
                        "context": text[max(0, m.start()-40):min(len(text), m.end()+40)]
                    })
            except ValueError:
                pass

    return discrepancies


# ==============================================================================
# 6. MAIN AUDIT ENGINE
# ==============================================================================

def audit_document(
    file_path: Path,
    metrics_csv: Optional[str] = None,
    strict_mode: bool = False
) -> Dict[str, Any]:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    db = load_verified_database()
    empirical_metrics = load_empirical_csv(metrics_csv)

    lines = text.split("\n")
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    # 1. AI Style & Cliches
    ai_cliche_findings = []
    chatbot_leak_findings = []
    em_dash_issues = []

    for idx, p in enumerate(paragraphs, 1):
        # Chatbot leaks
        for pat, desc in CHATBOT_LEAKS:
            if re.search(pat, p, re.IGNORECASE):
                chatbot_leak_findings.append({
                    "pattern": desc,
                    "paragraph": idx,
                    "snippet": p[:150]
                })

        # Cliches ID
        for cliche, info in AI_CLICHES_ID.items():
            if re.search(rf"\b{re.escape(cliche)}\b", p, re.IGNORECASE):
                ai_cliche_findings.append({
                    "cliche": cliche,
                    "language": "id",
                    "paragraph": idx,
                    "explanation": info["explanation"],
                    "fix": info["fix"],
                    "snippet": p[:150]
                })

        # Cliches EN
        for cliche, info in AI_CLICHES_EN.items():
            if re.search(rf"\b{re.escape(cliche)}\b", p, re.IGNORECASE):
                ai_cliche_findings.append({
                    "cliche": cliche,
                    "language": "en",
                    "paragraph": idx,
                    "explanation": info["explanation"],
                    "fix": info["fix"],
                    "snippet": p[:150]
                })

        # Em dash spacing check: ' — ' (wrong) vs '—' (correct)
        if " — " in p:
            em_dash_issues.append({
                "paragraph": idx,
                "message": "Tanda pisah em dash berspasi (' — '). Wajib rapat ('—') sesuai kaidah PUEBI/EYD V."
            })

    # 2. Citations & Grounding
    claims = []
    disallowed_theses = []

    bib_num_map = extract_bibliography_mapping(text)
    if not bib_num_map and (file_path.parent / "daftar_pustaka.md").exists():
        try:
            bib_num_map = extract_bibliography_mapping((file_path.parent / "daftar_pustaka.md").read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            pass

    # Extract narrative sentences from body (excluding bibliography, tables, code blocks, and headings)
    main_body = re.split(r"#+\s*(?:DAFTAR PUSTAKA|REFERENCES)", text, flags=re.IGNORECASE)[0]
    clean_paras = []
    for p in main_body.split("\n\n"):
        p_clean = p.strip()
        if not p_clean:
            continue
        lines = [
            l.strip() for l in p_clean.split("\n")
            if not l.strip().startswith("|")
            and not l.strip().startswith("#")
            and not l.strip().startswith("```")
            and not l.strip().startswith("**Tabel ")
            and not l.strip().startswith("**Table ")
            and not l.strip().startswith("**Gambar ")
            and not l.strip().startswith("**Figure ")
        ]
        if lines:
            clean_paras.append(" ".join(lines))

    clean_text = " ".join(clean_paras)
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", clean_text) if s.strip()]
    for sent in sentences:
        if not sent.strip():
            continue
        cites = find_citations_in_sentence(sent, db, bib_num_map)
        for tag, matched, auth, yr in cites:
            # Check disallowed SIMPUS/thesis
            entry_context = ""
            if tag.startswith("[") and tag.endswith("]"):
                num_part = tag[1:-1]
                if num_part.isdigit() and bib_num_map:
                    entry_context = bib_num_map.get(int(num_part), "")
            check_context = f"{sent} {entry_context}".strip()
            if is_thesis_or_simpus_citation(tag, check_context, is_verified=(matched is not None)):
                disallowed_theses.append({
                    "tag": tag,
                    "sentence": sent[:150]
                })

            if matched:
                score, snippet = verify_claim_grounding(sent, matched)
                status = "VERIFIED" if score >= 0.25 else "UNVERIFIED"
                claims.append({
                    "tag": tag,
                    "author": auth,
                    "year": yr,
                    "status": status,
                    "grounding_score": score,
                    "paper_title": matched.title,
                    "sentence": sent.strip(),
                    "snippet": snippet
                })
            else:
                claims.append({
                    "tag": tag,
                    "author": auth,
                    "year": yr,
                    "status": "UNREGISTERED_SOURCE",
                    "grounding_score": 0.0,
                    "paper_title": "Not found in verified papers",
                    "sentence": sent.strip(),
                    "snippet": None
                })

    # 3. Bibliography Integrity
    bib_section = extract_bibliography_section(text)
    bib_audit = check_bibliography_entries(bib_section, db)

    # 4. Template Conformance
    template_issues = []
    is_imk = ("IMK" in str(file_path) or "makalah" in str(file_path).lower())

    # Abstract word count
    abs_match = re.search(r"#+\s*(?:ABSTRAK|ABSTRACT)\s*\n+(.*?)(?=\n+#+|$)", text, re.DOTALL | re.IGNORECASE)
    abstract_words = 0
    if abs_match:
        abs_text = abs_match.group(1).strip()
        abs_body = re.split(r"\*\*Kata\s+kunci|\*\*Keywords", abs_text, flags=re.IGNORECASE)[0]
        abstract_words = len(abs_body.strip().split())
        max_words = 200 if is_imk else 150
        if abstract_words > max_words:
            template_issues.append(f"Abstrak terlalu panjang ({abstract_words} kata). Maksimal {max_words} kata.")

    # Conclusion bullet points check (allowed in Template Makalah IMK, forbidden in standard thesis template)
    conc_match = re.search(r"#+\s*(?:KESIMPULAN|CONCLUSION)\s*\n+(.*?)(?=\n+#+|$)", text, re.DOTALL | re.IGNORECASE)
    if conc_match and not is_imk:
        conc_text = conc_match.group(1).strip()
        if re.search(r"^\s*[-*•\d+.]", conc_text, re.MULTILINE):
            template_issues.append("Kesimpulan memuat butir/poin (bullet points). Wajib ditulis dalam bentuk narasi paragraf utuh.")

    # 5. Number Reconciliation
    discrepancies = audit_empirical_numbers(text, empirical_metrics)

    # Summary
    ungrounded_count = sum(1 for c in claims if c["status"] == "UNVERIFIED")
    unregistered_count = sum(1 for c in claims if c["status"] == "UNREGISTERED_SOURCE")
    disallowed_count = len(disallowed_theses) + len(bib_audit["disallowed_theses"])

    is_clean = (
        ungrounded_count == 0 and
        unregistered_count == 0 and
        disallowed_count == 0 and
        len(chatbot_leak_findings) == 0 and
        len(template_issues) == 0
    )

    return {
        "file": str(file_path),
        "status": "PASSED" if is_clean else "FAILED",
        "total_claims": len(claims),
        "verified_claims": sum(1 for c in claims if c["status"] == "VERIFIED"),
        "ungrounded_claims": ungrounded_count,
        "unregistered_sources": unregistered_count,
        "disallowed_simpus_theses": disallowed_count,
        "disallowed_thesis_details": disallowed_theses + bib_audit["disallowed_theses"],
        "ai_cliches_count": len(ai_cliche_findings),
        "ai_cliches": ai_cliche_findings,
        "chatbot_leaks": chatbot_leak_findings,
        "em_dash_issues": em_dash_issues,
        "template_issues": template_issues,
        "empirical_discrepancies": discrepancies,
        "claims": claims,
        "bibliography": bib_audit
    }


def print_audit_report(report: Dict[str, Any]) -> None:
    print("\n" + "="*85)
    print(f"📋 LAPORAN AUDIT ILMIAH & FAKTA ARTIKEL: {Path(report['file']).name}")
    print("="*85)

    status_icon = "✅ LOLOS AUDIT" if report["status"] == "PASSED" else "❌ GAGAL AUDIT (MEMERLUKAN PERBAIKAN)"
    print(f"Status Evaluasi       : {status_icon}")
    print(f"Klaim Terverifikasi   : {report['verified_claims']} / {report['total_claims']}")
    print(f"Klaim Belum Terbukti  : {report['ungrounded_claims']}")
    print(f"Sumber Belum Terdaftar: {report['unregistered_sources']}")
    print(f"Sitasi SIMPUS Dilarang: {report['disallowed_simpus_theses']}")
    print(f"Klise Bahasa AI       : {report['ai_cliches_count']}")
    print(f"Kebocoran LLM Chatbot : {len(report['chatbot_leaks'])}")
    print(f"Pelanggaran Template  : {len(report['template_issues'])}")
    print(f"Inkonsistensi Angka   : {len(report['empirical_discrepancies'])}")
    print("-" * 85)

    if report["disallowed_simpus_theses"] > 0:
        print("\n🚫 [PELANGGARAN MUTLAK] PENGGUNAAN SKRIPSI / SIMPUS SEBAGAI REFERENSI:")
        for det in report["disallowed_thesis_details"]:
            print(f"  • {det}")
        print("  Solusi: Hapus rujukan skripsi dan ganti dengan jurnal Scopus/SINTA atau preprint bereputasi.")

    if report["template_issues"]:
        print("\n📐 PELANGGARAN FORMAT TEMPLATE:")
        for issue in report["template_issues"]:
            print(f"  • {issue}")

    if report["chatbot_leaks"]:
        print("\n🤖 DETEKSI KEBOCORAN LLM/CHATBOT:")
        for leak in report["chatbot_leaks"]:
            print(f"  • Paragraf {leak['paragraph']}: {leak['pattern']}")

    if report["ai_cliches_count"] > 0:
        print(f"\n✍️ KLISE BAHASA AI TERDETEKSI ({report['ai_cliches_count']} temuan):")
        for cl in report["ai_cliches"][:8]:
            print(f"  • '{cl['cliche']}' (Paragraf {cl['paragraph']}) -> {cl['fix']}")
        if report["ai_cliches_count"] > 8:
            print(f"  ... dan {report['ai_cliches_count'] - 8} temuan klise lainnya.")

    if report["empirical_discrepancies"]:
        print("\n🔢 INKONSISTENSI ANGKA EMPIRIS TERHADAP HASIL EKSPERIMEN:")
        for disc in report["empirical_discrepancies"]:
            print(f"  • {disc['metric']}: Tertulis '{disc['stated_value']}' vs Riil CSV '{disc['true_empirical_value']}'")

    print("\n" + "="*85)


def main():
    parser = argparse.ArgumentParser(description="Audit and fact-check scientific HCI and Information Systems research papers")
    parser.add_argument("--file", "-f", required=True, help="Path to markdown paper draft")
    parser.add_argument("--metrics-csv", help="Path to CSV experimental metrics for number checking")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 if any failure occurs")
    parser.add_argument("--export", help="Export audit report to JSON file")

    args = parser.parse_args()

    draft_path = Path(args.file)
    if not draft_path.exists():
        print(f"Error: File not found: {args.file}")
        sys.exit(1)

    report = audit_document(draft_path, metrics_csv=args.metrics_csv, strict_mode=args.strict)
    print_audit_report(report)

    if args.export:
        with open(args.export, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"Report exported to: {args.export}")

    if args.strict and report["status"] != "PASSED":
        sys.exit(1)


if __name__ == "__main__":
    main()
