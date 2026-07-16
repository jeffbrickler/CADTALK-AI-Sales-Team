#!/usr/bin/env python3
"""Compute CRM hygiene gaps against scripts/hygiene-contract.json.

The gap computer for the CADTALK CRM hygiene flow (design doc 2026-07-15).
ct-hygiene runs this on the current Pipedrive state BEFORE proposing fills,
and the sales-crm STAGE MOVE gate runs it with check="entering" before a move.
Read-only: this script never talks to Pipedrive; the caller supplies state.

Usage:
    python validate_hygiene.py <payload.json>
    python validate_hygiene.py -            (read payload from stdin)

Payload shape (logical field NAMES as keys — never hash API keys):

    {
      "stage": "propose",             # one of contract stage_order
      "check": "at",                  # "at" (audit) or "entering" (gate)
      "flags": {"demo_completed": true, "proposal_sent": false,
                 "partner_sourced": false, "compelling_event_named": true},
      "deal":         {"Forecast Category": 14, ...},
      "organization": {"Organization Type": 19, ...},
      "persons":      [{"Name": "...", "Email": "...", "Role": ["Champion"],
                        "is_primary": true, ...}],
      "participants_count": 3
    }

Dueness semantics:
  * check="at" stage S      -> every field with due_by_stage index <= index(S)
  * check="entering" stage T -> every field with due_by_stage index <  index(T)
  * applies_when "always" applies; any other value is a flag name — the
    field only applies when payload flags[<name>] is true.
  * Person tiering: a person is KEY if is_primary OR Role intersects
    contract key_roles; key persons need key_required, others other_required.
  * Fields listed in contract "excluded" are never checked (CS-owned).
  * ALL gaps are reported, not just the first.

Exit codes:
    0  no gaps
    1  hygiene gaps — every one listed on stderr
    2  usage/spec error (unreadable payload, malformed JSON, unknown
       stage/check, missing/malformed contract file)
"""

import json
import sys
from pathlib import Path

CONTRACT_PATH = Path(__file__).resolve().parent / "hygiene-contract.json"


def fail_spec(msg: str) -> "NoReturn":  # noqa: F821 - py<3.11 friendly
    print(f"SPEC ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


def load_contract() -> dict:
    if not CONTRACT_PATH.is_file():
        fail_spec(f"contract file not found: {CONTRACT_PATH}")
    try:
        return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail_spec(f"contract file is not valid JSON: {exc}")


def load_payload(argv: list) -> dict:
    if len(argv) != 2:
        fail_spec("usage: validate_hygiene.py <payload.json | ->")
    raw_source = argv[1]
    try:
        raw = sys.stdin.read() if raw_source == "-" else Path(raw_source).read_text(encoding="utf-8")
    except OSError as exc:
        fail_spec(f"cannot read payload: {exc}")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail_spec(f"payload is not valid JSON: {exc}")
    if not isinstance(payload, dict):
        fail_spec("payload must be a JSON object")
    return payload


def is_filled(record: dict, field: str) -> bool:
    value = record.get(field)
    if value is None:
        return False
    if isinstance(value, str) and not value.strip():
        return False
    if isinstance(value, list) and not value:
        return False
    return True


def due_indexes(contract: dict, payload: dict) -> tuple:
    """Return (stage_order, max_due_index) for this payload or spec-fail."""
    stage_order = contract.get("stage_order", [])
    stage = payload.get("stage")
    if stage not in stage_order:
        fail_spec(f"unknown stage {stage!r} — expected one of: {', '.join(stage_order)}")
    check = payload.get("check", "at")
    idx = stage_order.index(stage)
    if check == "at":
        return stage_order, idx
    if check == "entering":
        return stage_order, idx - 1
    fail_spec(f"unknown check {check!r} — expected 'at' or 'entering'")


def applies(entry: dict, flags: dict) -> bool:
    when = entry.get("applies_when", "always")
    if when == "always":
        return True
    return bool(flags.get(when))


def field_gaps(contract: dict, payload: dict, max_due: int) -> list:
    gaps = []
    stage_order = contract["stage_order"]
    flags = payload.get("flags", {}) or {}
    excluded = set(contract.get("excluded", []))
    for record_name in ("deal", "organization"):
        record = payload.get(record_name)
        record = record if isinstance(record, dict) else {}
        for entry in contract.get(record_name, []):
            field = entry.get("field")
            if field in excluded:
                continue
            due = entry.get("due_by_stage")
            if due not in stage_order:
                fail_spec(f"contract {record_name}.{field} has unknown due_by_stage {due!r}")
            if stage_order.index(due) > max_due:
                continue
            if not applies(entry, flags):
                continue
            if not is_filled(record, field):
                gaps.append(
                    f"{record_name}.{field} (due by {due}{'' if entry.get('applies_when', 'always') == 'always' else ' — ' + entry['applies_when']})"
                )
    return gaps


def person_gaps(contract: dict, payload: dict, max_due: int) -> list:
    spec = contract.get("person", {})
    stage_order = contract["stage_order"]
    due = spec.get("due_by_stage", "close")
    if due not in stage_order:
        fail_spec(f"contract person.due_by_stage {due!r} not in stage_order")
    if stage_order.index(due) > max_due:
        return []
    key_roles = set(spec.get("key_roles", []))
    gaps = []
    persons = payload.get("persons")
    persons = persons if isinstance(persons, list) else []
    for i, person in enumerate(persons):
        if not isinstance(person, dict):
            continue
        roles = person.get("Role")
        roles = set(roles) if isinstance(roles, list) else set()
        is_key = bool(person.get("is_primary")) or bool(roles & key_roles)
        required = spec.get("key_required" if is_key else "other_required", [])
        label = person.get("Name") or f"persons[{i}]"
        tier = "key contact" if is_key else "contact"
        for field in required:
            if not is_filled(person, field):
                gaps.append(f"person.{field} missing on {tier} {label!r} (due by {due})")
    return gaps


def participant_gaps(contract: dict, payload: dict, max_due: int) -> list:
    spec = contract.get("participants", {})
    stage_order = contract["stage_order"]
    due = spec.get("due_by_stage", "close")
    if due not in stage_order:
        fail_spec(f"contract participants.due_by_stage {due!r} not in stage_order")
    if stage_order.index(due) > max_due:
        return []
    minimum = int(spec.get("min", 0))
    count = payload.get("participants_count")
    count = count if isinstance(count, int) else 0
    if count < minimum:
        return [
            f"participants: {count} attached, minimum {minimum} (due by {due} — multi-threading floor)"
        ]
    return []


def validate(contract: dict, payload: dict) -> list:
    _, max_due = due_indexes(contract, payload)
    gaps = []
    gaps += field_gaps(contract, payload, max_due)
    gaps += person_gaps(contract, payload, max_due)
    gaps += participant_gaps(contract, payload, max_due)
    return gaps


def main(argv: list) -> int:
    contract = load_contract()
    payload = load_payload(argv)
    gaps = validate(contract, payload)
    if gaps:
        print("HYGIENE GAPS:", file=sys.stderr)
        for item in gaps:
            print(f"  - {item}", file=sys.stderr)
        return 1
    print("no hygiene gaps")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
