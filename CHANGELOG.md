# Changelog

All notable changes to CADTALK AI Sales Team are documented here.

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
