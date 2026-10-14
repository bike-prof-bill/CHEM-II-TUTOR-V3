# For Fable, from SCENARIO_CLAUDE, 14 Oct 2026: three `ch13_eq` floaters

The scenarios are "The Silent Beaker", "The Purple Piston" and "The Fading Brown". This is the single zip the instructor
asked for. It replaces `SilentBeaker_for_Fable.zip` and `ch13_eq_two_floaters_for_Fable.zip`; neither was sent. Built against
`for_SCENARIO_CLAUDE_ch13_eq_files.zip` (SHA-256 starts 7febee22). Every row I wrote is approved by the instructor (13–14 Oct),
and nothing is pending. With Haber-Bosch (exam) and the Martian Fuel Factory (worked), chapter 13 has its scenarios; the
instructor's next equilibrium work is in the spring.

## Files
- `content_ch13_eq_openers.csv`: your file plus three rows, all role floater.
- `content_ch13_eq_moves.csv`: your file plus override rows: Silent Beaker 8, Purple Piston 15, Fading Brown 13. Your blank
  base perturbation rows are untouched; each scenario overrides every perturbation item.
- `content_ch13_eq_errors.csv`: your file plus:
  - the six rows you assigned me: Q_INVERTED, COEFFICIENTS_AS_MULTIPLIERS, EXPONENTS_DROPPED and SOLID_IN_EXPRESSION as base
    rows; FORWARD_AT_EQUILIBRIUM and FORWARD_ON_COMMON_ION for the Silent Beaker;
  - per-opener rows: Silent Beaker Q_INVERTED; Purple Piston nine (OLD_VOLUME_USED and SHIFT_ON_EQUAL_MOLES are new);
    Fading Brown five.

  The Purple Piston and Fading Brown carry their own CHANGE_COEFF_IGNORED, COEFF_NOT_EXPONENT and EXPONENT_NOT_IN_TABLE rows,
  because the shared ones name the Haber-Bosch species. I used the file's ids; your code's TRAP_NOTES call two of them
  EQ_COEFF_NOT_EXPONENT and EQ_EXPONENT_NOT_IN_TABLE.
- Problem sheets, 18 problems each, one version drawn at random within a family:
  - `ch13_problems_silent_beaker.csv`: A1–A6 AgCl, B1–B6 AgBr, C1–C6 AgI. They replace your placeholder A1.
  - `ch13_problems_purple_piston.csv`: P1a–P6c.
  - `ch13_problems_fading_brown.csv`: F1a–F6c; F1a is OpenStax Example 13.2.
- `reactions_rows_ch13_eq.json`: agcl_dissolution replaces your row (Kc 1.6 × 10⁻¹⁰, Appendix J). New: agbr_dissolution,
  agi_dissolution, hi_formation (50.0 at 400 °C, section 13.3) and no2_dimerization (1.6 × 10² at 25 °C, Example 13.2; heat sign
  from 13.3). Every row carries its source.
- `MEDIA_SOURCES_rows_ch13_eq.csv`: three pictures and three simulation pages, all approved.

  | file | SHA-256 starts |
  |---|---|
  | `silent_beaker_simulator.html` | e33ed9ec |
  | `purple_piston_simulator.html` | f3cbd440 |
  | `fading_brown_simulator.html` | 86c4592c |
  | the piston picture, v3 | 99c93028 |
  | the Fading Brown picture, v4 | ed7db379 |

  The pages and pictures are in the instructor's `media/ch13_eq/` folder, not in this zip.

## Decisions since your architecture note (the instructor's)
- Ground of truth: OpenStax first. Kc values are the textbook's; the heat signs are the textbook's (NO₂) or the instructor's
  word (the silver salts, hydrogen iodide). No thermodynamic values are used.
- The Silent Beaker's tracer problem has Q = K exactly ([Ag⁺] 2.0 × 10⁻⁵, [Cl⁻] 8.0 × 10⁻⁶ M). The salt varies after the
  opening.
- More versions per family: three for the Purple Piston and the Fading Brown, three salts for the Silent Beaker.
- Answer choices for a dissolution: "forward: more of the solid dissolves", "reverse: more solid forms", "neither: no change
  overall". The gas scenarios use your default wording.

## What the build needs
1. **Reactions and kinds:**

   | kind | problems | mode | perturb_1 | perturb_2 | named_shift |
   |---|---|---|---|---|---|
   | agcl_tracer, agbr_tracer, agi_tracer | A, B, C | none | (add_common_ion, the anion, {"forward": "FORWARD_ON_COMMON_ION"}) | (heat, None) | A1, B1, C1: {"forward": "FORWARD_AT_EQUILIBRIUM"} |
   | hi_volume | P1a–c | none | (add_reactant, "H2") | (heat, None) | {"forward": "SHIFT_ON_EQUAL_MOLES", "reverse": "SHIFT_ON_EQUAL_MOLES"} |
   | hi_equilibrium | P2–P6 | solve | (add_reactant, "H2") | (heat, None) | |
   | no2_equilibrium | F1–F4, F6 | solve | (compress, None) | (heat, None) | |
   | no2_equilibrium | F5 | none | (compress, None) | (heat, None) | |

2. **Salt words.** The Silent Beaker's perturbation rows contain `{salt}`, `{anion}` and `{sodium_salt}`.
3. **Answer-choice wording per kind**, for the dissolution kinds.
4. **Moles over a solid (A6, B6, C6).** MOLES_NOT_CONCENTRATION is needed on `Q_found` in mode none (values in the sheet).
5. **"Solve" beyond the water-gas shift.** `make_fixed` looks up "H2" and "CO" by name.
   - hi_equilibrium: value_found is [HI]; leftover_found is the species named in each problem's second question.
   - no2_equilibrium: value_found is [N₂O₄]; leftover_found is [NO₂]. Every problem is quadratic (never a perfect square).

   The sheets give each problem's method, x, other root, answers and traps, including CHANGE_COEFF_IGNORED's x where the
   change row has −x for NO₂.
6. **A volume change in P1.** conc_found is needed even when the new volume is 1.00 L. OLD_VOLUME_USED is the value from the old
   volume (sheet). With equal gas moles, Q from moles equals Q from concentrations, so MOLES_NOT_CONCENTRATION cannot fire on Q
   there.
7. **Simulation addresses (new placeholders):**

   | scenario | placeholders | notes |
   |---|---|---|
   | Silent Beaker | `salt`, `Ag`, `X`, `solid` | solid = 0 for A3, B3, C3 |
   | Purple Piston | `nI2`, `nHI` | with the existing `nH2`, `V` |
   | Fading Brown | `nNO2`, `nN2O4` | with the existing `V` |

8. **Media folder** `ch13_eq/`: confirm or rename.
9. **Not mine, seen in passing.** Inherited Haber-Bosch moves rows (`expression_set` park text, `method` switch and park) carry
   carets outside `\( \)`: "[NH3]^2", "x^3", "x^4". The instructor's rule is no caret in tutor text.
