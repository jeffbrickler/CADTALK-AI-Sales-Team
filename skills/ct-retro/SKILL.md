---
name: ct-retro
description: End-of-session retro — harvest corrections into the plugin LEARNINGS.md, promote recurring ones to TODOS, and check the plugin for registration drift. Use for 'run a retro', 'what did we learn', 'capture that correction', 'check the plugin is consistent'.
---

# CADTALK Retro — the self-improvement loop

Invoked as `/ct-retro`. Run it at the end of a working session, or any time a
correction is worth capturing. Three passes: harvest, promote, check.

## Pass 1 — Harvest corrections → `LEARNINGS.md`

Scan the session for moments the plugin did the wrong thing and the rep corrected it:
- edits the rep made to a skill's output,
- drafts the rep rejected,
- wrong grounding (a brain-index doc ID that 404'd, a stale claim),
- tool-name drift (a Pipedrive tool that no longer exists under that name).

For each, decide where it belongs:
- **Ships with the plugin** (the skill should behave differently for everyone) →
  append an entry to the plugin `LEARNINGS.md` in its format, tagged with the target
  skill (`ct-prep`, `ct-crm`, `sales-crm`, or `plugin` for cross-cutting).
- **Rep-personal or deal-specific** (only true for this rep/deal) → write it to the
  workspace `MEMORY.md`, not `LEARNINGS.md`.
- **Ambiguous** → ask the rep which it is before writing.

Never invent a learning. If the session had no real corrections, say so and write
nothing.

## Pass 2 — Promote recurring learnings → `TODOS.md`

Read `LEARNINGS.md`. If the same `skill-tag` has **two or more open entries** pointing
at the same root cause, that is a signal the skill itself should change. Add a
`TODOS.md` item (in the existing TODOS format: What / Why / Context / Depends on)
proposing the skill fix, and reference the learning entries. Do not fold the change
yourself — that happens in a release.

## Pass 3 — Registration + grounding check

Catch the plugin's own drift (the automated version of the 3-file registration
checklist):

1. Run `python scripts/validate-plugin.py`. It warns on any skill directory missing a
   routing row in the root `CLAUDE.md`. Report every warning.
2. For each `skills/ct-*/` directory, grep `skills/ct-help/SKILL.md` for a matching
   `### ct-<name>` detail block. Report any skill with no ct-help detail block.
3. For each brain-index doc ID flagged as 404 during Pass 1, list it so the next
   release can fix `references/brain-index.md`.

Output a short drift report: routing gaps, ct-help gaps, stale doc IDs. If everything
is registered and grounded, say "no drift."

---

## Output

A single retro summary: N learnings written (with where each went), any TODOS
promoted, and the drift report. Keep it short — this is a maintenance pass, not a
narrative.

## Common mistakes

- Writing deal-specific facts into `LEARNINGS.md` — those go to workspace `MEMORY.md`.
- Inventing learnings to fill the log — only capture real corrections.
- Folding a skill change directly — `/ct-retro` proposes (LEARNINGS/TODOS); releases fold.
