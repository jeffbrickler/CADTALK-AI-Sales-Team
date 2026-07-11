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

## Wire stage skills to the sales-crm per-stage field contract
**What:** Finish Phase 1 of the packaging plan. `agents/sales-crm.md` has a DRAFT per-stage CRM update contract (which Pipedrive fields each stage sets). Confirm the field list with Jeff, then wire ct-qualify, ct-prep, ct-se, ct-proposal, ct-followup to emit their standard payload through the sales-crm contract (ct-prospect already routes through it).
**Why:** The single-writer backbone (v2.2.0) exists but only ct-prospect is wired. Until every stage skill emits a standard CRM payload, hygiene is uniform in mechanism but not yet in coverage.
**Pros:** Two reps working the same deal leave identical Pipedrive state at every stage.
**Cons:** Needs Jeff's per-stage field decision first; touches 5 skills.
**Context:** Phase 1 of packaging-plan-standalone-skills-20260710.md. DRAFT contract is in agents/sales-crm.md "Per-stage CRM update contract". Ship as v2.2.1 once the field list is confirmed.
**Depends on:** Jeff confirming which Pipedrive fields each pipeline stage must set.
