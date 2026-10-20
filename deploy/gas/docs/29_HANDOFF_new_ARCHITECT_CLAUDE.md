# Handoff to the next ARCHITECT_CLAUDE (from Fable, the third architect, 20 Oct 2026)

Read this first, then `BUILD_LOG.md` (the dated record of every change and ruling), then the documents it names as you need
them. The full conversation that built most of what is below is in the transcripts directory; search it rather than reading it whole.

## The people and the roles
- **The instructor** (40 years teaching chemistry, Marshall University, CHM 212) owns every teaching decision, approves every
  word a student reads, and reads everything you send. His time is the scarce resource of this project. He wrote the
  scenarios' substance over days; your work on them takes minutes. Respect that ratio.
- **You, ARCHITECT_CLAUDE ("Fable" was my name):** structure, the shell, the factory, the archetypes' design, data and analysis
  design, tests, releases, grant consulting, and consultant to the others. Your role does not change because a task is large.
- **SCENARIO_CLAUDE:** writes scenarios, problems, the named errors' questions, and briefs Simulation_Claude. A new one started
  20 Oct with `docs/26`, `docs/27` and `docs/28`. Questions between you go through the instructor.
- **Simulation_Claude:** builds the interactive pages under `media/`. **Opus** (constructor) may fill archetypes on request.
- **The analysis lane:** measures, never modifies. Keep the separation.

## Standing rules (every reply)
1. No sycophancy: no praise, no padding.
2. Plain speech at college-graduate level; jargon only when unavoidable, then defined.
3. Every deliverable has two sections, in order: **Needs your decision** (short list, each with a recommendation), then
   **Engineering** (skippable).
4. Anything marked DRAFT must not reach a student until he approves it. The factory enforces this.
5. Do not change the teaching without asking. When a rule of his collides with a request of his, say so and ask.
Lessons from my mistakes: count before you report (I once wrote "four scenarios" for six, and "sixteen gaps" for seventeen);
check claims against the code before stating them (I once said the model graded text steps; it had not since 11 Oct); refer to
files by their names; when he asks for everything at once, deliver everything at once.

## What exists (20 Oct 2026)
Twenty-three archetypes, all with approved scenarios, released together on 19 Oct; shell version a819f89c.

| chapter | archetypes |
|---|---|
| 10 | ch10_cc (generated problems; 4 scenarios, target 7) |
| 13 | ch13_eq (one archetype covering ICE, Q vs K, Le Chatelier; 5 scenarios, target 6) |
| 14 | ch14_ph, ch14_acidbase, ch14_buffer, ch14_titration |
| 15 | ch15_ksp, ch15_common_ion, ch15_qsp, ch15_complex |
| 16 | ch16_entropy, ch16_free_energy, ch16_spontaneity, ch16_equilibrium_G, ch16_G_and_K |
| 17 | ch17_balancing, ch17_cell, ch17_E_G_K, ch17_nernst, ch17_electrolysis |
| 19 | ch19_cft |
| 21 | ch21_decay, ch21_binding |
Chapters 11 and 12 (eight archetypes) are designed in `docs/27` and wait for SCENARIO_CLAUDE's sheets. V2 (the earlier tutor)
runs in CHM 212 and collects data; V3 (this repository) runs behind a faculty preview page on Netlify.

## How it is built
- **The factory** (`run.py`, `engine.py`): reads each archetype's Python file and its content CSVs (openers, moves, errors), makes
  every problem, validates it (no two values a typed number could match; named mistakes clear of right values; a mistake that
  equals a given is dropped as undetectable), and writes `gas/Archetype_<id>.gs` (shipped) and `output/<id>.bundle.json`. It
  refuses to ship an archetype while any DRAFT row applies. It reports each archetype's scenarios against the instructor's targets.
- **Three kinds of archetype file:**
  - *generated* (`ch10_cc.py`): problems drawn from data (`archetypes/data/substances.json`) within per-scenario limits
    (`content_ch10_cc_limits.csv`), plus coded scene rules in `draw_state`;
  - *hand-coded fixed* (`ch13_eq.py`, chapter 14 and 15 files, with `_equilibrium.py`, `_acidbase.py`, `_solubility.py`): every
    number computed from constants in `archetypes/data/*.json`;
  - *sheet-driven* (chapters 16 to 21, and 11 and 12 next): `scripts/sheet_to_problems.py` turns an approved problem sheet into
    `archetypes/data/sheets/<id>.json`; `archetypes/_sheet.py` builds each problem's board from a step order, option sets,
    tolerances (the sheet's own column first) and simulation values (the sheet's own column first, else read from the sentence).
    A new sheet archetype is a short file like `ch17_cell.py`.
- **The shell** (`gas/`, pasted into Google Apps Script; the brain): `Core.gs` orders the modules (built lazily, so file order in
  Apps Script does not matter); `stepmap.gs` (the board), `parse.gs` (numbers, units, typed arithmetic), `match.gs` (values,
  equations by substitution, tables), `ladder.gs` (two wrong tries to the notebook, two more parks the step; the rung ladder),
  `guards.gs` (leak guard, banned openers, no question after completion except the labelled parting thought), `prompt.gs` (what
  the model sees: never an answer), `Code.gs` (requests, preview mode, the 50-column log), `Tone.gs` (generated: approved tone
  phrases, completion phrases, account probes), `Units.gs` (generated from `units.json`). A test proves the shell names no
  chemistry.
- **The page** (`index.html`, deployed to Netlify with `scripts/make_netlify_site.sh`): reads `deploy/config.js`; a `preview`
  block there turns on the faculty mode (yellow bar, rung menu, comment box, logging under preview:). The config holds the token
  and never travels in the zips.
- **Tests:** `make test` runs everything (per-chapter Python tests that re-derive every number independently, shell harness walks,
  random-clicker regressions over all archetypes, unit tests, the simulation-address audit, generated-file and content-baseline
  checks). `make baseline` re-snapshots approved text; do it only when approved text changed on his word.

## The release routine
1. Build here, `make test` green.
2. Give him: the repository zip (he drops it into CHEM-II-TUTOR-V3 and runs `sh scripts/retire_stale_files.sh` and `make test`
   himself; his green run is the proof the folder matches), the paste set (every non-test `gas/*.gs`, with a checklist naming
   each new or replace and the alive reply to expect), the page if it changed, the media zip if media changed.
3. He pastes, makes a New version (never a New deployment), reloads /exec and checks shell and content versions.
4. He builds and drags `deploy/netlify_site` (the folder itself) onto the site's Deploys page.
Pitfalls already met: his folder lagged a week behind the zips (a drop never deletes); a file pasted into the wrong Apps Script
file; a copied archetype file kept its old content; student mode shown because config.js lacked the preview block.

## What is open
1. **This week (his target):** chapter 10 to 7 scenarios, chapter 13 to 6, chapters 11 and 12 built at 6 each. When the sheets
   come: convert, write the eight short archetype files to the step orders in `docs/27`, add the per-chapter Python test
   (re-derive every number from the sentences) and harness walk, wire both into the Makefile, `check_generated.sh` and the
   random clicker. Chapter 10 scenarios may need scene rules coded in `draw_state`; chapter 13's sixth is hand-encoded in `ch13_eq.py`.
2. **Simulations must be active (his rule, 20 Oct).** Seventeen problems name data their page lacks (`docs/27`, end); the test
   `tests/regression/sim_addresses.py` lists them and fails on any new gap. Chapters 11 and 12 need pages.
3. **The audit (`The Guarded Tutor against the neuro-symbolic gold standard`, a doc in this project):** nine ranked improvements;
   six need his ruling. Items 3 to 5 (unnamed-error mining, a red-team suite, generated state diagrams) need none.
4. **Smaller:** the Bleach Puzzle's Kb-step question is my plain wording, approved, rewritable by SCENARIO_CLAUDE; the
   "dilution ignored" mistake is often undetectable in chapter 15 because of the numbers chosen (fix in future numbers, not code).
5. **His talk** (two weeks from 16 Oct): the deck is a Slides artifact in this project; the demo script and handout are in
   `docs/talks/`.
6. **Grant:** the HEPC STaR draft is in `docs/grants/`; Encova was set aside until spring.

## Content versions at handoff
- ch10_cc: 3c7a971cb6
- ch13_eq: fe4f9eeb27
- ch14_acidbase: 53ded9568d
- ch14_buffer: 87e7ecfa2a
- ch14_ph: 1a89944180
- ch14_titration: 472782f756
- ch15_common_ion: 2c42d7686c
- ch15_complex: d25bc5255e
- ch15_ksp: a39a63edb9
- ch15_qsp: 408904f2d8
- ch16_G_and_K: dfbe04700f
- ch16_entropy: b243817d25
- ch16_equilibrium_G: 3b3d2d38ea
- ch16_free_energy: fcbfd02411
- ch16_spontaneity: ae111a7022
- ch17_E_G_K: d203bc65e3
- ch17_balancing: 836fda9a66
- ch17_cell: 579ee9bde7
- ch17_electrolysis: 4f77e232eb
- ch17_nernst: d8ffa79157
- ch19_cft: 7b7a452133
- ch21_binding: 5d9d14083a
- ch21_decay: 0500a17d05

Shell version a819f89c. The last green run on his machine was 19 Oct, before the 20 Oct changes (simulation values, units, option sets, the tolerance column, the menu); those are green here and in the current zips.
