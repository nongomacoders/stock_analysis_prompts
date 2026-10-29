Material facts/calculations (historical unless stated). Balance sheet at 31 Mar 2026: total equity R1,329m, ordinary share capital R5,410m, retained loss R(4,111)m; 780m ordinary shares after 4m treasury shares (pp.8,11). Statutory ordinary NAV/share = 1,329/780 = R1.70; share capital is not NAV. Cash-flow closing cash R113m = opening R107m + net increase R6m + FX nil (p.12); balance-sheet cash R112m plus R1m held-for-sale cash = R113m (pp.8,12 fn). PBD: principal POCI net carrying R3,845m = 3,975 + 382 − 728 + 383 − 167; other FVTPL R644m = 702 + 28 − 116 + 30; total PBD R4,489m = 4,677 + 410 − 844 + 383 − 167 + 30 (p.13; p.8). Debt: total interest-bearing liabilities R4,016m = notes 822 + loans 2,921 + overdrafts 273; senior 3,547 + subordinated 196 + overdrafts 273; within 12 months R1,396m, thereafter R2,620m; undrawn overdraft facilities R475m (p.14). Interest-bearing debt rose R300m (3,743−3,443) vs cash net proceeds/settlements +R303m (1,145−842), leaving R3m unexplained in this capture; overdrafts fell R91m and cash net overdraft movement was −R91m; lease liabilities fell R19m vs R30m repayment (pp.8,12,14).

Question answers/uncertainty. Q-NTU-DEFAULT-02: partial; the PBD bridge above reconciles principal POCI net carrying, but pp.8–15 do not give gross carrying amount or separate cumulative ECL allowance; R(167)m is period impairment loss, not conventional coverage. Other FVTPL is separate. Q-NTU-DEFAULT-04: partial; the same bridge reconciles signed PBD movement, but the printed non-IFRS amount is not in pp.8–15, so comparison/rounding cannot be tested. Q-NTU-DEFAULT-06: open; only total trade and other receivables R497m is shown (p.8), no trade/other split or ECL policy in capture. Q-NTU-DEFAULT-08: open; historical-book dated movements are on p.24, not captured. Management explanation: note 1 says principal portfolios are POCI at amortised cost; other purchased book debts lack title/SPPI and are FVTPL (p.13). No guidance in pp.8–15.

Pending: note 6.3 FVTPL and trade/other receivables notes pp.22,25; historical-book p.24; CODM pp.31,35; POCI gross/cumulative pp.21–24; debt/lease reconciliation pp.14–15 and later notes.

```json
{
  "ledger_version": 1,
  "updates": [
    {
      "question_id": "Q-NTU-DEFAULT-02",
      "status": "partial",
      "answer": "Principal POCI net carrying amount reconciles: 3,975 + 382 - 728 + 383 - 167 = 3,845 (Rm). Other FVTPL assets reconcile separately: 702 + 28 - 116 + 30 = 644. Gross carrying amount and separate cumulative ECL allowance are not disclosed in pp.8-15, so conventional coverage cannot be computed.",
      "evidence": [
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 13,
          "quote": "Balance at the beginning of the period | 3 975"
        },
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 13,
          "quote": "Impairment loss | (167)"
        },
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 13,
          "quote": "Balance at the end of the period | 3 845"
        }
      ]
    },
    {
      "question_id": "Q-NTU-DEFAULT-04",
      "status": "partial",
      "answer": "Signed PBD movement reconciles: principal 3,975 + 382 - 728 + 383 - 167 = 3,845; other FVTPL 702 + 28 - 116 + 30 = 644; total 4,677 + 410 - 844 + 383 - 167 + 30 = 4,489 (Rm). The printed non-IFRS amount is not in pp.8-15, so comparison and rounding cannot be tested.",
      "evidence": [
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 13,
          "quote": "Fair value movements | 30"
        },
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 13,
          "quote": "Balance at the end of the period | 3 845"
        }
      ]
    }
  ],
  "new_questions": [
    {
      "question": "Reconcile interest-bearing debt, bank overdrafts and lease liabilities movements to cash-flow proceeds/settlements, including non-cash, FX, lease additions/interest and held-for-sale effects; explain any residual.",
      "priority": "medium",
      "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf",
      "target_section": "Interest-bearing liabilities note 2 and cash-flow financing, physical pp.12,14-15",
      "evidence_required": "Opening/closing balances by instrument, cash proceeds/repayments, non-cash/FX/lease movements, and signed residual.",
      "closure_condition": "Signed bridge reconciles each debt/overdraft/lease balance to cash-flow and non-cash movements within stated rounding tolerance."
    }
  ]
}
```