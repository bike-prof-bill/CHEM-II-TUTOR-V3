# Fable list, chapter 17 (SCENARIO_CLAUDE, 18 Oct 2026). Running list for the single send; all five archetypes approved by the instructor, 18 Oct 2026.

## Needs your decision (Fable)

1. **Five new archetypes,** designed by SCENARIO_CLAUDE in the chapter 13–16 pattern:

   | id | archetype |
   |---|---|
   | `ch17_balancing` | balancing by half-reactions |
   | `ch17_cell` | galvanic cells |
   | `ch17_E_G_K` | E°, ΔG° and K |
   | `ch17_nernst` | the Nernst equation |
   | `ch17_electrolysis` | electrolysis |

   Step ids, expected values, trap values and right picks are in each problem sheet.
2. **Balancing needs one new step kind: a row of coefficient boxes** (approved by the instructor instead of an equation checker). Each
   problem sheet gives the species in screen order and the expected coefficients; a blank box means 1. The electron counts and n are
   ordinary numbers.
3. **Very large and very small K** (10¹⁶⁸, 10⁻¹⁵²): accept a power of ten, such as "10^168" or "1e168" (instructor, 18 Oct).

## Engineering

1. **Data:** Appendix L (OpenStax); F = 96,485 C/mol; 0.0592 V at 25 °C; molar masses from the OpenStax periodic table. Example
   17.10's chromium density, 7.19 g/cm³, is confirmed in the text.
2. **New pick kinds:**
   - `oxidized_pick`;
   - `anode_pick`, `electron_pick` and `bridge_pick`;
   - `verdict` (yes, no, or neither when E = 0).
3. **Tolerance:** ±0.01 V on Nernst answers (instructor, 18 Oct).
4. **Pages** (briefs sent, with templates, to SIMULATION_CLAUDE):

   | page | placeholders |
   |---|---|
   | `ch17/cell_simulator.html` | `left`, `right`, `cl`, `cr`, `theme` |
   | `ch17/electrolysis_simulator.html` | `ion`, `I`, `t`, `mode`, `theme` |

   Balancing has no page (approved).
5. **A textbook misprint:** Example 17.6 prints ΔG° as "−240.6 J/mol"; it is kJ/mol. The worked problem uses kJ.
6. **Approved with the archetypes:**
   - coefficient boxes for balancing, with the half-reactions shown after acceptance;
   - the textbook's HNO₃ + H⁺ form in the worked balancing problem;
   - picks for cell anatomy;
   - K accepted as a power of ten;
   - the Appendix L alkaline-type cells;
   - the E = 0 Nernst problems;
   - masses accepted within 0.5%;
   - "The Silver Tree" in place of "The Copper-Coated Nail".
7. **Pages approved by the instructor, 18 Oct 2026** (with SIMULATION_CLAUDE's four recommendations: 10 MΩ meter and 10 Ω lamp, compressed time with a true "time run" readout, open-circle electrons, the extra `circuit` and `m` parameters). Data checked by SCENARIO_CLAUDE: all 14
   Appendix L potentials (stored as V × 10⁴) and all molar masses match; no network calls.

   | page | SHA-256 starts | placeholders |
   |---|---|---|
   | `media/ch17/cell_simulator.html` | 117f743a | `left`, `right`, `cl`, `cr`, `circuit`, `theme` |
   | `media/ch17/electrolysis_simulator.html` | 569656a5 | `ion`, `I`, `t`, `mode`, `m`, `theme` |
8. **Media:** twenty pictures held in `media/ch17/`, with register rows and opener cells filled. Four code-generated pictures have
   captions added by SCENARIO_CLAUDE. Chapter 17 is complete.
