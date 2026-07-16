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


def test_api_request_network_failure_exits_clean_without_token(monkeypatch, capsys):
    import requests as real_requests

    def boom(method, url, **kwargs):
        raise real_requests.exceptions.ConnectionError(
            "HTTPSConnectionPool(host='x', port=443): Max retries exceeded "
            "with url: /api/v1/deals/1/participants?api_token=SECRET123"
        )

    monkeypatch.setattr(pp.requests, "request", boom)
    with pytest.raises(SystemExit) as excinfo:
        pp.api_request("GET", "https://x/api/v1/deals/1/participants",
                       params={"api_token": "SECRET123"})
    assert excinfo.value.code == 1
    err = capsys.readouterr().err
    assert "API ERROR: network failure" in err
    assert "SECRET123" not in err
