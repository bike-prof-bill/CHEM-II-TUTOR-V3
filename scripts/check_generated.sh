#!/bin/sh
# The committed generated files must be what run.py produces from the committed sources.
# Generation is deterministic; a mismatch means a hand edit or a forgotten regeneration.
set -e
cd "$(dirname "$0")/.."
GEN="gas/Archetype_ch10_cc.gs output/ch10_cc.bundle.json gas/Archetype_ch13_ice.gs output/ch13_ice.bundle.json gas/Units.gs"
mkdir -p /tmp/_gen_before
for f in $GEN; do cp "$f" /tmp/_gen_before/$(basename "$f"); done
python3 run.py all --per-kind 3 --seed 1 > /tmp/_gen_log.txt
cat /tmp/_gen_log.txt
bad=0
for f in $GEN; do cmp -s "$f" /tmp/_gen_before/$(basename "$f") || { echo "generated-check: $f differs"; bad=1; }; cp /tmp/_gen_before/$(basename "$f") "$f"; done
if [ "$bad" -eq 0 ]; then echo "generated-check: committed generated files match run.py output."
else echo "generated-check: FAILED. Run 'make generate' and commit."; exit 1; fi
