---
name: ct-inbox
description: Review and approve the overnight sweep's staged findings — hygiene fills, forecast demotes, stuck/dark next steps. Approved writes flow through the sales-crm contract; rejections are logged for the learning loop. Use for 'inbox', 'review my queue', 'what did the sweep find'.
---

# /ct-inbox — Morning Review Queue

The approval surface for `/ct-sweep`. Target: full review in under 5 minutes.

**Hard invariants:**
1. Every approved CRM write goes through the sales-crm contract
   (`agents/sales-crm.md`) — never a hand-built field key. The queue payloads
   carry logical names; the contract resolves keys.
2. The queue review IS the confirmation (batch-review-once). Do not re-confirm
   each write after approval.
3. Nothing is written or sent for rejected/deferred items.

## Step 1: Load

1. Find the newest `inbox/REVIEW-QUEUE-*.json` at the Deal Desk root (not in
   `processed/`). None → "Inbox empty — run /ct-sweep or wait for tonight."
2. Run `python ${CLAUDE_PLUGIN_ROOT}/scripts/validate_queue.py <queue.json>`; exit 0
   required (else report the queue is corrupt and stop — never guess payloads).

## Step 2: Brief

Present the MD brief sectioned ① Hygiene ② Commit integrity ③ Stuck & dark
④ Today. Show carried-forward items with their age ("from 07-15, 2 days old").
End with: "approve all · approve <ids> · edit <id> · reject <id> <reason> · skip".

## Step 3: Approvals

- **approve all / approve <ids>** — collect the approved items' payloads.
- **edit <id>** — show the payload, take the rep's changes, re-show, then treat
  as approved-edited. Record what changed. After edits, re-run
  `python ${CLAUDE_PLUGIN_ROOT}/scripts/validate_queue.py` on the updated queue
  before write-back (keeps the hash-key guard on edited payloads).
- **reject <id> <reason>** — no write; reason required (one line is fine).
- **skip** (or unaddressed items) — stay queued; next sweep carries them forward.

## Step 4: Write-back (approved items only)

Batch by deal. For each deal, apply the merged payload through the sales-crm
contract (field updates, Forecast Category demotes, activity creates). The
batch-review-once rule applies: the Step-3 approval was the review. Tell the
sales-crm contract the Draft→Confirm requirement is already satisfied — the
Step-3 batch review IS the Confirm; pass items as pre-approved so the contract
does not re-prompt. Hygiene-gate warnings are reported in results, never
re-prompted. Report per-deal write results; any write failure keeps that item
queued and flags it.

## Step 5: Feedback log (learning-loop instrumentation, spec Section 8)

Append one JSON line per decided item to `inbox/feedback-log.jsonl`:

```json
{"ts": "<iso>", "run_date": "<queue run_date>", "item_id": "...",
 "deal": "...", "type": "...",
 "action": "approved|approved-edited|rejected",
 "edit_summary": "<what the rep changed, empty if none>",
 "reason": "<rejection reason, empty otherwise>"}
```

No analysis here — `/ct-improve` (v2.16) digests this file.

## Step 6: Close out

Remove DECIDED items (approved, approved-edited, rejected) from the queue JSON.
Then:
- **Unresolved items remain** (skipped or write-failed): rewrite the queue file
  in place — still valid per `validate_queue.py` — and LEAVE it in `inbox/`;
  the next sweep carries them forward.
- **No unresolved items remain:** move the queue pair (`.json` + `.md`) to
  `inbox/processed/`.

One-line summary: "N approved (M edited), K rejected, J carried forward."
