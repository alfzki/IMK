"""Extractor for research limitations, gaps, discussions, and future work from local corpus."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple

from calm_carson.brainstorm.models import ResearchGapItem

logger = logging.getLogger(__name__)

# Heuristic patterns for Indonesian and English limitation / future work sentences
PATTERNS_LIMITATION = [
    re.compile(r"(?:memiliki|terdapat|menghadapi|adanya)\s+(?:beberapa\s+)?keterbatasan", re.IGNORECASE),
    re.compile(r"keterbatasan\s+(?:tersebut|penelitian|data|metode|sistem|penelitian ini|studi)", re.IGNORECASE),
    re.compile(r"(?:belum|kurang)\s+(?:sepenuhnya\s+)?(?:dapat\s+)?(?:mengakomodasi|mendukung|mencakup|optimal|tersedia|terintegrasi)", re.IGNORECASE),
    re.compile(r"(?:kendala|kelemahan|hambatan)\s+(?:yang\s+dihadapi|seperti|dalam|pada)", re.IGNORECASE),
    re.compile(r"(?:masih\s+bersifat|masih\s+menggunakan|saat\s+ini\s+masih)\s+(?:manual|konvensional|kertas|statis)", re.IGNORECASE),
    re.compile(r"(?:rentan\s+terhadap|celah\s+keamanan|risiko\s+kebocoran)", re.IGNORECASE),
    re.compile(r"(?:limitation|threats\s+to\s+validity|drawback|shortcoming|vulnerability)", re.IGNORECASE),
    re.compile(r"does\s+not\s+yet\s+support|main\s+limitation\s+of|restricted\s+to", re.IGNORECASE),
]

PATTERNS_FUTURE_WORK = [
    re.compile(r"saran\s+(?:yang\s+dapat\s+diberikan|pada\s+penelitian\s+selanjutnya|kedepannya|untuk\s+penelitian|perbaikan)", re.IGNORECASE),
    re.compile(r"rekomendasi\s+(?:pengembangan|perbaikan|penelitian\s+selanjutnya)", re.IGNORECASE),
    re.compile(r"(?:perlu|dapat)\s+(?:dilakukan|dibangun|dikembangkan|ditambahkan|diintegrasikan)\s+(?:penelitian|sistem|fitur|modul|pengujian)", re.IGNORECASE),
    re.compile(r"(?:diharapkan|berpotensi)\s+dapat\s+(?:dikembangkan|ditingkatkan|diterapkan|dijadikan)", re.IGNORECASE),
    re.compile(r"penelitian\s+(?:selanjutnya|mendatang|lanjutan)\s+(?:dapat|disarankan|diharapkan)", re.IGNORECASE),
    re.compile(r"(?:future\s+work|future\s+research|next\s+step|promising\s+direction|open\s+challenge)", re.IGNORECASE),
    re.compile(r"further\s+exploration|we\s+plan\s+to\s+extend|remains\s+an\s+open\s+issue", re.IGNORECASE),
]

PATTERNS_OPEN_PROBLEM = [
    re.compile(r"(?:permasalahan\s+utama|masalah\s+yang\s+sering\s+dihadapi|urgensi\s+permasalahan)", re.IGNORECASE),
    re.compile(r"(?:sulit\s+dalam|kesulitan\s+dalam|inefisiensi\s+pada|ketidaksesuaian\s+antara)", re.IGNORECASE),
    re.compile(r"(?:kebocoran\s+data|falsifikasi|manipulasi|pemalsuan\s+data)", re.IGNORECASE),
    re.compile(r"(?:open\s+problem|critical\s+gap|unresolved\s+issue|persistent\s+challenge)", re.IGNORECASE),
]

# Heading regexes for Markdown documents
HEADING_GAP_REGEX = re.compile(
    r"^(?:#{1,6}\s+.*)?\b(limitations?|threats?\s+to\s+validity|future\s+work|future\s+research|saran|rekomendasi|batasan\s+masalah|arah\s+penelitian|open\s+challenges?|kesenjangan|gap\s+penelitian)\b.*$",
    re.IGNORECASE,
)

# Weighted cluster keywords: (keyword, weight)
CLUSTER_WEIGHTED_KEYWORDS = {
    "security_privacy": [
        ("vapt", 4), ("penetration testing", 4), ("vulnerability", 3), ("differential privacy", 4),
        ("owasp", 3), ("curbstoning", 3), ("whistleblowing", 3), ("sdc", 3),
        ("keamanan", 2), ("privasi", 2), ("enkripsi", 2), ("serangan", 2),
        ("fraud", 3), ("pemalsuan", 3), ("zero trust", 3), ("audit trail", 3),
        ("jwt", 2), ("mfa", 2), ("mitm", 2), ("authenticat", 2),
    ],
    "sdi_interoperability": [
        ("satu data", 4), ("interoperabilitas", 3), ("simetris", 3), ("sdmx", 3),
        ("spbe", 3), ("api gateway", 3), ("gateway", 2), ("integrasi", 1),
        ("microservice", 2), ("metadata", 2), ("restful", 1), ("broker", 2), ("etl", 2),
        ("api", 1),
    ],
    "data_collection_capi": [
        ("capi", 4), ("cawi", 4), ("fasih", 4), ("shk", 3),
        ("pencacahan", 3), ("kuesioner", 2), ("data entri", 3), ("entri data", 3),
        ("survei", 1), ("sensus", 2), ("offline-first", 3), ("pwa", 2),
    ],
    "geospatial": [
        ("webgis", 4), ("spasial", 3), ("gis", 3), ("remote sensing", 3),
        ("citra satelit", 3), ("landsat", 3), ("rth", 3), ("osm", 2),
        ("peta", 2), ("geographically", 3), ("tata ruang", 2),
    ],
    "dissemination_dashboard": [
        ("dashboard", 3), ("disseminasi", 3), ("open data", 3), ("knowledge graph", 3),
        ("chatbot", 3), ("visualisasi", 2), ("portal", 2), ("shiny", 3),
        ("publikasi", 2), ("grafik", 1),
    ],
}


def classify_topic_cluster(text: str) -> str:
    """Classify text into a predefined SIS topic cluster based on weighted keyword scoring with word boundaries."""
    text_lower = text.lower()
    scores = {cluster: 0 for cluster in CLUSTER_WEIGHTED_KEYWORDS}

    for cluster, kw_list in CLUSTER_WEIGHTED_KEYWORDS.items():
        for kw, weight in kw_list:
            # Word boundary regex pattern
            pattern = rf"\b{re.escape(kw)}\b"
            matches = len(re.findall(pattern, text_lower))
            scores[cluster] += matches * weight

    best_cluster, highest_score = max(scores.items(), key=lambda item: item[1])
    if highest_score > 0:
        return best_cluster
    return "other"



def split_sentences_id(text: str) -> List[str]:
    """Split Indonesian/English text into sentences cleanly."""
    clean = re.sub(r"\s+", " ", text).strip()
    raw_sentences = re.split(r"(?<=[.!?])\s+", clean)
    sentences = []
    for s in raw_sentences:
        s = s.strip()
        if len(s) >= 20:  # ignore trivial sentence fragments
            sentences.append(s)
    return sentences


class ResearchGapExtractor:
    """Extracts research limitations, bottlenecks, and future recommendations from local documents."""

    def __init__(self, workspace_root: Optional[Path] = None):
        if workspace_root is None:
            # Default to workspace root
            self.workspace_root = Path(__file__).resolve().parent.parent.parent.parent
        else:
            self.workspace_root = Path(workspace_root)

        self.theses_json_path = self.workspace_root / "literature" / "theses_data.json"
        self.markdowns_dir = self.workspace_root / "literature" / "markdowns"
        self.literature_dir = self.workspace_root / "literature"
        self.proposals_dir = self.workspace_root / "proposals"
        self.brainstorming_dir = self.workspace_root / "brainstorming"

    def extract_from_theses_abstracts(
        self,
        cluster_filter: Optional[str] = None,
        min_year: Optional[int] = None,
        max_items: Optional[int] = None,
    ) -> List[ResearchGapItem]:
        """Mine limitations and future work recommendations from STIS theses dataset."""
        if not self.theses_json_path.exists():
            logger.warning("theses_data.json not found at %s", self.theses_json_path)
            return []

        try:
            with open(self.theses_json_path, "r", encoding="utf-8") as f:
                theses_list = json.load(f)
        except Exception as e:
            logger.error("Error reading %s: %s", self.theses_json_path, e)
            return []

        extracted_items: List[ResearchGapItem] = []

        for item in theses_list:
            thesis_id = item.get("id", "")
            title = item.get("judul", "").strip()
            author = item.get("penulis", "").strip().title()
            year_str = str(item.get("tahun", "")).strip()
            abstract = item.get("abstrak", "").strip()
            advisor = item.get("pembimbing", "").strip()
            peminatan = item.get("peminatan", "").strip()

            if not abstract or not title:
                continue

            try:
                year_int = int(year_str) if year_str.isdigit() else 0
                if min_year and year_int and year_int < min_year:
                    continue
            except ValueError:
                pass

            combined_text = f"{title} {item.get('kata_kunci', '')} {abstract}"
            cluster = classify_topic_cluster(combined_text)
            if cluster_filter and cluster != cluster_filter and cluster_filter != "all":
                continue

            # Parse sentences in abstract
            sentences = split_sentences_id(abstract)

            limitation_sentences: List[str] = []
            future_work_sentences: List[str] = []
            open_problem_sentences: List[str] = []

            for sent in sentences:
                is_future = any(p.search(sent) for p in PATTERNS_FUTURE_WORK)
                is_limitation = any(p.search(sent) for p in PATTERNS_LIMITATION)
                is_open = any(p.search(sent) for p in PATTERNS_OPEN_PROBLEM)

                if is_future:
                    future_work_sentences.append(sent)
                elif is_limitation:
                    limitation_sentences.append(sent)
                elif is_open:
                    open_problem_sentences.append(sent)

            # Synthesize items
            # 1. Future Work
            if future_work_sentences:
                excerpt = " ".join(future_work_sentences)
                gap_id = f"gap_stis_{thesis_id[:8]}_fw"
                extracted_items.append(
                    ResearchGapItem(
                        id=gap_id,
                        source_type="stis_thesis",
                        source_title=title,
                        year=year_str,
                        author=author,
                        cluster=cluster,
                        gap_category="future_work",
                        raw_excerpt=excerpt,
                        synthesized_summary=f"Saran riset lanjutan dari skripsi alumni ({author}, {year_str}): {excerpt[:200]}...",
                        recommended_opportunity=self._formulate_opportunity(excerpt, cluster, "future_work"),
                        source_location=f"literature/theses_data.json#{thesis_id}",
                        metadata={
                            "advisor": advisor,
                            "peminatan": peminatan,
                            "no_induk": item.get("no_induk", ""),
                        },
                    )
                )

            # 2. Methodological Limitation
            if limitation_sentences:
                excerpt = " ".join(limitation_sentences)
                gap_id = f"gap_stis_{thesis_id[:8]}_lim"
                extracted_items.append(
                    ResearchGapItem(
                        id=gap_id,
                        source_type="stis_thesis",
                        source_title=title,
                        year=year_str,
                        author=author,
                        cluster=cluster,
                        gap_category="methodological_bottleneck",
                        raw_excerpt=excerpt,
                        synthesized_summary=f"Limitasi/kendala metodologi pada {title}: {excerpt[:200]}...",
                        recommended_opportunity=self._formulate_opportunity(excerpt, cluster, "methodological_bottleneck"),
                        source_location=f"literature/theses_data.json#{thesis_id}",
                        metadata={
                            "advisor": advisor,
                            "peminatan": peminatan,
                            "no_induk": item.get("no_induk", ""),
                        },
                    )
                )

            # 3. Open Problem in Object
            if open_problem_sentences and not limitation_sentences:
                excerpt = " ".join(open_problem_sentences)
                gap_id = f"gap_stis_{thesis_id[:8]}_prob"
                extracted_items.append(
                    ResearchGapItem(
                        id=gap_id,
                        source_type="stis_thesis",
                        source_title=title,
                        year=year_str,
                        author=author,
                        cluster=cluster,
                        gap_category="open_problem",
                        raw_excerpt=excerpt,
                        synthesized_summary=f"Masalah operasional/lapangan pada objek {title}: {excerpt[:200]}...",
                        recommended_opportunity=self._formulate_opportunity(excerpt, cluster, "open_problem"),
                        source_location=f"literature/theses_data.json#{thesis_id}",
                        metadata={
                            "advisor": advisor,
                            "peminatan": peminatan,
                            "no_induk": item.get("no_induk", ""),
                        },
                    )
                )

            if max_items and len(extracted_items) >= max_items:
                break

        return extracted_items

    def extract_from_markdown_sections(
        self,
        cluster_filter: Optional[str] = None,
        target_dirs: Optional[List[str]] = None,
    ) -> List[ResearchGapItem]:
        """Scan Markdown files for explicit Limitation, Future Work, and Discussion sections."""
        if target_dirs is None:
            search_dirs = [
                self.markdowns_dir,
                self.literature_dir,
                self.proposals_dir,
                self.brainstorming_dir,
            ]
        else:
            search_dirs = [self.workspace_root / d for d in target_dirs]

        extracted_items: List[ResearchGapItem] = []

        for sdir in search_dirs:
            if not sdir.exists():
                continue
            for md_path in sdir.rglob("*.md"):
                # Skip templates or non-content files
                if md_path.name in ("README.md", "AGENTS.md", "references.md"):
                    continue
                try:
                    rel_path = md_path.relative_to(self.workspace_root).as_posix()
                except ValueError:
                    rel_path = md_path.name

                with open(md_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                current_gap_heading: Optional[str] = None
                current_gap_lines: List[Tuple[int, str]] = []
                current_gap_level = 0

                doc_title = md_path.stem.replace("_", " ")

                for line_idx, line in enumerate(lines, start=1):
                    heading_match = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
                    if heading_match:
                        hashes, h_text = heading_match.groups()
                        h_level = len(hashes)

                        # If we were collecting a gap section and encountered same or higher level heading, flush it
                        if current_gap_heading and h_level <= current_gap_level:
                            item = self._create_md_gap_item(
                                current_gap_heading,
                                current_gap_lines,
                                md_path,
                                rel_path,
                                doc_title,
                                cluster_filter,
                            )
                            if item:
                                extracted_items.append(item)
                            current_gap_heading = None
                            current_gap_lines = []

                        # Check if this heading is a limitation/future work heading
                        if HEADING_GAP_REGEX.match(line.strip()):
                            current_gap_heading = h_text.strip()
                            current_gap_level = h_level
                            current_gap_lines = []
                        elif not current_gap_heading and ("pembahasan" in h_text.lower() or "diskusi" in h_text.lower()):
                            current_gap_heading = h_text.strip()
                            current_gap_level = h_level
                            current_gap_lines = []
                    else:
                        if current_gap_heading:
                            current_gap_lines.append((line_idx, line))

                # Flush last section if any
                if current_gap_heading and current_gap_lines:
                    item = self._create_md_gap_item(
                        current_gap_heading,
                        current_gap_lines,
                        md_path,
                        rel_path,
                        doc_title,
                        cluster_filter,
                    )
                    if item:
                        extracted_items.append(item)

        return extracted_items

    def extract_from_hybrid_search(
        self,
        query: str,
        cluster_filter: Optional[str] = None,
        top_k: int = 5,
    ) -> List[ResearchGapItem]:
        """Use the Hybrid Search Engine to retrieve contextually relevant gap snippets."""
        try:
            from calm_carson.search import create_search_engine
            engine = create_search_engine(workspace_root=self.workspace_root)
            results = engine.search(query, top_k=top_k * 2, mode="hybrid")
        except Exception as e:
            logger.warning("Hybrid search engine unavailable or error: %s", e)
            return []

        gap_items: List[ResearchGapItem] = []
        for r in results:
            content = r.content
            # Check if chunk contains limitation or future work cues
            has_lim = any(p.search(content) for p in PATTERNS_LIMITATION)
            has_fw = any(p.search(content) for p in PATTERNS_FUTURE_WORK)
            has_open = any(p.search(content) for p in PATTERNS_OPEN_PROBLEM)

            if not (has_lim or has_fw or has_open):
                continue

            cluster = classify_topic_cluster(f"{r.file_path} {r.breadcrumb} {content}")
            if cluster_filter and cluster != cluster_filter and cluster_filter != "all":
                continue

            cat = "future_work" if has_fw else ("methodological_bottleneck" if has_lim else "open_problem")

            gap_id = f"gap_hybrid_{r.chunk_id[:8]}"
            gap_items.append(
                ResearchGapItem(
                    id=gap_id,
                    source_type="intl_paper" if "INTL" in r.file_path or "reviews" in r.file_path else "proposal_note",
                    source_title=r.file_path.split("/")[-1].replace(".md", ""),
                    year="2024-2026",
                    author=r.breadcrumb.split(" > ")[-1] if " > " in r.breadcrumb else "Dokumen Workspace",
                    cluster=cluster,
                    gap_category=cat,
                    raw_excerpt=content[:600],
                    synthesized_summary=f"Temuan penelusuran hybrid ({r.file_path}:{r.start_line}): {content[:150]}...",
                    recommended_opportunity=self._formulate_opportunity(content[:400], cluster, cat),
                    source_location=f"{r.file_path}:{r.start_line}-{r.end_line}",
                    metadata={"rrf_score": r.score, "breadcrumb": r.breadcrumb},
                )
            )
            if len(gap_items) >= top_k:
                break

        return gap_items

    def extract_all(
        self,
        cluster_filter: Optional[str] = None,
        min_year: Optional[int] = 2021,
    ) -> List[ResearchGapItem]:
        """Run comprehensive gap extraction across STIS theses, Markdowns, and review catalogs."""
        items: List[ResearchGapItem] = []
        seen_summaries = set()

        # 1. Mine STIS abstracts
        theses_items = self.extract_from_theses_abstracts(cluster_filter=cluster_filter, min_year=min_year)
        for it in theses_items:
            key = it.source_title.lower() + it.gap_category
            if key not in seen_summaries:
                seen_summaries.add(key)
                items.append(it)

        # 2. Mine Markdown sections
        md_items = self.extract_from_markdown_sections(cluster_filter=cluster_filter)
        for it in md_items:
            key = it.source_title.lower() + it.gap_category
            if key not in seen_summaries:
                seen_summaries.add(key)
                items.append(it)

        return items

    def _create_md_gap_item(
        self,
        heading_text: str,
        lines: List[Tuple[int, str]],
        md_path: Path,
        rel_path: str,
        doc_title: str,
        cluster_filter: Optional[str],
    ) -> Optional[ResearchGapItem]:
        """Convert collected markdown lines into a ResearchGapItem."""
        if not lines:
            return None

        content = "".join([l[1] for l in lines]).strip()
        if len(content) < 40:
            return None

        start_line = lines[0][0]
        end_line = lines[-1][0]

        h_lower = heading_text.lower()
        if any(w in h_lower for w in ("future", "saran", "rekomendasi", "arah")):
            cat = "future_work"
        elif any(w in h_lower for w in ("limitation", "batasan", "kelemahan", "threats")):
            cat = "methodological_bottleneck"
        else:
            cat = "open_problem"

        cluster = classify_topic_cluster(f"{rel_path} {heading_text} {content}")
        if cluster_filter and cluster != cluster_filter and cluster_filter != "all":
            return None

        source_type = "intl_paper" if "INTL" in rel_path or "reviews" in rel_path else "proposal_note"
        gap_id = f"gap_md_{md_path.stem[:8]}_{start_line}"

        return ResearchGapItem(
            id=gap_id,
            source_type=source_type,
            source_title=doc_title,
            year="2024",
            author=rel_path.split("/")[0].capitalize(),
            cluster=cluster,
            gap_category=cat,
            raw_excerpt=content[:800],
            synthesized_summary=f"Bagian '{heading_text}' pada {rel_path} (L{start_line}-L{end_line}): {content[:180]}...",
            recommended_opportunity=self._formulate_opportunity(content, cluster, cat),
            source_location=f"{rel_path}:{start_line}-{end_line}",
            metadata={"heading": heading_text},
        )

    def _formulate_opportunity(self, text: str, cluster: str, cat: str) -> str:
        """Formulate a research opportunity recommendation tailored to STIS D-IV SIS requirements."""
        if cluster == "security_privacy":
            if cat == "methodological_bottleneck":
                return "Mengembangkan arsitektur proteksi data mikro real-time dengan integrasi Differential Privacy matematis dan tamper-evident cryptographic audit trail berbasis API, menggantikan proses masking offline statis."
            elif cat == "future_work":
                return "Mengimplementasikan automated security pipeline (DevSecOps SAST/DAST) dan mitigasi serangan rekonstruksi data pada endpoint API layanan statistik."
            else:
                return "Merancang secure query proxy dengan dynamic privacy budgeting (epsilon) untuk kepatuhan UU Perlindungan Data Pribadi pada diseminasi data BPS."

        elif cluster == "sdi_interoperability":
            if cat == "methodological_bottleneck":
                return "Membangun API Gateway Satu Data Indonesia terintegrasi dengan validasi skema semantik otomatis (SDMX/SIMETRIS) dan zero-trust mTLS untuk pertukaran data lintas K/L/D."
            elif cat == "future_work":
                return "Menambahkan otomasi penilaian kualitas metadata statistik menggunakan representasi graf atau semantic matcher untuk standardisasi metadata sektoral."
            else:
                return "Mengembangkan middleware interoperabilitas SPBE dengan message broker terdistribusi guna mengatasi latensi dan inkonsistensi data antar-OPD."

        elif cluster == "data_collection_capi":
            if cat == "methodological_bottleneck":
                return "Mengembangkan modul backend deteksi anomali entri data survei real-time berbasis analisis paradatak (dwell-time dan urutan pengisian) untuk memitigasi falsifikasi pencacahan mitra."
            elif cat == "future_work":
                return "Mengintegrasikan enkripsi data mikro terisolasi pada database lokal SQLite perangkat pencacah CAPI serta automated integrity verification saat transmisi sinkronisasi."
            else:
                return "Membangun asisten validasi data entri pintar pada CAPI untuk mendeteksi inkonsistensi jawaban secara instan di lapangan."

        elif cluster == "geospatial":
            return "Mengembangkan platform WebGIS interaktif dengan komputasi spasial terdistribusi untuk otomasi pemutakhiran peta sensus dan integrasi data geospasial tematik."

        elif cluster == "dissemination_dashboard":
            return "Merancang arsitektur diseminasi data statistik modern berbasis Semantic Knowledge Graph atau Conversational RAG yang aman untuk pencarian indikator makro/mikro."

        return "Mengembangkan artefak sistem informasi statistik berbasis DSRM yang mengotomasi pemrosesan data, pengujian ISO/IEC 25010, dan integrasi fase GSBPM."
