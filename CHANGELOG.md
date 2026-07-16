# Changelog

All notable changes to CADTALK AI Sales Team are documented here.

---

## v2.12.0 — 2026-07-15

CRM Hygiene. Guarantees the required-by-close field set and participant attachment across every deal, closing the gap between a field existing in Pipedrive and it actually being filled in before close.

### Added
- **`/ct-hygiene`** skill — intake / sweep / audit / gate modes; guarantees the required-by-close field set and participant attachment. `/ct-crm` fronts hygiene-shaped requests.
- **`sales-hygiene` agent** — read-only gatherer (Pipedrive state, Deal Desk files, Fireflies transcripts, live web) producing sourced fill proposals.
- **`scripts/hygiene-contract.json`** + **`scripts/validate_hygiene.py`** (+tests) — machine-readable required-by-close spec and stage-dueness gap computer.
- **`scripts/pipedrive_participants.py`** (+tests) — deal participants via REST (the connected MCP has no participant tools); idempotent, dry-run, checklist-note fallback when no token. `/ct-setup` Section F sets it up.

### Changed
- **`agents/sales-crm.md`** — STAGE MOVE now runs the hygiene gate (warn + confirm, never hard-block); PARTICIPANTS operation documented; Tier + Health Score moved to CS ownership (removed from the per-stage rep contract).
- 8 producing skills (research/contacts/se/prep/proposal/commit/followup/qualify) end with a hygiene sweep so run intel lands in Pipedrive.

---

## v2.11.0 — 2026-07-14

The Guided Create Flow: every new opportunity stamps three records (Deal + Organization incl. CAD/ERP systems + Person incl. Role) with zero silent blanks. Per-user pipeline profiles make the flow motion-aware for each rep. Design doc: `AzureAD+JeffBrickler-remove-ct-cro-design-20260714-164928.md` (office-hours + eng review, ENG CLEARED).

### Added
- **`scripts/create-contract.json`** — the single machine-readable source of truth for required-at-create fields (logical names only; hash keys stay in the vendored references). Sync rule: changes here must be mirrored in Pipedrive's native required-fields config.
- **`scripts/validate_create_payload.py`** — deterministic guard the sales-crm writer runs before any create; rejects incomplete payloads listing ALL missing fields; `⚠ unknown` escape for non-hard fields; fail-closed prose fallback if Python breaks post-setup.
- **`scripts/test_validate_create_payload.py`** — 24 pytest cases covering every validator path (pytest is now the repo's test convention; dev dependency).
- **`/ct-crm new`** — guided opportunity create: profile walk-up, motion detection within the rep's pipeline scope, search-before-create dedup (search error ≠ no match), ask-missing loop, Draft → Confirm, ordered `addOrganization` → `addPerson` → `addDeal` with partial-failure retry + reconcile notes. Legacy minimal phrasings enter the flow instead of erroring.
- **`crm-profile.md` per-user profile** — `/ct-setup` Section E interviews pipelines (live `getStages` cross-checked against the vendored stage-ids ref) + Pipedrive Owner ID (own-deal lookup, or guided Settings→ID copy for new reps with zero deals); written at the Deal Desk root; `/ct-setup pipelines` re-runs it. Config varies scope, never schema.

### Changed
- **`agents/sales-crm.md` CREATE section** rewritten to the three-record contract; SQL Date now stamps INSIDE the `addDeal` call for deals created directly into Discovery (pipelines 1/2/3) — atomic, no two-call gap.
- **`/ct-setup`** — Python promoted from optional to REQUIRED (validator self-test gates setup completion); PDF/reportlab stays optional.
- **ct-prospect / ct-qualify** — opportunity creates route through the Guided Create Flow; research/qualification facts seed the payload.

### Ops (Jeff, one-time)
- Configure Pipedrive-native required fields per stage/pipeline to mirror `create-contract.json` (zero-code enforcement floor covering manual web-UI creates). Verify plan-tier support.

---

## v2.10.0 — 2026-07-14

The plugin is for people who sell. The v2.6.0 leadership module was CRO-task tooling (forecasting, sales-model design, pricing, NRR, quota/capacity, board reporting) — the wrong audience for a rep-facing sales team, so it's gone. Deal coaching is unaffected and stays clearly labeled as coaching.

### Removed
- **`/ct-cro`** revenue-leadership module (`skills/ct-cro/SKILL.md`)
- **CRO references** — `references/cro-sales-playbook.md`, `references/cro-pricing-strategy.md`, `references/cro-nrr-playbook.md`
- **CRO CLI models** — `scripts/cro_revenue_forecast.py`, `scripts/cro_churn_analyzer.py`
- Routing/help entries for `/ct-cro` in `CLAUDE.md`, `skills/ct-sales/SKILL.md`, `skills/ct-help/SKILL.md` (including the LEADERSHIP section of the help index)

### Unchanged (coaching stays)
- `/ct-qualify` Coach Mode via `references/deal-coach.md` (vendored from `jeffbrickler/cro-deal-coach` — upstream repo name only; plugin-side it is deal coaching)
- `/ct-score`, `/ct-commit`, `/ct-proposal` decision-gate mode

---

## v2.9.0 — 2026-07-11

Five more skills externalized to their own source-of-truth repos, same pattern as voice (v2.8.0). Each is now maintained in a private repo and vendored into this plugin, so Jeff can iterate a skill or reference centrally and re-sync the package. Seeded from the current (audited) plugin content — **no v2.7.0 regression**; the round-trip is lossless and idempotent.

### Added
- **`scripts/sync-skills.sh`** — clones the five externalized repos (`discovery-review-scorecard`, `commit-gate-scorecard`, `cro-deal-coach`, `proposal-decision-gate`, `pipedrive-update`) and regenerates their vendored copies. Separate from `sync-voice.sh` by design.
- **`scripts/ct-score-frontmatter.md`** / **`scripts/ct-commit-frontmatter.md`** — pin the plugin skill names (`ct-score`, `ct-commit`) and single-line (indexer-safe) descriptions across syncs, independent of how each upstream repo writes its own frontmatter.

### Source-of-truth repos (all private, `jeffbrickler/`)
- `discovery-review-scorecard` → `skills/ct-score/SKILL.md`
- `commit-gate-scorecard` → `skills/ct-commit/SKILL.md`
- `cro-deal-coach` → `references/deal-coach.md` (`/ct-qualify` Coach Mode)
- `proposal-decision-gate` → `templates/decision-gate/*.md` (`/ct-proposal` decision-gate mode)
- `pipedrive-update` → `references/pipedrive-custom-fields.md` + `pipedrive-stage-ids.md` (data layer only; the `sales-crm` single-writer agent stays plugin-owned and consumes them)

---

## v2.8.0 — 2026-07-11

Voice standard externalized. The CADTALK voice/writing system now lives in its own source-of-truth repo (`jeffbrickler/cadtalk-voice`, private) and is vendored into this plugin, so it can be updated centrally and wired into other projects. Ships the upstream **v1.6** voice standard.

### Added
- **`scripts/sync-voice.sh`** — pulls the voice standard from `jeffbrickler/cadtalk-voice` and regenerates `references/cadtalk-voice-reference.md` (verbatim) and `skills/ct-voice/SKILL.md` (upstream body + pinned plugin frontmatter). One command to re-sync after an upstream edit.
- **`scripts/ct-voice-frontmatter.md`** — pins the plugin skill's `name: ct-voice` and its single-line (indexer-safe) description across syncs, independent of how upstream writes its own frontmatter.

### Changed
- **`skills/ct-voice/SKILL.md`** updated to upstream v1.6 — context-compressed (dropped Quick Start / Team Adoption / Troubleshooting), 80+ AI-fingerprint banned-word list, hard em-dash ban, and an explicit "drive the business case in dollars" engine. All content skills that defer to the reference (`/ct-outreach`, `/ct-followup`, `/ct-proposal`, `/ct-prep`, `/ct-se`) pick up the update for free.
- **`references/cadtalk-voice-reference.md`** replaced with the upstream unified reference (verbatim copy; do not hand-edit — edit upstream and re-sync).
- **CLAUDE.md** Voice section documents the source-of-truth repo and the sync workflow.

---

## v2.7.0 — 2026-07-11

CRM stage-wiring. Completes Phase 1 of the packaging plan — every pipeline-stage skill now emits its standard payload through the single sales-crm writer, so two reps working the same deal leave identical Pipedrive state at every stage. Field list confirmed against the live Pipedrive export (2026-07-11) and the internal Sales Process doc.

### Added
- **SQL Date / SQO Date conversion stamps** — the sales-crm STAGE MOVE contract now stamps **SQL Date** on entry to Discovery (opportunity pipelines 1/2/3) and **SQO Date** on entry to Prove, **set-once** (never overwritten on re-entry, backward moves never clear them) so funnel conversion metrics stay clean.
- **Per-stage payloads wired** through `agents/sales-crm.md` for `/ct-qualify` (Tier, Forecast Category, Health Score, MEDDPICC), `/ct-prep` (discovery activity, scheduled next follow-up), `/ct-se` (demo activity, Feedback on Demonstration, MEDDPICC decision criteria/competition), `/ct-proposal` (stage→Propose, value, close date, Feedback on Proposal, MEDDPICC decision/paperwork process), `/ct-commit` (Forecast Category gate, Health Score, Compelling Event + Date, EB Last Direct Touch), `/ct-followup` (activity, scheduled next follow-up, Health Score). `/ct-score` already emitted its WGLL pin. Sales cadence is a scheduled Pipedrive activity (due date), not a field write.

### Changed
- `agents/sales-crm.md` per-stage contract promoted from DRAFT to **CONFIRMED (2026-07-11)** with real field keys; MEDDPICC confirmed as the 8 Large-text Deal fields (write to fields, not notes).
- **Field reference audited to the sales rep loop.** `references/pipedrive-custom-fields.md` trimmed from ~110 to ~40 fields — removed customer-success, billing, renewal, support, and internal-marketing fields (CSS, NPS, CSP, renewal/quarterly check-ins, FreshDesk/Chargebee/Invoice, license, lifecycle Status, Marketing Status/Assets, web-visitor plumbing), legacy duplicate fields, and per Jeff's scoping: Next Check-In, Last Check-In, Parent Account, Product Line, Org Source, Deal Label, Event, Linked web visitor. Added a scope note; these still exist in Pipedrive, just out of the writer's map. Added **MEDDPICC-Coach** and **EB Last Direct Touch**; documented **Compelling Event / Compelling Event Date** as current names for the old Trigger Type / Trigger Date keys.

---

## v2.6.0 — 2026-07-10

Leadership module. Phase 5 of packaging Jeff's standalone skills — a leader-facing revenue-advisory layer above the rep loop.

### Added
- **`/ct-cro`** — CADTALK revenue-leadership advisory: forecasting, sales-model design, pricing, NRR/retention, quota + capacity, board reporting. Diagnostic questions, board-metric targets/red-flags, ARR waterfall, NRR benchmarks, and a Bottom-line → What → Why → How-to-act → Decision output shape with 🟢/🟡/🔴 confidence tags. Ported and CADTALK-scoped from the `cro-advisor` skill.
- **`references/cro-sales-playbook.md`, `cro-pricing-strategy.md`, `cro-nrr-playbook.md`** — the three universal B2B-SaaS revenue playbooks the skill reads, each headed with a CADTALK note linking back to the rep skills and the voice + sales-crm contracts.
- **`scripts/cro_revenue_forecast.py`, `cro_churn_analyzer.py`** — CLI models (weighted pipeline forecast with scenarios; NRR/GRR/cohort + at-risk accounts).

### Changed
- Routing + orchestrator + help docs updated for `/ct-cro` (CLAUDE.md routing table, `/ct-sales` command reference + cross-skill map, `/ct-help` skill map + detail block under a new LEADERSHIP section).

### Guardrails
- **Advisory and read-only.** `/ct-cro` never writes Pipedrive; any pipeline read runs through the sales-crm contract. Leader-facing, explicitly not the rep loop — reconciles its forecast against `/ct-commit`. Foreign protocol references from the source skill (agent-protocol, company-context, `[INVOKE]`) were stripped; communication defers to `references/cadtalk-voice-reference.md`.

---

## v2.5.0 — 2026-07-10

Coaching + enablement + fulfillment. Phase 4 of packaging Jeff's standalone skills — two folds into existing skills plus one new post-close skill, closing the loop from qualification through order handoff.

### Added
- **`/ct-qualify` gains Coach Mode** — enterprise deal coaching for a live deal the AE owns: BANTED health check, 9 cycle killers, buying-committee mapping / multi-threading, the Success Plan, coach-without-taking-over, stuck-deal protocols, and a Deal Health Card. Folds in `cro-deal-coach`. Engine in **`references/deal-coach.md`**. Default Qualify Mode (new-prospect flow) is unchanged.
- **`/ct-train` gains Enablement Mode** — build the team's operating tools: sales playbook, 30/60/90 ramp plan, weekly sales-meeting agenda, competitive battlecard, enablement audit. Folds in `saas-sales-enablement`. Engine in **`references/sales-enablement.md`**, which pulls CADTALK specifics from the content skills rather than restating them. `/ct-se` now draws its demo-script scaffold from Sections 4–5 of the same reference.
- **`/ct-fulfill`** — new post-close skill. Turns closed-won deals into per-deal order-submission emails to fulfillment@cadtalk.com, built to the New Order Processing SOP (partner rules, PO handling, pod, HOLD conditions) in the CADTALK internal voice. Ported from `cadtalk-fulfillment-order-emails` with **`references/sop-order-rules.md`** and **`references/fulfillment-email-template.md`**. Reads Pipedrive through the sales-crm contract; never writes the CRM or sends email.

### Changed
- Both folds route any CRM access through the sales-crm contract; their legacy `pipedrive_*` names map via the contract (reads only for `/ct-fulfill`). Descriptions single-lined for the indexer.
- Routing + orchestrator + help docs updated for Coach Mode, Enablement Mode, and `/ct-fulfill` (CLAUDE.md routing table, `/ct-sales` command reference + cross-skill map, `/ct-help` skill map + detail blocks).

---

## v2.4.0 — 2026-07-10

Stage gates. Phase 3 of packaging Jeff's standalone skills — two pipeline-stage scorecards plus a decision-gate mode.

### Added
- **`/ct-score`** — WGLL discovery scorecard (Phase 0 Intake + Discover, 5 dimensions each, 0–4, max 20), outputs a Pipedrive-ready pin + coaching flags. Ported from `discovery-review-scorecard`.
- **`/ct-commit`** — commit-gate forecast-integrity scorecard (Aftermarket + partner/New-ERP gates, Health Score, weighted forecast, fake-commit finder). Ported from `commit-gate-scorecard`.
- **`templates/decision-gate/`** — the five decision-meeting templates (brief/presentation/call-script/objections/follow-up + intake schema) from `proposal-decision-gate`.

### Changed
- **`/ct-proposal` gains a Decision-Gate mode** — post-demo go/no-go meeting kit (decision brief, exec deck, rep call script, decision questions, objection handling, follow-up), folding in `proposal-decision-gate`. Default mode still writes the proposal document.
- Both scorecards route CRM reads/writes through the sales-crm contract; their legacy `pipedrive_*` tool names map via the contract. Multiline descriptions flattened to single-line.
- Routing + help + orchestrator docs updated for `/ct-score`, `/ct-commit`, and the decision-gate mode.

---

## v2.3.0 — 2026-07-10

Voice standard. Phase 2 of packaging Jeff's standalone skills. One voice system every rep-authored output runs through, so the team sounds like one voice.

### Added
- **`references/cadtalk-voice-reference.md`** — the unified CADTALK voice system (personal voice + anti-AI-slop + Strunk & White clarity + brand constraints), copied verbatim from the standalone `cadtalk-voice` skill.
- **`/ct-voice` skill** — standalone WRITE / REVIEW / COACH on any copy (emails, follow-ups, recaps, scripts, proposals, posts, "does this sound on-brand?"). Ported from `cadtalk-voice`; multiline description flattened to single-line for the indexer.

### Changed
- **Content skills apply the voice before output** — `/ct-outreach`, `/ct-followup`, `/ct-proposal`, `/ct-prep`, `/ct-se` each end with a voice pass against the reference.
- **CLAUDE.md** — single voice-standard rule + `/ct-voice` routing row.
- **`/ct-help`** — added `/ct-voice` and `/ct-crm` to the skill map and detail blocks (ct-crm's help entry was missing after v2.2.0).
- **`/ct-sales`** — command-reference rows + cross-skill references for `/ct-crm` and `/ct-voice`.

---

## v2.2.0 — 2026-07-10

CRM hygiene backbone. Phase 1 of packaging Jeff's standalone skills into the plugin. Establishes a single Pipedrive write path so every rep's CRM updates are identical.

### Added
- **`agents/sales-crm.md`** — the single CADTALK Pipedrive write engine. Embeds the field-key/stage-ID references, maps operations to the connected Pipedrive MCP tool base names, and defines the machine-to-machine intent interface skills use. Ported from the standalone `pipedrive-update` skill. (No `tools:` restriction — it needs the Pipedrive MCP.)
- **`references/pipedrive-custom-fields.md`** + **`references/pipedrive-stage-ids.md`** — CADTALK's custom field API keys, option IDs, pipeline/stage IDs, activity key_strings, product IDs. Copied verbatim so keys stay exact.
- **`/ct-crm` skill** — direct Pipedrive updates for reps (set fields, log calls, notes, stage moves, queries), running the same sales-crm contract as the automated writes.

### Changed
- **CLAUDE.md single-writer rule** — no ct-* skill writes Pipedrive directly; all CRM writes go through the sales-crm contract, and field keys come only from the references.
- **`/ct-prospect`** Phase 4 routes its Pipedrive record creation through the sales-crm contract instead of writing directly.
- **`scripts/validate-plugin.py`** — WARNs when any skill/agent other than sales-crm / ct-crm names a Pipedrive write tool directly (single-writer enforcement).

### Follow-on (needs Jeff's input)
- Per-stage CRM field contract is DRAFT in `agents/sales-crm.md`. Once Jeff confirms which fields each stage must set, wire the remaining stage skills (ct-qualify, ct-prep, ct-se, ct-proposal, ct-followup) to emit their standard payload through sales-crm.

---

## v2.1.0 — 2026-07-11

Sales Engineer module. Adds `/ct-se` — Brain-grounded technical demo prep for CADTALK deals.

### Added
- **`/ct-se <company>` skill** (`skills/ct-se/SKILL.md`) — 4-phase demo-prep workflow: (1) stack intake (Pipedrive → deal folder → user → web), (2) capability mapping via the grounding chain (Brain → CT Outline docs → human) with per-claim evidence status (≤5 grounding calls, scoped to the CAD×ERP pair), (3) demo script against the prospect's stack, (4) technical objection prep. Output: `TECH-DEMO-PREP.md` in the deal folder.
- **`agents/sales-engineer.md`** — SE subagent definition and grounding contract. Runs inline in `/ct-se` for v1; becomes load-bearing when `/ct-prospect` wires it in (phase 2).
- **`templates/demo-prep.md`** — structure for `TECH-DEMO-PREP.md`.

### Anti-hallucination design
Every capability claim is grounded through a chain: the Brain first (source-grounded), the CT Outline document site as backup when the Brain MCP is offline, then human escalation ("verify with a senior SE, engineering, or a senior solution architect") when neither has evidence. Only if both the Brain and Outline are unreachable is the whole brief bannered UNVERIFIED. No "yes it works" claim ships untagged.

### Boundary
`/ct-prep` is AE business-discovery prep; `/ct-se` is SE technical demo prep. They're complementary — run both for a technical demo. Documented in CLAUDE.md routing, ct-help, ct-train, and the ct-sales cross-skill table.

### Deferred (phase 2 / not in this release)
`/ct-prospect --se` 6th-agent wiring and `/ct-qualify` technical-fit scoring — the SE agent ships and gets supervised use first.

---

## v2.0.2 — 2026-07-10

Registration hotfix. Restores the plugin's slash-command surface — all 17 skills were invisible in Claude Code autocomplete because none had YAML frontmatter (the skill indexer requires it).

### Fixed
- **Frontmatter added to all 17 SKILL.md files** — single-line trigger-rich `name:`/`description:` blocks. This is the core fix; without it no `/ct-*` command registered.
- **Frontmatter added to all 5 agent files** — `name:`, `description:`, and a built-in `tools:` scope (Read, Grep, Glob, WebSearch, WebFetch), replacing the useless "Agent from cadtalk-sales-team plugin" fallback and unrestricted tools. MCP tools left unscoped (instance-scoped per user, cannot be pinned in frontmatter).
- **`ct-sales` moved into `skills/`** — was at repo root, where it could not register.
- **Stale-path repairs** — `ct-sales` sub-skill routing `skills/ct-sales-<command>/` → `skills/ct-<command>/`; `ct-prospect` dead `~/.claude/agents/ct-sales-*.md` references → Agent-tool `subagent_type` strings (`cadtalk-sales-team:sales-*`). Prose/logic otherwise untouched.
- **Stale command references** in agent files (`/sales prospect` → `/ct-prospect`).

### Changed
- **`plugin.json` `skills` array deleted** — Claude Code auto-discovers `skills/*/SKILL.md`. The explicit list had already drifted (missing ct-help + ct-train); removing it eliminates the drift class entirely.

### Added
- **`scripts/validate-plugin.py`** — FAILs on missing/multiline frontmatter or a stray `skills` array; WARNs on a missing CLAUDE.md routing row. Run before every version bump.
- **`.githooks/pre-commit`** — runs the validator on every commit. Install once per clone: `git config core.hooksPath .githooks`.

### Upgrade note (teammates)
If you installed an earlier upstream build, remove the 14 legacy pre-rename skill copies at `~/.claude/skills/sales-*` — otherwise every command registers twice (`sales-prep` AND `ct-prep`). Reinstall the plugin after upgrading.

---

## v2.0.1 — 2026-07-10

Planning session: registration fix + `/ct-se` sales engineer agent design.

### Added
- **TODOS.md** — Output-location convention reconciliation captured as a future work item (ct-sales "File Output" vs. Deal Desk convention; best addressed after v2.1.0 ships).

### Design (not shipped yet)
- **v2.0.2 scope locked:** frontmatter on 17 skills + 6 agents, `ct-sales` moved into `skills/`, stale-path repairs, plugin.json `skills` array deleted, 14 legacy `sales-*` copies cleanup, validator + pre-commit hook.
- **v2.1.0 scope locked:** `/ct-se` skill (4-phase Brain-grounded demo prep), `agents/sales-engineer.md`, demo-prep template, docs pass.
- Design doc: eng review passed (12 findings, 0 unresolved), full plans at `~/.gstack/projects/jeffbrickler-CADTALK-AI-Sales-Team/`.

---

## v2.0.0 — 2026-07-08

First team-distributable release. Jeff's Deal Desk is now a proper Claude Code plugin.

### Added
- **RPM plugin install** — `claude plugin marketplace add jeffbrickler/CADTALK-AI-Sales-Team` + `claude plugin install cadtalk-sales-team@cadtalk-ai-sales-team` installs the full system in one command. No manual file copying.
- **`/cadtalk-setup` onboarding skill** — Guided first-run: identity selection, CLAUDE.md install, MCP connection checks (Pipedrive, ZoomInfo, Outlook, CT Docs, Python/PDF), smoke test, and confirmation. ~10 minutes for a fresh install.
- **CLAUDE.md bundled** — The 900-line Deal Desk identity file is now in the repo and installed automatically by `/cadtalk-setup`. Claude knows it's operating as a CADTALK sales operator the moment setup completes.
- **`.claude-plugin/plugin.json`** — Registers the plugin with RPM. Names it `cadtalk-sales-team`, version `2.0.0`. Points at all 14 skills.
- **Teammate Quick Start in README** — Step-by-step install guide for Chris, Matthew, and Lucca.

### Changed
- **`install.sh` / `uninstall.sh` removed** — The shell installer is replaced by the plugin. Install via `claude plugin marketplace add` + `claude plugin install`; remove via `claude plugin uninstall cadtalk-sales-team`.

### Skills (unchanged from v1)
All 13 CADTALK-customized skills are included:
`/sales`, `/sales-prep`, `/sales-prospect`, `/sales-research`, `/sales-qualify`,
`/sales-contacts`, `/sales-outreach`, `/sales-followup`, `/sales-proposal`,
`/sales-objections`, `/sales-icp`, `/sales-competitors`, `/sales-report`, `/sales-report-pdf`

### Install
```bash
claude plugin add github:jeffbrickler/CADTALK-AI-Sales-Team
/cadtalk-setup
```

---

## v1.0.0 — 2026 (Jeff's machine only)

Original Deal Desk build. 13 skills, 5 agents, Deal Desk CLAUDE.md. Local only — not distributable. Baseline for v2.0.0.
