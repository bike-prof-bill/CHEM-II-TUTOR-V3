# Release checklist: chapter 13 (15 Oct 2026)

Do these in order. Each line says where.

## A. Repository
1. Drop `ch13_release_copy_into_repository.zip` the usual way. Then, in Finder, rename `media/ch13_ice` to `media/ch13_eq` and put the
   three floaters' files in it (`silent_beaker_simulator.html`, `purple_piston_simulator.html`, `fading_brown_simulator.html`, the
   three pictures). Commit.

## B. Apps Script (the brain)
2. Paste, one file each, replacing the old text: `Core`, `stepmap`, `Code`, `Shell_version`.
3. Make a new script file `Archetype_ch13_eq` and paste `gas/Archetype_ch13_eq.gs` into it.
4. Delete the script file `Archetype_ch13_ice`.
5. Deploy → Manage deployments → pencil → Version: New version → Deploy.
6. Open the `/exec` URL. Expect: `shell_expected` and `shell_actual` both `61bae0be`, `shell_ok` true; archetypes `ch10_cc` at
   `3c7a971cb6` and `ch13_eq` at `0948c5d45d` with five openers listed; no `ch13_ice`.

## C. Netlify (the faculty preview page)
7. `cp deploy/config.example.js deploy/config.js`; put the `/exec` URL and APP_TOKEN in it, and your email in `preview.contact`. Leave the `preview` block in: it turns on the yellow banner, the rung menu, the comment link, and logs every session under `preview:<name>`. For a student site later, remove `preview`.
8. `sh scripts/make_netlify_site.sh` (it warns if `media/ch13_eq` is missing).
9. Drag `deploy/netlify_site` onto https://app.netlify.com/drop. Open the address it gives; the yellow bar should show. Run one chapter 13 problem at Worked; see a log row with student_id `preview:...`.
10. Send reviewers the address and `docs/18_FACULTY_PREVIEW_GUIDE.md` (one page).

## D. Afterwards
- Students' chapter 13 rung records start fresh under `ch13_eq` (none exist yet).
- The analysis lane should expect `archetype_id = ch13_eq` from this day, with `problem_kind` in {haber_setup, wgs_equilibrium,
  agcl_tracer, agbr_tracer, agi_tracer, hi_volume, hi_equilibrium, no2_equilibrium}.
