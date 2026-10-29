"""Word-level PDF text extraction with bounding boxes.

Uses pypdfium2 char boxes grouped into words by whitespace and inter-character gaps.
Coordinates are PDF points, origin bottom-left (y increases upward).
"""
from __future__ import annotations

from dataclasses import dataclass

import pypdfium2 as pdfium


@dataclass
class Word:
    text: str
    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def xc(self) -> float:
        return (self.x0 + self.x1) / 2.0

    @property
    def yc(self) -> float:
        return (self.y0 + self.y1) / 2.0


def extract_words(pdf_bytes: bytes, physical_page: int) -> list[Word]:
    """Return words with boxes for a physical page (1-based)."""
    doc = pdfium.PdfDocument(pdf_bytes)
    try:
        page = doc[physical_page - 1]
        tp = page.get_textpage()
        try:
            n = tp.count_chars()
        except AttributeError:  # older pypdfium2 without count_chars binding
            n = len(tp.get_text_range())
        words: list[Word] = []
        cur: list[dict] = []

        def flush() -> None:
            if not cur:
                return
            text = "".join(c["ch"] for c in cur)
            if text.strip():
                words.append(
                    Word(
                        text,
                        min(c["l"] for c in cur),
                        min(c["b"] for c in cur),
                        max(c["r"] for c in cur),
                        max(c["t"] for c in cur),
                    )
                )
            cur.clear()

        prev: dict | None = None
        for i in range(n):
            ch = tp.get_text_range(i, 1)
            box = tp.get_charbox(i, loose=False)
            if box is None:
                flush()
                prev = None
                continue
            l, b, r, t = box
            char = {"ch": ch, "l": l, "b": b, "r": r, "t": t}
            if ch.isspace() or ch in "\r\n\x0b\x0c\xa0":
                flush()
                prev = None
                continue
            gap = (l - prev["r"]) if prev else 0.0
            big_gap = prev is not None and gap > 2.0
            if prev is None or big_gap:
                flush()
            cur.append(char)
            prev = char
        flush()
        return words
    finally:
        doc.close()


def cluster_lines(words: list[Word], y_tol: float) -> list[list[Word]]:
    """Group words into visual lines (top-down)."""
    if not words:
        return []
    lines: list[list[Word]] = []
    for w in sorted(words, key=lambda w: -w.yc):
        for line in lines:
            ref_yc = sum(x.yc for x in line) / len(line)
            if abs(w.yc - ref_yc) <= y_tol:
                line.append(w)
                break
        else:
            lines.append([w])
    for line in lines:
        line.sort(key=lambda w: w.x0)
    lines.sort(key=lambda line: -sum(w.yc for w in line) / len(line))
    return lines
