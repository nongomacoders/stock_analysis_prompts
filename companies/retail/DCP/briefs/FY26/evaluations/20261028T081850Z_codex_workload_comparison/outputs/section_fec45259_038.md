### 1. Stored Questions Answered in This Section

No stored questions from earlier sections were supplied with this capture (the prompt states 12 of 449 open records are current-capture questions, but none were included in the `STORED QUESTIONS FROM EARLIER SECTIONS` block). All 12 D003-targeted questions remain open and are carried forward in Section 4.

### 2. Footnote & Qualification Deep-Dive

- **p.116 footnote `*`**: "Pursuant to the provisions of section 56 of the Companies Act, disclosures from foreign nominee companies have been included in this analysis." [D003, physical PDF p. 116]. This confirms the shareholder-spread table includes foreign nominee holdings that would otherwise be excluded — relevant only to ownership concentration analysis, not to revenue/margin/credit forecasting. No reconciliation impact on financials.
- **p.119 non-public breakdown**: Total non-public = 8 holdings, 73 901 275 shares (8.59%). Arithmetic check: 3 190 direct + 73 898 085 indirect = 73 901 275 ✓. Directors (7 holdings) 63 711 063 + prescribed officer (1) 10 190 190 = 73 901 274 — **1-share rounding discrepancy** vs stated 73 901 275 (immaterial; likely rounding in the 10 190 212 vs 10 190 211 line). Flag as low-priority arithmetic check.
- **p.117 vs p.119 director holdings tension**: p.117 lists "Directors and associates" = 73 901 275 shares (8.59%); p.119 breaks this into directors 63 711 063 + prescribed officers 10 190 212 = 73 901 275 ✓. Consistent.
- **p.120 AGM notice**: Confirms FY end = **28 February 2026** (ordinary resolution 1: "year ended 28 February 2026"). Also confirms Ivan Saltzman and Saul Saltzman are being ratified as **Non-Executive Directors** (resolution 4), and Ivan Saltzman's indirect holding (34 940 933 via Ivlyn) is disclosed on p.119 — consistent with the executive-to-NED transition flagged in stored questions Q-c0abddef102f479a / Q-b1f7b19313ed451a. **No remuneration or share-based payment amounts are disclosed in this section** — those remain for the remuneration note (not in this capture).
- **No footnote references to revenue, debtors, inventory, or lease items appear in this section** — it is purely shareholder-analysis and AGM-notice material. No credit/merchandise footnote to unpack here.

### 3. New Questions to Test in Future Sections

| ID | Priority | Target section | Trigger | Specific check | Why it matters |
|---|---|---|---|---|---|
| Q-new-1 | Medium | D001 (Integrated Report, remuneration section) / D003 notes | p.120 resolution 4 ratifies Ivan & Saul Saltzman as NEDs; p.119 shows Ivan's 34 940 933 indirect (4.06%) and Saul's 348 591 (0.04%) | Locate director remuneration table and share-based payment note; confirm whether any FY2026 amounts relate to the executive→NED transition and whether FY2027 NED fees are disclosed | Cost base and related-party disclosure for FY2027 forecast |
| Q-new-2 | Low | D003 (p.119) | 1-share rounding discrepancy in non-public total (73 901 274 vs 73 901 275) | Confirm whether 10 190 212 is correct or a typo; reconcile to 73 901 275 | Immaterial; only affects ownership % precision |
| Q-new-3 | Medium | D001 (remuneration) / D003 | p.120 confirms AGM 31 July 2026 and FY end 28 Feb 2026 | Confirm FY2026 year-end date and whether any post-balance-sheet events (NED transitions effective 1 July 2026) are disclosed as adjusting/non-adjusting | Forecast period alignment and any one-off FY2027 costs |
| Q-new-4 | Low | D001 (shareholder info) | p.118 P/E 25.77, dividend yield 1.24%, market cap R31.82bn | Cross-check DPS implied by dividend yield (1.24% × R37.00 ≈ 45.9c) against stated DPS (interim + final 15.92c) in D002/D003 dividend note | Validates dividend forecast and payout ratio |
| Q-new-5 | Medium | D002 / D003 (dividend note) | p.118 dividend yield 1.24% at R37.00 implies ~45.9c total DPS | Extract interim DPS, final DPS (stated 15.92c), total DPS, EPS, HEPS; compute payout ratio vs policy | Dividend sustainability and forecast |

### 4. Updated Open Questions Ledger

```json
{"ledger_version": 1, "updates": [], "new_questions": [
  {"question": "In the remuneration and share-based payment notes (D001 Integrated Report remuneration section or D003 notes), confirm whether any FY2026 amounts relate to the Ivan Saltzman and Saul Saltzman executive-to-NED transitions (ratified at AGM 31 July 2026 per p.120 resolution 4), and whether FY2027 NED fees are disclosed. State amounts in Rm or confirm nil.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D001 (remuneration governance and disclosure) / D003 notes", "evidence_required": "Director remuneration table, share-based payment note, and related-party note for FY2026 vs FY2025 in Rm, with page citations; explicit statement if transition-related amounts are nil.", "closure_condition": "Transition-related remuneration/share-based/related-party amounts quantified or confirmed nil, with source pages cited; impact on FY2027 cost base noted."},
  {"question": "Reconcile the 1-share discrepancy in the p.119 non-public breakdown: directors 63 711 063 + prescribed officers 10 190 212 = 73 901 274 vs stated total 73 901 275. Confirm whether 10 190 212 is correct or a typo, and reconcile to the p.117 'Directors and associates' 73 901 275 (8.59%).", "priority": "low", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D003 (p.119)", "evidence_required": "Corrected prescribed officer holding figure or confirmation of rounding, with page citation.", "closure_condition": "Discrepancy explained (rounding vs typo) and total reconciled to 73 901 275."},
  {"question": "Confirm FY2026 financial year-end date (28 February 2026 per p.120 ordinary resolution 1) and check whether any post-balance-sheet events — specifically the Ivan Saltzman and Saul Saltzman NED transitions effective 1 July 2026 — are disclosed as adjusting or non-adjusting events in the notes.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D003 notes / D001", "evidence_required": "Year-end date with page citation; events-after-reporting-period note showing any transition-related disclosure, with page citations; explicit statement if none.", "closure_condition": "Year-end date confirmed with citation; any post-balance-sheet transition disclosure quantified or confirmed absent."},
  {"question": "Cross-check the p.118 dividend yield (1.24% at R37.00 closing price, implying ~45.9c total DPS) against the stated interim DPS, final DPS (15.92c), total DPS, EPS and HEPS in the D002/D003 dividend note; compute payout ratio vs stated dividend policy.", "priority": "medium", "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf", "target_section": "D002 Financial review / D003 dividend note", "evidence_required": "Dividend per share table, EPS/HEPS reconciliation, both years, cents, with page citations; stated dividend policy.", "closure_condition": "DPS/EPS/HEPS extracted for both years; implied DPS from yield reconciled to stated total DPS; payout ratio computed and reconciled to policy."}
]}
```

### 5. Baseline Forecast Inputs Captured Here

| Metric | Value | Source |
|---|---|---|
| Shares in issue | 860 084 483 | [D003, p.116, p.117, p.118] |
| Total shareholdings | 40 596 | [D003, p.116] |
| Non-public shareholders | 8 holdings; 73 901 275 shares (8.59%) | [D003, p.117, p.119] |
| Public shareholders | 40 587 holdings; 782 208 330 shares (90.95%) | [D003, p.117] |
| Largest fund manager | Coronation 230 463 849 (26.80%) | [D003, p.117] |
| Largest beneficial holder | Coronation 127 971 326 (14.88%) | [D003, p.117] |
| Opening price 03 Mar 2025 | R32.92 | [D003, p.118] |
| Closing price 27 Feb 2026 | R37.00 | [D003, p.118] |
| Period high / low | R38.00 / R28.10 | [D003, p.118] |
| Volume traded | 418 217 667 (48.63% of issued) | [D003, p.118] |
| Rand value traded | R13 858 267 709 | [D003, p.118] |
| P/E at 27 Feb 2026 | 25.77 | [D003, p.118] |
| Earnings yield | 3.88% | [D003, p.118] |
| Dividend yield | 1.24% | [D003, p.118] |
| Market cap at 27 Feb 2026 | R31 823 125 871 | [D003, p.118] |
| FY end | 28 February 2026 | [D003, p.120] |
| AGM date | 31 July 2026 (virtual) | [D003, p.120] |
| Auditors | Forvis Mazars (designated: Stephan Adlam) | [D003, p.120] |

### 6. Next Section to Capture

**D002 Financial review (pp. 103–107)** — resolves Q-b71788dcac604cc4 (DPS/EPS/HEPS, ecosystem investment), Q-56cfbb30e03e4077 (Health Window quantification), Q-c6b2c9f6610b4734 (dispensary revenue/margin), Q-a0b5279a24d84ae3 (wholesale segment split), and Q-b7dc12c1601344d2 (Dis-Chem Life metrics). If D002 is unavailable, capture **D003 pp. 108–115** (primary statements: financial position, changes in equity, cash flows) to obtain the balance-sheet and cash-flow inputs needed for the forecast model.