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
