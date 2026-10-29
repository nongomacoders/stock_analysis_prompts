# Completed single-pass versus three-pass comparison

PAN continuation is complete. Both pending calls succeeded on their first new attempt;
the authorized three-attempt exponential-backoff policy (15s,30s,Retry-After respected)
was configured but no wait/retry was needed. PAN meaning and movement were reused unchanged.

| Case | One-pass cost | Three-pass total cost | One-pass request seconds | Three-pass summed request seconds | Ledger valid: one / three |
|---|---:|---:|---:|---:|---|
| NTU | $0.004702 | $0.010517 | 18.457 | 29.956 | No / Yes |
| PAN | $0.004671 | $0.011184 | 16.914 | 30.421 | Yes / Yes |

New PAN requests: USD0.0094843224,input24747,completion5379,reasoning0,cached1122. Continuation dispatch-to-last-accounting42.049s. Combined known experiment subtotalUSD0.0310742712; original429billing remains unavailable, so this is not a verified complete bill.

All eight planned successful outputs are now available across the two runs. There was
also the original failed429request, preserved separately. No successful analysis was
regenerated. No production data or app prompts changed. NTU's prior semantic-closure
concerns remain; PAN financial quality awaits Gemini. Ledger validation checks literal
evidence/structure, not full accounting accuracy. This small, unreplicated comparison
does not establish which workflow is more robust.
