Section reading brief — Purchased book debts (pp21–23)

Historical facts/calculations. At 31 Mar 2026 the principal book portfolio is POCI: gross R3,414m + cumulative impairment gain R431m = net R3,845m (pp22–23). At 30 Sep 2025: R3,377m + R598m = R3,975m; at 31 Mar 2025: R3,066m + R624m = R3,690m (p22). Six-month change to 31 Mar 2026: gross +R37m; cumulative gain -R167m; net -R130m; check +37 -167 = -130 (p22). The positive R431m is a cumulative impairment gain, not conventional loss coverage; p23’s “Expected credit loss allowance” column is signed positive and adds to gross. Trade receivables are separate: gross R395m - impairment R5m = net R390m; other loans R5m; other financial assets R644m; total net R4,884m (p22). Page 21 says other financial assets within PBD include a fair-valued receivables balance, but the capture does not label the entire R644m as FVTPL.

Management explanation/policy. PBDs are classified as POCI/stage 3 on initial recognition; classification does not change even if cash flows return to contractual terms. Lifetime ECL changes go to P/L; favourable changes are impairment gains even if lifetime ECLs are below initial estimate (p21). Valuation uses monthly statistical models, net cash flows over a rolling 12 months discounted at a credit-adjusted EIR; weighted average CAEIR 19.2% at 31 Mar 2026 (31 Mar 2025 17.9%; 30 Sep 2025 18.4%) (p21). No forward guidance in captured section.

Question answers/uncertainty. Q-NTU-DEFAULT-02: resolved on arithmetic and separation: principal gross + signed cumulative gain = net for all three dates; six-month movement reconciles; POCI is separate from trade receivables and other financial assets (pp21–23). Q-NTU-DEFAULT-04: partial. CAEIR 19.2% and impairment gain R431m are available, but pp21–23 do not give principal/other collections, FV changes, or the printed non-IFRS amortisation amount, so signed PBD amortisation cannot be reconstructed or compared. Remaining material uncertainty is therefore the Q04 reconstruction/comparison; the capture supports arithmetic reconciliation only, not driver attribution.

Pending: signed PBD amortisation/collections/FV changes and printed non-IFRS amount at physical pp.13,31,35; any continuation p.24.

```json
{
  "ledger_version": 1,
  "updates": [
    {
      "question_id": "Q-NTU-DEFAULT-02",
      "status": "resolved",
      "answer": "Principal book POCI reconciles: 31 Mar 2026 gross 3,414 + cumulative impairment gain 431 = net 3,845; 30 Sep 2025 3,377 + 598 = 3,975; 31 Mar 2025 3,066 + 624 = 3,690. Six-month change: gross +37, gain -167, net -130. Trade receivables 395 - 5 = 390; other financial assets 644 (p21 notes fair-valued receivables within them); total net 4,884. POCI is separate from trade receivables and other financial assets.",
      "evidence": [
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 22,
          "quote": "Gross carrying value | 5 395 3 414"
        },
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 23,
          "quote": "Total carrying amount | 3 414 |  | 431 | 3 845"
        },
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 21,
          "quote": "include a receivables balance measured at fair value"
        }
      ]
    },
    {
      "question_id": "Q-NTU-DEFAULT-04",
      "status": "partial",
      "answer": "CAEIR 19.2% and principal-book impairment gain 431 are disclosed, but pp21-23 do not provide principal/other collections, FV changes, or the printed non-IFRS amortisation amount; signed PBD amortisation cannot be reconstructed or compared.",
      "evidence": [
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 21,
          "quote": "weighted average credit-adjusted effective interest rate at period end is 19.2%"
        }
      ]
    }
  ],
  "new_questions": []
}
```