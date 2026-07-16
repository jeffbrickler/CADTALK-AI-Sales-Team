# CRM Hygiene — Design Spec

**Date:** 2026-07-15
**Target release:** v2.12.0
**Status:** Approved by Jeff (interactive design session)

## Problem

Research and call intelligence produced by the AI sales team never lands in Pipedrive.
`/ct-research`, `/ct-contacts`, `/ct-competitors` generate org tech-stack, buying-committee
maps, and person data that stay in Deal Desk files. `scripts/create-contract.json` marks
MEDDPICC, feedback, and SQO fields as "fill later," but nothing guarantees later happens.
The Pipedrive MCP connector cannot attach deal participants, so multi-threading is graded
(`ct-score` WGLL: 4+ participants) but never written.

**Goal:** by the time a deal closes, every required field on the deal, organization, and
person records is filled, and every buying-committee contact is attached to the deal as a
participant.

## Decisions (confirmed with Jeff)

| Question | Decision |
|---|---|
| Triggers | All four: new-opportunity intake, post-skill sweep, on-demand audit, stage-move gate |
| Participants | Direct Pipedrive API via `PIPEDRIVE_API_TOKEN` (Jeff will set env var); checklist-note fallback if unset |
| Sources | Deal Desk files, Fireflies transcripts, live web re-research (in that order) |
| Deal fields required by close | All 9 MEDDPICC, Forecast Category, Compelling Event + Compelling Event Date, SQL Date, SQO Date, EB Last Direct Touch, Feedback on Demonstration + Feedback on Proposal (when demo/proposal happened) |
| Tier + Health Score | CS-owned. Hygiene never gates on them, never writes them. Remove rep ownership from the per-stage contract in `agents/sales-crm.md` |
| Org fields required by close | Source System + Target System, Org Type + Label + Owner, firmographics (revenue range, employee count, industry, website, LinkedIn). Fit scores NOT required |
| Person fields | Tiered: key contacts (Economic Buyer, Champion, primary contact) get full enrichment (email, phone, job title, Role enum, LinkedIn); all others get name + email + Role |
| Participants standard | Everyone surfaced by calls or research gets a person record and is attached; minimum 4 flagged; partner reps attached too |
| Gate mode | Warn + confirm — show gaps, attempt auto-fill, then "move anyway?" override |
| Write model | Batch review: one table of field → proposed value → source; Jeff approves/edits once, then all writes execute |
| Command structure | Two skills, one front door: `/ct-crm` routes hygiene-shaped requests to `ct-hygiene`; hooks and stage-gate invoke `ct-hygiene` directly |

## Architecture

Single-writer rule preserved: **all Pipedrive writes route through the `sales-crm` agent.**
The only exception is participant attach, which the MCP connector cannot do — handled by
`scripts/pipedrive_participants.py` using the API token.

### New files

| File | Purpose |
|---|---|
| `skills/ct-hygiene/SKILL.md` | Orchestrator with four modes (intake, sweep, audit, gate) |
| `agents/sales-hygiene.md` | Read-only gather/extract agent: pulls Pipedrive state, Deal Desk files, Fireflies transcripts, live web; outputs field → proposed value → source table. Never writes |
| `scripts/hygiene-contract.json` | Machine-readable required-by-close spec (pattern mirrors `create-contract.json`) |
| `scripts/validate_hygiene.py` | Gap computer: current record JSON + contract + stage → gap list. Exit codes: 0 complete, 1 gaps, 2 spec error (same semantics as `validate_create_payload.py`) |
| `scripts/test_validate_hygiene.py` | Validator tests |
| `scripts/pipedrive_participants.py` | `list <deal_id>` / `add <deal_id> <person_id>` via REST API; idempotent; dry-run mode |

### Edited files

| File | Edit |
|---|---|
| `agents/sales-crm.md` | STAGE MOVE op gains gate step (invoke ct-hygiene audit; warn + confirm). Remove Tier/Health from per-stage rep contract |
| `skills/ct-crm/SKILL.md` | Front-door routing: completeness/audit/enrichment asks → ct-hygiene |
| 8 producing skills (`ct-research`, `ct-contacts`, `ct-se`, `ct-prep`, `ct-proposal`, `ct-commit`, `ct-followup`, `ct-qualify`) | Final step: run ct-hygiene sweep with this run's artifacts as source |
| `skills/ct-setup/SKILL.md` | Setup step for `PIPEDRIVE_API_TOKEN` + `PIPEDRIVE_DOMAIN` (Pipedrive → Personal preferences → API) |
| `CLAUDE.md` | Skill Routing table: add ct-hygiene row |

## Data flow (shared spine, all modes)

```
gather → diff → propose → confirm → write → verify
```

1. **Gather** (`sales-hygiene` agent): read current Pipedrive records (MCP read tools),
   Deal Desk files for the account, Fireflies transcripts, live web only for org
   firmographics still missing. Every proposed value carries its source
   (file path / call title+date / URL).
2. **Diff** (`validate_hygiene.py`): compare Pipedrive state against the contract for the
   deal's current stage. Each contract field has `due_by_stage`; close gate = everything due.
3. **Propose/confirm:** one batch table — field, current value, proposed value, source.
   Jeff approves or edits once.
4. **Write:** `sales-crm` agent executes field updates and notes; participants script
   attaches people. **Inferred values only fill blanks — never overwrite a non-empty
   field.** Conflicts (Pipedrive says X, source says Y) are flagged in the table, not written.
5. **Verify:** re-read records, confirm writes landed, report residual gaps with reasons
   (`no-source`, `user-skipped`, `conflict`).

### Modes

- **Intake** — Jeff shares contacts + website + partner details for a new opportunity.
  Search Pipedrive for org/persons/deal; anything missing is created by **delegating to
  ct-crm's guided create flow** (ct-hygiene never creates records directly); then run the
  first sweep and attach all known participants.
- **Sweep** — invoked as the final step of producing skills; that run's artifacts are the
  primary source. Small, fast, scoped to what the run learned.
- **Audit** — `/ct-hygiene [deal]` or `all open deals`: full gap report per deal, then the
  shared spine to fill what sources can fill.
- **Gate** — invoked by sales-crm STAGE MOVE: run audit for the target stage's due set;
  show gaps; attempt fill; ask "move anyway?".

## hygiene-contract.json shape

```json
{
  "deal": [
    {"field_key": "…", "name": "Champion (MEDDPICC)", "due_by_stage": "prove",
     "applies_when": "always"},
    {"field_key": "…", "name": "Feedback on Demonstration", "due_by_stage": "propose",
     "applies_when": "demo_completed"},
    {"field_key": "…", "name": "Partner Contact", "due_by_stage": "discovery",
     "applies_when": "partner_sourced"}
  ],
  "organization": [ … ],
  "person": {
    "key_roles": ["economic_buyer", "champion", "primary"],
    "key_required": ["email", "phone", "job_title", "role", "linkedin"],
    "other_required": ["name", "email", "role"]
  },
  "participants": {"min": 4, "include_partner": true, "source": "calls_and_research"},
  "excluded": ["tier", "health_score"]
}
```

Field keys come from `references/pipedrive-custom-fields.md`; stage names map to IDs via
`references/pipedrive-stage-ids.md`. `applies_when` conditions: `always`,
`demo_completed`, `proposal_sent`, `partner_sourced`.

## Participants script

- Env: `PIPEDRIVE_API_TOKEN`, `PIPEDRIVE_DOMAIN` (e.g. `cadtalk.pipedrive.com`).
- REST: `GET/POST /v1/deals/{id}/participants`.
- Idempotent: `add` skips persons already attached.
- `--dry-run` prints what would change.
- Token unset → exit with clear message; skill falls back to maintaining a pinned
  "Participants checklist" note on the deal and asks Jeff to attach manually.

## Error handling

- Fireflies or web unavailable → proceed with remaining sources; mark unfillable gaps `no-source`.
- Validator spec error (exit 2) → abort before any write.
- Partial write failure → verify step reports exactly which fields landed; rerun is safe
  (fill-blanks-only makes writes idempotent).

## Testing

- `test_validate_hygiene.py`: gap math per stage, `applies_when` conditions, tiered person
  rules, participant floor, excluded fields never flagged.
- Participants script `--dry-run` against a known deal.
- `scripts/validate-plugin.py` passes after all file additions.
- Manual E2E: run audit on one real open deal; confirm batch table sources are accurate
  before approving writes.

## Out of scope

- CS/billing/renewal fields (per `references/pipedrive-custom-fields.md` scope note).
- Tier + Health Score (CS-owned).
- Lead records (deals only).
- Scheduled/cron sweeps (can be added later via /loop or scheduled tasks; not in v2.12.0).
