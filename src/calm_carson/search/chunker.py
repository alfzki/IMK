"""
calm_carson.search.chunker
Hierarchical Markdown Chunker that preserves document heading structure,
breadcrumb hierarchy, and logical paragraph/table boundaries.
"""

import hashlib
import os
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class MarkdownChunk:
    chunk_id: str
    doc_path: str
    doc_title: str
    breadcrumb: str
    heading_stack: List[str]
    content: str  # Contextualized text (with breadcrumb header)
    raw_content: str  # Original raw markdown snippet
    start_line: int
    end_line: int
    char_count: int = field(init=False)

    def __post_init__(self):
        self.char_count = len(self.content)

    def to_dict(self) -> Dict:
        return asdict(self)


class HierarchicalMarkdownChunker:
    """
    Splits markdown documents into semantically coherent chunks while maintaining
    hierarchical heading breadcrumbs (e.g. # H1 > ## H2 > ### H3).
    """

    def __init__(
        self,
        min_chunk_size: int = 300,
        max_chunk_size: int = 1400,
        chunk_overlap: int = 150,
    ):
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_file(self, file_path: str, base_dir: Optional[str] = None) -> List[MarkdownChunk]:
        """Reads and chunks a markdown file."""
        if not os.path.isfile(file_path):
            return []

        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        except Exception as e:
            print(f"[!] Error reading file '{file_path}': {e}")
            return []

        rel_path = file_path
        if base_dir:
            try:
                rel_path = os.path.relpath(file_path, base_dir)
            except ValueError:
                rel_path = file_path

        return self.chunk_text(text, doc_path=rel_path)

    def chunk_text(self, text: str, doc_path: str = "document.md") -> List[MarkdownChunk]:
        """Parses markdown text and produces hierarchical chunks."""
        lines = text.splitlines()
        if not lines:
            return []

        # 1. Detect Document Title
        doc_title = Path(doc_path).stem.replace("_", " ").replace("-", " ").title()
        for line in lines[:20]:
            clean = line.strip()
            if clean.startswith("# "):
                doc_title = re.sub(r"^#\s+", "", clean).strip()
                doc_title = re.sub(r"[*_`]", "", doc_title)
                break

        # 2. Parse into logical blocks associated with heading stacks
        # Each block is: (heading_stack, block_lines, start_line, end_line)
        heading_stack: List[Tuple[int, str]] = []  # List of (level, title)
        blocks: List[Dict] = []

        current_block_lines: List[str] = []
        block_start_line = 1
        in_code_block = False

        for line_idx, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Handle fenced code blocks
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                current_block_lines.append(line)
                continue

            # Check heading (only when outside code blocks)
            heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped) if not in_code_block else None

            if heading_match:
                # Flush previous block if any
                if current_block_lines:
                    text_block = "\n".join(current_block_lines).strip()
                    if text_block:
                        blocks.append({
                            "headings": [h[1] for h in heading_stack],
                            "lines": current_block_lines,
                            "text": text_block,
                            "start_line": block_start_line,
                            "end_line": line_idx - 1,
                        })
                    current_block_lines = []

                level = len(heading_match.group(1))
                heading_text = re.sub(r"[*_`#]", "", heading_match.group(2)).strip()

                # Pop headings with level >= current level
                while heading_stack and heading_stack[-1][0] >= level:
                    heading_stack.pop()

                heading_stack.append((level, heading_text))
                block_start_line = line_idx
                continue

            # Check paragraph / table / list boundary
            if not in_code_block and stripped == "":
                if current_block_lines:
                    text_block = "\n".join(current_block_lines).strip()
                    if text_block:
                        blocks.append({
                            "headings": [h[1] for h in heading_stack],
                            "lines": current_block_lines,
                            "text": text_block,
                            "start_line": block_start_line,
                            "end_line": line_idx - 1,
                        })
                    current_block_lines = []
                    block_start_line = line_idx + 1
            else:
                if not current_block_lines:
                    block_start_line = line_idx
                current_block_lines.append(line)

        # Flush final block
        if current_block_lines:
            text_block = "\n".join(current_block_lines).strip()
            if text_block:
                blocks.append({
                    "headings": [h[1] for h in heading_stack],
                    "lines": current_block_lines,
                    "text": text_block,
                    "start_line": block_start_line,
                    "end_line": len(lines),
                })

        # 3. Assemble blocks into chunks with heading context
        chunks: List[MarkdownChunk] = []
        path_hash = hashlib.md5(doc_path.encode("utf-8")).hexdigest()[:8]
        chunk_idx = 0

        current_chunk_blocks: List[Dict] = []
        current_chunk_len = 0

        def emit_chunk(block_list: List[Dict]):
            nonlocal chunk_idx
            if not block_list:
                return

            raw_text = "\n\n".join(b["text"] for b in block_list).strip()
            if not raw_text:
                return

            # Combine heading stacks from the blocks (prefer deepest common)
            all_headings = block_list[0]["headings"]
            for b in block_list[1:]:
                if len(b["headings"]) > len(all_headings):
                    all_headings = b["headings"]

            breadcrumb_parts = [Path(doc_path).name] + all_headings
            breadcrumb_str = " > ".join(breadcrumb_parts)

            # Prepend breadcrumb header to contextual content
            context_header = f"[Konteks: {breadcrumb_str}]\n\n"
            content = context_header + raw_text

            start_l = block_list[0]["start_line"]
            end_l = block_list[-1]["end_line"]
            cid = f"{path_hash}_{chunk_idx:04d}"
            chunk_idx += 1

            chunk = MarkdownChunk(
                chunk_id=cid,
                doc_path=doc_path,
                doc_title=doc_title,
                breadcrumb=breadcrumb_str,
                heading_stack=all_headings,
                content=content,
                raw_content=raw_text,
                start_line=start_l,
                end_line=end_l,
            )
            chunks.append(chunk)

        for b in blocks:
            b_len = len(b["text"])

            # If a single block exceeds max_chunk_size (e.g. large table or massive paragraph), split it
            if b_len > self.max_chunk_size:
                if current_chunk_blocks:
                    emit_chunk(current_chunk_blocks)
                    current_chunk_blocks = []
                    current_chunk_len = 0

                # Split long text by lines
                sub_lines = b["text"].splitlines()
                sub_buf: List[str] = []
                sub_len = 0
                sub_start = b["start_line"]

                for sl_idx, sl in enumerate(sub_lines):
                    sub_buf.append(sl)
                    sub_len += len(sl) + 1
                    if sub_len >= self.max_chunk_size:
                        emit_chunk([{
                            "headings": b["headings"],
                            "text": "\n".join(sub_buf),
                            "start_line": sub_start,
                            "end_line": b["start_line"] + sl_idx,
                        }])
                        # Retain overlap lines
                        overlap_lines = sub_buf[-2:] if len(sub_buf) > 2 else []
                        sub_buf = list(overlap_lines)
                        sub_len = sum(len(x) + 1 for x in sub_buf)
                        sub_start = b["start_line"] + sl_idx

                if sub_buf:
                    emit_chunk([{
                        "headings": b["headings"],
                        "text": "\n".join(sub_buf),
                        "start_line": sub_start,
                        "end_line": b["end_line"],
                    }])
                continue

            # Heading changed -> always flush previous chunk so different headings are never merged
            if current_chunk_blocks:
                prev_headings = current_chunk_blocks[-1]["headings"]
                if prev_headings != b["headings"]:
                    emit_chunk(current_chunk_blocks)
                    current_chunk_blocks = []
                    current_chunk_len = 0

            # Accumulate block
            if current_chunk_len + b_len > self.max_chunk_size and current_chunk_len >= self.min_chunk_size:
                emit_chunk(current_chunk_blocks)
                current_chunk_blocks = []
                current_chunk_len = 0

            current_chunk_blocks.append(b)
            current_chunk_len += b_len

        if current_chunk_blocks:
            emit_chunk(current_chunk_blocks)

        return chunks
