"""Render PAN physical pages 17 and 18 for coordinate acceptance and visual verification."""
from __future__ import annotations

import hashlib
import pathlib
import pypdfium2 as pdfium

PDF_PATH = pathlib.Path("companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf")
RENDER_DIR = pathlib.Path(r"C:\Users\diond\AppData\Local\Temp\opencode\agentic_build_p1_renders")
RENDER_DIR.mkdir(parents=True, exist_ok=True)


def render():
    pdf = pdfium.PdfDocument(str(PDF_PATH))
    results = {}
    for p_num in (17, 18):
        page = pdf[p_num - 1]
        bitmap = page.render(scale=3.0)
        img = bitmap.to_pil()
        out_path = RENDER_DIR / f"PAN_{p_num}_p1.png"
        img.save(str(out_path))
        with open(out_path, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        w, h_px = img.size
        results[p_num] = {
            "path": str(out_path),
            "sha256": h,
            "width": w,
            "height": h_px,
        }
        print(f"Rendered p.{p_num} -> {out_path} ({w}x{h_px}, sha256={h[:16]}...)")
    return results


if __name__ == "__main__":
    render()
