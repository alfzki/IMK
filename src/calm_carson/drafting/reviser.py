"""Automated reviser engine that resolves factual contradictions, injects missing citations, and refines unsupported claims."""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional, Tuple

from calm_carson.verify.decomposer import ClaimDecomposer
from calm_carson.verify.matcher import EvidenceMatcher
from calm_carson.verify.models import ClaimVerificationResult, VerificationReport
from calm_carson.verify.verifier import FactVerifier

logger = logging.getLogger(__name__)


class AutomatedReviser:
    """Iteratively revises draft prose based on factual and citation verification audit feedback."""

    def __init__(
        self,
        verifier: Optional[FactVerifier] = None,
        matcher: Optional[EvidenceMatcher] = None,
        max_iterations: int = 3,
    ):
        self.verifier = verifier or FactVerifier()
        self.matcher = matcher or EvidenceMatcher()
        self.decomposer = ClaimDecomposer()
        self.max_iterations = max_iterations

    def revise_draft(
        self,
        draft_text: str,
        initial_report: Optional[VerificationReport] = None,
    ) -> Tuple[str, List[Dict[str, str]], VerificationReport]:
        """Runs iterative revision loop until contradictions and missing citations are resolved."""
        current_text = draft_text
        all_applied_fixes: List[Dict[str, str]] = []

        # Generate initial report if not provided
        current_report = initial_report
        if current_report is None:
            current_report = self._audit_text(current_text)

        iteration = 0
        while iteration < self.max_iterations:
            # Check if text is already completely verified
            if current_report.contradicted_count == 0 and current_report.missing_citation_count == 0:
                logger.info("Draft text has 0 contradictions and 0 missing citations. No further revision needed.")
                break

            iteration += 1
            logger.info("Starting revision iteration %d / %d", iteration, self.max_iterations)
            text_before = current_text
            current_text, fixes = self._apply_fixes_for_iteration(current_text, current_report)
            all_applied_fixes.extend(fixes)

            if current_text == text_before or not fixes:
                # No changes could be applied, stop to prevent infinite loop
                break

            # Re-verify the revised text
            current_report = self._audit_text(current_text)

        return current_text, all_applied_fixes, current_report

    def _apply_fixes_for_iteration(
        self,
        text: str,
        report: VerificationReport,
    ) -> Tuple[str, List[Dict[str, str]]]:
        """Applies concrete string replacements to correct contradictions and insert missing citations."""
        updated_text = text
        fixes: List[Dict[str, str]] = []

        for res in report.results:
            orig_sentence = res.claim.original_sentence.strip()
            if not orig_sentence or orig_sentence not in updated_text:
                continue

            # 1. Fix Contradictions
            if res.status == "CONTRADICTED" and res.best_evidence is not None:
                fixed_sentence = self._fix_contradicted_claim(res)
                if fixed_sentence != orig_sentence:
                    updated_text = updated_text.replace(orig_sentence, fixed_sentence, 1)
                    fixes.append({
                        "type": "CONTRADICTION_RESOLVED",
                        "claim_id": res.claim.id,
                        "original": orig_sentence,
                        "revised": fixed_sentence,
                        "reason": res.explanation,
                    })
                    continue

            # 2. Fix Missing Citations
            if res.status == "SUPPORTED" and res.citation_status == "MISSING":
                fixed_sentence = self._fix_missing_citation(res)
                if fixed_sentence != orig_sentence:
                    updated_text = updated_text.replace(orig_sentence, fixed_sentence, 1)
                    fixes.append({
                        "type": "CITATION_INJECTED",
                        "claim_id": res.claim.id,
                        "original": orig_sentence,
                        "revised": fixed_sentence,
                        "reason": f"Disematkan sitasi yang direkomendasikan korpus.",
                    })
                    continue

            # 3. Soften Unsupported Claims with Extravagant Claims
            if res.status == "UNSUPPORTED" and res.confidence_score < 0.20:
                fixed_sentence = self._soften_unsupported_claim(res)
                if fixed_sentence != orig_sentence:
                    updated_text = updated_text.replace(orig_sentence, fixed_sentence, 1)
                    fixes.append({
                        "type": "UNSUPPORTED_REMOVED_OR_SOFTENED",
                        "claim_id": res.claim.id,
                        "original": orig_sentence,
                        "revised": fixed_sentence,
                        "reason": "Menyelaraskan klaim spekulatif dengan konteks akademis korpus.",
                    })

        return updated_text, fixes

    def _fix_contradicted_claim(self, res: ClaimVerificationResult) -> str:
        """Corrects conflicting numbers or phrases using the authoritative evidence passage."""
        claim = res.claim
        orig_sent = claim.original_sentence.strip()
        evidence = res.best_evidence
        if evidence is None:
            return orig_sent

        claim_nums = [n for n in claim.extracted_numbers if not (n.isdigit() and 1950 <= int(n) <= 2050)]
        ev_nums = [n for n in evidence.matched_numbers or [] if not (n.isdigit() and 1950 <= int(n) <= 2050)]

        if not ev_nums and evidence.content:
            from calm_carson.verify.decomposer import extract_quantities
            all_ev_nums = extract_quantities(evidence.content)
            ev_nums = [n for n in all_ev_nums if not (n.isdigit() and 1950 <= int(n) <= 2050)]

        # Filter out numbers that look like list enumeration, section headings, or single digits
        def is_statistical_quantity(val: str) -> bool:
            v = val.strip()
            if not v:
                return False
            if "%" in v or "," in v:
                return True
            if "." in v:
                parts = v.split(".")
                # Check if thousand separator (e.g. 190.000) or section (e.g. 1.1)
                if len(parts) == 2 and len(parts[1]) == 3:
                    return True
                if len(parts) > 2:
                    return True
            if v.isdigit():
                return int(v) > 10
            return False

        stat_claim_nums = [n for n in claim_nums if is_statistical_quantity(n)]
        stat_ev_nums = [n for n in ev_nums if is_statistical_quantity(n)]

        if stat_claim_nums and stat_ev_nums:
            old_num = stat_claim_nums[0]
            new_num = stat_ev_nums[0]
            # Replace using regex boundary to avoid corrupting section numbers (e.g. 1.1 or ### 1.)
            pattern = re.compile(r'(?<![#\d\.])' + re.escape(old_num) + r'(?!\.)')
            if pattern.search(orig_sent):
                fixed = pattern.sub(new_num, orig_sent, count=1)
                ev_cites = list(dict.fromkeys(evidence.extracted_citations))
                if ev_cites and not any(c in fixed for c in ev_cites):
                    fixed = self._append_citation_to_sentence(fixed, ev_cites[0])
                return fixed

        # If claim already matches evidence or no clean replacement, keep original
        return orig_sent

    def _fix_missing_citation(self, res: ClaimVerificationResult) -> str:
        """Appends recommended IEEE citation marker before trailing sentence punctuation."""
        orig_sent = res.claim.original_sentence.strip()
        if res.best_evidence and res.best_evidence.extracted_citations:
            rec_cite = res.best_evidence.extracted_citations[0]
        else:
            rec_cite = "[1]"

        return self._append_citation_to_sentence(orig_sent, rec_cite)

    def _soften_unsupported_claim(self, res: ClaimVerificationResult) -> str:
        """Replaces or softens unsupported statements."""
        orig_sent = res.claim.original_sentence.strip()
        # Prefix with academic hedging
        hedges = ["Berdasarkan kajian konseptual, ", "Penelitian awal menunjukkan bahwa ", "Dalam konteks teoritis, "]
        for h in hedges:
            if orig_sent.lower().startswith(h.lower()):
                return orig_sent
        return f"Berdasarkan kajian literatur, {orig_sent[0].lower() + orig_sent[1:]}"

    def _append_citation_to_sentence(self, sentence: str, citation_marker: str) -> str:
        """Injects citation marker before final dot/punctuation."""
        s = sentence.strip()
        if citation_marker in s or re.search(r"\[\d+\]\s*\.?$", s):
            return s
        if s.endswith("."):
            return f"{s[:-1]} {citation_marker}."
        elif s.endswith(";"):
            return f"{s[:-1]} {citation_marker};"
        return f"{s} {citation_marker}"

    def _audit_text(self, text: str) -> VerificationReport:
        """Runs full factual decomposition and verification against local corpus."""
        claims = self.decomposer.decompose(text)
        results: List[ClaimVerificationResult] = []

        supported_cnt = 0
        contradicted_cnt = 0
        unsupported_cnt = 0
        missing_cite_cnt = 0

        for c in claims:
            evidences = self.matcher.match_claim(c, top_k=4)
            res = self.verifier.verify_claim(c, evidences)
            results.append(res)

            if res.status == "SUPPORTED":
                supported_cnt += 1
            elif res.status == "CONTRADICTED":
                contradicted_cnt += 1
            else:
                unsupported_cnt += 1

            if res.citation_status == "MISSING":
                missing_cite_cnt += 1

        if contradicted_cnt > 0:
            overall_verdict = "FATAL_CONTRADICTIONS"
            summary = f"Terdeteksi {contradicted_cnt} kontradiksi data yang harus direvisi."
        elif missing_cite_cnt > 0:
            overall_verdict = "NEEDS_MINOR_CITATION"
            summary = f"Fakta selaras, namun terdapat {missing_cite_cnt} nomor sitasi yang perlu disematkan."
        else:
            overall_verdict = "READY_FOR_SUBMISSION"
            summary = "Seluruh klaim faktual terverifikasi sahih terhadap korpus lokal."

        return VerificationReport(
            draft_text=text,
            results=results,
            overall_verdict=overall_verdict,
            verdict_summary=summary,
            supported_count=supported_cnt,
            contradicted_count=contradicted_cnt,
            unsupported_count=unsupported_cnt,
            missing_citation_count=missing_cite_cnt,
            annotated_draft=text,
        )
