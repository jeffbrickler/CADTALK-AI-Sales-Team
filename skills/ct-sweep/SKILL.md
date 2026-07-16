---
name: ct-sweep
description: Overnight pipeline sweep — reads the rep's Pipedrive via REST, runs hygiene + commit-gate + stuck/dark analysis, and stages a review queue for /ct-inbox. Produces files only; never writes the CRM, never sends anything. Use for 'run my sweep', nightly scheduled runs, or 'rebuild my inbox'.
---

# /ct-sweep — Overnight Pipeline Sweep

Runs unattended (nightly scheduled task) or on demand. Output: one review queue
(`inbox/REVIEW-QUEUE-{date}.md` + `.json`) the rep approves in `/ct-inbox`.

**Hard invariants (spec 2026-07-16, non-negotiable):**
1. NEVER write Pipedrive. This skill produces files only.
2. NEVER send email or any outbound message.
3. NEVER assume interactive MCP is available — all CRM reads go through
   `scripts/pipedrive_read.py` (REST token). If the Pipedrive MCP happens to be
   connected, still use the script (one code path).
4. NEVER edit plugin or reference files.

## Step 1: Locate context

1. Deal Desk root: the current working folder if it contains `crm-profile.md`,
   else ask (interactive) or abort with a clear log line (headless).
2. Read `crm-profile.md` → rep's pipeline IDs + Pipedrive Owner ID.
3. Ensure `inbox/` and `inbox/processed/` folders exist at the Deal Desk root.

## Step 2: Snapshot (deterministic)

Run: `python ${CLAUDE_PLUGIN_ROOT}/scripts/pipedrive_read.py snapshot --owner-id <id> --pipelines <ids> --out <deal-desk>/inbox/.snapshot-{YYYY-MM-DD}.json`

On exit 1 (API failure) or exit 2 (env vars missing), do NOT leave the inbox
empty — write BOTH:
1. A minimal VALID queue JSON (`inbox/REVIEW-QUEUE-{YYYY-MM-DD}.json`) containing
   a single `flag-only` item: id `{run_date}-0-flag-only-1`, deal `SWEEP`,
   evidence = the exact error, risk_note = what to fix (exit 2 → point at
   /ct-setup Section F; exit 1 → retry note). No payload. It must include
   `run_date` + `generated_at` and pass
   `python ${CLAUDE_PLUGIN_ROOT}/scripts/validate_queue.py` before writing the
   MD — same bar as normal queues.
2. The matching MD note (`inbox/REVIEW-QUEUE-{YYYY-MM-DD}.md`).

That way `/ct-inbox` surfaces the failure instead of showing "empty". Then stop.

## Step 3: Deterministic pre-pass

For every deal in the snapshot:
- Build the `validate_hygiene.py` payload (logical names — map hash keys via
  `references/pipedrive-custom-fields.md`), run with `check="at"` for the deal's
  current stage. Each gap → candidate `hygiene-fill` item (only when the fill
  value is knowable from CRM context/notes — otherwise `flag-only`).
- `_annotations.stuck` / `.dark` → candidates for Section ③.
- `_annotations.commit_review` → candidates for Section ②.
- **Section ④ Today:** every snapshot `activities_due` entry with due date
  <= today (local machine date) → one `flag-only` item (id, evidence,
  risk_note; no payload). These go into the queue JSON like all other items.

### Step 3b: Reconciliation grade (Approach C)

Grade each open deal against the CREATE contract — the required fields every deal
should carry — using `scripts/create-contract.json` (`records.deal.required`, plus
the `conditional` fields when their `when` condition holds for the deal's stage/
pipeline). This catches records that skipped the Guided Create Flow (manual web
creates, older deals) — the retro-clean half of CRM enforcement.

For each open deal:
- Compare its populated fields to the contract's required list (map logical names to
  values via the snapshot; never hand-build hash keys).
- A missing required field → a candidate `reconcile-fill` item. If conversation or
  snapshot context already knows the value, pre-fill it in the item; otherwise mark it
  ask-the-rep.
- Skip `excluded_at_create` fields — those are not expected at create time.

These candidates feed the queue as a new section ⑤ (below). Writes still happen only
on approval in `/ct-inbox`, through the sales-crm contract.

## Step 4: Agent judgment (grounded in vendored references — no new methodology)

- **Commit integrity:** run the `/ct-commit` gate criteria (skills/ct-commit) on
  each commit_review deal — apply the gate checks (Steps 2A/2B/3) to snapshot
  fields only; skip ct-commit's interactive input and write-back steps. Gate
  fail → `forecast-demote` item with the exact Forecast Category change
  proposed + evidence per check.
- **Stuck/dark:** apply `references/deal-coach.md` Section 7 protocols. Each deal
  gets the protocol step it is due for (Day-14 re-engage, Day-21 direct,
  Day-28 breakup, stalled-deal BANTED gap) as an `activity-create` or
  `flag-only` item. Draft copy is NOT written here (that is v2.15) — propose the
  activity + the protocol step name.
- **Priority:** order items within each section by deal value × risk.

## Step 5: Write the queue

`{YYYY-MM-DD}` throughout = the local machine date.

**Item ids and supersede rule:**
- Item id = `{run_date}-{deal_id}-{type}-{n}`.
- A carried item is superseded when today's findings contain the same
  (deal_id, type).
- Carried items keep their ORIGINAL id and their `carried_from` run_date.

**Order matters — old queues are moved only AFTER the new queue validates,
so a crash mid-run never loses queued items:**

1. Carry forward: read carry-forward candidates from ALL unprocessed
   `inbox/REVIEW-QUEUE-*.json` files (not just the newest). Items with
   deal_id 0 / deal `SWEEP` (failure notices) are NEVER carried forward.
   Dedup by (deal_id, type), keeping the item with the oldest `carried_from`;
   items without `carried_from` use the run_date prefix of their id as their
   age. Items not superseded by today's findings are copied into today's
   queue with `carried_from` set to their original run_date. Do NOT move
   anything yet.
2. Write `inbox/REVIEW-QUEUE-{YYYY-MM-DD}.json` — schema per
   `scripts/validate_queue.py` docstring. Payloads use LOGICAL field names only.
3. Run: `python ${CLAUDE_PLUGIN_ROOT}/scripts/validate_queue.py <queue.json>` —
   exit 0 required; on failure, fix and re-validate before writing the MD.
4. Write `inbox/REVIEW-QUEUE-{YYYY-MM-DD}.md` — the human brief, Jeff-voice
   Register 4 (direct, numbered, short), sectioned:
   ① Hygiene gaps ② Commit integrity ③ Stuck & dark ④ Today (due activities)
   ⑤ Reconcile (CREATE-contract gaps — `reconcile-fill` items from Step 3b,
   pre-filled where context knew the value, ask-the-rep otherwise; approving
   writes the field through the sales-crm contract).
   Each item shows: deal, finding, proposed action, evidence, item id.
   Header line: item counts per section + "open /ct-inbox to review".
5. ONLY NOW move the older queue pairs (`.json` + `.md`) to `inbox/processed/`
   (superseded by the validated new queue).
6. Delete the `.snapshot-*.json` scratch file.

## Step 6: Sign off

Print (or log, headless): `sweep complete: N items staged -> inbox/REVIEW-QUEUE-{date}.md`.
Do not summarize deal contents to stdout in headless mode beyond counts.
