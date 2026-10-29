"""Render evidence pages to PNG for visual acceptance (re-derivable evidence storage).

Renders are NOT committed in bulk; pages table stores path + sha256 + geometry, and this
committed script regenerates them deterministically from the SHA-verified source PDF.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

import pypdfium2 as pdfium
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication

EVIDENCE_DIR = Path(r"C:\Users\diond\AppData\Local\Temp\opencode\agentic_build_p1_renders")
SCALE = 3.0


def render_pages(pdf_path: Path, physical_pages: list[int], prefix: str = "PAN") -> dict[int, dict]:
    """Render pages and return {page: {path, sha256, width_px, height_px}}."""
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    app = QApplication.instance() or QApplication([])
    doc = pdfium.PdfDocument(pdf_path.read_bytes())
    out: dict[int, dict] = {}
    try:
        for pno in physical_pages:
            page = doc[pno - 1]
            bmp = page.render(scale=SCALE, rev_byteorder=True)
            img = QImage(bmp.buffer, bmp.width, bmp.height, bmp.stride, QImage.Format_RGB888)
            dest = EVIDENCE_DIR / f"{prefix}_{pno:02d}_p1.png"
            ok = img.save(str(dest))
            if not ok:
                raise RuntimeError(f"render save failed for page {pno}")
            raw = dest.read_bytes()
            out[pno] = {
                "path": str(dest),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "width_px": img.width(),
                "height_px": img.height(),
            }
            bmp.close()
            page.close()
    finally:
        doc.close()
    return out
