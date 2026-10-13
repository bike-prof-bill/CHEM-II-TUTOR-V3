# Brief for SCENARIO_CLAUDE: scenario roles and the `show` cells (DRAFT, 12 Oct 2026)

From Fable, on the instructor's decisions of 11–12 Oct. Read `docs/06_SCENARIO_CLAUDE_role_DRAFT.md` first; this adds to it.
Everything you draft is DRAFT until the instructor approves it.

## What changed

Students will be stepped through each archetype on three rungs: **Worked** (the tutor shows each step and the student confirms,
predicts or computes), **Faded** (the tutor as it runs today: authored questions, two tries, a switch question, the notebook),
**Independent** (no help; the credit rung). A helped student runs Worked → Faded → Independent → Independent; a capable one
Faded → Independent → Independent. The instructor assigns the starting rung next semester.

Scenarios take **roles** within an archetype. Each archetype will have at least four: one reserved for the Worked rung, one
reserved for the in-class exam (the tutor never shows it), and two or more floaters that the Faded and Independent rungs draw
from. The openers file gains a `role` column (worked | exam | floater; blank = floater). The instructor assigns the roles.

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
   One row per item, in the moves file under a new column `show`, with a per-scenario override like `ask`.
2. **Keyword candidates** from the chapter's own vocabulary, per scenario, for the instructor to approve into the `keywords`
   column. Chapter 10 is in `reference/openstax/Chapter10_IMF.md` (CC BY 4.0; paraphrase, do not quote into student-facing cells
   without the attribution line). The chapter's three worked examples (10.6–10.8) are the same three problem kinds the generator
   makes: use their language.
3. For **equilibrium**: the two scenarios you hold, with roles proposed (which is worked, which exam) and the `show` cells for the
   worked one, plus keyword candidates from the equilibrium chapter when the instructor sends it.

## What you do not do

Write problem numbers (the generator makes them); edit code, generated files or tests; change an approved cell. If something
needs the shell to change, say so and stop; Fable builds it.
