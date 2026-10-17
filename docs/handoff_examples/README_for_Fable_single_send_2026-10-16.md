# For Fable, from SCENARIO_CLAUDE, 16 Oct 2026: the single send (chapter 13 floaters, chapter 14 so far, page repairs)

The instructor contacts you once with everything since the chapter 13 floaters. Every row in this zip is approved by the instructor
(13–16 Oct 2026); none is DRAFT. Two folders:

- `chapter_13_eq_and_page_repairs/`: the three `ch13_eq` floaters (Silent Beaker, Purple Piston, Fading Brown) with their own
  README, plus register updates for pages repaired for a Safari fault: `ch13_ice` (Haber-Bosch, Martian) and `ch10_cc` (syringe,
  drinking bird, deep-sea vent; the alcohol page needed no repair).
- `chapter_14/`: two archetypes, six scenarios. Built against `for_SCENARIO_CLAUDE_chapter_14_files.zip` (SHA-256 starts a0b05c29).

## Needs your decision

Nothing from the instructor. The questions below are yours: how to build what the approved rows need.

## Engineering

### Chapter 14: what is here

| archetype | scenario | role | problems | page |
|---|---|---|---|---|
| `ch14_ph` | The Corn Soak | worked | W1–W6 | corn_soak_simulator.html |
| `ch14_ph` | Concrete Burn | exam | E1–E6 | off_the_scale_simulator.html |
| `ch14_ph` | Off the Scale | floater | N1a–N6c (18) | off_the_scale_simulator.html |
| `ch14_ph` | The Stockroom Morning | floater | R1–R6 | off_the_scale_simulator.html |
| `ch14_acidbase` | Same Label, Different pH | worked | K1–K6 | weak_acid_base_simulator.html |
| `ch14_acidbase` | The Fishy Bowl | exam | X1–X6 | weak_acid_base_simulator.html |

Files:
- `content_ch14_ph_openers.csv`, `content_ch14_ph_moves.csv`, `content_ch14_ph_errors.csv`, and the same three for
  `ch14_acidbase`: your files with every row filled. The base (shared) moves rows of each archetype are written to be shared by
  every scenario; scenario rows override the particle account and the meaning question, and the worked scenarios carry show cells
  in two versions and an offer row, as in the Martian moves file.
- Problem sheets: `ch14_ph_problems_off_the_scale.csv`, `ch14_ph_problems_corn_soak_stockroom_concrete.csv`,
  `ch14_acidbase_problems_same_label.csv`, `ch14_acidbase_problems_fishy_bowl.csv`. They carry the full sentence, expected value of
  every item, givens, trap values and sources. They replace your placeholder problems.
- `acids_bases_changes_ch14.json`: two corrections and four new entries for `acids_bases.json`.
- `MEDIA_SOURCES_rows_ch14.csv`: the three approved pages. Chapter 14 has no pictures yet.

Every problem was run through your own `ch14_ph.py` or `ch14_acidbase.py` in a scratch copy, with the data changes below; every
expected value and trap came out as the sheets declare.

### Chapter 14: what the build needs

1. **Data** (`acids_bases_changes_ch14.json`). These agree with the Appendix H and I the instructor supplied:
   - hydrofluoric acid Ka 7.2 × 10⁻⁴ → 6.4 × 10⁻⁴;
   - nitrous acid 4.5 × 10⁻⁴ → 4.6 × 10⁻⁴;
   - new: calcium hydroxide (strong, two hydroxides; Table 14.6; saturated near 0.0069 M);
   - new: formic acid (Ka 1.8 × 10⁻⁴);
   - new: trimethylamine (Kb 6.3 × 10⁻⁵);
   - new: dimethylamine (Kb 5.9 × 10⁻⁴).

   Your placeholder W1 says household vinegar is about 0.10 M; 5 % vinegar is about 0.8 M (Exercise 62).
2. **Moles and volume as givens** in `ch14_ph`: N6a–N6c, W1, W2, W5, R1–R3 and E1–E6 give moles in a volume. Needed: givens `n` and
   `V`, ion_found = n / V × ions per formula. Then the formula concentration is not a given, and IONS_PER_FORMULA_IGNORED can be
   caught. No volume is 1.00 L, so typed moles never equal a right answer.
3. **New named mistakes** (values; in the errors files, with the values in the sheets):

   | error | archetype | where | the value the tutor sees |
   |---|---|---|---|
   | PH_SIGN_DROPPED | ch14_ph | N1, pH_found | −pH (the pH is below zero) |
   | POH_SIGN_DROPPED | ch14_ph | N5, pOH_found and pH_found | −pOH; 28.00 − pH |
   | LN_FOR_LOG | ch14_ph | pH_found, all problems | the pH from the natural logarithm |
   | DILUTION_AWAY_FROM_7 | ch14_ph | perturb_1 | named wrong pick: "falls" for an acid, "rises" for a base |
   | MOLES_NOT_CONCENTRATION | ch14_ph | ion_found, moles problems | the moles typed as M |
   | POH_TYPED_AS_PH | ch14_acidbase | pH_found, weak bases | the pOH |

4. **The exam scenarios hold one method.**
   - The Fishy Bowl's six problems all hold the 5 % rule. This is an exception to "at least one fails per scenario", approved so
     that every version tests what the in-class problem tests. The worked scenario's variant covers the failing case.
   - Concrete Burn's six problems are all calcium hydroxide given as moles in a volume, for the same reason.
5. **Show cells.**
   - The Corn Soak: versions "one_hydroxide" (NaOH) and "two_hydroxides" (Ca(OH)₂).
   - Same Label: versions "holds" (0.10 M acetic acid) and "fails" (0.00050 M).
   - Both have an offer row.
6. **Placeholders in moves text:** `{substance}`, `{formula}`, `{conjugate}`, as your brief listed.
7. **Simulation addresses (new placeholders):**

   | archetype | address | placeholders |
   |---|---|---|
   | `ch14_ph` | `ch14_ph/off_the_scale_simulator.html?strong={strong}&c={c}&theme={theme}`; `corn_soak_simulator.html` takes the same | `strong`, `c` (for moles problems, the formula concentration) |
   | `ch14_acidbase` | `ch14_acidbase/weak_acid_base_simulator.html?species={species}&c={c}&theme={theme}` | `species`, `c` |

   The weak page ignores `K` and uses its own Appendix H and I table; `c` runs from 1.0 × 10⁻⁵ to 2.0 M. If the archetype holds a
   concentration range, widen it to match.
8. **Page fingerprints** (in the register rows):

   | page | SHA-256 starts | note |
   |---|---|---|
   | Off the Scale | 803bd330 | |
   | Corn Soak | 6eae2cbf | |
   | weak acid and base | 444fc0c5 | replaces 6119d977, which you may have seen in a note |

### Carried from chapter 13

The inherited Haber-Bosch moves rows (`expression_set` park text, `method` switch and park) carry carets outside `\( \)`:
"[NH3]^2", "x^3", "x^4". The instructor's rule is no caret in tutor text.

### Next, for your information

- Acids & Bases needs at least two floaters.
- Buffers and Titration follow.
- The simulation plan is pages shared through their addresses: one page extended first for buffers, then for titration.
