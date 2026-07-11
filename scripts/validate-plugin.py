#!/usr/bin/env python3
"""
validate-plugin.py — CADTALK sales-team plugin structure validator.

Run before every version bump and as a pre-commit hook. Catches the failure
modes that silently drop skills/agents from Claude Code autocomplete.

FAIL (exit 1):
  - A skills/*/SKILL.md or agents/*.md lacks valid YAML frontmatter
    (missing opening `---`, missing `name:`, or missing `description:`).
  - A `description:` uses multiline YAML (`|` or `>` block scalar) or spans
    multiple lines — the skill indexer mis-parses these and drops the skill.
  - A plugin.json `skills` array exists but is incomplete. The array should be
    ABSENT (Claude Code auto-discovers skills/*/SKILL.md); an explicit list is
    the exact thing that drifts.

WARN (exit 0):
  - A skill has no routing row in the plugin CLAUDE.md (docs table feeds
    ct-help and description drafting; frontmatter is what actually ships).

Usage: python scripts/validate-plugin.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILURES = []
WARNINGS = []


def parse_frontmatter(path):
    """Return (fields, error). fields is a dict of frontmatter keys.
    error is a string if the block is malformed, else None."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "no opening '---' frontmatter delimiter"
    # find closing delimiter
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, "no closing '---' frontmatter delimiter"
    fields = {}
    for i in range(1, end):
        line = lines[i]
        m = re.match(r"^([A-Za-z0-9_-]+):\s?(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2)
        fields[key] = val
    return fields, None


def check_multiline_description(path):
    """Return error string if description is multiline/block-scalar, else None."""
    fields, err = parse_frontmatter(path)
    if err:
        return None  # frontmatter error already reported elsewhere
    desc = fields.get("description")
    if desc is None:
        return None
    stripped = desc.strip()
    if stripped in ("|", ">", "|-", ">-", "|+", ">+"):
        return "description uses a multiline YAML block scalar (indexer drops the skill)"
    if stripped == "":
        return "description is empty or continues on the next line (must be single-line)"
    return None


def validate_frontmatter_files():
    targets = sorted((ROOT / "skills").glob("*/SKILL.md")) + sorted(
        (ROOT / "agents").glob("*.md")
    )
    for path in targets:
        rel = path.relative_to(ROOT)
        fields, err = parse_frontmatter(path)
        if err:
            FAILURES.append(f"{rel}: {err}")
            continue
        if "name" not in fields:
            FAILURES.append(f"{rel}: frontmatter missing 'name:'")
        if "description" not in fields:
            FAILURES.append(f"{rel}: frontmatter missing 'description:'")
        ml = check_multiline_description(path)
        if ml:
            FAILURES.append(f"{rel}: {ml}")


def validate_plugin_json():
    pj = ROOT / ".claude-plugin" / "plugin.json"
    if not pj.exists():
        FAILURES.append(".claude-plugin/plugin.json: missing")
        return
    data = json.loads(pj.read_text(encoding="utf-8"))
    if "skills" not in data:
        return  # correct — auto-discovery
    listed = {Path(s).name for s in data["skills"]}
    actual = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
    missing = actual - listed
    FAILURES.append(
        ".claude-plugin/plugin.json: a 'skills' array exists — it should be "
        "REMOVED (Claude Code auto-discovers skills/*/SKILL.md)."
        + (f" It is also incomplete, missing: {sorted(missing)}" if missing else "")
    )


def validate_claude_md_rows():
    claude_md = ROOT / "CLAUDE.md"
    if not claude_md.exists():
        WARNINGS.append("CLAUDE.md: missing (routing table feeds ct-help)")
        return
    text = claude_md.read_text(encoding="utf-8")
    for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        name = path.parent.name
        if f"/{name}`" not in text and f"/{name} " not in text:
            WARNINGS.append(f"CLAUDE.md: no routing row for /{name}")


def main():
    validate_frontmatter_files()
    validate_plugin_json()
    validate_claude_md_rows()

    for w in WARNINGS:
        print(f"WARN  {w}")
    for f in FAILURES:
        print(f"FAIL  {f}")

    if FAILURES:
        print(f"\n{len(FAILURES)} failure(s), {len(WARNINGS)} warning(s). Plugin INVALID.")
        return 1
    print(f"\nOK — 0 failures, {len(WARNINGS)} warning(s). Plugin valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
