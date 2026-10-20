# Putting the tutor page on Netlify (15 Oct 2026)

The tutor has two halves. The brain (checks, Gemini, the log) runs on Google Apps Script at the `/exec` address; that does not
move. The page students see (`index.html`) and its pictures and simulations (`media/`) are plain files, and those go on Netlify.
The full move of the brain to Netlify stays a December job, as the spec says.

## Steps
1. `cp deploy/config.example.js deploy/config.js` and put in it the `/exec` URL and the APP_TOKEN. Keep `deploy/config.js` out of
   git (it is in `.gitignore`).
2. Make sure `media/ch13_eq/` holds the chapter 13 files: the five from `media/ch13_ice/` (rename the folder) plus the three
   floaters' pictures and pages from SCENARIO_CLAUDE and Simulation_Claude.
3. `sh scripts/make_netlify_site.sh` → `deploy/netlify_site/`. It lists every picture and simulation the tutor refers to (20 today) and marks any missing from `media/`; fix those before step 4. The site gets a `gallery.html` with all of them, linked from the yellow bar.
4. Open https://app.netlify.com/drop and drag the `netlify_site` folder onto it. Netlify gives a `*.netlify.app` address; rename
   the site in Site settings if you like. (Or, with the Netlify CLI: `netlify deploy --prod --dir deploy/netlify_site`.)
5. Open the address. "New problem" should work at once with no settings box. Add `?debug=1` to see the raw server replies.
6. Each later release: repeat 3 and 4. Apps Script pastes are separate and still needed for any change to the brain.

## What to check once
- The alive reply (`/exec` in a browser) lists `ch10_cc` and `ch13_eq` with the content versions the report names.
- A picture loads (the Drinking Bird opener) and a simulation opens (the alcohol page), which proves `media/` landed.
- A log row appears in the Sheet after one turn, which proves the page is talking to the brain from its new address.
