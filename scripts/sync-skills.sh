#!/usr/bin/env bash
#
# sync-skills.sh — vendor the externalized CADTALK sales skills into this plugin.
#
# Each skill is maintained in its own source-of-truth repo (see CLAUDE.md,
# "Skills — externalized source of truth"). This script clones each repo at the
# given ref and regenerates the vendored copies below. Do NOT hand-edit the
# vendored files — edit the upstream repo, bump its VERSION, then re-run this.
#
# Voice has its own sync (scripts/sync-voice.sh); it is intentionally separate.
#
# Usage: scripts/sync-skills.sh [ref]   (default ref: main)
#
set -euo pipefail

REF="${1:-main}"
GH="${CADTALK_SKILLS_GH_OWNER:-jeffbrickler}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# print body AFTER the 2nd '---' fence (strip YAML frontmatter)
strip_fm() { awk 'fence>=2 { print } /^---[[:space:]]*$/ { fence++ }' "$1"; }
# same, but also trim leading blank lines of the body
strip_fm_trim() { strip_fm "$1" | awk 'NF{p=1} p'; }

clone() { # $1=repo slug -> $TMP/$1
  local url="https://github.com/${GH}/$1"
  git clone --depth 1 --branch "$REF" "$url" "$TMP/$1" -q
}

echo "Syncing externalized skills from ${GH} @ ${REF}"

# 1. discovery-review-scorecard -> skills/ct-score/SKILL.md  (frontmatter pinned)
clone discovery-review-scorecard
{ cat "$ROOT/scripts/ct-score-frontmatter.md"; echo ""; strip_fm_trim "$TMP/discovery-review-scorecard/SKILL.md"; } \
  > "$ROOT/skills/ct-score/SKILL.md"
echo "  ✓ skills/ct-score/SKILL.md"

# 2. commit-gate-scorecard -> skills/ct-commit/SKILL.md  (frontmatter pinned)
clone commit-gate-scorecard
{ cat "$ROOT/scripts/ct-commit-frontmatter.md"; echo ""; strip_fm_trim "$TMP/commit-gate-scorecard/SKILL.md"; } \
  > "$ROOT/skills/ct-commit/SKILL.md"
echo "  ✓ skills/ct-commit/SKILL.md"

# 3. cro-deal-coach -> references/deal-coach.md  (frontmatter stripped, body verbatim)
clone cro-deal-coach
strip_fm_trim "$TMP/cro-deal-coach/SKILL.md" > "$ROOT/references/deal-coach.md"
echo "  ✓ references/deal-coach.md"

# 4. proposal-decision-gate -> templates/decision-gate/*.md  (verbatim)
clone proposal-decision-gate
cp "$TMP/proposal-decision-gate/templates/"*.md "$ROOT/templates/decision-gate/"
echo "  ✓ templates/decision-gate/*.md"

# 5. pipedrive-update -> references/pipedrive-{custom-fields,stage-ids}.md  (verbatim)
clone pipedrive-update
cp "$TMP/pipedrive-update/references/custom-fields.md" "$ROOT/references/pipedrive-custom-fields.md"
cp "$TMP/pipedrive-update/references/stage-ids.md"     "$ROOT/references/pipedrive-stage-ids.md"
echo "  ✓ references/pipedrive-custom-fields.md + pipedrive-stage-ids.md"

echo "Done. Review the diff, run: python scripts/validate-plugin.py"
