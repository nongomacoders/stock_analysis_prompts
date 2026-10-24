"""Workflow test harness: Evaluate DeepSeek toleration and performance on Stage 1 Forensic Audit Prompts.

Tests prompt submission against OpenRouter API using deepseek/deepseek-v4.1-flash-1017,
measures token usage, latency, cost, and saves output for forensic quality comparison.
"""

import argparse
import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from section_capture.openrouter import (
    estimate_cost,
    get_openrouter_api_key,
    get_openrouter_model,
    query_openrouter,
)
from workflow.export_stage1 import export_stage1_prompt


def main():
    parser = argparse.ArgumentParser(description="Test DeepSeek on Stage 1 Forensic Audit prompt.")
    parser.add_argument("--ticker", default="APF", help="Company ticker symbol (default: APF)")
    parser.add_argument("--compact", action="store_true", default=True, help="Use compacted prompt (default: True)")
    parser.add_argument("--full", dest="compact", action="store_false", help="Use uncompacted full prompt")
    parser.add_argument("--model", default=None, help="OpenRouter model ID override (defaults to configured model)")
    parser.add_argument("--timeout", type=int, default=300, help="HTTP timeout in seconds (default: 300)")
    parser.add_argument("--max-tokens", type=int, default=16384, help="Max completion tokens (default: 16384)")
    args = parser.parse_args()

    api_key = get_openrouter_api_key()
    if not api_key:
        print("ERROR: OpenRouter API key not found in secrets.env or environment.")
        sys.exit(1)

    active_model = args.model or get_openrouter_model()
    ticker = args.ticker.upper()

    print(f"=== STAGE 1 DEEPSEEK TOLERATION TEST: {ticker} ===")
    print(f"Target Model: {active_model}")
    print(f"Prompt Mode:  {'Compacted (Deduplicated Master Ledger)' if args.compact else 'Full (Uncompacted)'}")
    print(f"Timeout:      {args.timeout}s | Max Completion Tokens: {args.max_tokens}")

    # 1. Prepare / Export the Stage 1 prompt
    print(f"\n[1/4] Preparing Stage 1 prompt for {ticker}...")
    prompt_path = export_stage1_prompt(ticker=ticker, compact=args.compact)
    prompt_text = prompt_path.read_text(encoding="utf-8")
    char_count = len(prompt_text)
    token_estimate = char_count // 4
    print(f"      Prompt path: {prompt_path}")
    print(f"      Length:      {char_count:,} characters (~{token_estimate:,} tokens)")

    # 2. Query DeepSeek via OpenRouter
    print(f"\n[2/4] Sending prompt to {active_model} via OpenRouter...")
    start_time = time.time()
    try:
        response_text, stats = query_openrouter(
            prompt=prompt_text,
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

    # 3. Process Usage & Cost Stats
    prompt_tok = stats.get("prompt_tokens", 0)
    comp_tok = stats.get("completion_tokens", 0)
    tot_tok = stats.get("total_tokens", 0)
    cost = estimate_cost(active_model, prompt_tok, comp_tok)

    print(f"\n[3/4] DeepSeek API response received successfully in {elapsed:.1f} seconds!")
    print(f"      - Prompt Tokens:     {prompt_tok:,}")
    print(f"      - Completion Tokens: {comp_tok:,}")
    print(f"      - Total Tokens:      {tot_tok:,}")
    print(f"      - Estimated Cost:    ${cost:.5f} USD" if cost is not None else "      - Estimated Cost:    Unknown")
    print(f"      - Response Length:   {len(response_text):,} characters ({len(response_text.split()):,} words)")

    # 4. Save Response to Briefs Directory
    out_dir = prompt_path.parent
    mode_suffix = "compact" if args.compact else "full"
    out_path = out_dir / f"{ticker}_FY26_stage1_deepseek_response.md"
    out_path.write_text(response_text, encoding="utf-8")
    print(f"\n[4/4] Saved DeepSeek audit response to:")
    print(f"      {out_path}")

    # Check for presence of key Stage 1 sections
    print("\n--- Structural Compliance Verification ---")
    sections = [
        ("Section 1: True Economic Performance", ["economic performance", "earnings quality", "1. executive forensic audit summary"]),
        ("Section 2: Discrepancy & Anomaly Ledger", ["discrepancy", "anomaly ledger", "2. comprehensive discrepancy"]),
        ("Section 3: Multi-Period Data Schedules", ["data schedules", "schedules", "3. standardized"]),
        ("Section 4: Questions Ledger Verification", ["questions ledger", "verification", "4. systematic questions"]),
        ("Section 5: Stage 2 Valuation Bridge", ["valuation bridge", "baseline parameters", "5. stage 2 valuation bridge"]),
    ]
    resp_lower = response_text.lower()
    for name, keywords in sections:
        found = any(kw in resp_lower for kw in keywords)
        mark = "[PASS]" if found else "[MISSING]"
        print(f"  {mark:<9} {name}")

    print("\nTest completed successfully!")


if __name__ == "__main__":
    main()
