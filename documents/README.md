# Source registry

`registry.json` records the current starting report. Original bytes remain in `company_results/`; do not rename, rewrite or annotate them in place.

The PAN FY2026 hash, byte size and physical-page count were computed from the local file during setup. The company, reporting period and description come from the user handoff and have that provenance recorded. Other existing reports have not yet been registered or evaluated.

Before a run, recompute the source SHA-256. If bytes differ, register a new document version and preserve the earlier identity. Physical pages are 1-based; printed labels are independent strings, never arithmetic offsets.
