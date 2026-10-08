# Preservation and Loan-Book Review: hfa (Oregon Housing and Community Services) — us-or-oregon-city — as of 2026-10-08

Companion files in this folder: `Oregon_City_AtRisk_Inventory.xlsx` (Summary, Board_Totals, Intervention_Queue, Preservation_Queue, Events, Agency_Calendar, Notice_Compliance, Owners_Sponsors, Sources_Vintages, Data_Gaps_Verify, Assumptions), `oregon_city_leads.csv`, `oregon_city_events.csv`, `summary.json`, `manifest.json`.

## Run Summary

- **Profile:** `hfa` — Oregon Housing and Community Services (qualified purchaser, receives PuSH notices, administers QC; per pack profile, verify).
- **Geography object:** `{mode: city_limits, city: "Oregon City", county_fips: "41005", resolution: "OHCS inventory City string", geo_grade: city_name_weak}`. No polygon join was available, so the twelve inventory rows are those whose City field reads Oregon City. All twelve carry ZIP 97045; no 97045 row carries another city name. Rows warned `city_name_weak`: all.
- **Horizon:** 10 years. Bands are months: OVERDUE < 0, CRITICAL 0–12, URGENT 12–24, APPROACHING 24–36, MONITOR 36–60, SCHEDULED 60–120, BEYOND > 120.
- **Files and vintages:** OHCS Oregon Affordable Housing Inventory export 2026-10-02 (bundled); bundled tri-county pipeline run as of 2026-10-04 (its Oregon City rows are reused where it scored them). No OHCS servicing extract, notice log, QC log or PBCA opt-out log was loaded.
- **Calendar header (verbatim from the event table):**
  `RECORDED 2 / REPORTED 12 / DERIVED 6 / ESTIMATED 2 / PROXY 0 / Suppressed 0 / Rejected 0 | helper deadlines 10 (notice arithmetic, verification due dates; not counted above) | agency act-by 10 (next 90 days 6; overdue 2) | stale contract dates flagged 2`
- **Book coverage:** none. **Degraded run:** book absent; capital factor 0 for all rows; outputs are preservation targeting and notice compliance only. ESCALATE cannot be reached without the extract and a notice log.
- **Pipeline:** the bundled `civicpreserve.py` could not execute because the repository is a flat upload (it expects `skills/preservation-loan-book/scripts/` and `plb/`). Scores labeled "tri-county run" come from the bundled 2026-10-04 run; scores labeled "analyst" were computed by hand against `affordable_public_am.json` and are diagnostics, not pipeline output.
- **Live pulls:** every direct download was denied by the session's network policy (proxy 403): hud.gov, huduser.gov, data.hud.gov, oregon.gov, data.oregon.gov, rd.usda.gov, clackamas.us, preservationdatabase.org. Web-search summaries of agency pages, news and directories were the only live channel; each is cited with its vintage in Sources_Vintages and treated as REPORTED or third-party. Nothing from a listing site is treated as a termination.
- **pii_scope:** organization. **records_classification:** internal working file, not a public packet (no Redaction_Log was produced; run the board-packet workflow before any public release).
- **Notice log:** blank for 100% of rows (none loaded).
- **Universe added beyond the inventory:** two LIHTC properties that directories and the Novoco District 5 list place inside the city but the OHCS inventory omits (Barclay Hills, Newell Creek / Stone Creek).

## Board Totals

**Book verdict:** BOOK ABSENT — not issued. **Preservation verdict for the city: STRESSED.** One 100-unit public-housing site is in an approved Section 18 disposition and will be sold; the city's largest restricted block (260 units, for-profit owner) carries an extended-use end date that conflicts with the standard 30-year term; two LIHTC properties totaling 209 units are missing from the state inventory, and one of them is being marketed at market rents.

**Headline:** 14 properties / 1,002 total units reviewed / 142 restricted units with an owner cliff inside 36 months (100 public housing, 38 HAP, 4 HAP) / 0 PRAC units inside 36 months (two PRAC dates are stale, not cliffs) / 0 PSH units / $0 public UPB at risk (book absent). Add 260 units if Kingsberry Heights' 30-year reading holds.

| owner_cliff_band | properties | units_at_risk | HAP | PRAC | other RA (public housing / PBV) | properties |
|---|---|---|---|---|---|---|
| CRITICAL (0–12 mo) | 2 | 104 | 4 | 0 | 100 | Oregon City View Manor (ESTIMATED), Our Apartment |
| URGENT (12–24) | 0 | 0 | 0 | 0 | 0 | — |
| APPROACHING (24–36) | 1 | 38 | 38 | 0 | 0 | Rosewood Terrace (OAHTC end 2029-04-01) |
| MONITOR (36–60) | 0 | 0 | 0 | 0 | 0 | — |
| SCHEDULED (60–120) | 1 | 48 | 47 | 0 | 0 | Oregon City Terrace (Year 15, 2036) |
| BEYOND (> 120) | 1 | 19 | 0 | 18 | 0 | Fisher Ridge (HDGP 2040) |
| BEYOND — Verify — Ambiguous | 1 | 260 | 0 | 0 | 0 | Kingsberry Heights (REPORTED 2044 vs DERIVED ~2026) |
| stale contract date — verify | 1 | 15 | 0 | 14 | 0 | Meadowlark (PRAC 2025-10-31) |
| no dated cliff | 3 | 39 | 0 | 0 | 10 | Housing Authority Units: Oregon City, South Leland, 144 Molalla Ave |
| no dated cliff — not in inventory | 1 | 84 | 0 | 0 | 0 | Barclay Hills |
| no dated cliff — not in inventory (possible loss) | 1 | 125 | 0 | 0 | 0 | Newell Creek / "Stone Creek Apartments at Oregon City" |
| pipeline / being preserved | 2 | 270 | 0 | 0 | 169 | Clackamas Heights (99 → 200, under construction), Las Flores (171, opened 2024) |
| **Total** | **14** | **1,002** | **89** | **32** | **279** | |

Being-preserved units: 371 (200 Clackamas Heights replacement units; 171 Las Flores). The 99 Clackamas Heights public-housing units are offline from 2025 until completion (fall 2027, ESTIMATED).

**Top sponsors by exposure (restricted units):** Housing Authority of Clackamas County 223 (OCVM 100, Clackamas Heights 99 in redevelopment, HA Units 24); Berry Heights LP / PWA-Red LLC 260 (Kingsberry); Maple OC LP 171 (Las Flores, new); unknown owners 209 (Barclay Hills, Newell Creek); Northwest Rosewood Terrace LLC 38; OCT I LP 48.

## Agency Act-By Calendar (next 90 days)

| due | property | action | owner | basis | status |
|---|---|---|---|---|---|
| 2026-01-24 | Our Apartment | HAP_OPTOUT_NOTICE_DEADLINE (expiration − 12 mo) | pbca_liaison | DERIVED | PASSED — no opt-out notice known; confirm at the CA |
| 2026-09-26 | Our Apartment | HAP_OPTOUT_PACKAGE_DUE (expiration − 120 d) | pbca_liaison | DERIVED | PASSED — confirm the HUD-9624 renewal request is on file |
| 2026-10-12 | Oregon pack | 2027 QAP public hearing — comment on a preservation set-aside (OHCS pathways reported fully subscribed) | nofa_program_manager | REPORTED | 0.1 mo |
| 2026-10-31 | Meadowlark | next expected PRAC expiration — confirm 2026-27 renewal with HUD Portland Multifamily | hud_mf_asset_manager | DERIVED | 0.8 mo |
| 2026-11-07 | Oregon City View Manor | intergovernmental request to HACC: disposition timeline, sale terms, buyer affordability covenant (if any), TPV count | nofa_program_manager | DERIVED (as_of + 30 d) | 1.0 mo |
| 2026-11-07 | Kingsberry Heights | read the recorded Declaration of Land Use Restrictive Covenants (OHCS file first, then Clackamas County Recorder); check the OHCS QC log and PuSH notice log | push_program_manager | DERIVED | 1.0 mo |
| 2026-11-07 | Newell Creek / Stone Creek | OHCS LIHTC compliance record for the 1997 project; recorder search for a LURA release or qualified-contract decontrol | compliance_officer | DERIVED | 1.0 mo |
| 2026-11-07 | Barclay Hills | OHCS LIHTC compliance record; add the row to the inventory | compliance_officer | DERIVED | 1.0 mo |
| 2026-12-01 | Oregon pack | HB 4036 (2026) report to interim committees — opportunity to name Oregon City's at-risk stock | board_liaison | REPORTED | 1.8 mo |

## Intervention Queue

Cards are grouped by primary route in precedence order. Only CRITICAL/URGENT/APPROACHING action bands get cards; the rest are summarized by band below.

### Route: notice_compliance (secondary until verified)

### [#1] Kingsberry Heights — Oregon City   Route [notice_compliance (secondary) / nofa_offer] Queue [PLAN — pending verification] Score [27.2 analyst under the 30-year reading; 6.0 under the 2044 reading] Units at risk [260] Public UPB [$0 — not in book]
- Units / HAP / PRAC / other RA / PSH: 260 / 0 / 0 / 0 / 0 (total_assumed_restricted); 93 three-bedroom units (36%) — family vulnerability flag.
- First agency act-by: LURA_VERIFICATION_DUE 2026-11-07 DERIVED — 1.0 month — owner push_program_manager — cite IRC 42(h)(6); ORS 456.766–456.819 (2025 numbering, formerly 456.250–.265) (verify).
- Owner cliff: LIHTC_EXTENDED_USE_END 2044-01-01 REPORTED (OHCS inventory) **conflicts with** ~2026-12-31 DERIVED (placed in service 1996 + 15-year compliance + 15-year extended use). Both parses stored in alt_dates; Verify — Ambiguous forces the 0.40 multiplier. The 2023 NOAH/OHCS ten-year expiring list excerpt did not show this property, which weakly supports 2044, but the recorded agreement controls.
- Declared intent / notice status / renewal status: unknown / unknown (no notice log loaded) / n/a. A 2012 sale listing was withdrawn; no QC request known.
- Our position: not in book (OHCS Funded = false; OHCS is the allocating agency and LURA counterparty only).
- Physical: no HUD inspection record (LIHTC-only); built 1996.   - Sponsor capacity: for-profit LIHTC partnership past Year 15 (2011) = 6 risk points; owner of record per OHCS list Berry Heights LP; inventory names PWA-Red LLC with an individual general partner (name withheld, organization scope).
- Intervention: push_window_prep — owner push_program_manager — cite ORS 456.781 / OAR 813-115-0030 (confirm current text) — owner notice n / tenant notice n — notice address unknown (SOS lookup blocked this session; Verify — Notice Address).
- Evidence: E-K1 2044-01-01 REPORTED inventory; E-K2 2026-12-31 DERIVED rule; E-K3 Year 15 2010-12-31 DERIVED.   - Verify before acting: the recorded LURA date; PuSH coverage of a LIHTC-only property under ORS 456.766; QC log; notice log.   - Handoffs ready: critical-dates-tracker (seed_dates with both parses; documents_to_request: LURA from OHCS file room).

### Route: optout_response

### [#2] Our Apartment — Oregon City   Route [optout_response] Queue [WATCH] Score [18.0 tri-county run] Units at risk [4] Public UPB [$0 — not in book]
- Units / HAP / PRAC / other RA / PSH: 4 / 4 / 0 / 0 / 0 (total_assumed_restricted); two-bedroom units.
- First agency act-by: HAP_OPTOUT_PACKAGE_DUE 2026-09-26 DERIVED — PASSED (−0.4 months) — owner pbca_liaison — cite 42 U.S.C. 1437f(c)(8); 24 CFR 402.8; Section 8 Renewal Policy Guide ch. 11 (verify).
- Owner cliff: HAP_EXPIRATION 2027-01-24 REPORTED (OHCS inventory); next expected expiration 2028-01-24 if renewed annually.
- Declared intent / notice status / renewal status: none known / unknown / unknown (Verify — CA Log).
- Our position: not in book. Under 5 units: no PuSH derivations (ORS 456.766 five-unit scope, verify).
- Physical: HUD inspection 85 (2018, stale).   - Sponsor capacity: Northwest Housing Alternatives (nonprofit, Milwaukie) owns; Cascade Management manages = mission sponsor 6.
- Intervention: optout_tenant_notice_check — owner pbca_liaison — first action: confirm at the CA that a renewal request (HUD-9624) is on file — owner notice n / tenant notice n — notice address: sponsor's business office (inventory; verify).
- Evidence: E-O1 2027-01-24 REPORTED.   - Verify before acting: CA log.   - Handoffs ready: none.

### Route: nofa_offer

### [#3] Oregon City View Manor — Oregon City   Route [nofa_offer / ta_sponsor] Queue [PLAN by rubric — board should read as ACT] Score [40.5 analyst] Units at risk [100] Public UPB [$0 — not in book]
- Units / HAP / PRAC / other RA / PSH: 100 / 0 / 0 / 100 (public housing, counted as other RA) / 0 (total_assumed_restricted); 1962 single-family and duplex units on 22 acres; families with children (Head Start facility on site).
- First agency act-by: AGENCY_INFO_REQUEST_HACC 2026-11-07 DERIVED — 1.0 month — owner nofa_program_manager — cite Section 18 of the 1937 Act; 24 CFR 970.9 and 970.19; 42 U.S.C. 1437f(t) (verify).
- Owner cliff: SECTION_18_DISPOSITION_SALE 2026–2027 ESTIMATED. Anchoring event: HUD Section 18 disposition approval 2024-10-31 RECORDED (per HACC's OCVM page). HACC states every household receives a tenant protection voucher, relocation was expected to begin in 2026, and the site will be sold after relocation; a June 2025 report put expected net proceeds at $12–16 million to fund Clackamas Heights. No closed sale, buyer or listing was found as of this run.
- Declared intent / notice status / renewal status: DECLARED (public plan to sell) / n/a — Section 18 is a HUD process, not a PuSH withdrawal; whether Section 9 public housing is "publicly supported housing" under ORS 456.766 is unverified / n/a.
- Our position: not in book. The OHCS inventory names the owner as "CEDAR SINAI PARK" — a data error (that is a Portland nonprofit); the owner is the Housing Authority of Clackamas County.
- Physical: HUD inspection passing 2016 (stale).   - Sponsor capacity: housing authority = mission sponsor 6; the sponsor is executing a repositioning strategy, not failing.
- Intervention: preservation_nofa_invitation to HACC or to a mission buyer for an affordable re-use of the site, plus policy engagement on sale covenants — owner nofa_program_manager — cite (above) — owner notice n / tenant notice n (HUD-governed) — notice address: HACC (Oregon City office; verify).
- Evidence: E-V1 2024-10-31 RECORDED; E-V2 2026–2027 ESTIMATED.   - Verify before acting: disposition date; sale terms; whether any affordability covenant binds the buyer; TPV issuance count; PuSH applicability.   - Handoffs ready: sponsor-credibility-assessor only if HACC or a buyer applies; off-market-deal-finder not applicable (not NOAH).
- Why the rubric under-scores it: the hfa rubric has no Section 18 line and the sale date is ESTIMATED (×0.5). Under a `pha_am` profile this row would route to recap_committee with a cliff inside 24 months. The board should treat it as the city's largest near-term hard-unit loss regardless of the score.

### [#4] Rosewood Terrace — Oregon City   Route [nofa_offer] Queue [PLAN] Score [34.6 tri-county run] Units at risk [38] Public UPB [$0 — not in book]
- Units / HAP / PRAC / other RA / PSH: 38 / 38 / 0 / 0 / 0 (reported_buckets: 38 at 60% AMI); 36 two-bedroom, 2 three-bedroom.
- First agency act-by: PUSH_WINDOW_PREP 2046-01-01 DERIVED — BEYOND; nothing due inside the horizon except sponsor outreach.
- Owner cliff: SOFT_PROGRAM_END (OAHTC) 2029-04-01 REPORTED — 29.8 months — APPROACHING. HAP_EXPIRATION 2038-05-31 REPORTED (likely a 20-year MAHRA renewal; verify term at the CA). LIHTC_EXTENDED_USE_END 2049-01-01 REPORTED (withdrawal anchor). OTHER_OHCS 2038-06-24.
- Declared intent / notice status / renewal status: none / unknown (window not open) / HAP long-term.
- Our position: OHCS Funded = true, but no extract loaded — "expected in book — join missing" cannot be evaluated; book absent.
- Physical: HUD inspection 81 (2015) after 68 (2014) — stale; roof replacement permitted 2022.   - Sponsor capacity: Northwest Real Estate Capital Corp (nonprofit, Boise, Idaho) — mission sponsor 6; inventory owner type "Housing Authority" is wrong (Verify — Owner type).
- Intervention: preservation_nofa_invitation — owner nofa_program_manager — cite ORS ch. 456/458 program statutes; IRC 42 (4%) (confirm current text) — owner notice n / tenant notice n — notice address: sponsor business office (verify).
- Reading: the OAHTC pass-through ends in 2029, which removes a rent buffer on the owner's loan; the HAP continues to carry tenant rents, so the tenant-facing risk is indirect (owner cash flow, refinance pressure).
- Evidence: E-R1 2029-04-01 REPORTED; E-R2 2038-05-31 REPORTED; E-R3 2049-01-01 REPORTED.   - Verify before acting: OAHTC loan maturity and refinance plan; HAP renewal term.   - Handoffs ready: sizing-lihtc-permanent-debt (before/after 2029) if the sponsor engages.
- Mandate fit: eligible on paper (ohcs_preservation_nofa; lihtc_4pct_gap; zero_pct_rehab_recap), but OHCS reports its 2025–27 preservation pathways fully subscribed; the 2027 QAP and the 2026-session $20 million GO bond allocation are the next openings (verify).

### Summarized by band (no card)
- **BEYOND:** Fisher Ridge (HDGP 2040) — WATCH 11.0; PRAC date 2026-02-28 is stale, next expected 2027-02-28; prac_renewal_coordination as secondary.
- **SCHEDULED:** Oregon City Terrace (Year 15 2036-05-20 DERIVED) — Monitoring 9.0; recapped 2020–21 with 9% LIHTC; HAP expiration missing from inventory.
- **Stale contract date:** Meadowlark (PRAC 2025-10-31) — WATCH 5.0; next expected 2026-10-31, inside one month; sponsor SAM registration shows "Expired" on a third-party mirror (verify). The only protection on these 15 units is the annual PRAC; no OHCS instrument exists.
- **Verification rows (not scorable):** Barclay Hills (84), Newell Creek / Stone Creek (125) — see Data Gaps.

## Book Watchlist

No OHCS servicing extract was loaded. Rows flagged OHCS Funded = true in the inventory (expected in book under the hfa profile) are: Oregon City Terrace, Rosewood Terrace, Fisher Ridge, South Leland, Las Flores. Each is `not_in_extract` (book_coverage none); none can be shown as monitored or on watch. Supply the extract to lift this section.

## Preservation Queue (not in our book)

| # | property | units | queue | score | primary route | owner cliff (basis) | band | verify |
|---|---|---|---|---|---|---|---|---|
| 1 | Kingsberry Heights | 260 | PLAN (pending) | 27.2 / 6.0 analyst | notice_compliance (secondary) | EU end 2044-01-01 (REPORTED) vs ~2026-12-31 (DERIVED) | BEYOND / CRITICAL | Ambiguous; Notice Log; PuSH Coverage |
| 2 | Oregon City View Manor | 100 | PLAN (read as ACT) | 40.5 analyst | nofa_offer | Section 18 sale 2026–27 (ESTIMATED) | CRITICAL | Owner name; Disposition date |
| 3 | Rosewood Terrace | 38 | PLAN | 34.6 run | nofa_offer | OAHTC end 2029-04-01 (REPORTED) | APPROACHING | Owner type |
| 4 | Our Apartment | 4 | WATCH | 18.0 run | optout_response | HAP 2027-01-24 (REPORTED) | CRITICAL | CA Log |
| 5 | Fisher Ridge | 19 | WATCH | 11.0 run | none | HDGP 2040-08-04 (REPORTED) | BEYOND | Stale PRAC date |
| 6 | Oregon City Terrace | 48 | WATCH (Monitoring) | 9.0 run | none | Year 15 2036-05-20 (DERIVED) | SCHEDULED | HAP date missing |
| 7 | Meadowlark | 15 | WATCH | 5.0 run | none | PRAC 2025-10-31 stale (REPORTED) | stale | Stale PRAC date; Sponsor |
| 8 | Barclay Hills | 84 | VERIFY | — | none | unknown | — | Inventory Coverage; Owner |
| 9 | Newell Creek / Stone Creek | 125 | VERIFY (possible loss) | — | none | ~2027-12-31 (DERIVED, unverified) or released | URGENT / lost | Inventory Coverage; Program Status; Lost |
| 10 | Housing Authority Units: Oregon City | 24 | EXCLUDED | 6.0 run | excluded | none dated | — | Program; Dates |
| 11 | South Leland | 10 | EXCLUDED | 6.0 run | excluded | none dated | — | Program; Dates |
| 12 | 144 Molalla Ave | 5 | EXCLUDED | 6.0 run | excluded | none dated | — | Owner; Program |

## Notice Compliance

| Req-ID | property | window | statute (verified_live: false) | status |
|---|---|---|---|---|
| PUSH-01 | Kingsberry Heights | owner first notice to OHCS and local governments 36–30 months before termination: 2041-01-01 to 2041-07-01 (REPORTED 2044) or 2023-12-31 to 2024-06-30 (DERIVED alt) | ORS 456.781 / OAR 813-115-0030 (formerly ORS 456.260(1)) | not yet due (REPORTED) or due passed with notice_status unknown (alt) — Verify — Notice Log; no demand letter until the LURA date is read |
| PUSH-02 | Kingsberry Heights | second notice 30–24 months: 2041-07-01 to 2042-01-01 (REPORTED) or 2024-06-30 to 2024-12-31 (alt) | same | as above |
| PUSH-03 | Kingsberry Heights | tenant notice 36–30 months for terminations on or after 2028-07-01 (SB 973), else 24–20 months | SB 973 (2025); OHCS PuSH-CP guide | unknown; tenant_notice_check |
| PUSH-01 | Rosewood Terrace | 2046-01-01 to 2046-07-01 (anchor 2049-01-01) | ORS 456.781 / OAR 813-115-0030 | not yet due |
| PUSH-01 | Oregon City Terrace | 2078-12-31 to 2079-06-30 (anchor 2081-12-31) | same | not yet due |
| HAP-01 | Our Apartment | owner one-year non-renewal notice by 2026-01-24 | 42 U.S.C. 1437f(c)(8); 24 CFR 402.8 | no notice known — unconfirmed; confirm renewal at the CA |
| HAP-02 | Rosewood Terrace | by 2037-05-31 | same | not yet due |
| S18-01 | Oregon City View Manor | HUD resident consultation and TPV issuance before disposition | 24 CFR 970.9, 970.19; 42 U.S.C. 1437f(t) | HUD approval 2024-10-31; not a PuSH notice — OHCS holds no statutory notice right here |

No NOTICE_COMPLIANCE_BREACH is emitted: no notice log was loaded, so `not_received_confirmed` cannot be established for any row. Unknown is not silence.

## Mandate Fit

Pack `mandate.json` lists ohcs_preservation_nofa, lihtc_4pct_gap and zero_pct_rehab_recap. Live status (REPORTED, verify): OHCS says its 2025–27 preservation pathways are fully subscribed with project commitments; the $15 million preservation pool was used for the waitlist and a 2026 LIHTC set-aside; $20 million in general obligation bonds from the 2026 session is expected ahead of a spring-2027 sale, with the 2027 QAP hearing on 2026-10-12. HB 4036 (2026), signed 2026-04-22, created the Housing Opportunity, Longevity and Durability Fund, but the enrolled text limits it to at-risk housing owned or operated by the State of Oregon. SB 5702's $25 million preservation line was not confirmed. Net: every `nofa_offer` route above is `eligible` by rule but has no open product today; record `mandate_fit: eligible — product closed (verify)`.

## Status Flips Since Last Run

Compared with the bundled tri-county run (2026-10-04):
- **new_to_list:** Barclay Hills (84), Newell Creek / Stone Creek (125) — not in the OHCS inventory.
- **recap_closed:** Clackamas Heights (financing closed late October 2025; construction under way).
- **declared intent (Section 18 sale):** Oregon City View Manor — the prior run excluded it for lack of a dated cliff.
- **re-classified:** Kingsberry Heights — EXCLUDED (no cliff in horizon) → PLAN pending verification, on the extended-use date conflict.
- **no flip:** Rosewood Terrace, Our Apartment, Fisher Ridge, Oregon City Terrace, Meadowlark.
- **lost:** none recorded. Newell Creek is flagged as a possible loss; `lost` requires termination evidence.

## Pipeline, not scored

- **Clackamas Heights redevelopment** — 99 public-housing units vacated January–August 2025 under an approved Section 18 disposition; financing closed late October 2025 (LIHTC equity, OHCS LIFT $36 million, Metro bond $17 million, Clackamas County HOME $3.5 million; TDC $124 million); demolition from November 2025; ceremonial groundbreaking 2026-06-03; completion anticipated fall 2027; 200 new affordable homes with a right of return for relocated households. Handoff: map-progress-monitor / map-troubled-project-escalator. Inventory address (8057 SE Monroe St) and status need correction.
- **Las Flores** — 171 units (70 at 30% AMI with rent assistance, 101 at 60% AMI; 12 farmworker set-asides), opened September 2024; inventory still reads "In Development" with no expiration dates. Inventory correction only.

## Data Gaps and Verification Queue

Ranked by units affected. Full table in the Data_Gaps_Verify tab.

1. **Kingsberry Heights (260):** read the recorded LURA to resolve 2044 vs ~2026. If the 30-year reading holds, the first and second PuSH owner notices were due in 2024, the tenant-notice window has passed, and the property is at or past its termination date without any notice on file. Check the QC log for a qualified-contract request.
2. **Newell Creek / Stone Creek (125):** the LIHTC directories list a 1997, 125-unit project at 14155 Beavercreek Rd; current listings market "Stone Creek Apartments at Oregon City" (110 units, built 1998) at $1,300–$2,135 with no income-restriction language and a market-rate manager. Either the restriction was released (a qualified-contract decontrol after Year 15 in 2012 would fit) or the listings are wrong. Pull the OHCS compliance record and the recorder's release, if any.
3. **Oregon City View Manor (100):** fix the owner name in the inventory; obtain the disposition timeline and sale terms from HACC.
4. **Barclay Hills (84):** add to the inventory with placed-in-service year and extended-use end.
5. **Housing Authority Units: Oregon City (24), South Leland (10), 144 Molalla Ave (5):** program, owner and dates unknown; HACC data request, OHCS file, SOS worklist. Mainstream Housing, Inc. of Eugene lists no Clackamas County property, so the 144 Molalla owner entry is suspect.
6. **Stale contract dates:** Meadowlark PRAC 2025-10-31 (next expected 2026-10-31), Fisher Ridge PRAC 2026-02-28 (next expected 2027-02-28). Neither sits in the OVERDUE row.
7. **Missing dates:** Oregon City Terrace HAP expiration; Las Flores expiration dates.
8. **Physical:** no inspection score newer than 2019 for any property (HUD data blocked).
9. **Sources still verified_live = false:** every statute and rule cite; every agency page read through search summaries.
10. **Files that would lift the queue:** OHCS servicing extract (capital factor), OHCS PuSH notice log and QC log (intent factor, notice compliance), PBCA opt-out log (HAP rows), HUD Multifamily Assistance and Section 8 tape (current HAP/PRAC dates), HUD LIHTC database and OHCS compliance list (Barclay Hills, Newell Creek), REAC/NSPIRE export.

## Assumptions, Statutory Cites and Limits

- as_of 2026-10-08; profile hfa; geography city_limits by inventory city string (city_name_weak); horizon 10 years; universe all; NOAH watch off; pii_scope organization; book absent.
- Every date carries a basis and a source; no balance was guessed for any row; no dollar figure is a book figure (none exist in this run); the OCVM proceeds estimate is a news-reported figure about HACC's own sale and is not public UPB.
- Stale HAP/PRAC dates never enter OVERDUE, never derive an agency deadline and never produce `lost`. Public housing units are counted as other RA units, never as HAP or PRAC.
- Kingsberry Heights carries two parses; the Verify — Ambiguous flag forces the 0.40 multiplier and both dates are stored. The recorded agreement controls.
- Newell Creek is not recorded as lost; `lost` requires termination evidence.
- Natural-person owner names print as "individual GP name withheld". No phone numbers, emails or tenant-level data appear in any output. This is an internal working file; the public-packet workflow (Redaction_Log, ORS 192.345/192.355 cites) has not been run.
- **Statutes (all verified_live: false — confirm current text before sending anything):** the Oregon preservation statutes were renumbered in 2025: ORS 456.250 → 456.766 (definitions), the PuSH block now runs 456.766–456.819 with 456.828 (publication); OHCS cites 456.781 (notices), 456.804 (extension for late notice), 456.814 (designee; withdrawal eligibility). The pack's templates and calendar still cite 456.250–.265, OAR 813-115, HB 2095 (2021), SB 973 (2025). SB 973 moves tenant notice to 36–30 months for terminations on or after 2028-07-01 and required OHCS rules by 2025-12-01; the OHCS PuSH-CP Instruction Guide (v1.0, 2025-09-26; page dated 2026-01-28) gives first government notice 36–30 months, second 30–24 months, tenant 24–20 months (36–30 on the new schedule), a right of first refusal that can run up to 36 months after withdrawal, and a $5,000 safe-harbor penalty cited to the old ORS 456.267. Section 18: 24 CFR part 970; TPVs 42 U.S.C. 1437f(t). HAP: 42 U.S.C. 1437f(c)(8), 24 CFR 402.8. LIHTC: IRC 42(h)(6).
- Scores are diagnostics. The deterministic pipeline did not run; a completed run is not an accepted portfolio; case completion does not legally discharge the underlying obligation. Re-run through `civicpreserve.py pipeline` once the package layout is restored and the network policy allows the HUD, OHCS and USDA hosts.
