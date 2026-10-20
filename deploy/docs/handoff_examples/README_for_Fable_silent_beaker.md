# For Fable, from SCENARIO_CLAUDE: "The Silent Beaker" (`ch13_eq`), content and build notes

Status: every row in this zip is approved by the instructor (13 Oct 2026), including the simulation page's register row.
Built against `for_SCENARIO_CLAUDE_ch13_eq_files.zip` (SHA-256 starts 7febee22). I ran all 18 problems through a scratch copy of
your `ch13_eq.py` (my changes in the scratch copy only): every Q, direction, perturbation answer and trap below came out as declared.

## Files
- `content_ch13_eq_openers.csv`: your file with the Silent Beaker row added (role floater).
- `content_ch13_eq_moves.csv`: your file with eight override rows for the Silent Beaker (account_given, Q_found, shift_predicted,
  perturb_1, perturb_1_why, perturb_2, perturb_2_why, meaning_given). It inherits relation_chosen, conc_found and reflection.
  Floater: no show cells, no offer row. Your four blank base perturbation rows are untouched.
- `content_ch13_eq_errors.csv`: the six rows you assigned me filled (Q_INVERTED, COEFFICIENTS_AS_MULTIPLIERS, EXPONENTS_DROPPED,
  SOLID_IN_EXPRESSION as base rows; FORWARD_AT_EQUILIBRIUM and FORWARD_ON_COMMON_ION for this opener), plus a Q_INVERTED
  override for this opener.
- `ch13_problems_silent_beaker.csv`: A1–A6 (AgCl), B1–B6 (AgBr), C1–C6 (AgI), your sheet's columns plus three: perturbation 1,
  perturbation 2, named wrong pick. Together they replace your placeholder A1. Problem 5 of each salt adds silver nitrate (instructor, 13 Oct), so it does not repeat change 1.
- `reactions_rows_silent_beaker.json`: `agcl_dissolution` replaces the current row; `agbr_dissolution` and `agi_dissolution` are new.
- `MEDIA_SOURCES_row_silent_beaker.csv`: register rows for the picture and for `silent_beaker_simulator.html` (approved; SHA-256
  starts e33ed9ec). The page itself goes to the instructor's media folder, not in this zip.

## Decisions since your architecture note (the instructor's, 13 Oct, later than your note)
- Kc for AgCl is 1.6 × 10⁻¹⁰, OpenStax Appendix J, Table J1, not the sketch's 1.8 × 10⁻¹⁰. The tracer problem's numbers are
  [Ag⁺] 2.0 × 10⁻⁵ and [Cl⁻] 8.0 × 10⁻⁶ M, so Q = K exactly. The sketch's 1.3 × 10⁻⁵ M would give Q above the textbook's K. Your
  equality tolerance still applies; it is not needed here.
- The salt varies after the opening: AgCl, AgBr, AgI (AgCN and AgSCN dropped). The opening scene stays silver chloride.
- No thermodynamic values: dH_sign = +1 for all three, on the instructor's word ("dissolving takes in heat"); rule-of-thumb level.
- Role: floater.

## What the build needs
1. **Three reactions and three kinds.** `agcl_tracer`, `agbr_tracer`, `agi_tracer`. Each takes perturb_1 = (add_common_ion, its
   anion, {"forward": "FORWARD_ON_COMMON_ION"}) and perturb_2 = (heat, None). A1, B1 and C1 carry named_shift
   {"forward": "FORWARD_AT_EQUILIBRIUM"}.
2. **Salt words in the moves rows.** The perturbation rows contain `{salt}` ("silver bromide"), `{anion}` ("bromide") and
   `{sodium_salt}` ("sodium bromide"), filled from the problem's reaction. Rename them to your placeholder form if you have one.
3. **Direction option wording for a dissolution.** "forward toward more silver ion" reads badly. Proposed, first word bare as you
   require: "forward: more of the solid dissolves", "reverse: more solid forms", "neither: no change overall". This needs
   per-kind option text. Approved by the instructor, 13 Oct.
4. **Moles with a solid (A6, B6, C6).** These give moles of the two ions in 0.500 L over the solid. In the scratch run I passed
   mol = [0, nAg, nX]. A cleaner way to mark the solid as present but not counted is yours to choose. The trap
   MOLES_NOT_CONCENTRATION is needed on `Q_found` in mode `none` (moles straight into Q: A6 6.3 × 10⁻¹², B6 1.0 × 10⁻¹⁴, C6
   6.3 × 10⁻¹⁸); today it exists only on the table and value_found.
5. **Simulation address.** The approved page reads `salt`, `Ag`, `X`, `solid`, `theme`. Your draft
   sim_keys are `cAg`, `cCl`. Please adopt the page's names and add `salt` and `solid` (solid = 0 for A3, B3, C3; 1 otherwise; 6s:
   the concentrations, not the moles). The four are new placeholders for the tutor's list.
6. **Media folder.** The opener row uses `ch13_eq/` for the picture and the page; confirm or rename.
7. **Not mine, seen in passing.** Inherited Haber-Bosch moves rows (`expression_set` park text, `method` switch and park) carry
   carets outside `\( \)`: "[NH3]^2", "x^3", "x^4". The instructor's rule is no caret in tutor text.
