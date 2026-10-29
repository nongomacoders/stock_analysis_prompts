import sys
import pypdfium2 as pdfium

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pdf_path = r"companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf"
doc = pdfium.PdfDocument(pdf_path)

def dump_pages(pages, out_filename):
    with open(out_filename, "w", encoding="utf-8") as f:
        for p_num in pages:
            page = doc.get_page(p_num - 1)
            text = page.get_textpage().get_text_range()
            f.write(f"\n--- PHYSICAL PAGE {p_num} ---\n")
            f.write(text)
            page.close()
    print(f"Dumped pages {pages} to {out_filename}")

dump_pages([3, 4, 5, 6, 8, 9, 11, 12], "scratch/pages_highlights_statements.txt")
dump_pages([13, 14, 15, 16, 17, 18, 19], "scratch/pages_notes_1_to_5.txt")
dump_pages([20, 21, 22, 23, 24, 25, 26, 27, 28, 29], "scratch/pages_notes_6_risk_fv.txt")
dump_pages([30, 31, 32, 33, 34, 35, 36], "scratch/pages_note_7_segments.txt")

doc.close()
