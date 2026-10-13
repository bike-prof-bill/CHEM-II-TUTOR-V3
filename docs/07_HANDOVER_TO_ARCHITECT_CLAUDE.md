# Handover from Fable to ARCHITECT_CLAUDE (11 Oct 2026)

Read this, then `BUILD_LOG.md` (every decision and every change, dated), then `docs/02_REBUILD_SPEC_spine_v2.md` and
`docs/00_HANDOFF_READ_FIRST.md` for the original brief. The instructor owns every teaching decision; you own structure. The standing
rules at the top of the project instructions apply unchanged: no praise, plain speech, two sections in every deliverable
(**Needs your decision** first, then **Engineering**), DRAFT never reaches a student unapproved, do not change the teaching without asking.

## Where things stand

- **The spine rebuild (steps 1–5) is complete**, plus step 6a (the log never loses a row) and 6b (no repeated problems). 6c (distress
  check) waits on the instructor's wording and resources; 6d (compliance list) on his requirements. `docs/03_STEP_6_PROPOSAL_DRAFT.md`.
- **Clausius-Clapeyron (`ch10_cc`) is closed for now**: four scenarios, 24 problems, every authored row approved, a simulator for
  each scenario, two videos, two pictures, all in `docs/MEDIA_SOURCES.csv`. Scenarios: The Rubbing Alcohol Chill (ΔHvap kinds),
  The Syringe Boiling Trick and The Drinking Bird (pressure kinds), The Deep-Sea Vent (temperature kinds). Five retired openers live
  as a test fixture (`tests/fixtures/`), from which `run.py` builds `gas/Archetype_ch10_cc_test.gs` so every kind stays tested.
- **Equilibrium (`ch13_ice`)** is step-3 scaffolding: V2's six problems as fixed variants, the table kind, branching. The instructor
  will replace most of it. It is next.
- **The instructor was mid-way through the first full run of the four scenarios** (`docs/TEST_PLAN_ch10_cc_four_scenarios.md`)
  when this handover was written. See "Open issues" for what the run had found.

## The lanes

Fable/ARCHITECT_CLAUDE (this chat), Opus (constructor; unused so far), SCENARIO_CLAUDE (`docs/06_SCENARIO_CLAUDE_role.md`:
drafts scenarios, step maps, moves, sources), Simulation_Claude (`docs/04_SIMULATION_CLAUDE_role.md`: builds simulation
pages), the analysis side (measures, never modifies). The other chats cannot see this chat or the repository; every file moves
through the instructor. Their hand-offs arrive here as zips.

## The routines (do not change them without telling the instructor)

- **Every report ends with two zips**: `<name>_copy_into_repository.zip` (the repository minus `.git`, `REPOSITORY.md` and
  `media/`) and `project_knowledge_<date>.zip` (`scripts/make_project_knowledge.sh`). The instructor drops the first into his
  repository with Finder (`docs/UPDATING_THE_REPOSITORY.md`), commits and pushes with GitHub Desktop; CI runs on the push.
- **`media/` is the instructor's and Simulation_Claude's.** Zips never contain it. Media that arrives inside a SCENARIO_CLAUDE zip
  is passed straight back to the instructor in the same report (it happened twice; once forgotten).
- **Apps Script**: each report names the `gas/*.gs` files to re-paste; then Deploy → Manage deployments → pencil → New version.
  The alive reply (`/exec` in a browser) shows `content_version` per archetype and `shell_expected` / `shell_actual` / `shell_ok`,
  a run-time fingerprint of the pasted modules against the repository's; `shell_ok` false means a stale paste.
- **Content baseline**: `content/BASELINE_authored.txt` is guarded on every push (`make content-check`). An instructor-directed
  change is applied by replacing exactly the affected lines by hand and recording it in `BUILD_LOG.md`; never regenerate it.
- **Chemistry numbers** come from the instructor with a source (NIST unless he says otherwise) into `archetypes/data/substances.json`
  (the universal table; each field sourced); archetypes keep only teaching parameters (`LIQUIDS` in `ch10_cc.py`).
- **Every scenario is walked in a headless browser** (Playwright is installed; `walk_*.py` scripts in the working folder were
  throwaways; write a new one) and its screenshots go to the instructor. He runs it himself afterwards in Google mode.
- `make test` runs everything (generator suites, verifier suites per scenario, module tests, replay, regression, generated-file
  check, content check, purity); `make generate` rebuilds the bundles, the test fixture, `Units.gs` and `Shell_version.gs`.

## The content files (per archetype, all the instructor's or approved)

`content_<a>_openers.csv` (15 columns: scenario, keywords, fits, kinds, pictures, alt text, simulation and when it opens, credit,
label words, optional items), `content_<a>_moves.csv` (one row per item; `item@K1;K2` rows for kinds; an `opener` column for
scenario overrides), `content_<a>_errors.csv` (named-error wording, with overrides), `content_<a>_limits.csv` (generator limits per
scenario and liquid: known point, ranges, offsets, depth), `content_<a>_sentences.csv` (problem-sentence templates). The step maps as
the tutor runs them are regenerated into `docs/STEP_MAP_*.csv`; the rules into `docs/STEP_MAP_rules_everywhere.csv`.

## Open issues, most important first

1. **Pictures and videos do not show on the instructor's machine in Google mode** (reported 11 Oct, last thing). The server sends
   the media path (his debug output shows it); the same page and content show the picture in headless Chromium here. The page
   now prints "The picture did not load. The page looked for it at: <absolute path>" when a load fails (last commit). Likely causes:
   the page opened from a download folder rather than the repository (no `media/` beside it), or Safari's local-file restriction
   (Develop → Disable Local File Restrictions). Get that red line from him first.
2. **The model's judging of accounts.** On 10 Oct it refused two true accounts while holding out for the fuller mechanism. The
   prompt now says truth, not completeness, is the test (`gas/prompt.gs`). A prompt change cannot be proven by the suite; his next
   transcript is the test. If it still fails, the structural option is: gates plus second reader decide, the model only speaks.
3. **The model improvising a question at a choice item.** Fixed in Phase B on 10 Oct (`Core.say`: when the next item is a pick or a
   prediction, the authored question is asked, the model's own replaced; with nothing to judge the model is not called). His 11 Oct
   transcript still showed an improvised question with a matching shell fingerprint, which contradicts the fix; confirm with a fresh
   transcript where an account is accepted and the Equations list is next.
4. **Project knowledge** uploads: the instructor could not find the upload control. The fallback (attach the kit files to each new
   chat) works and the other chats use it.
5. **"Spinning away in GitHub"** (his last message): probably the Actions run or a slow push of the 13 MB vent video. Check the
   Actions tab with him; the last commits changed only the page and the fingerprint.
6. Step 6c/6d; the worked → faded → independent sequence (`docs/06_SCENARIO_CLAUDE_role.md`, bottom); the
   `direction` kind's return with a better battery of questions (instructor); the equilibrium archetype.

## What to do first

Answer the instructor in his two-section format. Ask for the red "did not load" line. Then continue his run-through plan.

Current build codes: content `8c9971e226` (ch10_cc), shell `81663305` (expected). Reports name the files to paste; the full
Apps Script set is listed in `INSTALL_CHEAT_SHEET.md`.
