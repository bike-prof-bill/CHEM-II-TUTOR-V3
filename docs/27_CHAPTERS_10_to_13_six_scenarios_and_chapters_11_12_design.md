# Chapters 10 to 13 at six scenarios (seven for chapter 10), and the design of chapters 11 and 12 (Fable, 20 Oct 2026)

**The instructor's targets (20 Oct):** at least four scenarios for every archetype; at least six for every archetype in the first
four chapters, and seven for Clausius-Clapeyron. This week: chapters 10 to 13. The build now reports each archetype's count
against its target ("scenarios: 4 of the target 7 (needs 3 more)").

## Where each stands
| chapter | archetype | now | target | to write |
|---|---|---|---|---|
| 10 | `ch10_cc` Clausius-Clapeyron | 4 | 7 | 3 scenarios |
| 11 | `ch11_henry`, `ch11_raoult`, `ch11_colligative`, `ch11_osmotic` | 0 | 6 each | 24 scenarios, four new archetypes |
| 12 | `ch12_rates`, `ch12_initial_rates`, `ch12_integrated`, `ch12_arrhenius` | 0 | 6 each | 24 scenarios, four new archetypes |
| 13 | `ch13_eq` (ICE, Q vs K, Le Chatelier in one walk) | 5 | 6 | 1 scenario |
Chapter 13 stays one archetype: every problem walks all three of the instructor's chapter 13 milestones, so six scenarios cover
all three. Chapters 14 to 21 meet their target of four.

## Chapter 10: three more scenarios (generated, not sheet)
`ch10_cc` makes its problems from data, so a new scenario is an opener row plus, where the scene needs it, a rule for its
numbers (as the Drinking Bird keeps the body at room temperature). Send the opener row, the kinds it fits, the liquids it may
use, and the rule in words; Fable codes the rule and tests it. Eleven liquids in the data have no scenario yet: 1-propanol,
1-butanol, heptane, cyclohexane, benzene, toluene, chloroform, carbon tetrachloride, 2-butanol, isobutyl alcohol, tert-butyl
alcohol. Each scenario keeps the existing page or names a new one.

## Chapter 13: one more scenario
In the chapter 13 problem-sheet format (`ch13_problems_silent_beaker.csv`), with its kind chosen from the eight that exist
(`haber_setup`, `wgs_equilibrium`, the three tracers, `hi_volume`, `hi_equilibrium`, `no2_equilibrium`) or a new reaction
with its K and source, in which case Fable adds the kind.

## Chapters 11 and 12: eight new archetypes, sheet format (as chapters 16 to 21)
Each problem's steps, in order. Number steps end `_found`; picks end `_pick`; one perturbation, `perturb_1`, then its why. A
problem uses the steps its kind needs; skip the others. Tolerance: 2 % or half a unit in the last written place unless the
instructor sets another; counts exact.

**`ch11_henry`** (C = k_H P). Kinds `concentration`, `pressure`, `change`. Steps: `Pgas_found` (partial pressure, when a mole
fraction and total pressure are given) → `C_found` (M) → `mass_found` (g/L, when asked) | for `pressure`: `C_found` →
`Pgas_found` | for `change`: `C1_found`, `C2_found`. Perturbation: the water is warmed (solubility falls) or the pressure raised
(rises). Named mistakes to design for: k_H inverted; total pressure used for partial; mL/L or g/mol slips.

**`ch11_raoult`** (P = χ_solvent P°). Kinds `nonvolatile`, `volatile_pair`. Steps: `n_solvent_found`, `n_solute_found`,
`chi_found`, `P_found`, `dP_found` (the lowering) | for a pair: `chiA_found`, `PA_found`, `PB_found`, `Ptotal_found`, `yA_found`
(mole fraction in the vapour). Perturbation: more solute (vapour pressure falls). Mistakes: χ of the solute used; grams used for
moles; the pair's pressures not added.

**`ch11_colligative`** (ΔT = i K m). Kinds `boiling`, `freezing`, `molar_mass`. Steps: `mol_found`, `kg_found`, `m_found`
(molality, typed mol/kg or molal: a bare "m" is the metre), `i_found` (van 't Hoff factor), `dT_found`, `T_found` (new boiling or freezing
point, °C) | for `molar_mass`: `dT_found` → `m_found` → `mol_found` → `M_found` (g/mol). Perturbation: more solute (boiling point
rises, freezing point falls). Mistakes: i left out for an electrolyte; grams of solution for kg of solvent; ΔT added the wrong way
for freezing.

**`ch11_osmotic`** (Π = iMRT). Kinds `pressure`, `molar_mass`. Steps: `M_found` (molarity), `i_found`, `T_found` (K), `Pi_found`
(atm) | for `molar_mass`: `Pi_found` given → `M_found` → `mol_found` → `Mmolar_found`. Pick: `flow_pick` (water flows into |
out of | neither, the cell or bag). Perturbation: the outside solution made stronger (water leaves; option set rises/falls/
unchanged on the cell's volume). Mistakes: °C for K; R in J for atm; i left out.

**`ch12_rates`** (rate = −(1/a) Δ[A]/Δt = (1/c) Δ[C]/Δt). Kinds `from_reactant`, `from_product`. Steps: `rate_found` (the
reaction's rate, M/s), `rateX_found` for each other species asked, `sign_pick` (disappearing | appearing). Perturbation: none
needed if the instructor prefers; otherwise doubling a coefficient's species (unchanged reaction rate). Mistakes: the coefficient
multiplied not divided; the sign kept on a rate.

**`ch12_initial_rates`**. Kinds `two_reactants`, `one_reactant`. Steps: `orderA_found`, `orderB_found` (whole numbers, exact),
`overall_found`, `k_found` (with its units: M⁻¹ s⁻¹, M⁻² s⁻¹, s⁻¹, M/s; in the tutor since 20 Oct), `rate_found` (a predicted rate).
Perturbation: one concentration doubled (the rate rises by 2^order). Mistakes: order from the wrong pair of trials; k units for
the wrong order; the ratio inverted.

**`ch12_integrated`**. Kinds `zero`, `first`, `second`. Steps: `order_pick` (zero | first | second, from which plot is straight
or from k's units), `k_found`, `At_found` ([A] at a time) or `t_found` (time to a concentration), `half_found` (half-life).
Perturbation: the starting concentration doubled (first-order half-life unchanged; second-order halves; zero-order doubles).
Mistakes: log for ln; the first-order formula for a second-order reaction; [A]0 and [A]t swapped.

**`ch12_arrhenius`** (ln(k2/k1) = −(Ea/R)(1/T2 − 1/T1)). Kinds `Ea_from_k`, `k_from_Ea`. Steps: `T1_found`, `T2_found` (K),
`Ea_found` (kJ/mol) | `k2_found`. Perturbation: a catalyst is added (the rate rises; Ea falls). Mistakes: °C for K; R in kJ with
Ea in J; the reciprocal temperatures subtracted the wrong way.

## Simulations: active for every scenario
The instructor's rule (20 Oct): simulations must be active. Two changes follow.
1. **Every new scenario names its page**, an existing one or one Simulation_Claude builds, and every problem sheet carries a new
   column, `simulation parameters`, with the page's values for that problem (`reaction=H2Ol_to_H2Og; T=373`). The tutor uses
   them as given. Chapters 11 and 12 need pages: four for chapter 11, four for chapter 12, or fewer pages with modes.
2. **The pages already built now receive every problem's values**, read from each problem's own sentence (585 problems). Seventeen
   problems name a reaction, half-cell or ion the page does not have, and open the page's default with a notice until the data
   are added (the list below). A test fails if any new gap appears.

| page | missing | problems |
|---|---|---|
| `ch16/G_and_Q_simulator.html` | CH₃CO₂H(aq) → H⁺ + CH₃CO₂⁻; HF(aq) → H⁺ + F⁻ | SK6, WC5 |
| `ch16/entropy_simulator.html` | H₂O(l) → H₂O(s) (freezing) | MI3 |
| `ch16/free_energy_simulator.html` | ZnS(s) + H₂(g) → Zn(s) + H₂S(g); 2 Fe₂O₃(s) + 3 C(s) → 4 Fe(s) + 3 CO₂(g) | ZO1, ZO2 |
| `ch17/cell_simulator.html` | the PbO₂/PbSO₄ (lead–acid) and O₂/H₂O (fuel cell) half-cells | LA1–LA5, FC1–FC6 |
| `ch17/electrolysis_simulator.html` | Mg²⁺ from molten salt | AB4 |
