"""Central SQLite persistence for report maps, captured sections, prompts, LLM responses, and question ledgers."""
from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from companies import PACKAGE_DIR, SECTORS
from companies.sectors import (
    get_icb_code,
    get_jse_sector_code,
    get_jse_sector_name,
    normalize_sector_code,
)

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "documents/analysis.sqlite"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS reports (
    sha256 TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    original_path TEXT NOT NULL,
    byte_size INTEGER NOT NULL DEFAULT 0,
    physical_page_count INTEGER NOT NULL,
    report_map_json TEXT,
    questions_ledger TEXT NOT NULL DEFAULT '',
    stage1_prompt TEXT,
    stage1_response TEXT,
    stage1_updated_at TEXT,
    stage2_prompt TEXT,
    stage2_response TEXT,
    stage2_updated_at TEXT,
    target_price_zar REAL,
    reference_price_zar REAL,
    recommendation TEXT,
    upside_pct REAL,
    dividend_yield_pct REAL,
    tsr_pct REAL,
    monitoring_triggers TEXT,
    valuation_summary_json TEXT,
    parent_report_sha256 TEXT,
    doc_type TEXT NOT NULL DEFAULT 'annual_report',
    announcement_date TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (parent_report_sha256) REFERENCES reports(sha256)
);

CREATE TABLE IF NOT EXISTS sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id TEXT UNIQUE NOT NULL,
    report_sha256 TEXT NOT NULL,
    section_number INTEGER NOT NULL,
    section_id TEXT NOT NULL,
    heading TEXT NOT NULL,
    subheading TEXT,
    analyst_question TEXT,
    selected_text TEXT NOT NULL,
    selections_json TEXT NOT NULL,
    stored_questions_snapshot TEXT,
    prompt TEXT NOT NULL,
    llm_response TEXT,
    manifest_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (report_sha256) REFERENCES reports(sha256)
);

CREATE TABLE IF NOT EXISTS app_state (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS market_quotes (
    ticker TEXT PRIMARY KEY,
    price_zar REAL NOT NULL,
    prev_close_zar REAL,
    currency TEXT NOT NULL,
    raw_price REAL NOT NULL,
    change_pct REAL,
    updated_at TEXT NOT NULL
);
"""


@dataclass
class SavedSection:
    package_id: str
    report_sha256: str
    section_number: int
    section_id: str
    name: str
    heading: str
    subheading: str | None
    analyst_question: str | None
    selected_text: str
    selections: list[dict]
    stored_questions: str | None
    prompt: str
    llm_response: str | None
    manifest: dict
    created_at: str
    db_path: Path

    @property
    def response_time_seconds(self) -> float | None:
        return self.manifest.get("review", {}).get("response_time_seconds")

    @property
    def cost_usd(self) -> float | None:
        return self.manifest.get("review", {}).get("cost_usd")

    @property
    def model_used(self) -> str | None:
        return self.manifest.get("review", {}).get("model")

    @property
    def total_tokens(self) -> int | None:
        t = self.manifest.get("review", {}).get("tokens")
        if isinstance(t, dict):
            return t.get("total_tokens")
        return None


def resolve_db_path(db_path: str | Path | None = None) -> Path:
    if db_path is None:
        target = Path(DB_PATH)
    else:
        candidate = Path(db_path)
        if candidate.suffix.lower() in {".sqlite", ".sqlite3", ".db"}:
            target = candidate
        else:
            target = candidate / "analysis.sqlite"
    target.parent.mkdir(parents=True, exist_ok=True)
    return target.resolve()


def to_relative_project_path(path: Path | str | None) -> str:
    """Normalizes a file or folder path as a forward-slash relative path to ROOT if inside it."""
    if not path:
        return ""
    p = Path(path)
    p_str = str(path).replace("\\", "/")
    if not p.is_absolute():
        return p_str
    try:
        rel = p.resolve().relative_to(ROOT.resolve())
        return str(rel).replace("\\", "/")
    except ValueError:
        parts = p.parts
        for i, part in enumerate(parts):
            if part.lower() == "companies":
                return "/".join(parts[i:])
        return p_str


def resolve_project_path(path_str: str | Path | None) -> Path | None:
    """Resolves a stored path string (relative or absolute) to a valid Path on the current machine."""
    if not path_str:
        return None
    p = Path(path_str)
    if p.is_absolute() and p.exists():
        return p
    cand = (ROOT / p).resolve()
    if cand.exists():
        return cand
    if p.is_absolute():
        parts = p.parts
        for i, part in enumerate(parts):
            if part.lower() == "companies":
                cand2 = (ROOT / Path(*parts[i:])).resolve()
                if cand2.exists():
                    return cand2
    return cand


KNOWN_COMPANIES: dict[str, tuple[str, str]] = {
    "LEW": ("Lewis Group Limited", "retail"),
    "PAN": ("Pan African Resources", "mining"),
    "ORN": ("Orion Minerals", "mining"),
    "TRU": ("Truworths International", "retail"),
    "HAR": ("Harmony Gold Mining", "mining"),
    "ANG": ("AngloGold Ashanti", "mining"),
    "GFI": ("Gold Fields", "mining"),
    "GRT": ("Growthpoint Properties", "reit"),
    "RDF": ("Redefine Properties", "reit"),
    "VKE": ("Vukile Property Fund", "reit"),
    "HYP": ("Hyprop Investments", "reit"),
    "ATT": ("Attacq Limited", "reit"),
    "FFB": ("Fortress Real Estate", "reit"),
    "EQU": ("Equites Property Fund", "reit"),
    "RES": ("Resilient REIT", "reit"),
    "IOC": ("iOCO Limited", "it"),
    "IOCO": ("iOCO Limited", "it"),
    "EOH": ("iOCO Limited", "it"),
    "ALH": ("Altron Limited", "it"),
    "DTC": ("Datatec Limited", "it"),
    "WBO": ("Wilson Bayly Holmes-Ovcon", "construction"),
    "WBHO": ("Wilson Bayly Holmes-Ovcon", "construction"),
    "RBX": ("Raubex Group", "construction"),
    "PPC": ("PPC Limited", "construction"),
    "AFT": ("Afrimat Limited", "construction"),
    "SSK": ("Stefanutti Stocks", "construction"),
    "CGR": ("Calgro M3 Holdings", "construction"),
    "CALGRO": ("Calgro M3 Holdings", "construction"),
}


def detect_company_meta(path_or_filename: str | Path | None) -> tuple[str, str, str]:
    """Infers (ticker, company_name, sector) from report path or filename."""
    if not path_or_filename:
        return "TARGET", "Unknown Asset", "retail"
    p = Path(path_or_filename)
    parts = [part.lower() for part in p.parts]

    # 1. Direct path match under companies/<sector>/<ticker>/...
    if "companies" in parts:
        idx = parts.index("companies")
        if idx + 2 < len(parts):
            cand_sec = parts[idx + 1]
            cand_ticker = parts[idx + 2].upper()
            if cand_sec in SECTORS:
                default_title = (
                    f"{cand_ticker} Technologies" if cand_sec == "it"
                    else (f"{cand_ticker} Properties" if cand_sec == "reit"
                    else (f"{cand_ticker} Construction" if cand_sec == "construction"
                    else (f"{cand_ticker} Group" if cand_sec == "retail" else f"{cand_ticker} Resources")))
                )
                name = KNOWN_COMPANIES.get(cand_ticker, (default_title, cand_sec))[0]
                return cand_ticker, name, cand_sec

    # 2. Check filename and path (excluding 'companies' directory name to avoid 'pan' in 'companies')
    s = str(path_or_filename).lower()
    s_clean = re.sub(r'[\/\\]companies[\/\\]', '/', s)
    fname = p.name.lower()

    # Check known companies
    for ticker, (name, sec) in KNOWN_COMPANIES.items():
        t_low = ticker.lower()
        n_words = [w.lower() for w in re.split(r'[\s\-_]+', name) if len(w) >= 4 and w.lower() not in {"group", "limited", "properties", "holdings", "technologies", "resources", "international", "financial"}]
        name_match = any(w in fname for w in n_words)
        if re.search(rf'\b{re.escape(t_low)}\b', fname) or t_low in fname or name.lower() in s_clean or name_match:
            real_ticker = "CGR" if ticker == "CALGRO" else ("IOC" if ticker in {"IOCO", "EOH"} else ticker)
            return real_ticker, name, sec

    # Check company directories on disk
    for sec in SECTORS:
        sec_dir = PACKAGE_DIR / sec
        if sec_dir.exists():
            for c in sec_dir.iterdir():
                if c.is_dir() and not c.name.startswith((".", "_")):
                    t_cand = c.name.lower()
                    if re.search(rf'\b{re.escape(t_cand)}\b', fname) or t_cand in s_clean:
                        t = c.name.upper()
                        if sec == "retail":
                            title = f"{t} Group"
                        elif sec == "reit":
                            title = f"{t} Properties"
                        elif sec == "it":
                            title = f"{t} Technologies"
                        elif sec == "finance":
                            title = f"{t} Financial"
                        else:
                            title = f"{t} Resources"
                        return t, title, sec

    # Fallback sector detection
    for cand_sec in SECTORS:
        if cand_sec in s_clean:
            return "TARGET", "Target Asset", cand_sec

    return "TARGET", "Target Asset", "retail"


def parse_valuation_summary(text: str | None) -> dict[str, Any]:
    """Extract executive valuation metrics and monitoring triggers from a Stage 2 note."""
    if not text:
        return {}
    res: dict[str, Any] = {}

    # ---------------------------------------------------------------------
    # Fast-Path: Standardized machine-readable JSON summary block (```json ... ```)
    # ---------------------------------------------------------------------
    json_blocks = re.findall(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', text, re.IGNORECASE)
    for jb in json_blocks:
        try:
            data = json.loads(jb)
            if isinstance(data, dict):
                has_metric = any(
                    k in data
                    for k in (
                        "target_price_zar", "target_price",
                        "reference_price_zar", "reference_price",
                        "recommendation", "implied_upside_pct", "upside_pct",
                    )
                )
                if has_metric:
                    tp = data.get("target_price_zar", data.get("target_price"))
                    ref = data.get("reference_price_zar", data.get("reference_price"))
                    rec = data.get("recommendation")
                    up = data.get("implied_upside_pct", data.get("upside_pct"))
                    dy = data.get("forward_dividend_yield_pct", data.get("dividend_yield_pct"))
                    tsr = data.get("projected_12m_tsr_pct", data.get("tsr_pct"))

                    if tp is not None:
                        try:
                            res["target_price"] = float(str(tp).replace("R", "").replace(",", "").strip())
                        except (ValueError, TypeError):
                            pass
                    if ref is not None:
                        try:
                            res["reference_price"] = float(str(ref).replace("R", "").replace(",", "").strip())
                        except (ValueError, TypeError):
                            pass
                    if rec:
                        res["recommendation"] = str(rec).strip().upper()
                    if up is not None:
                        try:
                            res["upside_pct"] = float(str(up).replace("%", "").strip())
                        except (ValueError, TypeError):
                            pass
                    if dy is not None:
                        try:
                            res["dividend_yield_pct"] = float(str(dy).replace("%", "").strip())
                        except (ValueError, TypeError):
                            pass
                    if tsr is not None:
                        try:
                            res["tsr_pct"] = float(str(tsr).replace("%", "").strip())
                        except (ValueError, TypeError):
                            pass
                    sec = data.get("sector") or data.get("jse_sector_code") or data.get("jse_sector_name")
                    if sec:
                        s_clean = normalize_sector_code(str(sec)) or str(sec).strip().lower()
                        if s_clean:
                            res["sector"] = s_clean
                    jse_c = data.get("jse_sector_code")
                    if jse_c and str(jse_c).strip():
                        res["jse_sector_code"] = str(jse_c).strip().upper()
                    jse_n = data.get("jse_sector_name")
                    if jse_n and str(jse_n).strip():
                        res["jse_sector_name"] = str(jse_n).strip()
                    t_json = data.get("ticker")
                    if t_json and str(t_json).strip():
                        res["_ticker"] = str(t_json).strip().upper()

                    # Extract triggers if included in JSON
                    if "monitoring_triggers" in data:
                        raw_trig = data["monitoring_triggers"]
                        if isinstance(raw_trig, list):
                            res["monitoring_triggers"] = "\n".join(f"- {t}" for t in raw_trig)
                        elif isinstance(raw_trig, str) and raw_trig.strip():
                            res["monitoring_triggers"] = raw_trig.strip()
                    break
        except Exception:
            continue

    sec2_idx = re.search(r'\n##\s*2[\.\s]', text)
    sec1_text = text[:sec2_idx.start()] if sec2_idx else text[:10000]

    # Clean table lines: join continuation lines within Section 1
    raw_lines = sec1_text.splitlines()
    joined_lines: list[str] = []
    cur_row = ""
    for line in raw_lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("|"):
            if cur_row:
                if not cur_row.endswith("|"):
                    cur_row += " " + s
                    if cur_row.endswith("|") and cur_row.count("|") >= 3:
                        joined_lines.append(cur_row)
                        cur_row = ""
                    continue
                else:
                    joined_lines.append(cur_row)
                    cur_row = s
            else:
                cur_row = s
        elif cur_row:
            cur_row += " " + s
            if cur_row.endswith("|") and cur_row.count("|") >= 3:
                joined_lines.append(cur_row)
                cur_row = ""
        else:
            if cur_row:
                joined_lines.append(cur_row)
                cur_row = ""
            joined_lines.append(line)
    if cur_row:
        joined_lines.append(cur_row)

    for line in joined_lines:
        s = line.strip()
        if not s:
            continue

        if s.startswith("|") and "|" in s[1:]:
            cells = [c.strip() for c in s.split("|") if c.strip()]
            if len(cells) < 2:
                continue
            metric = cells[0].lower()
            if "---" in metric or "institutional valuation metric" in metric or "valuation & market metric" in metric:
                continue

            # Target determinations are in cells[1:-1] if >= 3 cells, else cells[1:]
            det_cells = cells[1:-1] if len(cells) >= 3 else cells[1:]
            det_text = " ".join(det_cells)

            # 0. Sector
            if "sector" in metric and "sector" not in res:
                sec_raw = det_cells[0] if det_cells else ""
                s_norm = normalize_sector_code(sec_raw)
                if s_norm:
                    res["sector"] = s_norm

            # 1. Recommendation
            elif "recommendation" in metric and "recommendation" not in res:
                for c in reversed(det_cells):
                    m_start = re.search(r'^\*{0,2}(BUY|HOLD|SELL|OVERWEIGHT|UNDERWEIGHT|NEUTRAL)\b', c, re.IGNORECASE)
                    if m_start:
                        res["recommendation"] = m_start.group(1).upper()
                        break
                    m_any = re.search(r'\b(BUY|HOLD|SELL|OVERWEIGHT|UNDERWEIGHT|NEUTRAL)\b', c, re.IGNORECASE)
                    if m_any and not any(k in c.lower() for k in ["tranche", "basis", "source", "prior"]):
                        res["recommendation"] = m_any.group(1).upper()
                        break

            # 2. Target Price
            elif "target" in metric and "price" in metric and "target_price" not in res:
                prices: list[float] = []
                for m in re.finditer(r'R\s*([\d,\.]+)', det_text, re.IGNORECASE):
                    tail = det_text[m.end():m.end()+15].lower()
                    if re.match(r'\s*(?:bn|billion|m\b|million|/m|/month|m2|m²)', tail):
                        continue
                    try:
                        val = float(m.group(1).replace(",", ""))
                        if 0.001 <= val < 100000:
                            prices.append(val)
                    except ValueError:
                        pass
                if prices:
                    res["target_price"] = prices[-1]

            # 3. Reference Price
            elif ("reference" in metric or "current" in metric) and "price" in metric and "reference_price" not in res:
                prices = []
                for m in re.finditer(r'R\s*([\d,\.]+)', det_text, re.IGNORECASE):
                    tail = det_text[m.end():m.end()+15].lower()
                    if re.match(r'\s*(?:bn|billion|m\b|million|/m|/month|m2|m²)', tail):
                        continue
                    try:
                        val = float(m.group(1).replace(",", ""))
                        if 0.001 <= val < 100000:
                            prices.append(val)
                    except ValueError:
                        pass
                if prices:
                    res["reference_price"] = prices[-1]

            # 4. TSR (check before upside)
            elif ("tsr" in metric or "total shareholder return" in metric) and "tsr_pct" not in res:
                pcts = re.findall(r'([+\-]?[\d\.]+)%', det_text)
                if pcts:
                    try:
                        res["tsr_pct"] = float(pcts[-1])
                    except ValueError:
                        pass

            # 5. Upside
            elif "upside" in metric and "upside_pct" not in res:
                pcts = re.findall(r'([+\-]?[\d\.]+)%', det_text)
                if pcts:
                    try:
                        res["upside_pct"] = float(pcts[-1])
                    except ValueError:
                        pass

            # 6. Dividend Yield
            elif "dividend" in metric and "yield" in metric and "dividend_yield_pct" not in res:
                pcts = re.findall(r'([+\-]?[\d\.]+)%', det_text)
                if pcts:
                    try:
                        res["dividend_yield_pct"] = float(pcts[-1])
                    except ValueError:
                        pass

        else:
            # Bullet point or colon line
            lower = s.lower()
            if "recommendation" in lower and "recommendation" not in res:
                m = re.search(r'Recommendation[^\n:]*?:[^\n\r]*?\b(BUY|HOLD|SELL|OVERWEIGHT|UNDERWEIGHT|NEUTRAL)\b', s, re.IGNORECASE)
                if m:
                    res["recommendation"] = m.group(1).upper()
            elif "target" in lower and "price" in lower and "target_price" not in res:
                m = re.search(r'Target\s+Price[^\n:]*?:[^\n\r\d]*?R?[^\n\r\d]*?([\d,\.]+)', s, re.IGNORECASE)
                if m:
                    try:
                        res["target_price"] = float(m.group(1).replace(",", ""))
                    except ValueError:
                        pass
            elif ("reference" in lower or "current" in lower) and "price" in lower and "target" not in lower and "reference_price" not in res:
                m = re.search(r'(?:Reference|Current)[^\n:]*?Price[^\n:]*?:[^\n\r\d]*?R?[^\n\r\d]*?([\d,\.]+)', s, re.IGNORECASE)
                if m:
                    try:
                        res["reference_price"] = float(m.group(1).replace(",", ""))
                    except ValueError:
                        pass
            elif ("tsr" in lower or "total shareholder return" in lower) and "tsr_pct" not in res:
                m = re.search(r'(?:Total\s+Shareholder\s+Return|TSR)[^\n:]*?:[^\n\r]*?([+\-]?[\d\.]+)%', s, re.IGNORECASE)
                if m:
                    try:
                        res["tsr_pct"] = float(m.group(1))
                    except ValueError:
                        pass
            elif "upside" in lower and "upside_pct" not in res:
                m = re.search(r'Upside[^\n:]*?:[^\n\r]*?([+\-]?[\d\.]+)%', s, re.IGNORECASE)
                if m:
                    try:
                        res["upside_pct"] = float(m.group(1))
                    except ValueError:
                        pass
            elif "dividend" in lower and "yield" in lower and "dividend_yield_pct" not in res:
                m = re.search(r'Dividend\s+Yield[^\n:]*?:[^\n\r]*?([+\-]?[\d\.]+)%', s, re.IGNORECASE)
                if m:
                    try:
                        res["dividend_yield_pct"] = float(m.group(1))
                    except ValueError:
                        pass

    # Fallback to prose recommendation
    if "recommendation" not in res:
        prose_rec = re.search(
            r'\b(?:upgrade[d]?\s+(?:our\s+institutional\s+recommendation\s+)?(?:from\s+\w+\s+)?to|with\s+a\s+|recommendation\s+(?:of\s+|is\s+))\s*\*{0,2}(BUY|HOLD|SELL|OVERWEIGHT|UNDERWEIGHT|NEUTRAL)\b',
            sec1_text,
            re.IGNORECASE,
        )
        if prose_rec:
            res["recommendation"] = prose_rec.group(1).upper()

    if "sector" not in res:
        m_sec = re.search(r'\*\s*\*{0,2}Sector:\*{0,2}\s*([^\n\r]+)', sec1_text, re.IGNORECASE)
        if m_sec:
            s_norm = normalize_sector_code(m_sec.group(1))
            if s_norm:
                res["sector"] = s_norm

    # Monitoring Triggers / Action Plan
    trig_match = re.search(
        r'(?:###?\s*(?:(?:6\.?\s*)?(?:Actionable\s+Portfolio\s+)?Monitoring\s+Triggers|Institutional\s+Action\s+Plan\s+&|What\s+to\s+Watch\s+For).*?)(?=(\n## |\Z))',
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if trig_match:
        res["monitoring_triggers"] = trig_match.group(0).strip()

    t_hint = res.pop("_ticker", None)
    if not t_hint:
        if "orion minerals" in sec1_text.lower() or "(jse: orn" in sec1_text.lower() or "base metals mining" in sec1_text.lower():
            t_hint = "ORN"
    if "sector" in res:
        if "jse_sector_code" not in res:
            res["jse_sector_code"] = get_jse_sector_code(res["sector"], ticker=t_hint)
        if "jse_sector_name" not in res:
            res["jse_sector_name"] = get_jse_sector_name(res["sector"], ticker=t_hint)

    return res


DOC_TYPES: dict[str, dict[str, str]] = {
    "iar": {
        "code": "IAR",
        "label": "Integrated Annual Report (IAR)",
        "badge": "[IAR]",
        "desc": "Strategy, leadership reviews (CEO/CFO), high-level financials, governance & ESG",
    },
    "afs": {
        "code": "AFS",
        "label": "Annual Financial Statements (AFS)",
        "badge": "[AFS]",
        "desc": "Statutory primary statements, accounting policies & technical financial notes",
    },
    "presentation": {
        "code": "PRES",
        "label": "Results Presentation (PRES)",
        "badge": "[PRES]",
        "desc": "Investor / analyst slide deck & operational annexures",
    },
    "sens": {
        "code": "SENS",
        "label": "SENS / Continuous Disclosure (SENS)",
        "badge": "[SENS]",
        "desc": "Stock exchange continuous disclosure announcements",
    },
    "annual_report": {
        "code": "AR",
        "label": "General Annual Report (AR)",
        "badge": "[AR]",
        "desc": "Single combined annual integrated report",
    },
}


def get_doc_code(doc_type: str | None) -> str:
    """Returns the uppercase short code (e.g. 'IAR', 'AFS', 'PRES', 'SENS', 'AR')."""
    if not doc_type:
        return "AR"
    dt = doc_type.lower().strip()
    return DOC_TYPES.get(dt, {}).get("code", "AR")


def get_doc_badge(doc_type: str | None, announcement_date: str | None = None) -> str:
    """Returns the formatted badge for display (e.g. '[IAR]', '[AFS]', '[SENS 2026-09-15]')."""
    dt = (doc_type or "annual_report").lower().strip()
    if dt == "sens" and announcement_date:
        return f"[SENS {announcement_date}]"
    return DOC_TYPES.get(dt, {}).get("badge", "[AR]")


def detect_doc_type_and_date(path_or_filename: str | Path | None) -> tuple[str, str | None]:
    """Infers (doc_type, announcement_date) from report path or filename."""
    if not path_or_filename:
        return "annual_report", None
    p = Path(path_or_filename)
    filename = p.name.lower()
    path_str = str(p).lower().replace("\\", "/")

    # Extract announcement date (YYYYMMDD or YYYY-MM-DD or YYYY_MM_DD)
    date_match = re.search(r"\b(20\d{2})[-_]?(\d{2})[-_]?(\d{2})\b", filename)
    announcement_date = None
    if date_match:
        announcement_date = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"

    # Check SENS first
    if "/sources/sens/" in path_str or path_str.endswith("/sens") or "/sens/" in path_str:
        return "sens", announcement_date
    if "sens" in filename or "asx" in filename or "announcement" in filename:
        if not any(k in filename for k in ("annual", "year-end", "iar", "afs", "financial_statement")):
            return "sens", announcement_date

    # Check AFS (Annual Financial Statements)
    if any(k in filename for k in ("afs", "financial_statement", "financial-statement", "financial statement", "annual_financial_statements")):
        return "afs", announcement_date

    # Check IAR (Integrated Annual Report)
    if any(k in filename for k in ("iar", "integrated_report", "integrated-report", "integrated report", "integrated_annual_report")):
        return "iar", announcement_date

    # Check presentation / slides
    if any(k in filename for k in ("presentation", "deck", "slides")):
        return "presentation", announcement_date

    if any(k in filename for k in ("interim", "half-year", "h1", "hy")):
        return "interim", announcement_date

    return "annual_report", announcement_date


def auto_link_companion_reports(
    report_sha256: str,
    report_path: Path | str,
    doc_type: str | None = None,
    db_path: str | Path | None = None,
) -> str | None:
    """Finds and links companion/parent Annual Reports in the same company tree."""
    resolved = resolve_db_path(db_path)
    p = Path(report_path).resolve()
    sources_dir = None
    if p.parent.name.lower() == "sens" and p.parent.parent.name.lower() == "sources":
        sources_dir = p.parent.parent
    elif p.parent.name.lower() == "sources":
        sources_dir = p.parent

    if not sources_dir or not sources_dir.exists():
        return None

    with connect_db(resolved) as conn:
        cur = conn.cursor()
        effective_type = (doc_type or "annual_report").lower().strip()

        if effective_type in ("afs", "presentation", "sens"):
            existing = cur.execute("SELECT parent_report_sha256 FROM reports WHERE sha256 = ?", (report_sha256,)).fetchone()
            if existing and existing["parent_report_sha256"]:
                return existing["parent_report_sha256"]

            # Look for an IAR or Annual Report in sources_dir
            for cand_pdf in sources_dir.glob("*.pdf"):
                cand_name = cand_pdf.name
                row = cur.execute(
                    "SELECT sha256, questions_ledger, doc_type FROM reports WHERE (original_path LIKE ? OR filename = ?) AND sha256 != ?",
                    (f"%{cand_name}%", cand_name, report_sha256),
                ).fetchone()
                if row and row["doc_type"] in ("iar", "annual_report"):
                    parent_sha = row["sha256"]
                    cur.execute(
                        "UPDATE reports SET parent_report_sha256 = ? WHERE sha256 = ?",
                        (parent_sha, report_sha256),
                    )
                    # Sync questions ledger if empty
                    this_row = cur.execute("SELECT questions_ledger FROM reports WHERE sha256 = ?", (report_sha256,)).fetchone()
                    if this_row and not (this_row["questions_ledger"] or "").strip() and row["questions_ledger"]:
                        cur.execute(
                            "UPDATE reports SET questions_ledger = ? WHERE sha256 = ?",
                            (row["questions_ledger"], report_sha256),
                        )
                    conn.commit()
                    return parent_sha

        elif effective_type in ("iar", "annual_report"):
            # This is a primary report; check if any AFS, presentation, or SENS in sources_dir are unlinked
            cand_files = list(sources_dir.glob("*.pdf"))
            sens_sub = sources_dir / "sens"
            if sens_sub.exists():
                cand_files.extend(sens_sub.glob("*.pdf"))
            for cand_pdf in cand_files:
                cand_name = cand_pdf.name
                row = cur.execute(
                    "SELECT sha256, parent_report_sha256, doc_type, questions_ledger FROM reports WHERE (original_path LIKE ? OR filename = ?) AND sha256 != ?",
                    (f"%{cand_name}%", cand_name, report_sha256),
                ).fetchone()
                if row and not row["parent_report_sha256"] and row["doc_type"] in ("afs", "presentation", "sens"):
                    cur.execute(
                        "UPDATE reports SET parent_report_sha256 = ? WHERE sha256 = ?",
                        (report_sha256, row["sha256"]),
                    )
                    this_row = cur.execute("SELECT questions_ledger FROM reports WHERE sha256 = ?", (report_sha256,)).fetchone()
                    if this_row and this_row["questions_ledger"] and not (row["questions_ledger"] or "").strip():
                        cur.execute(
                            "UPDATE reports SET questions_ledger = ? WHERE sha256 = ?",
                            (this_row["questions_ledger"], row["sha256"]),
                        )
            conn.commit()

    return None


def auto_link_parent_report(sens_sha256: str, sens_path: Path | str, db_path: str | Path | None = None) -> str | None:
    """Backward compatibility alias for auto_link_companion_reports."""
    return auto_link_companion_reports(sens_sha256, sens_path, doc_type="sens", db_path=db_path)


def set_report_doc_type(sha256: str, doc_type: str, db_path: str | Path | None = None) -> None:
    """Updates the document classification for a report and synchronizes companion links."""
    resolved = resolve_db_path(db_path)
    now = datetime.now(timezone.utc).isoformat()
    norm_type = doc_type.lower().strip()
    with connect_db(resolved) as conn:
        conn.execute(
            "UPDATE reports SET doc_type = ?, updated_at = ? WHERE sha256 = ?",
            (norm_type, now, sha256),
        )
        row = conn.execute("SELECT original_path FROM reports WHERE sha256 = ?", (sha256,)).fetchone()
        if row and row["original_path"]:
            auto_link_companion_reports(sha256, row["original_path"], doc_type=norm_type, db_path=resolved)


def link_sens_report(
    sens_sha256: str,
    parent_sha256: str,
    doc_type: str = "sens",
    announcement_date: str | None = None,
    db_path: str | Path | None = None,
) -> bool:
    """Explicitly link a SENS announcement to a parent company report, copying questions ledger if empty."""
    resolved = resolve_db_path(db_path)
    with connect_db(resolved) as conn:
        parent_row = conn.execute("SELECT sha256, questions_ledger FROM reports WHERE sha256 = ?", (parent_sha256,)).fetchone()
        if not parent_row:
            return False
        sens_row = conn.execute("SELECT sha256, questions_ledger FROM reports WHERE sha256 = ?", (sens_sha256,)).fetchone()
        if not sens_row:
            return False

        updates = ["parent_report_sha256 = ?", "doc_type = ?"]
        params = [parent_sha256, doc_type]
        if announcement_date:
            updates.append("announcement_date = ?")
            params.append(announcement_date)

        # Seed questions ledger from parent if empty
        if not (sens_row["questions_ledger"] or "").strip() and (parent_row["questions_ledger"] or "").strip():
            updates.append("questions_ledger = ?")
            params.append(parent_row["questions_ledger"])

        params.append(sens_sha256)
        conn.execute(f"UPDATE reports SET {', '.join(updates)} WHERE sha256 = ?", params)
        conn.commit()
        return True


def get_linked_sens_reports(parent_sha256: str, db_path: str | Path | None = None) -> list[dict]:
    """Retrieve all SENS notices linked to a primary report, ordered chronologically."""
    resolved = resolve_db_path(db_path)
    if not resolved.exists():
        return []
    with connect_db(resolved) as conn:
        rows = conn.execute(
            """
            SELECT sha256, filename, original_path, physical_page_count,
                   doc_type, announcement_date, questions_ledger, updated_at
            FROM reports
            WHERE parent_report_sha256 = ?
            ORDER BY COALESCE(announcement_date, '9999-99-99') ASC, created_at ASC
            """,
            (parent_sha256,),
        ).fetchall()
        return [dict(r) for r in rows]


def get_parent_report(sens_sha256: str, db_path: str | Path | None = None) -> dict | None:
    """Retrieve parent report for a SENS announcement if linked."""
    resolved = resolve_db_path(db_path)
    if not resolved.exists():
        return None
    with connect_db(resolved) as conn:
        row = conn.execute(
            """
            SELECT p.*
            FROM reports c
            JOIN reports p ON c.parent_report_sha256 = p.sha256
            WHERE c.sha256 = ?
            """,
            (sens_sha256,),
        ).fetchone()
        return dict(row) if row else None


def _migrate_schema(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS app_state (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    cols = {row[1] for row in cur.execute("PRAGMA table_info(reports)").fetchall()}
    new_cols = [
        ("stage1_prompt", "TEXT"),
        ("stage1_response", "TEXT"),
        ("stage1_updated_at", "TEXT"),
        ("stage2_prompt", "TEXT"),
        ("stage2_response", "TEXT"),
        ("stage2_updated_at", "TEXT"),
        ("target_price_zar", "REAL"),
        ("reference_price_zar", "REAL"),
        ("recommendation", "TEXT"),
        ("upside_pct", "REAL"),
        ("dividend_yield_pct", "REAL"),
        ("tsr_pct", "REAL"),
        ("monitoring_triggers", "TEXT"),
        ("valuation_summary_json", "TEXT"),
        ("parent_report_sha256", "TEXT"),
        ("doc_type", "TEXT NOT NULL DEFAULT 'annual_report'"),
        ("announcement_date", "TEXT"),
        ("sens_updates_json", "TEXT"),
        ("stage2_baseline_response", "TEXT"),
        ("stage2_baseline_updated_at", "TEXT"),
    ]
    for col_name, col_type in new_cols:
        if col_name not in cols:
            cur.execute(f"ALTER TABLE reports ADD COLUMN {col_name} {col_type}")

    # Backfill valuation summary if missing
    rows = cur.execute(
        "SELECT sha256, stage2_response FROM reports WHERE stage2_response IS NOT NULL AND target_price_zar IS NULL"
    ).fetchall()
    for r in rows:
        summary = parse_valuation_summary(r["stage2_response"])
        if summary:
            cur.execute(
                """
                UPDATE reports SET
                    target_price_zar = ?,
                    reference_price_zar = ?,
                    recommendation = ?,
                    upside_pct = ?,
                    dividend_yield_pct = ?,
                    tsr_pct = ?,
                    monitoring_triggers = ?,
                    valuation_summary_json = ?
                WHERE sha256 = ?
                """,
                (
                    summary.get("target_price"),
                    summary.get("reference_price"),
                    summary.get("recommendation"),
                    summary.get("upside_pct"),
                    summary.get("dividend_yield_pct"),
                    summary.get("tsr_pct"),
                    summary.get("monitoring_triggers"),
                    json.dumps(summary, ensure_ascii=False),
                    r["sha256"],
                ),
            )
    conn.commit()


def connect_db(db_path: str | Path | None = None) -> sqlite3.Connection:
    path = resolve_db_path(db_path)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA_SQL)
    _migrate_schema(conn)
    return conn


def upsert_report(
    sha256: str,
    filename: str = "",
    original_path: str = "",
    byte_size: int = 0,
    physical_page_count: int = 1,
    report_map: dict | None = None,
    questions_ledger: str | None = None,
    parent_report_sha256: str | None = None,
    doc_type: str | None = None,
    announcement_date: str | None = None,
    db_path: str | Path | None = None,
) -> Path:
    now = datetime.now(timezone.utc).isoformat()
    map_json = json.dumps(report_map, ensure_ascii=False) if report_map is not None else None
    norm_orig_path = to_relative_project_path(original_path) if original_path else ""
    inferred_type, inferred_date = detect_doc_type_and_date(norm_orig_path or filename)
    effective_doc_type = doc_type or inferred_type
    effective_date = announcement_date or inferred_date

    with connect_db(db_path) as conn:
        existing = conn.execute("SELECT * FROM reports WHERE sha256 = ?", (sha256,)).fetchone()
        effective_parent = parent_report_sha256
        if existing is None:
            effective_ledger = (questions_ledger or "").strip()
            if effective_doc_type == "sens" and not effective_parent and original_path:
                effective_parent = auto_link_parent_report(sha256, original_path, db_path=db_path)

            if effective_parent and not effective_ledger:
                parent_row = conn.execute("SELECT questions_ledger FROM reports WHERE sha256 = ?", (effective_parent,)).fetchone()
                if parent_row and parent_row["questions_ledger"]:
                    effective_ledger = parent_row["questions_ledger"].strip()

            conn.execute(
                """
                INSERT INTO reports (
                    sha256, filename, original_path, byte_size, physical_page_count,
                    report_map_json, questions_ledger, parent_report_sha256,
                    doc_type, announcement_date, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    sha256,
                    filename or (report_map or {}).get("source_filename", "") or "report.pdf",
                    norm_orig_path,
                    byte_size,
                    physical_page_count or (report_map or {}).get("physical_page_count", 1),
                    map_json,
                    effective_ledger,
                    effective_parent,
                    effective_doc_type,
                    effective_date,
                    now,
                    now,
                ),
            )
        else:
            new_filename = filename or existing["filename"]
            new_orig = norm_orig_path or existing["original_path"]
            new_size = byte_size if byte_size > 0 else existing["byte_size"]
            new_pages = physical_page_count if physical_page_count > 1 else existing["physical_page_count"]
            new_map = map_json if map_json is not None else existing["report_map_json"]
            new_q = questions_ledger.strip() if questions_ledger is not None else existing["questions_ledger"]
            new_parent = effective_parent if effective_parent is not None else existing["parent_report_sha256"]
            new_type = doc_type if doc_type is not None else (existing["doc_type"] or effective_doc_type)
            new_date = effective_date if effective_date is not None else existing["announcement_date"]

            if new_type == "sens" and not new_parent and new_orig:
                new_parent = auto_link_parent_report(sha256, new_orig, db_path=db_path)

            conn.execute(
                """
                UPDATE reports
                   SET filename = ?,
                       original_path = ?,
                       byte_size = ?,
                       physical_page_count = ?,
                       report_map_json = ?,
                       questions_ledger = ?,
                       parent_report_sha256 = ?,
                       doc_type = ?,
                       announcement_date = ?,
                       updated_at = ?
                 WHERE sha256 = ?
                """,
                (new_filename, new_orig, new_size, new_pages, new_map, new_q, new_parent, new_type, new_date, now, sha256),
            )
    return resolve_db_path(db_path)


def get_report_map(sha256: str, db_path: str | Path | None = None) -> dict | None:
    path = resolve_db_path(db_path)
    if not path.exists():
        return None
    with connect_db(path) as conn:
        row = conn.execute("SELECT report_map_json FROM reports WHERE sha256 = ?", (sha256,)).fetchone()
        if row and row["report_map_json"]:
            try:
                return json.loads(row["report_map_json"])
            except ValueError:
                return None
    return None


def get_questions_ledger(sha256: str, db_path: str | Path | None = None) -> str:
    path = resolve_db_path(db_path)
    if not path.exists():
        return ""
    with connect_db(path) as conn:
        row = conn.execute("SELECT questions_ledger FROM reports WHERE sha256 = ?", (sha256,)).fetchone()
        if row and row["questions_ledger"]:
            return row["questions_ledger"].strip()
    return ""


def next_section_number(report_sha256: str, db_path: str | Path | None = None) -> int:
    with connect_db(db_path) as conn:
        row = conn.execute(
            "SELECT COALESCE(MAX(section_number), 0) AS max_num FROM sections WHERE report_sha256 = ?",
            (report_sha256,),
        ).fetchone()
        return int(row["max_num"]) + 1


def insert_section(
    *,
    package_id: str,
    report_sha256: str,
    section_number: int,
    section_id: str,
    name: str,
    heading: str,
    subheading: str | None,
    analyst_question: str | None,
    selected_text: str,
    selections: list[dict],
    stored_questions: str | None,
    prompt: str,
    manifest: dict,
    llm_response: str | None = None,
    created_at: str | None = None,
    db_path: str | Path | None = None,
) -> SavedSection:
    now = created_at or datetime.now(timezone.utc).isoformat()
    resolved = resolve_db_path(db_path)
    src = manifest.get("source") or {}
    upsert_report(
        sha256=report_sha256,
        filename=src.get("filename", ""),
        original_path=src.get("original_path", ""),
        byte_size=int(src.get("byte_size", 0) or 0),
        physical_page_count=int(src.get("physical_page_count", 1) or 1),
        report_map=manifest.get("document_map"),
        db_path=resolved,
    )
    with connect_db(resolved) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO sections (
                package_id, report_sha256, section_number, section_id,
                heading, subheading, analyst_question, selected_text,
                selections_json, stored_questions_snapshot, prompt,
                llm_response, manifest_json, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                package_id,
                report_sha256,
                section_number,
                section_id,
                heading,
                subheading,
                analyst_question,
                selected_text,
                json.dumps(selections, ensure_ascii=False),
                stored_questions,
                prompt,
                llm_response,
                json.dumps(manifest, ensure_ascii=False),
                now,
                now,
            ),
        )
    return SavedSection(
        package_id=package_id,
        report_sha256=report_sha256,
        section_number=section_number,
        section_id=section_id,
        name=name,
        heading=heading,
        subheading=subheading,
        analyst_question=analyst_question,
        selected_text=selected_text,
        selections=selections,
        stored_questions=stored_questions,
        prompt=prompt,
        llm_response=llm_response,
        manifest=manifest,
        created_at=now,
        db_path=resolved,
    )


def _row_to_saved_section(row: sqlite3.Row, db_path: Path) -> SavedSection:
    manifest = json.loads(row["manifest_json"])
    selections = json.loads(row["selections_json"])
    name = manifest.get("section_name") or f"{row['section_number']:02d}-{row['section_id']}"
    return SavedSection(
        package_id=row["package_id"],
        report_sha256=row["report_sha256"],
        section_number=row["section_number"],
        section_id=row["section_id"],
        name=name,
        heading=row["heading"],
        subheading=row["subheading"],
        analyst_question=row["analyst_question"],
        selected_text=row["selected_text"],
        selections=selections,
        stored_questions=row["stored_questions_snapshot"],
        prompt=row["prompt"],
        llm_response=row["llm_response"],
        manifest=manifest,
        created_at=row["created_at"],
        db_path=db_path,
    )


def list_sections(report_sha256: str, db_path: str | Path | None = None) -> list[SavedSection]:
    resolved = resolve_db_path(db_path)
    if not resolved.exists():
        return []
    with connect_db(resolved) as conn:
        rows = conn.execute(
            "SELECT * FROM sections WHERE report_sha256 = ? ORDER BY section_number ASC, id ASC",
            (report_sha256,),
        ).fetchall()
        return [_row_to_saved_section(r, resolved) for r in rows]


def get_section(package_id: str, db_path: str | Path | None = None) -> SavedSection | None:
    resolved = resolve_db_path(db_path)
    if not resolved.exists():
        return None
    with connect_db(resolved) as conn:
        row = conn.execute("SELECT * FROM sections WHERE package_id = ?", (package_id,)).fetchone()
        return _row_to_saved_section(row, resolved) if row else None


def extract_questions_ledger_from_response(response_text: str) -> str | None:
    """Extract Section 4 (Updated Open Questions Ledger) from an LLM Markdown response if present."""
    text = (response_text or "").strip()
    if not text:
        return None
    sec4_match = re.search(
        r"(?:^|\n)#{1,4}\s*(?:4\.?\s*)?Updated Open Questions Ledger[^\n]*\n(.*?)(?=\n#{1,4}\s*(?:5\.?\s*)?(?:Baseline Forecast|Next Section)|\Z)",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if not sec4_match:
        return None
    block = sec4_match.group(1).strip()
    fence_match = re.search(r"```(?:markdown|md)?\s*\n(.*?)```", block, re.IGNORECASE | re.DOTALL)
    if fence_match:
        extracted = fence_match.group(1).strip()
    else:
        extracted = block
    return extracted or None


def save_section_llm_response(
    package_id: str,
    llm_response: str,
    update_ledger: bool = True,
    response_time_seconds: float | None = None,
    cost_usd: float | None = None,
    tokens: dict | None = None,
    model: str | None = None,
    db_path: str | Path | None = None,
) -> tuple[SavedSection | None, str | None]:
    """Save the LLM response onto a section row and optionally auto-extract & update the report's questions ledger."""
    resolved = resolve_db_path(db_path)
    cleaned_resp = (llm_response or "").strip()
    now = datetime.now(timezone.utc).isoformat()
    extracted_ledger = extract_questions_ledger_from_response(cleaned_resp) if update_ledger else None
    with connect_db(resolved) as conn:
        row = conn.execute("SELECT * FROM sections WHERE package_id = ?", (package_id,)).fetchone()
        if not row:
            return None, None
        manifest = json.loads(row["manifest_json"])
        review = manifest.setdefault("review", {})
        review["model_brief"] = "recorded" if cleaned_resp else "not_run"
        if response_time_seconds is not None:
            review["response_time_seconds"] = round(float(response_time_seconds), 2)
        if cost_usd is not None:
            review["cost_usd"] = round(float(cost_usd), 6)
        if model:
            review["model"] = model
        if tokens:
            review["tokens"] = tokens
        conn.execute(
            "UPDATE sections SET llm_response = ?, manifest_json = ?, updated_at = ? WHERE package_id = ?",
            (cleaned_resp or None, json.dumps(manifest, ensure_ascii=False), now, package_id),
        )

        if extracted_ledger:
            conn.execute(
                "UPDATE reports SET questions_ledger = ?, updated_at = ? WHERE sha256 = ?",
                (extracted_ledger, now, row["report_sha256"]),
            )
            # Sync questions ledger across suite: to parent & siblings, or from parent to children
            rep = conn.execute("SELECT parent_report_sha256 FROM reports WHERE sha256 = ?", (row["report_sha256"],)).fetchone()
            if rep and rep["parent_report_sha256"]:
                parent_sha = rep["parent_report_sha256"]
                conn.execute(
                    "UPDATE reports SET questions_ledger = ?, updated_at = ? WHERE sha256 = ?",
                    (extracted_ledger, now, parent_sha),
                )
                conn.execute(
                    "UPDATE reports SET questions_ledger = ?, updated_at = ? WHERE parent_report_sha256 = ? AND sha256 != ?",
                    (extracted_ledger, now, parent_sha, row["report_sha256"]),
                )
            else:
                conn.execute(
                    "UPDATE reports SET questions_ledger = ?, updated_at = ? WHERE parent_report_sha256 = ?",
                    (extracted_ledger, now, row["report_sha256"]),
                )
        updated_row = conn.execute("SELECT * FROM sections WHERE package_id = ?", (package_id,)).fetchone()
        return _row_to_saved_section(updated_row, resolved), extracted_ledger


def clear_section_llm_response(package_id: str, db_path: str | Path | None = None) -> SavedSection | None:
    """Clear the stored LLM response and review metadata on a section row."""
    resolved = resolve_db_path(db_path)
    now = datetime.now(timezone.utc).isoformat()
    with connect_db(resolved) as conn:
        row = conn.execute("SELECT * FROM sections WHERE package_id = ?", (package_id,)).fetchone()
        if not row:
            return None
        manifest = json.loads(row["manifest_json"])
        manifest["review"] = {"model_brief": "not_run"}
        conn.execute(
            "UPDATE sections SET llm_response = NULL, manifest_json = ?, updated_at = ? WHERE package_id = ?",
            (json.dumps(manifest, ensure_ascii=False), now, package_id),
        )
        updated_row = conn.execute("SELECT * FROM sections WHERE package_id = ?", (package_id,)).fetchone()
        return _row_to_saved_section(updated_row, resolved)


def delete_section(package_id: str, db_path: str | Path | None = None) -> bool:
    """Delete a section row from the database."""
    resolved = resolve_db_path(db_path)
    with connect_db(resolved) as conn:
        cur = conn.execute("DELETE FROM sections WHERE package_id = ?", (package_id,))
        return cur.rowcount > 0


def save_stage1_report(
    report_sha256: str,
    prompt: str | None = None,
    response: str | None = None,
    db_path: str | Path | None = None,
) -> bool:
    """Save Stage 1 Forensic Audit prompt and/or response on a report row."""
    resolved = resolve_db_path(db_path)
    now = datetime.now(timezone.utc).isoformat()
    with connect_db(resolved) as conn:
        row = conn.execute("SELECT * FROM reports WHERE sha256 = ?", (report_sha256,)).fetchone()
        if not row:
            return False
        updates = ["stage1_updated_at = ?", "updated_at = ?"]
        params = [now, now]
        if prompt is not None:
            updates.append("stage1_prompt = ?")
            params.append(prompt)
        if response is not None:
            updates.append("stage1_response = ?")
            params.append(response)
        params.append(report_sha256)
        conn.execute(f"UPDATE reports SET {', '.join(updates)} WHERE sha256 = ?", params)
        return True


def get_stage1_report(report_sha256: str, db_path: str | Path | None = None) -> dict | None:
    """Retrieve Stage 1 Forensic Audit data for a report."""
    resolved = resolve_db_path(db_path)
    with connect_db(resolved) as conn:
        row = conn.execute(
            "SELECT sha256, filename, stage1_prompt, stage1_response, stage1_updated_at FROM reports WHERE sha256 = ?",
            (report_sha256,),
        ).fetchone()
        if not row:
            return None
        return dict(row)


def save_stage2_report(
    report_sha256: str,
    prompt: str | None = None,
    response: str | None = None,
    sens_updates: list[dict] | None = None,
    db_path: str | Path | None = None,
) -> bool:
    """Save Stage 2 Institutional Valuation prompt and/or response on a report row."""
    resolved = resolve_db_path(db_path)
    now = datetime.now(timezone.utc).isoformat()
    with connect_db(resolved) as conn:
        row = conn.execute("SELECT * FROM reports WHERE sha256 = ?", (report_sha256,)).fetchone()
        if not row:
            return False
        updates = ["stage2_updated_at = ?", "updated_at = ?"]
        params: list[Any] = [now, now]
        if prompt is not None:
            updates.append("stage2_prompt = ?")
            params.append(prompt)
        if sens_updates is not None:
            updates.append("sens_updates_json = ?")
            params.append(json.dumps(sens_updates, ensure_ascii=False))
        if response is not None:
            # Preserve original baseline if this is the first subsequent update
            cols = {col[1] for col in conn.execute("PRAGMA table_info(reports)").fetchall()}
            if "stage2_baseline_response" in cols:
                current_baseline = row["stage2_baseline_response"] if "stage2_baseline_response" in row.keys() else None
                if row["stage2_response"] and not current_baseline and row["stage2_response"].strip() != response.strip():
                    updates.extend(["stage2_baseline_response = ?", "stage2_baseline_updated_at = ?"])
                    params.extend([row["stage2_response"], row["stage2_updated_at"] or now])

            updates.append("stage2_response = ?")
            params.append(response)
            summary = parse_valuation_summary(response)
            if summary:
                if row:
                    det_ticker, _, detected_sec = detect_company_meta(row["original_path"] or row["filename"])
                    if not summary.get("sector") and detected_sec:
                        summary["sector"] = detected_sec
                    if summary.get("sector"):
                        if not summary.get("jse_sector_code"):
                            summary["jse_sector_code"] = get_jse_sector_code(summary["sector"], ticker=det_ticker)
                        if not summary.get("jse_sector_name"):
                            summary["jse_sector_name"] = get_jse_sector_name(summary["sector"], ticker=det_ticker)
                updates.extend([
                    "target_price_zar = ?",
                    "reference_price_zar = ?",
                    "recommendation = ?",
                    "upside_pct = ?",
                    "dividend_yield_pct = ?",
                    "tsr_pct = ?",
                    "monitoring_triggers = ?",
                    "valuation_summary_json = ?",
                ])
                params.extend([
                    summary.get("target_price"),
                    summary.get("reference_price"),
                    summary.get("recommendation"),
                    summary.get("upside_pct"),
                    summary.get("dividend_yield_pct"),
                    summary.get("tsr_pct"),
                    summary.get("monitoring_triggers"),
                    json.dumps(summary, ensure_ascii=False),
                ])
        params.append(report_sha256)
        conn.execute(f"UPDATE reports SET {', '.join(updates)} WHERE sha256 = ?", params)
        return True


def get_stage2_report(report_sha256: str, db_path: str | Path | None = None) -> dict | None:
    """Retrieve Stage 2 Institutional Valuation data for a report."""
    resolved = resolve_db_path(db_path)
    with connect_db(resolved) as conn:
        row = conn.execute(
            """
            SELECT
                sha256, filename, stage2_prompt, stage2_response, stage2_updated_at,
                target_price_zar, reference_price_zar, recommendation, upside_pct,
                dividend_yield_pct, tsr_pct, monitoring_triggers, valuation_summary_json,
                sens_updates_json, stage2_baseline_response, stage2_baseline_updated_at
            FROM reports WHERE sha256 = ?
            """,
            (report_sha256,),
        ).fetchone()
        if not row:
            return None
        return dict(row)


def get_analyzed_stocks(db_path: str | Path | None = None) -> list[dict]:
    """Retrieve all reports with their Stage 1 & Stage 2 valuation status, target prices, and monitoring triggers."""
    resolved = resolve_db_path(db_path)
    if not resolved.exists():
        return []
    with connect_db(resolved) as conn:
        rows = conn.execute(
            """
            SELECT
                r.sha256,
                r.filename,
                r.original_path,
                r.physical_page_count,
                r.target_price_zar,
                r.reference_price_zar,
                r.recommendation,
                r.upside_pct,
                r.dividend_yield_pct,
                r.tsr_pct,
                r.monitoring_triggers,
                r.stage1_updated_at,
                r.stage2_updated_at,
                r.created_at,
                r.updated_at,
                length(r.stage1_response) AS s1_len,
                length(r.stage2_response) AS s2_len,
                COUNT(s.id) AS section_count,
                (SELECT COUNT(*) FROM reports child WHERE child.parent_report_sha256 = r.sha256) AS sens_count
            FROM reports r
            LEFT JOIN sections s ON s.report_sha256 = r.sha256
            WHERE r.parent_report_sha256 IS NULL
            GROUP BY r.sha256
            ORDER BY
                CASE WHEN r.stage2_response IS NOT NULL THEN 1 ELSE 2 END ASC,
                COALESCE(r.stage2_updated_at, r.updated_at) DESC
            """
        ).fetchall()

        cur = conn.cursor()
        quotes_map: dict[str, dict] = {}
        has_quotes_table = cur.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='market_quotes'"
        ).fetchone()
        if has_quotes_table:
            q_rows = cur.execute("SELECT ticker, price_zar, prev_close_zar, change_pct, updated_at FROM market_quotes").fetchall()
            for qr in q_rows:
                quotes_map[qr["ticker"].upper()] = {
                    "price_zar": qr["price_zar"],
                    "prev_close_zar": qr["prev_close_zar"],
                    "change_pct": qr["change_pct"],
                    "updated_at": qr["updated_at"],
                }

        results = []
        for r in rows:
            ticker, company_name, sector = detect_company_meta(r["original_path"] or r["filename"])
            ticker = ticker or "UNCLASSIFIED"
            company_name = company_name or "Unclassified Document"
            sector = sector or "unassigned"
            jse_code = get_jse_sector_code(sector, ticker=ticker) if sector in SECTORS else ""
            jse_name = get_jse_sector_name(sector, ticker=ticker) if sector in SECTORS else ""

            quote = quotes_map.get(ticker.upper())
            live_price = quote["price_zar"] if quote else None
            live_change = quote["change_pct"] if quote else None
            quote_updated = quote["updated_at"] if quote else None
            tp_val = r["target_price_zar"]
            live_upside = (
                round(((tp_val - live_price) / live_price) * 100.0, 1)
                if (tp_val is not None and live_price and live_price > 0)
                else None
            )

            results.append({
                "sha256": r["sha256"],
                "filename": r["filename"],
                "original_path": r["original_path"],
                "ticker": ticker,
                "company_name": company_name,
                "sector": sector,
                "jse_sector_code": jse_code,
                "jse_sector_name": jse_name,
                "target_price_zar": tp_val,
                "reference_price_zar": r["reference_price_zar"],
                "live_price_zar": live_price,
                "live_price_change_pct": live_change,
                "live_price_updated_at": quote_updated,
                "live_upside_pct": live_upside,
                "recommendation": r["recommendation"] or ("ANALYZED" if r["s2_len"] else "IN PROGRESS"),
                "upside_pct": r["upside_pct"],
                "dividend_yield_pct": r["dividend_yield_pct"],
                "tsr_pct": r["tsr_pct"],
                "monitoring_triggers": r["monitoring_triggers"] or "",
                "has_stage1": bool(r["s1_len"] and r["s1_len"] > 0),
                "has_stage2": bool(r["s2_len"] and r["s2_len"] > 0),
                "stage1_length": r["s1_len"] or 0,
                "stage2_length": r["s2_len"] or 0,
                "section_count": r["section_count"] or 0,
                "sens_count": r["sens_count"] or 0,
                "stage1_updated_at": r["stage1_updated_at"],
                "stage2_updated_at": r["stage2_updated_at"],
                "updated_at": r["updated_at"],
            })
        return results


def get_app_setting(key: str, default: str | None = None, db_path: str | Path | None = None) -> str | None:
    """Retrieve a persistent setting from the database."""
    try:
        with connect_db(db_path) as conn:
            row = conn.execute("SELECT value FROM app_state WHERE key = ?", (key,)).fetchone()
            if row and row["value"]:
                return str(row["value"])
    except Exception:
        pass
    return default


def set_app_setting(key: str, value: str, db_path: str | Path | None = None) -> None:
    """Store a persistent setting in the database."""
    now = datetime.now(timezone.utc).isoformat()
    try:
        with connect_db(db_path) as conn:
            conn.execute(
                """
                INSERT INTO app_state (key, value, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = excluded.updated_at
                """,
                (key, str(value), now),
            )
            conn.commit()
    except Exception:
        pass


def save_last_opened_dir(folder: Path | str, db_path: str | Path | None = None) -> None:
    """Save the last opened directory to the database, normalized as relative path if inside ROOT."""
    folder_path = Path(folder).resolve()
    try:
        rel = folder_path.relative_to(ROOT)
        stored_val = str(rel).replace("\\", "/")
    except ValueError:
        stored_val = str(folder_path)
    set_app_setting("last_opened_dir", stored_val, db_path=db_path)


def load_last_opened_dir(db_path: str | Path | None = None) -> Path:
    """Load the last opened directory from the database with fallback to latest report or companies root."""
    val = get_app_setting("last_opened_dir", db_path=db_path)
    if val:
        candidate = (ROOT / val).resolve()
        if candidate.is_dir():
            return candidate
        abs_cand = Path(val)
        if abs_cand.is_dir():
            return abs_cand

    try:
        with connect_db(db_path) as conn:
            row = conn.execute(
                "SELECT original_path, filename FROM reports ORDER BY updated_at DESC LIMIT 1"
            ).fetchone()
            if row:
                if row["original_path"]:
                    orig = Path(row["original_path"])
                    if orig.is_dir():
                        return orig
                    if orig.parent.is_dir():
                        return orig.parent
                if row["filename"]:
                    matches = list((ROOT / "companies").glob(f"**/{row['filename']}"))
                    if matches and matches[0].parent.is_dir():
                        return matches[0].parent
    except Exception:
        pass

    return (ROOT / "companies").resolve()


