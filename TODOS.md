# TODOS

## New skill addition checklist (3 files to update)
**What:** When a new ct-* workflow skill is added to the plugin, update all three registration points.
**Why:** ct-help will silently miss the new skill if only the skills/ directory is updated.
**Checklist:**
1. Create `skills/ct-[name]/SKILL.md`
2. Add routing row to plugin `CLAUDE.md`
3. Add detail block to `skills/ct-help/SKILL.md`
**Depends on:** nothing — do this whenever a new skill is added.
**Context:** Identified during eng review of ct-train + ct-help training module (2026-07-08). Currently 13 workflow skills covered in ct-help.
