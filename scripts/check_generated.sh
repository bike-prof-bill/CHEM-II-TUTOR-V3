#!/bin/sh
# The committed generated files must be what run.py produces from the committed
# sources. Generation is deterministic; a mismatch means someone edited the
# generated file by hand or forgot to regenerate after a source change.
set -e
cd "$(dirname "$0")/.."
cp gas/Archetype_ch10_cc.gs /tmp/_gen_before.gs
cp output/ch10_cc.bundle.json /tmp/_gen_before.json
python3 run.py ch10_cc --per-kind 3 --seed 1 > /tmp/_gen_log.txt
cat /tmp/_gen_log.txt
if cmp -s gas/Archetype_ch10_cc.gs /tmp/_gen_before.gs && cmp -s output/ch10_cc.bundle.json /tmp/_gen_before.json; then
  echo "generated-check: committed generated files match run.py output."
else
  echo "generated-check: FAILED. Committed gas/Archetype_ch10_cc.gs or output/ch10_cc.bundle.json differ from run.py output. Run 'make generate' and commit."
  cp /tmp/_gen_before.gs gas/Archetype_ch10_cc.gs; cp /tmp/_gen_before.json output/ch10_cc.bundle.json
  exit 1
fi
