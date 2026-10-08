# Release assessment — 2026-10-06

## Blunt verdict

The source contains valuable agency analysis and integrity work. It does not yet justify selling
an autonomous public-agency system of record. A polished dashboard, more agent personas, and a
large passing test count cannot supply missing agency validation, identity controls, or support.
The defensible near-term product is a local analyst decision-support download with supervised
onboarding, a bounded jurisdiction pack, and a documented acceptance process.

## Provenance and actual integration

The Cursor session `bc-10048060-0632-44c8-8e4b-b8e6881c94c9` was read in the browser. It advocates
the domain model, Codex integrity/instrument/case/validation stack, and an agency-first interface.
It acknowledges a static UI and missing institutional controls. Its statements about changes
being pushed to main were not borne out by the GitHub main fetched during this build:
`3326ebd236f48c4662e2e303700a2c3d211824db` still contains the legacy application.

This candidate is based on fetched `origin/codex/agency-validation` at
`fb3eb3c80a95b076980f1ddc8697e1b965eac7be`, which contains the stacked agency work. The previous
output manifest identifies the earlier integrity release at `fe9b6cdad41292f75550842a7ab2ce61af34bcb8`.
The older operations and acceptance outputs were used as context. Their claims were not treated
as new authorization or as proof of current tests.

The new review interface implements the Cursor session's agency-oriented design direction from
actual pipeline artifacts. It does not claim to include the unavailable Cursor frontend source.
No remote branch was merged or published by this build. The download excludes the buyer-oriented
root application and the sibling off-market skill.

## Improvements implemented in this candidate

One command builds a labeled synthetic demonstration from the actual pipeline. The offline
review separates all four risk dimensions, sorts agency act-by before owner cliff, exposes
underlying evidence and positions, and optionally reads matching case states from SQLite.
It visibly distinguishes no database from no cases. It rejects incomplete or inconsistent runs.
SHA-256 baselines detect subsequent file changes, including extra or missing files; resealing
an altered run is refused. Embedded source markup is escaped and never evaluated as instructions.
A strict browser content-security policy disallows network calls. The agent workflow explicitly
separates supplied-document instructions from user authorization and declines unsupported claims.

## Release gates before broad paid availability

| Gate | Evidence required | Present state |
|---|---|---|
| Real-book accuracy | Independently controlled servicing tape; position-level reconciliation; adjudicated missed-risk and false-alert results across periods | Not supplied; not established |
| Jurisdiction and program authority | Applicable, effective-dated rule reviews signed off by authorized agency reviewers/counsel; change process | Validation tooling exists; approval not established |
| Security and privacy | Threat model, approved data flow, independent security assessment, least-privilege deployment and tested recovery | Local trusted-workspace boundary only |
| Identity and approvals | Authenticated actors, enforced roles, independently verified approval and controlled audit retention if sold for multiuser operations | Actor strings and local SQLite; insufficient for this claim |
| Procurement usability | Staff usability trials, accessibility evaluation, installation trials on target agency machines | Technical local review; no formal accessibility claim |
| Commercial distribution | Rights review, chosen license terms, signed release, dependency inventory/audit, installer/update policy, support owner and entitlement policy | Source candidate and checksums only |
| Operations | Backup/restore exercises, retention settings, rollback and incident/support procedures exercised with agency IT | Not established |

A per-download purchase is a pricing mechanism, not a trust model. Do not collect an agency's
servicing tape merely to enforce a license. Decide whether the sale covers a named user, an agency,
a version, updates or support before implementing entitlement checks. No pricing or contractual
terms have been invented here.

## Limits of the new controls

The integrity baseline is locally generated and unsigned. An attacker able to replace both data
and the baseline can defeat it. The review's case data are a snapshot, not live writes. The full
result is embedded, so it must be protected as internal data even when names are not visible in
the initial table. Existing CSV/XLSX outputs and their downstream spreadsheet behavior require
their own security review; the HTML safety tests do not certify every output format.

No third-party code-security audit, legal certification, real-agency outcome study, formal
accessibility conformance test, commercial license review or production incident exercise was
performed in this build. Never describe the test results as those assurances.
