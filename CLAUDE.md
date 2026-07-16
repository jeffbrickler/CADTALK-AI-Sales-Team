# CADTALK AI Sales Team — Plugin

This file is part of the `cadtalk-sales-team` Claude Code plugin.
It routes skill commands and works **additively** with your local Deal Desk folder.

**This is not the Deal Desk identity file.**
The full CADTALK identity (connected systems, pipeline IDs, qualification framework,
all commands) lives in your local Deal Desk Cowork folder:

```
Deal Desk/CLAUDE.md   ← master identity — loads when you open a deal folder in Cowork
```

Both files load together when you're working inside a deal folder. This file routes
plugin skills; the Deal Desk CLAUDE.md provides operator identity and context.

---

## Skill Routing

When the user's request matches a skill below, invoke it via the Skill tool.

| Request | Skill |
|---------|-------|
| New deal folder + Pipedrive record; open or archive a deal, CSM handoff | `/ct-deal` |
| Schedule automations — morning brief, stale alert, nightly sweep, council | `/ct-automate` |
| Generate a deck, one-pager, battlecard, or ROI calculator | `/ct-assets` |
| Contract prep — NDA triage, redline review, risk, package | `/ct-contract` |
| First-time setup, onboarding, "set me up" | `/ct-setup` |
| Meeting prep, "prep for [company]" | `/ct-prep` |
| Prospect analysis, full audit | `/ct-prospect` |
| Technical demo prep, sales engineering, "will it work with their stack" | `/ct-se` |
| Update Pipedrive, log a call, set MEDDPICC, move stage, pipeline query | `/ct-crm` |
| Create a new opportunity/deal — guided, all fields, no blanks | `/ct-crm new` |
| CRM hygiene, audit deal completeness, enrich CRM, attach participants, new opportunity intake | `/ct-hygiene` |
| Voice/tone review, "does this sound on-brand?", write/edit any copy, coaching | `/ct-voice` |
| Company research | `/ct-research` |
| Lead qualification, BANT, MEDDIC | `/ct-qualify` |
| Self-coach a deal, "review my deal", "why is it stuck", multi-thread, dark deal, success plan | `/ct-qualify` (Coach Mode) |
| Score a discovery call, WGLL, "grade this call" | `/ct-score` |
| Commit gate, "is this a real commit", forecast integrity, find fake commits | `/ct-commit` |
| Post-demo go/no-go, proposal/decision meeting kit | `/ct-proposal` (decision-gate mode) |
| Decision maker mapping, contacts | `/ct-contacts` |
| Cold outreach, email sequence | `/ct-outreach` |
| Follow-up sequence | `/ct-followup` |
| Proposal generation | `/ct-proposal` |
| Objection handling | `/ct-objections` |
| ICP builder | `/ct-icp` |
| Competitive intelligence | `/ct-competitors` |
| Pipeline report (Markdown) | `/ct-report` |
| Pipeline report (PDF) | `/ct-report-pdf` |
| General sales orchestration | `/ct-sales` |
| Help with commands, how do I use [skill] | `/ct-help` |
| Training, new user onboarding, learn the workflow | `/ct-train` |
| Hand won deals to fulfillment, order emails, "process this order", billing/onboarding kickoff | `/ct-fulfill` |
| Overnight sweep, "run my sweep", stage my review queue | `/ct-sweep` |
| Morning review, "inbox", approve sweep findings | `/ct-inbox` |

**`/ct-prep` vs `/ct-se`:** `/ct-prep` is AE business-discovery prep (who's meeting, what pain, talk track). `/ct-se` is SE technical demo prep (does our addin work with their CAD×ERP stack, what to demo). Run both for a technical demo — they're complementary, not overlapping.

## CRM hygiene — single writer rule

CADTALK's Pipedrive has exactly one write path: the **sales-crm** contract
(`agents/sales-crm.md`) plus the field references in `references/`. This is what
makes every rep's CRM updates identical.

- **No ct-* skill writes Pipedrive directly.** When a skill needs to update the
  CRM, it follows `agents/sales-crm.md` inline (or dispatches
  `subagent_type: cadtalk-sales-team:sales-crm`). It never calls a Pipedrive
  write tool with a hand-built field key.
- **Field keys and stage IDs come only from `references/pipedrive-custom-fields.md`
  and `references/pipedrive-stage-ids.md`.** Never fabricate a key.
- Each pipeline stage leaves the standard update payload defined in the sales-crm
  per-stage contract, so a deal looks the same no matter which rep worked it.

**One sanctioned exception:** deal participants are impossible via the connected MCP, so `scripts/pipedrive_participants.py` (invoked by `/ct-hygiene`) calls the Pipedrive REST API directly — participants only, nothing else; every other write stays in the sales-crm contract. `scripts/pipedrive_read.py` is the sanctioned READ path for headless sweep runs (the interactive MCP may be absent in scheduled sessions) — read-only, so the single-writer rule is unaffected.

## Voice — single standard

Every rep-authored output uses one voice standard: `references/cadtalk-voice-reference.md`
(the `/ct-voice` skill is the standalone WRITE/REVIEW/COACH command). Content skills
(`/ct-outreach`, `/ct-followup`, `/ct-proposal`, `/ct-prep`, `/ct-se`) apply it
before returning copy — personal voice, no AI slop, Strunk & White clarity, CADTALK
brand, in one pass. This is what makes the team sound like one voice.

**Source of truth.** The voice standard is maintained in its own repo,
`jeffbrickler/cadtalk-voice`, and vendored into this plugin. `references/cadtalk-voice-reference.md`
and `skills/ct-voice/SKILL.md` are generated by `scripts/sync-voice.sh` — do not
hand-edit them; edit the upstream repo, then re-run the sync, re-validate, and ship
a new plugin version. `scripts/ct-voice-frontmatter.md` pins the plugin's `ct-voice`
name and single-line description across syncs.

## Skills — externalized source of truth

Five more skills follow the same vendored-sync pattern as voice. Each is
maintained in its own private repo under `jeffbrickler/` and vendored into this
plugin by `scripts/sync-skills.sh`. **Do not hand-edit the vendored copies** —
edit the upstream repo, bump its `VERSION`, then run `scripts/sync-skills.sh`,
re-validate, and ship a new plugin version.

| Source repo | Vendored into | Consumed by |
|---|---|---|
| `discovery-review-scorecard` | `skills/ct-score/SKILL.md` | `/ct-score` |
| `commit-gate-scorecard` | `skills/ct-commit/SKILL.md` | `/ct-commit` |
| `cro-deal-coach` | `references/deal-coach.md` | `/ct-qualify` Coach Mode |
| `proposal-decision-gate` | `templates/decision-gate/*.md` | `/ct-proposal` decision-gate mode |
| `pipedrive-update` | `references/pipedrive-custom-fields.md` + `pipedrive-stage-ids.md` | `sales-crm` agent |

`ct-score` and `ct-commit` keep their plugin skill name + single-line description
via `scripts/ct-score-frontmatter.md` / `ct-commit-frontmatter.md` (the sync
strips the upstream frontmatter and prepends the pin). **pipedrive-update is the
data layer only** — the audited field/stage references. The `sales-crm`
single-writer agent (the write-contract logic) stays plugin-owned and consumes
those references; it is not externalized, so the single-writer rule above is
unaffected.
