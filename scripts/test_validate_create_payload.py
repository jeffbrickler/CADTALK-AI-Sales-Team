"""pytest suite for validate_create_payload.py — the 14 paths from the
eng-review coverage diagram (design doc 2026-07-14, Test Plan 5A).

Run: pytest scripts/test_validate_create_payload.py
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent
SCRIPT = SCRIPTS / "validate_create_payload.py"
CONTRACT = SCRIPTS / "create-contract.json"

HARD_REQUIRED_DEAL = ["Title", "Pipeline", "Stage", "Organization", "Person", "Owner"]

MOTION_PIPELINE = {
    "aftermarket": "Aftermarket",
    "new_erp": "New ERP/PLM Prospects",
    "partner_sourced": "Partners",
    "expansion": "Expansions",
}


def full_payload(motion="new_erp", stage="Qualify"):
    """A payload that satisfies the contract for the given motion."""
    deal = {
        "Title": "Siemens - CADTALK for D365",
        "Pipeline": MOTION_PIPELINE[motion],
        "Stage": stage,
        "Value": 60000,
        "Currency": "USD",
        "Expected close date": "2026-09-30",
        "Owner": 12345,
        "Organization": "Siemens AG",
        "Person": "Jane Smith",
        "ACV": 60000,
        "Forecast Category": "Pipeline",
        "Tier": "Tier 1",
        "Health Score": "Green",
        "Source channel": "Partner referral",
        "Compelling Event": "ERP go-live Q4",
        "Compelling Event Date": "2026-10-01",
        "_unknown": [],
    }
    if motion == "partner_sourced":
        deal.update(
            {
                "Partner": 111,
                "Partner Organization": 222,
                "Partner Contact": 333,
                "Partner Rep": 444,
            }
        )
    if stage == "Discovery":
        deal["SQL Date"] = "2026-07-14"
    return {
        "motion": motion,
        "deal": deal,
        "organization": {
            "Name": "Siemens AG",
            "Organization Type": "Prospect",
            "Label": "Hot",
            "Source System": "SolidWorks",
            "Target System": "D365 Business Central",
            "Owner": 12345,
            "_unknown": [],
        },
        "person": {
            "Name": "Jane Smith",
            "Organization": "Siemens AG",
            "Email": "jane@siemens.com",
            "Phone": "+1 555 0100",
            "Role": "Champion",
            "_unknown": [],
        },
    }


def run(payload=None, arg=None, stdin=None):
    argv = [sys.executable, str(SCRIPT)]
    if arg is not None:
        argv.append(arg)
    elif payload is not None:
        argv.append("-")
        stdin = json.dumps(payload)
    return subprocess.run(argv, input=stdin, capture_output=True, text=True)


# --- spec / usage errors (exit 2) -------------------------------------------

def test_missing_payload_file():
    res = run(arg=str(SCRIPTS / "does-not-exist.json"))
    assert res.returncode == 2
    assert "cannot read payload" in res.stderr


def test_malformed_payload_json():
    res = run(arg="-", stdin="{not json")
    assert res.returncode == 2
    assert "not valid JSON" in res.stderr


def test_unknown_motion():
    payload = full_payload()
    payload["motion"] = "sdr_conversion"
    res = run(payload)
    assert res.returncode == 2
    assert "unknown motion" in res.stderr


def test_contract_file_missing_or_malformed(tmp_path, monkeypatch):
    # Copy the script next to a broken contract and run it there.
    broken_dir = tmp_path
    script_copy = broken_dir / "validate_create_payload.py"
    script_copy.write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")

    # Missing contract
    res = subprocess.run(
        [sys.executable, str(script_copy), "-"],
        input=json.dumps(full_payload()),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 2
    assert "contract file not found" in res.stderr

    # Malformed contract
    (broken_dir / "create-contract.json").write_text("{broken", encoding="utf-8")
    res = subprocess.run(
        [sys.executable, str(script_copy), "-"],
        input=json.dumps(full_payload()),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 2
    assert "not valid JSON" in res.stderr


# --- hard-required (exit 1, no unknown escape) ------------------------------

@pytest.mark.parametrize("field", HARD_REQUIRED_DEAL)
def test_each_hard_required_field_missing_fails(field):
    payload = full_payload()
    payload["deal"].pop(field, None)
    res = run(payload)
    assert res.returncode == 1
    assert f"deal.{field} (hard-required" in res.stderr


def test_hard_required_cannot_be_flagged_unknown():
    payload = full_payload()
    payload["deal"].pop("Owner", None)
    payload["deal"]["_unknown"] = ["Owner"]
    res = run(payload)
    assert res.returncode == 1
    assert "deal.Owner (hard-required" in res.stderr


def test_all_missing_fields_reported_not_just_first():
    payload = full_payload()
    payload["deal"].pop("Tier", None)
    payload["organization"].pop("Source System", None)
    payload["person"].pop("Role", None)
    res = run(payload)
    assert res.returncode == 1
    assert "deal.Tier" in res.stderr
    assert "organization.Source System" in res.stderr
    assert "person.Role" in res.stderr


# --- motion rules ------------------------------------------------------------

def test_partner_motion_without_relates_fails():
    payload = full_payload(motion="partner_sourced")
    for f in ("Partner", "Partner Organization", "Partner Contact", "Partner Rep"):
        payload["deal"].pop(f, None)
    res = run(payload)
    assert res.returncode == 1
    for f in ("Partner", "Partner Organization", "Partner Contact", "Partner Rep"):
        assert f"deal.{f} (required for motion 'partner_sourced')" in res.stderr


def test_non_partner_motion_without_relates_passes():
    payload = full_payload(motion="new_erp")
    assert "Partner" not in payload["deal"]
    res = run(payload)
    assert res.returncode == 0


# --- conditional fields -------------------------------------------------------

def test_discovery_create_on_stamp_pipeline_without_sql_date_fails():
    payload = full_payload(motion="new_erp", stage="Discovery")
    payload["deal"].pop("SQL Date", None)
    res = run(payload)
    assert res.returncode == 1
    assert "deal.SQL Date" in res.stderr


def test_discovery_create_on_expansion_pipeline_needs_no_sql_date():
    # Pipeline 4 stamp policy is an open question — no SQL Date conditional.
    payload = full_payload(motion="expansion", stage="Discovery")
    payload["deal"].pop("SQL Date", None)
    res = run(payload)
    assert res.returncode == 0


def test_compelling_event_named_requires_date():
    payload = full_payload()
    payload["deal"].pop("Compelling Event Date", None)
    res = run(payload)
    assert res.returncode == 1
    assert "deal.Compelling Event Date" in res.stderr


def test_no_compelling_event_no_date_required():
    payload = full_payload()
    payload["deal"].pop("Compelling Event Date", None)
    payload["deal"].pop("Compelling Event", None)
    payload["deal"]["_unknown"] = ["Compelling Event"]
    res = run(payload)
    assert res.returncode == 0


# --- unknown flag --------------------------------------------------------------

def test_unknown_flagged_field_passes():
    payload = full_payload()
    payload["deal"].pop("Tier", None)
    payload["deal"]["_unknown"] = ["Tier"]
    res = run(payload)
    assert res.returncode == 0


def test_silent_blank_still_fails():
    payload = full_payload()
    payload["deal"]["Tier"] = "   "  # whitespace ≠ filled
    res = run(payload)
    assert res.returncode == 1
    assert "deal.Tier" in res.stderr


# --- valid payload per motion ---------------------------------------------------

@pytest.mark.parametrize("motion", list(MOTION_PIPELINE))
def test_valid_payload_passes_per_motion(motion):
    res = run(full_payload(motion=motion))
    assert res.returncode == 0, res.stderr
    assert "payload valid" in res.stdout
