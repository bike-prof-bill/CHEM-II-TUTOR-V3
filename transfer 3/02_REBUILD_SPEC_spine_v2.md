# Rebuild spec: the verifier spine, version 2

**8 October 2026.** Decided by the instructor after the 7 October critique. Read `00_HANDOFF_READ_FIRST.md` first. This document supersedes nothing in it; it adds the next job.

**The job in one sentence:** rebuild the verifier (`Core.gs`) and the generator's output contract around three structural changes, prove it with two archetypes that share no code, and leave every test green. Pedagogy, decisions, and all authored text are unchanged.

**Why now:** three latent faults (bare small integers ignored as answers; the fortuitous-answer filter guarding only the final key; the wrong-try ladder counting per item when per stage was decided) plus a monolithic `Core.gs` would be cheap to fix with one archetype and expensive after 28 more are stacked on it.

---

## Change 1: the step map becomes a real schema

Today an item is `{state, kind, register, requires, rule}`. Replace with:

```
{
  "id": "rearranged",
  "stage": "setup",                  // every item belongs to a stage; the ladder counts per stage
  "kind": "equation",                // text | pick | equation | number | direction | table | reflection
  "register": "symbolic",            // macro | submicro | symbolic | inference
  "face": "check",                   // choice | check | why   (all three logged; this is the dominant one)
  "requires": ["relation_chosen"],   // dependency rule, unchanged in meaning
  "branch": null,                    // on a pick item: {"eq_a": ["rearranged"], "eq_b": ["rearranged_dH","rearranged_T"]}
                                     // items named here exist only when that option is picked
  "label_when_done": "Rearranged for the unknown",   // shown ONLY after the item is ticked; never before
  "pin": true,                       // the accepted value or equation stays on screen
  "explicit": true,                  // never implied by a later correct number
  "credit_gate": false
}
```

Rules:
- **Ladder per stage.** `tries`, `bailed`, `park` are keyed by `stage`. The moves file gains a `stage` column; `switch_ask`, `notebook_prompt`, `return_ask`, `park_text` may be given per stage with optional per-item override. The log still records which item failed.
- **Branching.** When a `pick` item with `branch` is ticked, the items it names become live; items under other options are never shown, never counted, never required. `activeState` and progress ("3 of 8") count only live items.
- **New input kinds.** `direction` (a pick from rises / falls / unchanged, or larger / smaller, checked deterministically; used for predict-observe-explain before the simulation). `table` (an ICE-style grid: each cell is a number or a symbolic expression checked by the equation engine). `reflection` (free text, never graded for correctness, required to be a sentence; the metacognitive close: which step was hardest and one sentence why).
- **Progress display.** The page shows `label_when_done` for ticked items and a count for the rest. Labels ahead are hints and stay hidden.
- **Pins.** Any item with `pin: true` keeps its accepted content on screen: the relation, the rearranged equation, the kelvin temperature, the converted pressure.

## Change 2: the generator declares every number; the verifier guesses nothing

The generator emits, per variant, one table of everything that may legitimately appear and one table of every wrong turn:

```
"expected": [
  {"id": "T1_K", "state": "T_in_K", "role": "intermediate", "label": "T1 in K",
   "value": 357.05, "unit": "K", "dim": {"K": 1}, "abs_tol": 0.2,
   "also": [{"value": 83.9, "unit": "degC", "abs_tol": 0.2}]},
  {"id": "key", "state": "value_found", "role": "key", "require_unit": true, ...},
  {"id": "g_P1", "state": null, "role": "given", "value": 107.5, "unit": "kPa", ...},
  {"id": "R",   "state": null, "role": "constant", "value": 8.314, ...}
],
"traps": [
  {"id": "CELSIUS_NOT_CONVERTED", "state": "value_found", "value": 80.39, "unit": "K", "abs_tol": 1.0}
]
```

Rules:
- The verifier matches a typed number against `expected` and `traps` **only**. No heuristics: no "small integers are constants," no stray-number closure. A number matching nothing is `stray`, full stop. (This is what fixes van't Hoff `i = 2` and reaction order `2`: they are declared.)
- **Generator validation, run on every variant before it ships:** no two `expected` entries with different `state` lie within the larger of their tolerances of each other (after unit conversion); no trap lies within three tolerances of any `expected` entry of the same state; no given, after unit conversion, lies within three tolerances of the key. A variant that fails is thrown away and counted. This generalizes the fortuitous filter from "key only" to every number.
- **Units as data.** Port V2's dimension-vector engine: every `expected` entry carries `dim`; the engine converts and checks cancellation. The units table moves out of code into a data file so a second discipline adds units without touching the shell.
- The verifier's matcher is one pure function: `(parsedNumber, expected, traps, ticked) → {type, id}`. Testable on its own.

## Change 3: every turn runs in two phases

- **Phase A, `verdict`.** Deterministic only: parse, match, tick, branch, ladder, pins, notebook card or park, progress. Returns in about a second. No model call ever.
- **Phase B, `say`.** The model's draft, with the second reader (which needs only the student's message) run **in parallel** (`UrlFetchApp.fetchAll` on Apps Script; `Promise.all` on Netlify), then guards, one rewrite, then the authored fallback.
- The page sends A, renders its result at once ("T1 in kelvin, checked"; the pin; the meter), then sends B and renders the sentence when it arrives. Notebook-card and park turns skip B entirely.
- One log row per turn carrying both phases' timings. Replay of past logged turns must still work (A is a pure function of the message and the session; it is the thing replay tests).
- The code split falls out of this: `parse`, `match`, `stepmap`, `ladder`, `guards`, `prompt`, `log`, each a file with its own tests; `Core` becomes the thin thing that orders them. `test_core.js` stays as the integration suite.

## Three cheap checks that move out of the prompt

Deterministic, on the model's draft, before guards: exactly one question mark; no opener from a banned-phrase list (your V2 list: "Spot on", "Exactly right", "Perfect", "Great job", "You nailed it", "Excellent work"); not the same first three words as the previous reply. Fail → rewrite once → authored fallback. Delete the corresponding prompt rules.

## The test: two archetypes, no shared code

1. **Clausius-Clapeyron**, from the existing generator, re-emitted in the new contract. Its content (openers, moves rows, liquids, traps) is unchanged.
2. **ICE, from V2's six problems as fixed variants.** Port `SOLVERS.ice` from `Code_V2-6.txt` to `archetypes/ch13_ice.py`; emit the six problems from V2's `problemPools["ch13_ice"]` with declared numbers; use V2's `OPENERS["ch13_ice"]` and `OPENER_KEYWORDS["ch13_ice"]`; turn `WORKFLOWS["ch13_ice"]` into DRAFT moves rows. Step map uses `branch` (find-K versus solve-for-x; perfect square versus quadratic; the `ask` species) and `table` (the change row). Traps from `STUDENT_TRAPS.txt`: `COEFFICIENT_NOT_SQUARED` (x computed with 2x² in place of (2x)²), `EXCEEDS_INITIAL` (x larger than the starting amount; the direction check), `INITIAL_IN_K` (K from initial concentrations), `ORDER_OF_OPERATIONS` (unbracketed denominator; an equation-form trap). The final answer is a small number with units: this is the regression test for the integer bug.
3. **Nothing in the shell may name chemistry.** `grep` the shell for "ice", "clausius", "kelvin", "atm": zero hits outside the data files. A reviewer should be able to delete both chemistry files and the shell still loads.

## Definition of done

- All existing tests pass unchanged in meaning: 600/600 generator, every scripted-student check, every variant of both archetypes completable.
- New per-module tests, plus three regression tests named for the faults they catch: integer answer accepted; intermediate-versus-trap collision rejected by the generator; two fails on different items of one stage trigger one notebook card.
- A **random-clicker** persona: picks at random, types filler; in 200 runs per archetype it never reaches a credit gate.
- The **build report** prints, per archetype and overall: opinion-only share (three ways: by step, by credit gate, by exposure), generation share, gate mix by face, and every G3 item with its justification.
- Phase A under 1.5 s on the local server for every variant.
- A repository with both suites run on every push. No work on the spine begins before the repository exists.

## Order

1. Repository and continuous tests (one day).
2. Change 2 (declared numbers, units as data). Clausius re-emitted. Tests green.
3. Change 1 (schema, stages, branching, new kinds). ICE stand-in built as its test. Tests green.
4. Change 3 (two phases, module split, prompt rules to checks). Tests green; latency measured.
5. Content verified unchanged: a diff of every authored string before and after is empty.

## Do not

- Change any authored text, any decision in the handoff's table, or any grading window.
- Port V2's rule prose into the prompt. Rules become checks or are dropped.
- Build a real ICE generator yet; the six fixed problems are the point.
- Touch `index.html` beyond what Phase A/B rendering, labels-when-done, and pins require.
- Start the Netlify move or the durable store; that is December.
