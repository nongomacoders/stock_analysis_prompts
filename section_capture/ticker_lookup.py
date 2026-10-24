"""Intelligent ticker examination and prompt appropriateness verification.

Inspects entered company tickers locally (detecting existing hubs and registered metadata)
or via OpenRouter LLM to discover corporate name, JSE/ICB sector, and assess whether
Stage 1 Forensic Audit and Stage 2 Institutional Valuation prompts are appropriate.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from PySide6.QtCore import QThread, Signal

from companies import find_company_dir
from companies.sectors import (
    SECTOR_REGISTRY,
    get_all_sector_codes,
    get_sector_config,
    normalize_sector_code,
    resolve_sector_alias,
)
from section_capture.db import KNOWN_COMPANIES
from section_capture.openrouter import get_model_display_name, get_openrouter_api_key, query_openrouter
from section_capture.packages import has_sector_prompt
from section_capture.report_map import has_orientation_prompt


def examine_ticker_locally(ticker: str) -> dict[str, Any] | None:
    """Checks if a company hub or registered metadata already exists locally for the ticker."""
    t_up = ticker.strip().upper()
    if not t_up:
        return None

    # 1. Check existing hub on disk under companies/<sector>/<ticker>
    found = find_company_dir(t_up)
    if found:
        sector_code, company_dir = found
        known_name = KNOWN_COMPANIES.get(t_up, (f"{t_up} Limited", sector_code))[0]
        # Check if company has an existing config.py with company_title
        cfg_file = company_dir / "models" / "config.py"
        if cfg_file.exists():
            try:
                for line in cfg_file.read_text(encoding="utf-8").splitlines():
                    if "company_name" in line and "=" in line:
                        val = line.split("=", 1)[1].strip().strip('"\'')
                        if val:
                            known_name = val
                            break
            except Exception:
                pass

        pdf_count = 0
        sources_dir = company_dir / "sources"
        if sources_dir.exists():
            pdf_count = len([p for p in sources_dir.glob("*.pdf") if "sens" not in p.name.lower()])

        return {
            "ticker": t_up,
            "company_name": known_name,
            "sector_code": sector_code,
            "company_dir": company_dir,
            "hub_exists": True,
            "pdf_count": pdf_count,
            "source": "local_filesystem",
        }

    # 2. Check KNOWN_COMPANIES registry
    if t_up in KNOWN_COMPANIES:
        name, sec = KNOWN_COMPANIES[t_up]
        return {
            "ticker": t_up,
            "company_name": name,
            "sector_code": sec,
            "company_dir": None,
            "hub_exists": False,
            "pdf_count": 0,
            "source": "known_registry",
        }

    return None


def check_prompt_appropriateness(sector_code: str) -> dict[str, Any]:
    """Inspects whether dedicated Stage 1 and Stage 2 prompts & forensic models are active for the sector."""
    sec = (sector_code or "").lower().strip()
    if not sec or sec not in SECTOR_REGISTRY:
        return {
            "sector_code": sec,
            "is_registered_sector": False,
            "stage1_supported": False,
            "stage2_supported": False,
            "has_orientation_prompt": False,
            "has_reading_prompt": False,
            "status": "New Sector Required",
            "summary": f"Sector '{sec}' is not yet registered in the equity research pipeline.",
            "guidance": f"Run `python new_sector.py {sec or 'sector_code'} --name \"...\"` to onboard this sector.",
        }

    cfg = get_sector_config(sec)
    has_orient = has_orientation_prompt(sec)
    has_brief = has_sector_prompt(sec)

    # Check Stage 1 forensic directives in export_stage1.py
    stage1_supported = False
    from workflow.export_stage1 import build_stage1_prompt_content
    try:
        # Dry-run check against dummy sections
        dummy_sec = [{"section_number": 1, "section_id": "D001", "heading": "Test", "subheading": "", "analyst_question": "", "selected_text": "Sample", "stored_questions_snapshot": "", "llm_response": ""}]
        build_stage1_prompt_content(dummy_sec, "Test Corp", "TST", detected_sector=sec, filename="test.pdf")
        stage1_supported = True
    except ValueError as ve:
        if "does not have dedicated Stage 1" in str(ve):
            stage1_supported = False
        else:
            stage1_supported = True
    except Exception:
        stage1_supported = True

    # Check Stage 2 valuation model in generate_stage2.py
    stage2_supported = False
    from workflow.generate_stage2 import generate_stage2_prompt
    try:
        generate_stage2_prompt("TST", "Test Corp", detected_sector=sec, stage1_content="test")
        stage2_supported = True
    except ValueError as ve:
        if "does not have a dedicated Stage 2" in str(ve):
            stage2_supported = False
        else:
            stage2_supported = True
    except Exception:
        stage2_supported = True

    all_ok = has_orient and has_brief and stage1_supported and stage2_supported
    status = "Appropriate & Ready" if all_ok else "Partially Configured"

    return {
        "sector_code": sec,
        "display_name": cfg.display_name,
        "jse_code": cfg.jse_code,
        "icb_code": cfg.icb_code,
        "is_registered_sector": True,
        "stage1_supported": stage1_supported,
        "stage2_supported": stage2_supported,
        "has_orientation_prompt": has_orient,
        "has_reading_prompt": has_brief,
        "stage1_persona": cfg.stage1_persona,
        "stage2_persona": cfg.stage2_persona,
        "status": status,
        "summary": f"Dedicated {cfg.display_name} prompt templates and forensic models active.",
        "guidance": "",
    }


def build_ticker_examination_prompt(ticker: str) -> str:
    """Builds a structured prompt for OpenRouter to discover company details and assess Stage 1/2 appropriateness."""
    registered_sectors = ", ".join(sorted(get_all_sector_codes()))
    return f"""You are a senior Johannesburg Stock Exchange (JSE) and FTSE/JSE ICB equity research analyst.
Examine the following stock ticker symbol on the JSE:

Ticker: {ticker.strip().upper()}

Please provide accurate, verified details on this company and assess whether our two-stage institutional research pipeline prompts are appropriate for its business and accounting model:

- Stage 1 Mandate: Cognitive Forensic Accounting Audit (audits accounting policies, IFRS recognition, balance sheet quality, debt covenants, and segmental earnings before valuation).
- Stage 2 Mandate: Institutional Valuation Note (2-year operational forecast, SOTP DCF or relevant intrinsic valuation model, target price in ZAR, and monitoring triggers).

Registered sector options in our system: [{registered_sectors}].

Return ONLY a valid JSON object with the following exact keys:
{{
  "ticker": "{ticker.strip().upper()}",
  "company_name": "Official Full Legal Company Name",
  "jse_sector": "Official FTSE/JSE ICB Sector Name",
  "icb_code": "Official ICB numeric code (e.g. 30201020, 551030)",
  "matched_sector_code": "One of [{registered_sectors}] or closest industry slug",
  "business_summary": "1-2 sentence description of primary operations and profit drivers.",
  "stage1_appropriateness": {{
    "status": "Appropriate" or "Requires Special Focus",
    "focus_areas": "Core accounting junctions to audit (e.g. revenue recognition, ECL staging, capex capitalization, lease liabilities).",
    "caveats": "Any accounting complexity, non-IFRS metrics, or risk junctions specific to this asset."
  }},
  "stage2_appropriateness": {{
    "status": "Appropriate" or "Requires Special Focus",
    "recommended_valuation_model": "Primary intrinsic valuation methodology (e.g. SOTP DCF, Dividend Discount Model, NAV, EV/EBITDA).",
    "key_drivers": "The top 2-3 forward operational and cash flow drivers to forecast."
  }}
}}
"""


def parse_examination_response(raw_text: str) -> dict[str, Any]:
    """Robustly extracts and parses JSON data from the LLM examination response."""
    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
        text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)

    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        text = match.group(0)

    try:
        data = json.loads(text)
        if isinstance(data, dict):
            # Normalize matched_sector_code
            raw_sec = data.get("matched_sector_code", "")
            data["matched_sector_code"] = normalize_sector_code(raw_sec) or resolve_sector_alias(raw_sec) or raw_sec.lower()
            return data
    except Exception:
        pass

    return {
        "error": "Failed to parse structured JSON from examination response",
        "raw": raw_text,
    }


class TickerExamineWorker(QThread):
    """Background worker executing OpenRouter examination query without blocking Qt event loop."""

    finished_examination = Signal(dict)
    failed_examination = Signal(str)

    def __init__(self, ticker: str, parent=None):
        super().__init__(parent)
        self.ticker = ticker.strip().upper()

    def run(self):
        try:
            api_key = get_openrouter_api_key()
            if not api_key:
                self.failed_examination.emit("OpenRouter API key not configured in secrets.env or environment.")
                return

            prompt = build_ticker_examination_prompt(self.ticker)
            resp = query_openrouter(prompt, timeout=60, max_tokens=2048)
            content = resp[0] if isinstance(resp, tuple) else resp
            parsed = parse_examination_response(content)

            if "error" in parsed and "company_name" not in parsed:
                self.failed_examination.emit(f"Could not parse company details: {parsed.get('error')}")
                return

            self.finished_examination.emit(parsed)
        except Exception as exc:
            self.failed_examination.emit(str(exc))
