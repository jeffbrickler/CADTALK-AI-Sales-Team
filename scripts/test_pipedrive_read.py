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


def test_fetch_non_json_body_exits_1(monkeypatch):
    class HtmlResp:
        status_code = 502
        def json(self):
            raise ValueError("not JSON")
    monkeypatch.setattr(pr.requests, "request", lambda *a, **k: HtmlResp())
    with pytest.raises(SystemExit) as e:
        pr.fetch_all_deals("https://x/api/v1", "tok", owner_id=9)
    assert e.value.code == 1


def test_pagination_stall_exits_1(monkeypatch):
    stalled = {"success": True, "data": [mkdeal(id=1)],
               "additional_data": {"pagination":
                   {"more_items_in_collection": True, "next_start": 0}}}
    monkeypatch.setattr(pr.requests, "request", lambda *a, **k: FakeResp(stalled))
    with pytest.raises(SystemExit) as e:
        pr.fetch_all_deals("https://x/api/v1", "tok", owner_id=9)
    assert e.value.code == 1


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
