"""Factual verification and citation validation module for thesis draft writing."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from calm_carson.verify.annotator import DraftAnnotator
from calm_carson.verify.decomposer import ClaimDecomposer
from calm_carson.verify.exporter import VerificationExporter
from calm_carson.verify.matcher import EvidenceMatcher
from calm_carson.verify.models import (
    ClaimVerificationResult,
    EvidenceMatch,
    FactClaim,
    VerificationReport,
)
from calm_carson.verify.verifier import FactVerifier


def verify_draft_text(
    draft_text: str,
    workspace_root: Optional[Path] = None,
    export_files: bool = True,
) -> VerificationReport:
    """End-to-end pipeline to verify factual claims in a draft text against the local corpus."""
    decomposer = ClaimDecomposer()
    claims = decomposer.decompose(draft_text)

    matcher = EvidenceMatcher(workspace_root=workspace_root)
    verifier = FactVerifier()
    annotator = DraftAnnotator()

    results = []
    for claim in claims:
        evidences = matcher.match_claim(claim, top_k=4)
        res = verifier.verify_claim(claim, evidences)
        results.append(res)

    annotated_text = annotator.annotate(results)

    supported_count = sum(1 for r in results if r.status == "SUPPORTED")
    contradicted_count = sum(1 for r in results if r.status == "CONTRADICTED")
    unsupported_count = sum(1 for r in results if r.status == "UNSUPPORTED")
    missing_cit_count = sum(1 for r in results if r.citation_status == "MISSING")

    if contradicted_count > 0:
        overall_verdict = "FATAL_CONTRADICTIONS"
        verdict_summary = (
            f"Draf mengandung {contradicted_count} klaim yang bertentangan langsung dengan data korpus. "
            "Draf TIDAK BOLEH diajukan sebelum dilakukan koreksi data faktual."
        )
    elif missing_cit_count > 0 or unsupported_count > 0:
        overall_verdict = "NEEDS_MINOR_CITATION"
        verdict_summary = (
            f"Semua fakta selaras, namun terdapat {missing_cit_count} klaim yang memerlukan penambahan nomor sitasi "
            f"dan {unsupported_count} klaim yang perlu penguatan rujukan."
        )
    else:
        overall_verdict = "READY_FOR_SUBMISSION"
        verdict_summary = "Seluruh klaim faktual didukung penuh oleh korpus dokumen lokal dan menyertakan sitasi yang valid."

    report = VerificationReport(
        draft_text=draft_text,
        results=results,
        overall_verdict=overall_verdict,
        verdict_summary=verdict_summary,
        supported_count=supported_count,
        contradicted_count=contradicted_count,
        unsupported_count=unsupported_count,
        missing_citation_count=missing_cit_count,
        annotated_draft=annotated_text,
    )

    if export_files:
        exporter = VerificationExporter(workspace_root=workspace_root)
        exporter.export_json(report)
        exporter.export_markdown(report)

    return report


__all__ = [
    "FactClaim",
    "EvidenceMatch",
    "ClaimVerificationResult",
    "VerificationReport",
    "ClaimDecomposer",
    "EvidenceMatcher",
    "FactVerifier",
    "DraftAnnotator",
    "VerificationExporter",
    "verify_draft_text",
]
