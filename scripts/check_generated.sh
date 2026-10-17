#!/bin/sh
# The committed generated files must be what run.py produces from the committed sources.
# Generation is deterministic; a mismatch means a hand edit or a forgotten regeneration.
set -e
cd "$(dirname "$0")/.."
GEN="gas/Shell_version.gs gas/Archetype_ch10_cc.gs gas/Archetype_ch10_cc_test.gs output/ch10_cc.bundle.json gas/Units.gs gas/Tone.gs gas/Archetype_ch13_eq_test.gs gas/Archetype_ch14_ph_test.gs gas/Archetype_ch14_ph.gs output/ch14_ph.bundle.json gas/Archetype_ch14_acidbase_test.gs gas/Archetype_ch14_acidbase.gs output/ch14_acidbase.bundle.json gas/Archetype_ch14_buffer_test.gs gas/Archetype_ch14_titration_test.gs gas/Archetype_ch15_ksp_test.gs gas/Archetype_ch15_common_ion_test.gs gas/Archetype_ch15_qsp_test.gs gas/Archetype_ch15_complex_test.gs gas/Archetype_ch13_eq.gs output/ch13_eq.bundle.json"
mkdir -p /tmp/_gen_before
for f in $GEN; do cp "$f" /tmp/_gen_before/$(basename "$f"); done
python3 run.py all --per-kind 3 --seed 1 > /tmp/_gen_log.txt
cat /tmp/_gen_log.txt
bad=0
for f in $GEN; do cmp -s "$f" /tmp/_gen_before/$(basename "$f") || { echo "generated-check: $f differs"; bad=1; }; cp /tmp/_gen_before/$(basename "$f") "$f"; done
if [ "$bad" -eq 0 ]; then echo "generated-check: committed generated files match run.py output."
else echo "generated-check: FAILED. Run 'make generate' and commit."; exit 1; fi
