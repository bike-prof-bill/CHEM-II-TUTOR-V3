# For the new SCENARIO_CLAUDE: where things stand (from Fable, 13 Oct 2026)

Read first `00_READ_ME_FIRST_project_knowledge.md`, then your role (`docs/06_SCENARIO_CLAUDE_role.md`), then the brief on rungs
and show cells (`docs/08_…`), then this. The two chapter checklists (`docs/10_…`, `docs/11_…`) say what is built and tested. The
retiring SCENARIO_CLAUDE's own hand-over, if the instructor asked it for one, says what it was holding; ask him for it.

## The standing rules you inherit (all the instructor's; dates in BUILD_LOG.md)

- The instructor approves every cell before it reaches a student; DRAFT is the mark for anything not yet approved.
- A scenario is a scene a student has seen or felt, in short plain sentences, with an **instrument reading** in it (the sensor is
  the bridge from the macroscopic to the submicroscopic, 13 Oct). The problem is hidden until the particle account is given.
- Every archetype has at least four scenarios: one with role **worked**, one **exam** (served to everyone once at the Independent
  rung, unannounced; the same problem then sits on the in-class exam), the rest **floaters**. Roles are a column in the openers file.
- The worked scenario carries `show` cells (the tutor shows the step, the student still produces it), optionally in **versions**
  (`version` column: `one`/`two` for chapter 10, `equal`/`unequal` for chapter 13; blank = every version), and an `offer` row whose
  text is shown after the reflection and whose version tells the shell which version the worked rung starts on.
- Keywords: the chapter's own words (OpenStax, `reference/openstax/`); a keyword shorter than four letters (IMF) matches only as a
  whole word; label words (naming the phenomenon without mechanism) go in their own column.
- "ln" appears only inside an equation or expression; prose says "natural logarithm". No caret notation in tutor text; math is
  written \( … \) and the page renders it.
- Chemistry numbers come with a source (NIST or the textbook) and go to a data table (`substances.json`, `reactions.json`), never
  into prose alone. Equilibrium problems are fixed text; Clausius-Clapeyron problems are generated within the limits file.
- Named errors live in the archetype's errors file (id, note, ask, opener, status); the shell detects them from the values, table
  rows or expression forms Fable declares. A new error needs its detectable form stated (a value, a wrong table row, a wrong
  expression shape) or it cannot be built.
- Media never passes through Fable: pages and pictures go to the instructor's `media/`; their rows go into `docs/MEDIA_SOURCES.csv`
  (via Fable) with the SHA-256 and the approval date.

## File shapes (the chapter 13 zip is the model of a complete hand-off)

- Openers: 15 columns + `role`. Moves: state, stage, label_when_done, ask, switch_ask, notebook_prompt, return_ask, park_text,
  status, opener, show, version. Errors: error id, note, ask, opener, status. Problems (fixed archetypes): id, opener, family,
  sentence, constants and sources, expected item by item, trap values, status. Media rows: the register's 13 columns.
- One zip per round, every item approved, a README listing what is in it; partial zips are fine if the README says what is missing.

## What is in hand and what is next

| Archetype | Scenarios | Roles | Next |
|---|---|---|---|
| ch10_cc Clausius-Clapeyron | Rubbing Alcohol Chill, Syringe Boiling Trick, Drinking Bird, Deep-Sea Vent (all approved, keywords from the chapter) | Alcohol worked (versions one/two, offer), Bird exam, Syringe and Vent floaters | a fifth scenario: the ΔHvap and temperature kinds each have one scenario, so the exam's practice coverage is thin there |
| ch13_ice ICE tables | Haber-Bosch Harvest (H1–H6), Martian Fuel Factory (M1–M6), all approved | Martian worked (equal/unequal, offer), Haber exam | two more scenarios (floaters), fixed problems six each, with the instrument reading in the scene |
| ch13_q_vs_k Q versus K | none in V3 (V2's six are inventoried in `docs/09_…`, kept as sensor scenes) | — | four scenarios; its map is account → Q expression (pick) → Q (number) → shift predicted (direction) → meaning → reflection; separate from ICE on the instructor's word |
| chapter 11 | the instructor's plan: four archetypes, four scenarios each | — | after equilibrium |

Open with the instructor, not yours: the distress-check wording, the compliance list, the ladder wording, the tone of the
acknowledgements (he wants it warmer without flattery; Fable will draft a phrase set for his approval).
