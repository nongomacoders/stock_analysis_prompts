"""PDF coordinates are displayed-page points, origin at the top left."""
from __future__ import annotations

import hashlib
import io
import math
from dataclasses import dataclass, field
from pathlib import Path

import pdfplumber
from PySide6.QtCore import QPointF, QRect, QRectF, QSize
from PySide6.QtGui import QColor, QImage, QPainter, QPainterPath, QPolygonF
from PySide6.QtPdf import QPdfDocument
from .report_map import load_cached_map


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
            text = native.within_bbox(box).extract_text(layout=True) or ""
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
