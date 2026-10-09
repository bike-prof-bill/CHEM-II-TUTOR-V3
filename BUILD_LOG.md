# Build log: the verifier spine rebuild (docs/02_REBUILD_SPEC_spine_v2.md)

One entry per step. Numbers are from the run that shipped the step. Nothing here is a decision; decisions are the instructor's and live in the handoff.

## Step 1 (8 Oct 2026): repository and continuous tests

- Build folder is the repository root; documents under `docs/`; V2 under `reference/v2/`.
- CI: generator 600/600, verifier 47/47, generated files reproducible, authored content 212 strings baselined, shell purity 9 hits (advisory).

## Step 2 (8 Oct 2026): the generator declares every number; the verifier guesses nothing

**What changed**

- `units.json` is the only place a unit is named: dimension vectors, conversion factor and offset, and the aliases a student may type. `engine.py` reads it; `run.py` writes `gas/Units.gs` from it for the verifier. The hard-coded unit tables in `engine.py` and `Core.gs` are gone.
- Every variant now carries `expected`: one table of every number that may legitimately appear, each with `id`, `role` (intermediate / key / given / constant), `state`, `value`, `unit`, `dim`, `abs_tol`, alternative forms (`also`), and `require_unit`. `traps` carry `state`. The old `targets` field is gone. 14 to 24 declared numbers per variant.
- `Core.gs` has one pure matcher, `CORE.match(parsedNumber, expected, traps, ticked) → {type, …}`, exported and tested on its own. Types: `expected`, `needs_unit`, `wrong_dimension`, `trap`, `given`, `constant`, `stray`. Removed: the constant list, "small integers are constants", the stray-number closure, the hard-coded unit regex, the chemistry words in the prose-detector's stop list (now derived from `units.json` and the archetype's own symbol aliases).
- Matching never converts units silently. A typed unit must equal the declared form's unit; a bare number matches by value but cannot tick an entry that requires its unit. Converting a given is the student's step, so "39.9 kJ/mol" does not satisfy "ΔHvap in J/mol". A right value with a unit of another dimension ("357 atm" for a temperature) is `wrong_dimension`: refused, logged under guards as `WRONG_DIMENSION`, counted like a stray.
- Generator validation on every variant (`engine.validate`), replacing the key-only fortuitous filter: (1) no two declared entries of different state within the larger tolerance of each other; (2) no trap within three tolerances of any same-state entry (intermediates included, not just the key); (3) no given, after unit conversion, within three tolerances of the key. Rejections are counted by rule. Shipped bundle: 4 of 112 tries rejected, all by rule 1; rules 2 and 3 rejected nothing, as the old filter also rejected nothing.
- Constants the archetype declares for Clausius: R (8.314, 8.3145), 0.08206, 273.15, 273, 760, 101.325, 101.3, 1000, 1 (the 1 in 1/T), and, per the instructor (8 Oct), 0, 2 and 3 for integers written in prose. Not 100, and not 0.008314 (the latter is already an accepted alternative form of the ΔHvap-in-J step, per the shipped design).

**Two readings of rule 1, both switchable in `engine.py`**

Read literally, rule 1 rejected 20% of all variants and 48% of those with a normal-boiling-point given (the instructor's `ONE_ATM_POINT = 0.35`), because in those problems the pressure conversion equals a conversion factor (760, 101.325, 1) and the pressure ratio equals a given. Two policies, both defaulting to the reading that keeps those problems:

- `CONSTANT_COLLISIONS_REJECT = False`: an intermediate equal to a declared constant does not reject the variant. The matcher checks intermediates before constants, so the student who types 760 after converting 1 atm gets the conversion step credited, which is what happened. Keys are never exempt: a key within tolerance of a constant still rejects.
- `DROP_INTERMEDIATE_EQUAL_TO_GIVEN = True`: an intermediate equal to a number on the page (the ratio P2/P1 when P1 = 1 atm) is not evidence and is removed from that variant's declaration, recorded in `dropped`; the state must keep another route or the variant is rejected. 12 of the 108 shipped variants have one such removal.

Measured on 1,200 tries: literal reading 20% rejected; recommended reading 6%; normal-boiling-point share falls from 35% to about 31% instead of to about 18%.

**Tests**

- `test_ch10_cc.py`: 600/600; every shipped variant passes validation; every declared number carries `dim`. Field names updated, meaning unchanged.
- `gas/test_core.js`: 47/47, field names updated, meaning unchanged.
- New: `tests/regression/integer_answer_accepted.test.js` (10 checks), `tests/regression/collision_rejected_by_generator.py` (9), `tests/modules/units.test.js` (8), `tests/modules/test_units.py`.
- Authored content: 212/212 baseline strings present and unchanged.
- Shell purity: 9 → 2 (both in `index.html`, untouched by design until step 3).

**Behaviour change to watch in the logs**

A number in prose that matches nothing declared is now a stray, and a stray on a number item counts as a wrong try, exactly as before for strays. Undeclared small integers are strays rather than constants; 0, 1, 2 and 3 are declared for this archetype. The instructor's standing position (8 Oct): collisions of this kind are solved per archetype, by better problems and by declaring what is harmless there; the same question will arise for Raoult's law. The two validate() switches stay at their defaults. Declaring 2 exposed a precedence question at once: in one shipped problem the kJ-for-J slip produces T2 ≈ 1.9 K, whose ±1 K window covers 2, so "step 2" was read as that trap. Resolved in the matcher: a bare number equal to a declared constant is the constant, before traps; the same number typed with a unit cannot be a constant and still reaches the trap. Tested.

**Not done in this step**

- Dimensional checking inside typed equations (V2's `eqDim`): the equation checker still reads symbols only; a number with a unit inside an equation line is not parsed. Belongs with the `parse`/`match` split in step 4.
- `index.html` keeps its two chemistry references (subtitle, plot field names); step 3.

## Step 3 (8 Oct 2026): the step map becomes a schema; the second archetype

**What changed in the tutor shell**

- Every step-map item now carries the full schema: `id`, `stage`, `kind`, `register`, `face`, `requires`, `branch`, `label_when_done`, `pin`, `explicit`, `credit_gate` (`engine.stamp_board`, with the generator refusing an item that names an unknown requirement, branch target, or kind). `stage` and `label_when_done` come from the instructor's moves file, by item id; an item with no stage is its own stage, which is the pre-rebuild behaviour.
- **Ladder per stage.** `tries`, `bailed` and `park` are keyed by stage. Parking hands over every unmet item of the stage (its equation, its table, its right option, or its `park_text`). The log records both the item (`state`) and the `stage`. Regression test `one_stage_one_notebook_card`.
- **Branching.** A `pick` item with `branch` opens the items named under the picked option; items under other options are never live, never shown, never counted, never required. Progress counts live items only. Equilibrium problems use it: approach (find K / solve for x) and method (square root / quadratic / small x).
- **Three new input kinds.** `direction`: a deterministic pick (larger / smaller / unchanged), by button or by a typed word, before the inference. `table`: a grid typed as lines `I:`, `C:`, `E:` (or sent structured by the page); numeric cells compared directly, symbolic cells in x checked by substitution with the same engine that checks equations; a wrong row is named by row, never corrected. `reflection`: free text, never graded, required to be a sentence, never a wrong try, and the problem is not complete until it is written.
- **Pins and labels.** Any item with `pin: true` keeps its accepted content on screen (relation, rearranged equation, kelvin temperature, converted pressure, the table, the chosen option). The page shows `label_when_done` for ticked items only, under "Established"; labels ahead stay hidden. Picks with their own options are offered as buttons under the tutor's reply.
- **Moves file.** Gains `stage` and `label_when_done` columns (DRAFT values on the Clausius file; every existing cell unchanged, content check passes). A row keyed `stage:<name>` may give stage-level defaults for `switch_ask`, `notebook_prompt`, `return_ask`, `park_text`; item rows override.
- **The shell names no chemistry: 0 hits.** The mechanism-word list left `Core.gs` for the archetype files; the page's subtitle, archetype and kind menus are filled from the server; the simulation payload arrives in display units; `local_server.js` and `Code.gs` load every generated archetype file by name. Purity is a required CI job from this step.
- Equation checker: a numeric left side equal to a declared value is read as that symbol (`49 = (2x)²/(0.200 − x)²` is `K = …`), declared per check as `literal_for`. Traps may declare a bound (`above`) as well as a value; the conservation trap uses it.

**The second archetype: `archetypes/ch13_ice.py`, equilibrium concentrations by ICE table**

- V2's six problems as fixed variants (`FIXED`), text verbatim; V2's `SOLVERS.ice` rewritten as one `solve()`; V2's openers and keywords as `content_ch13_ice_openers.csv`; V2's `WORKFLOWS["ch13_ice"]` turned into eleven DRAFT moves rows. Traps from the instructor's `STUDENT_TRAPS.txt`: `ORDER_OF_OPERATIONS` (value, and as a bent equation set), `COEFFICIENT_NOT_SQUARED` (value for x and for the product, and as a bent set), `INITIAL_IN_K` (K = 0), `EXCEEDS_INITIAL` (a bound). V2's `SMALL_X_APPROXIMATION` is not carried: it is not in the instructor's list; the small-x option in the method pick covers the behaviour as a wrong choice.
- Keys re-derived independently in `test_ch13_ice.py` by bisection on the mass-action equation; all six agree with V2's closed forms. 9 variants (one per opener × fitting problem). No shared code with `ch10_cc.py`: deleting either chemistry file leaves the shell loading.
- Where the answer is x itself (a product with coefficient 1), x is not a separate item: one number cannot establish two items. Equilibrium concentrations equal to the key within three windows are not declared separately for the same reason.

**Tests:** generator 600/600 and 9/9; verifier 50/50 (three schema checks added) and the new `gas/test_ice.js` 40/40; regression 36/36 across four files; modules 8 + python; generated files reproducible; authored content 212/212 unchanged (additions listed); purity 0.

**Instructor, 8 Oct, on step 3:** the direction question is deleted from the equilibrium archetype (the kind stays in the shell, unused). Stages approved in principle; fairness and pacing, and the warnings and outlets required by federal and state rules, need a discussion before the ladder's wording is final. The brown-gas opener stays; the other equilibrium openers will be replaced. Each archetype will start with two scenarios the instructor fully vets. Build paused after step 3 at the instructor's request.

## Between steps (9 Oct 2026): the instructor's first motivating picture and simulation

- An opener may now carry media: a picture shown with the opening question, a second picture shown once the account is accepted, alt text for both, and a simulation page, with a setting for when the simulation opens (`account` or `meaning`). Five new columns on the openers file; the engine passes them through; the server sends the first picture with the question and the rest only after the account is earned; the page shows the picture above the veiled problem, swaps it on reveal, and opens the simulation in its own card. Files live under `media/<archetype>/`.
- First use: "The Rubbing Alcohol Chill" (Clausius-Clapeyron), with the instructor's two pictures and his 2-propanol simulator, opening at `account` as he asked for the trial.
- `docs/03_STEP_6_PROPOSAL_DRAFT.md` written for approval (log durability, no repeated problems, distress check, compliance list).
- Direction kind: the instructor expects to bring it back with a better set of questions; it stays in the shell.
- Instructor, 9 Oct: "The Rubbing Alcohol Chill" is the opener for finding the vaporization enthalpy of alcohols. Its fits column is now methanol; ethanol; 1-propanol; 2-propanol, its kinds dH; slope, and its simulation opens at `meaning` (after the deterministic items, before the metacognitive close). The baseline's one line for that fits cell was replaced by hand on his instruction; every other baseline line is untouched. Clausius pool: 96 variants.
