#!/usr/bin/env bash
#
# sync-voice.sh — pull the CADTALK voice standard from its source-of-truth repo
# into this plugin (vendored sync).
#
# Source of truth: https://github.com/jeffbrickler/cadtalk-voice
#   SKILL.md                                      -> skills/ct-voice/SKILL.md (frontmatter swapped)
#   references/CADTALK-Unified-Voice-Reference.md -> references/cadtalk-voice-reference.md (verbatim)
#
# The reference doc is copied verbatim — it is the one standard every content
# skill (ct-outreach, ct-followup, ct-proposal, ct-prep, ct-se) already defers
# to, so they pick up the update for free. The ct-voice SKILL body is copied
# from upstream but its frontmatter is replaced with scripts/ct-voice-frontmatter.md
# so the plugin skill keeps name: ct-voice and a single-line (indexer-safe)
# description regardless of how upstream writes its own frontmatter.
#
# Usage:  scripts/sync-voice.sh [ref]      (ref defaults to main; can be a tag)
# After a sync: run scripts/validate-plugin.py, bump the plugin version, and ship.

set -euo pipefail

REPO_URL="${CADTALK_VOICE_REPO:-https://github.com/jeffbrickler/cadtalk-voice}"
REF="${1:-main}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FRONTMATTER="$ROOT/scripts/ct-voice-frontmatter.md"

if [ ! -f "$FRONTMATTER" ]; then
  echo "error: $FRONTMATTER not found (needed to rebuild ct-voice frontmatter)" >&2
  exit 1
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Cloning $REPO_URL@$REF ..."
git clone --depth 1 --branch "$REF" "$REPO_URL" "$TMP/voice" -q

SRC_SKILL="$TMP/voice/SKILL.md"
SRC_REF="$TMP/voice/references/CADTALK-Unified-Voice-Reference.md"
for f in "$SRC_SKILL" "$SRC_REF"; do
  [ -f "$f" ] || { echo "error: expected file missing in upstream: $f" >&2; exit 1; }
done

# 1. Reference doc — verbatim.
cp "$SRC_REF" "$ROOT/references/cadtalk-voice-reference.md"

# 2. ct-voice SKILL.md — plugin frontmatter + upstream body (everything after
#    upstream's second '---' frontmatter fence).
{
  cat "$FRONTMATTER"
  echo ""
  awk 'fence>=2 { print } /^---[[:space:]]*$/ { fence++ }' "$SRC_SKILL"
} > "$ROOT/skills/ct-voice/SKILL.md"

VER="$(cat "$TMP/voice/VERSION" 2>/dev/null || echo unknown)"
echo "Synced voice standard v$VER from $REPO_URL@$REF."
echo "Next: python scripts/validate-plugin.py  &&  bump version  &&  /ship"
