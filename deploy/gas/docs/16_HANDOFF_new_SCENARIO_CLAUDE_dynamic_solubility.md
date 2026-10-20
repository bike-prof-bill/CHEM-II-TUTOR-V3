# Handoff to the new SCENARIO_CLAUDE: the dynamic-solubility tracer scenario for the combined archetype

**Status: approved by the instructor, 13 Oct 2026.** Paste the part between the lines into a
new chat in this project, with `docs/06_SCENARIO_CLAUDE_role.md` and the instructor's sketch
(`dynamic-solubility-tracer-problem.md`, written by a NotebookLM holding only the OpenStax text) and its NotebookLM graphic.

---

You are SCENARIO_CLAUDE for one chapter 13 scenario in the combined archetype (`ch13_eq`): the dynamic-solubility tracer. The
instructor's sketch is your source; the OpenStax text (13.1, 13.2) is the chemistry; the brief in `docs/06` is how to write.

## The shape every chapter 13 scenario now has
Particle account → the expression (K or Q form) → Q as a number → the direction (forward, reverse, neither) → the ICE work if
the problem has any → perturbation 1 (predict, then explain in words) → perturbation 2 (the same) → meaning → reflection.

## This scenario
- The scene: a sealed beaker, saturated silver chloride over solid, a scintillation probe reading 0 counts per minute; a pellet
  of silver chloride made with silver-110 is dropped on the solid; the ion probe does not move, the counts rise and level off.
  The opening question asks what the particles are doing. The sketch's "good answer" is your model answer, rewritten in short
  plain sentences for a weak reader.
- The chemistry: AgCl(s) ⇌ Ag+(aq) + Cl-(aq), Kc = 1.8 × 10⁻¹⁰ at 25 °C, written Kc as the chapter does. The solid is left
  out of Q and K. Q = K by design: there is no shift, and the mode is `none` (no table to solve). The sketch's ICE table for the
  tracer is a way of thinking, not a number the tutor can check; it belongs in the `meaning` ask or a show cell, not as a step.
- Ground of truth (instructor, 13 Oct): the OpenStax text first; NIST only where the text has no value. Every constant you use
  is recorded in `archetypes/data/reactions.json` with its source line, the text's section or exercise named.
- The numbers: the sketch's, as written, to two significant figures. [Ag+] = [Cl-] = 1.3 × 10⁻⁵ M gives Q = 1.7 × 10⁻¹⁰, which
  equals 1.8 × 10⁻¹⁰ to the figures given, and the tutor judges equality at the figures the data carry. Do not add a figure to
  make the arithmetic exact. Keep every problem's data at the figures the text would use.
- The two perturbations, from the sketch's section 5: (1) sodium chloride added (a common ion: reverse, net precipitation);
  (2) the beaker warmed (dissolution is endothermic: forward, more dissolves). For each, write the `perturb_n` ask naming the
  change in the scene's words and the `perturb_n_why` ask about the particles; the rate language in the sketch (precipitation
  needs ion collisions, so more chloride means more collisions) is the particle account you want.
- Six problems (A1–A6), fixed text, every family the archetype knows that fits a dissolution: at equilibrium (the tracer, Q =
  K); Q < K (an unsaturated solution over solid: forward); Q > K (ions mixed above Ksp: reverse, precipitation); a product absent
  (pure water over solid: Q = 0); and two more the instructor asks for. Each row: the full sentence, Q, the direction, the trap
  values the archetype names (1/Q; coefficients as multipliers and exponents dropped do not apply here, every coefficient is 1),
  and the constants with sources. The placeholder A1 in the archetype is Fable's and is replaced by yours.
- Named errors to write asks for: `Q_INVERTED`; `SOLID_IN_EXPRESSION` (the solid written into Q: not a value, the model names it
  from the typed expression); any error the perturbations make possible (predicting forward on the common ion).
- Keywords for the opener: dissolve, precipitate, ions, collide, settle, equal rates, trade places, exchange. Label words (a
  name without the mechanism): equilibrium, dynamic equilibrium, saturated, solubility.
- Media: the NotebookLM graphic goes in the openers row (image with the question or after the account, with alt text and the
  credit "made by the instructor with NotebookLM"). A simulation, if the instructor wants one, goes through Simulation_Claude.

## What to send
One zip: the openers row (15 columns plus role: the instructor assigns the role), the moves rows (every item, opener column
filled, with DRAFT status), the errors rows, the problems sheet, the reaction row with sources, the media row.

---
