# Chapter 10 (Clausius-Clapeyron, `ch10_cc`): what is built and tested, 13 Oct 2026

For SCENARIO_CLAUDE's question of 13 Oct. Every row is in the repository on this date and covered by the suite named in the last
column (`make test`). Content `b73787b901`, shell `bb174cdf`.

| Hand-off item | Built | Where | Test |
|---|---|---|---|
| Prediction (direction) before the number, on pressure AND temperature problems | yes, 10 Oct | `direction_predicted` on P1, P2, T1, T2 kinds; checked deterministically against the answer's direction | `test_vent.js`, `test_syringe.js`, `test_core.js` 6s |
| Depth step (vent): pressure from depth | yes, 10 Oct | `P_from_depth` item, a number, on the vent's T kinds; depth is a given, pressure the intermediate | `test_vent.js` |
| Pressure-difference step (bird) | yes, 10 Oct | `dP_found` item, derived from the answer and the known pressure | `test_bird.js`, `test_core.js` 7 |
| Per-student draws (no problem twice while others remain) | yes, step 6b | served list per student and archetype (`v3hist_…`), reset when exhausted, logged `HISTORY_RESET` | `tests/regression/no_repeated_problem.test.js` |
| Worked rung and its offer | yes, 13 Oct | `show` and `version` columns, `offer` row; Worked → Faded → Independent; the offered two-point problem on the same liquid, extra | `test_core.js` 6t |
| Label-word column | yes, 9 Oct | `label_words` in the openers file (col 13): naming without mechanism does not pass the gate | `test_core.js` (opener gate), `test_syringe.js` |
| 44.01 kJ/mol trigger on `WATER_DH_USED` | yes, 13 Oct | `substances.json` `dHvap_at_25C_kJ_mol` (sourced); second trap value, Drinking Bird, P kinds | generator validation; `test_bird.js` (first trigger) |
| "ln" only inside mathematics | yes, 13 Oct | four cells and the slope sentence; the shell's units sentence spells the function out | `test_core.js` 6r |
| Keywords (12 Oct lists) | yes, 13 Oct | four `keywords` cells; short keywords (IMF) match as whole words | `test_core.js` (gate) |
| Scenario roles | yes, 13 Oct | `role` column: Alcohol worked, Bird exam (served once at Independent, unannounced), Syringe and Vent floaters | `test_core.js` 6t |
| Math as \( \) in authored text | yes, 13 Oct | KaTeX in `index.html`, tutor messages only; the instructor confirms on screen | page parses; not rendered in the sandbox |
| Wording updates of 12 Oct (inverse function, external pressure, the P-kind park text) | yes | moves cells; baseline replaced by hand | `test_syringe.js` |

Not SCENARIO_CLAUDE's to track but relevant: units read and cancelled in typed setups (11 Oct), near miss and repeat (11 Oct),
relative subscripts (11 Oct), authored questions everywhere (11 Oct).

## The three simulation pages

`media/` never passes through Fable; the pages are the instructor's and Simulation_Claude's. Their addresses as the tutor calls them
(from the openers file, `simulation` column; `{…}` filled per problem):

- Syringe: `ch10_cc/syringe_boiling_simulator.html?substance={substance}&T={T}&unit={unit}&theme={theme}`, opens after the answer, before the meaning question
- Drinking bird: `ch10_cc/drinking_bird_simulator.html?substance={substance}&T={T}&T_known={T_known}&unit={unit}&theme={theme}`, opens after the answer and the difference
- Vent: `ch10_cc/deep_sea_vent_simulator.html?depth={depth}&unit={unit}&theme={theme}`, opens after the answer

Their rows are in `docs/MEDIA_SOURCES.csv` (lines 7, 9, 11). The files themselves the instructor sends to SCENARIO_CLAUDE from his
`media/ch10_cc/` folder; Fable does not hold them.
