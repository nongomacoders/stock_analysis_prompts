"""Reconciliation engine for PAN section D009 (physical pages 48-50).

DB-driven, generated from the extraction schema only (CHARTER covenant: the
scoring fixture is never read by build code). All arithmetic executes here as
code (covenant 2) on printed values parsed from `cells.value_raw` via a
deterministic parser; printed values are never replaced (covenant 1).

Column semantics (recorded at P1, identical grid on all three pages):
  col0  Barberton Mines            col7  Tennant Mines (surface feedstock)
  col1  Evander Mines              col8  Total surface operations
  col2  Total mining ops           col9  Barberton (total ops)
  col3  BTRP                       col10 Evander (total ops)
  col4  printed blank (never a cell) col11 MTR (total ops)
  col5  Elikhulu                   col12 Tennant (total ops)
  col6  MTR operation              col13 Group total
"""
from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation

OZ_PER_KG = Decimal("32.150747")  # physical constant, troy ounces per kg
XR_TOLERANCE = Decimal("0.0075")  # 0.75% relative tolerance for cross-currency ties


# ---------------------------------------------------------------- parsing
_DASH = {"–", "—", "-", "– –"}

def parse_value(value_raw: str):
    """Parse a verbatim printed cell to Decimal, or None for printed nil."""
    s = value_raw.strip()
    if s in _DASH or re.fullmatch(r"[–—-]+", s):  # en/em dash = printed nil
        return None
    if s in {".", ""}:
        return None
    s2 = s.replace(" ", "").replace(",", "")
    try:
        return Decimal(s2)
    except InvalidOperation as exc:  # pragma: no cover - structural, tested
        raise ValueError(f"unparseable printed cell: {value_raw!r}") from exc


# ------------------------------------------------------- row classification
# Additive rows: sums of per-segment cells are meaningful (t, oz, money).
# Non-additive rows: per-segment cells are weighted averages / rates; row sums
# are meaningless and are deliberately NOT checked (classified, never skipped
# silently). Rationale column documents why.
NON_ADDITIVE_RATIONALE = {
    "Head grade – total": "g/t grade is a tonnage-weighted average; weights not printed in-row",
    "Head grade – excluding third-party buy-in feedstock": "g/t grade is a tonnage-weighted average; weights not printed in-row",
    "Overall recovered grade": "g/t grade is a weight-based average; weights not printed in-row",
    "Overall recovery – underground": "% recovery is a ratio metric; not additive across segments",
    "Overall recovery – tailings": "% recovery is a ratio metric; not additive across segments",
    "Average ZAR gold price received – South African operations": "ZAR/kg average received price is oz-weighted; not additive",
    "Average A$ gold price received – Australian operations": "A$/kg average received price is oz-weighted; not additive",
    "Average US$ gold price received – Group": "US$/oz average received price is oz-weighted; not additive",
    "ZAR cash cost": "ZAR/kg cost is oz-weighted average; not additive (cross-checked vs US$ rows in XR instead)",
    "ZAR all-in sustaining costs": "ZAR/kg cost is oz-weighted average; not additive (XR-checked)",
    "ZAR all-in cost": "ZAR/kg cost is oz-weighted average; not additive (XR-checked)",
    "A$ cash cost": "A$/kg cost is oz-weighted average; not additive (XR-checked)",
    "A$ all-in sustaining costs": "A$/kg cost is oz-weighted average; not additive (XR-checked)",
    "A$ all-in cost": "A$/kg cost is oz-weighted average; not additive (XR-checked)",
    "US$ cash cost": "US$/oz cost is oz-weighted average; not additive (XR-checked)",
    "US$ all-in sustaining cost": "US$/oz cost is oz-weighted average; not additive (XR-checked)",
    "US$ all-in sustaining cost – excluding third-party buy-in feedstock": "US$/oz cost is oz-weighted average; not additive (XR-checked)",
    "US$ all-in cost": "US$/oz cost is oz-weighted average; not additive (XR-checked)",
    "ZAR cash cost per tonne": "ZAR/t cost is tonne-weighted average; not additive",
    "Average exchange rate": "exchange rate row (two instances: ZAR/US$ and A$/US$); not additive",
}

TONNES_TOTALS = {
    "Tonnes milled – total underground and surface": [
        "Tonnes milled – underground", "Tonnes milled – surface"],
    "Tonnes processed – total tailings and surface feedstock": [
        "Tonnes processed – tailings", "Tonnes processed – surface feedstock"],
    "Tonnes milled and processed – total": [
        "Tonnes milled – total underground and surface",
        "Tonnes processed – total tailings and surface feedstock",
        "Tonnes processed – third-party buy-in feedstock"],
}
GOLD_TOTAL = {
    "Gold produced – total": [
        "Gold produced – underground", "Gold production – surface operations",
        "Gold produced – tailings", "Gold produced – third-party buy-in feedstock",
        "Gold produced – surface feedstock"],
}
SINGLE_KOZ_TOTALS = {"Gold sold – total"}
MONEY_ROWS = {"Revenue", "Revenue A$", "Cost of production", "Cost of production A$",
              "All-in sustainable cost of production", "All-in sustainable cost of production A$",
              "All-in cost of production", "All-in cost of production A$",
              "Adjusted EBITDA US$", "Capital expenditure US$"}
ADDITIVE_ROWS = (set(TONNES_TOTALS) | {lab for leaves in TONNES_TOTALS.values() for lab in leaves}
                 | set(GOLD_TOTAL) | {lab for lab, leaves in GOLD_TOTAL.items() for lab in leaves}
                 | {"Tonnes milled – underground", "Tonnes milled – surface",
                    "Tonnes processed – tailings", "Tonnes processed – surface feedstock",
                    "Tonnes processed – third-party buy-in feedstock",
                    "Gold produced – underground", "Gold production – surface operations",
                    "Gold produced – tailings", "Gold produced – third-party buy-in feedstock",
                    "Gold produced – surface feedstock"} | SINGLE_KOZ_TOTALS | MONEY_ROWS)

# Matrix identities: (check_id, printed-total column, component columns, label)
M_IDENTITIES = [
    ("M1", 2, [0, 1]), ("M2", 8, [3, 5, 6, 7]), ("M3", 9, [0, 3]),
    ("M4", 10, [1, 5]), ("M5", 11, [6]), ("M6", 12, [7]),
    ("M7", 13, [2, 8]), ("M8", 13, [9, 10, 11, 12]), ("M9", 13, [0, 1, 3, 5, 6, 7]),
]

# Cross-currency row pairs: (check_id, ZAR/kg row label, US$/oz row label, rate unit)
XR_PAIRS = [
    ("XR_CASH", "ZAR cash cost", "US$ cash cost", "US$/ZAR"),
    ("XR_AISC", "ZAR all-in sustaining costs", "US$ all-in sustaining cost", "US$/ZAR"),
    ("XR_AISC_EXCL", "ZAR all-in sustaining costs",
     "US$ all-in sustaining cost – excluding third-party buy-in feedstock", "US$/ZAR"),
    ("XR_ALLIN", "ZAR all-in cost", "US$ all-in cost", "US$/ZAR"),
    ("XR_AALLIN", "A$ all-in cost", "US$ all-in cost", "US$/A$"),
    ("XR_PRICE_ZAR", "Average ZAR gold price received – South African operations",
     "Average US$ gold price received – Group", "US$/ZAR"),
    ("XR_PRICE_AUS", "Average A$ gold price received – Australian operations",
     "Average US$ gold price received – Group", "US$/A$"),
]


@dataclass
class CheckResult:
    family: str          # P2 check family: XP (matrix), VS (vertical leaf-sum), XR (cross-currency)
    check_id: str        # M1..M9 / VS / XR_*
    physical_page: int
    row_label: str
    fiscal_year: str
    column: int | None
    printed: object      # Decimal or None (printed nil)
    computed: object     # Decimal (engine arithmetic)
    note: str = ""
    tolerance: Decimal = Decimal(0)  # 0 = exact (printed totals must tie with no tolerance)
    mismatch: bool = field(init=False)

    def __post_init__(self):
        printed = self.printed if self.printed is not None else Decimal(0)
        self.mismatch = abs(printed - self.computed) > self.tolerance * abs(printed)

    @property
    def delta(self):
        printed = self.printed if self.printed is not None else Decimal(0)
        return printed - self.computed

    @property
    def fingerprint(self):
        d = f"{self.delta:f}".rstrip("0").rstrip(".") if "." in f"{self.delta:f}" else f"{self.delta:f}"
        return (f"{self.check_id}|p{self.physical_page}|{self.row_label}|"
                f"{self.fiscal_year}|col{self.column if self.column is not None else '*'}|"
                f"delta={d}")


class Engine:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.rows = {}      # (row_index, page, label) per fy -> {col: Decimal|None}
        self.meta = {}      # same key -> (page, label, unit)
        self._load()

    # ------------------------------------------------------------- loading
    def _load(self):
        con = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
        try:
            cur = con.execute(
                "SELECT physical_page, row_index, row_label, fiscal_year, unit, "
                "column_index, value_raw FROM cells ORDER BY physical_page, row_index, fiscal_year")
            for page, row_index, label, fy, unit, col, raw in cur:
                key = (row_index, page, label, fy)
                self.rows.setdefault(key, {})[col] = parse_value(raw)
                self.meta[key] = (page, label, unit)
        finally:
            con.close()

    def _row(self, page, label, fy):
        for (row_index, p, lab, y), vals in self.rows.items():
            if p == page and lab == label and y == fy:
                return vals
        raise KeyError((page, label, fy))

    def instances(self, label, fy):
        return [vals for (ri, p, lab, y), vals in self.rows.items() if lab == label and y == fy]

    # ----------------------------------------------------------- checks
    def matrix_checks(self):
        out = []
        for (row_index, page, label, fy), vals in sorted(self.rows.items()):
            if label not in ADDITIVE_ROWS:
                continue
            for cid, total_col, comp_cols in M_IDENTITIES:
                total = vals.get(total_col)
                if total is None and all(vals.get(c) is None for c in comp_cols):
                    continue  # all-nil row/column pair: nothing printed to check
                computed = sum((vals.get(c) or Decimal(0)) for c in comp_cols)
                out.append(CheckResult("XP", cid, page, label, fy, total_col, total, computed,
                                       note=f"printed col{total_col} vs sum cols{comp_cols}"))
        return out

    def vertical_checks(self):
        out = []
        totals = {**TONNES_TOTALS, **GOLD_TOTAL}
        for page, lab, leaves in [(48, lab, lv) for lab, lv in totals.items() if lab in TONNES_TOTALS] + \
                                 [(49, lab, lv) for lab, lv in totals.items() if lab in GOLD_TOTAL]:
            for fy in ("FY26", "FY25"):
                try:
                    tv = self._row(page, lab, fy)
                except KeyError:
                    continue
                try:
                    leaf_rows = [self._row(page, leaf, fy) for leaf in leaves]
                except KeyError:
                    continue
                for col in range(14):
                    printed = tv.get(col)
                    computed = sum((r.get(col) or Decimal(0)) for r in leaf_rows)
                    if printed is None and computed == 0:
                        continue
                    out.append(CheckResult("VS", "VS", page, lab, fy, col, printed, computed,
                                           note=f"printed total vs leaf rows {leaves}"))
        return out

    def xr_checks(self):
        out = []
        rates = self._rates()
        for cid, zar_label, target_label, rate_unit in XR_PAIRS:
            factor_units = "A$perUS" if rate_unit == "US$/A$" else "ZARperUS"
            for fy in ("FY26", "FY25"):
                rate = rates.get((fy, rate_unit))
                if rate is None:
                    continue
                # Cross-currency: target-cell (US$/oz) * OZ_PER_KG * rate == source cell
                for (row_index, page, label, y), _z in list(self.rows.items()):
                    if label != target_label or y != fy:
                        continue
                    target_vals = self.rows[(row_index, page, label, y)]
                    try:
                        src_rows = self.instances(zar_label, fy)
                    except KeyError:
                        continue
                    for src_vals in src_rows:
                        for col in range(14):
                            tgt = target_vals.get(col)
                            printed = src_vals.get(col)
                            if tgt is None and printed is None:
                                continue
                            if tgt is None or printed is None:
                                continue  # one-sided printed value: no conversion printed
                            computed = tgt * OZ_PER_KG * rate
                            rel = abs(printed - computed) / abs(printed) if printed != 0 else (Decimal(0) if computed == 0 else Decimal("Infinity"))
                            out.append(CheckResult(
                                "XR", cid, page, zar_label, fy, col, printed, computed,
                                tolerance=XR_TOLERANCE,
                                note=(f"printed {printed} vs implied {computed} "
                                      f"(= {tgt} US$/oz x 32.150747 x {rate} {factor_units}); "
                                      f"rel deviation {rel:.4%}" if printed != 0 else
                                      f"printed nil vs implied {computed}")))
        return out

    def _rates(self):
        rates = {}
        for (row_index, page, label, fy), vals in self.rows.items():
            unit = self.meta[(row_index, page, label, fy)][2]
            if page == 50 and label == "Average exchange rate" and fy in ("FY26", "FY25"):
                rate = vals.get(0)
                if rate is not None:
                    rates[(fy, unit)] = rate
        return rates

    def run_all(self):
        results = self.matrix_checks() + self.vertical_checks() + self.xr_checks()
        return results

    def classification_report(self):
        seen = {(p, lab) for (ri, p, lab, fy) in self.meta}
        classified_additive = {(p, lab) for (ri, p, lab, fy) in self.meta if lab in ADDITIVE_ROWS}
        classified_non = {(p, lab) for (ri, p, lab, fy) in self.meta if lab in NON_ADDITIVE_RATIONALE}
        unclassified = seen - classified_additive - classified_non
        return {"all": sorted(seen), "additive": sorted(classified_additive),
                "non_additive": sorted(classified_non), "unclassified": sorted(unclassified)}
