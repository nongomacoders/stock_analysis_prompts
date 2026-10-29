Captured p.24 is only the principal-book ECL allowance rollforward; it does not classify debt purchasing vs corporate/BPO or provide outlook. Historical facts (p.24): allowance 797 at 30 Sep 2024; H1 FY25 total impairment loss 173 (acquired loss 96; historical loss 77); 624 at 31 Mar 2025. H2 FY25 total loss 26 (acquired gain 156; historical loss 182); 598 at 30 Sep 2025. H1 FY26 total loss 167 (acquired gain 24; historical loss 191); 431 at 31 Mar 2026. Signed checks: 797−173=624; 624−26=598; 598−167=431. Historical-book: H1 FY25 77; H2 FY25 182; FY25 full-year 259 (77+182); H1 FY26 191. Do not compare H1 FY26 191 directly with FY25 259 as like-for-like; it is six months vs full year. Current H1 historical loss is above either prior half but below prior full year. Management explanation (p.24): R431 cumulative impairment gain reflects elevated performance above investment base-case, mainly Banking & Specialised Lending; current-year reduction reflects payer drop-offs and reduced settlement activity on historical books. That is explanation, not guidance; no guidance in capture. No vintage or FX split is disclosed on p.24, so FX/vintage limitation cannot be quantified; no FX plug used. R431 is labelled cumulative impairment gain, not conventional loss coverage; gross/net reconciliation and POCI vs FVTPL classification are not in this capture. Q-DEFAULT-08: resolved for stated closure condition by summing prior halves; vintage/FX remains unquantified. Q-DEFAULT-01: not addressed by p.24; remains open. Pending: physical p.25 and later Note 6.1/portfolio notes for gross carrying amounts, POCI/FVTPL classification, vintage/FX splits; pp.3–7 for business-model/outlook Q-DEFAULT-01.

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
          "quote": "principal book portfolios | (58) (82) (8) |  |  |  | (34) | (182) |"
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