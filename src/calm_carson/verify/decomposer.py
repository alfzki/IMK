"""Decomposes paragraphs and draft text into atomic factual claims with extracted quantities and citations."""

from __future__ import annotations

import re
from typing import List, Tuple

from calm_carson.verify.models import FactClaim

# Citation patterns
REGEX_CITATION_IEEE = re.compile(r"\[\s*\d+(?:\s*[,–-]\s*\d+)*\s*\]")
REGEX_CITATION_AUTHOR = re.compile(r"\([A-Z][a-zA-Z\s\.\&]+(?:et\s+al\.?)?,\s*\d{4}\)")

# Number and quantitative patterns
REGEX_PERCENTAGE = re.compile(r"\b\d+(?:[.,]\d+)?\s*%(?:\s*(?:hingga|sampai|[-–])\s*\d+(?:[.,]\d+)?\s*%)?", re.IGNORECASE)
REGEX_THOUSAND = re.compile(r"\b\d{1,3}(?:\.\d{3})+(?:[.,]\d+)?\b")
REGEX_DECIMAL = re.compile(r"\b\d+[,.]\d+\b")
REGEX_INTEGER = re.compile(r"\b\d+\b")


def extract_quantities(text: str) -> List[str]:
    """Extracts all numbers, percentages, and quantities from text in normalized forms."""
    # First strip citations [1], [2], [1]-[3], (Author, 2024) so citation indices aren't treated as quantities
    clean_text = REGEX_CITATION_IEEE.sub(" ", text)
    clean_text = REGEX_CITATION_AUTHOR.sub(" ", clean_text)
    # Also strip equation tags like (1), (2), \tag{1}
    clean_text = re.sub(r"\(\s*\d+\s*\)", " ", clean_text)
    clean_text = re.sub(r"\\tag\{\s*\d+\s*\}", " ", clean_text)

    quantities: List[str] = []

    # 1. Percentages
    for match in REGEX_PERCENTAGE.finditer(clean_text):
        quantities.append(match.group(0).strip())

    # 2. Thousands
    for match in REGEX_THOUSAND.finditer(clean_text):
        q = match.group(0).strip()
        if q not in quantities:
            quantities.append(q)

    # 3. Decimals
    for match in REGEX_DECIMAL.finditer(clean_text):
        q = match.group(0).strip()
        if q not in quantities:
            quantities.append(q)

    # 4. Integers (e.g. 2023, 15, 400)
    for match in REGEX_INTEGER.finditer(clean_text):
        q = match.group(0).strip()
        # Avoid re-adding numbers that are part of already captured thousands/decimals
        if not any(q in existing for existing in quantities):
            quantities.append(q)

    return quantities


def extract_citations(text: str) -> List[str]:
    """Extracts IEEE and author-year citation markers from text."""
    citations: List[str] = []
    for m in REGEX_CITATION_IEEE.finditer(text):
        citations.append(m.group(0).strip())
    for m in REGEX_CITATION_AUTHOR.finditer(text):
        citations.append(m.group(0).strip())
    return citations


def split_text_into_sentences(text: str) -> List[Tuple[str, int, int]]:
    """
    Splits text into sentences while respecting common academic abbreviations.
    Returns list of (sentence_str, start_char, end_char).
    """
    # Protected abbreviations
    protected = {
        "et al.": "et al<DOT>",
        "vol.": "vol<DOT>",
        "no.": "no<DOT>",
        "pp.": "pp<DOT>",
        "dkk.": "dkk<DOT>",
        "e.g.": "e<DOT>g<DOT>",
        "i.e.": "i<DOT>e<DOT>",
        "dst.": "dst<DOT>",
        "s.d.": "s<DOT>d<DOT>",
    }

    masked = text
    for abbr, repl in protected.items():
        masked = re.sub(re.escape(abbr), repl, masked, flags=re.IGNORECASE)

    # Split on sentence boundaries: (. ! ?) followed by whitespace or quote
    pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'\[\(-])")
    spans = []
    current_idx = 0

    splits = pattern.split(masked)
    for part in splits:
        unmasked = part
        for abbr, repl in protected.items():
            unmasked = unmasked.replace(repl, abbr)

        # find actual start and end in original text
        start_char = text.find(unmasked, current_idx)
        if start_char == -1:
            start_char = current_idx
        end_char = start_char + len(unmasked)
        current_idx = end_char

        clean = unmasked.strip()
        if clean:
            spans.append((clean, start_char, end_char))

    return spans


class ClaimDecomposer:
    """Decomposes paragraphs into distinct factual claims with citation and quantity awareness."""

    def decompose(self, draft_text: str) -> List[FactClaim]:
        """Parses draft text into an ordered list of FactClaims."""
        # Pre-filter structural lines (headings, tables, blockquotes, horizontal lines, bibliography)
        filtered_lines = []
        for line in draft_text.splitlines():
            ls = line.strip()
            if (
                ls.startswith("#")
                or ls.startswith("|")
                or ls.startswith(">")
                or ls.startswith("---")
                or ls.startswith("$$")
                or ls.endswith("$$")
                or re.match(r"^\[\s*\d+\s*\]", ls)
            ):
                continue
            filtered_lines.append(line)
        cleaned_body = "\n".join(filtered_lines)

        sentences = split_text_into_sentences(cleaned_body)
        claims: List[FactClaim] = []

        for idx, (sent_text, start_pos, end_pos) in enumerate(sentences, start=1):
            s_stripped = sent_text.strip()
            # Ignore questions or very short fragments
            if (
                s_stripped.endswith("?")
                or len(s_stripped) < 15
            ):
                continue

            citations = extract_citations(sent_text)
            numbers = extract_quantities(sent_text)

            # Clean claim text (strip bracket citations for pure propositional matching)
            clean_claim = REGEX_CITATION_IEEE.sub("", sent_text)
            clean_claim = REGEX_CITATION_AUTHOR.sub("", clean_claim)
            clean_claim = re.sub(r"\s+", " ", clean_claim).strip()

            claim_id = f"claim_{idx}"
            claims.append(
                FactClaim(
                    id=claim_id,
                    claim_text=clean_claim,
                    original_sentence=sent_text,
                    start_char=start_pos,
                    end_char=end_pos,
                    extracted_numbers=numbers,
                    embedded_citations=citations,
                )
            )

        return claims
