# CivicPreserve — downloadable agency candidate

Preservation early warning and affordable-housing loan-book review for public-agency analysts.
This release is a **pilot candidate**, not a certified system of record or a production-ready
commercial product. It includes working software, tests, and an offline review interface.

## Install and run

Use Python 3.12 and an agency-controlled directory. Commands below work in PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-tested.txt
.\.venv\Scripts\python.exe civicpreserve.py doctor
.\.venv\Scripts\python.exe civicpreserve.py demo --out demo-run
Start-Process demo-run/review.html
```

On macOS/Linux, use `python3.12 -m venv .venv` and `.venv/bin/python` instead.
Those platforms are not verified by this release's Windows test run. Installation downloads
dependencies; the analysis and review workflow then runs locally. The package does not include
Python, a signed installer, an offline wheelhouse or model-provider credentials.

The demo runs synthetic servicing and inventory fixtures through the actual pipeline, persists
cases to SQLite, establishes an integrity baseline, and produces a browser-openable review.
Its date is intentionally fixed for reproducible testing. It is not a live data feed.

For real inputs, follow `skills/preservation-loan-book/references/downloadable-edition.md`
and the existing servicing, case and acceptance references. Use a separate directory and
database for each agency. The default rule pack concerns Oregon/Portland; it must not be
silently applied as another jurisdiction's approved policy.

## What is delivered

- Deterministic preservation calendars, instrument-level positions and covenant lineage.
- Independent preservation, financial, evidence and readiness assessments.
- Persistent, version-checked cases with evidence and separate submit/approve attribution.
- Offline property review, search, dimension filters, source detail and current case snapshots.
- Completed-run checks, cross-artifact consistency checks and local file-integrity baselines.
- Independent-book acceptance tooling and synthetic regression tests.
- A reusable agent skill at `skills/preservation-loan-book/SKILL.md`.

The skill can be copied into an agent host's supported skill directory. Merely copying it does
not install Python dependencies or approve transmitting agency information to an external model.
The Python entry point works without an AI subscription. No additional specialist agent packages
are required to run the included pipeline; optional sibling handoffs remain human work if absent.

## Verification

```text
python civicpreserve.py test
```

The test launcher uses the included historical public OHCS inventory dated 2026-10-02.
Set `OHCS_CSV` to override that location. Tests explicitly skip when that file is absent.
The public inventory is not an agency servicing tape. A green suite does not certify an agency book.
`TEST-RESULTS.txt` records the actual release checks. `RELEASE-ASSESSMENT.md` identifies sellability
gaps and provenance. `RELEASE-FILES.json` records SHA-256 file checksums, not a publisher signature.

## Commercial boundary

Do not advertise this candidate as “best in class,” regulator-approved, legally authoritative,
authenticated, multi-tenant, or calibrated on real HFA outcomes. The evidence does not support
those claims. It is suitable for technical evaluation and an authorized, supervised pilot.
No sales checkout, payment processing, license grant, download entitlement, support SLA or
commercial warranty is created by this package. Those are business decisions and release work
that remain with the publisher.
