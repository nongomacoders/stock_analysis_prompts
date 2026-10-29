```json
{
  "open_ledger_updates": [
    {
      "question_id": "Q-c0cabdef12345678",
      "status": "partial",
      "answer": "The section confirms Larry Saltzman's role as Non-Executive Chair and notes his other board commitments. It does not provide the specific remuneration, share-based payment, or related-party disclosure amounts for the Ivan Saltzman executive-to-non-executive transition. The year-end date is not explicitly stated in this section, though 'end of February 2026' is referenced.",
      "evidence": [
        {
          "source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6",
          "physical_page": 52,
          "quote": "As at the end of February 2026, the Board comprised of 11 Directors:"
        },
        {
          "source_sha256": "fec45259c705c9e6e1c07249c8349ac24b4379707108758cfcbd08329487dee6",
          "physical_page": 53,
          "quote": "Ivan retired as an executive at the end of June 2026 and is now a non-independent Non-Executive Director on the Board."
        }
      ]
    }
  ],
  "new_questions": [
    {
      "question": "Extract FY2026 director remuneration, share-based payment expense/accrual, and related-party transactions involving Ivan Saltzman and Stan Goetsch, confirming whether any amounts relate to the executive-to-NED transition (effective 1 July 2026) and whether FY2027 NED fees are disclosed.",
      "priority": "medium",
      "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf",
      "target_section": "D002 Financial review / D003 (remuneration & related-party notes)",
      "evidence_required": "Director remuneration table, share-based payment note, and related-party note for FY2026 vs FY2025 in Rm, with page citations; explicit statement if transition-related amounts are nil.",
      "closure_condition": "Transition-related remuneration/share-based/related-party amounts quantified or confirmed nil, with source pages cited; impact on FY2027 cost base noted."
    },
    {
      "question": "Confirm the exact FY2026 financial year-end date and reporting period in the financial review/statements, reconciling to the 'end of February 2026' reference on p. 52.",
      "priority": "medium",
      "target_document": "1785744572-DIS-CHEMIR2026INTERACTIVE.pdf",
      "target_section": "D002 Financial review / D003",
      "evidence_required": "Verbatim year-end date and period statement with page citation.",
      "closure_condition": "Year-end date confirmed with citation and consistent with p. 52 reference."
    }
  ]
}
```