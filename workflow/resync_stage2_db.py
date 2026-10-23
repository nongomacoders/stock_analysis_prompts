import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from section_capture.db import save_stage2_report, get_analyzed_stocks

ticker_notes = {
    "04298ad002d052400cc330807e0c3a32ba8d267cbb21179ffbcfeb0b09021841": "companies/it/IOC/briefs/FY26/IOC_FY26_stage2_valuation_note.md",
    "57f64ee4e94b2d9ad9b4f0d31edde7498e25de988a08b9b5d5a112d1f6e53c4a": "companies/reit/APF/briefs/FY26/APF_FY26_stage2_valuation_note.md",
    "d20cdd6e34bde68c871b45bc80f57dea9ce6b963d607464e3c28f0456ba9eae0": "companies/mining/ORN/briefs/FY26/ORN_FY26_stage2_valuation_note.md",
    "4f42a10cf4986783285887e8458999c314edb3c4dcc6985c18e1a46795b82e14": "companies/retail/LEW/briefs/FY26/LEW_FY26_stage2_valuation_note.md",
    "62b10bcd8e6216c00bbe005ae85a3c3341e01e82fd24af0516de18bf69c9b4dd": "companies/mining/PAN/briefs/FY26/PAN_FY26_stage2_valuation_note.md",
}

def main():
    print("Resyncing Stage 2 valuation notes to documents/analysis.sqlite...")
    for sha, rel_path in ticker_notes.items():
        note_file = PROJECT_ROOT / rel_path
        if not note_file.exists():
            print(f"Error: {rel_path} not found!")
            continue
        content = note_file.read_text(encoding="utf-8")
        ok = save_stage2_report(report_sha256=sha, response=content)
        print(f"Synced {rel_path} (SHA: {sha[:10]}...) -> success: {ok}")

    print("\nVerified Analyzed Stocks Coverage:")
    stocks = get_analyzed_stocks()
    for s in stocks:
        tp = s.get("target_price_zar")
        rp = s.get("reference_price_zar")
        rec = s.get("recommendation")
        up = s.get("upside_pct")
        sec = s.get("jse_sector_code")
        tp_str = f"R{tp:.2f}" if tp is not None else "N/A"
        rp_str = f"R{rp:.2f}" if rp is not None else "N/A"
        up_str = f"{up:+.1f}%" if up is not None else "N/A"
        print(f"  {s['ticker']:<5} | Sector: {str(sec):<6} | Target: {tp_str:<7} | Ref: {rp_str:<7} | Rec: {str(rec):<11} | Upside: {up_str}")

if __name__ == "__main__":
    main()
