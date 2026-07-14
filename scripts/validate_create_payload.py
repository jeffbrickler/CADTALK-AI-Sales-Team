#!/usr/bin/env python3
"""Validate an opportunity-create payload against scripts/create-contract.json.

The enforcement backstop for the CADTALK Guided Create Flow (design doc
2026-07-14). The sales-crm writer runs this on the assembled payload BEFORE
calling any Pipedrive create tool, and never calls them on a nonzero exit.

Usage:
    python validate_create_payload.py <payload.json>
    python validate_create_payload.py -          (read payload from stdin)

Payload shape (logical field NAMES as keys — never hash API keys):

    {
      "motion": "partner_sourced",
      "deal":         {"Title": "...", "Pipeline": "Partners", ...,
                       "_unknown": ["Tier"]},
      "organization": {"Name": "...", ..., "_unknown": []},
      "person":       {"Name": "...", ..., "_unknown": ["Phone"]}
    }

Validation semantics:
  * hard_required fields must be present with a non-empty value — the
    "_unknown" escape does NOT apply to them.
  * Every other required field is satisfied by a non-empty value OR by
    being listed in that record's "_unknown" array (ask-don't-skip: the
    blank becomes a recorded decision the Draft displays as unknown).
  * Motion "partner_sourced" additionally requires the partner relate
    fields on the deal; other motions must NOT be forced to carry them.
  * A deal created directly into Discovery on the SQL-stamp pipelines
    must carry "SQL Date" in the same payload (atomic stamp, eng 4A).
  * ALL missing fields are reported, not just the first.

Exit codes:
    0  payload satisfies the contract
    1  contract violations (missing fields) — every one listed on stderr
    2  usage/spec error (unreadable payload, malformed JSON, unknown
       motion, missing/malformed contract file)
"""

import json
import sys
from pathlib import Path

CONTRACT_PATH = Path(__file__).resolve().parent / "create-contract.json"

DISCOVERY_STAGE_NAME = "discovery"


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
        fail_spec("usage: validate_create_payload.py <payload.json | ->")
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
    return True


def is_satisfied(record: dict, field: str) -> bool:
    """Required (non-hard) field: filled, or explicitly flagged unknown."""
    if is_filled(record, field):
        return True
    unknown = record.get("_unknown", [])
    return isinstance(unknown, list) and field in unknown


def validate(contract: dict, payload: dict) -> list:
    missing = []

    motion_key = payload.get("motion")
    motions = contract.get("motions", {})
    if motion_key not in motions:
        fail_spec(
            f"unknown motion {motion_key!r} — expected one of: {', '.join(sorted(motions))}"
        )
    motion = motions[motion_key]

    records = {
        name: payload.get(name) if isinstance(payload.get(name), dict) else {}
        for name in ("deal", "organization", "person")
    }
    deal = records["deal"]

    def real_items(mapping):
        """Skip '_comment'-style annotation keys in the contract JSON."""
        return [
            (k, v) for k, v in mapping.items()
            if not k.startswith("_") and isinstance(v, (list, dict))
        ]

    # 1. Hard-required (no unknown escape).
    for record_name, fields in real_items(contract.get("hard_required", {})):
        record = records.get(record_name, {})
        for field in fields:
            if not is_filled(record, field):
                missing.append(f"{record_name}.{field} (hard-required — cannot be unknown)")

    # 2. Per-record required fields (unknown-flag allowed).
    hard = {
        (rname, f)
        for rname, fields in real_items(contract.get("hard_required", {}))
        for f in fields
    }
    for record_name, spec in real_items(contract.get("records", {})):
        record = records.get(record_name, {})
        for field in spec.get("required", []):
            if (record_name, field) in hard:
                continue  # already checked, stricter rule
            if not is_satisfied(record, field):
                missing.append(f"{record_name}.{field} (required — fill or flag unknown)")

    # 3. Motion extras (e.g. partner relates on partner_sourced only).
    for record_name, fields in real_items(motion.get("extra_required", {})):
        record = records.get(record_name, {})
        for field in fields:
            if not is_satisfied(record, field):
                missing.append(
                    f"{record_name}.{field} (required for motion {motion_key!r})"
                )

    # 4. Conditional deal fields.
    for cond in contract.get("records", {}).get("deal", {}).get("conditional", []):
        field = cond.get("field")
        when = cond.get("when")
        if when == "compelling_event_named":
            if is_filled(deal, "Compelling Event") and not is_satisfied(deal, field):
                missing.append(
                    f"deal.{field} (required — a compelling event was named)"
                )
        elif when == "stage_is_discovery_on_opportunity_pipeline":
            stage = str(deal.get("Stage", "")).strip().lower()
            pipeline = str(deal.get("Pipeline", "")).strip()
            if stage == DISCOVERY_STAGE_NAME and pipeline in cond.get("pipelines", []):
                # Atomic stamp: unknown-flag deliberately NOT accepted here —
                # the flow stamps today's date itself; a rep never "doesn't know" it.
                if not is_filled(deal, field):
                    missing.append(
                        f"deal.{field} (required — created directly into Discovery on {pipeline}; "
                        "stamp inside the same addDeal call)"
                    )

    return missing


def main(argv: list) -> int:
    contract = load_contract()
    payload = load_payload(argv)
    missing = validate(contract, payload)
    if missing:
        print("CREATE CONTRACT VIOLATIONS:", file=sys.stderr)
        for item in missing:
            print(f"  - {item}", file=sys.stderr)
        return 1
    print("payload valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
