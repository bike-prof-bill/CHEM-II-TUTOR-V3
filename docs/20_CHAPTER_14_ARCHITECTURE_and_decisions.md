# Chapter 14 (acid-base equilibria): four archetypes, as the instructor ruled (15 Oct 2026)

**Fable, for the instructor.** Four archetypes, one per concept so none is missed: `ch14_ph` (pH & pOH), `ch14_acidbase`
(Acids & Bases: weak acids and bases), `ch14_buffer` (Buffers), `ch14_titration` (Titration). Each has its own content files,
scenarios and roles. Shared arithmetic lives in `archetypes/_acidbase.py`. Nothing ships: no openers rows, every moves row DRAFT.
Seventeen placeholder problems from OpenStax worked examples let the harness walk every step (53 checks); every number is
re-derived in `test_ch14.py`.

## Rulings recorded (15 Oct)
1. Four archetypes, not one. The second is named Acids & Bases.
2. Perturbations are predictions in words (rises / falls / unchanged, then why); two for weak acids, bases and buffers, one for
   strong acids and bases.
3. Buffers: after each prediction the student computes the new pH. The addition is a volume of strong acid or base, small
   next to the buffer but more than 0.75 mL (the archetype refuses less), and large enough that the tutor can tell the new pH
   from the old (pH is read to two decimals; the archetype refuses an addition that moves it by 0.06 or less).
4. Titration by region: the pure acid solution (Ka), Henderson-Hasselbalch up to just before the equivalence point, salt
   hydrolysis (the conjugate's Kb = Kw/Ka) at the equivalence point, the excess titrant after it. A strong acid with a strong base
   has three regions, pH 7.00 at equivalence.
5. Constants: SCENARIO_CLAUDE works from the OpenStax appendices; values in `acids_bases.json` carry "instructor confirms".
6. The small-x rule follows the text: the right method when the 5 % rule holds, the quadratic when it fails, a check step after
   the percent. (The instructor's own classroom rule, c > 100·K, is noted here and not encoded.)

## Step maps
- **pH & pOH** (`strong_acid`, `strong_base`): account → pH relation → the ion concentration from the formula, with units,
  counting ions per formula unit → pH → pOH → tenfold dilution: pH rises (acid) or falls (base), then why → meaning → reflection.
- **Acids & Bases** (`weak_acid`, `weak_base`): account → Ka or Kb expression → ICE table (water not in it) → the expression in
  x → method (small-x or quadratic) → x, with units → (pOH) → pH → percent ionised → the 5 % check (holds / fails) → dilution:
  percent ionised rises, why → the conjugate as a salt: pH rises (acid) or falls (base), why → meaning → reflection.
- **Buffers** (`buffer`): account → Henderson-Hasselbalch → base-to-acid ratio → pH → a little strong base: pH rises, why,
  the new pH → a little strong acid: pH falls, why, the new pH → meaning → reflection.
- **Titration** (`weak_start`, `weak_before`, `weak_at`, `weak_after`, `strong_before`, `strong_at`, `strong_after`; the kind is
  computed from the moles, so a scenario lists the kinds it covers): account → region (a pick: start / before / at / after the
  equivalence point) → the relation that region needs → moles of acid and of titrant, both, with units → the region's chain
  (start: the weak chain; before: ratio then pH; at: the conjugate's concentration in the total volume, Kb, x, pOH, pH; after:
  the excess over the total volume, pOH, pH; strong at: 7.00) → which side of 7 and why → meaning → reflection.

## Named wrong turns the tutor can see (values or shape; the asks are SCENARIO_CLAUDE's)
pH & pOH: the pOH offered as the pH; the formula concentration as [OH⁻] for a dihydroxide (undetectable when it equals the given,
which it always does for a plain dihydroxide problem; a problem that also dilutes avoids that). Acids & Bases: x = Ka·c (square
root forgotten); the weak acid treated as strong; pKa as pH; the fraction for the percent; the small-x value where the 5 % rule
fails; x above the starting concentration; water in the table or the expression; three wrong picks (percent falls on dilution;
the conjugate moves the pH the wrong way). Buffers: the inverted ratio (on the ratio and the pH); pKa plus the ratio without
the logarithm; the added acid or base treated as free in solution; "unchanged" after an addition. Titration: moles from one
solution only; the sample volume used instead of the total; the inverted ratio before equivalence; the acid left treated as
strong; Ka used for the hydrolysis; pH 7 at a weak acid's equivalence point; pKa offered at equivalence; the pOH as the pH.
Where a wrong value coincides with a given (equal concentrations of acid and titrant make "sample volume alone" give the given
back), the engine drops the trap as undetectable; the brief tells SCENARIO_CLAUDE how to choose numbers so it is caught.

## Shell changes made for this chapter
Typed calculations may carry log, ln, sqrt and exp ("-log(0.0025)", "14 + log(0.010)", "sqrt(1.8e-5*0.1)" are read like numbers).
pH and pOH are read to two decimals (window 0.03); other values to two significant figures.

## Still open
- The titration pairs beyond these two (weak base with strong acid) and a dihydroxide dilution problem for pH & pOH, if wanted.
- Simulations for chapter 14 (a pH probe over a titration curve is the natural one) through Simulation_Claude.
