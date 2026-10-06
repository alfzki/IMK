"""Evidence collector that gathers context, empirical statistics, citations, and previous alumni theses from local corpus."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from calm_carson.drafting.models import ChapterOutline, EvidenceItem, SubSectionOutline
from calm_carson.verify.decomposer import extract_citations, extract_quantities

logger = logging.getLogger(__name__)


class EvidenceCollector:
    """Collects multi-source evidence from Markdown hybrid search, theses database, gaps DB, and empirical banks."""

    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        search_engine: Optional[Any] = None,
        allow_simpus_theses: bool = False,
    ):
        if workspace_root is None:
            self.workspace_root = Path(__file__).resolve().parent.parent.parent.parent
        else:
            self.workspace_root = Path(workspace_root)

        self.allow_simpus_theses = allow_simpus_theses
        self.search_engine = search_engine
        if self.search_engine is None:
            try:
                from calm_carson.search.hybrid import MarkdownHybridSearchEngine

                index_dir = self.workspace_root / "literature" / "search_index"
                if index_dir.exists():
                    self.search_engine = MarkdownHybridSearchEngine(index_dir=str(index_dir))
            except Exception as e:
                logger.warning("Hybrid search engine could not be initialized in EvidenceCollector: %s", e)
                self.search_engine = None

        # Load metadata caches
        self._theses_db: List[Dict[str, Any]] = self._load_json(self.workspace_root / "literature" / "theses_data.json") if allow_simpus_theses else []
        self._verified_papers: List[Dict[str, Any]] = self._load_json(self.workspace_root / "references" / "verified_papers.json")
        self._gaps_db: List[Dict[str, Any]] = self._load_json(self.workspace_root / "literature" / "brainstorming_gaps.json")
        self._bank_masalah: str = self._load_text(self.workspace_root / "proposals" / "bank_data_masalah_proposal.md")

    def _load_json(self, path: Path) -> List[Dict[str, Any]]:
        if not path.exists():
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception as e:
            logger.warning("Failed to load JSON %s: %s", path, e)
            return []

    def _load_text(self, path: Path) -> str:
        if not path.exists():
            return ""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.warning("Failed to load text %s: %s", path, e)
            return ""

    def collect_for_subsection(
        self,
        subsection: SubSectionOutline,
        topic_info: Dict[str, Any],
        max_items: int = 4,
    ) -> List[EvidenceItem]:
        """Gathers relevant evidence passages for a specific subsection."""
        evidences: List[EvidenceItem] = []

        # 1. Query Hybrid Search Engine
        if self.search_engine is not None and subsection.search_queries:
            query = " ".join(subsection.search_queries[:2])
            if subsection.target_quantities:
                query += " " + " ".join(subsection.target_quantities[:2])

            try:
                results = self.search_engine.search(query, top_k=max_items, mode="hybrid")
                for r in results:
                    content = r.content.strip()
                    evidences.append(
                        EvidenceItem(
                            source=getattr(r, "doc_path", "corpus_markdown"),
                            content=content,
                            line_reference=f"L{r.start_line}-L{r.end_line}",
                            relevance_score=getattr(r, "rrf_score", 0.5),
                            extracted_citations=extract_citations(content),
                            extracted_numbers=extract_quantities(content),
                        )
                    )
            except Exception as e:
                logger.warning("Hybrid search query failed for %s: %s", subsection.id, e)

        # 2. Extract from Bank Data Masalah if relevant to Chapter 1
        if subsection.id.startswith("1.1") and self._bank_masalah:
            topic_id = topic_info.get("id", "")
            passages = self._extract_bank_masalah_passages(topic_id)
            for p in passages:
                evidences.append(
                    EvidenceItem(
                        source="proposals/bank_data_masalah_proposal.md",
                        content=p["content"],
                        line_reference=p.get("line_ref", "L1-L50"),
                        relevance_score=0.95,
                        extracted_citations=extract_citations(p["content"]),
                        extracted_numbers=extract_quantities(p["content"]),
                    )
                )

        # 3. Pull benchmarking literature if relevant to Chapter 2
        if subsection.id.startswith("2.2") or subsection.id.startswith("2.3"):
            cluster = topic_info.get("cluster", "")
            if self.allow_simpus_theses:
                theses_items = self._find_relevant_theses(cluster, limit=3)
                for t in theses_items:
                    content = f"Skripsi STIS ({t.get('year', '')}) oleh {t.get('author', '')}: '{t.get('title', '')}'. Pembimbing: {t.get('advisor', '')}. Abstrak: {t.get('abstract', '')[:300]}..."
                    evidences.append(
                        EvidenceItem(
                            source="literature/theses_data.json",
                            content=content,
                            line_reference=f"ID:{t.get('id', '')}",
                            relevance_score=0.85,
                            extracted_citations=[f"[Skripsi STIS {t.get('year', '')}]"],
                            extracted_numbers=extract_quantities(content),
                        )
                    )
            else:
                papers_items = self._find_relevant_verified_papers(cluster, limit=3)
                for p in papers_items:
                    cite_tag = p.get('filename', '').replace('.pdf', '')
                    content = f"Publikasi Ilmiah ({p.get('year', '')}) oleh {p.get('author', '')}: '{p.get('title', '')}'. Jurnal: {p.get('journal', '')}. Metode: {p.get('methods', '')}. DOI: {p.get('doi', '')}."
                    evidences.append(
                        EvidenceItem(
                            source=p.get('local_path', 'references/verified_papers.json'),
                            content=content,
                            line_reference=f"DOI:{p.get('doi', '')}",
                            relevance_score=0.90,
                            extracted_citations=[f"\\cite{{{cite_tag}}}"],
                            extracted_numbers=extract_quantities(content),
                        )
                    )

        # 4. Pull Research Gaps if relevant to Section 2.4
        if subsection.id.startswith("2.4") and self._gaps_db:
            cluster = topic_info.get("cluster", "")
            matched_gaps = [g for g in self._gaps_db if g.get("cluster") == cluster or not cluster][:3]
            for g in matched_gaps:
                content = f"Kesenjangan Riset [{g.get('gap_category', '')}]: {g.get('synthesized_summary', '')}. Rekomendasi Peluang: {g.get('recommended_opportunity', '')}"
                evidences.append(
                    EvidenceItem(
                        source="literature/brainstorming_gaps.json",
                        content=content,
                        line_reference=f"Gap-ID:{g.get('id', '')}",
                        relevance_score=0.90,
                        extracted_citations=[],
                        extracted_numbers=extract_quantities(content),
                    )
                )

        return evidences[:max_items * 2]

    def collect_for_chapter(
        self,
        chapter: ChapterOutline,
        topic_info: Dict[str, Any],
    ) -> Dict[str, List[EvidenceItem]]:
        """Collects evidence for all subsections in a chapter."""
        chapter_evidence: Dict[str, List[EvidenceItem]] = {}
        for sub in chapter.subsections:
            chapter_evidence[sub.id] = self.collect_for_subsection(sub, topic_info)
        return chapter_evidence

    def _extract_bank_masalah_passages(self, topic_id: str) -> List[Dict[str, str]]:
        """Extracts specific problem blocks from bank_data_masalah_proposal.md."""
        passages = []
        if not self._bank_masalah:
            return []

        key_marker = "TOPIK 1"
        if "topik_2" in topic_id:
            key_marker = "TOPIK 2"
        elif "topik_3" in topic_id:
            key_marker = "TOPIK 3"

        sections = self._bank_masalah.split("## ")
        for sec in sections:
            if key_marker in sec:
                # Break into Masalah 1, Masalah 2, Masalah 3
                parts = sec.split("### ")
                for p in parts[1:]:
                    lines = p.strip().splitlines()
                    title = lines[0] if lines else "Masalah"
                    content = "\n".join(lines[:12])
                    passages.append({
                        "title": title,
                        "content": content,
                        "line_ref": f"Bank-{key_marker}-{title[:15]}",
                    })
        return passages

    def _find_relevant_theses(self, cluster: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Finds top relevant STIS theses matching the cluster."""
        matched = []
        for t in self._theses_db:
            abstract = str(t.get("abstract", "")).lower()
            title = str(t.get("title", "")).lower()
            keywords = str(t.get("keywords", "")).lower()

            if cluster == "data_collection" and ("survei" in title or "capi" in title or "mitra" in title):
                matched.append(t)
            elif cluster == "interoperability_sdi" and ("metadata" in title or "integrasi" in title or "spbe" in title):
                matched.append(t)
            elif cluster == "security_privacy" and ("privasi" in title or "keamanan" in title or "kriptografi" in title):
                matched.append(t)

            if len(matched) >= limit:
                break

        if not matched and self._theses_db:
            matched = self._theses_db[:limit]

        return matched

    def _find_relevant_verified_papers(self, cluster: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Finds top relevant peer-reviewed papers matching cluster or HCI / Information Systems themes."""
        matched = []
        for p in self._verified_papers:
            title = str(p.get("title", "")).lower()
            methods = str(p.get("methods", "")).lower()
            relevance = str(p.get("relevance", "")).lower()
            all_text = f"{title} {methods} {relevance}"
            if cluster == "data_collection" and ("survey" in all_text or "kuesioner" in all_text or "webqual" in all_text):
                matched.append(p)
            elif cluster == "interoperability_sdi" and ("portal" in all_text or "government" in all_text or "architecture" in all_text):
                matched.append(p)
            elif cluster == "security_privacy" and ("privacy" in all_text or "security" in all_text or "risiko" in all_text):
                matched.append(p)
            elif any(k in all_text for k in ["usability", "ucd", "heuristic", "webqual", "interaction", "interface", "experience"]):
                matched.append(p)

            if len(matched) >= limit:
                break

        if not matched and self._verified_papers:
            matched = self._verified_papers[:limit]

        return matched
