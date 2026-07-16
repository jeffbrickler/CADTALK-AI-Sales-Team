# De-CRO the Plugin (Rep-Focus) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove or reframe every manager/CRO-seat decision surface in the cadtalk-sales-team plugin so all skills serve the rep coaching themselves, per Jeff's decisions on 2026-07-16.

**Architecture:** Three vendored skills are reframed in their upstream repos (cro-deal-coach, commit-gate-scorecard, discovery-review-scorecard) then re-vendored via `scripts/sync-skills.sh`. Enablement Mode is deleted (plugin-owned). Reports and routing prose are edited in-plugin. One version bump + changelog at the end.

**Tech Stack:** Markdown skills, bash sync script, `python scripts/validate-plugin.py`, gh CLI (ADMIN confirmed on all three upstream repos).

**User decisions (locked):**
1. ct-qualify Coach Mode → reframe deal-coach to rep self-coach (upstream edit).
2. ct-commit → reframe as rep self-gate (upstream edit).
3. ct-train Enablement Mode + references/sales-enablement.md → remove.
4. ct-report / ct-report-pdf → keep, reframe wording for rep.
5. ct-score → strip "or manager review" (upstream edit; noted to user, no objection).

**Reframe principle (use everywhere):** The coach persona is *Claude/the skill*; the human is *the rep who owns the deal*. Never "you are a CRO / coach my AE." Socratic questioning, Rule of Two, debriefs all survive — pointed at the rep's own deal/call.

Plugin worktree root (all relative paths below): `C:\Users\JeffBrickler\Documents\ClaudeCode\dev\CADTALK-AI-Sales-Team-fresh\.claude\worktrees\office-hours-17991c`
Scratchpad for upstream clones: `C:\Users\JEFFBR~1\AppData\Local\Temp\claude\...\scratchpad` (session scratchpad; exact path in session env).

---

### Task 1: Reframe upstream `cro-deal-coach` to rep self-coach

**Files:**
- Clone: `jeffbrickler/cro-deal-coach` → `<scratchpad>/cro-deal-coach`
- Modify: `SKILL.md` (frontmatter description + body), `VERSION` (check exact filename/convention in repo; bump minor)

- [ ] **Step 1: Clone and inspect**

```bash
cd <scratchpad> && git clone https://github.com/jeffbrickler/cro-deal-coach && ls cro-deal-coach
```
Read `SKILL.md` frontmatter + `VERSION` (or equivalent). Body should match vendored `references/deal-coach.md` lines 1–300.

- [ ] **Step 2: Apply persona replacements to SKILL.md body** (old → new; old strings quoted from vendored copy, verify against upstream before editing)

1. Intro paragraph (lines 3–7 of body):
   - OLD: `reviewing a deal\nthe CRO didn't work themselves and coaching the AE who's closer to it.` (exact wrapping per file)
   - NEW: `a rep reviewing a deal they own with a coach's eyes — seeing it clearly and deciding the next move themselves.`
   - OLD: `Calibrated for $50K+ ACV, multi-stakeholder enterprise deals, and a CRO new to\ncoaching AEs.`
   - NEW: `Calibrated for $50K+ ACV, multi-stakeholder enterprise deals, and a rep coaching themselves between manager check-ins.`
2. Persona paragraph (body line 14):
   - OLD: `You are a CRO reviewing deals you didn't work yourself, coaching an AE who is closer to them than you are. Your goal is not to close the deal for the AE — it is to help the AE see clearly and act decisively. The biggest coaching mistake a former top seller makes is taking deals over. It feels like helping. It teaches dependency.`
   - NEW: `You are the rep's deal coach. The deal belongs to the rep you're talking to — your goal is not to decide for them, it is to help them see the deal clearly and act decisively. The biggest coaching mistake is handing over answers. It feels like helping. It teaches dependency.`
3. Core principle (body line 16):
   - OLD: `your job is to ask questions until the AE reaches the right conclusion themselves`
   - NEW: `your job is to ask questions until the rep reaches the right conclusion themselves`
4. Section 1 intake (body line 24): OLD `don't ask the AE to hand-key` → NEW `don't ask the rep to hand-key`
5. Section 1 items 7–8 (body lines 32–33):
   - OLD: `What's the next step as the AE understands it?` → NEW: `What's the next step as you understand it?`
   - OLD: `8. **The CRO's concern:** Why are you looking at this deal? Is it a coaching session, a deal review, a risk flag, or a rescue?`
   - NEW: `8. **Your concern:** Why are you looking at this deal? Routine review, stuck, going dark, or a gut feeling something's off?`
6. Section 2 BANTED table row D (body line 50): OLD `a deal that the AE thinks is in the final stage` → NEW `a deal that looks like it's in the final stage`
7. Section 6 title + framing (body lines 178–218) — keep the three modes and Rule of Two, repoint at Claude-as-coach:
   - OLD heading: `## Section 6: How to Coach Without Taking Over` → NEW: `## Section 6: How to Coach Without Handing Over Answers`
   - OLD: `This is the hardest skill for a former top seller. You know what you would do. Doing it for them is always faster in the short term and damaging in the long term.`
   - NEW: `The coach's discipline: giving the rep the answer is always faster in the short term and damaging in the long term. The rep owns the deal and the action.`
   - OLD: `based on the deal's risk and the rep's capability.` → NEW: `based on the deal's risk and how stuck the rep is.`
   - Mode 3 example (body line 203): keep, it already coaches the rep directly — no change needed.
   - Rule of Two (line 207): OLD `you are coaching too hard and creating a dependency.` → keep; OLD `advice you give a rep` → keep (coach = Claude).
   - Rule of Two test (line 209): OLD `before we talk next week` → NEW `in the next week` (no standing manager meeting implied).
   - Post-Call Debrief (line 213): OLD `When an AE runs a call that you observe (or get a recording of), use this debrief format:` → NEW: `After any call the rep runs (notes or recording in hand), walk them through this self-debrief:`
8. Section 7 (body line 258): OLD `If the AE hesitates, they already know it's wrong.` → NEW `If you hesitate, you already know it's wrong.`
9. Section 8 (body lines 284–287):
   - OLD: `3. One coaching question — the question the CRO should ask the AE to help them reach the conclusion themselves`
   - NEW: `3. One coaching question — the question for the rep to sit with until they reach the conclusion themselves`
   - OLD: `**For CRO coaching specifically:**\nWhich coaching mode to use (Socratic / Collaborative / Direct), and the first question to open the coaching session.`
   - NEW: `**Coaching mode:**\nWhich mode this session ran in (Socratic / Collaborative / Direct), and the opening question used.`
10. Frontmatter `description`: replace any `CRO` / `coach my AE` phrasing with rep-self phrasing, e.g. `Enterprise deal self-coaching for a rep's own deals — BANTED review, cycle killers, multi-threading, success plans, stuck-deal protocols. Use for 'review my deal', 'why is this deal stuck', 'the deal went dark', 'build a success plan'.` (Adapt to upstream's existing description shape.)
11. Grep the file for remaining `CRO|my AE|the AE` — fix any stragglers with the same principle (buyer-persona "AE" mentions like the partner-AE note at body line 120 STAY — that's the partner's AE, not our seat).

- [ ] **Step 3: Bump upstream VERSION** (minor bump, e.g. 1.x.0 → 1.(x+1).0 per repo convention).

- [ ] **Step 4: Commit + push upstream**

```bash
cd <scratchpad>/cro-deal-coach && git add -A && git commit -m "refactor: reframe persona from CRO-coaching-AE to rep self-coach" && git push
```
Expected: push to main succeeds (ADMIN access confirmed).

### Task 2: Reframe upstream `commit-gate-scorecard` to rep self-gate

**Files:**
- Clone: `jeffbrickler/commit-gate-scorecard` → `<scratchpad>/commit-gate-scorecard`
- Modify: `SKILL.md`, `VERSION`

- [ ] **Step 1: Clone; read SKILL.md; grep `board|team|manager|CRO`** to find all manager-seat lines (vendored copy shows one known hit).

- [ ] **Step 2: Apply replacements**

1. Judge line (vendored ct-commit line 22):
   - OLD: `You are the CADTALK forecast-integrity judge. Decide whether a deal has earned the **Commit** label using proof instead of feel, and report a weighted forecast the team can take to the board.`
   - NEW: `You are the CADTALK forecast-integrity judge. Decide whether a deal has earned the **Commit** label using proof instead of feel, so the number the rep calls is one they can defend in any forecast conversation.`
2. Any other `board`/`team forecast` framing found in Step 1 → same rep-self principle ("your commit, your pipeline, your forecast call"). Sweep-mode wording ("find fake commits", "weekly audit") stays — a rep sweeping their own pipeline is in scope.
3. Frontmatter description: keep if already rep-phrased (`'score my commit', 'is [company] a real commit'`); remove any board/team phrasing.

- [ ] **Step 3: Bump VERSION, commit, push**

```bash
cd <scratchpad>/commit-gate-scorecard && git add -A && git commit -m "refactor: reframe forecast framing from board/team to rep self-gate" && git push
```

### Task 3: Strip manager-review path from upstream `discovery-review-scorecard`

**Files:**
- Clone: `jeffbrickler/discovery-review-scorecard` → `<scratchpad>/discovery-review-scorecard`
- Modify: `SKILL.md`, `VERSION`

- [ ] **Step 1: Clone; locate the optional-inputs bullet** (vendored ct-score line 34): `- Whether this is a self-assessment or manager review`

- [ ] **Step 2: Delete that bullet.** Grep `manager|CRO` for any other hits; fix with the same principle (self-score framing). "Pipeline quality judge" persona (Claude's seat) stays.

- [ ] **Step 3: Bump VERSION, commit, push**

```bash
cd <scratchpad>/discovery-review-scorecard && git add -A && git commit -m "refactor: self-assessment only — drop manager-review path" && git push
```

### Task 4: Re-vendor via sync-skills.sh + validate

**Files:**
- Regenerated: `skills/ct-score/SKILL.md`, `skills/ct-commit/SKILL.md`, `references/deal-coach.md` (also re-copies decision-gate + pipedrive refs, unchanged)

- [ ] **Step 1: Run sync**

```bash
cd <worktree-root> && bash scripts/sync-skills.sh
```
Expected: 5 ✓ lines, exit 0.

- [ ] **Step 2: Verify** — `git diff --stat` shows only the 3 reframed files changed; grep `references/deal-coach.md` + `skills/ct-commit/SKILL.md` + `skills/ct-score/SKILL.md` for `CRO|coach my AE|board|manager review` → zero hits (except legitimate buyer-persona/partner-AE mentions).

- [ ] **Step 3: Validate + commit**

```bash
python scripts/validate-plugin.py && git add -A && git commit -m "feat: re-vendor rep-self reframes of deal-coach, commit-gate, discovery scorecard"
```

### Task 5: Reframe plugin-owned Coach Mode routing (ct-qualify, CLAUDE.md, ct-sales, ct-help)

**Files:**
- Modify: `skills/ct-qualify/SKILL.md:3,22-30`, `CLAUDE.md` (routing row), `skills/ct-sales/SKILL.md:117`, `skills/ct-help/SKILL.md:34,105-130`

- [ ] **Step 1: ct-qualify frontmatter description (line 3)** — replace Coach Mode trigger list:
   - OLD fragment: `'review this deal', 'coach my AE on this opportunity', 'why is this deal stuck', 'is this deal real', 'how do I multi-thread this account', 'the deal went dark — what now', 'build a success plan', or 'my AE says it's close but I'm not sure'`
   - NEW fragment: `'review my deal', 'why is this deal stuck', 'is this deal real', 'how do I multi-thread this account', 'the deal went dark — what now', or 'build a success plan'`

- [ ] **Step 2: ct-qualify Coach Mode block (lines 22–30)**:
   - OLD: `an *existing* deal the AE already owns, and the ask is to\n  review it, diagnose why it's stuck, coach the AE, multi-thread it, restart a\n  dark deal, or build a Success Plan. Triggers: "review this deal", "coach my AE\n  on this", "why is [company] stuck", "is this deal real", "the deal went dark",\n  "help me multi-thread", "build a success plan", "my AE says it's close but I'm\n  not sure".`
   - NEW: `an *existing* deal the rep already owns, and the ask is to\n  review it, diagnose why it's stuck, multi-thread it, restart a dark deal, or\n  build a Success Plan. Triggers: "review my deal", "why is [company] stuck",\n  "is this deal real", "the deal went dark", "help me multi-thread", "build a\n  success plan".`
   - Keep `coach-without-taking-\n  over` reference text but update to match new Section 6 name: `coach-without-handing-over-answers` (or simply `coaching modes`; match whatever the parenthetical list reads best as).

- [ ] **Step 3: CLAUDE.md routing row**:
   - OLD: `| Coach a deal, "review this deal", "why is it stuck", multi-thread, dark deal, success plan | \`/ct-qualify\` (Coach Mode) |`
   - NEW: `| Self-coach a deal, "review my deal", "why is it stuck", multi-thread, dark deal, success plan | \`/ct-qualify\` (Coach Mode) |`

- [ ] **Step 4: ct-sales line 117**:
   - OLD: `- \`/ct-qualify\` Coach Mode reviews live deals (BANTED, cycle killers, multi-thread, Success Plan) via \`references/deal-coach.md\` — complements \`/ct-commit\` (forecast) and \`/ct-score\` (discovery)`
   - NEW: `- \`/ct-qualify\` Coach Mode helps a rep self-review their live deals (BANTED, cycle killers, multi-thread, Success Plan) via \`references/deal-coach.md\` — complements \`/ct-commit\` (forecast) and \`/ct-score\` (discovery)`

- [ ] **Step 5: ct-help ct-qualify entry** — Read lines 100–130; replace:
   - Line 34: `Coach Mode: review/coach a live deal` → `Coach Mode: self-review a live deal`
   - Line ~108: `COACH MODE: reviews a live deal the AE already owns` → `COACH MODE: self-review of a live deal the rep already owns`
   - Line ~114: drop `"coach my AE"` from trigger list (and `my AE says it's close` if present)
   - Line ~122: `the coaching question to ask the AE` → `the coaching question for the rep to sit with`

- [ ] **Step 6: Commit**

```bash
git add -A && git commit -m "refactor: Coach Mode routing reframed to rep self-coaching"
```

### Task 6: Remove Enablement Mode

**Files:**
- Delete: `references/sales-enablement.md`
- Modify: `skills/ct-train/SKILL.md:3,8-27`, `skills/ct-help/SKILL.md:63-65,537-565`, `CLAUDE.md` (routing row), `skills/ct-sales/SKILL.md:118`

- [ ] **Step 1: Delete reference**

```bash
git rm references/sales-enablement.md
```

- [ ] **Step 2: ct-train frontmatter (line 3)**:
   - NEW description: `Training and onboarding for CADTALK reps. Use for learning the workflow and rep onboarding — an interactive 7-stage mock-deal walkthrough (~20 min).`

- [ ] **Step 3: ct-train body** — collapse the two-mode intro (lines 8–21) to Training only:
   - Replace `Two modes:` block with a single paragraph: `The interactive 7-stage mock-deal walkthrough below. Covers the full workflow: research → qualify → prep → outreach → report. ~20 minutes. Works without MCP connections. This is what a new rep runs in Week 1.`
   - Line 27 (How to run): drop the sentence `For an enablement build ("build a playbook", "ramp plan for a new AE", etc.), run Enablement Mode via references/sales-enablement.md instead of the stage flow.`
   - Grep rest of file for `enablement|Enablement` and remove stragglers.

- [ ] **Step 4: ct-help** — Read lines 60–70 and 535–565; replace:
   - Section header `ONBOARDING & ENABLEMENT` → `ONBOARDING & TRAINING`
   - Line 65: `/ct-train  Training walkthrough (~20 min) — or Enablement Mode: playbooks, ramp plans, battlecards, audits` → `/ct-train  Training walkthrough (~20 min) — interactive mock-deal onboarding`
   - Lines ~544–561: delete the ENABLEMENT paragraph, the enablement WHEN-TO-RUN sentence (`Enablement when a manager needs a playbook...`), the two enablement example invocations, the enablement deliverable line, and the `Reinventing CADTALK facts in an enablement build` pitfall. Keep Training content intact.

- [ ] **Step 5: CLAUDE.md** — delete routing row:
   - `| Build a playbook, ramp plan, weekly meeting, battlecard, enablement audit | \`/ct-train\` (Enablement Mode) |`
   - Also update the ct-train row above it if it says `(interactive walkthrough); and — in Enablement Mode — ...` (routing table row `Training, new user onboarding, learn the workflow`  stays; just ensure no Enablement remnant).

- [ ] **Step 6: ct-sales line 118** — delete:
   - `- \`/ct-train\` Enablement Mode builds playbooks/ramp plans/battlecards/audits via \`references/sales-enablement.md\`, pulling specifics from the content skills`

- [ ] **Step 7: Verify + commit**

```bash
grep -ri "sales-enablement" --include="*.md" . ; grep -rn "Enablement Mode" --include="*.md" skills/ CLAUDE.md
```
Expected: no hits outside CHANGELOG/docs history. Then:

```bash
git add -A && git commit -m "feat!: remove Enablement Mode — manager tooling out of rep plugin"
```

### Task 7: Reframe reports for the rep

**Files:**
- Modify: `skills/ct-report/SKILL.md:10`, `skills/ct-report-pdf/SKILL.md:19`

- [ ] **Step 1: ct-report line 10**:
   - OLD: `produce an executive-ready report that tells Jeff exactly where the pipeline stands and what to do this week.`
   - NEW: `produce a clean report that tells the rep exactly where their pipeline stands and what to do this week — ready for a manager 1:1 or forecast call.`

- [ ] **Step 2: ct-report-pdf line 19**:
   - OLD: `The PDF is designed for sharing with sales leadership, investors, or team members who need a clean, portable document rather than a markdown file.`
   - NEW: `The PDF is a clean, portable version of the rep's own pipeline report — handy for a manager 1:1, a forecast call, or anyone who'd rather read a document than a markdown file.`
   (ct-help lines 441/450/462 already rep-framed — leave.)

- [ ] **Step 3: Commit**

```bash
git add -A && git commit -m "refactor: pipeline reports framed as the rep's own pipeline"
```

### Task 8: CLAUDE.md externalized-table wording, changelog, version bump, final validation

**Files:**
- Modify: `CLAUDE.md` (externalized-skills table row for cro-deal-coach — repo name stays `cro-deal-coach`, that's the slug; no change needed unless prose says "CRO deal coach" descriptively), `CHANGELOG.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (if it carries version)

- [ ] **Step 1: Full-repo residue grep**

```bash
grep -rniE "coach (my|the|an) AE|you are a CRO|manager review|take to the board|enablement mode" --include="*.md" --include="*.json" --include="*.py" --include="*.sh" . | grep -v CHANGELOG | grep -v docs/superpowers
```
Expected: zero hits. Fix any found.

- [ ] **Step 2: Bump version** in `.claude-plugin/plugin.json`: `2.12.0` → `2.13.0`. Check `marketplace.json` for a version field; bump to match if present.

- [ ] **Step 3: CHANGELOG.md entry** (top, match existing format):

```markdown
## 2.13.0 — 2026-07-16

**Rep-focus: CRO/manager surface removed.** The plugin serves reps, not the manager seat.

- `/ct-qualify` Coach Mode reframed: rep self-coaching on their own deal (upstream `cro-deal-coach` rewritten from CRO-coaching-an-AE persona).
- `/ct-commit` reframed: rep self-gate — defend your own number, board/team-forecast framing removed (upstream `commit-gate-scorecard`).
- `/ct-score`: self-assessment only; manager-review path removed (upstream `discovery-review-scorecard`).
- `/ct-train` Enablement Mode removed (playbooks, ramp plans, weekly meetings, enablement audits) along with `references/sales-enablement.md`. Training Mode (rep walkthrough) unchanged.
- `/ct-report` + `/ct-report-pdf` reframed as the rep's own pipeline prep for 1:1s/forecast calls.
```

- [ ] **Step 4: Validate + commit**

```bash
python scripts/validate-plugin.py && git add -A && git commit -m "chore: v2.13.0 — rep-focus release; changelog + version bump"
```

- [ ] **Step 5: Final check** — `git log --oneline -8` shows the task commits; working tree clean.

---

## Self-Review Notes

- Spec coverage: all 5 locked decisions have tasks (1→D1, 2→D2, 6→D3, 7→D4, 3→D5). Routing/help/orchestrator cleanup: Tasks 5–6. Version/changelog: Task 8.
- Buyer-persona "VP/CFO/AE" mentions in agents/ and prospecting skills confirmed out of scope (audit: those are target contacts).
- `/ct-cro` residue: none live (audit) — CHANGELOG/TODOS history intentionally untouched.
- Vendored files never hand-edited: all three reframes go upstream, then Task 4 syncs. Plugin-owned edits only in Tasks 5–8.
- Ship (PR to main) is a separate step after this plan — use existing repo ship conventions (branch `feat/crm-hygiene` is the current worktree branch; consider a fresh branch `feat/rep-focus` before committing Task 1's sync output).
