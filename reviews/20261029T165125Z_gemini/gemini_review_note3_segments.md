# Gemini-Role Review: Note 3 Segment Analysis (PAN Section S007)

**Evaluation Run**: `reviews/20261029T165125Z_gemini/gemini_review_note3_segments.md`  
**Review Target**: commits `f82c638` (P0), `4b94f70` (P1+P2) plus the P4 artifacts on branch `agentic-report-build`.  
**Subject**: `WORKPLAN_SEGMENT_ANALYSIS.md`, `build/extraction/extract_pan_note3_segments.py`, `tests_reconcile/test_note3_segments.py`, `READING_BRIEF_SEGMENT_ANALYSIS.md`, `build/report_view.xlsx` (5 tabs).

---

### 1. Covenant compliance

| Covenant | Finding | Verdict |
|---|---|---|
| **1 — never replace a printed figure** | All 880 Note 3 cells carry printed glyphs verbatim (`value_raw`, including brackets and en-dashes). The Adjusted EBITDA scope difference is recorded as an `ambiguity` conflict; 663.1 and 609,431 both remain in the database. No substituting occurred on the default branch. | PASS |
| **2 — arithmetic in code** | Horizontal identities (cols 0–4 = subtotal; subtotal + 4 non-operating columns = group) execute as pytest assertions over all 72 rows. No prose sum appears in the brief that is not also asserted in the suite. Excel contains 0 formulas (enforced by a guard that raises on any cell starting with `=`). | PASS |
| **3 — lineage** | Every cell carries page (21–24), document SHA-256 and `p1_note3_segments_v2`. Pages 21–24 renders recorded with SHA-256. | PASS |
| **4 — ledger independence** | `Q-c1e6100f7a674873` (APM definitions) stays **open** even though the scope difference is now arithmetically proved — correct, because definition wording is a prose matter. | PASS |

### 2. Methodological observations

- **Column geometry derived, not hardcoded.** Edges come from per-page numeric right-edge clusters (≥4 tokens, 5pt tolerance). This is materially stronger than the earlier D009 approach and makes the extractor portable to the FY25 pages, which have no shared render.
- **Fragment re-joining is evidence-preserving.** FY25 numbers split across a wide space (`242,` + `186`) are rejoined at ≤12pt with glyphs concatenated, so `value_raw` still reads as the printed digits.
- **The intra-group block was not forced into the grid.** Pages 21/23 print a second block with different column semantics; routing it to `note3_intra_group` and excluding it from segment identities is the correct call, and it is disclosed as a conflict rather than silently dropped.
- **The 0.1 EBITDA residual is genuinely closed.** The brief's claim that p.50 Group EBITDA is the sum of unrounded segment figures is backed by an executed check (663,101 → 663.1; 245,765 → 245.8) plus a per-column rounding check of the four operating segments. This is a real improvement over the D009-only pass, where the 0.1 gap was merely recorded.

### 3. Residual risks accepted

1. The 594 revenue cell sits in the Agricultural ESG column by geometry (anchor 671.9 vs ESG edge 671.4, Corporate edge 714.1). Arithmetic cannot distinguish ESG from Corporate because only one of the two is non-zero, so this rests on geometry alone. Acceptable, but worth an independent render look if ESG revenue becomes material to the narrative.
2. Note 3 Group figures are USD; the D009 ZAR table's translation basis is not evidenced in these pages. The brief correctly leaves that step pending rather than inferring a rate.
3. The engine was narrowed to the three D009 regions. This is the right fix for cross-section column-semantics mixing, but it means new sections must each bring their own identities — a scaling cost, not a defect.

**Verdict: ACCEPT WITHOUT AMENDMENT.**
