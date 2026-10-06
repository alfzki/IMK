"""Evaluator for calculating semantic similarity, topic overlap risks, and differentiation feedback."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import numpy as np

from calm_carson.originality.models import (
    DifferentiationFeedback,
    OriginalityReport,
    PublicationMatch,
)

logger = logging.getLogger(__name__)


class OriginalityEvaluator:
    """Evaluates idea novelty, computes dense semantic similarities, and provides critical differentiation advice."""

    def __init__(self, embedding_engine: Optional[Any] = None):
        if embedding_engine is not None:
            self.embedding_engine = embedding_engine
        else:
            try:
                from calm_carson.search.dense import DenseEmbeddingEngine
                self.embedding_engine = DenseEmbeddingEngine()
            except Exception as e:
                logger.warning("Could not initialize DenseEmbeddingEngine: %s", e)
                self.embedding_engine = None

    def evaluate(
        self,
        idea_text: str,
        raw_publications: List[Dict[str, Any]],
        generated_queries: Optional[List[str]] = None,
    ) -> OriginalityReport:
        """Evaluates semantic similarity between user idea and retrieved publications."""
        if not raw_publications:
            return OriginalityReport(
                idea_text=idea_text,
                generated_queries=generated_queries or [],
                matches=[],
                max_similarity=0.0,
                mean_similarity=0.0,
                overall_risk="DISTINCT_NOVEL",
                risk_summary="Tidak ditemukan publikasi ilmiah yang relevan atau tumpang tindih secara langsung. Ide memiliki ruang kebaruan yang sangat luas.",
                differentiation_feedbacks=self._generate_feedbacks(idea_text, 0.0, []),
            )

        # Prepare text representation for each paper: Title + Abstract
        paper_texts = []
        for p in raw_publications:
            title = p.get("title", "")
            abstract = p.get("abstract", "")
            # Truncate abstract to 500 chars to avoid diluting key thematic focus
            text_repr = f"{title}. {abstract[:500]}" if abstract else title
            paper_texts.append(text_repr)

        # Calculate cosine similarities
        if self.embedding_engine is not None:
            idea_emb = self.embedding_engine.encode([idea_text])[0]
            papers_emb = self.embedding_engine.encode(paper_texts)
            # Dot product (since embeddings are L2 normalized)
            similarities = np.dot(papers_emb, idea_emb).tolist()
        else:
            # Fallback lexical Jaccard similarity if dense model unavailable
            similarities = [self._jaccard_similarity(idea_text, pt) for pt in paper_texts]

        matches: List[PublicationMatch] = []
        for p, sim in zip(raw_publications, similarities):
            sim_score = max(0.0, min(1.0, float(sim)))

            if sim_score >= 0.70:
                overlap_level = "HIGH"
            elif sim_score >= 0.45:
                overlap_level = "MODERATE"
            else:
                overlap_level = "LOW"

            matches.append(
                PublicationMatch(
                    id=str(p.get("id", "")),
                    title=p.get("title", ""),
                    authors=p.get("authors", []),
                    year=int(p.get("year", 2024)),
                    venue=p.get("venue", ""),
                    doi=p.get("doi"),
                    url=p.get("url"),
                    abstract=p.get("abstract", ""),
                    citation_count=int(p.get("citation_count", 0)),
                    similarity_score=round(sim_score, 4),
                    overlap_level=overlap_level,
                    source_database=p.get("source_database", "openalex"),
                )
            )

        # Sort matches by similarity score descending
        matches.sort(key=lambda m: m.similarity_score, reverse=True)

        max_sim = matches[0].similarity_score if matches else 0.0
        top_k = matches[:10]
        mean_sim = float(np.mean([m.similarity_score for m in top_k])) if top_k else 0.0

        # Assess overall risk
        high_count = sum(1 for m in matches if m.overlap_level == "HIGH")
        if max_sim >= 0.75 or high_count >= 2:
            overall_risk = "HIGH_OVERLAP"
            risk_summary = (
                f"Tingkat tumpang tindih TINGGI ({max_sim:.2f} max similarity, {high_count} paper sangat serupa). "
                "Terdapat publikasi internasional yang mengkaji permasalahan dan metodologi hampir identik. "
                "Wajib mempertegas aspek pembeda (novelty) pada arsitektur sistem, karakteristik data BPS, dan pengujian empiris."
            )
        elif max_sim >= 0.50:
            overall_risk = "MODERATE_OVERLAP"
            risk_summary = (
                f"Tingkat tumpang tindih SEDANG ({max_sim:.2f} max similarity). "
                "Lanskap literatur global telah memiliki penelitian dalam domain serupa, namun terdapat celah riset "
                "yang dapat dieksplorasi sebagai kontribusi baru bagi sistem informasi statistik di Indonesia."
            )
        else:
            overall_risk = "DISTINCT_NOVEL"
            risk_summary = (
                f"Tingkat tumpang tindih RENDAH ({max_sim:.2f} max similarity). "
                "Ide memiliki diferensiasi yang kuat terhadap literatur global arus utama dan belum banyak dieksplorasi."
            )

        feedbacks = self._generate_feedbacks(idea_text, max_sim, matches[:3])

        return OriginalityReport(
            idea_text=idea_text,
            generated_queries=generated_queries or [],
            matches=matches,
            max_similarity=max_sim,
            mean_similarity=mean_sim,
            overall_risk=overall_risk,
            risk_summary=risk_summary,
            differentiation_feedbacks=feedbacks,
        )

    def _generate_feedbacks(
        self,
        idea_text: str,
        max_sim: float,
        top_matches: List[PublicationMatch],
    ) -> List[DifferentiationFeedback]:
        """Generates structured differentiation advice across 5 strategic dimensions."""
        idea_lower = idea_text.lower()
        feedbacks: List[DifferentiationFeedback] = []

        # 1. Metodologi & Algoritma
        overlap_note = ""
        if top_matches:
            top = top_matches[0]
            overlap_note = f"Publikasi terdahulu seperti '{top.title}' ({top.year}) umumnya telah mengeksplorasi konsep dasar tersebut."

        feedbacks.append(
            DifferentiationFeedback(
                dimension="methodology_algorithm",
                dimension_name="Metodologi & Arsitektur Algoritma",
                overlap_analysis=overlap_note or "Penelitian global sering menggunakan pendekatan batch statis atau model analitik generik.",
                recommended_differentiation=(
                    "Transisikan sistem dari pemrosesan statis/offline ke arsitektur real-time streaming atau on-demand query. "
                    "Jika menggunakan machine learning, padukan teknik deteksi sequence-aware (misal dwell-time dan urutan pengisian) "
                    "atau mekanisme privasi matematis formal (Laplace/Gaussian mechanism dengan dynamic privacy budget tracking)."
                ),
                actionable_guidance=(
                    "Gunakan framework modern berlatensi rendah (misal FastAPI atau Go) dengan pemisahan microservices "
                    "dan pengamanan endpoint RESTful API terstandar OWASP API Top 10."
                ),
            )
        )

        # 2. Karakteristik Data Statistik Resmi Indonesia (BPS)
        feedbacks.append(
            DifferentiationFeedback(
                dimension="data_characteristics",
                dimension_name="Spesifisitas & Kompleksitas Data Statistik BPS",
                overlap_analysis="Penelitian internasional sebagian besar menggunakan dataset publik global (seperti US Census, Kaggle, atau dataset akademik).",
                recommended_differentiation=(
                    "Fokuskan pada struktur dan kompleksitas unik data survei/sensus Badan Pusat Statistik (BPS), "
                    "seperti hierarki kuesioner berlapis (blok sensus, rumah tangga, individu), format kode klasifikasi nasional (KBLI/KBKI), "
                    "dan keterbatasan infrastruktur jaringan lapangan (kebutuhan offline-first CAPI)."
                ),
                actionable_guidance=(
                    "Susun skenario evaluasi menggunakan data sintetis yang meniru persis skema kuesioner resmi BPS "
                    "(misal: Survei Harga Konsumen / Sakernas / Susenas) agar relevan dengan tugas fungsi BPS."
                ),
            )
        )

        # 3. Rekayasa Perangkat Lunak & Artefak DSRM
        feedbacks.append(
            DifferentiationFeedback(
                dimension="dsrm_system_engineering",
                dimension_name="Rekayasa Perangkat Lunak & Artefak Sistem (DSRM)",
                overlap_analysis="Banyak publikasi akademik di bidang komputer murni berhenti pada eksperimen notebook / proof-of-concept tanpa artefak perangkat lunak utuh.",
                recommended_differentiation=(
                    "Jadikan rekayasa sistem informasi statistik berbasis Design Science Research Methodology (DSRM) sebagai pembeda utama: "
                    "bangun artefak aplikasi/middleware end-to-end yang dapat diuji dan didemonstrasikan langsung saat sidang skripsi."
                ),
                actionable_guidance=(
                    "Sertakan fitur enterprise-grade: tamper-evident cryptographic audit trail (hash chaining SHA-256), "
                    "role-based access control (RBAC/JWT), dan automated health-check / logging."
                ),
            )
        )

        # 4. Kepatuhan Regulasi Nasional (UU PDP & SPBE)
        feedbacks.append(
            DifferentiationFeedback(
                dimension="regulatory_compliance",
                dimension_name="Kepatuhan Regulasi Nasional (UU PDP & SPBE)",
                overlap_analysis="Paper internasional mengacu pada regulasi asing (GDPR di Eropa atau HIPAA di AS) yang memiliki konteks hukum berbeda.",
                recommended_differentiation=(
                    "Jadikan kepatuhan terhadap UU No. 27 Tahun 2022 tentang Perlindungan Data Pribadi (UU PDP) "
                    "dan Perpres No. 39 Tahun 2019 tentang Satu Data Indonesia (SDI) sebagai justifikasi urgensi penelitian."
                ),
                actionable_guidance=(
                    "Tautkan batasan teknis sistem dengan pasal kewajiban pengendali data spesifik dalam UU PDP "
                    "(misal hak penghapusan data, pencegahan re-identifikasi data individu, dan transparansi pemrosesan)."
                ),
            )
        )

        # 5. Metrik Evaluasi Komprehensif (ISO/IEC 25010)
        feedbacks.append(
            DifferentiationFeedback(
                dimension="evaluation_metrics",
                dimension_name="Standar Evaluasi Kualitas Perangkat Lunak (ISO/IEC 25010)",
                overlap_analysis="Publikasi sejenis umumnya hanya mengukur satu aspek sempit (misal akurasi model saja atau latensi jaringan saja).",
                recommended_differentiation=(
                    "Terapkan pengujian multi-dimensi standar ISO/IEC 25010: Functional Suitability (Black-box testing), "
                    "Performance Efficiency (stress test latensi/throughput), Usability (SUS/UEQ), dan Security (VAPT / OWASP ZAP)."
                ),
                actionable_guidance=(
                    "Sajikan perbandingan kuantitatif sebelum dan sesudah implementasi sistem untuk membuktikan dampak nyata solusi."
                ),
            )
        )

        return feedbacks

    def _jaccard_similarity(self, text_a: str, text_b: str) -> float:
        """Simple fallback lexical token similarity."""
        tokens_a = set(text_a.lower().split())
        tokens_b = set(text_b.lower().split())
        if not tokens_a or not tokens_b:
            return 0.0
        intersection = len(tokens_a.intersection(tokens_b))
        union = len(tokens_a.union(tokens_b))
        return float(intersection) / float(union) if union > 0 else 0.0
