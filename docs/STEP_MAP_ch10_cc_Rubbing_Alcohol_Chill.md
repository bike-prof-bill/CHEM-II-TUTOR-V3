# The step map behind "The Rubbing Alcohol Chill" — what the tutor checks, and when (9 Oct 2026)

Read from the generated problems themselves (`output/ch10_cc.bundle.json`), not from memory. Two kinds of problem come from this
opener: **ΔHvap from two pressure–temperature points** ("dH") and **ΔHvap and the normal boiling point from a plotted data set**
("slope"). The step map differs between them; both are below. Words in `code` are the item ids in the moves file.

## How to read an item

- **Kind** says what can satisfy it: *text* (a sentence, judged by the model behind the server's gates), *pick* (a choice from the
  Equations list), *equation* (a typed line, checked by substituting numbers), *number* (a typed value matched against the problem's
  declared values). Words typed at a number item cost nothing and establish nothing.
- **Requires** says what must already be established before the item can be ticked. Correct later work implies the symbolic
  steps before it (a right ΔHvap ticks "values substituted"), except items marked **explicit**, which must be typed out: the
  rearrangement, always.
- **Rule** on a number item: *all* = every declared value for that item must be typed (both temperatures); *any* = one is enough.
- **Stage** is what the wrong-try ladder counts. Two wrong tries anywhere in a stage: notebook card. Two more after the return: the
  whole stage is parked (handed over), and the attempt can no longer earn credit.
- **Pin**: once ticked, the accepted content stays on screen under "Your symbols".
- **Credit gate**: the item that must be ticked (and the run clean) for the attempt to earn credit.

## Kind "dH": ΔHvap from two points (8 items, 5 stages)

| # | item | stage | kind | requires | what ticks it | wrong try when |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `account_given` | opening | text | — | A sentence of the student's own that engages the scenario and says what particles are doing; the model judges, a second reader checks for a false statement. | A sentence that the model rejects (not a question). |
| 2 | `relation_chosen` | setup | pick | 1 | The Clausius-Clapeyron relation picked from the Equations list. Pinned. The picked text is placed in the answer box. | Picking a look-alike. |
| 3 | `rearranged` | setup | equation, **explicit** | 2 | A typed equation with ΔHvap alone on the left that holds when the server substitutes values. Pinned. A true-but-not-isolated line is progress, not a wrong try. | A line that does not hold, or holds only for a sign-flipped or log-base-10 version (named: `EQ_SIGN_FLIPPED`, `EQ_LOG_BASE`). |
| 4 | `T_in_K` | units | number, rule *all* | 1 | Both temperatures typed in kelvin, with K. Arithmetic like `(273.15 + 47.5) K` is read. Pinned. | A number that matches nothing declared (a stray), while this is the active item. |
| 5 | `P_same_units` | units | number, rule *any* | 1 | Either pressure converted into the other's unit, typed with its unit. Pinned. | As above. |
| 6 | `substituted` | solve | number, rule *any* | 3, 4, 5 | Any one of: P2/P1, P1/P2, ln(P2/P1), 1/T2 − 1/T1 (with 1/K), ΔHvap/R (with K). | A stray while active. |
| 7 | `value_found` | solve | number, rule *all* | 6 | ΔHvap within the grading window, **unit required** (kJ/mol, or J/mol as the alternative form). A bare right number gets "what are the units?" and does not advance. | A stray; or one of four named errors: `CELSIUS_NOT_CONVERTED`, `KJ_WITH_R_IN_J`, `LOG10_FOR_LN`, `PRESSURE_UNITS_MIXED`, each with its own authored note. |
| 8 | `meaning_given` | meaning | text, **credit gate** | 7 | A sentence on what the number lets the student claim; model judges, second reader checks. The data plot and the simulation open when this item becomes active. | A sentence the model rejects. |

Order is not fixed: items 4 and 5 can be done before 2 and 3. The *active* item (the one the authored question is about, and the one a stray is charged to) is the first unmet item in the order above whose requirements are met.

## Kind "slope": ΔHvap and the normal boiling point from data (7 items, 4 stages)

| # | item | stage | kind | requires | what ticks it | wrong try when |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `account_given` | opening | text | — | as above | as above |
| 2 | `relation_chosen` | setup | pick | 1 | as above | as above |
| 3 | `rearranged_dH` | setup | equation, **explicit** | 2 | ΔHvap alone on the left in terms of the slope m and R. Pinned. | Does not hold, or sign flipped. |
| 4 | `dH_found` | solve | number, rule *all* | 3 | ΔHvap with unit (kJ/mol or J/mol). | Stray; or `SLOPE_SIGN_KEPT`, `KJ_WITH_R_IN_J`. |
| 5 | `rearranged_T` | setup | equation, **explicit** | 2 | T alone on the left in terms of m, b and ln P. Pinned. | Does not hold, or log base 10. |
| 6 | `bp_found` | solve | number, rule *all* | 5 | Normal boiling point with unit (°C, or K as the alternative form). | Stray; or `ONE_ATM_IN_TORR_LINE`, `KPA_IN_TORR_LINE`. |
| 7 | `meaning_given` | meaning | text, **credit gate** | 4, 6 | as above | as above |

Two rearrangements, two answers; the ladder's *setup* stage spans both rearrangements and *solve* spans both answers.

## Conditions that apply everywhere

- **Nothing is revealed until earned.** The problem text appears only after item 1; the plot and simulation only when the meaning item is active; a model reply that states a declared value the student has not typed is rewritten or replaced by the authored question.
- **A question costs nothing.** A message ending in "?" with no numbers is never a wrong try.
- **Words at a number item cost nothing** and get the authored question plus "This step is checked on the value: type it, with its unit."
- **The ladder, per stage:** try 1 → the model asks from another account (your `switch_ask`); try 2 → notebook card (your `notebook_prompt`), and the student must return with a sentence; two more → the stage is parked: its unmet items are handed over (the rearranged equation as `park_text`, the pinned values), the problem continues, the attempt earns no credit.
- **Completion:** when no live item remains. **Credit:** completion with a clean run (no park) and the meaning item ticked. After completion the tutor acknowledges and asks nothing.
- **What the problem never does:** name the liquid (it says "unidentified alcohol"), use kPa, show the answer, or let a bare number without a unit stand as the final answer.

## What is not in the map (and could be)

- A `reflection` item (free text, never graded, must be a sentence) after the meaning question. Exists in the shell; used by the equilibrium archetype; not in Clausius-Clapeyron. Adding it is one board line and one moves row.
- A `direction` item (a prediction: larger / smaller / unchanged) before the simulation. Exists in the shell; deleted from equilibrium at your request pending a better set of questions.
- Stage-level defaults for `switch_ask`, `notebook_prompt`, `return_ask`, `park_text`: a moves row keyed `stage:solve` etc. None written yet; every item has its own row.
