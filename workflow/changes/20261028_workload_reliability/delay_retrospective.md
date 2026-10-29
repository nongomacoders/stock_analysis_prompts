# Delay review — 2026-10-28

The saved evidence attributes the long run to the size of the live trial, repeated
ledger-contract failures, completion exhaustion, debugging/resumption and repeated
test runs. No telemetry-related approval rejection appeared in the visible tool
results for this implementation/rerun sequence. Earlier project records describe
separate telemetry-related interruptions; they must not be assigned to this run.

## Measured evidence

| Measure | NTU | DCP |
| --- | --- | --- |
| Fresh captures | 9 | 84 |
| Successful saved model receipts | 17 | 124 |
| Successful ledger-repair receipts | 6 | 38 |
| Sum of recorded call-wrapper time | 373.44 s | 1,961.15 s |
| First request to last saved receipt | 1,996.07 s | 3,244.56 s |

DCP ran approximately 10:20–11:14 SAST: about 54 minutes, with about 33 minutes
inside recorded successful call wrappers. NTU's full Stage 2 separately exhausted
65,536 and 98,304 completion ceilings, without a completed answer. Failed calls
without receipts add unmeasured time/usage. Recorded call durations can include
retries. The companies ran concurrently; durations cannot be added into wall time.

Nine pytest invocations totalled 551.14 seconds (about nine minutes) of process
runtime, overlapping model work. Repeated fixture fixes, prompt/context changes,
runner repairs and interrupted-run recovery extended the elapsed run. The exact
timestamp of the user's stuck question is unavailable to the receipt analysis;
these figures describe the completed trials, not a claimed exact pre-question total.

## Telemetry interpretation

The commands set `DOTNET_CLI_TELEMETRY_OPTOUT=1` and
`POWERSHELL_TELEMETRY_OPTOUT=1`. These are opt-out settings, not commands to send
telemetry. Microsoft documents these values at:

- https://learn.microsoft.com/en-us/dotnet/core/tools/telemetry
- https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_telemetry?view=powershell-7.5

Important limitation: Microsoft's PowerShell documentation says its opt-out must
be present **before the PowerShell process starts**. Setting it inside an already
started exec command does not establish that startup telemetry was disabled.
The Python audit hook blocked Python DNS/connect/sendto operations during tests,
not all host/shell traffic. No packet trace was collected. Therefore this review
does not prove that no telemetry occurred, or exclude a small contribution; it
finds no evidence that telemetry explains the long reruns. No telemetry/settings
or permission changes were made for this review.

## Execution mistakes and future method

The live comparison was too large before the new ledger protocol was proven.
Instead of validating one or two sections and stopping on recurring protocol
failure, the process became an extended live debugging loop. Increasing completion
budgets did not fix ledger growth. Editing runners during other dispatches also
made traceback source lines harder to interpret. The earlier reassurance that the
agent was not stuck understated the repeated failure/recovery cycle.

For future trials:

1. Test captured failures offline and run a one/two-section live pilot first.
2. Expand to full company comparisons only after the pilot demonstrates valid,
   bounded handoffs; report expected section/call counts before broad dispatch.
3. Allow one repair per failing unit; recurring failures stop the broad trial for
   diagnosis instead of expanding budgets or continuing repair loops.
4. Use targeted tests during small fixes and a full suite at a coherent milestone.
5. Dispatch immutable runner copies and preserve exact requests and receipts.
6. Report failure counts, actual stage and remaining work plainly; distinguish
   active debugging, remote inference, completed output and incomplete recovery.
7. Treat launch-time telemetry opt-out and observed approval/network errors
   separately; do not disable the managed proxy or permission checks on suspicion.

Reproduction: `delay_retrospective.py` reads saved receipts only and exits 0.
Its output is `delay_retrospective.json`. No paid models or application tests were
rerun for this review; production code and financial evidence were unchanged.
