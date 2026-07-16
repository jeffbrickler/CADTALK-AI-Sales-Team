# v2.14 Overnight Sweep + /ct-inbox Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the first autonomous loop — a nightly headless sweep that stages CRM findings + proposed writes into a review queue, and a `/ct-inbox` skill where the rep approves them (writes then flow through the sales-crm contract), with feedback instrumentation from day one.

**Architecture:** Spec = `docs/superpowers/specs/2026-07-16-autonomous-sweep-inbox-design.md` (Sections 1–5 + Section 8 instrumentation). Deterministic layer: two new standalone Python scripts (`pipedrive_read.py` read-only REST snapshot with stuck/dark/commit annotations; `validate_queue.py` sidecar schema guard) mirroring the participants-script conventions (argparse, `requests`, exit 0/1/2, standalone). Agent layer: two new skills (`/ct-sweep` produces the queue, never writes; `/ct-inbox` reviews and writes via the sales-crm contract). Invariants: single-writer intact (new script is READ-only), nothing sends unattended, headless runs assume no interactive MCP.

**Tech Stack:** Python 3 + requests + pytest (repo conventions), markdown skills, `python scripts/validate-plugin.py` + pre-commit hook as gate.

**Branch:** `feat/autonomous-sweep` (already created off v2.13.0 main; spec committed).

**Repo root for all paths:** `C:\Users\JeffBrickler\Documents\ClaudeCode\dev\CADTALK-AI-Sales-Team-fresh\.claude\worktrees\office-hours-17991c`

---

### Task 1: `pipedrive_read.py` — pure annotation/filter functions (TDD)

**Files:**
- Create: `scripts/pipedrive_read.py`
- Test: `scripts/test_pipedrive_read.py`

- [ ] **Step 1: Write the failing tests**

```python
# scripts/test_pipedrive_read.py
"""Tests for pipedrive_read.py — pure helpers + CLI plumbing (API mocked)."""
import json
from datetime import date

import pytest

import pipedrive_read as pr


TODAY = date(2026, 7, 17)


def mkdeal(**over):
    d = {
        "id": 1, "title": "Acme", "pipeline_id": 1, "stage_id": 4,
        "status": "open",
        "stage_change_time": "2026-06-01 09:00:00",
        "last_activity_date": "2026-07-10",
        "add_time": "2026-05-01 09:00:00",
        "1a706bae5b0046828ae5a1b573c722bd96068058": None,  # Forecast Category
    }
    d.update(over)
    return d


class TestAnnotate:
    def test_days_in_stage_from_stage_change_time(self):
        a = pr.annotate_deal(mkdeal(), TODAY)
        assert a["days_in_stage"] == 46
        assert a["stuck"] is True  # > 30

    def test_stage_change_missing_falls_back_to_add_time(self):
        a = pr.annotate_deal(mkdeal(stage_change_time=None), TODAY)
        assert a["days_in_stage"] == 77

    def test_days_dark_from_last_activity(self):
        a = pr.annotate_deal(mkdeal(), TODAY)
        assert a["days_dark"] == 7
        assert a["dark"] is False  # not > 14

    def test_dark_when_no_activity_ever_uses_add_time(self):
        a = pr.annotate_deal(mkdeal(last_activity_date=None), TODAY)
        assert a["days_dark"] == 77
        assert a["dark"] is True

    def test_commit_review_flag_definitely_and_probably(self):
        key = pr.FORECAST_KEY
        assert pr.annotate_deal(mkdeal(**{key: 13}), TODAY)["commit_review"] is True
        assert pr.annotate_deal(mkdeal(**{key: "14"}), TODAY)["commit_review"] is True
        assert pr.annotate_deal(mkdeal(**{key: 15}), TODAY)["commit_review"] is False
        assert pr.annotate_deal(mkdeal(), TODAY)["commit_review"] is False

    def test_not_stuck_not_dark_fresh_deal(self):
        a = pr.annotate_deal(
            mkdeal(stage_change_time="2026-07-10 09:00:00",
                   last_activity_date="2026-07-16"), TODAY)
        assert a["stuck"] is False and a["dark"] is False


class TestFilterPipelines:
    def test_keeps_only_requested_pipelines(self):
        deals = [mkdeal(id=1, pipeline_id=1), mkdeal(id=2, pipeline_id=2),
                 mkdeal(id=3, pipeline_id=4)]
        out = pr.filter_pipelines(deals, [1, 2])
        assert [d["id"] for d in out] == [1, 2]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd <repo-root> && python -m pytest scripts/test_pipedrive_read.py -q`
Expected: FAIL / error — `ModuleNotFoundError: No module named 'pipedrive_read'`

- [ ] **Step 3: Write the module header + pure functions**

```python
#!/usr/bin/env python3
# scripts/pipedrive_read.py
"""Read-only Pipedrive snapshot for the overnight sweep (/ct-sweep).

The plugin's SECOND sanctioned direct-REST script (first: pipedrive_participants.py).
This one is READ-ONLY — it never writes Pipedrive. The single-writer rule
(agents/sales-crm.md) governs writes and is untouched. Headless sweep runs use
this because the interactive Pipedrive MCP may be absent in scheduled sessions.

Env (see /ct-setup Section F):
    PIPEDRIVE_API_TOKEN   personal API token
    PIPEDRIVE_DOMAIN      e.g. cadtalk.pipedrive.com

Usage:
    python pipedrive_read.py snapshot --owner-id 123 --pipelines 1,2 --out snap.json

Output JSON:
    {"generated_at": iso, "owner_id": N, "pipelines": [..],
     "deals": [ raw Pipedrive deal fields + "_annotations": {
         days_in_stage, days_dark, stuck, dark, commit_review } ],
     "activities_due": [ raw open activities due today or overdue ]}

Annotations (deterministic pre-pass, spec Section 3):
    stuck         days_in_stage > 30
    dark          days_dark > 14 (no touch; falls back to add_time if never touched)
    commit_review Forecast Category is Definitely (13) or Probably (14)

Exit codes: 0 success · 1 API error · 2 usage/config error
"""

import argparse
import json
import os
import sys
from datetime import date, datetime

import requests

TIMEOUT = 30
STUCK_DAYS = 30
DARK_DAYS = 14
# Forecast Category field key + commit-relevant values (13=Definitely, 14=Probably).
# Source: references/pipedrive-custom-fields.md (audited data layer).
FORECAST_KEY = "1a706bae5b0046828ae5a1b573c722bd96068058"
COMMIT_VALUES = {"13", "14"}


def _parse_day(value):
    """'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS' -> date, else None."""
    if not value:
        return None
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def annotate_deal(deal: dict, today: date) -> dict:
    staged = _parse_day(deal.get("stage_change_time")) or _parse_day(deal.get("add_time"))
    touched = _parse_day(deal.get("last_activity_date")) or _parse_day(deal.get("add_time"))
    days_in_stage = (today - staged).days if staged else 0
    days_dark = (today - touched).days if touched else 0
    forecast = deal.get(FORECAST_KEY)
    return {
        "days_in_stage": days_in_stage,
        "days_dark": days_dark,
        "stuck": days_in_stage > STUCK_DAYS,
        "dark": days_dark > DARK_DAYS,
        "commit_review": str(forecast) in COMMIT_VALUES if forecast is not None else False,
    }


def filter_pipelines(deals: list, pipelines: list) -> list:
    keep = set(pipelines)
    return [d for d in deals if d.get("pipeline_id") in keep]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest scripts/test_pipedrive_read.py -q`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/pipedrive_read.py scripts/test_pipedrive_read.py
git commit -m "feat: pipedrive_read annotation helpers — stuck/dark/commit pre-pass (TDD)"
```

### Task 2: `pipedrive_read.py` — fetch + CLI (mocked API tests)

**Files:**
- Modify: `scripts/pipedrive_read.py` (append)
- Test: `scripts/test_pipedrive_read.py` (append)

- [ ] **Step 1: Write the failing tests (mock `requests.request`)**

```python
# append to scripts/test_pipedrive_read.py

class FakeResp:
    def __init__(self, payload, status=200):
        self._payload, self.status_code = payload, status
    def json(self):
        return self._payload


def test_fetch_all_deals_paginates(monkeypatch):
    pages = {
        0: {"success": True, "data": [mkdeal(id=1)],
            "additional_data": {"pagination":
                {"more_items_in_collection": True, "next_start": 1}}},
        1: {"success": True, "data": [mkdeal(id=2)],
            "additional_data": {"pagination":
                {"more_items_in_collection": False}}},
    }
    def fake(method, url, timeout, params):
        assert method == "GET" and "/deals" in url
        return FakeResp(pages[params["start"]])
    monkeypatch.setattr(pr.requests, "request", fake)
    deals = pr.fetch_all_deals("https://x/api/v1", "tok", owner_id=9)
    assert [d["id"] for d in deals] == [1, 2]


def test_fetch_api_failure_exits_1(monkeypatch):
    monkeypatch.setattr(pr.requests, "request",
                        lambda *a, **k: FakeResp({"success": False, "error": "bad"}, 401))
    with pytest.raises(SystemExit) as e:
        pr.fetch_all_deals("https://x/api/v1", "tok", owner_id=9)
    assert e.value.code == 1


def test_main_missing_env_exits_2(monkeypatch, capsys):
    monkeypatch.delenv("PIPEDRIVE_API_TOKEN", raising=False)
    monkeypatch.delenv("PIPEDRIVE_DOMAIN", raising=False)
    with pytest.raises(SystemExit) as e:
        pr.main(["snapshot", "--owner-id", "9", "--pipelines", "1,2", "--out", "x.json"])
    assert e.value.code == 2


def test_main_writes_snapshot(monkeypatch, tmp_path):
    monkeypatch.setenv("PIPEDRIVE_API_TOKEN", "tok")
    monkeypatch.setenv("PIPEDRIVE_DOMAIN", "cadtalk.pipedrive.com")
    deals_page = {"success": True,
                  "data": [mkdeal(id=1, pipeline_id=1), mkdeal(id=2, pipeline_id=4)],
                  "additional_data": {"pagination": {"more_items_in_collection": False}}}
    acts_page = {"success": True, "data": [{"id": 7, "subject": "call", "done": False}],
                 "additional_data": {"pagination": {"more_items_in_collection": False}}}
    def fake(method, url, timeout, params):
        return FakeResp(deals_page if "/deals" in url else acts_page)
    monkeypatch.setattr(pr.requests, "request", fake)
    out = tmp_path / "snap.json"
    pr.main(["snapshot", "--owner-id", "9", "--pipelines", "1,2", "--out", str(out)])
    snap = json.loads(out.read_text(encoding="utf-8"))
    assert [d["id"] for d in snap["deals"]] == [1]          # pipeline 4 filtered out
    assert "_annotations" in snap["deals"][0]
    assert snap["activities_due"][0]["id"] == 7
    assert snap["owner_id"] == 9 and snap["pipelines"] == [1, 2]
```

- [ ] **Step 2: Run to verify the new tests fail**

Run: `python -m pytest scripts/test_pipedrive_read.py -q`
Expected: 4 new FAIL (`fetch_all_deals`/`main` not defined), Task-1 tests still pass

- [ ] **Step 3: Implement fetch + CLI**

```python
# append to scripts/pipedrive_read.py

def _get(url: str, params: dict):
    """GET wrapper: clean exit on network/API failure; never echo the URL
    (api_token rides in the query string — a traceback would leak it)."""
    try:
        resp = requests.request("GET", url, timeout=TIMEOUT, params=params)
    except requests.exceptions.RequestException as exc:
        print(f"API ERROR: network failure ({type(exc).__name__}) — check the "
              "connection and PIPEDRIVE_DOMAIN, then retry.", file=sys.stderr)
        sys.exit(1)
    body = resp.json() if resp.status_code != 204 else {}
    if resp.status_code >= 400 or not body.get("success", False):
        print(f"API ERROR: HTTP {resp.status_code} — check the token and IDs.",
              file=sys.stderr)
        sys.exit(1)
    return body


def _paginate(url: str, token: str, extra: dict) -> list:
    items, start = [], 0
    while True:
        body = _get(url, {"api_token": token, "limit": 500, "start": start, **extra})
        items.extend(body.get("data") or [])
        page = (body.get("additional_data") or {}).get("pagination") or {}
        if not page.get("more_items_in_collection"):
            return items
        start = page.get("next_start", start + 500)


def fetch_all_deals(base: str, token: str, owner_id: int) -> list:
    return _paginate(f"{base}/deals", token, {"status": "open", "user_id": owner_id})


def fetch_open_activities(base: str, token: str, owner_id: int) -> list:
    return _paginate(f"{base}/activities", token, {"user_id": owner_id, "done": 0})


def base_url(domain: str) -> str:
    domain = domain.strip().rstrip("/")
    for prefix in ("https://", "http://"):
        if domain.startswith(prefix):
            domain = domain[len(prefix):]
    return f"https://{domain}/api/v1"


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(prog="pipedrive_read.py",
                                     description="Read-only Pipedrive snapshot.")
    sub = parser.add_subparsers(dest="command", required=True)
    snap = sub.add_parser("snapshot", help="write a snapshot JSON")
    snap.add_argument("--owner-id", type=int, required=True)
    snap.add_argument("--pipelines", required=True,
                      help="comma-separated pipeline ids, e.g. 1,2")
    snap.add_argument("--out", required=True, help="output JSON path")
    args = parser.parse_args(argv)

    token = os.environ.get("PIPEDRIVE_API_TOKEN")
    domain = os.environ.get("PIPEDRIVE_DOMAIN")
    if not token or not domain:
        print("CONFIG ERROR: set PIPEDRIVE_API_TOKEN and PIPEDRIVE_DOMAIN "
              "(see /ct-setup Section F).", file=sys.stderr)
        sys.exit(2)

    base = base_url(domain)
    pipelines = [int(p) for p in args.pipelines.split(",") if p.strip()]
    today = date.today()
    deals = filter_pipelines(fetch_all_deals(base, token, args.owner_id), pipelines)
    for d in deals:
        d["_annotations"] = annotate_deal(d, today)
    snapshot = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "owner_id": args.owner_id,
        "pipelines": pipelines,
        "deals": deals,
        "activities_due": fetch_open_activities(base, token, args.owner_id),
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, ensure_ascii=False, indent=1)
    print(f"snapshot: {len(deals)} deals, "
          f"{len(snapshot['activities_due'])} open activities -> {args.out}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run full script tests**

Run: `python -m pytest scripts/test_pipedrive_read.py -q`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/pipedrive_read.py scripts/test_pipedrive_read.py
git commit -m "feat: pipedrive_read snapshot CLI — paginated read-only REST fetch"
```

### Task 3: `validate_queue.py` — queue sidecar schema guard (TDD)

**Files:**
- Create: `scripts/validate_queue.py`
- Test: `scripts/test_validate_queue.py`

- [ ] **Step 1: Write the failing tests**

```python
# scripts/test_validate_queue.py
"""Tests for validate_queue.py — review-queue sidecar schema guard."""
import json

import pytest

import validate_queue as vq


def mkitem(**over):
    item = {
        "id": "2026-07-17-001",
        "deal": "Acme Fabrication",
        "deal_id": 123,
        "type": "hygiene-fill",
        "evidence": "MEDDPICC-Champion blank at Discovery (due at Qualify)",
        "proposed_payload": {"MEDDPICC-Champion": "Sarah Chen, CFO"},
        "risk_note": "Blank champion at stage move will trip the hygiene gate.",
    }
    item.update(over)
    return item


def mkqueue(items):
    return {"run_date": "2026-07-17", "generated_at": "2026-07-17T05:02:11",
            "items": items}


def check(queue):
    return vq.validate(queue)  # returns list of problem strings


class TestSchema:
    def test_valid_queue_no_problems(self):
        assert check(mkqueue([mkitem()])) == []

    def test_unknown_type_rejected(self):
        probs = check(mkqueue([mkitem(type="auto-send-email")]))
        assert any("type" in p for p in probs)

    def test_duplicate_ids_rejected(self):
        probs = check(mkqueue([mkitem(), mkitem()]))
        assert any("duplicate" in p for p in probs)

    def test_missing_required_key_rejected(self):
        bad = mkitem(); del bad["risk_note"]
        probs = check(mkqueue([bad]))
        assert any("risk_note" in p for p in probs)

    def test_hash_key_in_payload_rejected(self):
        # payloads carry LOGICAL names only; 40-hex API keys resolve in sales-crm
        bad = mkitem(proposed_payload={
            "1a706bae5b0046828ae5a1b573c722bd96068058": 15})
        probs = check(mkqueue([bad]))
        assert any("hash" in p.lower() for p in probs)

    def test_flag_only_needs_no_payload(self):
        item = mkitem(type="flag-only"); del item["proposed_payload"]
        assert check(mkqueue([item])) == []

    def test_actionable_type_requires_payload(self):
        item = mkitem(type="forecast-demote"); del item["proposed_payload"]
        probs = check(mkqueue([item]))
        assert any("proposed_payload" in p for p in probs)

    def test_carried_from_optional_and_valid(self):
        assert check(mkqueue([mkitem(carried_from="2026-07-16")])) == []


class TestCli:
    def test_cli_exit_0_on_valid(self, tmp_path):
        f = tmp_path / "q.json"
        f.write_text(json.dumps(mkqueue([mkitem()])), encoding="utf-8")
        with pytest.raises(SystemExit) as e:
            vq.main([str(f)])
        assert e.value.code == 0

    def test_cli_exit_1_on_problems(self, tmp_path):
        f = tmp_path / "q.json"
        f.write_text(json.dumps(mkqueue([mkitem(type="nope")])), encoding="utf-8")
        with pytest.raises(SystemExit) as e:
            vq.main([str(f)])
        assert e.value.code == 1

    def test_cli_exit_2_on_unreadable(self, tmp_path):
        with pytest.raises(SystemExit) as e:
            vq.main([str(tmp_path / "missing.json")])
        assert e.value.code == 2
```

- [ ] **Step 2: Run to verify failure**

Run: `python -m pytest scripts/test_validate_queue.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'validate_queue'`

- [ ] **Step 3: Implement**

```python
#!/usr/bin/env python3
# scripts/validate_queue.py
"""Validate a REVIEW-QUEUE JSON sidecar (spec Section 4).

/ct-sweep runs this on the sidecar it just wrote; /ct-inbox runs it before
presenting a queue. Guards the machine payload the approval flow trusts.

Rules:
  * queue: run_date, generated_at, items[] required
  * item required keys: id, deal, deal_id, type, evidence, risk_note
  * type in {hygiene-fill, forecast-demote, activity-create, followup-draft, flag-only}
  * ids unique within the queue
  * proposed_payload REQUIRED for every type except flag-only
  * payload keys are LOGICAL field names — a 40-char hex key is a spec violation
    (hash keys resolve at write time inside the sales-crm contract)
  * carried_from optional (YYYY-MM-DD of the run the item first appeared in)

Exit codes: 0 valid · 1 problems (all listed on stderr) · 2 usage/spec error
"""
import json
import re
import sys
from pathlib import Path

TYPES = {"hygiene-fill", "forecast-demote", "activity-create",
         "followup-draft", "flag-only"}
ITEM_REQUIRED = ("id", "deal", "deal_id", "type", "evidence", "risk_note")
HASH_KEY = re.compile(r"^[0-9a-f]{40}$")


def validate(queue: dict) -> list:
    problems = []
    for key in ("run_date", "generated_at", "items"):
        if key not in queue:
            problems.append(f"queue missing required key: {key}")
    items = queue.get("items")
    if not isinstance(items, list):
        problems.append("items must be a list")
        return problems
    seen = set()
    for i, item in enumerate(items):
        where = f"item[{i}] ({item.get('id', '?')})"
        for key in ITEM_REQUIRED:
            if key not in item:
                problems.append(f"{where}: missing required key: {key}")
        itype = item.get("type")
        if itype not in TYPES:
            problems.append(f"{where}: unknown type: {itype!r}")
        iid = item.get("id")
        if iid in seen:
            problems.append(f"{where}: duplicate id")
        seen.add(iid)
        payload = item.get("proposed_payload")
        if itype in TYPES - {"flag-only"} and not payload:
            problems.append(f"{where}: proposed_payload required for type {itype}")
        for pkey in (payload or {}):
            if HASH_KEY.match(str(pkey)):
                problems.append(
                    f"{where}: payload key looks like a hash API key ({pkey}); "
                    "use logical field names only")
    return problems


def main(argv=None) -> None:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 1:
        print("usage: validate_queue.py <queue.json>", file=sys.stderr)
        sys.exit(2)
    path = Path(argv[0])
    try:
        queue = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"SPEC ERROR: cannot read queue: {exc}", file=sys.stderr)
        sys.exit(2)
    problems = validate(queue)
    if problems:
        for p in problems:
            print(f"QUEUE ERROR: {p}", file=sys.stderr)
        sys.exit(1)
    print(f"queue OK: {len(queue['items'])} item(s)")
    sys.exit(0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests**

Run: `python -m pytest scripts/test_validate_queue.py -q`
Expected: all PASS. Then full suite: `python -m pytest scripts/ -q` — everything passes.

- [ ] **Step 5: Commit**

```bash
git add scripts/validate_queue.py scripts/test_validate_queue.py
git commit -m "feat: validate_queue — review-queue sidecar schema guard (TDD)"
```

### Task 4: `/ct-sweep` skill

**Files:**
- Create: `skills/ct-sweep/SKILL.md`

- [ ] **Step 1: Write the skill.** Full content:

````markdown
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
````

- [ ] **Step 2: Validate + commit**

Run: `python scripts/validate-plugin.py`
Expected: `OK — 0 failures` (single-line description rule satisfied).

```bash
git add skills/ct-sweep
git commit -m "feat: /ct-sweep — overnight sweep skill, files-only output"
```

### Task 5: `/ct-inbox` skill (+ feedback instrumentation)

**Files:**
- Create: `skills/ct-inbox/SKILL.md`

- [ ] **Step 1: Write the skill.** Full content:

````markdown
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
2. Run `python <plugin>/scripts/validate_queue.py <queue.json>`; exit 0
   required (else report the queue is corrupt and stop — never guess payloads).

## Step 2: Brief

Present the MD brief sectioned ① Hygiene ② Commit integrity ③ Stuck & dark
④ Today. Show carried-forward items with their age ("from 07-15, 2 days old").
End with: "approve all · approve <ids> · edit <id> · reject <id> <reason> · skip".

## Step 3: Approvals

- **approve all / approve <ids>** — collect the approved items' payloads.
- **edit <id>** — show the payload, take the rep's changes, re-show, then treat
  as approved-edited. Record what changed.
- **reject <id> <reason>** — no write; reason required (one line is fine).
- **skip** (or unaddressed items) — stay queued; next sweep carries them forward.

## Step 4: Write-back (approved items only)

Batch by deal. For each deal, apply the merged payload through the sales-crm
contract (field updates, Forecast Category demotes, activity creates). The
batch-review-once rule applies: the Step-3 approval was the review. Report
per-deal write results; any write failure keeps that item queued and flags it.

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

Move the queue pair (`.json` + `.md`) to `inbox/processed/`. If items were
skipped, note they'll reappear in tomorrow's queue. One-line summary:
"N approved (M edited), K rejected, J carried forward."
````

- [ ] **Step 2: Validate + commit**

Run: `python scripts/validate-plugin.py` → OK.

```bash
git add skills/ct-inbox
git commit -m "feat: /ct-inbox — approval queue + feedback-log instrumentation"
```

### Task 6: Scheduling — `/ct-setup` Section G

**Files:**
- Modify: `skills/ct-setup/SKILL.md` (append a new section after Section F)

- [ ] **Step 1: Read the tail of `skills/ct-setup/SKILL.md`** (find Section F's end and match its formatting).

- [ ] **Step 2: Append Section G.** Content:

````markdown
## Section G — Schedule the overnight sweep (optional but recommended)

The sweep (`/ct-sweep`) can run nightly so the review queue is ready each
morning. Requires Section F (API token env vars) to be complete first —
verify with: `python scripts/pipedrive_read.py snapshot --owner-id <id> --pipelines <ids> --out %TEMP%\sweep-test.json` (expect a one-line success).

**Primary — Claude Code scheduled task:** create a schedule that runs the
prompt `/ct-sweep` weeknights at 5:00am local, working directory = the rep's
Deal Desk folder. (In a Claude session: "schedule /ct-sweep weeknights 5am in
this folder".)

**Fallback — Windows Task Scheduler:**
```powershell
schtasks /Create /TN "CADTALK Sweep" /SC WEEKLY /D MON,TUE,WED,THU,FRI /ST 05:00 `
  /TR "cmd /c cd /d \"<Deal Desk path>\" && claude -p \"/ct-sweep\""
```

**Verify:** next morning, `inbox/REVIEW-QUEUE-{date}.md` exists. First week is
a watched pilot — the rep reviews every item; success = <5-min review, >70%
items approved unedited, zero unapproved writes.
````

- [ ] **Step 3: Validate + commit**

```bash
python scripts/validate-plugin.py && git add skills/ct-setup && git commit -m "feat: ct-setup Section G — schedule the overnight sweep"
```

### Task 7: Routing + single-writer doc updates

**Files:**
- Modify: `CLAUDE.md` (routing table + single-writer section)
- Modify: `skills/ct-help/SKILL.md` (quick list + two full entries)
- Modify: `skills/ct-sales/SKILL.md` (cross-skill references)

- [ ] **Step 1: CLAUDE.md routing table** — add two rows after the `/ct-hygiene` row:

```markdown
| Overnight sweep, "run my sweep", stage my review queue | `/ct-sweep` |
| Morning review, "inbox", approve sweep findings | `/ct-inbox` |
```

- [ ] **Step 2: CLAUDE.md single-writer section** — after the participants-exception sentence (`**One sanctioned exception:** ... every other write stays in the sales-crm contract.`), append to the same paragraph:

```markdown
`scripts/pipedrive_read.py` is the sanctioned READ path for headless sweep runs (the interactive MCP may be absent in scheduled sessions) — read-only, so the single-writer rule is unaffected.
```

- [ ] **Step 3: ct-help** — in the quick list add under the CRM/pipeline group:

```
/ct-sweep                       Overnight pipeline sweep — stages the review queue (files only, no writes)
/ct-inbox                       Morning review — approve/reject the sweep's staged findings
```

Add two full entries (same format as existing ones) after the ct-hygiene entry: WHAT IT DOES / WHEN TO RUN IT / HOW TO USE IT / WHAT YOU'LL GET / COMMON MISTAKES. ct-sweep mistakes: "Expecting it to write the CRM — it stages only; approval happens in /ct-inbox." ct-inbox mistakes: "Re-confirming every write after approving — the queue review IS the confirm (batch-review-once)."

- [ ] **Step 4: ct-sales Cross-Skill References** — add:

```markdown
- `/ct-sweep` stages nightly findings (hygiene, commit integrity, stuck/dark) into the review queue; `/ct-inbox` is where the rep approves them — approved writes flow through the sales-crm contract
```

- [ ] **Step 5: Validate + commit**

```bash
python scripts/validate-plugin.py && git add CLAUDE.md skills/ct-help skills/ct-sales && git commit -m "docs: route /ct-sweep + /ct-inbox; document sanctioned read path"
```

### Task 8: Version bump + changelog + full gate

**Files:**
- Modify: `.claude-plugin/plugin.json` (`"version": "2.13.0"` → `"2.14.0"`)
- Modify: `CHANGELOG.md` (new entry above v2.13.0)

- [ ] **Step 1: CHANGELOG entry**

```markdown
## v2.14.0 — <today's date>

Overnight Sweep + Inbox: the first autonomous loop. A nightly headless sweep stages CRM findings and proposed writes into a review queue; the rep approves in `/ct-inbox` and only then do writes flow through the sales-crm contract. Spec: `docs/superpowers/specs/2026-07-16-autonomous-sweep-inbox-design.md`.

### Added
- **`/ct-sweep`** — overnight pipeline sweep (hygiene gaps, commit-gate integrity, stuck >30d / dark >14d with deal-coach protocol steps, today's due activities). Files only: never writes the CRM, never sends, never assumes interactive MCP.
- **`/ct-inbox`** — morning approval queue: approve all / per-item / edit-then-approve / reject-with-reason; approved writes via the sales-crm contract (batch-review-once); processed queues archived.
- **`scripts/pipedrive_read.py`** (+tests) — second sanctioned direct-REST script, READ-ONLY (headless runs can't use the interactive MCP); snapshot with stuck/dark/commit annotations.
- **`scripts/validate_queue.py`** (+tests) — review-queue sidecar schema guard; payloads carry logical field names only (hash keys resolve in the sales-crm contract).
- **Feedback instrumentation** — `inbox/feedback-log.jsonl` records approve/edit/reject per item (fuel for the v2.16 `/ct-improve` learning loop).
- **`/ct-setup` Section G** — schedule the nightly sweep (Claude scheduled task; Task Scheduler fallback).
```

- [ ] **Step 2: Full gate**

Run: `python -m pytest scripts/ -q` — expected: all pass (55 existing + ~17 new).
Run: `python scripts/validate-plugin.py` — expected: OK.

- [ ] **Step 3: Commit**

```bash
git add -A && git commit -m "chore: v2.14.0 — overnight sweep + inbox; changelog + version bump"
```

### Task 9: Pilot checklist → TODOS.md

**Files:**
- Modify: `TODOS.md`

- [ ] **Step 1: Append**

```markdown
## v2.14 pilot (Jeff, one week — spec Section 7 metrics)
- [ ] /ct-setup Section G: schedule nightly sweep (env vars already set)
- [ ] Manual first run: `/ct-sweep` in Deal Desk, inspect queue MD + JSON
- [ ] Daily: /ct-inbox review — track review time (<5 min target)
- [ ] End of week: % items approved unedited (>70% target); zero unapproved writes (hard)
- [ ] Feed verdict into v2.15 (meeting lifecycle) go/no-go
```

- [ ] **Step 2: Commit**

```bash
git add TODOS.md && git commit -m "docs: v2.14 pilot checklist"
```

---

## Self-Review Notes

- **Spec coverage:** S1 runner→Task 6; S2 read layer→Tasks 1–2; S3 sweep→Task 4; S4 queue→Tasks 3–4; S5 inbox→Task 5; S8 instrumentation→Task 5 Step 5 + changelog. v2.15/v2.16 intentionally out of scope (own plans).
- **Type consistency:** queue item keys (`id, deal, deal_id, type, evidence, proposed_payload, risk_note, carried_from`) identical across validate_queue.py, its tests, ct-sweep Step 5, ct-inbox Steps 1–5. `FORECAST_KEY` value matches `references/pipedrive-custom-fields.md`.
- **Windows note:** run pytest from repo root so `scripts/` is the rootdir pytest picks up (matches existing test invocation). CRLF warnings are normal.
- **Ship:** after Task 9 → PR to main per repo convention (merge origin/main first if it moved; diff against origin/main, not local main).
