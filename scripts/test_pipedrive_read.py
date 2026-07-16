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
