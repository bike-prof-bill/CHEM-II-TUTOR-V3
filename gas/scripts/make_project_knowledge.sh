#!/bin/sh
# Builds the "project knowledge" zip: every readable source of truth, flattened (the project knowledge uploader keeps no folders),
# so a new chat in the project starts from the present. Excludes generated files, binaries and tests.
# Usage: sh scripts/make_project_knowledge.sh <output zip>
set -e
cd "$(dirname "$0")/.."
OUT="${1:-project_knowledge_$(date +%Y-%m-%d).zip}"; TMP=$(mktemp -d)
add() { f="$1"; n=$(echo "$f" | sed 's|/|__|g'); cp "$f" "$TMP/$n"; }
for f in README.md REPOSITORY.md BUILD_LOG.md INSTALL_CHEAT_SHEET.md GUIDE_MOVES_AND_OPENERS.md units.json content_*.csv \
         docs/*.md docs/*.csv docs/briefs_and_design/*.md docs/instructor_source_material/* \
         archetypes/*.py archetypes/data/*.json archetypes/data/*.md \
         gas/Core.gs gas/parse.gs gas/match.gs gas/stepmap.gs gas/ladder.gs gas/guards.gs gas/prompt.gs gas/log.gs gas/logqueue.gs gas/Code.gs gas/local_server.js \
         engine.py run.py tests/regression/README.md; do
  [ -f "$f" ] && add "$f"
done
cat > "$TMP/00_READ_ME_FIRST_project_knowledge.md" << 'EOT'
# Project knowledge: what this folder is

Built from the repository on the date in the zip's name by `scripts/make_project_knowledge.sh`. Folder names are flattened into
file names with `__` (so `docs__STEP_MAP_rules_everywhere.csv` is `docs/STEP_MAP_rules_everywhere.csv` in the repository).

Read first: `BUILD_LOG.md` (what has been built, step by step, with the instructor's decisions), then the role document for the
lane you are in (`docs__04_SIMULATION_CLAUDE_role_DRAFT.md`, `docs__06_SCENARIO_CLAUDE_role_DRAFT.md`), then
`docs__STEP_MAP_ch10_cc_Rubbing_Alcohol_Chill.csv` and `docs__STEP_MAP_rules_everywhere.csv`.

Not here: generated files (`gas/Archetype_*.gs`, `gas/Units.gs`, `output/*.json`), pictures and simulations (`media/`), tests.
Those live in the repository. The instructor's `media/` folder is his and Simulation_Claude's.
EOT
case "$OUT" in /*) ABS="$OUT" ;; *) ABS="$PWD/$OUT" ;; esac; rm -f "$ABS"; (cd "$TMP" && zip -qr "$ABS" .)
echo "$(ls "$TMP" | wc -l | tr -d ' ') files -> $OUT"; rm -rf "$TMP"
