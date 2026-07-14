# TODOS

## Approach C: CRM reconciliation sweep (v2 layer after Guided Create Flow)
**What:** Post-create / end-of-conversation CRM sweep that grades records against `scripts/create-contract.json`, auto-fills what conversation context knows, asks the rep for the rest — the ct-score gate pattern applied to data hygiene.
**Why:** Catches misses from ANY path (manual web creates, skills bypassing the flow) and retro-cleans existing dirty deals. This is the deferred half of Jeff's "doesn't always write" complaint — v1 covers creates + stage moves only.
**Pros:** Completes the enforcement story; familiar WGLL gate pattern; pairs with the Pipedrive-native required-fields floor.
**Cons:** Sweep-fatigue risk if it nags every conversation; ~2 CC sessions of build.
**Context:** Staged explicitly as the v2 layer in the approved Guided Create Flow design (2026-07-14, `~/.gstack/projects/jeffbrickler-CADTALK-AI-Sales-Team/AzureAD+JeffBrickler-remove-ct-cro-design-20260714-164928.md`, Approach C section). Premise 3's full per-skill write-moment enumeration lands here. Start at `skills/ct-score` gate pattern + `create-contract.json`.
**Depends on:** Guided Create Flow v1 shipped and piloted.

## SDR lead-conversion motion (postponed — not in use)
**What:** Wire SDR lead pipelines (6/8/11/12/13) → opportunity-pipeline conversion through the Guided Create Flow.
**Why:** SDRs are named target users of the plugin, but per Jeff (2026-07-14) the SDR motion is not in use right now — postponed until it is.
**Context:** Blocker when revived: which lead pipeline converts into which opportunity pipeline per persona. Start at the Motions table in the Guided Create Flow design doc + `convertLeadToDeal` in the sales-crm tool mapping. Pre-build SDR observation (design doc Assignment) feeds this.
**Depends on:** SDR motion becoming active; Jeff's lead→opp mapping decision; Guided Create Flow v1 shipped.

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

## Completed

## Wire stage skills to the sales-crm per-stage field contract
**What:** Finish Phase 1 of the packaging plan. Confirm the field list with Jeff, then wire the stage skills to emit their standard payload through the sales-crm contract.
**Completed:** v2.7.0 (2026-07-11). Field list confirmed against the live Pipedrive export + Sales Process doc; SQL/SQO Date set-once stamps added to the STAGE MOVE contract (Discovery→SQL, Prove→SQO); ct-qualify, ct-prep, ct-se, ct-proposal, ct-commit, ct-followup wired (ct-prospect + ct-score already routed). Contract promoted DRAFT→CONFIRMED in agents/sales-crm.md.
