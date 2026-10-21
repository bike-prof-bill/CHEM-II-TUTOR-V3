# Release: the chapter 11 pilot, The Salted Road (21 Oct 2026)

One new archetype built to brief 32, with the new ladder (pivot, then help by policy), More help and More info, the simulation
sequence, and the precision rule. The 23 older archetypes keep their content versions; their behaviour is unchanged except that
every archetype now has the two buttons and the policy menu on the preview page. Shell version ecb292d9; build stamp
V3-0.1-20261021-01.

## 1. Repository
Drop `CURRENT_repository_copy_into_CHEM-II-TUTOR-V3.zip` (Replace), then `make test`. New lines to expect:
- `ch11 (one archetype, 6 problems; 96 values re-derived): all checks pass`
- `node gas/test_ch11.js` ... `70 passed, 0 failed`
- `ch11_colligative: 200 runs, ... credits 0` in the random clicker
- `shell version ecb292d9 (Code.gs c40b4ad2) | build stamp V3-0.1-20261021-01`
- `[ch11_colligative] textbook passages for More info: 10`
Then drop `media_ch11_drop_into_CHEM-II-TUTOR-V3.zip` into the same folder (it adds `media/ch11/freezing_point_simulator.html`
and `media/ch11_colligative/salted_road.jpg`; nothing else).

## 2. Apps Script: eleven files
| file | new or replace |
|---|---|
| Archetype_ch11_colligative | **new** (+ Script, name it exactly) |
| Core | replace |
| parse | replace |
| match | replace |
| stepmap | replace |
| ladder | replace |
| log | replace |
| prompt | replace |
| Code | replace |
| Shell_version | replace |
| Units | replace |

Paste all eleven before saving the last; then **run `refreshHeaders` once** (select it in the function menu and press Run) so the
two new log columns (`policy`, `help_rung`) get their names; then Deploy → Manage deployments → pencil → New version → Deploy.
Reload /exec: `"build":"V3-0.1-20261021-01"`, shell_expected and shell_actual `ecb292d9`, 24 archetypes; `ch11_colligative`
with content_version 0147ae933a.

Optional script property: `HELP_POLICY` = A, B or C sets the default policy for students (B if unset). The preview menu
overrides it per problem.

## 3. Netlify
`sh scripts/make_netlify_site.sh` (expect `media files the tutor refers to: 121; present: 121; missing: 0` once the media zip is
in), then drag `deploy/netlify_site`.

## 4. Try it (preview page)
Pick `Ch 11 · Freezing point depression`, Help B, New problem. The conversation is `docs/35`. Things to try on purpose: a wrong
number twice (the pivot), a third time (the companion), a fourth (the notebook), a fifth (park); More help; More info at any step;
the prediction then the page (your freezing point and prediction marked); the slider task; type 1.3-style coarse values (the
precision rule). Switch to Help A or C and repeat.

## Content versions
Unchanged for the 23 older archetypes (see docs/30). New: ch11_colligative 0147ae933a.
