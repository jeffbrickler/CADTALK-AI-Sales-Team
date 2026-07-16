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

    def test_string_payload_rejected(self):
        probs = check(mkqueue([mkitem(proposed_payload="raw")]))
        assert any("proposed_payload must be an object" in p for p in probs)

    def test_list_payload_rejected(self):
        probs = check(mkqueue([mkitem(proposed_payload=["MEDDPICC-Champion"])]))
        assert any("proposed_payload must be an object" in p for p in probs)

    def test_non_dict_item_rejected_cleanly(self):
        probs = check(mkqueue([42]))
        assert any("must be an object" in p for p in probs)

    def test_uppercase_hash_key_rejected(self):
        bad = mkitem(proposed_payload={
            "1A706BAE5B0046828AE5A1B573C722BD96068058": 15})
        probs = check(mkqueue([bad]))
        assert any("hash" in p.lower() for p in probs)

    def test_two_items_missing_id_not_flagged_duplicate(self):
        a = mkitem(); del a["id"]
        b = mkitem(deal="Beta Corp"); del b["id"]
        probs = check(mkqueue([a, b]))
        assert not any("duplicate" in p for p in probs)


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

    def test_cli_exit_2_on_non_object_json(self, tmp_path):
        f = tmp_path / "q.json"
        f.write_text(json.dumps([mkitem()]), encoding="utf-8")
        with pytest.raises(SystemExit) as e:
            vq.main([str(f)])
        assert e.value.code == 2

    def test_cli_exit_1_on_non_dict_item(self, tmp_path):
        f = tmp_path / "q.json"
        f.write_text(json.dumps(mkqueue([42])), encoding="utf-8")
        with pytest.raises(SystemExit) as e:
            vq.main([str(f)])
        assert e.value.code == 1
