"""Render physical PDF pages (1-based) from SHA-verified originals using pypdfium2 + PySide6 QImage.
Also dumps pypdfium2 text for each page. Read-only on source PDFs."""
import hashlib, json, sys
from pathlib import Path
import pypdfium2 as pdfium
from PySide6.QtGui import QImage

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[8]
OUT = Path(__file__).resolve().parents[1] / "source_pages"
OUT.mkdir(exist_ok=True)
DOCS = {
    "NTU": (ROOT / "companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf",
            "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", [13, 21, 22, 23]),  # p13 = confirmation only, outside experiment capture
    "PAN": (ROOT / "companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf",
            "62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd", [48, 49, 50]),
}
record = {}
for key, (path, expected, pages) in DOCS.items():
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    record[key] = {"path": str(path), "expected": expected, "actual": actual, "match": actual == expected, "pages": pages}
    if actual != expected:
        print("HASH MISMATCH", key); continue
    pdf = pdfium.PdfDocument(str(path))
    record[key]["page_count"] = len(pdf)
    for p in pages:
        page = pdf[p - 1]
        tp = page.get_textpage()
        (OUT / f"{key}_{p}.txt").write_text(tp.get_text_range(), encoding="utf-8")
        tp.close()
        bm = page.render(scale=2.2, rev_byteorder=True)
        w, h = bm.width, bm.height
        buf = bytes(bm.buffer)
        img = QImage(buf, w, h, bm.stride, QImage.Format_RGBA8888 if bm.n_channels == 4 else QImage.Format_RGB888)
        img.copy().save(str(OUT / f"{key}_{p}.png"))
        bm.close(); page.close()
    pdf.close()
(OUT / "render_record.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
print(json.dumps(record, indent=2))
