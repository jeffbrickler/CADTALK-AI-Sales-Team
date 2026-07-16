---
name: ct-deal
description: Deal-folder lifecycle — create, open/sync, or archive a CADTALK deal. Use for 'new deal', 'start a deal for [company]', 'open the [company] deal', 'archive [company] won/lost', CSM handoff.
---

# CADTALK Deal Lifecycle

Invoked as `/ct-deal <mode> <company> [args]`. Modes: `new`, `open`, `archive`.
If no mode is given, infer it: an unknown company → `new`; a known deal folder →
`open`; the words "won"/"lost" present → `archive`.

This skill manages the **deal folder** (the local context hub) and keeps it in
sync with Pipedrive. Every Pipedrive write goes through the sales-crm single-writer
contract — this skill never calls a Pipedrive write tool with a hand-built key.

## CRM writes — through sales-crm only

When Pipedrive is connected, all record creates/updates follow `agents/sales-crm.md`
(or dispatch `subagent_type: cadtalk-sales-team:sales-crm`). Field keys resolve from
`references/pipedrive-custom-fields.md`; stage IDs from `references/pipedrive-stage-ids.md`.
Respect the autonomy phase in the Deal Desk's `deal-desk.local.md` (default Phase 1:
propose the create/move for approval before executing).

## Resolving the Deal Desk root

Deal folders live under `<Deal Desk root>/deals/`. Find the root by walking up from
the current directory to the folder containing `deal-desk.local.md` (or `crm-profile.md`).
If neither is found, tell the user to run `/ct-setup` first.

---

## Mode: new — `/ct-deal new <company> [pipeline]`

Pipeline aliases: `aftermarket` (1), `new-erp` (2), `expansions` (4). Default:
`aftermarket` unless the company is clearly a partner-led ERP deal.

1. **Org record.** Search Pipedrive for the org (sales-crm read). If none, create it
   (sales-crm) — propose for approval under Phase 1.
2. **Deal record.** Create the deal in the chosen pipeline at Stage 1 (Discovery)
   via the sales-crm STAGE MOVE / create contract. Owner = the rep's Pipedrive Owner
   ID from `crm-profile.md`.
3. **Enrich.** Run ZoomInfo `account_research` on the company; capture revenue,
   headcount, industry, and any CAD/ERP signals for the folder.
4. **Folder.** Create `deals/<CompanyName_ERP>/` and `deals/<CompanyName_ERP>/artifacts/`.
   Derive `<CompanyName_ERP>` as the company name (spaces → underscores) + `_` + the
   target ERP if known, else just the company name.
5. **Deal CLAUDE.md.** Copy `deals/_deal-template/CLAUDE.md` into the new folder and
   fill: company, target ERP, Pipedrive deal ID, pipeline, stage (Discovery), value
   if known, creation date, any contacts found.
6. **Deal MEMORY.md.** Copy `deals/_deal-template/MEMORY.md` (empty) into the folder.
7. **Present:** the folder path, the Pipedrive deal URL, and the recommended first
   action — `/ct-prep <company>` (discovery) or `/ct-research <company>` if research
   is thin.

## Mode: open — `/ct-deal open <company>`

1. Locate the deal folder under `deals/` by name match (case-insensitive, allow the
   `_ERP` suffix). If several match, list them and ask which.
2. Pull the current deal record from Pipedrive (sales-crm read): stage, value, last
   activity, next activity, owner.
3. Refresh the deal's CLAUDE.md — update the stage line, value, last/next activity.
   Leave hand-written context sections (Pain, Competition, Next Step) untouched.
4. Present the current state and **what changed since last session** (stage moves,
   new activities, value changes).

## Mode: archive — `/ct-deal archive <company> <won|lost>`

1. Pull the final deal record from Pipedrive (sales-crm read).
2. Write a **deal summary** as the final MEMORY.md entry: outcome, final value,
   cycle length (created → closed), win/loss reason, and 2–3 lessons.
3. **On `won`, also generate the CSM handoff package** (this replaces the old
   `/handoff`): key contacts with buying persona, ERP go-live date, implementation
   partner, Health Score, churn-risk flags, integration scope, Phase-2 flag, and a
   monitoring cadence — High risk = weekly, Medium = bi-weekly, Standard = monthly.
   Save it as `artifacts/handoff.md` in the deal folder and present it.
4. Move the deal folder to `deals/_archive/<won|lost>/`.
5. Append a one-line archive record to the Deal Desk root `MEMORY.md`
   (company, outcome, value, date).
6. If Pipedrive still shows the deal open, propose the sales-crm status update
   (`won`/`lost`) for approval — do not execute silently.

---

## Output location

All deal artifacts go in the deal folder (`deals/<CompanyName_ERP>/` and its
`artifacts/` subfolder) — never the current working directory. This is the canonical
target every downstream skill (`/ct-prep`, `/ct-se`, `/ct-proposal`) writes to.

## Common mistakes

- Creating the Pipedrive deal outside the sales-crm contract — always route writes
  through it so the record looks identical to every other rep's.
- Executing a create or stage move under Phase 1 without approval — propose first.
- Overwriting hand-written deal context on `open` — only refresh the status lines.
