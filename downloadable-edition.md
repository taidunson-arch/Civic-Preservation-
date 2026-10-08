# Downloadable agency edition

This candidate combines the existing domain pipeline, instrument graph, four risk dimensions,
persistent case workflow and acceptance protocol with an offline review desk. The review is
generated from a completed run, not manually maintained sample rows. It is a local analyst
tool. Authentication, electronic signatures, automatic source-system updates and paid-download
entitlement enforcement are not implemented.

## Agent operating modes

Use the same evidence model across these tasks rather than creating conflicting copies of a portfolio:

- **Intake and reconciliation:** map authorized exports using `servicing-extract.md`, preserve source IDs,
  inspect rejected rows and join gaps, reconcile individual positions as well as totals.
- **Preservation review:** identify agency act-by dates separately from owner cliffs; inspect each
  date's basis and source; qualify unverified program rules and missing notices.
- **Book monitoring:** explain all four dimensions with observation date and policy version. Missing
  financial observations produce UNKNOWN; no model-generated financial facts or legal conclusions.
- **Case preparation:** use `manage_cases.py` for durable, version-checked cases. Evidence references
  must identify actual materials. The submitting and approving actor must differ, but actor strings
  do not establish authenticated independence in this edition.
- **Acceptance review:** use `validate_book.py` with independent controls, adjudicated labels and
  applicable rule reviews. Never derive an expected answer from the same output being checked.
- **Agency briefing:** export an offline internal review from a verified run; generate the existing
  public packet separately and inspect its redaction log before authorized disclosure.

Each task's handoff should identify run ID, as-of date, source limitations, unresolved exceptions,
the responsible desk and the next evidence needed. Do not declare an action completed because
a draft handoff or recommendation exists. Refer to sibling skills only if they are installed;
otherwise produce a human handoff that states the missing capability.

## Local review commands

From the distribution root, after installing the tested requirements:

```text
python civicpreserve.py doctor
python civicpreserve.py demo --out demo-run
python civicpreserve.py pipeline --config ABSOLUTE_CONFIG_PATH
python civicpreserve.py review seal --run-dir COMPLETED_RUN_DIRECTORY
python civicpreserve.py review verify --run-dir COMPLETED_RUN_DIRECTORY
python civicpreserve.py review review --run-dir COMPLETED_RUN_DIRECTORY --out NEW_REVIEW.html --db AGENCY.sqlite
```

The fixed-date demo uses synthetic fixtures, not current agency data. Every demo invocation needs
a new output directory. The review exporter refuses to overwrite a file. For agency work, set the
explicit as-of date and absolute input paths in the configuration. Read the successful run path
from `latest.json`; inspect `last_attempt.json` so a later failure is not overlooked.

The first seal establishes a local SHA-256 baseline; it cannot prove that previously modified
files were authentic. Verification catches subsequent changed, added, and removed files. It
also compares property populations, four-dimensional classifications and aggregate counts across
the result JSON and risk CSV. It does not validate every source fact or program rule. Keep the
baseline and release checksum in a separate trusted archive if independent tamper evidence is needed.

The optional case database is opened read-only and must contain the exact run manifest. It provides
current case states for properties in this run, including cases opened during earlier runs. Without
it, the review displays “Not connected.” Historical portfolio data and current case states have
different timestamps. Export another review after case changes.

The offline HTML embeds the full result and case snapshot. It contains no remote fonts, scripts,
analytics, automatic notices or online services. Its content-security policy blocks network calls,
and source text is rendered as text. Store it with the same access restrictions as the inputs.
It is not a live editing interface or a redacted public document.
