# Brief for SCENARIO_CLAUDE: Q versus K (`ch13_q_vs_k`), four scenarios

**13 Oct 2026, from Fable (third ARCHITECT_CLAUDE).** The archetype skeleton is built and walked in the harness
(`archetypes/ch13_q_vs_k.py`, `test_ch13_q_vs_k.py`, `gas/test_q_vs_k.js`). Nothing ships until your content arrives and the
instructor approves it: the openers file has no row, so the factory writes no bundle for this archetype.

## Decisions on record that bind this archetype
- Fixed problems, not generated (instructor, 13 Oct; the default for every new archetype).
- Q versus K is a separate archetype from ICE, and its scenarios do not reuse the Haber-Bosch Harvest or the Martian Fuel Factory
  (your own hand-off README, 13 Oct). The placeholder problems in the archetype are V2's (HI, N2O4, SO3, methanol): replace them.
- A sensor in every scene; the problem hidden until the particle account is given; roles (one worked, one exam, two floaters);
  the offer is extra; "ln" only inside an equation, no caret in tutor text (`docs/06_SCENARIO_CLAUDE_role.md`).

## The step map (what the student does, in order)
1. `account_given`: the particle account (your opener question, model answer, keyword cells).
2. `relation_chosen`: the Q expression from the Equations list (`eq_q`; K's expression is a look-alike and counts as a wrong try).
3. `conc_found` (only when the problem gives moles in a vessel that is not 1 L): the starting concentrations with units.
4. `Q_found`: Q as a number, asked for by name after the expression (so a number typed earlier is not read as Q, and Q = K is
   allowed). The key item; required unit: none.
5. `shift_predicted`: the `direction` kind. Options: "forward toward more <first product>", "reverse toward less <first
   product>", "neither because it is already at equilibrium". The right one is computed from Q and K. A student may type the
   word (forward, reverse, neither) instead of clicking. If you want other option wording, say so: the first word must stay a
   bare word, because the shell reads that word alone.
6. `meaning_given` (credit gate), then `reflection`.
When a reactant is absent (Q undefined) there is no `Q_found` item and the right direction is reverse; when a product is absent,
Q = 0 and the right direction is forward.

## Named errors (values the checker can see; you write the note and the ask in `content_ch13_q_vs_k_errors.csv`)
- `Q_INVERTED`: 1/Q typed as Q.
- `COEFFICIENTS_AS_MULTIPLIERS`: coefficients multiplied in rather than used as exponents.
- `EXPONENTS_DROPPED`: every exponent read as 1.
- `DIRECTION_REVERSED` is not a value: the wrong pick is a wrong try; a row lets the ask be scenario-specific.
Each is kept on a problem only when its value is clearly apart from Q and from the other traps; choose numbers so they are.

## What to send (one zip, as for chapter 13)
- `content_ch13_q_vs_k_openers.csv`: four rows, same 15 columns plus `role`; the fits column lists problem ids.
- `content_ch13_q_vs_k_moves.csv`: the rows now in the file are DRAFT (four copied from ICE, three empty: `conc_found`,
  `Q_found`, `shift_predicted`); rewrite every one for Q versus K, with show cells and the offer row for the worked scenario.
- `content_ch13_q_vs_k_errors.csv`: notes and asks for the ids above.
- A problems sheet like `docs/handoff_examples/ch13_problems.csv`: six per scenario, every family covered (all present with Q < K;
  Q > K; a product absent; a reactant absent; Q = K), full sentence, expected Q, trap values, constants with sources.
- Reaction rows for `archetypes/data/reactions.json` with a source for every Kc and its temperature. The four V2 rows now in that
  file are marked "source needed" and are yours to confirm or replace.
- Simulation addresses and media rows go through Simulation_Claude and the instructor as before.
