# Self-Contained AI Sales Team — Design Spec

**Date:** 2026-07-16
**Status:** Approved by Jeff (brainstorming session, 2026-07-16)
**Scope:** Three releases — v2.15.0, v2.16.0, v2.17.0
**Baseline:** Plugin main @ v2.14.0 (24 skills, 8 agents). Deal Desk CLAUDE.md @ 948 lines.

---

## Problem

The Deal Desk CLAUDE.md (`CADTALK-Deal-Desk/CLAUDE.md`, 948 lines) predates most of the plugin. It now duplicates large parts of the plugin surface and loads ~25k tokens into every Deal Desk session whether needed or not:

| CLAUDE.md section (approx. lines) | Already owned by plugin |
|---|---|
| ~40 legacy `/commands` (~450) | ct-prep, ct-qualify, ct-followup, ct-proposal, ct-prospect, ct-competitors, ct-outreach, ct-report, ct-hygiene, ct-crm, ct-score, ct-commit, ct-sweep, ct-inbox |
| Pipedrive Action Reference + field-update rules (~70) | `agents/sales-crm.md` (field keys + stage IDs embedded) |
| Writing Standards (~12) | ct-voice / cadtalk-voice |
| BANT+H qualification framework (~40) | ct-qualify + ct-score |
| Competitive positioning (~40) | ct-competitors |
| Generic skill tables — `sales-skills:*`, `sales:*`, `marketing:*`, `legal:*` (~55) | Superseded by ct-* suite |

Meanwhile, several Deal Desk capabilities exist **only** in CLAUDE.md prose, so a fresh plugin install does not produce a working Deal Desk: deal-folder lifecycle, scheduled automations, content generation, contract triage, the Outline doc-ID map ("Brain index"), and the autonomy-phase model.

There is also no self-improvement mechanism: corrections Jeff makes in sessions evaporate, and the plugin's own registration drift (skills/ dir vs CLAUDE.md routing vs ct-help) is caught only by a manual TODOS checklist.

## Goal

1. **Self-contained:** fresh plugin install + `/ct-setup` produces a fully working Deal Desk.
2. **Agent-driven:** skills route, agents (sales-crm, sales-engineer, research fleet) do the work, Brain grounds claims.
3. **Token-lean:** Deal Desk CLAUDE.md drops 948 → ~80 lines; everything else loads on demand.
4. **Self-improving:** session learnings and CRM drift feed back into the plugin automatically.

## Decisions (locked with Jeff, 2026-07-16)

1. **CLAUDE.md shape:** plugin-generated thin file. Plugin owns the truth.
2. **Architecture:** **static router + local facts file** (Approach B). Plugin ships a fixed router CLAUDE.md; user facts live in a separate `deal-desk.local.md` that skills read on demand. Rejected: template mail-merge (upgrade/merge conflicts), config-JSON render script (over-machinery).
3. **Brain index:** moves to a plugin reference file (`references/brain-index.md`), loaded on demand by grounding skills. Rejected: runtime Outline fetch (per-run cost + fresh-install dependency), staying in CLAUDE.md (constant token cost).
4. **Ports into plugin:** deal-folder lifecycle, automation setup, content generation, and the deal-critical leftovers (/contract, /handoff, /council). **Dropped, no port:** /brand, /seo, /weekly — generic skills cover ad-hoc.
5. **Self-improving loop:** ct-retro + Approach C reconciliation sweep, together in one release.
6. **Phasing:** three releases — v2.15 dedupe core, v2.16 ports, v2.17 self-improvement. Each independently shippable and piloted.

---

## v2.15.0 — Dedupe core

The biggest token win and the foundation for the ports.

### 1. Router CLAUDE.md (`templates/deal-desk/CLAUDE.md`, rewritten)

Fixed ~80-line file the plugin ships and re-copies verbatim on upgrade. Contents, in order:

- **Identity** — 5–8 lines: CADTALK Deal Desk operator identity ("sales operator, not chatbot; every output ties to a Pipedrive record").
- **Skill routing table** — one row per user-facing ct-* skill (mirrors plugin CLAUDE.md routing table; single source generated from the same content).
- **Operating rules** — the 7 rules from the current file, compressed (~10 lines). These are behavioral, not data, so they stay in the always-loaded router.
- **Autonomy pointer** — 2 lines: "Autonomy phase and all workspace facts: read `deal-desk.local.md`. Phase 1 (draft-only) until that file says otherwise."
- **Facts pointer** — 1 line: skills needing pipeline IDs, pricing doc IDs, metrics, team, or brand kit read `deal-desk.local.md`.

Explicitly **not** in the router: commands, Pipedrive tool reference, writing standards, qualification frameworks, competitive positioning, doc-ID maps, metrics, team roster.

### 2. `deal-desk.local.md` (user facts file)

Written once by `/ct-setup`, never touched by plugin upgrades. Sections:

- **Autonomy phase** — current phase (1/2/3) + per-action-type unlocks (the Phase 2 "go semi-auto on X" ledger).
- **Pipelines** — the 3 revenue pipeline IDs + stage table + the reference-only pipeline list.
- **Metrics baseline** — ARR, targets, win rates, deal floor, cycle lengths (dated).
- **Team roster.**
- **Pricing doc IDs** — the 6 pricing-reference Outline IDs (user-specific; distinct from brain-index, which is sales-process content).
- **Brand kit** — Canva brand kit ID.

Format: markdown with stable `##` headings so skills can Grep a single section instead of reading the whole file. A template with empty sections ships at `templates/deal-desk/deal-desk.local.template.md`.

**Consumers (initial wiring):** sales-crm agent (pipeline IDs — verify against its embedded constants; embedded stays authoritative, local.md is the human-readable mirror), ct-report/ct-sweep (metrics, pipelines), ct-proposal (pricing doc IDs), ct-assets in v2.16 (brand kit), every write-path skill (autonomy phase).

### 3. `references/brain-index.md` (Brain index)

The ~45-row Outline doc-ID map moves from Deal Desk CLAUDE.md into the plugin. Same table shape: content → location → document ID. Includes the "pull by ID directly; search is fallback only" rule and the Sales Collection ID.

- **Loaded by:** ct-prep, ct-se, ct-proposal, ct-qualify, ct-competitors, ct-contract (v2.16), ct-outreach (persona sequences). Each gets one line added: "Grounding doc IDs: load `references/brain-index.md`."
- **Maintenance:** hand-edited in the plugin repo for now; a sync script (pattern of `sync-voice.sh`) is deferred until the index actually churns. Stale-ID risk is handled by the existing rule — if an ID 404s, fall back to Outline search and flag for correction (v2.17 ct-retro harvests these flags).

### 4. `skills/ct-deal` (deal-folder lifecycle)

New skill, three modes. All Pipedrive writes route through the sales-crm agent per the single-writer contract.

- **`new [company] [pipeline]`** — search-or-create org, create deal at Discovery via sales-crm, ZoomInfo enrich, create `deals/[CompanyName_ERP]/` + `artifacts/`, instantiate deal CLAUDE.md + MEMORY.md from `templates/deal-desk/deals/_deal-template/`, present folder path + Pipedrive URL + recommended first action.
- **`open [name]`** — locate folder, pull live Pipedrive state via sales-crm, refresh deal CLAUDE.md stage/activity lines, present delta since last session.
- **`archive [name] [won|lost]`** — final Pipedrive pull, deal summary (outcome, value, cycle length, win/loss reason, lessons) → deal MEMORY.md, move folder to `deals/_archive/[won|lost]/`, log in hub MEMORY.md. **Includes the CSM handoff package** (the old `/handoff`): contacts + personas, go-live date, Health Score, churn-risk flags, monitoring cadence — generated on `won`.

Deal-folder templates (`templates/deal-desk/deals/_deal-template/`) already exist in the repo; ct-deal is the skill that finally uses them from a fresh install.

### 5. `/ct-setup` migration + generation path

ct-setup gains a Deal Desk section (runs after connector checks):

1. **Fresh workspace:** copy router CLAUDE.md, interview for facts (autonomy phase defaults to 1, pipeline IDs, metrics, team, pricing IDs, brand kit — every question skippable, blanks allowed), write `deal-desk.local.md`, scaffold `deals/` tree.
2. **Existing fat CLAUDE.md detected** (heuristic: file > 300 lines or contains "Pipedrive Action Reference"): extract facts into `deal-desk.local.md` (present extraction for approval — Phase 1 rules apply to file surgery too), archive original to `CLAUDE.md.pre-v2.15.bak`, write router. Never delete the original.
3. **Idempotent re-run:** router re-copied (upgrade path), local.md left untouched, diff shown if router changed.

### 6. Registration

Per the TODOS 3-file checklist, for ct-deal: SKILL.md + plugin CLAUDE.md routing row + ct-help detail block. (Automated check lands in v2.17.)

---

## v2.16.0 — Ports

Ports the remaining CLAUDE.md-only capabilities so the plugin surface is complete.

### 1. `skills/ct-automate`

Scheduled-automation backbone via the scheduled-tasks MCP. Modes = the 5 automations from the old Automation Layer:

| Mode | Schedule | Runs |
|---|---|---|
| `morning-brief` | weekdays 7:00 | daily briefing (meetings, priorities, follow-ups due) |
| `stale-alert` | Mon 6:00 | stale-deal report (>14 days) |
| `pre-meeting-prep [deal]` | 24h before linked calendar event | ct-prep with inferred type |
| `weekly-council` | Sun 20:00 | council-mode ct-report (see below) |
| `deal-healthcheck [deal]` | every 7 days | activity check + health warnings |

Plus `list` (show all, flag ones that missed runs) and `remove`. ct-setup Section G (nightly sweep) folds into ct-automate as a 6th mode — one skill owns all schedules. Autonomy: schedules that only read + draft are Phase-1-safe; anything that writes routes through sales-crm and respects the phase in local.md.

### 2. `skills/ct-assets`

Content generation: `deck [type]` (Gamma default, Canva if branded), `collateral [type]` (Canva, brand kit from local.md, brand-template search first), `roi` (xlsx calculator: hours saved, error reduction, payback). Grounding structure docs (exec one-pager, business case template, battlecards) pulled via brain-index. SOW/pricing stay in ct-proposal (already there). Degrades gracefully: if Gamma/Canva connectors absent, falls back to pptx/docx skills and says so.

### 3. `skills/ct-contract`

Contract preparation: NDA triage (GREEN/YELLOW/RED), review against redline policy, risk assessment, package assembly (agreement + SOW + order form). Wraps the `legal:*` plugin skills where installed; grounding docs (redline policy, agreement template, currency policy) via brain-index. Output is always draft-for-Jeff's-review — contracts never auto-send regardless of autonomy phase.

### 4. Folds

- **/handoff** → ct-deal `archive won` path (done in v2.15; v2.16 verifies in pilot).
- **/council** → `ct-report council` mode: the 35-min agenda format (coverage, win-rate trend, stage conversion, partner attach, SDR productivity, contact capture, channel health).
- **/brand, /seo, /weekly** → dropped. Not ported, not stubbed. Generic marketing/Ahrefs skills cover ad-hoc requests.

### 5. Registration

3-file checklist × 3 new skills + ct-report mode note.

---

## v2.17.0 — Self-improving loop

Two mechanisms, one release.

### 1. `skills/ct-retro`

End-of-session (or on-demand) harvest. Three passes:

1. **Correction harvest** — scan session for: Jeff edits to skill output, rejected drafts, wrong grounding (doc-ID 404s, stale claims), tool-name drift. Each becomes a dated entry in `LEARNINGS.md` (new plugin file): *what happened → why → how to apply*, tagged by skill.
2. **TODO promotion** — recurring learnings (same tag ≥2 entries) get promoted to a TODOS.md item with context, per the existing TODOS entry format.
3. **Registration check** — automated version of the 3-file checklist: diff `skills/` directory vs plugin CLAUDE.md routing table vs ct-help detail blocks; report drift. Also verifies brain-index IDs that were flagged as 404 during the period.

**Consumption side:** plugin CLAUDE.md gains one router line — "before running a ct-* skill, if `LEARNINGS.md` has entries tagged for it, apply them." Keeps per-skill files untouched; learnings ride along until a release folds them into the skill proper (at which point ct-retro marks them folded).

**Boundary:** LEARNINGS.md lives in the plugin repo (travels with fresh installs). Personal/workspace learnings that shouldn't ship (deal-specific, Jeff-personal) go to workspace MEMORY.md instead — ct-retro asks when ambiguous.

### 2. Approach C — CRM reconciliation sweep (from TODOS)

Extension to ct-sweep, per the staged v2 design (2026-07-14 Guided Create Flow doc, Approach C section):

- Grade open-deal records against `scripts/create-contract.json` (required-by-stage fields).
- Auto-fill what conversation/context already knows; queue the rest as ask-the-rep items in the ct-inbox queue (same MD + JSON queue as v2.14).
- Retro-clean path for existing dirty deals: batch grade, present prioritized fix list, writes only through sales-crm with Phase-appropriate approval.
- Anti-nag guard: sweep runs on schedule (nightly, via ct-automate) or explicit invocation only — never auto-triggers per conversation.

**Depends on:** Guided Create Flow v1 (shipped v2.11.0) — satisfied. v2.14 pilot verdict feeds go/no-go, per TODOS.

---

## What gets deleted from Deal Desk CLAUDE.md

After v2.15 migration, the following sections exist only in the plugin (or die):

| Section | Fate |
|---|---|
| 40 legacy commands | plugin skills (existing + ct-deal/ct-automate/ct-assets/ct-contract) |
| Connected-systems + generic-skill tables | die; connectors are discoverable, ct-setup verifies them |
| Outline doc-ID map | `references/brain-index.md` |
| Pipedrive Action Reference + field rules | sales-crm agent (already authoritative) |
| Autonomy model | local.md (phase state) + router pointer |
| Pipelines/stages, metrics, team, pricing IDs, brand kit | local.md |
| Writing standards | ct-voice |
| BANT+H framework | ct-qualify/ct-score |
| Competitive positioning | ct-competitors |
| Automation layer | ct-automate |
| Operating rules, identity | router (compressed) |

## Testing & rollout

Per release: PR + CHANGELOG + ct-help update + one-week Jeff pilot (v2.14 pilot pattern).

- **v2.15 pilot metrics:** session token baseline before/after router swap (target: >20k tokens saved per Deal Desk session start); ct-deal creates one real deal folder end-to-end; migration produces a local.md Jeff signs off without edits.
- **v2.16 pilot metrics:** each automation fires on schedule once; one real deck + one ROI sheet generated; one NDA triaged.
- **v2.17 pilot metrics:** ct-retro produces ≥3 useful LEARNINGS entries in week one (Jeff-judged); registration check catches a seeded drift; sweep queue reviewed <5 min/day, zero unapproved writes (v2.14 hard rule carries over).

## Risks

- **Router too thin:** if sessions start failing to route correctly without the fat file, add rows to the routing table — not prose. The routing table is the only part of the router expected to grow.
- **local.md staleness:** metrics baseline dates itself; ct-report flags a baseline >1 quarter old.
- **Brain-index staleness:** 404-fallback rule + ct-retro flagging (v2.17). Accepted gap for v2.15–16.
- **Windows worktree gotchas** during ship (known from v2.13): ship from main checkout, not worktree, per memory.

## Out of scope

- SDR lead-conversion motion (postponed in TODOS — SDR motion inactive).
- Meeting lifecycle (v2.15 candidate in earlier planning — superseded by this plan's numbering; renumber when scheduled).
- Output-location reconciliation TODO — folded naturally: ct-deal makes deal folders the default target; per-skill prose sweep happens in v2.16 registration pass.
- Sync scripts for brain-index (deferred until churn justifies it).
