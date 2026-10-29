import pdfplumber
from pathlib import Path

pres_pdf = Path("companies/retail/DCP/sources/completed/FY26/1780031786-FY2026AnalystPresentation.pdf")
iar_pdf = Path("companies/retail/DCP/sources/completed/FY26/1785744572-DIS-CHEMIR2026INTERACTIVE.pdf")

def search_pdf(pdf_path, search_terms):
    results = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            for term in search_terms:
                if term.lower() in text.lower():
                    if term not in results:
                        results[term] = []
                    results[term].append(page_idx + 1)
    return results

terms = ["gearing", "s189", "545", "505", "355", "358", "better rewards", "x, bigly", "bigly", "330", "115", "pipeline", "wholesale", "covenant", "bullet", "standard bank"]

print("--- PRES RESULTS ---")
res_pres = search_pdf(pres_pdf, terms)
for k, v in res_pres.items():
    print(f"{k}: pages {v}")

print("--- IAR RESULTS ---")
res_iar = search_pdf(iar_pdf, terms)
for k, v in res_iar.items():
    print(f"{k}: pages {v}")
