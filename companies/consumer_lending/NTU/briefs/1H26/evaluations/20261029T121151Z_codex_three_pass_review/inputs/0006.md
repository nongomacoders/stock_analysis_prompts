# Small three-pass experiment: partial results

**Decision: clearer calculation output in NTU, but robust accuracy improvement not demonstrated. PAN comparison incomplete.**

| NTU comparison | One pass | Three passes combined |
|---|---:|---:|
| API-reported cost | $0.004702 | $0.010517 |
| Summed request seconds | 18.457 | 29.956 |
| Prompt tokens | 8675 | 27675 |
| Completion tokens | 3429 | 5602 |
| Ledger format/evidence accepted | No | Yes |
| Original question closed with sufficient evidence | No | No |

Three-pass NTU costs2.24times as much in this sample. It shows useful percentage movements, but an early scope mistake survives and the final answer still closes a question whose total reconciliation is pending. The single-pass answer also gets the impairment direction right. A valid ledger is not a correct answer.

PAN completed its dictionary and calculation passes, then its why pass failed HTTP429Too Many Requests. The planned fresh single-pass PAN call was not dispatched. Do not compare an unfinished pipeline against historical answers as if it were a complete controlled pair.

Seven requests dispatched, six completed, one rate-limited; eight planned. Known API cost subtotal **$0.02158995**, failed-call cost unavailable. Overall dispatch-to-last-accounting **94.86s**. Stop occurred as planned; no paid retry. The failed request supplies no evidence of which specific quota caused429.

**Recommendation:** keep this as an experiment. First review whether a source-grounded term table and final closure check can prevent earlier model mistakes being inherited. Do not adopt three calls across the app or treat more detailed prose as verified analysis. Manual Gemini handoff in gemini/review_prompt.md; no further paid calls made.
