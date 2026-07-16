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
