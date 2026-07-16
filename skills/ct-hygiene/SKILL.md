---
name: ct-hygiene
description: CRM hygiene guard — audits and enriches Pipedrive so every required field on deal/org/person is filled and every buying-committee contact is attached as a deal participant by close. Use for 'is this deal complete', 'audit Acme', 'enrich the CRM', 'new opportunity: [company] + contacts', 'attach participants', 'CRM gaps'.
---

# CADTALK CRM Hygiene

Invoked as `/ct-hygiene <deal | company | "all open deals">` — or automatically
(sweep after producing skills, gate before stage moves, intake on new
opportunities routed from `/ct-crm`).

**Goal:** by the time a deal closes, everything in
`scripts/hygiene-contract.json` is filled and all contacts are participants.
That JSON is the single source of truth for what "complete" means — read it;
never restate the field list. Tier and Health Score are CS-owned: never gate on
them, never write them.

## The spine (all modes)

    gather → diff → propose → confirm → write → verify

1. **Gather.** Dispatch `subagent_type: cadtalk-sales-team:sales-hygiene` with
   the deal identifier (+ run artifacts in sweep mode). It returns current
   state, proposed fills with sources, conflicts, a participants roster, and
   no-source gaps. For a quick gate check you may skip the dispatch and read
   the deal/org/persons inline via the sales-crm QUERY procedures.
2. **Diff.** Build the validator payload (logical field names; `stage` = the
   deal's current stage mapped to contract stage_order; `check` = "at" for
   audits/sweeps, "entering" for gates; flags from deal context: demo_completed,
   proposal_sent, partner_sourced, compelling_event_named; persons array;
   participants_count from `python scripts/pipedrive_participants.py list <deal_id>`
   — if the token is unset, count from the pinned Participants checklist note
   instead). Write it to a temp file and run
   `python scripts/validate_hygiene.py <file>`. Exit 0 → say "no gaps" and stop
   (sweep/audit) or proceed with the move (gate). Exit 2 → report the spec
   error; write nothing.
3. **Propose → Confirm (batch review — ONE table).** Show every gap with its
   proposed fill and source, conflicts, and no-source gaps in one table. The rep
   approves/edits ONCE. **No write before the confirm.** Inferred values only
   fill blanks — never overwrite a non-empty field.
4. **Write.** Field updates, notes, and any missing person records go through
   the sales-crm contract (`agents/sales-crm.md`; batch → dispatch
   `subagent_type: cadtalk-sales-team:sales-crm`). Person creation follows the
   create resolution rules (search first, no duplicates). Participants:
   `python scripts/pipedrive_participants.py add <deal_id> <person_ids...>`
   (idempotent). Token unset → maintain a pinned **"Participants checklist"**
   note on the deal (via sales-crm NOTE) listing who still needs manual attach,
   and tell the rep.
5. **Verify.** Re-read the records (QUERY), confirm writes landed, then report:
   filled, still-open gaps tagged `no-source` / `user-skipped` / `conflict`.
   Failed write → the fill-blanks-only rule makes a rerun safe; say exactly
   which fields landed.

## Modes

**Intake** — rep shares a new opportunity (contacts, website, partner details).
Search Pipedrive for the org, persons, and deal (sales-crm resolution rules).
Anything missing → **delegate creation to the `/ct-crm` guided create flow**
(`skills/ct-crm/SKILL.md`) — ct-hygiene never creates records directly. Then run
the spine once with the shared details as source, and attach all known
participants.

**Sweep** — dispatched as the final step of producing skills (ct-research,
ct-contacts, ct-se, ct-prep, ct-proposal, ct-commit, ct-followup, ct-qualify).
That run's artifacts are the primary source; scope the table to what the run
learned. If the deal/org can't be resolved in Pipedrive, skip silently.

**Audit** — `/ct-hygiene <deal>` runs the full spine (`check: "at"`).
`/ct-hygiene all open deals` → list open deals (sales-crm QUERY), run the diff
per deal, show a per-deal gap summary table first, then offer to run fills
deal-by-deal.

**Gate** — called by the sales-crm STAGE MOVE contract before a move (and by
mark-won). Run the diff with `check: "entering"` + the target stage ("close"
for won). Gaps → show the list, offer to fill now (spine), then ask **"move
anyway?"** — the rep can always override; record an override in the deal's
hygiene note. Never hard-block.

## Stage mapping

Contract stage_order is logical: `create, discovery, prove, propose, contracts,
close`. Map the deal's Pipedrive stage via `references/pipedrive-stage-ids.md`
(Discovery 4/9/15, Prove 5/10/16, Propose 43/11/17, Contracts 6/12/18 across
pipelines 1/2/3). Stages before Discovery map to `create`; won/lost map to
`close`. Expansions (pipeline 4): map by same-named stages; where a stage name
doesn't exist, use the nearest earlier stage.

## Boundaries

- Single-writer rule holds: every Pipedrive write goes through sales-crm.
  The ONLY exception is `scripts/pipedrive_participants.py` (participants are
  impossible via the connected MCP).
- Never overwrite non-empty fields. Conflicts are reported, not resolved.
- Tier / Health Score: CS-owned, untouchable.
- Voice: terse. A hygiene report is a punch list, not a pitch.
