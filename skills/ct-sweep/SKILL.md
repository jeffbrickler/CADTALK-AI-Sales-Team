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

Run: `python <plugin>/scripts/pipedrive_read.py snapshot --owner-id <id> --pipelines <ids> --out <deal-desk>/inbox/.snapshot-{YYYY-MM-DD}.json`

Exit 2 = env vars missing → write a one-line queue MD saying setup is incomplete
(point at /ct-setup Section F) and stop. Exit 1 = API failure → same, retry note.

## Step 3: Deterministic pre-pass

For every deal in the snapshot:
- Build the `validate_hygiene.py` payload (logical names — map hash keys via
  `references/pipedrive-custom-fields.md`), run with `check="at"` for the deal's
  current stage. Each gap → candidate `hygiene-fill` item (only when the fill
  value is knowable from CRM context/notes — otherwise `flag-only`).
- `_annotations.stuck` / `.dark` → candidates for Section ③.
- `_annotations.commit_review` → candidates for Section ②.

## Step 4: Agent judgment (grounded in vendored references — no new methodology)

- **Commit integrity:** run the `/ct-commit` gate criteria (skills/ct-commit) on
  each commit_review deal using snapshot fields. Gate fail → `forecast-demote`
  item with the exact Forecast Category change proposed + evidence per check.
- **Stuck/dark:** apply `references/deal-coach.md` Section 7 protocols. Each deal
  gets the protocol step it is due for (Day-14 re-engage, Day-21 direct,
  Day-28 breakup, stalled-deal BANTED gap) as an `activity-create` or
  `flag-only` item. Draft copy is NOT written here (that is v2.15) — propose the
  activity + the protocol step name.
- **Priority:** order items within each section by deal value × risk.

## Step 5: Write the queue

1. Carry forward: read the newest unprocessed `inbox/REVIEW-QUEUE-*.json` (if
   any); items not superseded by today's findings are copied in with
   `carried_from` set to their original run_date. Then move that older queue
   pair to `inbox/processed/` (superseded).
2. Write `inbox/REVIEW-QUEUE-{YYYY-MM-DD}.json` — schema per
   `scripts/validate_queue.py` docstring. Payloads use LOGICAL field names only.
3. Run: `python <plugin>/scripts/validate_queue.py <queue.json>` — exit 0
   required; on failure, fix and re-validate before writing the MD.
4. Write `inbox/REVIEW-QUEUE-{YYYY-MM-DD}.md` — the human brief, Jeff-voice
   Register 4 (direct, numbered, short), sectioned:
   ① Hygiene gaps ② Commit integrity ③ Stuck & dark ④ Today (due activities).
   Each item shows: deal, finding, proposed action, evidence, item id.
   Header line: item counts per section + "open /ct-inbox to review".
5. Delete the `.snapshot-*.json` scratch file.

## Step 6: Sign off

Print (or log, headless): `sweep complete: N items staged -> inbox/REVIEW-QUEUE-{date}.md`.
Do not summarize deal contents to stdout in headless mode beyond counts.
