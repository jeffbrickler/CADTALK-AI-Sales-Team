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
