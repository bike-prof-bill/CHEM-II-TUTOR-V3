# Chapter 13 combined: one archetype, four longer scenarios (`ch13_eq`)

**13 Oct 2026 (evening), Fable, for the instructor.** The instructor's new rule for chapter 13: ICE and Q versus K are one
archetype; four scenarios; each begins with the direction (Q against K), does its ICE work where the problem has any, then meets
two separate perturbations, then the meaning and the last metacognitive question. This document is the architecture. The
instructor's background/suggestion document is still to come and may change the shape below; what is here is built and tested
so the two SCENARIO_CLAUDEs can start, not a final word.

## What the student does, in order
1. Particle account (the opener's question; a sensor in the scene).
2. The expression from the Equations list. The K form and the Q form both count (the student meets Q first); the instructor
   can make it one or the other.
3. Starting concentrations with units, only when the problem gives moles in a vessel that is not 1 L.
4. Q as a number, asked for by name after the expression (so Q = K is allowed and a number typed earlier is not read as Q). Q is
   checked against the value the data give (1.7 × 10⁻¹⁰ for the tracer), not against K restated.
5. The direction: forward, reverse, or neither, checked against Q and K.
6. The ICE work, by the problem's mode: `setup` (table, expression, method; stops before x: Haber), `solve` (through x, the
   other root, the answer, the leftover, K confirmed: Martian), or `none` (the tracer: nothing to solve).
7. Perturbation 1: a change to the mixture, named in the scenario's own words; the student predicts forward, reverse or
   neither; then says in words what the particles do (a text item the model judges, as it judges the account).
8. Perturbation 2: the same shape, a different change.
9. Meaning (credit gate), then the reflection.

## Perturbations the archetype can score (from the reaction record, no human arithmetic)
add a reactant or a product; remove one; add a common ion (a product ion of a dissolution); add a pure solid or liquid (no
shift); heat or cool (needs the sign of ΔH, recorded with a source in `reactions.json`); compress or expand (by the change in
gas moles; equal moles each side gives no shift); an inert gas at constant volume; a catalyst (no shift). The scenario sheet
names the type and the species; the scenario's moves rows carry the words ("a technician opens a valve and draws off ammonia").
A change that needs a number (a second ICE table after the perturbation) is not built; the instructor's document may ask for it.

## Where the pieces live
- `archetypes/_equilibrium.py`: the shared arithmetic (quotient with solids left out, direction, x by bisection, the quadratic's
  roots by the formula, perturbation directions). `ch13_ice` keeps its own copy until it retires, so nothing shipped moves.
- `archetypes/ch13_eq.py`: the archetype. Thirteen problems: H1–H6 and M1–M6 exactly as approved under `ch13_ice` (the test
  proves every declared number, trap and table unchanged), plus A1, the tracer, as a DRAFT placeholder.
- `content_ch13_eq_openers.csv` (no row yet), `content_ch13_eq_moves.csv` (the ICE rows marked DRAFT for re-approval plus the
  four perturbation rows), `content_ch13_eq_errors.csv` (the ICE errors plus Q's and `SOLID_IN_EXPRESSION`).
- `test_ch13_eq.py`, `gas/test_eq.js` (43 checks: the tracer at Q = K, Haber and Martian with both perturbations, every problem
  completable clean).
- Ships nothing until an approved scenario row exists; `ch13_ice` stays as the tutor the students see.

## Retirement plan
When the four scenarios are approved: `ch13_eq` ships; `ch13_ice` is removed from `archetypes/`, its content files and tests
retired (the log keeps their record); the two Claudes' rebuilt rows replace the DRAFT copies. The analysis lane should expect a
new archetype id in the log from that day.

## Rules settled by the instructor (13 Oct, evening)
- Ground of truth: the OpenStax text first; NIST only where the text has no value. Source lines in `reactions.json` say which.
- Significant figures: a problem's data carry the figures the text gives, and Q against K is judged at those figures (half a
  unit in the last place of K and of each concentration, propagated by the exponents). The tracer's 1.3 × 10⁻⁵ M and
  1.8 × 10⁻¹⁰ are equal to two figures; no figure is added to make the arithmetic exact. Each problem declares `sf`.
- The tracer has no table step. Perturbation pairs: the two Claudes propose, the instructor approves. The Q form and the K form
  of the expression both count (K is the special case of Q at equilibrium). A perturbation never asks for a number.
