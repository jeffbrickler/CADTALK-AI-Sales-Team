# CS Fields Out of CREATE Contract + Sweep Pipeline Scoping — Design

**Date:** 2026-07-16
**Trigger:** Jeff's sample `/ct-sweep` run (a) flagged Tier and Health Score as
missing deal fields, and (b) pulled deals from every pipeline. Tier and Health
Score are CS-owned — sales reps never fill them. Sweeps should be scopable to
the pipelines a rep actually works.

## Root causes

1. **CS fields flagged.** The hygiene contract (`scripts/hygiene-contract.json`,
   `excluded` list) already excludes Tier and Health Score, so hygiene proper
   never flags them. But `scripts/create-contract.json` still lists both in
   `records.deal.required`, and `/ct-sweep` Step 3b (reconciliation grade)
   checks every open deal against the CREATE contract — that is where the flags
   came from. The same required list also makes `/ct-crm new` (Guided Create
   Flow) demand Tier and Health Score from reps at deal creation.

2. **All pipelines swept.** `scripts/pipedrive_read.py` already filters by
   `--pipelines <ids>`; the sweep reads those IDs from the rep's
   `crm-profile.md` (written by `/ct-setup pipelines`). The sample run pulled
   everything because the profile listed all pipelines (or the run bypassed the
   profile). There is no way to scope a single run today.

## Decisions (Jeff, 2026-07-16)

- Remove Tier + Health Score from the CREATE contract entirely (not just the
  sweep reconciliation). One source of truth; consistent with the existing
  hygiene exclusion and the 2026-07-15 "CS-owned" ruling.
- Sweep pipeline selection: argument override, interactive ask, profile
  default — in that order.

## Change 1 — CS fields out of the CREATE contract

**File: `scripts/create-contract.json`**
- Remove `"Tier"` and `"Health Score"` from `records.deal.required`.
- Add both to `excluded_at_create`, with a comment marking them CS-owned
  (confirmed 2026-07-15/16): never required, never gated, never written by any
  rep-loop skill. Reads may still SURFACE them (sales-crm read path, ct-commit
  Health Score cross-check) — those consume CS data, never require or write it.

**Ripple (automatic — these consume the JSON, no code change):**
- `/ct-sweep` Step 3b reconciliation stops flagging Tier / Health Score.
- `/ct-crm new` Guided Create Flow stops asking for them.
- `scripts/validate_create_payload.py` loads the contract dynamically — logic
  untouched.

**Manual updates required:**
- `scripts/test_validate_create_payload.py` — tests currently assert Tier is
  required (payload fixtures, missing-field cases, `_unknown` cases). Rewrite
  those cases against a field that remains required (e.g. Forecast Category).
- `scripts/validate_create_payload.py` docstring example uses
  `"_unknown": ["Tier"]` — swap for a still-required field.

**Out of scope / unchanged:**
- `scripts/hygiene-contract.json` already excludes both — no change.
- `skills/ct-commit` Health Score cross-check — read-only consumer, unchanged.
- `agents/sales-crm.md` read-path mention of Tier/Health Score — reads are
  fine, unchanged.

**Jeff's action item (outside the plugin):** the contract carries a sync rule
with Pipedrive's native required-fields configuration (eng review T1-A). Ensure
the Pipedrive web UI does not require Tier or Health Score at deal creation.

## Change 2 — Sweep pipeline scoping

**File: `skills/ct-sweep/SKILL.md`** — Step 1 gains a pipeline-resolution rule:

1. **Argument given** — `/ct-sweep New ERP`, `/ct-sweep 1,2`, or mixed. Names
   map to IDs via `crm-profile.md` first, then
   `references/pipedrive-stage-ids.md`. Use exactly the resolved IDs.
2. **No argument, interactive** — list the pipelines from `crm-profile.md` and
   ask which to sweep; the full profile set is the default answer.
3. **No argument, headless/nightly** — use `crm-profile.md` as today. No
   behavior change for scheduled runs.

**Error handling:**
- Unresolvable pipeline name/ID in the argument — interactive: re-ask showing
  the valid list; headless: fall back to the profile set and record the fallback
  in the queue MD header.

**Queue header:** the `REVIEW-QUEUE-{date}.md` header line states which
pipelines were swept (names + IDs), so scope is visible at a glance in
`/ct-inbox`.

**Unchanged:**
- `scripts/pipedrive_read.py` — `--pipelines` already exists; no script change.
- `/ct-inbox`, `/ct-automate` — nightly scheduled runs keep using the profile.

**Separate from the plugin:** Jeff re-runs `/ct-setup pipelines` once to trim
his `crm-profile.md` to sales pipelines only — that fixes nightly scope
immediately, independent of this release.

## Testing

- `test_validate_create_payload.py` updated cases pass; full suite green.
- No new script surface: the sweep change is skill-doc only, exercised by the
  next sample sweep run.

## Files touched

| File | Change |
|---|---|
| `scripts/create-contract.json` | Tier + Health Score: required → excluded_at_create |
| `scripts/test_validate_create_payload.py` | re-anchor Tier-based cases on a still-required field |
| `scripts/validate_create_payload.py` | docstring example only |
| `skills/ct-sweep/SKILL.md` | Step 1 pipeline resolution + queue header line |
