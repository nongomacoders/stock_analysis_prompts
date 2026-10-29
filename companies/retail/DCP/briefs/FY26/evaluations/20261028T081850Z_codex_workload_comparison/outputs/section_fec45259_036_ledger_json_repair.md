```json
{
  "updates": [
    {
      "question_id": "Q-c744afc711774bb9",
      "status": "partial",
      "answer": "Revenue from contracts with customers FY2026 R42,825,777k vs FY2025 R39,172,347k (+9.3%); cost of sales R33,416,598k/R30,371,972k; gross profit R9,409,179k/R8,800,375k; other income R3,797,149k/R3,347,467k; total income R13,206,328k/R12,147,842k (+8.7%). Stored total income R11,190m and margins 30.9%/31.0%/30.7% do not match this capture (actual 30.84%/31.01%); store-sales R40,488m and intergroup R(1,814)m not visible. Remainder open for D006.",
      "evidence": [
        {
          "source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6",
          "physical_page": 108,
          "quote": "Revenue from contracts with customers |  | 42 825 777 | 39 172 347 | 9.3"
        },
        {
          "source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6",
          "physical_page": 108,
          "quote": "Total income |  | 13 206 328 | 12 147 842 | 8.7"
        }
      ]
    },
    {
      "question_id": "Q-335b06a0ce2649d5",
      "status": "resolved",
      "answer": "Revenue +9.3% to R42,825,777k; gross margin 21.97% FY2026 vs 22.47% FY2025 (down ~50bps); total income margin 30.84% vs 31.01%. Growth is top-line only; margin compressed.",
      "evidence": [
        {
          "source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6",
          "physical_page": 108,
          "quote": "Gross profit |  | 9 409 179 | 8 800 375 | 6.9"
        }
      ]
    },
    {
      "question_id": "Q-cdabe753e3ab46cb",
      "status": "partial",
      "answer": "FY2025 total income margin as reported here is 31.01% (R12,147,842k / R39,172,347k). The 30.7% 'excluding property gain' comparator is not reproduced in this capture; property gain amount not located. Remainder open for D006.",
      "evidence": [
        {
          "source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6",
          "physical_page": 108,
          "quote": "Total income |  | 13 206 328 | 12 147 842 | 8.7"
        }
      ]
    },
    {
      "question_id": "Q-0406bad610e94bcf",
      "status": "partial",
      "answer": "9.3% is total revenue from contracts with customers (R42,825,777k vs R39,172,347k), not merchandise-only. Segmental reconciliation and R6.2bn external wholesale still open.",
      "evidence": [
        {
          "source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6",
          "physical_page": 108,
          "quote": "Revenue from contracts with customers |  | 42 825 777 | 39 172 347 | 9.3"
        }
      ]
    },
    {
      "question_id": "Q-e9df7e72a7c4457d",
      "status": "partial",
      "answer": "Deferred revenue (contract liability) R34,242k FY2026 vs R86,912k FY2025 is the only rewards-adjacent balance visible; launch date and 17-week cohort basis not in this capture. Remainder open.",
      "evidence": [
        {
          "source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6",
          "physical_page": 109,
          "quote": "Deferred revenue (contract liability)"
        }
      ]
    },
    {
      "question_id": "Q-cbbfe2e5a90d4260",
      "status": "partial",
      "answer": "Cybersecurity and data protection listed only as a risk focus area on p.106; no IT/cyber cost, fine, impairment or contingent liability disclosed in D002/D003. Confirm absence in D006.",
      "evidence": [
        {
          "source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6",
          "physical_page": 106,
          "quote": "Cybersecurity and data protection."
        }
      ]
    },
    {
      "question_id": "Q-a2bc90ee61cf4284",
      "status": "partial",
      "answer": "Total capex FY2026 R1.1bn (FY2025 R1.4bn) stated in text; chart series values not legible in capture; cash-flow PP&E/intangible purchase lines not in this capture (p.111 not supplied). Remainder open for D003 cash-flow page.",
      "evidence": [
        {
          "source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6",
          "physical_page": 106,
          "quote": "Total capital expenditure for the year was R1.1 billion"
        }
      ]
    }
  ],
  "new_questions": [
    {
      "question": "Extract cash-flow statement purchase of PP&E and purchase of intangible assets for FY2026 and FY2025 (R'000) and reconcile to stated total capex R1.1bn (FY2025 R1.4bn) and to the intangible asset movement (R1,448,057k to R1,740,823k).",
      "priority": "high",
      "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf",
      "target_section": "D003 cash-flow statement (p. 111)",
      "evidence_required": "Cash-flow lines 'purchase of property, plant and equipment' and 'purchase of intangible assets' both years, R'000, with page citation; reconciliation to R1.1bn total capex and to intangible movement.",
      "closure_condition": "Both cash-flow lines extracted for both years and reconciled to stated capex and intangible movement, or discrepancy quantified; benign explanations (reclassification, accruals) allowed."
    },
    {
      "question": "Reconcile p.106 summary 'Bank loans (1,745)' to statement of financial position loans payable non-current R1,509,942k plus current R517,636k = R2,027,578k (gap ~R282m); state whether p.106 is gross or net of loans receivable R117,275k + R78,395k.",
      "priority": "high",
      "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf",
      "target_section": "D006 notes (loans payable note)",
      "evidence_required": "Loans payable note showing gross debt, loans receivable offset, and definition used in p.106 summary; both years, R'000, with page citations.",
      "closure_condition": "R282m gap explained with definition stated, or discrepancy quantified; forecast debt base confirmed."
    },
    {
      "question": "Decompose deferred revenue (contract liability) R34,242k FY2026 vs R86,912k FY2025 (release R52,670k) into loyalty programme, vouchers, prepaid and other components; confirm revenue recognition timing and whether release is in revenue or other income.",
      "priority": "high",
      "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf",
      "target_section": "D006 notes (contract liabilities / revenue note)",
      "evidence_required": "Contract liability composition and movement, both years, R'000, with page citations; revenue recognition policy for loyalty/vouchers.",
      "closure_condition": "Composition and release treatment confirmed with citation; forecast loyalty liability base stated."
    },
    {
      "question": "Explain investment in associates and joint ventures increase from R356,267k to R564,093k (+R207,826k) against associate profit of only R48,179k; identify acquisitions, capital injections, or revaluations and list associate/JV names.",
      "priority": "high",
      "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf",
      "target_section": "D006 notes (associates and joint ventures note)",
      "evidence_required": "Associates/JV note showing opening balance, additions, share of profit, dividends, closing balance, both years, R'000, with page citations; list of associates/JVs.",
      "closure_condition": "R207.8m increase explained with line-item breakdown; cash vs non-cash nature stated; forecast treatment confirmed."
    },
    {
      "question": "Decompose other reserves balance of negative R4,689,953k (FY2025 negative R4,660,301k) into treasury shares, share-based payment reserve, foreign currency translation reserve, and any bargain purchase reserve; confirm any share buyback activity in FY2026.",
      "priority": "medium",
      "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf",
      "target_section": "D006 notes (equity note / statement of changes in equity)",
      "evidence_required": "Other reserves breakdown both years, R'000, with page citations; share buyback disclosure (shares and amount) if any.",
      "closure_condition": "Other reserves decomposed with citation; buyback activity confirmed or ruled out; equity roll-forward reconciled."
    },
    {
      "question": "Confirm FY2026 interim dividend per share (implied 29.4c from total 45.3c less final 15.9c), FY2025 total DPS, and the stated dividend payout policy target; reconcile 45.3c DPS to 114.2c basic EPS (39.7% payout).",
      "priority": "medium",
      "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf",
      "target_section": "D006 notes (dividends note) / D002 dividend policy",
      "evidence_required": "Interim and final DPS both years, total DPS, stated payout policy target %, with page citations.",
      "closure_condition": "DPS components and payout policy confirmed with citation; payout ratio reconciled; forecast dividend base stated."
    },
    {
      "question": "Split net financing costs R506,568k FY2026 (FY2025 R490,605k) into IFRS 16 lease interest and bank/other interest; reconcile to lease liability movement (R2,663,849k to R2,943,233k) and average debt balances.",
      "priority": "medium",
      "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf",
      "target_section": "D006 notes (finance costs note / leases note)",
      "evidence_required": "Finance costs breakdown (lease interest vs bank interest) both years, R'000, with page citations; lease liability movement reconciliation.",
      "closure_condition": "Finance costs split confirmed with citation; interest forecast inputs stated."
    },
    {
      "question": "Decompose trade and other receivables R3,808,486k FY2026 vs R3,312,834k FY2025 (+14.9%) into trade receivables, other receivables and prepayments; provide ageing and ECL/impairment allowance; explain growth ahead of revenue (+9.3%).",
      "priority": "medium",
      "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf",
      "target_section": "D006 notes (trade receivables note / financial instruments)",
      "evidence_required": "Receivables breakdown and ageing both years, R'000, with page citations; ECL allowance and write-offs.",
      "closure_condition": "Receivables composition and ECL confirmed with citation; growth vs revenue explained; working-capital forecast input stated."
    },
    {
      "question": "Confirm inventory days and any inventory write-down/obsolescence provision for FY2026 vs FY2025, given inventory flat at R7,908,461k vs R7,905,213k while revenue grew 9.3%.",
      "priority": "low",
      "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf",
      "target_section": "D006 notes (inventory note)",
      "evidence_required": "Inventory composition, write-down/obsolescence provision, and inventory days both years, with page citations.",
      "closure_condition": "Inventory days and write-down confirmed with citation; margin quality assessed."
    },
    {
      "question": "Confirm whether any restatement, auditor qualification, or material weakness in internal controls is disclosed, given p.106 statement that no material breakdowns were identified.",
      "priority": "low",
      "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf",
      "target_section": "D004 / D006 (auditor's report / corporate governance)",
      "evidence_required": "Auditor's report opinion type and any emphasis-of-matter or qualification; any restatement disclosure, with page citations.",
      "closure_condition": "Audit opinion and any restatement confirmed with citation; forecast reliability assessed."
    }
  ]
}
```