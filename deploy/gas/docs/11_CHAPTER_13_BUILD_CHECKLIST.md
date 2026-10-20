# Chapter 13 (equilibrium): what is built and tested, 13 Oct 2026

**Superseded the same evening: the two scenarios landed (see BUILD_LOG, 13 Oct night). Everything in the "not built" table below except Q versus K, a generator and simulations' sim parameters is now built; the Haber and Martian scenarios, twelve fixed problems, ten named errors, roles, show cells and the offer are in.**

For SCENARIO_CLAUDE, companion to `docs/10_CHAPTER_10_BUILD_CHECKLIST.md`. Chapter 13 is step-3 scaffolding: the shell's new
kinds were proved on it (8 Oct) and nothing in it has been approved for a student. Content `4f3865b37b`, shell `bb174cdf`.

## ICE tables (`ch13_ice`): built and tested

| Item | Built | Where | Test |
|---|---|---|---|
| Step map with a branch (find K vs solve for x; perfect square vs quadratic) | yes, 8 Oct | `approach` pick with `branch`; items under the other option never shown or counted | `test_ice.js` (38 checks) |
| The change row as a table (each cell a number or a symbolic expression) | yes, 8 Oct | `table` kind, cells checked by the equation engine | `test_ice.js` |
| Nine fixed problems (V2's six, three kinds: findK, perfectSquare, quadratic) with every number declared | yes | `archetypes/ch13_ice.py` `FIXED`; `expected`/`traps` validated on every build | generator 9/9; `test_ice.js` "9 fixed problems completed" |
| Named errors: `INITIAL_IN_K`, `EXCEEDS_INITIAL`, `ORDER_OF_OPERATIONS`, `COEFFICIENT_NOT_SQUARED`, `SMALL_X_APPROXIMATION` | yes | trap values per problem; `ORDER_OF_OPERATIONS` also as an equation-form trap | `test_ice.js` |
| The integer-answer regression (a small number with units as the final answer) | yes | `tests/regression/integer_answer_accepted.test.js` | 12 checks |
| Rungs, roles, near miss, repeat, units reader, authored questions everywhere | yes, shell-level, nothing to add per archetype | `Core.gs` etc. | `test_core.js` |

## Not built, or placeholder, and whose it is

| Item | State | Whose |
|---|---|---|
| Openers | V2's six, titled "V2 opener 1–6", all role `floater`, no media, no keywords beyond V2's lists, never approved | instructor and SCENARIO_CLAUDE: the two scenarios in hand (Martian fuel factory, Haber-Bosch harvest) replace them |
| Moves rows | 10 rows, all DRAFT, V2's workflow text; no scenario overrides, no `show` cells, no offer | SCENARIO_CLAUDE drafts, instructor approves |
| Scenario roles | none assigned (all floaters) | instructor (recommendation on record: Martian worked, Haber-Bosch exam until the second pair exists) |
| Keywords and label words | V2's lists only; none checked against the equilibrium chapter | SCENARIO_CLAUDE from the chapter, instructor approves |
| Simulations and media rows | none; `simulation` cells empty; no `MEDIA_SOURCES` rows | Simulation_Claude via SCENARIO_CLAUDE |
| Problem sentences and limits files | none (`content_ch13_ice_sentences.csv`, `_limits.csv` do not exist); the nine problems are fixed text | Fable, once the instructor says whether equilibrium problems are generated or stay fixed |
| A real generator (random K, starting amounts, species) | not built; the spec said "do not build a real ICE generator yet" | Fable, on the instructor's word, with constants sourced into `substances.json` or a reactions table |
| `direction` kind on this archetype | removed on the instructor's instruction (10 Oct); the kind lives in the shell | instructor, if it returns with a better question set |
| Equation checks (`eq_checks`) for the K expression | none; `relation_chosen` is a pick, the table and `expression_set` carry the symbolic checks | Fable, if a typed K expression is wanted as a check |

## Q versus K (`ch13_q_vs_k`)

Not in V3. V2's six openers, keyword cells, milestones and problems are inventoried in `docs/09_CH13_SCENARIOS_AS_THEY_STAND.md`.
The instructor (12 Oct) keeps it a separate archetype. Its map, when built: account → the Q expression (pick) → Q computed (number) →
direction predicted (the `direction` kind, checked against Q and K) → meaning → reflection. Nothing of it is built or tested.
