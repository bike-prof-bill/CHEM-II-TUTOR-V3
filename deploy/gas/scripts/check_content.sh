#!/bin/sh
# Every authored string in the baseline must still be present, unchanged.
# Additions (a new column, a new row) are reported but allowed; removals and
# edits fail. Step 5 of the spec: the diff of authored strings is empty.
set -e
cd "$(dirname "$0")/.."
if [ ! -f content/BASELINE_authored.txt ]; then
  echo "content-check: no baseline. Run 'make baseline' ONCE from the unchanged files, then commit it."
  exit 1
fi
python3 scripts/snapshot_content.py content/CURRENT_authored.txt
missing=$(comm -23 content/BASELINE_authored.txt content/CURRENT_authored.txt)
added=$(comm -13 content/BASELINE_authored.txt content/CURRENT_authored.txt)
if [ -n "$added" ]; then
  echo "content-check: $(printf '%s\n' "$added" | wc -l | tr -d ' ') authored string(s) ADDED since baseline (allowed, listed):"
  printf '%s\n' "$added" | head -30
fi
if [ -n "$missing" ]; then
  echo "content-check: FAILED. $(printf '%s\n' "$missing" | wc -l | tr -d ' ') baseline string(s) changed or removed:"
  printf '%s\n' "$missing" | head -30
  exit 1
fi
echo "content-check: every baseline authored string present and unchanged."
