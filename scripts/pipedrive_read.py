#!/usr/bin/env python3
"""Read-only Pipedrive snapshot for the overnight sweep (/ct-sweep).

The plugin's SECOND sanctioned direct-REST script (first: pipedrive_participants.py).
This one is READ-ONLY — it never writes Pipedrive. The single-writer rule
(agents/sales-crm.md) governs writes and is untouched. Headless sweep runs use
this because the interactive Pipedrive MCP may be absent in scheduled sessions.

Env (see /ct-setup Section F):
    PIPEDRIVE_API_TOKEN   personal API token
    PIPEDRIVE_DOMAIN      e.g. cadtalk.pipedrive.com

Usage:
    python pipedrive_read.py snapshot --owner-id 123 --pipelines 1,2 --out snap.json

Output JSON:
    {"generated_at": iso, "owner_id": N, "pipelines": [..],
     "deals": [ raw Pipedrive deal fields + "_annotations": {
         days_in_stage, days_dark, stuck, dark, commit_review } ],
     "activities_due": [ raw open activities ]}

Annotations (deterministic pre-pass, spec Section 3):
    stuck         days_in_stage > 30
    dark          days_dark > 14 (no touch; falls back to add_time if never touched)
    commit_review Forecast Category is Definitely (13) or Probably (14)

Exit codes: 0 success · 1 API error · 2 usage/config error
"""

import argparse
import json
import os
import sys
from datetime import date, datetime

import requests

TIMEOUT = 30
STUCK_DAYS = 30
DARK_DAYS = 14
# Forecast Category field key + commit-relevant values (13=Definitely, 14=Probably).
# Source: references/pipedrive-custom-fields.md (audited data layer).
FORECAST_KEY = "1a706bae5b0046828ae5a1b573c722bd96068058"
COMMIT_VALUES = {"13", "14"}


def _parse_day(value):
    """'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS' -> date, else None."""
    if not value:
        return None
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def annotate_deal(deal: dict, today: date) -> dict:
    staged = _parse_day(deal.get("stage_change_time")) or _parse_day(deal.get("add_time"))
    touched = _parse_day(deal.get("last_activity_date")) or _parse_day(deal.get("add_time"))
    days_in_stage = (today - staged).days if staged else 0
    days_dark = (today - touched).days if touched else 0
    forecast = deal.get(FORECAST_KEY)
    return {
        "days_in_stage": days_in_stage,
        "days_dark": days_dark,
        "stuck": days_in_stage > STUCK_DAYS,
        "dark": days_dark > DARK_DAYS,
        "commit_review": str(forecast) in COMMIT_VALUES if forecast is not None else False,
    }


def filter_pipelines(deals: list, pipelines: list) -> list:
    keep = set(pipelines)
    return [d for d in deals if d.get("pipeline_id") in keep]


def _get(url: str, params: dict):
    """GET wrapper: clean exit on network/API failure; never echo the URL
    (api_token rides in the query string — a traceback would leak it)."""
    try:
        resp = requests.request("GET", url, timeout=TIMEOUT, params=params)
    except requests.exceptions.RequestException as exc:
        print(f"API ERROR: network failure ({type(exc).__name__}) — check the "
              "connection and PIPEDRIVE_DOMAIN, then retry.", file=sys.stderr)
        sys.exit(1)
    body = resp.json() if resp.status_code != 204 else {}
    if resp.status_code >= 400 or not body.get("success", False):
        print(f"API ERROR: HTTP {resp.status_code} — check the token and IDs.",
              file=sys.stderr)
        sys.exit(1)
    return body


def _paginate(url: str, token: str, extra: dict) -> list:
    items, start = [], 0
    while True:
        body = _get(url, {"api_token": token, "limit": 500, "start": start, **extra})
        items.extend(body.get("data") or [])
        page = (body.get("additional_data") or {}).get("pagination") or {}
        if not page.get("more_items_in_collection"):
            return items
        start = page.get("next_start", start + 500)


def fetch_all_deals(base: str, token: str, owner_id: int) -> list:
    return _paginate(f"{base}/deals", token, {"status": "open", "user_id": owner_id})


def fetch_open_activities(base: str, token: str, owner_id: int) -> list:
    return _paginate(f"{base}/activities", token, {"user_id": owner_id, "done": 0})


def base_url(domain: str) -> str:
    domain = domain.strip().rstrip("/")
    for prefix in ("https://", "http://"):
        if domain.startswith(prefix):
            domain = domain[len(prefix):]
    return f"https://{domain}/api/v1"


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(prog="pipedrive_read.py",
                                     description="Read-only Pipedrive snapshot.")
    sub = parser.add_subparsers(dest="command", required=True)
    snap = sub.add_parser("snapshot", help="write a snapshot JSON")
    snap.add_argument("--owner-id", type=int, required=True)
    snap.add_argument("--pipelines", required=True,
                      help="comma-separated pipeline ids, e.g. 1,2")
    snap.add_argument("--out", required=True, help="output JSON path")
    args = parser.parse_args(argv)

    token = os.environ.get("PIPEDRIVE_API_TOKEN")
    domain = os.environ.get("PIPEDRIVE_DOMAIN")
    if not token or not domain:
        print("CONFIG ERROR: set PIPEDRIVE_API_TOKEN and PIPEDRIVE_DOMAIN "
              "(see /ct-setup Section F).", file=sys.stderr)
        sys.exit(2)

    base = base_url(domain)
    pipelines = [int(p) for p in args.pipelines.split(",") if p.strip()]
    today = date.today()
    deals = filter_pipelines(fetch_all_deals(base, token, args.owner_id), pipelines)
    for d in deals:
        d["_annotations"] = annotate_deal(d, today)
    snapshot = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "owner_id": args.owner_id,
        "pipelines": pipelines,
        "deals": deals,
        "activities_due": fetch_open_activities(base, token, args.owner_id),
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, ensure_ascii=False, indent=1)
    print(f"snapshot: {len(deals)} deals, "
          f"{len(snapshot['activities_due'])} open activities -> {args.out}")


if __name__ == "__main__":
    main()
