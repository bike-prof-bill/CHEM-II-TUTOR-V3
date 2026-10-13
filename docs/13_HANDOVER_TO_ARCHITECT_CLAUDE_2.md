# Handover from Fable (second ARCHITECT_CLAUDE, 11–13 Oct 2026) to the third

Read this, then `BUILD_LOG.md` from "11 Oct 2026 (evening)" onward (every decision and change since the first handover, dated),
then `docs/07_HANDOVER_TO_ARCHITECT_CLAUDE.md` for the earlier history and `docs/02_REBUILD_SPEC_spine_v2.md` for the spine.
The standing rules in the project instructions apply unchanged: no praise, plain speech, two sections in every deliverable
(**Needs your decision** first, then **Engineering**), DRAFT never reaches a student unapproved, do not change the teaching without asking.

## First thing to do

You cannot work from the project-knowledge kit alone: it leaves out `index.html`, the tests, the Makefile, the CI workflow and
the generated bundles by design. Ask the instructor for the repository: in Finder, inside `CHEM-II-TUTOR-V3`, select all, deselect
`media` and `reference`, Compress. The zip includes `.git`, which is the source of truth when files and log disagree (it was on
11 Oct). Unzip with `unzip -o` (duplicate entries). Then `make test` before anything else; it should be entirely green.

## Where things stand (13 Oct, night)

- **Shell** `6671cbe2`, `CODE_VERSION 01e56c5c`. The alive reply (`/exec`) shows `shell_ok` and each archetype's `content_version`.
- **Clausius-Clapeyron (`ch10_cc`)**, content `3c7a971cb6`: four scenarios approved (Rubbing Alcohol Chill = worked, with versions
  one/two and the offer; Drinking Bird = exam; Syringe and Deep-Sea Vent = floaters); 27 generated problems; keywords from the
  chapter; four simulation pages checked and registered. Next: a fifth scenario (ΔHvap and temperature kinds each have one).
- **Equilibrium, ICE (`ch13_ice`)**, content `972b9cf0cc`: two scenarios approved (Martian Fuel Factory = worked, versions
  equal/unequal and the offer; Haber-Bosch Harvest = exam), twelve fixed problems, ten named errors, two simulations registered.
  No DRAFT row. Next: two floater scenarios (SCENARIO_CLAUDE, six fixed problems each).
- **Q versus K (`ch13_q_vs_k`)**: not in V3; V2's inventory in `docs/09_…`; its map is sketched in `docs/11_…`. Separate archetype.
- **Rungs** (Worked → Faded → Independent) are built: `Rungs` sheet + `DEFAULT_RUNG` script property; roles enforced; the offer;
  credit-eligible only at Independent; the exam scenario served once, unannounced, at Independent (credit decided in the exam room).
- The instructor has not yet installed the last zip (`chapter13_copy_into_repository.zip`, 13 Oct night) nor pasted since
  `a26b3186`. Until he does, the running tutor is behind the repository; check the alive reply before reading any transcript.
- Chats: SCENARIO_CLAUDE (new, holds the kit and `docs/12_…`; now the go-between with Simulation_Claude), Simulation_Claude
  (new), the analysis side (tell it the Log sheet's `queued`/`queue_ms` were displaced before 13 Oct, see BUILD_LOG).

## Decisions taken 11–13 Oct (all the instructor's; details and dates in the log)

Accounts: gates plus one reader; a false statement found by the second reader is refused (`SECOND_READER_VETO = true`). Authored
questions everywhere; the model acknowledges, answers pleas, and asks only where its question is the tutoring (a refused free-text
attempt, a trap, a switch). Subscripts 1/2 are relative (consistent relabel accepted). Either side of an equation. Near miss
(10 %) asks "Which values did you use to get that number?"; a repeated wrong number costs nothing. Units are read in a typed
setup and cancelled algebraically; three units sentences approved; mixed units inside a ratio are wrong. "ln" only inside an
equation; math as \( \); no caret in tutor text. Sensors stay in every scene. Scenario roles; the offer is extra. Equilibrium
problems are fixed text. Tone: warmer acknowledgements wanted, without flattery (not yet drafted; see open items).

## Routines (unchanged; do not change without telling him)

Every report ends with two zips: `<name>_copy_into_repository.zip` (repository minus `.git`, `REPOSITORY.md`, `media/`) and
`project_knowledge_<date>.zip` (`scripts/make_project_knowledge.sh`). He drops the first with Finder onto the repository window
(title bar must say `CHEM-II-TUTOR-V3`; a drop onto `gas/` cost a whole day on 11 Oct), Replace, Apply to all; commits and pushes
with GitHub Desktop; CI runs. Each report names the `gas/*.gs` files to paste; **a content or archetype change means
`Archetype_<a>` too**; `Shell_version` when `Core` or `Code` changed; **Cmd+S after each paste**, then Deploy → New version;
`refreshHeaders` once when a sheet column is added. The shell fingerprint hashes one function per module, so `shell_ok` true does
not prove every module is current: paste on the report's word. `media/` never passes through you. Content baseline: replace
affected lines by hand, never regenerate. Chemistry numbers: `substances.json`, `reactions.json`, each with a source.
Walk every new scenario here (Node harness or Playwright) before he installs it; the step-by-step install instructions have to be
literal (which window, which button); he is not a developer and says so.

## Open items, most important first

1. His run of the four chapter 10 scenarios with the final language, and of the two equilibrium scenarios, has not happened on
   the current build. Read the transcripts and the Log sheet columns (`units_check`, `near_miss`, `second_reader_quote`, `rung`).
2. Tone: draft a small set of plain acknowledgements (approved by him) for "Checked:" lines and the first sentence after a wrong
   try; keep the banned-opener list; never on a wrong answer. Content, not code (`check_phrases` idea in the log, 12 Oct).
3. Step 6c (distress check: his wording and resources; "I give up" is only a plea today) and 6d (compliance list). `docs/03_…DRAFT`.
4. Ladder wording after the fairness discussion (8 Oct); the `direction` kind's question set; a `make media-check` that hashes
   `media/` against the register's SHA-256s (Phase II safeguarding line).
5. Tools Competition: Phase I submitted 13 Oct (V2 Claude's document, abstract and Learning Engineering revised for V3 in the
   chat record); Phase II invitations 24 Nov; budget shape waits on individual-vs-institution (grants office).
6. The Netlify move and durable store: December, per the spec.
7. Known limits: `BUILD_STAMP` is a hand-set constant (retire for `CODE_VERSION`); the generated job in CI has `setup-node`
   added but the `shell version` line depends on Node; `test_core.js` is at 122 checks and slow to read.

## What the content files look like now

Openers: 15 columns + `role`. Moves: 12 columns (`show`, `version` added; `offer` is a state). Errors: id, note, ask, opener,
status. Problems sheet (fixed archetypes): `docs/handoff_examples/ch13_problems.csv`. Limits and sentences (generated archetypes)
with `version` on sentences. The brief `docs/08_…` and the role `docs/06_…` describe them for SCENARIO_CLAUDE; the two chapter
checklists `docs/10_…`, `docs/11_…` say what is built and which test covers it.
