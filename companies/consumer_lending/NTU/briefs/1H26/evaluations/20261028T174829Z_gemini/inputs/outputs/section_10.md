## Section 1 — Key facts and figures

**Instrument:** Interest-bearing liabilities and bank overdrafts, Rm, at 31 Mar 2026 (unaudited), 31 Mar 2025 (unaudited, first-time comparative), 30 Sep 2025 (audited). Note 2, pp. 14–15.

| Item | 31 Mar 2026 | 31 Mar 2025 | 30 Sep 2025 |
|---|---|---|---|
| Notes | 822 | 929 | 802 |
| Loans | 2,921 | 2,478 | 2,641 |
| Bank overdrafts | 273 | 457 | 364 |
| **Total interest-bearing liabilities** | **4,016** | **3,864** | **3,807** |
| Senior debt | 3,547 | 3,182 | 3,293 |
| Subordinated debt | 196 | 225 | 150 |
| Payable within 12 months | 1,396 | 1,039 | 1,237 |
| Payable thereafter | 2,620 | 2,825 | 2,570 |
| Total undrawn overdraft facilities | 475 | 43 | 136 |

- Arithmetic checks: 822+2,921+273 = 4,016 ✓; 3,547+196+273 = 4,016 ✓; 1,396+2,620 = 4,016 ✓. Loan sub-lines (p.15): 1,738+690+46+150+297 = 2,921 ✓; Notes 671+151+0 = 822 ✓.
- **Material conflict with stored questions:** the captured note shows bank overdrafts of **R273m** at 31 Mar 2026, not R2,273m as assumed in Q-8612694a3a674266 / Q-b6d6eda13d854fdf. The overdraft *fell* R91m vs 30 Sep 2025 (273−364 = −91), consistent with the cash-flow "net overdraft movement −R91m" cited in Q-b6d6eda13d854fdf. The R2,273m premise appears to be a misread (possibly 2,273 = total liabilities elsewhere, or a digit transposition); it is not supported here.
- Senior debt rose R254m vs Sep-25 (3,547−3,293), driven mainly by Senior amortising (+308: 1,738−1,430) partly offset by Revolving Facility (−74: 297−371). Subordinated rose R46m (new 03/10/2025 amortising tranche).
- Maturity: 34.8% (1,396/4,016) due within 12 months; weighted to thereafter.
- Undrawn overdraft facilities jumped to R475m (from R136m Sep-25, R43m Mar-25) — more headroom, not less.

## Section 2 — Footnotes, qualifications and reconciliations

- **Pledge/security (p.15 *):** purchased book debts, trade and other receivables, and cash are pledged for the duration of the agreement as security for interest-bearing liabilities and overdrafts. Material for PBD fungibility and secured-debt ranking; no covenant metrics given.
- **First-time comparative (p.14/15 **):** 31 Mar 2025 comparatives presented for the first time "to enhance presentation." Per standing guidance this is a presentation choice, **not** evidence of restatement or unreliability. No restatement of Sep-25 figures indicated.
- **Rate basis:** all facilities JIBAR-linked (3-month JIBAR + 2.8%–5.0%) except the Revolving Facility at Prime −0.25% to −0.35%. Rate-cap/hedge sensitivity not disclosed here.
- **Maturity-date oddity:** the "Notes – Bullet" line shows issue dates to 31/10/2025 and a maturity range 31/12/2026–31/03/2032, but one sub-line (15/02/2022, JIBAR+3.39%) matures 18/09/2025 and carries nil at Mar-26 (was R181m Mar-25) — consistent with repayment, not an error.
- **No covenant, facility-limit (gross) or drawn/undrawn split for term debt** is disclosed in this note; only total undrawn *overdraft* facilities (R475m) is given. Gross facility limits and covenant headroom remain open.

## Section 3 — Questions answered and next evidence

- **Q-8612694a3a674266 (overdraft driver):** *Contradicted as framed.* Overdrafts are R273m at Mar-26, down R91m from R364m Sep-25 — no R1.9bn increase exists in this note. Facility limits/maturities for overdrafts still not itemised; undrawn overdraft facilities R475m disclosed. Partial.
- **Q-b6d6eda13d854fdf (bridge):** *Partially addressed / premise contradicted.* The −R91m overdraft movement matches the cash-flow figure; no reclassification needed. Interest-bearing debt rose R209m (4,016−3,807) vs Sep-25. Full signed cash-flow-to-balance bridge still needs the cash-flow statement (p.12) and Sep-25/Mar-25 closing debt — Pending: D003.3 (p.12).
- **Q-7ccb4721205d4f99 (covenants/facilities):** *Partial.* Undrawn overdraft facilities R475m disclosed; covenant ratios, thresholds, headroom and term-debt facility limits/maturities **not** disclosed here. Pending: D003.1/D003.3 and any covenant note.
- **Q-5973eb62939a4c48 (cash-flow label):** not addressed by this note; remains open — Pending: D003.3 (p.12).
- Other stored questions (EBITDA bridge, PBD roll-forward, FX, headline EPS, other investments/derivative) are **not** addressed by this funding note; carry forward.

**New material questions (see JSON):**
1. Gross facility limits, covenant metrics/headroom and term-debt drawn/undrawn split at 31 Mar 2026 (target D003.1/D003.3 or covenant note).
2. Confirm the R2,273m overdraft figure in the stored questions is a misread vs the R273m in Note 2 (target D003.1 statement of financial position, p.8) — to prevent a false liquidity alarm propagating.

**Next evidence:** D003.1 (p.8 statement of financial position) to confirm overdraft/debt balances; D003.3 (p.12 cash-flow) for the financing bridge and label check.

## Section 4 — Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [
  {"question_id": "Q-8612694a3a674266", "status": "contradicted", "answer": "Note 2 shows bank overdrafts of R273m at 31 Mar 2026, not R2,273m; overdrafts fell R91m from R364m at 30 Sep 2025 (273-364=-91). No R1.9bn increase exists in this note. Total undrawn overdraft facilities rose to R475m (Sep-25 R136m; Mar-25 R43m). Overdraft facility limits/maturities and drawn/undrawn split for term debt are not itemised here.", "evidence": [
    {"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 14, "quote": "Bank overdrafts | 273 |  | 457 | 364"},
    {"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 14, "quote": "Total undrawn overdraft facilities | 475 |  | 43 | 136"}
  ]},
  {"question_id": "Q-b6d6eda13d854fdf", "status": "partial", "answer": "The -R91m net overdraft movement matches Note 2 (273 vs 364 at 30 Sep 2025); no reclassification is indicated. Total interest-bearing liabilities rose R209m (4,016-3,807) vs Sep-25, driven by senior debt +254 (3,547-3,293) partly offset by revolving facility -74. A full signed cash-flow-to-balance bridge still requires the cash-flow statement (p.12) and Mar-25 closing debt.", "evidence": [
    {"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 14, "quote": "Total interest-bearing liabilities | 4 016 |  | 3 864 | 3 807"},
    {"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 14, "quote": "Senior debt | 3 547 |  | 3 182 | 3 293"}
  ]},
  {"question_id": "Q-7ccb4721205d4f99", "status": "partial", "answer": "Total undrawn overdraft facilities R475m at 31 Mar 2026 (Sep-25 R136m; Mar-25 R43m). Covenant ratios, thresholds, headroom and term-debt facility limits/maturities are not disclosed in Note 2; remain open pending covenant/facility disclosures.", "evidence": [
    {"source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc", "physical_page": 14, "quote": "Total undrawn overdraft facilities | 475 |  | 43 | 136"}
  ]}
], "new_questions": [
  {"question": "What are the gross facility limits, covenant metrics/thresholds and headroom, and the drawn/undrawn split and maturities for term debt (senior, subordinated, revolving) at 31 Mar 2026? Note 2 gives only total undrawn overdraft facilities (R475m) and maturity buckets (R1,396m within 12 months; R2,620m thereafter).", "priority": "high", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003.1 statement of financial position (p.8) / D003.3 cash-flow (p.12) / any covenant or facility note", "evidence_required": "Gross facility limits, covenant ratios and thresholds with headroom, drawn/undrawn split and maturity dates for each term-debt class, Rm, at 31 Mar 2026 vs 30 Sep 2025", "closure_condition": "Covenant headroom and term-debt facility detail disclosed, or confirmed not disclosed; benign explanations (e.g. covenant detail in a separate debt note) acceptable. Forecast consequence: refinancing and liquidity risk, net debt trajectory."},
  {"question": "Confirm the bank overdraft balance at 31 Mar 2026: Note 2 (p.14) shows R273m, but stored questions reference R2,273m. Is R2,273m a misread (e.g. total liabilities or a transposition), and what is the correct closing overdraft on the statement of financial position (p.8)?", "priority": "high", "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf", "target_section": "D003.1 statement of financial position (p.8)", "evidence_required": "Bank overdraft line on the statement of financial position at 31 Mar 2026, 30 Sep 2025 and 31 Mar 2025, Rm, reconciled to Note 2", "closure_condition": "Overdraft balance confirmed as R273m (or corrected) and reconciled to the statement of financial position; benign explanation (misread/transposition) acceptable. Forecast consequence: prevents a false liquidity alarm in net debt modelling."}
]}
```