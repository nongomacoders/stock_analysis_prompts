import pdfplumber
import json
from pathlib import Path

afs_pdf = Path("companies/retail/DCP/sources/completed/FY26/1780031707-FY2026AnnualFinancialStatements.pdf")
pres_pdf = Path("companies/retail/DCP/sources/completed/FY26/1780031786-FY2026AnalystPresentation.pdf")
iar_pdf = Path("companies/retail/DCP/sources/completed/FY26/1785744572-DIS-CHEMIR2026INTERACTIVE.pdf")

# Let's extract specific pages from AFS
with pdfplumber.open(afs_pdf) as pdf:
    # Page 13: Statement of Comprehensive Income
    p13 = pdf.pages[12].extract_text()
    # Page 14: Statement of Financial Position
    p14 = pdf.pages[13].extract_text()
    # Page 17: Statement of Cash Flows
    p17 = pdf.pages[16].extract_text()
    # Page 36: Note 11 Earnings per share
    p36 = pdf.pages[35].extract_text()
    # Note 22 Leases (p55)
    p55 = pdf.pages[54].extract_text()
    # Note 23 Borrowings (p56)
    p56 = pdf.pages[55].extract_text()
    # Note 24 Payables / SCF (p57)
    p57 = pdf.pages[56].extract_text()
    # Note 27 Cash flow info (p60, 61, 62)
    p60 = pdf.pages[59].extract_text()
    p61 = pdf.pages[60].extract_text()
    p62 = pdf.pages[61].extract_text()
    # Note 29 Gearing (p79, 82)
    p79 = pdf.pages[78].extract_text()
    p82 = pdf.pages[81].extract_text()
    # Note 31 Subsequent events (p83, 84)
    p83 = pdf.pages[82].extract_text()
    p84 = pdf.pages[83].extract_text()

out_dir = Path("scratch/extracted_afs")
out_dir.mkdir(exist_ok=True)
(out_dir / "p13_pnl.txt").write_text(p13, encoding="utf-8")
(out_dir / "p14_balance_sheet.txt").write_text(p14, encoding="utf-8")
(out_dir / "p17_cash_flow.txt").write_text(p17, encoding="utf-8")
(out_dir / "p36_note11_heps.txt").write_text(p36, encoding="utf-8")
(out_dir / "p55_note22_leases.txt").write_text(p55, encoding="utf-8")
(out_dir / "p56_note23_borrowings.txt").write_text(p56, encoding="utf-8")
(out_dir / "p57_note24_payables_scf.txt").write_text(p57, encoding="utf-8")
(out_dir / "p60_61_note27_cashflow.txt").write_text(p60 + "\n--- PAGE 61 ---\n" + p61 + "\n--- PAGE 62 ---\n" + p62, encoding="utf-8")
(out_dir / "p79_82_note29_gearing.txt").write_text(p79 + "\n--- PAGE 82 ---\n" + p82, encoding="utf-8")
(out_dir / "p83_84_note31_subsequent.txt").write_text(p83 + "\n--- PAGE 84 ---\n" + p84, encoding="utf-8")

print("AFS pages extracted successfully.")
