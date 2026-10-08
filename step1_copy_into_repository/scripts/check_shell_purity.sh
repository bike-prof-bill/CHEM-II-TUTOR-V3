#!/bin/sh
# Spec, test 3: "Nothing in the shell may name chemistry." grep the shell for
# ice, clausius, kelvin, atm: zero hits outside the data files.
#
# "ice" is matched as a whole word (device, choice, notice are not chemistry); the others match anywhere.
# SHELL_FILES lists every file that must know no chemistry. Data and chemistry
# files are not searched. Until step 3 this reports; CI does not block on it.
cd "$(dirname "$0")/.."
SHELL_FILES="engine.py gas/Core.gs gas/local_server.js index.html"
# Step 4 module split adds: gas/parse.js gas/match.js gas/stepmap.js gas/ladder.js gas/guards.js gas/prompt.js gas/log.js
WORDS='\bice\b|clausius|kelvin|atm'
hits=0
for f in $SHELL_FILES; do
  [ -f "$f" ] || { echo "purity: $f not found (skipped)"; continue; }
  n=$(grep -inE "$WORDS" "$f" | wc -l | tr -d ' ')
  if [ "$n" -gt 0 ]; then
    echo "purity: $n hit(s) in $f"
    grep -inE "$WORDS" "$f" | head -20
    hits=$((hits + n))
  fi
done
if [ "$hits" -eq 0 ]; then
  echo "purity: shell names no chemistry."
else
  echo "purity: $hits hit(s) total. Required to be 0 at step 3."
  exit 1
fi
