"""IEEE standard bibliography formatter and citation renumbering engine."""

import re
from typing import Dict, List, Optional, Tuple

from calm_carson.publisher.models import BibliographyItem


class IEEEBibliographyRenderer:
    """Renders bibliographic records into official IEEE citation style strings."""

    def format_ieee_reference(self, item: BibliographyItem, number: Optional[int] = None) -> str:
        """Formats a single BibliographyItem into an IEEE reference string."""
        prefix = f"[{number}] " if number is not None else ""

        # Format authors
        author_str = self._format_authors(item.authors)

        # Dispatch based on entry type
        etype = (item.entry_type or "misc").lower()
        if etype == "article":
            ref_body = self._format_journal(item, author_str)
        elif etype in ("inproceedings", "conference"):
            ref_body = self._format_conference(item, author_str)
        elif etype == "book":
            ref_body = self._format_book(item, author_str)
        elif etype in ("incollection", "inbook"):
            ref_body = self._format_incollection(item, author_str)
        elif etype in ("mastersthesis", "phdthesis", "skripsi"):
            ref_body = self._format_thesis(item, author_str)
        else:
            ref_body = self._format_misc(item, author_str)

        return f"{prefix}{ref_body}"

    def renumber_manuscript_citations(
        self, text: str, bib_entries: Dict[str, BibliographyItem]
    ) -> Tuple[str, List[Tuple[int, BibliographyItem]]]:
        """Scans manuscript, builds sequential 1..N citation mapping, renumbers text and orders bibliography."""
        # 1. Split body and bibliography
        bib_split = re.split(r"(?:##\s*(?:DAFTAR\s*PUSTAKA|REFERENSI|REFERENCES)|\bDAFTAR\s*PUSTAKA\b)", text, flags=re.IGNORECASE)
        body = bib_split[0]

        # 2. Find citation order of first appearance
        # Match numeric citations [1], [2] or keys [@key]
        seen_keys: List[str] = []
        pattern = r"(?<!\!)(?<!\[)\[(\d+(?:\s*[,-]\s*\d+)*)\](?!\()|\[@([a-zA-Z0-9_\-:\.]+)\]"

        for m in re.finditer(pattern, body):
            num_grp = m.group(1)
            key_grp = m.group(2)

            if num_grp:
                # Compound numeric
                parts = [p.strip() for p in num_grp.split(",") if p.strip()]
                for p in parts:
                    if "-" in p:
                        dash = p.split("-")
                        if len(dash) == 2 and dash[0].strip().isdigit() and dash[1].strip().isdigit():
                            s = int(dash[0].strip())
                            e = int(dash[1].strip())
                            if s <= e and (e - s) < 50:
                                for n in range(s, e + 1):
                                    k = str(n)
                                    if k not in seen_keys:
                                        seen_keys.append(k)
                                continue
                    if p.isdigit() and p not in seen_keys:
                        seen_keys.append(p)
            elif key_grp and key_grp not in seen_keys:
                seen_keys.append(key_grp)

        # 3. Create mapping to 1..N
        key_to_new_num: Dict[str, int] = {}
        ordered_bib: List[Tuple[int, BibliographyItem]] = []

        new_counter = 1
        for old_k in seen_keys:
            key_to_new_num[old_k] = new_counter

            # Find matching bib entry
            matched_item = bib_entries.get(old_k)
            if not matched_item and old_k.isdigit():
                matched_item = next((b for b in bib_entries.values() if b.number == int(old_k)), None)

            if not matched_item:
                # Fallback dummy entry
                matched_item = BibliographyItem(
                    key=old_k,
                    number=new_counter,
                    title=f"Referensi {old_k}",
                    raw_text=f"[{old_k}] Referensi {old_k}",
                )
            else:
                # clone and assign new number
                matched_item.number = new_counter

            ordered_bib.append((new_counter, matched_item))
            new_counter += 1

        # Also append any unused/orphan references at the end
        for b_key, b_item in bib_entries.items():
            if b_key not in seen_keys and (b_item.number is None or str(b_item.number) not in seen_keys):
                b_item.number = new_counter
                ordered_bib.append((new_counter, b_item))
                new_counter += 1

        # 4. Replace citations in body text
        def replace_cite(match):
            raw = match.group(0)
            num_grp = match.group(1)
            key_grp = match.group(2)

            if num_grp:
                parts = [p.strip() for p in num_grp.split(",") if p.strip()]
                new_nums = []
                for p in parts:
                    if "-" in p:
                        dash = p.split("-")
                        if len(dash) == 2 and dash[0].strip().isdigit() and dash[1].strip().isdigit():
                            s = int(dash[0].strip())
                            e = int(dash[1].strip())
                            for n in range(s, e + 1):
                                mapped = key_to_new_num.get(str(n), n)
                                new_nums.append(mapped)
                            continue
                    if p.isdigit():
                        mapped = key_to_new_num.get(p, int(p))
                        new_nums.append(mapped)

                if new_nums:
                    # Sort and compress if consecutive
                    new_nums = sorted(list(set(new_nums)))
                    return self._format_citation_brackets(new_nums)
                return raw

            elif key_grp:
                mapped = key_to_new_num.get(key_grp)
                if mapped is not None:
                    return f"[{mapped}]"
                return raw

            return raw

        renumbered_body = re.sub(pattern, replace_cite, body)

        # 5. Rebuild full markdown text with rendered bibliography
        rendered_bib_lines = ["\n## Daftar Pustaka\n"]
        for num, item in ordered_bib:
            rendered_bib_lines.append(self.format_ieee_reference(item, number=num))

        full_text = renumbered_body.rstrip() + "\n\n" + "\n\n".join(rendered_bib_lines) + "\n"
        return full_text, ordered_bib

    def _format_citation_brackets(self, numbers: List[int]) -> str:
        """Formats list of numbers into IEEE bracket format like [1], [2], [3] or [1]-[3]."""
        if not numbers:
            return ""
        if len(numbers) == 1:
            return f"[{numbers[0]}]"

        # Check if consecutive
        is_consecutive = (len(numbers) >= 3) and (numbers[-1] - numbers[0] == len(numbers) - 1)
        if is_consecutive:
            return f"[{numbers[0]}]-[{numbers[-1]}]"

        # IEEE style separate brackets [1], [2]
        return ", ".join(f"[{n}]" for n in numbers)

    def _format_authors(self, authors: List[str]) -> str:
        """Normalizes authors to IEEE format: 'A. B. Author, C. D. Author, and E. F. Author'."""
        if not authors:
            return ""

        formatted = []
        for author in authors:
            author = author.strip()
            # If comma separated (Last, First)
            if "," in author:
                parts = [p.strip() for p in author.split(",", 1)]
                last = parts[0]
                first = parts[1] if len(parts) > 1 else ""
                initials = self._extract_initials(first)
                formatted.append(f"{initials} {last}".strip())
            else:
                parts = author.split()
                if len(parts) == 1:
                    formatted.append(parts[0])
                else:
                    last = parts[-1]
                    firsts = " ".join(parts[:-1])
                    initials = self._extract_initials(firsts)
                    formatted.append(f"{initials} {last}".strip())

        if len(formatted) == 1:
            return formatted[0]
        elif len(formatted) == 2:
            return f"{formatted[0]} and {formatted[1]}"
        elif len(formatted) > 6:
            # IEEE allows et al. after 6 authors or first author + et al.
            return f"{formatted[0]} et al."
        else:
            return ", ".join(formatted[:-1]) + f", and {formatted[-1]}"

    def _extract_initials(self, name: str) -> str:
        """Extracts initials from first/middle names: 'Simson L.' -> 'S. L.'"""
        words = name.split()
        initials = []
        for w in words:
            if not w:
                continue
            if len(w) == 2 and w[1] == ".":
                initials.append(w.upper())
            else:
                initials.append(f"{w[0].upper()}.")
        return " ".join(initials)

    def _format_journal(self, item: BibliographyItem, author_str: str) -> str:
        """IEEE Journal article: Author, "Title," Journal, vol. X, no. Y, pp. xx–yy, Year, doi: ..."""
        parts = []
        if author_str:
            parts.append(f"{author_str},")

        if item.title:
            t = item.title.strip().rstrip(".")
            parts.append(f'"{t},"')

        venue_part = []
        if item.venue:
            venue_part.append(f"*{item.venue}*")
        if item.volume:
            venue_part.append(f"vol. {item.volume}")
        if item.number_issue:
            venue_part.append(f"no. {item.number_issue}")
        if item.pages:
            venue_part.append(f"pp. {item.pages}")
        if item.year:
            venue_part.append(str(item.year))

        if venue_part:
            parts.append(", ".join(venue_part) + ".")

        if item.doi:
            parts.append(f"doi: {item.doi}.")

        return " ".join(parts)

    def _format_conference(self, item: BibliographyItem, author_str: str) -> str:
        """IEEE Conference: Author, "Title," in Proc. Conf, Location, Year, pp. xx–yy, doi: ..."""
        parts = []
        if author_str:
            parts.append(f"{author_str},")

        if item.title:
            t = item.title.strip().rstrip(".")
            parts.append(f'"{t},"')

        conf_part = []
        if item.venue:
            conf_part.append(f"in *{item.venue}*")
        if item.publisher:
            conf_part.append(item.publisher)
        if item.year:
            conf_part.append(str(item.year))
        if item.pages:
            conf_part.append(f"pp. {item.pages}")

        if conf_part:
            parts.append(", ".join(conf_part) + ".")

        if item.doi:
            parts.append(f"doi: {item.doi}.")

        return " ".join(parts)

    def _format_book(self, item: BibliographyItem, author_str: str) -> str:
        """IEEE Book: Author, Title. Location: Publisher, Year."""
        parts = []
        if author_str:
            parts.append(f"{author_str},")

        if item.title:
            parts.append(f"*{item.title.strip().rstrip('.')}*.")

        pub_parts = []
        if item.publisher:
            pub_parts.append(item.publisher)
        if item.year:
            pub_parts.append(str(item.year))

        if pub_parts:
            parts.append(", ".join(pub_parts) + ".")

        return " ".join(parts)

    def _format_incollection(self, item: BibliographyItem, author_str: str) -> str:
        """IEEE Book Chapter: Author, "Chapter Title," in Book, Publisher, Year, pp. xx-yy."""
        parts = []
        if author_str:
            parts.append(f"{author_str},")

        if item.title:
            parts.append(f'"{item.title.strip().rstrip(".")},"')

        book_parts = []
        if item.venue:
            book_parts.append(f"in *{item.venue}*")
        if item.publisher:
            book_parts.append(item.publisher)
        if item.year:
            book_parts.append(str(item.year))
        if item.pages:
            book_parts.append(f"pp. {item.pages}")

        if book_parts:
            parts.append(", ".join(book_parts) + ".")

        return " ".join(parts)

    def _format_thesis(self, item: BibliographyItem, author_str: str) -> str:
        """IEEE Thesis: Author, "Title," Skripsi/Thesis, School, Year."""
        parts = []
        if author_str:
            parts.append(f"{author_str},")

        if item.title:
            parts.append(f'"{item.title.strip().rstrip(".")},"')

        thesis_parts = []
        degree = "Skripsi Sarjana Terapan" if (
            "skripsi" in (item.entry_type or "").lower()
            or "mastersthesis" in (item.entry_type or "").lower()
            or "stis" in (item.school or "").lower()
        ) else "Thesis"
        thesis_parts.append(degree)

        if item.school:
            thesis_parts.append(item.school)
        else:
            thesis_parts.append("Politeknik Statistika STIS")

        if item.year:
            thesis_parts.append(str(item.year))

        if thesis_parts:
            parts.append(", ".join(thesis_parts) + ".")

        if item.url:
            parts.append(f"[Online]. Available: {item.url}")

        return " ".join(parts)

    def _format_misc(self, item: BibliographyItem, author_str: str) -> str:
        """IEEE Misc / Electronic resource / Reports."""
        if item.raw_text and item.raw_text.strip().startswith("["):
            # If already an inline raw formatted line, strip leading [N]
            cleaned = re.sub(r"^\[\d+\]\s*", "", item.raw_text.strip())
            return cleaned

        parts = []
        if author_str:
            parts.append(f"{author_str},")

        if item.title:
            parts.append(f'"{item.title.strip().rstrip(".")},"')

        misc_parts = []
        if item.venue:
            misc_parts.append(f"*{item.venue}*")
        if item.publisher:
            misc_parts.append(item.publisher)
        if item.year:
            misc_parts.append(str(item.year))

        if misc_parts:
            parts.append(", ".join(misc_parts) + ".")

        if item.doi:
            parts.append(f"doi: {item.doi}.")
        elif item.url:
            parts.append(f"[Online]. Available: {item.url}")

        return " ".join(parts)
