"""PDF coordinates are displayed-page points, origin at the top left."""
from __future__ import annotations

import hashlib
import io
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

import pdfplumber
from PySide6.QtCore import QPointF, QRect, QRectF, QSize
from PySide6.QtGui import QColor, QImage, QPainter, QPainterPath, QPolygonF
from PySide6.QtPdf import QPdfDocument
from .report_map import load_cached_map, load_questions_ledger


def extract_structured_text(crop) -> str:
    """Format tabular PDF crops as Markdown tables with superscript footnotes; preserve prose layout elsewhere."""
    chars = crop.chars
    if not chars:
        return ""
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
            if c["x0"] - cur[-1]["x1"] > max(8.0, main_size * 1.25):
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
            out = []
            for i, c in enumerate(seg_chars):
                txt = c["text"]
                if i > 0:
                    prev = seg_chars[i - 1]
                    if c["x0"] - prev["x1"] > max(1.0, c["size"] * 0.18) and prev["text"] != " " and txt != " ":
                        out.append(" ")
                if (c["size"] < msize * 0.75) and txt.strip().isalnum():
                    out.append(f"[^{txt.strip()}]")
                else:
                    out.append(txt)
            text_val = re.sub(r"\[\^([^\]]+)\]\s*\[\^([^\]]+)\]", r"[^\1\2]", "".join(out).strip())
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

    cols = []
    for s in sorted([seg for pl in table_rows for seg in pl["segs"]], key=lambda s: (s["x1"] - s["x0"], s["x0"])):
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
    if len(cols) < 2:
        return crop.extract_text(layout=True) or ""

    h_ys = sorted({round(l["top"], 1) for l in (crop.lines + crop.rects) if (l["x1"] - l["x0"]) > (crop.width * 0.4)})
    table_lines = parsed_lines[t_start:t_end + 1]

    mapped_rows = []
    for pl in table_lines:
        if len(pl["segs"]) == 1 and pl["segs"][0]["x1"] > cols[1]["x0"] + 5 and pl["segs"][0]["x0"] < cols[0]["x1"]:
            mapped_rows.append({"type": "full", "top": pl["top"], "bottom": pl["bottom"], "text": pl["segs"][0]["text"]})
            continue
        cells = [""] * len(cols)
        for seg in pl["segs"]:
            best_idx = min(
                range(len(cols)),
                key=lambda i: 0 if (min(seg["x1"], cols[i]["x1"]) - max(seg["x0"], cols[i]["x0"])) > 0
                else min(abs(seg["x0"] - cols[i]["x1"]), abs(seg["x1"] - cols[i]["x0"])),
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
    if out_lines:
        out_lines.append("")
    out_lines.append("| " + " | ".join(header_cells) + " |")
    out_lines.append("| " + " | ".join("---" for _ in cols) + " |")
    for r in body_rows:
        if r["type"] == "full":
            out_lines.append(f"| **{r['text']}** |" + " |" * (len(cols) - 1))
        else:
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
    image: QImage
    page_size: tuple[float, float]
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
        self.document = QPdfDocument()
        self.plumber = None
        result = self.document.load(str(self.path))
        if result != QPdfDocument.Error.None_ or self.document.pageCount() < 1:
            self.document.close()
            raise ValueError(f"Cannot open PDF ({result.name}). Password-protected PDFs are not supported yet.")
        try:
            self.plumber = pdfplumber.open(io.BytesIO(self.data))
        except Exception:
            self.document.close()
            raise
        self.report_map = load_cached_map(self.sha256, self.page_count)
        self.questions_ledger = load_questions_ledger(self.sha256)

    @property
    def page_count(self) -> int:
        return self.document.pageCount()

    def size(self, page: int) -> tuple[float, float]:
        if not 1 <= page <= self.page_count:
            raise ValueError("Physical page is outside the document.")
        size = self.document.pagePointSize(page - 1)
        return size.width(), size.height()

    def verify_unchanged(self) -> None:
        with self.path.open("rb") as stream:
            current = hashlib.file_digest(stream, "sha256").hexdigest()
        if current != self.sha256:
            raise ValueError("The source PDF changed since it was opened. Reopen it before saving.")

    def render(self, page: int, pixels_per_point: float = 2.0) -> QImage:
        width, height = self.size(page)
        scale = min(pixels_per_point, math.sqrt(24_000_000 / (width * height)))
        rendered = self.document.render(page - 1, QSize(math.ceil(width * scale), math.ceil(height * scale)))
        if rendered.isNull():
            raise ValueError("This PDF page could not be rendered.")
        # PDF paper is often transparent in the renderer. Composite onto white
        # so previews/exports remain readable in dark image viewers and chats.
        image = QImage(rendered.size(), QImage.Format.Format_RGB32)
        image.fill(QColor("white"))
        painter = QPainter(image)
        painter.drawImage(0, 0, rendered)
        painter.end()
        return image

    def selection(self, page: int, start: QPointF, end: QPointF):
        return self.document.getSelection(page - 1, start, end)

    def _crop_image(self, page: int, rect: QRectF, polygons: list[QPolygonF] | None = None) -> QImage:
        full = self.render(page, 3.0)  # 216 dpi where the memory cap permits.
        width, height = self.size(page)
        sx, sy = full.width() / width, full.height() / height
        left, top = math.floor(rect.left() * sx), math.floor(rect.top() * sy)
        right, bottom = math.ceil(rect.right() * sx), math.ceil(rect.bottom() * sy)
        pixels = QRect(left, top, right - left, bottom - top).intersected(full.rect())
        crop = full.copy(pixels)
        if not polygons:
            return crop
        # Text selections may span lines/columns. Hide unselected content inside
        # their enclosing rectangle rather than silently export neighbouring text.
        masked = QImage(crop.size(), QImage.Format.Format_ARGB32)
        masked.fill(QColor("white"))
        path = QPainterPath()
        for polygon in polygons:
            mapped = QPolygonF([QPointF(p.x() * sx - pixels.left(), p.y() * sy - pixels.top()) for p in polygon])
            path.addPolygon(mapped)
        painter = QPainter(masked)
        painter.setClipPath(path)
        painter.drawImage(0, 0, crop)
        painter.end()
        return masked

    def capture_text(self, page: int, start: QPointF, end: QPointF) -> Capture:
        selection = self.selection(page, start, end)
        if not selection.isValid() or not selection.text().strip():
            raise ValueError("No selectable text here. Use Area selection for a scanned page or a table.")
        width, height = self.size(page)
        rect = selection.boundingRectangle().intersected(QRectF(0, 0, width, height))
        polygons = selection.bounds()
        return Capture(
            page, "text", rect_tuple(rect), selection.text(), self._crop_image(page, rect, polygons),
            (width, height), [[[p.x(), p.y()] for p in poly] for poly in polygons],
            (selection.startIndex(), selection.endIndex()),
            warnings=["Native PDF text order may differ from visual reading order; check the image."],
        )

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
            # Qt reports float page sizes; pdfminer keeps decimal PDF values.
            # Clamp sub-point rounding at the original box before strict crop.
            box = (max(native.bbox[0], x + rect.left()), max(native.bbox[1], y + rect.top()),
                   min(native.bbox[2], x + rect.right()), min(native.bbox[3], y + rect.bottom()))
            # Fully enclosed characters only: don't include text from the other
            # side of a crop boundary. The image is retained to expose clipping.
            text = extract_structured_text(native.within_bbox(box))
            crossing = [c for c in native.chars if
                        c['x0'] < box[2] and c['x1'] > box[0] and c['top'] < box[3] and c['bottom'] > box[1]
                        and not (c['x0'] >= box[0] and c['x1'] <= box[2] and c['top'] >= box[1] and c['bottom'] <= box[3])]
            if crossing:
                warnings.append("The boundary crosses text. Enlarge the area to include full characters, headings and footnotes.")
        except Exception as exc:
            warnings.append(f"Text could not be extracted from this area: {exc}")
        if not text.strip():
            warnings.append("No native text in this area. Upload the image to a model that can read images; no OCR was run.")
        return Capture(page, "area", rect_tuple(rect), text, self._crop_image(page, rect), (width, height), warnings=warnings)

    def close(self):
        if self.plumber is not None:
            self.plumber.close()
            self.plumber = None
        self.document.close()
