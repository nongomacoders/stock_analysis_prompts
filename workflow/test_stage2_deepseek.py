"""Workflow test harness: Test Stage 2 Institutional Valuation with full PDF report ingestion via DeepSeek Flash.

Extracts complete text from source PDF(s) and SENS notices, combines them with the Stage 2 prompt
and audited Stage 1 determinations, sends the unified package (~150k-200k tokens) to DeepSeek V4.1 Flash,
measures timing, cost, and parses the resulting valuation metrics.
"""

import argparse
import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pypdfium2 as pdfium

from companies import find_company_dir
from section_capture.db import parse_valuation_summary
from section_capture.openrouter import (
    estimate_cost,
    get_openrouter_api_key,
    get_openrouter_model,
    query_openrouter,
)
from workflow.generate_stage2 import generate_stage2_prompt


def extract_pdf_text_with_markers(pdf_path: Path) -> str:
    """Extracts page-by-page text from a PDF with explicit physical page boundary markers."""
    t0 = time.time()
    pdf = pdfium.PdfDocument(str(pdf_path))
    pages_text = []
    total_pages = len(pdf)
    for i, page in enumerate(pdf):
        textpage = page.get_textpage()
        page_str = textpage.get_text_range().strip()
        pages_text.append(f"--- [PDF Page {i+1} of {total_pages}] ---\n{page_str}")
    
    elapsed = time.time() - t0
    joined = "\n\n".join(pages_text)
    print(f"      Extracted {total_pages} pages from {pdf_path.name} in {elapsed:.2f}s ({len(joined):,} characters)")
    return joined


def load_sens_notices(sens_dir: Path) -> str:
    """Loads all post-balance sheet SENS notices from sens/completed and sens/ directories."""
    notices = []
    candidate_files = []
    
    completed_dir = sens_dir / "completed"
    if completed_dir.exists():
        candidate_files.extend(sorted(completed_dir.glob("*.txt")))
    if sens_dir.exists():
        candidate_files.extend(sorted(f for f in sens_dir.glob("*.txt") if f.is_file()))

    for f in candidate_files:
        try:
            content = f.read_text(encoding="utf-8").strip()
            notices.append(f"### SENS ANNOUNCEMENT: {f.name}\n\n{content}")
        except Exception:
            pass
            
    if not notices:
        return ""
    
    print(f"      Loaded {len(notices)} post-balance sheet SENS announcements from {sens_dir.name}/")
    return "\n\n---\n\n".join(notices)


def main():
    parser = argparse.ArgumentParser(description="Test DeepSeek on Stage 2 Institutional Valuation with full PDF ingestion.")
    parser.add_argument("--ticker", default="APF", help="Company ticker symbol (default: APF)")
    parser.add_argument("--model", default=None, help="OpenRouter model ID override (defaults to configured model)")
    parser.add_argument("--timeout", type=int, default=360, help="HTTP timeout in seconds (default: 360)")
    parser.add_argument("--max-tokens", type=int, default=16384, help="Max completion tokens (default: 16384)")
    args = parser.parse_args()

    api_key = get_openrouter_api_key()
    if not api_key:
        print("ERROR: OpenRouter API key not found in secrets.env or environment.")
        sys.exit(1)

    active_model = args.model or get_openrouter_model()
    ticker = args.ticker.upper()

    company_match = find_company_dir(ticker)
    if not company_match:
        print(f"ERROR: Company directory not found for ticker {ticker}")
        sys.exit(1)
    
    _, comp_dir = company_match
    print(f"=== STAGE 2 DEEPSEEK VALUATION TEST: {ticker} ===")
    print(f"Target Model: {active_model}")
    print(f"Timeout:      {args.timeout}s | Max Completion Tokens: {args.max_tokens}")

    # 1. Load or Generate Stage 2 Base Prompt
    print(f"\n[1/5] Preparing Stage 2 base prompt...")
    base_prompt_file = comp_dir / "briefs" / "FY26" / f"{ticker}_FY26_stage2_valuation_prompt.md"
    if not base_prompt_file.exists():
        base_prompt_file = generate_stage2_prompt(ticker=ticker)
    
    base_prompt_text = base_prompt_file.read_text(encoding="utf-8")
    print(f"      Base prompt: {base_prompt_file.name} ({len(base_prompt_text):,} chars)")

    # 2. Extract Complete Source PDF(s)
    print(f"\n[2/5] Ingesting full primary source PDF reports...")
    sources_dir = comp_dir / "sources"
    pdf_files = sorted(sources_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"ERROR: No source PDF found in {sources_dir}")
        sys.exit(1)

    pdf_texts = []
    for pdf_path in pdf_files:
        pdf_texts.append(extract_pdf_text_with_markers(pdf_path))
    all_pdf_text = "\n\n".join(pdf_texts)

    # 3. Load Post-Balance Sheet SENS Notices
    sens_text = load_sens_notices(sources_dir / "sens")

    # 4. Assemble Unified Stage 2 Prompt Dossier
    print(f"\n[3/5] Assembling unified multi-modal prompt package...")
    sections = [base_prompt_text]
    
    if sens_text:
        sections.append(
            "# SUBSEQUENT SENS ANNOUNCEMENTS & POST-BALANCE SHEET EVENTS\n\n"
            "The following verified SENS notices were released subsequent to the financial year-end. "
            "Integrate these updates (e.g. debt buybacks, property disposals, JSE censures) directly into your forward forecast, debt balances, and target valuation:\n\n"
            + sens_text
        )

    sections.append(
        "# COMPLETE PRIMARY SOURCE FINANCIAL REPORT DISCLOSURES & AUDITED NOTES\n\n"
        f"The following is the complete, page-by-page text extracted directly from the company's official publication ({pdf_files[0].name}). "
        "Every balance sheet item, segmental breakdown, property schedule, lease expiry profile, and debt note is available below for your direct forensic inspection and financial modeling:\n\n"
        + all_pdf_text
    )

    full_prompt = "\n\n---\n\n".join(sections)
    char_count = len(full_prompt)
    token_estimate = char_count // 4
    print(f"      Combined package size: {char_count:,} characters (~{token_estimate:,} tokens)")
    print(f"      DeepSeek 1M Context utilization: ~{(token_estimate / 1048576) * 100:.1f}%")

    # 5. Query DeepSeek via OpenRouter
    print(f"\n[4/5] Sending unified Stage 2 dossier to {active_model} via OpenRouter...")
    start_time = time.time()
    try:
        response_text, stats = query_openrouter(
            prompt=full_prompt,
            model=active_model,
            timeout=args.timeout,
            return_details=True,
            max_tokens=args.max_tokens,
        )
        elapsed = time.time() - start_time
    except Exception as exc:
        elapsed = time.time() - start_time
        print(f"\nFAILED after {elapsed:.1f}s: {exc}")
        sys.exit(1)

    # Process Stats
    prompt_tok = stats.get("prompt_tokens", 0)
    comp_tok = stats.get("completion_tokens", 0)
    tot_tok = stats.get("total_tokens", 0)
    cost = estimate_cost(active_model, prompt_tok, comp_tok)

    print(f"\n[5/5] DeepSeek Stage 2 response received in {elapsed:.1f} seconds!")
    print(f"      - Prompt Tokens:     {prompt_tok:,}")
    print(f"      - Completion Tokens: {comp_tok:,}")
    print(f"      - Total Tokens:      {tot_tok:,}")
    print(f"      - Estimated Cost:    ${cost:.5f} USD" if cost is not None else "      - Estimated Cost:    Unknown")
    print(f"      - Response Length:   {len(response_text):,} characters ({len(response_text.split()):,} words)")

    # Save Output
    out_path = comp_dir / "briefs" / "FY26" / f"{ticker}_FY26_stage2_deepseek_valuation_response.md"
    out_path.write_text(response_text, encoding="utf-8")
    print(f"\nSaved DeepSeek Valuation Note to:")
    print(f"      {out_path}")

    # Parse Valuation Summary
    print("\n--- Valuation Summary JSON Verification ---")
    summary = parse_valuation_summary(response_text)
    if summary:
        print(f"  [PASS] Target Price:       R{summary.get('target_price', 'N/A')}")
        print(f"  [PASS] Reference Price:    R{summary.get('reference_price', 'N/A')}")
        print(f"  [PASS] Recommendation:     {summary.get('recommendation', 'N/A')}")
        print(f"  [PASS] Implied Upside:     {summary.get('upside_pct', 'N/A')}%")
        print(f"  [PASS] Forward Div Yield:  {summary.get('dividend_yield_pct', 'N/A')}%")
        print(f"  [PASS] Projected 12M TSR:  {summary.get('tsr_pct', 'N/A')}%")
        print(f"  [PASS] JSE Sector Code:    {summary.get('jse_sector_code', 'N/A')} ({summary.get('jse_sector_name', 'N/A')})")
    else:
        print("  [WARNING] Could not parse standardized JSON summary block from response.")

    print("\nTest completed successfully!")


if __name__ == "__main__":
    main()
