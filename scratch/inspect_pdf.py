import sys
import pypdfium2 as pdfium

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

pdf_path = r"companies/consumer_lending/NTU/sources/completed/1H26/nutunlimitedcondensedconsolidatedafs31march2026.pdf"
doc = pdfium.PdfDocument(pdf_path)
page_count = len(doc)
print(f"Total physical pages: {page_count}")

# Check bookmarks / TOC
try:
    toc = doc.get_toc()
    print(f"TOC entries count: {len(list(toc))}")
    for item in doc.get_toc():
        print(f"Level {item.level}: {item.title} -> Page {item.page_index + 1}")
except Exception as e:
    print("Error reading TOC:", e)

# Print first 200 chars of each page to see what's on each page
for i in range(page_count):
    page = doc.get_page(i)
    text = page.get_textpage().get_text_range()
    first_line = text.strip().split("\n")[0] if text.strip() else "(empty)"
    first_few = " ".join(text.strip().split()[:10])
    print(f"Page {i+1}: {first_few[:80]}")
    page.close()

doc.close()
