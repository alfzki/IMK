"""Draft annotator for inserting inline verification badges, citation reminders, and contradiction flags."""

from __future__ import annotations

from typing import List

from calm_carson.verify.models import ClaimVerificationResult


class DraftAnnotator:
    """Reconstructs draft text with inline factual verification annotations."""

    def annotate(self, results: List[ClaimVerificationResult]) -> str:
        """Joins annotated claims into a comprehensive annotated paragraph/document."""
        annotated_sentences = []
        for res in results:
            annotated_sentences.append(res.annotated_claim)
        return " ".join(annotated_sentences)

    def generate_clean_revision(self, results: List[ClaimVerificationResult]) -> str:
        """Generates a cleaned draft revision applying recommended citations and corrections."""
        revised_sentences = []
        for res in results:
            sent = res.claim.original_sentence
            if res.status == "SUPPORTED" and res.citation_status == "MISSING":
                # Append recommended citation
                if res.correction_suggestion and "tambahkan" in res.correction_suggestion.lower():
                    cite_match = res.best_evidence.extracted_citations if res.best_evidence else []
                    if cite_match:
                        cite_str = ", ".join(cite_match)
                        sent = f"{sent} {cite_str}"
            elif res.status == "CONTRADICTED":
                # Prefix with warning comment
                sent = f"/* [KOREKSI DIPERLUKAN]: {res.explanation} */ {sent}"
            elif res.status == "UNSUPPORTED":
                sent = f"/* [PERIKSA FAKTA/RUJUKAN]: */ {sent}"

            revised_sentences.append(sent)

        return " ".join(revised_sentences)
