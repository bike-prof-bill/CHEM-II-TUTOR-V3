# Chapter 15 (equilibria of other reaction classes): four archetypes, prepared 16–17 Oct 2026

**Fable, for the instructor.** Four archetypes from your milestones list: `ch15_ksp` (Ksp and molar solubility), `ch15_common_ion` (the common
ion), `ch15_qsp` (Qsp against Ksp: will a precipitate form), and, on your ruling of 17 Oct, `ch15_complex` (complex-ion equilibria:
the formation constant and the free metal ion). Shared arithmetic in
`archetypes/_solubility.py`; salts in `archetypes/data/salts.json` (Appendix J first; values marked for SCENARIO_CLAUDE to confirm
from the appendix). Fifteen placeholder problems let the harness walk every step (53 checks); every number is re-derived in
`test_ch15.py`. Nothing ships.

## Step maps
- **Ksp** (`s_from_ksp`: Ksp given; `ksp_from_s`: solubility in grams per litre given): particle account → the Ksp expression → the
  s table over the two ions (the solid is present and has no column) → the expression Ksp = (a s)^a (b s)^b → s (for `ksp_from_s`,
  moles per litre from grams per litre) → the concentration of the ion that forms more than once per unit (skipped for a 1:1 salt,
  where both equal s) → grams per litre (`s_from_ksp`) or Ksp (`ksp_from_s`) → one perturbation: a salt sharing an ion is added,
  solubility falls → why → meaning → reflection.
- **Common ion** (`common_cation`, `common_anion`): account → the Ksp expression → the s table with the ion already present in
  the I row → the expression → method: drop s next to the common ion when the 5 % rule holds, else the exact root; solving as in
  pure water is a wrong pick → s → the pure-water s for comparison → how many times smaller → perturbation: more of the common
  ion, solubility falls → why → meaning → reflection.
- **Qsp** (`precipitates`, `stays_dissolved`; the kind is computed from the numbers): account → the Qsp expression → each ion's
  concentration after mixing, over the total volume → Qsp → verdict (forms | none | saturated; a direction item) → perturbation:
  more of one ion, Q rises → why → meaning → reflection.

- **Complex ions** (`free_metal`): account (the ligand's lone pairs binding the metal) → the Kf expression (or Kd = 1/Kf) → the
  concentrations after complete formation, over the total volume (the complex, and the ligand left over; with a large excess the
  ligand left is accepted within the amount consumed) → Kd = 1/Kf → the dissociation table (complex | metal | ligand) → the
  expression Kd = x (L + n x)^n / (C − x) → method: drop x when it is small next to both the complex and the ligand left, else the
  exact root; starting before formation is a wrong pick → x, the free metal ion → how many times smaller than before complexing →
  perturbation: more ligand, free metal falls → why → meaning → reflection.

## Named wrong turns the tutor can see (values or shape; the asks are SCENARIO_CLAUDE's)
Ksp: the coefficient as a multiplier not an exponent and the exponent without its coefficient in the table (by shape); +s for an
ion that forms two per unit (table); Ksp over the coefficient without the root; the root of Ksp alone (the 4 or 27 left out); s
given where 2s was asked; grams and moles per litre swapped; Ksp from the ion concentrations with the exponents dropped. Common
ion: the pure-water s; the small-s value where s is not small; the pure-water method as a pick. Qsp: a concentration before
mixing used after it (named on Q; at the concentration step it equals a given and is read as a restatement); a concentration over
the other solution's volume; 1/Q; exponents dropped; coefficients multiplied in; the wrong verdict either way. Complex ions: the ligand's full concentration as the ligand left; Kf used where Kd was needed; the ligand to the first power
where n bind; the metal's pre-complexing concentration given as the free metal, or a table that starts before formation; the
small-x value where Kf is small enough that x is not small; the other solution's volume. Everywhere: "more dissolves when a
common ion is added" and "more free metal when ligand is added" as named picks.

## Shell and engine changes made for this chapter
Units g/L, mg/L and g/mol added to `units.json` (two new dimensions). In the s table, s is read as the unknown (an alias of x).

## Rulings (instructor, 17 Oct)
1. Complex Equilibrium built now, as the fourth archetype.
2. One perturbation per problem, as prediction in words.
3. The Qsp verdict keeps "saturated" as a distractor for now.
4. SCENARIO_CLAUDE confirms every Ksp and Kf from Appendices J and K; the placeholders are marked as unconfirmed.
