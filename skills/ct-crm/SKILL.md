---
name: ct-crm
description: Direct CADTALK Pipedrive updates — set fields, log calls, book meetings, add notes, move stages, create records, or query the pipeline. Use for 'update this deal', 'set MEDDPICC', 'log a call', 'move to Prove', 'stale deals', 'pipeline summary'.
---

# CADTALK CRM Update

Invoked as `/ct-crm <what to do>`

Direct access to CADTALK's Pipedrive for reps: field updates, activity logging,
notes, stage moves, record creation, and pipeline queries. This is the same CRM
engine every other skill writes through — so a manual `/ct-crm` update and an
automatic one from `/ct-qualify` land identically.

## How it works

This skill runs the **sales-crm contract** (`agents/sales-crm.md`). That file is
the single source of truth for CADTALK's Pipedrive field keys, option IDs, stage
IDs, and write procedures. Follow it exactly:

1. Read `agents/sales-crm.md` for the operation workflow and tool mapping.
2. Resolve field keys from `references/pipedrive-custom-fields.md` and stage/
   activity IDs from `references/pipedrive-stage-ids.md`. Never invent a key.
3. Execute the write against the connected Pipedrive MCP (tool base names mapped
   in the sales-crm contract: `updateDeal`, `addActivity`, `addNote`, etc.).
4. Confirm in one line: record, field, new value.

For a large or parallel batch of CRM operations, dispatch the sales-crm agent
(`subagent_type: cadtalk-sales-team:sales-crm`) with a structured intent instead
of running inline.

## Guided Create — `/ct-crm new` (v2.11.0)

**Every opportunity create runs this flow** — including legacy minimal phrasings
like "create a deal for Siemens in New ERP/PLM at Discovery". A minimal request
is never rejected; the flow asks for what's missing and completes.

1. **Profile.** Find `crm-profile.md` by walking up from the current folder
   through parents (stop at the home directory) — the git-config pattern, so it
   resolves from inside any deal subfolder. Not found anywhere → run the
   `/ct-setup` Section E interview and write the profile at the Deal Desk root.
2. **Motion.** Candidates are limited to the rep's profile pipelines. Infer
   from deal facts: partner involvement → Partner-sourced; existing customer
   org → Expansion or Aftermarket; net-new org evaluating ERP/PLM → New ERP/PLM.
   If the facts point outside the profile scope (e.g., an AE on a partner deal),
   offer to add that pipeline to `crm-profile.md` in-line. The inferred motion
   always appears in the Draft for correction.
3. **Assemble + validate + Draft + write** — follow the CREATE section of
   `agents/sales-crm.md` exactly: search-before-create record resolution
   (a search API error is never "no match"), ask-missing loop with the
   `⚠ unknown` escape, `python scripts/validate_create_payload.py` gate
   (required-field spec: `scripts/create-contract.json`), Draft → explicit
   Confirm, then `addOrganization` → `addPerson` → `addDeal` with SQL Date
   inside the create call when landing directly in Discovery (pipelines 1/2/3).
4. **Confirm** with record IDs and any `⚠ unknown` fields listed.

## Examples

- `/ct-crm new` — guided opportunity create (motion, all three records, zero silent blanks)
- `/ct-crm create a deal for Siemens in New ERP/PLM Prospects at Discovery` — same flow, seeded from the phrase
- `/ct-crm set MEDDPICC champion to Jane Smith (confirmed EB) on the Acme deal`
- `/ct-crm log a discovery call, done, on Contoso and set Health to Green`
- `/ct-crm move the Rockwell deal to Prove`
- `/ct-crm show me stale deals and overdue activities`

## Guardrail

If the request needs a field or stage not in the references, do not guess the
key. Look it up if a custom-fields-list tool is available, use it, and tell Jeff
so the reference can be extended. Never write a fabricated field key to Pipedrive.
