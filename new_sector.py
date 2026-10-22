#!/usr/bin/env python3
"""Sector Scaffolding Tool for Multi-Sector Equity Analysis.

Registers and scaffolds a new industry sector across the entire research workbench:
1. Adds SectorConfig to companies/sectors.py
2. Scaffolds prompts/<sector>/00-report-orientation/v1.0.0/prompt.md
3. Scaffolds prompts/<sector>/12-analyst-reading-brief/v1.1.0/prompt.md
4. Creates companies/<sector>/__init__.py

Usage:
    python new_sector.py healthcare --name "Healthcare & Pharmaceuticals" --short "Healthcare"
    python new_sector.py industrials --name "Industrials, Engineering & Capital Goods" --short "Industrials"
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

# Ensure UTF-8 output on Windows console
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent
SECTORS_FILE = ROOT / "companies/sectors.py"
PROMPTS_DIR = ROOT / "prompts"
COMPANIES_DIR = ROOT / "companies"

DEFAULT_COLORS = [
    ("#fdf4ff", "#86198f", "#f5d0fe"),  # Fuchsia
    ("#ecfeff", "#155e75", "#a5f3fc"),  # Cyan
    ("#f0fdf4", "#166534", "#bbf7d0"),  # Green
    ("#fff1f2", "#9f1239", "#fecdd3"),  # Rose
    ("#f8fafc", "#334155", "#cbd5e1"),  # Slate
]


def scaffold_orientation_prompt(sector_code: str, display_name: str) -> str:
    return f"""# {display_name.upper()} REPORT MAP ORIENTATION

**Sector:** {display_name} (`{sector_code}`)  
**Task Directive:** Identify and register major report sections from the table of contents or executive review.

## INSTRUCTIONS FOR REPORT ORIENTATION:
1. Scan the introductory sections, table of contents, and segmental overview.
2. Group the document into logical major functional sections:
   - Strategic & Executive Reports (Chairperson, CEO, Strategy & Targets, Material Risks)
   - Operational Reviews (Segmental operations, volume/service performance, operational KPIs)
   - Financial Review & Capital Allocation (CFO review, balance sheet & debt, cash flows)
   - Annual Financial Statements & Notes (Accounting policies, revenue recognition, key balance sheet notes)
   - Governance & Remuneration
3. Flag any complex accounting or operational disclosures that require dedicated verification.
"""


def scaffold_reading_brief_prompt(sector_code: str, display_name: str) -> str:
    return f"""# {display_name.upper()} FORENSIC READING BRIEF (STAGE 1 TIER 1)

**Sector:** {display_name} (`{sector_code}`)  
**Analysis Stage:** Section-by-Section Forensic Scrutiny  

## OBJECTIVE
You are assisting an institutional equity research analyst conducting a forensic accounting audit of {display_name} financial reports.
Analyze the captured section evidence below. Scrutinize all footnotes, accounting policies, segmental breakdowns, and management claims.

## SECTION-BY-SECTION SCRUTINY REQUIREMENTS:
1. **Accounting Integrity & Disclosures:**
   - Audit revenue recognition policies, contract assets/liabilities, and unbilled receivables.
   - Inspect capitalized costs vs expensed operational overheads.
   - Reconcile reported Adjusted EBITDA or normalized earnings against statutory operating profit.
2. **Operational Key Performance Indicators:**
   - Trace core unit economics, volume/capacity utilization, and pricing power.
   - Quantify structural cost inflation, labor costs, and operational bottlenecks.
3. **Balance Sheet & Liquidity Safeguards:**
   - Reconcile reported gross cash and debt against cash flow statement movements.
   - Assess covenant thresholds, maturity towers, and working capital cash drag.
4. **Dynamic Questions Ledger:**
   - Review prior unresolved questions in the ledger.
   - Resolve any questions where this section provides conclusive mathematical proof.
   - Formulate specific, quantified new questions with `Pending: [Target Section]` tags for upcoming disclosures.

## STRICT OUTPUT FORMATTING CONSTRAINTS (MANDATORY):
- Output clean, professional Markdown paragraphs and tables.
- Do NOT use raw unclosed HTML tags (`<br>`, `<span>`). Use `<br/>` if required.
- Place all new cross-section checks into a structured Markdown bullet list under 'Updated Open Questions Ledger'.
"""


def register_sector(
    code: str,
    name: str,
    short: str | None = None,
    stage1_persona: str | None = None,
    stage2_persona: str | None = None,
    aliases: list[str] | None = None,
) -> None:
    code = code.lower().strip()
    display_name = name.strip()
    short_label = short.strip() if short else code.capitalize()
    
    # Pick a distinct badge color palette
    from companies.sectors import SECTOR_REGISTRY
    if code in SECTOR_REGISTRY:
        print(f"[*] Sector '{code}' is already registered in companies/sectors.py")
        return

    color_idx = len(SECTOR_REGISTRY) % len(DEFAULT_COLORS)
    bg, fg, border = DEFAULT_COLORS[color_idx]

    s1_persona = stage1_persona or f"Managing Director and Senior Forensic {short_label} Financial Auditor"
    s2_persona = stage2_persona or f"Managing Director & Head of {short_label} Equity Research"
    sens_persona = s2_persona
    alias_tuple = tuple(aliases or [])

    # Format new SectorConfig entry
    new_entry = f"""    "{code}": SectorConfig(
        code="{code}",
        display_name="{display_name}",
        short_label="{short_label}",
        badge_bg="{bg}",
        badge_fg="{fg}",
        badge_border="{border}",
        stage1_persona="{s1_persona}",
        stage2_persona="{s2_persona}",
        sens_persona="{sens_persona}",
        aliases={repr(alias_tuple)},
    ),\n"""

    content = SECTORS_FILE.read_text(encoding="utf-8")
    marker = "SECTOR_REGISTRY: dict[str, SectorConfig] = {"
    idx = content.find(marker)
    if idx == -1:
        raise RuntimeError("Could not find SECTOR_REGISTRY definition in companies/sectors.py")

    insert_pos = content.find("\n}", idx)
    if insert_pos == -1:
        raise RuntimeError("Could not find closing bracket of SECTOR_REGISTRY in companies/sectors.py")

    updated = content[:insert_pos + 1] + new_entry + content[insert_pos + 1:]
    SECTORS_FILE.write_text(updated, encoding="utf-8")
    print(f"[+] Registered '{code}' in companies/sectors.py")


def scaffold_sector(
    code: str,
    name: str,
    short: str | None = None,
    stage1_persona: str | None = None,
    stage2_persona: str | None = None,
    aliases: list[str] | None = None,
) -> None:
    code = code.lower().strip()
    display_name = name.strip()
    short_label = short.strip() if short else code.capitalize()

    # 1. Register in sectors.py
    register_sector(code, display_name, short_label, stage1_persona, stage2_persona, aliases)

    # 2. Scaffold companies/<sector>/
    sector_hub = COMPANIES_DIR / code
    sector_hub.mkdir(parents=True, exist_ok=True)
    init_file = sector_hub / "__init__.py"
    if not init_file.exists():
        init_file.write_text(f'"""{display_name} companies."""\n', encoding="utf-8")
        print(f"[+] Created {init_file}")

    # 3. Scaffold prompts/<sector>/00-report-orientation/v1.0.0/prompt.md
    p0_dir = PROMPTS_DIR / code / "00-report-orientation/v1.0.0"
    p0_dir.mkdir(parents=True, exist_ok=True)
    p0_file = p0_dir / "prompt.md"
    if not p0_file.exists():
        p0_file.write_text(scaffold_orientation_prompt(code, display_name), encoding="utf-8")
        print(f"[+] Created {p0_file}")

    # 4. Scaffold prompts/<sector>/12-analyst-reading-brief/v1.1.0/prompt.md
    p1_dir = PROMPTS_DIR / code / "12-analyst-reading-brief/v1.1.0"
    p1_dir.mkdir(parents=True, exist_ok=True)
    p1_file = p1_dir / "prompt.md"
    if not p1_file.exists():
        p1_file.write_text(scaffold_reading_brief_prompt(code, display_name), encoding="utf-8")
        print(f"[+] Created {p1_file}")

    print(f"\n[✓] Sector '{code}' successfully created and integrated into all tools and UI views.")


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new sector across the research workbench.")
    parser.add_argument("code", help="Canonical lowercase sector code (e.g. healthcare, industrials, energy)")
    parser.add_argument("--name", required=True, help="Full display name (e.g. 'Healthcare & Pharmaceuticals')")
    parser.add_argument("--short", default=None, help="Short display label for UI badges/combos (e.g. 'Healthcare')")
    parser.add_argument("--stage1-persona", default=None, help="Auditor persona for Stage 1 prompt")
    parser.add_argument("--stage2-persona", default=None, help="Equity research persona for Stage 2 prompt")
    parser.add_argument("--aliases", nargs="*", default=None, help="Path or name aliases for automatic detection")

    args = parser.parse_args()
    scaffold_sector(
        code=args.code,
        name=args.name,
        short=args.short,
        stage1_persona=args.stage1_persona,
        stage2_persona=args.stage2_persona,
        aliases=args.aliases,
    )


if __name__ == "__main__":
    main()
