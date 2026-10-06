"""Logical alignment evaluator and citation verifier for factual claims."""

from __future__ import annotations

import logging
import re
from typing import Any, List, Optional, Tuple

import numpy as np

from calm_carson.verify.decomposer import extract_quantities
from calm_carson.verify.models import (
    ClaimVerificationResult,
    EvidenceMatch,
    FactClaim,
    VerificationReport,
)

logger = logging.getLogger(__name__)


class FactVerifier:
    """Verifies factual claims against retrieved evidence, evaluating alignment and citation status."""

    def __init__(self, embedding_engine: Optional[Any] = None):
        if embedding_engine is not None:
            self.embedding_engine = embedding_engine
        else:
            try:
                from calm_carson.search.dense import DenseEmbeddingEngine
                self.embedding_engine = DenseEmbeddingEngine()
            except Exception as e:
                logger.warning("DenseEmbeddingEngine not available: %s", e)
                self.embedding_engine = None

    def verify_claim(
        self,
        claim: FactClaim,
        evidences: List[EvidenceMatch],
    ) -> ClaimVerificationResult:
        """Verifies a single claim against candidate evidence passages."""
        if not evidences:
            return ClaimVerificationResult(
                claim=claim,
                status="UNSUPPORTED",
                citation_status="NOT_APPLICABLE" if not claim.embedded_citations else "MISMATCH",
                confidence_score=0.0,
                best_evidence=None,
                alternative_evidences=[],
                explanation="Tidak ditemukan bukti pendukung dalam korpus dokumen lokal untuk memverifikasi klaim ini.",
                correction_suggestion="Sertakan rujukan literatur atau bukti empiris resmi untuk klaim ini.",
                annotated_claim=f"{claim.original_sentence} [❓ TIDAK BERDASAR: belum ada rujukan di korpus]",
            )

        # 1. Compute semantic similarities with evidence passages
        best_evidence: Optional[EvidenceMatch] = None
        highest_sim = 0.0

        if self.embedding_engine is not None:
            claim_emb = self.embedding_engine.encode([claim.claim_text])[0]
            ev_texts = [e.content[:600] for e in evidences]
            ev_embs = self.embedding_engine.encode(ev_texts)
            similarities = np.dot(ev_embs, claim_emb).tolist()
        else:
            # Fallback lexical Jaccard
            similarities = [self._jaccard_similarity(claim.claim_text, e.content) for e in evidences]

        # Update evidence similarity scores and find the best candidate
        for e, sim in zip(evidences, similarities):
            sim_score = max(0.0, min(1.0, float(sim)))
            e.similarity_score = round(sim_score, 4)
            if sim_score > highest_sim:
                highest_sim = sim_score
                best_evidence = e

        if best_evidence is None or highest_sim < 0.25:
            return ClaimVerificationResult(
                claim=claim,
                status="UNSUPPORTED",
                citation_status="NOT_APPLICABLE" if not claim.embedded_citations else "MISMATCH",
                confidence_score=highest_sim,
                best_evidence=best_evidence,
                alternative_evidences=evidences[1:],
                explanation="Kemiripan semantik dengan korpus terlalu rendah (< 0.25). Tidak ditemukan fakta yang relevan.",
                correction_suggestion="Pastikan klaim mengacu pada temuan atau data yang terdokumentasi di korpus.",
                annotated_claim=f"{claim.original_sentence} [❓ TIDAK BERDASAR: skor kemiripan {highest_sim*100:.1f}%]",
            )

        # 2. Check for numerical alignment or contradiction
        is_contradicted, contra_detail = self._check_numeric_contradiction(claim, best_evidence)
        correction_suggestion: Optional[str] = None

        # 3. Determine Verification Status
        if is_contradicted:
            status = "CONTRADICTED"
            citation_status = "MISMATCH"
            explanation = f"Terdeteksi kontradiksi data faktual: {contra_detail}."
            correction_suggestion = f"Koreksi angka/pernyataan sesuai bukti di `{best_evidence.file_path}:L{best_evidence.start_line}`: {contra_detail}."
            annotated_claim = (
                f"{claim.original_sentence} "
                f"[⚠️ KONTRADIKSI: {contra_detail} (lihat `{best_evidence.file_path}:L{best_evidence.start_line}`)]"
            )

        elif highest_sim >= 0.40:
            status = "SUPPORTED"
            # 4. Check Citation Status
            citation_status, cit_explanation, recommended_cite = self._check_citation_status(claim, best_evidence)

            if citation_status == "VALID":
                explanation = f"Klaim didukung penuh oleh bukti di `{best_evidence.file_path}:L{best_evidence.start_line}` dan menyertakan sitasi yang valid."
                annotated_claim = f"{claim.original_sentence} [✓ TERVERIFIKASI: `{best_evidence.file_path}:L{best_evidence.start_line}`]"
            elif citation_status == "MISSING":
                explanation = (
                    f"Klaim didukung bukti empiris di `{best_evidence.file_path}:L{best_evidence.start_line}`, "
                    f"tetapi belum memiliki penanda sitasi. Disarankan menyertakan sitasi {recommended_cite}."
                )
                correction_suggestion = f"Tambahkan penanda sitasi {recommended_cite} di akhir klaim."
                annotated_claim = (
                    f"{claim.original_sentence} "
                    f"[💡 PERLU SITASI: didukung di `{best_evidence.file_path}:L{best_evidence.start_line}`, tambahkan {recommended_cite}]"
                )
            elif citation_status == "DISALLOWED_THESIS":
                status = "DISALLOWED"
                explanation = cit_explanation
                correction_suggestion = "Hapus rujukan skripsi alumni SIMPUS dan ganti dengan referensi artikel jurnal atau prosiding peer-reviewed."
                annotated_claim = (
                    f"{claim.original_sentence} [🚫 SITASI SKRIPSI DILARANG: skripsi alumni SIMPUS dilarang untuk artikel ilmiah]"
                )
            else:  # MISMATCH
                explanation = f"Klaim didukung konsepnya, namun nomor sitasi yang dicantumkan tidak sesuai dengan sumber rujukan korpus."
                correction_suggestion = f"Gunakan sitasi {recommended_cite} yang merujuk pada `{best_evidence.file_path}`."
                annotated_claim = (
                    f"{claim.original_sentence} "
                    f"[⚠️ SITASI KURANG SESUAI: rujukan korpus menyarankan {recommended_cite}]"
                )


        else:
            status = "UNSUPPORTED"
            citation_status = "NOT_APPLICABLE" if not claim.embedded_citations else "MISMATCH"
            explanation = f"Tingkat dukungan bukti korpus belum cukup meyakinkan (kemiripan {highest_sim*100:.1f}%)."
            correction_suggestion = "Perkuat argumen dengan menambahkan kutipan atau fakta dari korpus lokal."
            annotated_claim = f"{claim.original_sentence} [❓ KURANG BUKTI: rujukan belum definitif]"

        return ClaimVerificationResult(
            claim=claim,
            status=status,
            citation_status=citation_status,
            confidence_score=highest_sim,
            best_evidence=best_evidence,
            alternative_evidences=[e for e in evidences if e != best_evidence],
            explanation=explanation,
            correction_suggestion=correction_suggestion,
            annotated_claim=annotated_claim,
        )

    def _check_numeric_contradiction(
        self,
        claim: FactClaim,
        evidence: EvidenceMatch,
    ) -> Tuple[bool, str]:
        """Detects if a claim asserts numbers that directly contradict numbers in the evidence passage."""
        claim_nums = claim.extracted_numbers
        ev_nums = extract_quantities(evidence.content)

        if not claim_nums or not ev_nums:
            return False, ""

        # If all numbers in claim match directly in evidence, no contradiction
        if all(cn in ev_nums for cn in claim_nums):
            return False, ""

        # Separate calendar years (1950 - 2050) from quantities (percentages, decimals, counts)
        c_years = [n for n in claim_nums if n.isdigit() and 1950 <= int(n) <= 2050]
        c_quantities = [n for n in claim_nums if not (n.isdigit() and 1950 <= int(n) <= 2050)]

        e_years = [n for n in ev_nums if n.isdigit() and 1950 <= int(n) <= 2050]
        e_quantities = [n for n in ev_nums if not (n.isdigit() and 1950 <= int(n) <= 2050)]

        # Filter out student IDs (NIM 9 digits) and equation/section indicators from quantities
        def filter_pure_quantities(nums: List[str]) -> List[str]:
            res = []
            for n in nums:
                # Strip 9-digit NIMs
                if re.match(r"^2\d{8}$", n):
                    continue
                # Strip single digit list enumerations (1, 2, 3...) if standalone
                if n.isdigit() and int(n) < 10 and not any(k in claim.claim_text.lower() for k in ["celah", "service", "endpoint", "kategori", "skala", "pilar", "tahap"]):
                    continue
                res.append(n)
            return res

        c_quantities = filter_pure_quantities(c_quantities)
        e_quantities = filter_pure_quantities(e_quantities)

        # Contextual words overlap between claim and evidence
        claim_words = set(re.findall(r"\b[a-zA-Z]{4,}\b", claim.claim_text.lower()))
        ev_words = set(re.findall(r"\b[a-zA-Z]{4,}\b", evidence.content.lower()))
        overlap = claim_words.intersection(ev_words)

        # System/target subject alignment check:
        # A finding specifically about one application/system (e.g. JAFUNG) cannot contradict another (e.g. SIPADU)
        system_targets = ["sipadu", "jafung", "sijafung", "simwas", "mitra", "susenas", "sakernas", "st2023", "sp2020"]
        c_targets = {t for t in system_targets if t in claim.claim_text.lower()}
        e_targets = {t for t in system_targets if t in evidence.content.lower()}
        if c_targets and e_targets and not (c_targets & e_targets):
            return False, ""

        # 1. Non-year quantities contradiction:
        # Require strong contextual overlap (>= 4 shared domain words) and both sides having substantial quantities
        if c_quantities and e_quantities:
            # Check if any quantity in claim matches any quantity in evidence
            has_match = any(cq in ev_nums or any(cq in eq for eq in e_quantities) for cq in c_quantities)
            if not has_match and len(overlap) >= 4:
                # Ensure they are talking about the exact same measurable attribute
                shared_metrics = {"petugas", "mitra", "persen", "persentase", "celah", "endpoint", "mahasiswa", "responden", "sampel", "skor", "nilai"}
                active_metric = None
                for sm in shared_metrics:
                    if sm in overlap:
                        c_has_metric = bool(re.search(rf"\b\d+\s*{sm}\b|\b{sm}\s*\d+\b", claim.claim_text.lower()))
                        e_has_metric = bool(re.search(rf"\b\d+\s*{sm}\b|\b{sm}\s*\d+\b", evidence.content.lower()))
                        if sm in {"persen", "persentase"}:
                            c_has_metric = "%" in claim.claim_text or "persen" in claim.claim_text.lower()
                            e_has_metric = "%" in evidence.content or "persen" in evidence.content.lower()
                        if c_has_metric and e_has_metric:
                            active_metric = sm
                            break

                if active_metric:
                    return (
                        True,
                        f"klaim menyebut {', '.join(c_quantities)}, sedangkan bukti korpus mencatat {', '.join(e_quantities[:3])}",
                    )

        # 2. Year contradiction:
        # Only flag if both specifically discuss the same statistical event/survey/system census
        event_markers = {"sensus", "survei", "st2023", "sp2020", "sakernas", "susenas", "epss"}
        if c_years and e_years and not any(cy in e_years for cy in c_years):
            if any(em in overlap for em in event_markers) and len(overlap) >= 4:
                return (
                    True,
                    f"klaim menyebut tahun {', '.join(c_years)}, sedangkan bukti korpus mencatat tahun {', '.join(e_years[:3])}",
                )

        return False, ""

    def _check_citation_status(
        self,
        claim: FactClaim,
        evidence: EvidenceMatch,
    ) -> Tuple[str, str, str]:
        """Evaluates whether the claim's citation matches the evidence source."""
        unique_ev_cites = list(dict.fromkeys(evidence.extracted_citations))
        ev_cites = unique_ev_cites
        claim_cites = claim.embedded_citations

        recommended_cite = ", ".join(ev_cites) if ev_cites else "[rujukan terkait]"

        # Check for disallowed SIMPUS or skripsi citations in scientific papers
        ev_source = (getattr(evidence, "file_path", None) or getattr(evidence, "source", None) or "").lower()
        disallowed_indicators = ["simpus", "theses", "skripsi", "mastersthesis", "sarjana terapan", "tugas akhir"]
        if any(ind in ev_source for ind in disallowed_indicators):
            return "DISALLOWED_THESIS", "Rujukan mengarah ke skripsi alumni/SIMPUS yang dilarang untuk artikel ilmiah. Wajib menggunakan jurnal/prosiding resmi.", recommended_cite

        for cc in claim_cites:
            lower_cc = cc.lower()
            if any(ind in lower_cc for ind in disallowed_indicators):
                return "DISALLOWED_THESIS", "Sitasi mengarah ke skripsi alumni/SIMPUS yang dilarang untuk artikel ilmiah.", recommended_cite


        if not claim_cites:
            return "MISSING", "Klaim belum menyertakan penanda sitasi.", recommended_cite

        # Check if any claim citation matches evidence citation
        for cc in claim_cites:
            if cc in ev_cites:
                return "VALID", "Sitasi sesuai dengan bukti korpus.", recommended_cite

        # If evidence has citations and claim has citations, but they differ
        if ev_cites and claim_cites:
            return "MISMATCH", "Penanda sitasi berbeda dari rujukan bukti korpus.", recommended_cite

        return "VALID", "Sitasi diterima.", recommended_cite

    def _jaccard_similarity(self, text_a: str, text_b: str) -> float:
        """Fallback lexical token similarity."""
        tokens_a = set(re.findall(r"\b\w{3,}\b", text_a.lower()))
        tokens_b = set(re.findall(r"\b\w{3,}\b", text_b.lower()))
        if not tokens_a or not tokens_b:
            return 0.0
        return len(tokens_a.intersection(tokens_b)) / len(tokens_a.union(tokens_b))
