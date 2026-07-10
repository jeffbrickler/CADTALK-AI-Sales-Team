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

## Reconcile output-location conventions across skills
**What:** ct-sales/SKILL.md "File Output" says outputs save to the current directory; the plugin convention (Deal Desk CLAUDE.md, /ct-se design) is deal folders. Decide the winning convention per skill and update prose.
**Why:** Reps get briefs scattered between cwd and deal folders depending on which skill ran — inconsistent, hard to find later.
**Pros:** One predictable location for every output; /ct-report compilation gets simpler.
**Cons:** Content change across several skills; needs a per-skill decision (some outputs are pre-pipeline with no deal folder yet).
**Context:** Flagged during /plan-eng-review of the registration-fix + /ct-se design (2026-07-10). ct-sales prose predates the Deal Desk system. Start at ct-sales/SKILL.md "File Output" section; check each skill's output instruction against Deal Desk conventions.
**Depends on:** nothing; best done after v2.1.0 ships so /ct-se's convention is the reference.
