#!/usr/bin/env python3
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
