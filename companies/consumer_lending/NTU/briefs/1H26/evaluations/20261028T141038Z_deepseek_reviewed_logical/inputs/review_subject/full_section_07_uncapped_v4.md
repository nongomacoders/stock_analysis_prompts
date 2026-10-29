**Section reading brief — Nutun 1H26 primary statements (pp.9–11)**

**Material facts and signed calculations**
- **Income statement (p.9, historical, unaudited H1 FY26 vs H1 FY25 and audited FY25):** revenue R711m, cost of revenue R(385)m, gross profit R326m; net income from purchased book debts R69m; CAEIR R383m; interest expense R(177)m; impairment loss on principal book portfolios R(167)m; FV movements on other financial assets R30m. The printed PBD subtotal reconciles: **383 − 177 − 167 + 30 = 69**. Operating loss R(79)m; net finance charge R(39)m (finance income R6m, finance charges R(45)m); loss before tax R(92)m; income tax R29m; continuing loss R(63)m; discontinued nil; total loss R(63)m. Total basic/diluted EPS (8.1)c vs (8.2)c H1 FY25 and (30.3)c FY25.
- **Comprehensive income (p.10):** loss R(63)m plus exchange loss on translation R(4)m = total comprehensive loss R(67)m, all attributable to parent ordinary holders; NCI nil.
- **Equity (p.11):** opening audited 30 Sep 2025 parent ordinary equity R1,396m; total comprehensive loss R(67)m; grant of conditional share plans +R4m; treasury shares acquired R(4)m; closing unaudited 31 Mar 2026 equity R1,329m. Check: **1,396 − 67 + 4 − 4 = 1,329**. Closing components: share capital R5,410m + share-based payment reserve R7m + foreign currency translation reserve R23m + retained loss R(4,111)m = R1,329m. Shares: 784m opening, less 4m treasury acquired = **780m closing**. Statutory ordinary NAV/share = **R1,329m / 780m = R1.7038 ≈ R1.70**. NCI nil; no preference/non-ordinary claim is shown in this captured statement.
- No secondary note headings are observed in this capture. No management explanation or guidance appears; the above are reported historical facts.

**Question answers**
- **Q-16637545892d4890:** Resolved on this capture. Date-matched net ordinary shares 780m and parent ordinary equity R1,329m give statutory NAV/share ≈R1.70; share capital/reserves/retained loss reconcile as above. Historical fact from p.11.
- **Q-NTU-DEFAULT-04:** Partial. Page 9 supports the printed PBD subtotal: **CAEIR 383 − interest expense 177 − impairment 167 + FV movements 30 = net income from PBD 69**. But principal/other collections and the printed non-IFRS amortisation amount are not in pp.9–11, so the requested signed reconstruction and rounding/material residual assessment cannot be completed. Historical fact only; no guidance.

**Remaining material uncertainty:** Q-NTU-DEFAULT-04 remains partial pending the CODM/amortisation disclosures; no new material question is needed because the existing question captures the missing evidence.

**Pending:** physical page 12 for the next note disclosures (not supplied); pp.13,31,35 for signed CODM amortisation, collections and non-IFRS reconciliation.

```json
{
  "ledger_version": 1,
  "updates": [
    {
      "question_id": "Q-16637545892d4890",
      "status": "resolved",
      "answer": "Closing 31 Mar 2026 ordinary shares are 780m after 4m treasury shares acquired; parent ordinary equity is R1,329m. NAV/share = 1,329/780 = R1.7038 (~R1.70). Equity reconciles: 5,410 + 7 + 23 - 4,111 = 1,329; NCI nil.",
      "evidence": [
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 11,
          "quote": "Balance at 31 March 2026 - Unaudited | 780 |  | 5 410 | 7 | 23 | (4 111) | 1 329"
        }
      ]
    },
    {
      "question_id": "Q-NTU-DEFAULT-04",
      "status": "partial",
      "answer": "Page 9 gives CAEIR 383, interest expense (177), impairment (167), FV movements 30 and net income from PBD 69; 383 - 177 - 167 + 30 = 69. Principal/other collections and printed non-IFRS amortisation are absent from pp.9-11, so signed reconstruction and rounding assessment remain incomplete.",
      "evidence": [
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 9,
          "quote": "Net income from purchased book debts | 69"
        },
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 9,
          "quote": "Interest expense | (177)"
        },
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 9,
          "quote": "Impairment loss on principal book portfolios | (167)"
        },
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 9,
          "quote": "effective interest rate | 383"
        },
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 9,
          "quote": "Fair value movements on other financial assets | 30"
        }
      ]
    }
  ],
  "new_questions": []
}
```