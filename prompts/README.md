# Active prompts

Prompts are versioned under `prompts/<sector>/<stage>/<version>/prompt.md` and assembled automatically by `section_capture/packages.py` when saving a section pack based on company sector.

| Sector | Prompt | Version | Role |
| --- | --- | --- | --- |
| `mining` | `00-report-orientation` | `v1.0.0` | Orient the LLM with the major-section map of mining reports (production, capex, ore bodies). |
| `mining` | `12-analyst-reading-brief` | `v1.1.0` | Forensic financial analyst reading a mining report: throughput, grades, recoveries, AISC, capex cliffs, and Section 36 mining tax. |
| `retail` | `00-report-orientation` | `v1.0.0` | Orient the LLM with the major-section map of retail reports (brands, credit risk, store networks). |
| `retail` | `12-analyst-reading-brief` | `v1.1.0` | Forensic financial analyst reading a retail report: merchandise vs credit revenue, gross margin, debtor costs/IFRS 9 ECL, store footprint, and working capital. |
| `reit` | `00-report-orientation` | `v1.0.0` | Orient the LLM with the major-section map of REIT & listed property reports (property portfolios, lease profiles, debt). |
| `reit` | `12-analyst-reading-brief` | `v1.1.0` | Forensic financial analyst reading a REIT report: distributable income/DIPS, LTV & look-through debt, interest rate hedging, WALE, cap rates, and covenant headroom. |
| `it` | `00-report-orientation` | `v1.0.0` | Orient the LLM with the major-section map of IT & software reports (recurring revenue, contract assets, debt). |
| `it` | `12-analyst-reading-brief` | `v1.1.0` | Forensic financial analyst reading an IT report: ARR/MRR mix, billable consultant utilization, contract assets/deferred revenue, software capitalization, and legacy dispute provisions. |
| `finance` | `*` | `*` | Falls back to generic reading prompt unless sector-specific prompt is provided. |
| `telcos` | `*` | `*` | Falls back to generic reading prompt unless sector-specific prompt is provided. |
