# Autonomous Sweep + Inbox + Learning Loop — Design Spec

**Date:** 2026-07-16
**Author:** Jeff Brickler + Claude (brainstorming session, all sections user-approved)
**Status:** APPROVED design, pending implementation plan

## Goal

Move the plugin from all-pull (rep types `/ct-*`, waits) to independent execution with
human-in-the-loop approval: agents do the deal-management work unattended, the rep
approves in one short daily review. Jeff is currently the only seller and needs time
back for strategy; the design must transfer unchanged to hired reps later.

**Release train:**
- **v2.14 — Overnight Sweep + `/ct-inbox`** (+ feedback instrumentation)
- **v2.15 — Meeting lifecycle** (post-call + pre-meeting feeds into the same inbox)
- **v2.16 — `/ct-improve`** (the learning loop that folds rep feedback back into the system)

## Non-negotiable invariants

1. **Single-writer rule stands.** No autonomous run ever writes Pipedrive. All writes
   happen in an interactive approval session through the sales-crm contract.
2. **Nothing sends unattended.** Drafted emails/follow-ups are staged, never sent, by
   autonomous runs.
3. **The system never edits its own rules unapproved.** Learnings are proposed, the rep
   approves, then they are applied (same bar as CRM writes).
4. **Headless runs assume no interactive MCP.** Pipedrive/Fireflies connectors are
   interactively authenticated and may be absent in scheduled runs — autonomous reads go
   through token-auth REST scripts only.

---

## Section 1: Runner + scheduling

- Nightly weeknight scheduled task on the rep's machine, ~5:00am local, running headless
  in the rep's Deal Desk folder, invoking the new `/ct-sweep` skill.
- Primary mechanism: Claude Code scheduled tasks. Documented fallback: Windows Task
  Scheduler → `claude -p "/ct-sweep"`.
- `/ct-sweep` is also manually invocable any time ("run my sweep now") — same behavior.
- The run produces files only (queue + logs). It never writes the CRM, never sends
  anything, never edits plugin/reference files.

## Section 2: Read layer — `scripts/pipedrive_read.py` (read-only REST)

- Second sanctioned direct-REST script, alongside `pipedrive_participants.py`. This one
  is **read-only**; the single-writer rule governs writes and is untouched. CLAUDE.md
  gains one sentence documenting the read exception.
- Auth: same env vars as participants (`PIPEDRIVE_API_TOKEN`, `PIPEDRIVE_DOMAIN`),
  already configured via `/ct-setup` Section F.
- Pulls, scoped by the rep's `crm-profile.md` (pipelines + Owner ID):
  open deals + custom fields, activities due today, last-touch recency, stage age.
- Emits one JSON snapshot per run (timestamped, in a run-scratch area, not the inbox).
- pytest coverage per repo convention.

## Section 3: Sweep agent — `/ct-sweep` skill + `sales-sweep` agent

Two-layer judgment over the snapshot:

1. **Deterministic pre-pass (scripts, no model):**
   - `validate_hygiene.py` per deal (exists — hygiene gaps due at current stage);
   - stuck (>30 days in stage) and dark (>14 days no touch) day-math;
   - Definitely/Probably deals flagged for commit-gate review.
2. **Agent layer (judgment, grounded in existing vendored references — no new
   methodology):**
   - commit gate per flagged deal (ct-commit criteria);
   - coach-protocol next step for stuck/dark deals (deal-coach Section 7 protocols);
   - priority ranking across findings.

Output: the review queue (Section 4). Brief prose in Jeff-voice Register 4 (internal:
direct, numbered, short).

## Section 4: Review queue format

- Per run: `Deal Desk/inbox/REVIEW-QUEUE-{YYYY-MM-DD}.md` (human brief) +
  `REVIEW-QUEUE-{YYYY-MM-DD}.json` sidecar (machine payload).
- Item schema (validated by new `scripts/validate_queue.py`, pytest per convention):
  - `id` — stable per item
  - `deal` — Pipedrive deal name/id
  - `type` — `hygiene-fill` | `forecast-demote` | `activity-create` | `followup-draft` | `flag-only`
  - `evidence` — source of the proposal (CRM field state, transcript, day-math)
  - `proposed_payload` — **logical field names only**; hash keys resolve at write time
    inside the sales-crm contract (existing convention)
  - `risk_note` — what happens if approved/ignored
- Carry-forward: unprocessed items from prior runs appear in the next queue with an age
  marker; a new run supersedes rather than duplicates.

## Section 5: `/ct-inbox` skill

- Loads latest queue + carryovers → sectioned brief:
  ① hygiene gaps ② commit integrity (proposed demotes) ③ stuck/dark + coach next step
  ④ today (due activities/meetings).
- Approval flows: **approve all**, per-item, edit-then-approve, reject-with-reason.
- Approved writes flow through the **sales-crm contract, batch-review-once** — the queue
  review IS the confirm; no double-confirmation.
- Rejections and edit deltas are logged (Section 8 instrumentation).
- Processed queues move to `Deal Desk/inbox/processed/`.
- Target: full review in under 5 minutes.

## Section 6: Phase 2 — meeting lifecycle (v2.15)

Same runner, same inbox, two new feeds:

- **Post-call:** Fireflies polled via **API token** (not the interactive MCP) with a
  last-run watermark. Each new transcript →
  WGLL score (ct-score) + voice-compliant follow-up draft + CRM field proposals →
  inbox items (`followup-draft` etc.). Drafts never auto-send; approved drafts are sent
  from the interactive session.
- **Pre-meeting:** today's due activities/deals from the Pipedrive snapshot → prep
  briefs staged overnight (ct-prep structure). Calendar-based triggers are deferred
  until a token-auth calendar path exists — Pipedrive activities cover the majority
  case.

## Section 7: Multi-rep + testing

- Per-rep by construction: `crm-profile.md` scopes pipelines/owner; queue lives in each
  rep's own Deal Desk; API tokens per rep; no shared state. New-hire setup =
  `/ct-setup` + schedule the task.
- Testing: pytest for `pipedrive_read.py` and `validate_queue.py`; `--dry-run` mode on
  the sweep; then a one-week watched pilot on Jeff with metrics:
  - brief review time **< 5 min**
  - **> 70%** of items approved unedited
  - **zero** unapproved writes (hard requirement)

## Section 8: Learning loop — `/ct-improve` (v2.16; instrumentation ships in v2.14)

**Signals (captured from v2.14, zero extra rep effort):**
- `/ct-inbox` rejections with reason + edit-then-approve deltas →
  `Deal Desk/inbox/feedback-log.jsonl` (structured: item type, what changed, why).
- Draft-vs-sent email diffs (what the rep changed before sending) → same log.
- In-session corrections ("never/always/stop doing X") → auto-memory as today.

**Digest (weekly scheduled, or `/ct-improve` on demand):** a learning agent clusters the
log + memory and proposes **learning cards**: observation (with evidence count ≥ 3 —
one-off noise never graduates), proposed change, and a **tier**:
- **PERSONAL** → the rep's `rep-prefs.md` (new file next to `crm-profile.md`; sweep +
  content skills read it) or the rep's personal voice skill.
- **TEAM STANDARD** → drafted edit to the right upstream repo (`cadtalk-voice`,
  `commit-gate-scorecard`, `cro-deal-coach`, `discovery-review-scorecard`) or a plugin
  reference.

**Approval + application:** rep reviews cards like inbox items — approve / reject /
re-tier. Approved PERSONAL → prefs file updated immediately. Approved TEAM → upstream
commit + VERSION bump + `sync-skills.sh` + plugin ship (the established externalized-
skill flow, automated to Draft→approve).

**Boundary:** dev-workspace learning (build sessions) belongs to the `si` plugin and is
out of scope here; `/ct-improve` is the rep-facing product loop.

## Decisions log (from brainstorming)

| Decision | Choice |
|---|---|
| First autonomous loops | Scheduled pipeline sweep, then meeting lifecycle (both; sequenced) |
| Approval surface | Review queue files + `/ct-inbox` in Cowork |
| Cadence/content | Nightly weeknights; full brief (hygiene, commit, stuck/dark, today) |
| Build approach | A — staged autonomy on existing rails (vs cloud routines / agent-first rewrite) |
| Learning tiers | Two-tier (PERSONAL vs TEAM STANDARD), classified at review |
