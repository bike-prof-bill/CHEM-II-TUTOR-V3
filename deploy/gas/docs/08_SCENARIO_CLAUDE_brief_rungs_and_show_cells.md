# Brief for SCENARIO_CLAUDE: rungs, scenario roles and the `show` cells (v2, 13 Oct 2026; no longer a draft, on the instructor's word)

From Fable, on the instructor's decisions of 11–13 Oct. Read `docs/06_SCENARIO_CLAUDE_role.md` first; this adds to it. Everything
you draft is DRAFT until the instructor approves it. The rungs, roles, show cells and offer described here are built and running
(BUILD_LOG, 13 Oct); chapter 10 and the first two equilibrium scenarios already follow this brief.

## What changed

Students are stepped through each archetype on three rungs: **Worked** (the tutor shows each step and the student confirms,
predicts or computes; no notebook), **Faded** (authored questions, two tries, a switch question, the notebook), **Independent**
(no help; the only rung whose completions are credit-eligible). A helped student runs Worked → Faded → Independent → Independent;
a capable one Faded → Independent → Independent. The instructor assigns the starting rung (a `Rungs` sheet, or `DEFAULT_RUNG` for
everyone); one clean completion advances; two wrong tries on one stage at Independent demote to Faded for the next problem.

Scenarios take **roles** within an archetype. Each archetype has at least four: one `worked` (the Worked rung draws only it), one
`exam` (served to every student once, unannounced, as an Independent problem; the same problem then sits on the in-class exam,
where the credit is decided: a tutor pass without an exam pass earns nothing), and two or more `floater` (Faded and the other
Independent problems). The `role` column of the openers file (blank = floater). The instructor assigns the roles.

## What you draft

1. **`show` cells for the worked scenario of each archetype.** For every item of the step map, the text the tutor shows BEFORE
   asking the student to confirm it, predict the next, or type the number it implies. Everything checkable stays checked:
   the show text reveals the step, the student still produces the answer. Shape, per item:
   - the account item: the tutor gives the particle account in two short sentences and asks the student to say it back in their
     own words (still gated on a mechanism word);
   - picks (equation, direction): the tutor says which and why, then asks the student to pick it;
   - the rearrangement: the tutor shows it and asks the student to type it;
   - numbers: the tutor shows the setup with units and asks for the value;
   - the meaning and the reflection: unchanged.
   One row per item, in the moves file's `show` column, as a scenario override row (the `opener` column filled). On the Worked
   rung the show cell is the whole prompt, so it ends with the action ("Type it with M."). A `version` cell on the row
   (`one`/`two`, `equal`/`unequal`, blank = every version) ties it to one version of the worked problem. Mathematics is written
   \( … \); no caret notation; "ln" only inside an equation.
2. **Keyword candidates** from the chapter's own vocabulary, per scenario, for the instructor to approve into the `keywords`
   column (the chapters are in `reference/openstax/`, CC BY 4.0; paraphrase, do not quote into student-facing cells without the
   attribution line). A keyword shorter than four letters matches only as a whole word.
3. **For a fixed-text archetype** (equilibrium): the problems themselves, six per scenario, in the problems sheet (`docs/handoff_examples/ch13_problems.csv`
   is the model): sentence, every constant with its source, the expected value of every item, the trap values. For a generated
   archetype (Clausius-Clapeyron) the generator makes the numbers within the limits file; you do not write them.
4. **Named errors** in the archetype's errors file (id, note, ask, opener, status), each with its detectable form: a value, a wrong
   table row, or a wrong expression shape.

## Sensors (instructor, 13 Oct)

The V2 scenarios' instrument in every scene (a gauge, a probe, a vapor monitor) is the bridge from the macroscopic to the
submicroscopic and stays part of the brief: a new scenario carries a reading a student could have seen on an instrument,
and the particle account explains the reading. The V2 scenarios themselves are kept as they are.

## The offer after the reflection (instructor, 12 Oct)

A worked problem may end with an offer of a second worked problem on the same scenario that changes one thing (one point to
two for the alcohol; equal starts to unequal for the Martian fuel). It is one row in the moves file, state `offer`, per scenario,
its text in `ask` or `show`, with a `version` cell saying which version the offer belongs to; that version is the one the Worked
rung starts on, and the shell serves the other version with its own show cells. The offered problem is extra: logged, counted
toward none of the required problems (instructor, 13 Oct).

## What you do not do

Write problem numbers for a generated archetype (the generator makes them); edit code, generated files or tests; change an
approved cell. If something needs the shell to change, say so and stop; Fable builds it.
