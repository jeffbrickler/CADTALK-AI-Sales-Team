# CRM Hygiene (v2.12.0) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a CRM hygiene system to the cadtalk-sales-team plugin that guarantees every required Pipedrive field on deal/org/person is enriched and every buying-committee contact is attached as a deal participant by close.

**Architecture:** New `ct-hygiene` skill (4 modes: intake, sweep, audit, gate) + read-only `sales-hygiene` gather agent + machine-readable `hygiene-contract.json` + `validate_hygiene.py` gap computer + `pipedrive_participants.py` REST script (MCP has no participant tools). All writes stay routed through the existing `sales-crm` single-writer agent. `/ct-crm` fronts hygiene-shaped requests. Spec: `docs/superpowers/specs/2026-07-15-crm-hygiene-design.md`.

**Tech Stack:** Markdown skills/agents (Claude Code plugin conventions), Python 3 stdlib + `requests` (already in requirements.txt), pytest (subprocess-style, mirrors `scripts/test_validate_create_payload.py`).

**Working conventions (read first):**
- Repo root = the worktree root (contains `skills/`, `agents/`, `scripts/`, `references/`, `CLAUDE.md`).
- Contract JSON uses **logical field NAMES only** — never hash API keys (repo rule, see `scripts/create-contract.json:3`). Hash keys live only in `references/pipedrive-custom-fields.md`.
- Commit after every task. Windows: LF/CRLF warnings from git are harmless.
- Run tests with: `python -m pytest scripts/<file> -v` (pytest is available; existing suite runs this way).

---

### Task 1: hygiene-contract.json

**Files:**
- Create: `scripts/hygiene-contract.json`

- [ ] **Step 1: Write the contract file**

```json
{
  "version": 1,
  "_comment": "Single source of truth for the CRM hygiene / required-by-close contract (design doc 2026-07-15). Logical field NAMES only — hash API keys and option IDs live exclusively in references/pipedrive-custom-fields.md. skills/ct-hygiene, agents/sales-hygiene.md and scripts/validate_hygiene.py point here; never restate this list elsewhere. Tier and Health Score are CS-owned: excluded below, never gated, never written by hygiene.",

  "stage_order": ["create", "discovery", "prove", "propose", "contracts", "close"],
  "_stage_comment": "'create' = due at record creation (the create contract already enforces most of these). 'close' = final gate before Won. Dueness: a field with due_by_stage S is required once the deal is AT stage S (audit check 'at') and must be complete BEFORE entering any stage after S (gate check 'entering').",

  "deal": [
    {"field": "Forecast Category",          "due_by_stage": "create",    "applies_when": "always"},
    {"field": "Compelling Event",           "due_by_stage": "create",    "applies_when": "always"},
    {"field": "Compelling Event Date",      "due_by_stage": "create",    "applies_when": "compelling_event_named"},
    {"field": "Partner",                    "due_by_stage": "create",    "applies_when": "partner_sourced"},
    {"field": "Partner Organization",       "due_by_stage": "create",    "applies_when": "partner_sourced"},
    {"field": "Partner Contact",            "due_by_stage": "create",    "applies_when": "partner_sourced"},
    {"field": "Partner Rep",                "due_by_stage": "create",    "applies_when": "partner_sourced"},
    {"field": "SQL Date",                   "due_by_stage": "discovery", "applies_when": "always"},
    {"field": "MEDDPICC-Metrics",           "due_by_stage": "discovery", "applies_when": "always"},
    {"field": "MEDDPICC-Economic Buyer",    "due_by_stage": "discovery", "applies_when": "always"},
    {"field": "MEDDPICC-ID the Pain",       "due_by_stage": "discovery", "applies_when": "always"},
    {"field": "MEDDPICC-Champion",          "due_by_stage": "discovery", "applies_when": "always"},
    {"field": "SQO Date",                   "due_by_stage": "prove",     "applies_when": "always"},
    {"field": "MEDDPICC-Decision Criteria", "due_by_stage": "prove",     "applies_when": "always"},
    {"field": "MEDDPICC-Competition",       "due_by_stage": "prove",     "applies_when": "always"},
    {"field": "Feedback on Demonstration",  "due_by_stage": "prove",     "applies_when": "demo_completed"},
    {"field": "MEDDPICC-Decision Process",  "due_by_stage": "propose",   "applies_when": "always"},
    {"field": "MEDDPICC-Paperwork Process", "due_by_stage": "propose",   "applies_when": "always"},
    {"field": "MEDDPICC-Coach",             "due_by_stage": "propose",   "applies_when": "always"},
    {"field": "Feedback on Proposal",       "due_by_stage": "contracts", "applies_when": "proposal_sent"},
    {"field": "EB Last Direct Touch",       "due_by_stage": "contracts", "applies_when": "always"}
  ],

  "organization": [
    {"field": "Organization Type", "due_by_stage": "create",    "applies_when": "always"},
    {"field": "Label",             "due_by_stage": "create",    "applies_when": "always"},
    {"field": "Owner",             "due_by_stage": "create",    "applies_when": "always"},
    {"field": "Source System",     "due_by_stage": "create",    "applies_when": "always"},
    {"field": "Target System",     "due_by_stage": "create",    "applies_when": "always"},
    {"field": "Revenue Range",     "due_by_stage": "discovery", "applies_when": "always"},
    {"field": "Employee Count",    "due_by_stage": "discovery", "applies_when": "always"},
    {"field": "Industry",          "due_by_stage": "discovery", "applies_when": "always"},
    {"field": "Website",           "due_by_stage": "discovery", "applies_when": "always"},
    {"field": "LinkedIn",          "due_by_stage": "discovery", "applies_when": "always"}
  ],

  "person": {
    "_comment": "Tiered enrichment (Jeff, 2026-07-15): key contacts get the full set; everyone else name+email+role. A person is KEY if is_primary is true OR their Role list intersects key_roles.",
    "due_by_stage": "prove",
    "key_roles": ["Economic Buyer", "Champion"],
    "key_required": ["Name", "Email", "Phone", "Job Title", "Role", "LinkedIn Profile"],
    "other_required": ["Name", "Email", "Role"]
  },

  "participants": {
    "_comment": "Everyone surfaced by calls or research is attached; partner reps too. min is the multi-threading floor (matches ct-score WGLL signal).",
    "due_by_stage": "propose",
    "min": 4,
    "include_partner": true
  },

  "excluded": ["Tier", "Health Score"]
}
```

- [ ] **Step 2: Verify it parses**

Run: `python -m json.tool scripts/hygiene-contract.json > /dev/null && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add scripts/hygiene-contract.json
git commit -m "feat: hygiene-contract.json — required-by-close spec for CRM hygiene"
```

---

### Task 2: validate_hygiene.py — core stage-dueness (TDD)

**Files:**
- Create: `scripts/test_validate_hygiene.py`
- Create: `scripts/validate_hygiene.py`

- [ ] **Step 1: Write the failing tests (core dueness + exit codes)**

Create `scripts/test_validate_hygiene.py`:

```python
"""pytest suite for validate_hygiene.py — CRM hygiene gap computer
(design doc 2026-07-15).

Run: python -m pytest scripts/test_validate_hygiene.py -v
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent
SCRIPT = SCRIPTS / "validate_hygiene.py"


def run(payload, tmp_path):
    """Run the validator on a payload dict; return CompletedProcess."""
    p = tmp_path / "payload.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(p)],
        capture_output=True, text=True,
    )


def base_payload(stage="discovery", check="at"):
    """Minimal skeleton — deliberately empty records so tests add only
    the fields they assert on."""
    return {
        "stage": stage,
        "check": check,
        "flags": {
            "demo_completed": False,
            "proposal_sent": False,
            "partner_sourced": False,
            "compelling_event_named": False,
        },
        "deal": {},
        "organization": {},
        "persons": [],
        "participants_count": 0,
    }


def complete_deal():
    """Every always-on deal field in the contract, filled."""
    return {
        "Forecast Category": 14,
        "Compelling Event": 336,
        "SQL Date": "2026-07-01",
        "MEDDPICC-Metrics": "3 FTE re-keying BOMs",
        "MEDDPICC-Economic Buyer": "Jane Smith, VP Ops",
        "MEDDPICC-ID the Pain": "BOM errors delay NPI",
        "MEDDPICC-Champion": "Bob Lee, Eng Mgr",
        "SQO Date": "2026-07-08",
        "MEDDPICC-Decision Criteria": "D365 native, no middleware",
        "MEDDPICC-Competition": "Manual + CADLink eval",
        "MEDDPICC-Decision Process": "Eval -> pilot -> board",
        "MEDDPICC-Paperwork Process": "MSA via legal, 2 weeks",
        "MEDDPICC-Coach": "Sam in IT",
        "EB Last Direct Touch": "2026-07-14",
    }


def complete_org():
    return {
        "Organization Type": 19,
        "Label": 7,
        "Owner": 12345,
        "Source System": [53],
        "Target System": [40],
        "Revenue Range": "$50M-$100M",
        "Employee Count": 250,
        "Industry": "Industrial Machinery",
        "Website": "https://acme.example.com",
        "LinkedIn": "https://linkedin.com/company/acme",
    }


def key_person(name="Jane Smith", primary=False, role="Economic Buyer"):
    return {
        "Name": name,
        "Email": f"{name.split()[0].lower()}@acme.example.com",
        "Phone": "+1 555 0100",
        "Job Title": "VP Operations",
        "Role": [role],
        "LinkedIn Profile": "https://linkedin.com/in/janesmith",
        "is_primary": primary,
    }


def other_person(name="Pat Doe"):
    return {
        "Name": name,
        "Email": f"{name.split()[0].lower()}@acme.example.com",
        "Role": ["End User"],
        "is_primary": False,
    }


def full_payload(stage="close", check="at"):
    p = base_payload(stage=stage, check=check)
    p["deal"] = complete_deal()
    p["organization"] = complete_org()
    p["persons"] = [key_person(primary=True), other_person()]
    p["participants_count"] = 4
    return p


# ---------------------------------------------------------------- core

def test_complete_payload_at_close_passes(tmp_path):
    r = run(full_payload(), tmp_path)
    assert r.returncode == 0, r.stderr


def test_missing_due_field_at_stage_is_flagged(tmp_path):
    p = full_payload(stage="discovery")
    del p["deal"]["MEDDPICC-Metrics"]
    r = run(p, tmp_path)
    assert r.returncode == 1
    assert "deal.MEDDPICC-Metrics" in r.stderr


def test_not_yet_due_field_is_not_flagged(tmp_path):
    # MEDDPICC-Decision Process is due at propose; at discovery it's fine to be empty.
    p = full_payload(stage="discovery")
    del p["deal"]["MEDDPICC-Decision Process"]
    r = run(p, tmp_path)
    assert r.returncode == 0, r.stderr


def test_entering_checks_everything_due_before_target(tmp_path):
    # Gate on entering prove: discovery-due fields must be complete...
    p = full_payload(stage="prove", check="entering")
    del p["deal"]["MEDDPICC-Champion"]  # due discovery
    del p["deal"]["SQO Date"]           # due prove — NOT yet required when entering
    r = run(p, tmp_path)
    assert r.returncode == 1
    assert "deal.MEDDPICC-Champion" in r.stderr
    assert "SQO Date" not in r.stderr


def test_empty_string_and_empty_list_count_as_missing(tmp_path):
    p = full_payload(stage="discovery")
    p["deal"]["MEDDPICC-Metrics"] = "   "
    p["organization"]["Source System"] = []
    r = run(p, tmp_path)
    assert r.returncode == 1
    assert "deal.MEDDPICC-Metrics" in r.stderr
    assert "organization.Source System" in r.stderr


def test_all_gaps_reported_not_just_first(tmp_path):
    p = full_payload(stage="discovery")
    del p["deal"]["MEDDPICC-Metrics"]
    del p["deal"]["MEDDPICC-Champion"]
    r = run(p, tmp_path)
    assert r.returncode == 1
    assert "deal.MEDDPICC-Metrics" in r.stderr
    assert "deal.MEDDPICC-Champion" in r.stderr


# ---------------------------------------------------------- spec errors

def test_unknown_stage_is_spec_error(tmp_path):
    r = run(full_payload(stage="banana"), tmp_path)
    assert r.returncode == 2


def test_unknown_check_is_spec_error(tmp_path):
    r = run(full_payload(check="sideways"), tmp_path)
    assert r.returncode == 2


def test_malformed_payload_is_spec_error(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{not json", encoding="utf-8")
    r = subprocess.run(
        [sys.executable, str(SCRIPT), str(p)],
        capture_output=True, text=True,
    )
    assert r.returncode == 2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/test_validate_hygiene.py -v`
Expected: errors — `validate_hygiene.py` does not exist (subprocess exits nonzero / FileNotFoundError-style failure on every test).

- [ ] **Step 3: Write the implementation**

Create `scripts/validate_hygiene.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest scripts/test_validate_hygiene.py -v`
Expected: all 9 tests PASS. (Note: `test_complete_payload_at_close_passes` exercises persons/participants paths too — they pass because the payload has a complete key person, complete other person, and 4 participants.)

- [ ] **Step 5: Commit**

```bash
git add scripts/validate_hygiene.py scripts/test_validate_hygiene.py
git commit -m "feat: validate_hygiene.py — stage-dueness gap computer with tests"
```

---

### Task 3: validate_hygiene.py — conditionals, tiering, participants, exclusions (TDD)

**Files:**
- Modify: `scripts/test_validate_hygiene.py` (append tests)

The Task 2 implementation already contains this logic; these tests pin it down. If any test fails, fix `validate_hygiene.py` minimally until green.

- [ ] **Step 1: Append the failing/pinning tests**

Append to `scripts/test_validate_hygiene.py`:

```python
# ------------------------------------------------------- applies_when

def test_flag_off_field_not_required(tmp_path):
    # Feedback on Demonstration due at prove but only when demo_completed.
    p = full_payload(stage="prove")
    p["flags"]["demo_completed"] = False
    assert "Feedback on Demonstration" not in p["deal"]
    r = run(p, tmp_path)
    assert r.returncode == 0, r.stderr


def test_flag_on_field_required(tmp_path):
    p = full_payload(stage="prove")
    p["flags"]["demo_completed"] = True
    r = run(p, tmp_path)
    assert r.returncode == 1
    assert "deal.Feedback on Demonstration" in r.stderr


def test_partner_sourced_requires_partner_relates(tmp_path):
    p = full_payload(stage="discovery")
    p["flags"]["partner_sourced"] = True
    r = run(p, tmp_path)
    assert r.returncode == 1
    for f in ("Partner", "Partner Organization", "Partner Contact", "Partner Rep"):
        assert f"deal.{f}" in r.stderr


def test_compelling_event_date_required_when_named(tmp_path):
    p = full_payload(stage="discovery")
    p["flags"]["compelling_event_named"] = True
    assert "Compelling Event Date" not in p["deal"]
    r = run(p, tmp_path)
    assert r.returncode == 1
    assert "deal.Compelling Event Date" in r.stderr


# ---------------------------------------------------- person tiering

def test_key_person_missing_linkedin_is_gap(tmp_path):
    p = full_payload(stage="prove")
    del p["persons"][0]["LinkedIn Profile"]  # the primary/key person
    r = run(p, tmp_path)
    assert r.returncode == 1
    assert "LinkedIn Profile" in r.stderr


def test_other_person_missing_linkedin_is_fine(tmp_path):
    p = full_payload(stage="prove")
    # other_person() has no LinkedIn Profile and no Phone — both fine.
    r = run(p, tmp_path)
    assert r.returncode == 0, r.stderr


def test_other_person_missing_role_is_gap(tmp_path):
    p = full_payload(stage="prove")
    p["persons"][1]["Role"] = []
    r = run(p, tmp_path)
    assert r.returncode == 1
    assert "person.Role" in r.stderr


def test_role_makes_person_key_without_primary(tmp_path):
    # Champion role (key_roles) => key tier even when not primary.
    p = full_payload(stage="prove")
    champ = other_person("Chris Champ")
    champ["Role"] = ["Champion"]
    p["persons"].append(champ)  # lacks Phone/Job Title/LinkedIn
    r = run(p, tmp_path)
    assert r.returncode == 1
    assert "Chris Champ" in r.stderr


def test_person_rules_not_due_before_prove(tmp_path):
    p = full_payload(stage="discovery")
    p["persons"][1]["Role"] = []  # would be a gap at prove
    r = run(p, tmp_path)
    assert r.returncode == 0, r.stderr


# ---------------------------------------------------- participants

def test_participants_below_min_is_gap(tmp_path):
    p = full_payload(stage="propose")
    p["participants_count"] = 2
    r = run(p, tmp_path)
    assert r.returncode == 1
    assert "participants: 2 attached, minimum 4" in r.stderr


def test_participants_not_due_before_propose(tmp_path):
    p = full_payload(stage="prove")
    p["participants_count"] = 1
    r = run(p, tmp_path)
    assert r.returncode == 0, r.stderr


# ---------------------------------------------------- exclusions

def test_excluded_fields_never_flagged(tmp_path):
    # Tier / Health Score are CS-owned: absent everywhere, never a gap.
    r = run(full_payload(stage="close"), tmp_path)
    assert r.returncode == 0
    assert "Tier" not in r.stderr
    assert "Health Score" not in r.stderr
```

- [ ] **Step 2: Run the full suite**

Run: `python -m pytest scripts/test_validate_hygiene.py -v`
Expected: all 21 tests PASS (Task 2 implementation covers these paths). If any fail, fix `validate_hygiene.py` minimally and re-run until green.

- [ ] **Step 3: Also run the existing create-validator suite (no regressions)**

Run: `python -m pytest scripts/test_validate_create_payload.py -q`
Expected: all pass (nothing shared, but confirms the scripts dir is healthy).

- [ ] **Step 4: Commit**

```bash
git add scripts/test_validate_hygiene.py scripts/validate_hygiene.py
git commit -m "test: hygiene validator — conditionals, person tiering, participants, exclusions"
```

---

### Task 4: pipedrive_participants.py (TDD on pure logic)

**Files:**
- Create: `scripts/test_pipedrive_participants.py`
- Create: `scripts/pipedrive_participants.py`

- [ ] **Step 1: Write the failing tests (pure functions only — no network)**

Create `scripts/test_pipedrive_participants.py`:

```python
"""pytest suite for pipedrive_participants.py pure logic (no network).

Run: python -m pytest scripts/test_pipedrive_participants.py -v
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pipedrive_participants as pp


def test_plan_adds_skips_already_attached():
    assert pp.plan_adds(existing=[101, 202], wanted=[101, 303]) == [303]


def test_plan_adds_dedupes_wanted():
    assert pp.plan_adds(existing=[], wanted=[303, 303, 404]) == [303, 404]


def test_plan_adds_empty_when_all_attached():
    assert pp.plan_adds(existing=[1, 2, 3], wanted=[2, 3]) == []


def test_base_url_builds_from_domain():
    assert (
        pp.base_url("cadtalk.pipedrive.com")
        == "https://cadtalk.pipedrive.com/api/v1"
    )


def test_base_url_strips_scheme_and_slash():
    assert (
        pp.base_url("https://cadtalk.pipedrive.com/")
        == "https://cadtalk.pipedrive.com/api/v1"
    )


def test_parse_args_list():
    args = pp.parse_args(["list", "42"])
    assert args.command == "list"
    assert args.deal_id == 42
    assert args.person_ids == []
    assert args.dry_run is False


def test_parse_args_add_with_dry_run():
    args = pp.parse_args(["add", "42", "7", "8", "--dry-run"])
    assert args.command == "add"
    assert args.deal_id == 42
    assert args.person_ids == [7, 8]
    assert args.dry_run is True


def test_parse_args_add_requires_person(capsys):
    with pytest.raises(SystemExit):
        pp.parse_args(["add", "42"])
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest scripts/test_pipedrive_participants.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'pipedrive_participants'`.

- [ ] **Step 3: Write the implementation**

Create `scripts/pipedrive_participants.py`:

```python
#!/usr/bin/env python3
"""Attach or list Pipedrive deal participants via the REST API.

The connected Pipedrive MCP has NO participant tools (only the deal's single
primary person_id), so this script is the plugin's ONE sanctioned direct-API
path — participants only, nothing else. Every other Pipedrive write stays in
the sales-crm contract (agents/sales-crm.md).

Env (see /ct-setup Section F):
    PIPEDRIVE_API_TOKEN   personal API token (Pipedrive > Personal preferences > API)
    PIPEDRIVE_DOMAIN      e.g. cadtalk.pipedrive.com

Usage:
    python pipedrive_participants.py list <deal_id>
    python pipedrive_participants.py add  <deal_id> <person_id> [...] [--dry-run]

`add` is idempotent: it lists current participants first and skips person IDs
already attached. --dry-run prints the plan and writes nothing.

Exit codes:
    0  success (including "nothing to do")
    1  API error (HTTP failure, bad token, unknown deal/person)
    2  usage/config error (missing env vars, bad arguments)
"""

import argparse
import json
import os
import sys

import requests

TIMEOUT = 30


def base_url(domain: str) -> str:
    domain = domain.strip().rstrip("/")
    if domain.startswith("https://"):
        domain = domain[len("https://"):]
    elif domain.startswith("http://"):
        domain = domain[len("http://"):]
    return f"https://{domain}/api/v1"


def plan_adds(existing: list, wanted: list) -> list:
    """Person IDs to attach: wanted minus existing, order kept, deduped."""
    existing_set = set(existing)
    out = []
    for pid in wanted:
        if pid not in existing_set:
            out.append(pid)
            existing_set.add(pid)
    return out


def parse_args(argv: list) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="pipedrive_participants.py",
        description="List/attach Pipedrive deal participants.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="list participants on a deal")
    p_list.add_argument("deal_id", type=int)

    p_add = sub.add_parser("add", help="attach persons to a deal (idempotent)")
    p_add.add_argument("deal_id", type=int)
    p_add.add_argument("person_ids", type=int, nargs="+")
    p_add.add_argument("--dry-run", action="store_true")

    args = parser.parse_args(argv)
    if not hasattr(args, "person_ids"):
        args.person_ids = []
    if not hasattr(args, "dry_run"):
        args.dry_run = False
    return args


def get_config() -> tuple:
    token = os.environ.get("PIPEDRIVE_API_TOKEN", "").strip()
    domain = os.environ.get("PIPEDRIVE_DOMAIN", "").strip()
    if not token or not domain:
        print(
            "CONFIG ERROR: set PIPEDRIVE_API_TOKEN and PIPEDRIVE_DOMAIN "
            "(see /ct-setup Section F). Falling back? Use the pinned "
            "'Participants checklist' note flow in skills/ct-hygiene.",
            file=sys.stderr,
        )
        sys.exit(2)
    return token, domain


def api_get_participants(url_base: str, token: str, deal_id: int) -> list:
    resp = requests.get(
        f"{url_base}/deals/{deal_id}/participants",
        params={"api_token": token, "limit": 500},
        timeout=TIMEOUT,
    )
    if resp.status_code != 200:
        print(f"API ERROR: GET participants -> HTTP {resp.status_code}: {resp.text[:300]}", file=sys.stderr)
        sys.exit(1)
    data = resp.json().get("data") or []
    return [item["person_id"]["value"] if isinstance(item.get("person_id"), dict)
            else item.get("person_id") for item in data]


def api_add_participant(url_base: str, token: str, deal_id: int, person_id: int) -> None:
    resp = requests.post(
        f"{url_base}/deals/{deal_id}/participants",
        params={"api_token": token},
        json={"person_id": person_id},
        timeout=TIMEOUT,
    )
    if resp.status_code not in (200, 201):
        print(f"API ERROR: POST participant {person_id} -> HTTP {resp.status_code}: {resp.text[:300]}", file=sys.stderr)
        sys.exit(1)


def main(argv: list) -> int:
    args = parse_args(argv)
    token, domain = get_config()
    url = base_url(domain)

    existing = api_get_participants(url, token, args.deal_id)

    if args.command == "list":
        print(json.dumps({"deal_id": args.deal_id, "participant_person_ids": existing}))
        return 0

    adds = plan_adds(existing, args.person_ids)
    if not adds:
        print(f"deal {args.deal_id}: all {len(args.person_ids)} person(s) already attached — nothing to do")
        return 0
    if args.dry_run:
        print(f"DRY RUN deal {args.deal_id}: would attach person_ids {adds} "
              f"(skipping {len(args.person_ids) - len(adds)} already attached)")
        return 0
    for pid in adds:
        api_add_participant(url, token, args.deal_id, pid)
        print(f"deal {args.deal_id}: attached person {pid}")
    print(f"deal {args.deal_id}: {len(adds)} attached, {len(existing)} were already on the deal")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest scripts/test_pipedrive_participants.py -v`
Expected: all 8 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/pipedrive_participants.py scripts/test_pipedrive_participants.py
git commit -m "feat: pipedrive_participants.py — REST participant attach (MCP gap), idempotent + dry-run"
```

---

### Task 5: sales-hygiene agent

**Files:**
- Create: `agents/sales-hygiene.md`

- [ ] **Step 1: Write the agent definition**

```markdown
---
name: sales-hygiene
description: Read-only CRM hygiene gatherer for /ct-hygiene. Pulls current Pipedrive state, Deal Desk files, Fireflies call transcripts, and (last resort) live web research for one deal, then returns a field → proposed value → source table plus a participants roster. NEVER writes — all writes go through the sales-crm contract.
---

<!--
  NO `tools:` restriction on purpose (same rationale as sales-crm): this agent
  needs the connected Pipedrive MCP (reads) and the Fireflies MCP, and MCP tool
  names are instance-scoped per user so they cannot be pinned in frontmatter.
-->

# CADTALK Hygiene Gatherer (sales-hygiene)

You gather evidence for CRM hygiene on ONE deal. You are read-only: you never
call an update/add tool on any system. Your output feeds the ct-hygiene batch
review table; the sales-crm agent (and only it) executes approved writes.

## Inputs (from the dispatching skill)

- Deal identifier (Pipedrive deal ID or name) — and org/person names if known.
- The run artifacts of the calling skill, when dispatched as a sweep
  (e.g., a research brief, contact map, or call summary produced this session).
- Optionally: the gap list from `scripts/validate_hygiene.py` so you only chase
  fields that are actually missing.

## Gather order (stop as soon as a field is sourced)

1. **Pipedrive state (always first).** `searchDeals`/`getDeal`,
   `getOrganization`, `getPerson`(s), `getNotes`, `getActivities`. Record every
   already-filled field — hygiene never overwrites non-empty fields, so knowing
   current state prevents proposing junk.
2. **Run artifacts** passed by the calling skill (sweep mode) — the freshest
   evidence.
3. **Deal Desk files.** Search the deal folder (cwd and parents) for research
   briefs, prospect reports, contact maps, call notes.
4. **Fireflies transcripts.** Search meetings by company/contact name
   (`fireflies_search` / `fireflies_get_transcripts`, then
   `fireflies_get_summary` for candidates). Extract only what was actually said:
   MEDDPICC evidence, feedback quotes, compelling events, attendee names/roles.
5. **Live web (org firmographics only).** Revenue range, employee count,
   industry, website, LinkedIn. Never invent MEDDPICC or feedback from the web.

## Output — return EXACTLY this structure

    ## Current state
    (per record: field → current value; note which required fields are blank)

    ## Proposed fills
    | Record | Field | Proposed value | Source | Confidence |
    |--------|-------|----------------|--------|------------|
    (Source = file path, or "Fireflies: <meeting title> <date>", or URL.
     Confidence = high / medium / low.)

    ## Conflicts
    (Field where Pipedrive has value X but a source says Y — never propose an
     overwrite; list both so the rep decides.)

    ## Participants roster
    | Name | In Pipedrive? (person ID or NO) | On deal? | Evidence |
    (Everyone surfaced by calls or research, incl. partner reps.)

    ## No-source gaps
    (Required fields nothing could fill — the rep must supply these.)

## Rules

- Every proposed value carries a source. No source → it goes to No-source gaps.
- Empty ≠ wrong: only propose values for BLANK fields; conflicts go to Conflicts.
- Tier and Health Score are CS-owned: never propose values for them.
- Field names are logical names from `references/pipedrive-custom-fields.md`;
  never emit hash keys — the sales-crm writer resolves keys.
- If Fireflies or web tools are unavailable, continue with remaining sources and
  say so in No-source gaps.
```

- [ ] **Step 2: Commit**

```bash
git add agents/sales-hygiene.md
git commit -m "feat: sales-hygiene agent — read-only gather/extract for CRM hygiene"
```

---

### Task 6: ct-hygiene skill

**Files:**
- Create: `skills/ct-hygiene/SKILL.md`

- [ ] **Step 1: Write the skill**

```markdown
---
name: ct-hygiene
description: CRM hygiene guard — audits and enriches Pipedrive so every required field on deal/org/person is filled and every buying-committee contact is attached as a deal participant by close. Use for 'is this deal complete', 'audit Acme', 'enrich the CRM', 'new opportunity: [company] + contacts', 'attach participants', 'CRM gaps'.
---

# CADTALK CRM Hygiene

Invoked as `/ct-hygiene <deal | company | "all open deals">` — or automatically
(sweep after producing skills, gate before stage moves, intake on new
opportunities routed from `/ct-crm`).

**Goal:** by the time a deal closes, everything in
`scripts/hygiene-contract.json` is filled and all contacts are participants.
That JSON is the single source of truth for what "complete" means — read it;
never restate the field list. Tier and Health Score are CS-owned: never gate on
them, never write them.

## The spine (all modes)

    gather → diff → propose → confirm → write → verify

1. **Gather.** Dispatch `subagent_type: cadtalk-sales-team:sales-hygiene` with
   the deal identifier (+ run artifacts in sweep mode). It returns current
   state, proposed fills with sources, conflicts, a participants roster, and
   no-source gaps. For a quick gate check you may skip the dispatch and read
   the deal/org/persons inline via the sales-crm QUERY procedures.
2. **Diff.** Build the validator payload (logical field names; `stage` = the
   deal's current stage mapped to contract stage_order; `check` = "at" for
   audits/sweeps, "entering" for gates; flags from deal context: demo_completed,
   proposal_sent, partner_sourced, compelling_event_named; persons array;
   participants_count from `python scripts/pipedrive_participants.py list <deal_id>`
   — if the token is unset, count from the pinned Participants checklist note
   instead). Write it to a temp file and run
   `python scripts/validate_hygiene.py <file>`. Exit 0 → say "no gaps" and stop
   (sweep/audit) or proceed with the move (gate). Exit 2 → report the spec
   error; write nothing.
3. **Propose → Confirm (batch review — ONE table).** Show every gap with its
   proposed fill and source, conflicts, and no-source gaps in one table. The rep
   approves/edits ONCE. **No write before the confirm.** Inferred values only
   fill blanks — never overwrite a non-empty field.
4. **Write.** Field updates, notes, and any missing person records go through
   the sales-crm contract (`agents/sales-crm.md`; batch → dispatch
   `subagent_type: cadtalk-sales-team:sales-crm`). Person creation follows the
   create resolution rules (search first, no duplicates). Participants:
   `python scripts/pipedrive_participants.py add <deal_id> <person_ids...>`
   (idempotent). Token unset → maintain a pinned **"Participants checklist"**
   note on the deal (via sales-crm NOTE) listing who still needs manual attach,
   and tell the rep.
5. **Verify.** Re-read the records (QUERY), confirm writes landed, then report:
   filled, still-open gaps tagged `no-source` / `user-skipped` / `conflict`.
   Failed write → the fill-blanks-only rule makes a rerun safe; say exactly
   which fields landed.

## Modes

**Intake** — rep shares a new opportunity (contacts, website, partner details).
Search Pipedrive for the org, persons, and deal (sales-crm resolution rules).
Anything missing → **delegate creation to the `/ct-crm` guided create flow**
(`skills/ct-crm/SKILL.md`) — ct-hygiene never creates records directly. Then run
the spine once with the shared details as source, and attach all known
participants.

**Sweep** — dispatched as the final step of producing skills (ct-research,
ct-contacts, ct-se, ct-prep, ct-proposal, ct-commit, ct-followup, ct-qualify).
That run's artifacts are the primary source; scope the table to what the run
learned. If the deal/org can't be resolved in Pipedrive, skip silently.

**Audit** — `/ct-hygiene <deal>` runs the full spine (`check: "at"`).
`/ct-hygiene all open deals` → list open deals (sales-crm QUERY), run the diff
per deal, show a per-deal gap summary table first, then offer to run fills
deal-by-deal.

**Gate** — called by the sales-crm STAGE MOVE contract before a move (and by
mark-won). Run the diff with `check: "entering"` + the target stage ("close"
for won). Gaps → show the list, offer to fill now (spine), then ask **"move
anyway?"** — the rep can always override; record an override in the deal's
hygiene note. Never hard-block.

## Stage mapping

Contract stage_order is logical: `create, discovery, prove, propose, contracts,
close`. Map the deal's Pipedrive stage via `references/pipedrive-stage-ids.md`
(Discovery 4/9/15, Prove 5/10/16, Propose 43/11/17, Contracts 6/12/18 across
pipelines 1/2/3). Stages before Discovery map to `create`; won/lost map to
`close`. Expansions (pipeline 4): map by same-named stages; where a stage name
doesn't exist, use the nearest earlier stage.

## Boundaries

- Single-writer rule holds: every Pipedrive write goes through sales-crm.
  The ONLY exception is `scripts/pipedrive_participants.py` (participants are
  impossible via the connected MCP).
- Never overwrite non-empty fields. Conflicts are reported, not resolved.
- Tier / Health Score: CS-owned, untouchable.
- Voice: terse. A hygiene report is a punch list, not a pitch.
```

- [ ] **Step 2: Commit**

```bash
git add skills/ct-hygiene/SKILL.md
git commit -m "feat: ct-hygiene skill — intake/sweep/audit/gate CRM hygiene guard"
```

---

### Task 7: sales-crm.md edits (gate wiring + Tier/Health removal + participants note)

**Files:**
- Modify: `agents/sales-crm.md`

- [ ] **Step 1: Add the hygiene gate to STAGE MOVE**

In `agents/sales-crm.md`, the STAGE MOVE section (around line 161) currently ends with step 4 (conversion-date stamps). Insert a new step between step 2 and step 3 — renumber so the section reads 1..5. Replace the whole `### STAGE MOVE` section with:

```markdown
### STAGE MOVE
1. Find the deal if given by name.
2. Match the stage name to a `stage_id` in the reference — pipeline matters (same stage name exists in different pipelines).
3. **Hygiene gate (warn + confirm — never hard-block).** Before the move, run
   the ct-hygiene gate (`skills/ct-hygiene/SKILL.md`, Gate mode) with
   `check: "entering"` and the target stage ("close" when marking won). No
   gaps → proceed. Gaps → show the list, offer to fill now, then ask "move
   anyway?". An override proceeds and is recorded in the deal's hygiene note.
4. `updateDeal` with the `stage_id`. Confirm with deal + stage + pipeline.
5. **Conversion-date stamps (set-once — these drive funnel metrics, never overwrite):**
   - Moving **into Discovery** (opportunity pipelines 1/2/3 — stage_id 4, 9, or 15): if **SQL Date** (`80d471aaf715fb3bfd6320d1874949a864e0e909`) is empty, set it to today (`YYYY-MM-DD`). If already set, leave it.
   - Moving **into Prove** (stage_id 5, 10, or 16): if **SQO Date** (`6e75c1b17be487e2b52f2282ac4e06e39c90e3b5`) is empty, set it to today. If already set, leave it.
   - Read the deal's current SQL/SQO Date first; only write the one that is blank. Backward moves never clear a stamped date. (A deal created directly into Discovery gets SQL Date **inside the create call** — the CREATE contract owns that rule; this section owns move-time stamps only.)
```

- [ ] **Step 2: Add a PARTICIPANTS operation section**

Insert after the `### STAGE MOVE` section and before `### QUERY (read)`:

```markdown
### PARTICIPANTS (via script — the one non-MCP write)

The connected Pipedrive MCP has no participant tools. Deal participants are
handled by `scripts/pipedrive_participants.py` (requires `PIPEDRIVE_API_TOKEN`
+ `PIPEDRIVE_DOMAIN`; see `/ct-setup` Section F):

    python scripts/pipedrive_participants.py list <deal_id>
    python scripts/pipedrive_participants.py add <deal_id> <person_id...> [--dry-run]

Idempotent — already-attached persons are skipped. Token unset → fall back to a
pinned "Participants checklist" note on the deal (NOTE operation) so nothing is
lost; `/ct-hygiene` owns that fallback flow. This script is the ONLY sanctioned
direct-API call in the plugin; every other write stays in this contract.
```

- [ ] **Step 3: Remove Tier/Health from the per-stage contract (CS-owned)**

In the "Per-stage CRM update contract" table:
- Qualify row: change `Tier, Forecast Category, Health Score, MEDDPICC-Metrics / -Economic Buyer / -ID the Pain / -Champion as known, + pinned qualification note` → `Forecast Category, MEDDPICC-Metrics / -Economic Buyer / -ID the Pain / -Champion as known, + pinned qualification note`
- Commit row: change `Forecast Category (only advance to Definitely/Probably if the gate passes; else flag), Health Score, Compelling Event + Compelling Event Date, EB Last Direct Touch, compelling-event note` → `Forecast Category (only advance to Definitely/Probably if the gate passes; else flag), Compelling Event + Compelling Event Date, EB Last Direct Touch, compelling-event note`
- Follow-up row: change `log activity, schedule the next follow-up activity, updated Health Score` → `log activity, schedule the next follow-up activity`

Then add this line directly under the table (before "Reps never memorize field keys."):

```markdown
**Tier and Health Score are CS-owned (confirmed 2026-07-15):** rep-loop skills
and `/ct-hygiene` never gate on them and never write them. They remain in the
field reference and the CREATE contract for now (changing the create set
requires the Pipedrive-side required-fields sync); post-create they belong to CS.
```

Also update the intro sentence of that section: `MEDDPICC + feedback are Large-text (plain string), Tier/Forecast Category/Health Score are option IDs, SQL/SQO are dates.` → `MEDDPICC + feedback are Large-text (plain string), Forecast Category is an option ID, SQL/SQO are dates.`

And in the frontmatter `description:` change `field updates (MEDDPICC, Forecast, Tier, Health Score)` → `field updates (MEDDPICC, Forecast Category, dates)`.

- [ ] **Step 4: Commit**

```bash
git add agents/sales-crm.md
git commit -m "feat: sales-crm — hygiene gate on stage moves, participants script op, Tier/Health to CS"
```

---

### Task 8: ct-crm front door

**Files:**
- Modify: `skills/ct-crm/SKILL.md`

- [ ] **Step 1: Add routing to ct-hygiene**

In `skills/ct-crm/SKILL.md`, insert after the "## How it works" numbered list (after the paragraph about dispatching the sales-crm agent for large batches, around line 30):

```markdown
## Front door — hygiene-shaped requests route to /ct-hygiene

`/ct-crm` is the only CRM command a rep needs to remember. When the request is
about **completeness rather than a single operation** — "is this deal
complete", "audit Acme", "enrich the CRM from the calls", "new opportunity:
[company] + contacts + partner", "attach participants", "what's missing before
I move this to Contracts" — invoke `skills/ct-hygiene/SKILL.md` (Skill:
`cadtalk-sales-team:ct-hygiene`) instead of running a raw operation. ct-hygiene
delegates any record creation back to this skill's guided create flow, so the
two never duplicate.
```

- [ ] **Step 2: Commit**

```bash
git add skills/ct-crm/SKILL.md
git commit -m "feat: ct-crm fronts hygiene-shaped requests to ct-hygiene"
```

---

### Task 9: Sweep hooks in the 8 producing skills

**Files:**
- Modify: `skills/ct-research/SKILL.md`
- Modify: `skills/ct-contacts/SKILL.md`
- Modify: `skills/ct-se/SKILL.md`
- Modify: `skills/ct-prep/SKILL.md`
- Modify: `skills/ct-proposal/SKILL.md`
- Modify: `skills/ct-commit/SKILL.md`
- Modify: `skills/ct-followup/SKILL.md`
- Modify: `skills/ct-qualify/SKILL.md`

- [ ] **Step 1: Append the identical sweep block to each of the 8 files**

Append at the END of each SKILL.md (same text in all 8, exactly):

```markdown

## Hygiene sweep (final step)

After this skill's output is delivered, run the CRM hygiene sweep
(`skills/ct-hygiene/SKILL.md`, Sweep mode) with this run's artifacts as the
source — it pushes what this run learned (fields, contacts, participants) into
Pipedrive through the sales-crm contract. Batch review table first; writes only
after the rep confirms. If the deal/org can't be resolved in Pipedrive, skip
silently.
```

- [ ] **Step 2: Verify all 8 got it**

Run: `grep -l "Hygiene sweep (final step)" skills/*/SKILL.md`
Expected: exactly the 8 files listed above.

- [ ] **Step 3: Commit**

```bash
git add skills/ct-research/SKILL.md skills/ct-contacts/SKILL.md skills/ct-se/SKILL.md skills/ct-prep/SKILL.md skills/ct-proposal/SKILL.md skills/ct-commit/SKILL.md skills/ct-followup/SKILL.md skills/ct-qualify/SKILL.md
git commit -m "feat: hygiene sweep hook in the 8 producing skills"
```

---

### Task 10: ct-setup Section F (API token)

**Files:**
- Modify: `skills/ct-setup/SKILL.md`

- [ ] **Step 1: Add Section F**

In `skills/ct-setup/SKILL.md`, insert a new section AFTER "## Section E: CRM Profile — your pipelines + Owner ID" (starts line 238) and BEFORE "## Section D: Confirmation" (line 279; note the file's sections run A, B, C, E, D — keep that order, F goes between E and D):

```markdown
## Section F: Participants API token (for /ct-hygiene)

The connected Pipedrive MCP cannot attach deal participants, so
`scripts/pipedrive_participants.py` calls the Pipedrive REST API directly. It
needs two environment variables:

1. Get the token: Pipedrive → click your avatar → **Personal preferences** →
   **API** → copy the personal API token.
2. Ask the rep for their Pipedrive domain (the browser URL host, e.g.
   `cadtalk.pipedrive.com`).
3. Have the rep set both, persisted for future sessions (PowerShell):

       [Environment]::SetEnvironmentVariable("PIPEDRIVE_API_TOKEN", "<token>", "User")
       [Environment]::SetEnvironmentVariable("PIPEDRIVE_DOMAIN", "cadtalk.pipedrive.com", "User")

   (macOS/Linux: add `export PIPEDRIVE_API_TOKEN=...` and
   `export PIPEDRIVE_DOMAIN=...` to the shell profile.)
   **Never ask the rep to paste the token into chat** — they set it themselves;
   the script reads it from the environment.
4. Verify in a NEW terminal session against a real open deal ID:

       python scripts/pipedrive_participants.py list <deal_id>

   Expected: a JSON line with `participant_person_ids`. A CONFIG ERROR means
   the env vars aren't visible; an API ERROR usually means a bad token/domain.
5. If the rep can't get a token now, skip — `/ct-hygiene` falls back to a
   pinned "Participants checklist" note on each deal until the token exists.
```

- [ ] **Step 2: Commit**

```bash
git add skills/ct-setup/SKILL.md
git commit -m "feat: ct-setup Section F — Pipedrive participants API token"
```

---

### Task 11: Routing, version, changelog, plugin validation

**Files:**
- Modify: `CLAUDE.md` (repo root)
- Modify: `.claude-plugin/plugin.json`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Add the routing row**

In root `CLAUDE.md`, Skill Routing table, add after the `/ct-crm`-adjacent rows (keep table formatting):

```markdown
| CRM hygiene, audit deal completeness, enrich CRM, attach participants, new opportunity intake | `/ct-hygiene` |
```

- [ ] **Step 2: Bump version**

In `.claude-plugin/plugin.json` line 3: `"version": "2.11.0"` → `"version": "2.12.0"`.
Check whether `.claude-plugin/marketplace.json` also carries a version string (`grep -n version .claude-plugin/marketplace.json`); if yes, bump it identically.

- [ ] **Step 3: Add CHANGELOG entry**

Read the top of `CHANGELOG.md` first and match the existing entry format exactly (heading style, date placement). Content for the new top entry:

```markdown
## v2.12.0 — CRM Hygiene (2026-07-15)

- NEW `/ct-hygiene` skill — intake / sweep / audit / gate modes; guarantees the
  required-by-close field set and participant attachment. `/ct-crm` fronts
  hygiene-shaped requests.
- NEW `sales-hygiene` agent — read-only gatherer (Pipedrive state, Deal Desk
  files, Fireflies transcripts, live web) producing sourced fill proposals.
- NEW `scripts/hygiene-contract.json` + `scripts/validate_hygiene.py` (+tests) —
  machine-readable required-by-close spec and stage-dueness gap computer.
- NEW `scripts/pipedrive_participants.py` (+tests) — deal participants via REST
  (the connected MCP has no participant tools); idempotent, dry-run,
  checklist-note fallback when no token. `/ct-setup` Section F sets it up.
- sales-crm: STAGE MOVE now runs the hygiene gate (warn + confirm, never
  hard-block); PARTICIPANTS operation documented; Tier + Health Score moved to
  CS ownership (removed from the per-stage rep contract).
- 8 producing skills (research/contacts/se/prep/proposal/commit/followup/
  qualify) end with a hygiene sweep so run intel lands in Pipedrive.
```

- [ ] **Step 4: Run the plugin validator + full test suite**

Run: `python scripts/validate-plugin.py`
Expected: passes (exit 0). If it flags the new skill/agent, fix per its output.

Run: `python -m pytest scripts/ -q`
Expected: all tests pass (create-payload suite + 21 hygiene + 8 participants).

- [ ] **Step 5: Commit**

```bash
git add CLAUDE.md .claude-plugin/plugin.json CHANGELOG.md
git commit -m "chore: v2.12.0 — routing, version bump, changelog for CRM hygiene"
```

---

### Task 12: End-to-end smoke (manual, with Jeff)

No file changes — verification checklist for the session after merge.

- [ ] **Step 1: Validator smoke on a real deal.** Pick one open deal; build the payload by hand from its Pipedrive state; run `python scripts/validate_hygiene.py <file>`; confirm the gap list matches reality.
- [ ] **Step 2: Participants dry-run.** `python scripts/pipedrive_participants.py add <deal_id> <person_id> --dry-run` — confirm plan output; then a real `add` on one person; verify in Pipedrive UI.
- [ ] **Step 3: Full audit.** Run `/ct-hygiene <that deal>` — confirm the batch table shows sources, approve a subset, verify writes landed and skipped fields are reported.
- [ ] **Step 4: Gate.** Attempt a stage move via `/ct-crm` on a deal with known gaps — confirm warn + "move anyway?" behavior.

---

## Self-review notes

- **Spec coverage:** contract (T1), validator+tests (T2–3), participants (T4), agent (T5), skill with 4 modes (T6), gate wiring + Tier/Health removal + participants op (T7), front door (T8), 8 sweep hooks (T9), setup token (T10), routing/version/changelog/plugin-validate (T11), manual E2E (T12). Spec "Out of scope" items untouched. create-contract.json deliberately NOT edited (Tier/Health stay create-required — changing it requires the Pipedrive-side required-fields sync; noted in T7 Step 3 text).
- **Type consistency:** validator payload keys (`stage`, `check`, `flags`, `deal`, `organization`, `persons`, `participants_count`) match between tests, implementation, and the ct-hygiene skill text. `plan_adds(existing, wanted)`, `base_url(domain)`, `parse_args(argv)` names match tests.
- **Person "Name" required for key contacts** is included in `key_required` so both tiers require Name.
