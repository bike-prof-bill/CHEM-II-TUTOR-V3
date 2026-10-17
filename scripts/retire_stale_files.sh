#!/bin/sh
# Dropping a zip adds and replaces files; it never deletes. This removes the files retired since 13 Oct 2026 if they are still here
# (ch13_ice and the ch13_q_vs_k skeleton, both replaced by ch13_eq). Safe to run any time; it only touches the names listed.
cd "$(dirname "$0")/.." || exit 1
n=0
for f in archetypes/ch13_ice.py archetypes/ch13_q_vs_k.py \
         content_ch13_ice_openers.csv content_ch13_ice_moves.csv content_ch13_ice_errors.csv \
         content_ch13_q_vs_k_openers.csv content_ch13_q_vs_k_moves.csv content_ch13_q_vs_k_errors.csv \
         test_ch13_ice.py test_ch13_q_vs_k.py gas/test_ice.js gas/test_q_vs_k.js \
         gas/Archetype_ch13_ice.gs gas/Archetype_ch13_ice_test.gs gas/Archetype_ch13_q_vs_k.gs gas/Archetype_ch13_q_vs_k_test.gs \
         output/ch13_ice.bundle.json output/ch13_q_vs_k.bundle.json \
         tests/fixtures/content_ch13_ice_openers_allkinds.csv tests/fixtures/content_ch13_q_vs_k_openers_allkinds.csv \
         docs/14_SCENARIO_CLAUDE_brief_Q_vs_K.md; do
  if [ -e "$f" ]; then rm -f "$f"; echo "removed $f"; n=$((n+1)); fi
done
[ -d media/ch13_ice ] && [ ! -d media/ch13_eq ] && mv media/ch13_ice media/ch13_eq && echo "renamed media/ch13_ice to media/ch13_eq" && n=$((n+1))
echo "retired files removed: $n. Now run: make test"
