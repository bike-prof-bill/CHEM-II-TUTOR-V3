#!/bin/sh
# Builds deploy/netlify_site: the static tutor page and its media, ready to drag onto app.netlify.com/drop (or `netlify deploy --prod --dir deploy/netlify_site`).
# The backend stays on Apps Script; the page calls the /exec URL in config.js. Run from the repository root after `make test`.
set -e
OUT=deploy/netlify_site
rm -rf "$OUT"; mkdir -p "$OUT"
cp index.html "$OUT/"
[ -d media ] && cp -R media "$OUT/media" || echo "WARNING: no media/ folder here; copy it into $OUT/media before deploying"
[ -d "$OUT/media/ch13_eq" ] || echo "WARNING: media/ch13_eq/ is missing; the chapter 13 rows point there (rename media/ch13_ice and add the three floaters' files)"
cp deploy/netlify.toml "$OUT/netlify.toml"
if [ -f deploy/config.js ]; then cp deploy/config.js "$OUT/config.js"; else echo "NOTE: no deploy/config.js; students will see the settings box. Copy deploy/config.example.js to deploy/config.js and fill it in."; fi
find "$OUT" -name ".DS_Store" -delete
echo "site built in $OUT ($(find "$OUT" -type f | wc -l | tr -d ' ') files)"
