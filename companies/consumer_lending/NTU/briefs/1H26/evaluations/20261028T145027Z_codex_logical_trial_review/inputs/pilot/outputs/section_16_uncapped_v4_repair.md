```json
{
  "ledger_version": 1,
  "updates": [
    {
      "question_id": "Q-NTU-DEFAULT-08",
      "status": "resolved",
      "answer": "Prior halves summed: H1 FY25 historical-book loss 77 + H2 FY25 loss 182 = FY25 full-year loss 259. H1 FY26 historical-book loss 191 is a six-month figure, not a full-year figure. Vintage/FX split is not disclosed on p.24, so FX/vintage limitation cannot be quantified; no FX plug used.",
      "evidence": [
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 24,
          "quote": "principal book portfolios | (64) (38) 24 |  |  |  | 1 | (77) |"
        },
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 24,
          "quote": "book portfolios | (58) (82) (8) |  |  |  | (34) | (182) |"
        },
        {
          "source_sha256": "9a19b3b40ca26781100da0f0bd7d59a870fabd253a66ccac0c9926f14bc4fbbc",
          "physical_page": 24,
          "quote": "principal book portfolios | (242) 46 4 |  |  |  | 1 | (191) |"
        }
      ]
    }
  ],
  "new_questions": [
    {
      "question": "Reconcile principal book gross carrying amount, signed cumulative impairment gain/ECL allowance, and net carrying amount; establish whether portfolios are POCI amortised cost or other FVTPL, and do not treat R431m as conventional loss coverage.",
      "priority": "high",
      "target_document": "nutunlimitedcondensedconsolidatedafs31march2026.pdf",
      "target_section": "Note 6.1 credit risk / principal book portfolios, physical p.24 and later portfolio notes",
      "evidence_required": "Gross carrying amount, acquisition baseline, cumulative lifetime ECL/gain, net carrying amount, and portfolio classification by segment.",
      "closure_condition": "For each principal-book segment, gross carrying amount plus signed cumulative ECL/gain equals net carrying amount, and POCI/FVTPL classification is stated."
    }
  ]
}
```