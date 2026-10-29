"""PDF coordinates are displayed-page points, origin at the top left."""
from __future__ import annotations

import hashlib
import io
import logging
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

import pdfplumber
from PySide6.QtCore import QRectF
from .report_map import load_cached_map, load_questions_ledger

logging.getLogger("pdfminer").setLevel(logging.ERROR)


def extract_structured_text(crop) -> str:
    """Format tabular PDF crops as Markdown tables with superscript footnotes; preserve prose layout elsewhere."""
    chars = crop.chars
    if not chars:
        return ""
    vertical_edges = [e for e in crop.edges if e.get('orientation') == 'v' and e['bottom'] - e['top'] >= 10]
    sorted_chars = sorted(chars, key=lambda c: (round(c["top"], 1), c["x0"]))
    lines = []
    for ch in sorted_chars:
        if not ch["text"].strip() and ch["text"] != " ":
            continue
        mid = (ch["top"] + ch["bottom"]) / 2
        placed = False
        for line in lines:
            if abs(mid - line["mid"]) <= max(2.5, line["max_size"] * 0.45):
                line["chars"].append(ch)
                line["mid"] = sum((c["top"] + c["bottom"]) / 2 for c in line["chars"]) / len(line["chars"])
                line["max_size"] = max(line["max_size"], ch["size"])
                placed = True
                break
        if not placed:
            lines.append({"mid": mid, "max_size": ch["size"], "chars": [ch]})
    lines.sort(key=lambda l: l["mid"])

    parsed_lines = []
    for line in lines:
        lchars = sorted(line["chars"], key=lambda c: c["x0"])
        non_space = [c for c in lchars if c["text"].strip()]
        if not non_space:
            continue
        main_size = max(c["size"] for c in non_space)
        segs, cur = [], []
        for c in lchars:
            if not cur:
                if c["text"].strip():
                    cur.append(c)
                continue
            crosses_cell = any(cur[0]['x0'] < e['x0'] <= c['x0'] and e['top'] <= line['mid'] <= e['bottom']
                               for e in vertical_edges)
            if crosses_cell or c["x0"] - cur[-1]["x1"] > max(3.0, main_size * 0.5):
                segs.append((cur, main_size))
                cur = [c] if c["text"].strip() else []
            else:
                cur.append(c)
        if cur:
            segs.append((cur, main_size))

        rendered_segs = []
        for seg_chars, msize in segs:
            while seg_chars and not seg_chars[0]["text"].strip():
                seg_chars.pop(0)
            while seg_chars and not seg_chars[-1]["text"].strip():
                seg_chars.pop()
            if not seg_chars:
                continue

            chunks = []
            curr_is_small = None
            curr_chars = []
            for c in seg_chars:
                is_small = (c["size"] < msize * 0.75)
                if curr_is_small is None:
                    curr_is_small = is_small
                    curr_chars = [c]
                elif is_small == curr_is_small:
                    curr_chars.append(c)
                else:
                    chunks.append((curr_is_small, curr_chars))
                    curr_is_small = is_small
                    curr_chars = [c]
            if curr_chars:
                chunks.append((curr_is_small, curr_chars))

            out = []
            prev_char = None
            for is_small, chars in chunks:
                chunk_out = []
                for i, c in enumerate(chars):
                    txt = c["text"]
                    ref_prev = chars[i - 1] if i > 0 else prev_char
                    if ref_prev and (c["x0"] - ref_prev["x1"] > max(1.0, c["size"] * 0.18)) and ref_prev["text"] != " " and txt != " ":
                        chunk_out.append(" ")
                    chunk_out.append(txt)
                prev_char = chars[-1]

                chunk_str = "".join(chunk_out)
                stripped = chunk_str.strip()
                is_footnote = False
                if is_small and stripped:
                    if stripped.isdigit() and len(stripped) <= 3:
                        is_footnote = True
                    elif all(ch in "*†‡§#" for ch in stripped) and len(stripped) <= 3:
                        is_footnote = True
                    elif len(stripped) == 1 and stripped.isalpha():
                        is_footnote = True

                if is_footnote:
                    leading_space = " " if chunk_str.startswith(" ") else ""
                    trailing_space = " " if chunk_str.endswith(" ") else ""
                    out.append(f"{leading_space}[^{stripped}]{trailing_space}")
                else:
                    out.append(chunk_str)

            text_val = "".join(out).strip()
            if text_val:
                rendered_segs.append({
                    "x0": seg_chars[0]["x0"],
                    "x1": seg_chars[-1]["x1"],
                    "text": text_val,
                    "size": msize,
                })
        if rendered_segs:
            parsed_lines.append({
                "top": min(c["top"] for c in non_space),
                "bottom": max(c["bottom"] for c in non_space),
                "segs": rendered_segs,
            })

    def is_table_row(pl):
        segs = pl["segs"]
        root = getattr(crop, 'root_page', crop)
        if crop.bbox == root.bbox and (pl['top'] < root.bbox[1] + 35 or pl['bottom'] > root.bbox[3] - 35):
            return False  # Running headers/footers remain prose,not column anchors.
        return len(segs) >= 2 and all((s["x1"] - s["x0"]) < 95 and len(s["text"]) <= 25 for s in segs[1:])

    table_rows = [pl for pl in parsed_lines if is_table_row(pl)]
    if len(table_rows) < 2 or len(table_rows) < len(parsed_lines) * 0.35:
        return crop.extract_text(layout=True) or ""

    t_start = parsed_lines.index(table_rows[0])
    t_end = parsed_lines.index(table_rows[-1])
    while t_start > 0:
        prev_pl = parsed_lines[t_start - 1]
        if (len(prev_pl["segs"]) == 1
                and (prev_pl["segs"][0]["x1"] - prev_pl["segs"][0]["x0"]) < 95
                and prev_pl["segs"][0]["x0"] > crop.bbox[0] + 50):
            t_start -= 1
        else:
            break

    numeric = lambda text: bool(re.fullmatch(r'[\d\s.,()%+−–—-]+', text.strip()))
    numeric_rows = [pl for pl in table_rows if sum(numeric(s['text']) for s in pl['segs']) >= 2]
    anchors = [seg for pl in numeric_rows for seg in pl['segs'] if numeric(seg['text'])]
    if anchors:
        first_numeric = min(seg['x0'] for seg in anchors)
        anchors += [seg for pl in table_rows for seg in pl['segs'] if seg['x1'] < first_numeric]
    else:
        anchors = [seg for pl in table_rows for seg in pl['segs']]
    cols = []
    for s in sorted(anchors, key=lambda s: (s["x1"] - s["x0"], s["x0"])):
        x0, x1 = s["x0"], s["x1"]
        best = None
        for col in cols:
            if min(x1, col["x1"]) - max(x0, col["x0"]) > -4:
                new_x0, new_x1 = min(x0, col["x0"]), max(x1, col["x1"])
                conflict = any(
                    sum(1 for seg in pl["segs"] if min(seg["x1"], new_x1) - max(seg["x0"], new_x0) > 0) > 1
                    for pl in table_rows
                )
                if not conflict:
                    best = col
                    break
        if best is not None:
            best["x0"], best["x1"] = min(best["x0"], x0), max(best["x1"], x1)
        else:
            cols.append({"x0": x0, "x1": x1})
    cols.sort(key=lambda c: c["x0"])
    # A wide heading/prose span can overlap several real columns. It must not
    # become a competing column that swallows their numeric cells.
    cols = [col for col in cols if sum(
        other is not col and col['x0'] <= other['x0'] and other['x1'] <= col['x1']
        for other in cols
    ) < 2]
    hits = [sum(any(numeric(seg['text']) and min(seg['x1'], col['x1']) > max(seg['x0'], col['x0'])
                    for seg in pl['segs']) for pl in table_rows) for col in cols]
    data_starts = [col['x0'] for col, count in zip(cols, hits) if count >= 2]
    if data_starts:
        first_data = min(data_starts)
        cols = [col for col, count in zip(cols, hits) if col['x0'] < first_data or count >= 2]
    if len(cols) < 2:
        return crop.extract_text(layout=True) or ""

    h_ys = sorted({round(l["top"], 1) for l in (crop.lines + crop.rects) if (l["x1"] - l["x0"]) > (crop.width * 0.4)})
    table_lines = parsed_lines[t_start:t_end + 1]

    mapped_rows = []
    for pl in table_lines:
        prose_span = (not any(numeric(s['text']) for s in pl['segs'])
                      and any(s['x1'] - s['x0'] > 95 for s in pl['segs']))
        spanned_columns = sum(min(pl['segs'][-1]['x1'], col['x1']) > max(pl['segs'][0]['x0'], col['x0']) for col in cols)
        if (len(pl['segs']) == 1 or prose_span) and spanned_columns >= 2:
            mapped_rows.append({"type": "full", "top": pl["top"], "bottom": pl["bottom"], "text": ' '.join(s['text'] for s in pl['segs'])})
            continue
        cells = [""] * len(cols)
        for seg in pl["segs"]:
            best_idx = min(
                range(len(cols)),
                key=lambda i: (
                    -max(0, min(seg['x1'], cols[i]['x1']) - max(seg['x0'], cols[i]['x0'])),
                    min(abs(seg['x0'] - cols[i]['x1']), abs(seg['x1'] - cols[i]['x0'])),
                    cols[i]['x1'] - cols[i]['x0'],
                ),
            )
            cells[best_idx] = (cells[best_idx] + " " + seg["text"]).strip() if cells[best_idx] else seg["text"]
        mapped_rows.append({"type": "row", "top": pl["top"], "bottom": pl["bottom"], "cells": cells})

    header_count = 1
    for k in range(1, min(4, len(mapped_rows))):
        if mapped_rows[k - 1]["type"] != "row" or mapped_rows[k]["type"] != "row":
            break
        if any(mapped_rows[k - 1]["bottom"] - 1 <= y <= mapped_rows[k]["top"] + 2 for y in h_ys):
            header_count = k
            break
        if not any(re.search(r"\d,\d|\d+\.\d", c) for c in mapped_rows[k]["cells"][1:]):
            header_count = k + 1
        else:
            break

    header_cells = [""] * len(cols)
    for r in mapped_rows[:header_count]:
        if r["type"] == "row":
            for i, val in enumerate(r["cells"]):
                if val:
                    header_cells[i] = (header_cells[i] + " " + val).strip() if header_cells[i] else val

    body_rows = []
    idx = header_count
    while idx < len(mapped_rows):
        r = mapped_rows[idx]
        if (r["type"] == "row"
                and r["cells"][0]
                and not any(r["cells"][1:])
                and idx + 1 < len(mapped_rows)
                and mapped_rows[idx + 1]["type"] == "row"
                and mapped_rows[idx + 1]["cells"][0][:1].islower()
                and any(mapped_rows[idx + 1]["cells"][1:])):
            nxt = dict(mapped_rows[idx + 1])
            nxt["cells"] = list(nxt["cells"])
            nxt["cells"][0] = r["cells"][0] + " " + nxt["cells"][0]
            body_rows.append(nxt)
            idx += 2
            continue
        body_rows.append(r)
        idx += 1

    out_lines = [" ".join(s["text"] for s in pl["segs"]) for pl in parsed_lines[:t_start]]
    # A paragraph may finish beside the first date heading. Keep that sentence
    # in the prose stream rather than inventing a table-column name for it.
    if header_cells[0].endswith('.') and len(header_cells[0].split()) >= 4:
        out_lines.append(header_cells[0])
        header_cells[0] = ''
    if out_lines:
        out_lines.append("")
    table_header = ["| " + " | ".join(header_cells) + " |",
                    "| " + " | ".join("---" for _ in cols) + " |"]
    out_lines.extend(table_header)
    table_open = True
    for r in body_rows:
        if r["type"] == "full":
            out_lines.extend(["", r['text'], ""])
            table_open = False
        else:
            if not table_open:
                out_lines.extend(["| " + " | ".join("" for _ in cols) + " |", table_header[1]])
                table_open = True
            out_lines.append("| " + " | ".join(r["cells"]) + " |")
    if t_end + 1 < len(parsed_lines):
        out_lines.append("")
        for pl in parsed_lines[t_end + 1:]:
            out_lines.append(" ".join(s["text"] for s in pl["segs"]))
    return "\n".join(out_lines)


@dataclass
class Capture:
    page: int  # Original physical PDF page, 1-based.
    mode: str
    bbox: tuple[float, float, float, float]
    text: str
    image: object = None
    page_size: tuple[float, float] = (0.0, 0.0)
    polygons: list[list[list[float]]] = field(default_factory=list)
    text_indices: tuple[int, int] | None = None
    printed_label: str | None = None
    warnings: list[str] = field(default_factory=list)
    content_type: str = "unspecified"
    subheading: str | None = None


def rect_tuple(rect: QRectF) -> tuple[float, float, float, float]:
    return (rect.left(), rect.top(), rect.right(), rect.bottom())


class PdfSource:
    def __init__(self, path: str | Path):
        self.path = Path(path).resolve()
        self.data = self.path.read_bytes()
        self.sha256 = hashlib.sha256(self.data).hexdigest()
        self.plumber = None
        try:
            self.plumber = pdfplumber.open(io.BytesIO(self.data))
        except Exception as exc:
            raise ValueError(f"Cannot open PDF: {exc}") from exc
        if not self.plumber.pages:
            self.plumber.close()
            raise ValueError("Cannot open PDF: document has no pages.")
        self.report_map = load_cached_map(self.sha256, self.page_count)
        self.questions_ledger = load_questions_ledger(self.sha256)

    @property
    def page_count(self) -> int:
        return len(self.plumber.pages) if self.plumber else 0

    def size(self, page: int) -> tuple[float, float]:
        if not 1 <= page <= self.page_count:
            raise ValueError("Physical page is outside the document.")
        native = self.plumber.pages[page - 1]
        return float(native.width), float(native.height)

    def verify_unchanged(self) -> None:
        with self.path.open("rb") as stream:
            current = hashlib.file_digest(stream, "sha256").hexdigest()
        if current != self.sha256:
            raise ValueError("The source PDF changed since it was opened. Reopen it before saving.")

    def capture_area(self, page: int, rectangle: QRectF) -> Capture:
        width, height = self.size(page)
        rect = rectangle.normalized().intersected(QRectF(0, 0, width, height))
        if rect.width() < 2 or rect.height() < 2:
            raise ValueError("Draw a larger selection inside the page.")
        warnings = []
        text = ""
        try:
            native = self.plumber.pages[page - 1]
            if abs(native.width - width) > 1 or abs(native.height - height) > 1:
                raise ValueError("PDF text coordinates do not match the displayed page.")
            x, y = native.bbox[:2]
            box = (max(native.bbox[0], x + rect.left()), max(native.bbox[1], y + rect.top()),
                   min(native.bbox[2], x + rect.right()), min(native.bbox[3], y + rect.bottom()))
            text = extract_structured_text(native.within_bbox(box))
            crossing = [c for c in native.chars if
                        c['x0'] < box[2] and c['x1'] > box[0] and c['top'] < box[3] and c['bottom'] > box[1]
                        and not (c['x0'] >= box[0] and c['x1'] <= box[2] and c['top'] >= box[1] and c['bottom'] <= box[3])]
            if crossing:
                warnings.append("The boundary crosses text. Enlarge the area to include full characters, headings and footnotes.")
        except Exception as exc:
            warnings.append(f"Text could not be extracted from this area: {exc}")
        if not text.strip():
            warnings.append("No native text in this area.")
        return Capture(page, "area", rect_tuple(rect), text, None, (width, height), warnings=warnings)

    def close(self):
        if self.plumber is not None:
            self.plumber.close()
            self.plumber = None
