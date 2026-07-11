# Changelog

All notable changes to CADTALK AI Sales Team are documented here.

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
