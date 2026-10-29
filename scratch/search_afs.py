import pdfplumber
from pathlib import Path

afs_pdf = Path("companies/retail/DCP/sources/completed/FY26/1780031707-FY2026AnnualFinancialStatements.pdf")

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

terms = [
    "gearing",
    "supply chain financing",
    "supplier finance",
    "reverse factoring",
    "standard bank",
    "bullet",
    "headline earnings per share",
    "cash generated from operations",
    "reconciliation of headline earnings",
    "note 23",
    "note 27",
    "note 29",
    "note 31",
]

res = search_pdf(afs_pdf, terms)
for k, v in res.items():
    print(f"{k}: pages {v[:10]} (total {len(v)})")
