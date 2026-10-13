# Chapter 13 scenarios as they stand: ICE tables and Q versus K

**12 Oct 2026, for the instructor and SCENARIO_CLAUDE.** Everything here is V2's (the tool that ran this term), copied from `reference/v2/Code_V2-6.txt` and `index_V2.html`. In V3, `ch13_ice` carries these six openers and six problems as placeholders (status DRAFT, never approved); `ch13_q_vs_k` is not in V3 yet. None of it reaches a student under V3 until the instructor approves it or replaces it. His plan (12 Oct): four scenarios for equilibrium (two held by SCENARIO_CLAUDE, two more), one reserved worked, one reserved exam, two floaters.

The V2 scenarios were written to a different brief (one sentence, a sensor in every scene, every opener a 'sealed' something). The V3 brief (`docs/06_SCENARIO_CLAUDE_role.md`) asks for a scene a student has seen or felt, in short plain sentences, with the problem hidden until the particle account is given. The instructor (12–13 Oct): the V2 scenarios are kept as they are, and the sensor in every scene (the bridge from the macroscopic to the submicroscopic) continues in every new scenario.

## ICE tables (`ch13_ice`)

### V2's six openers, with their keyword cells

- A sealed clear soda bottle sits quiet, but a pressure sensor reveals gas molecules are escaping and redissolving at identical speeds without any net change in bubble size. What are the dissolved and gaseous carbon dioxide particles doing at the liquid boundary to preserve this motionless standoff?
  - keywords: rate, forward, reverse, dissolve, escape, equal
- A sealed jar of smelling salts maintains a sharp sting, yet a gas meter logs solid particles decomposing while vapor particles constantly recombine into solid. What are the solid and vapor particles doing during collisions that keeps their respective total amounts completely fixed?
  - keywords: equal, rates, decompose, recombine, constant, stoichiometry
- A sealed glass tube holds reddish-brown gas at a steady color tint, while an optical sensor shows dimeric pairs continually splitting and single molecules pairing up. What are the brown and clear gas particles doing during encounters to leave the visible tint perfectly stable?
  - keywords: equal, rates, dissociation, association, ratio, balance
- A bottle of salad vinegar tastes sour, but an ionization scanner shows only a tiny fraction of acid molecules ever yield ions while ions rapidly recombine. What are the intact acid molecules and separated ions doing in the solvent that prevents total ionization?
  - keywords: recombination, ionization, equal, rates, small, equilibrium
- A half-filled vintage perfume bottle never runs dry, as an ultrasonic sensor tracks liquid molecules continuously evaporating while vapor molecules crash back into the pool. What are the surface molecules doing on both sides of the interface to lock the liquid volume in place?
  - keywords: evaporate, condense, equal, rate, surface, vapor
- A cloudy fish tank water sample stops depositing white mineral crust, while an ion counter logs calcium ions precipitating as solid crystals simultaneously dissolve. What are the dissolved ions and solid mineral particles doing at the glass edge to halt further crust growth?
  - keywords: precipitation, dissolution, equal, rate, saturation, ions

### V2's milestones (the step map before V3's schema)
```
MILESTONES:
1. Laws and/or principles. A reasonable answer connects some of: the reaction runs until the forward and reverse processes go at the same pace, after which concentrations stop changing though both directions continue; everything changes in stoichiometric proportion, so a single unknown tracks all of it. The ICE table is bookkeeping for that one change.
2. Now that the problem is on screen, have them find the reaction quotient form in the Equations list, then iD stoichiometry shifts (-x, +2x).
3. Setup the Kc expression.
4. Solve for x and state the equilibrium concentrations.
5. Look back at their own result: ask them to compare the equilibrium concentrations they found with what they started with, and say what that shows about how far the reaction went before the forward and reverse rates matched. Do not assert what the size of K implies. The size of K alone does not fix the extent: that also depends on the starting concentrations, and in several of these problems a K well below 1 still converts a large fraction (0.100 M PCl5 with Kc = 0.025 is about 39% dissociated). A back-substitution check produces a number, not an account, so never make it the step-5 question.
```

### V2's watch list (the named errors)
Watch for: an inline fraction with an unbracketed denominator, x^2/0.1-x, which is a real error and not a typo; substituting initial concentrations into the equilibrium expression; and dropping the coefficient so that (2x)^2 is written as 2x^2 or as x^2.

Named errors carried into V3's scaffolding: `EXCEEDS_INITIAL` (x larger than what was there), `ORDER_OF_OPERATIONS` (x^2/0.1-x read as (x^2/0.1)-x), `SMALL_X_APPROXIMATION` (x dropped from the denominator where it is not small), `COEFFICIENT_NOT_SQUARED` (x where (2x) belongs), `INITIAL_IN_K` (K from initial concentrations).

### V2's six fixed problems (V3 kinds: findK, perfectSquare, quadratic)

- A 1.00 L flask is filled with 1.00 mol of H2 and 1.00 mol of I2. At equilibrium, the concentration of HI is 1.56 M. Calculate Kc for H2 + I2 <=> 2HI.
- For CO + H2O <=> CO2 + H2, Kc = 1.00 at 700 K. If initially 1.50 mol of CO and 1.50 mol of H2O are placed in a 2.00 L vessel, find equilibrium concentrations.
- For PCl5 <=> PCl3 + Cl2, Kc = 0.042 at 250 °C. Initially 0.80 mol PCl5 is in a 1.0 L container. Find equilibrium [Cl2].
- At a certain temperature, the equilibrium constant Kc for the decomposition of phosphorus pentachloride, PCl5(g) <=> PCl3(g) + Cl2(g), is 0.025. If the initial concentration of PCl5 is 0.100 M with no products present, what is the equilibrium concentration of PCl5?
- Initially, 0.500 M of N2O4 is placed in a reaction flask. At equilibrium, the concentration of NO2 is found to be 0.150 M. Calculate the equilibrium constant, Kc, for the reaction N2O4(g) <=> 2NO2(g).
- A mixture of 0.200 M H2 and 0.200 M I2 is allowed to reach equilibrium at a certain temperature. If the equilibrium constant, Kc, is 49.0 for the reaction H2(g) + I2(g) <=> 2HI(g), what is the equilibrium concentration of HI?

V3 step map as scaffolded (DRAFT): account_given → relation_chosen (pick) → the change row as a table → branch: find K | solve for x (perfect square | quadratic) → value_found → meaning_given → reflection. The `direction` kind was removed from this archetype on the instructor's instruction (10 Oct).

## Q versus K (`ch13_q_vs_k`)
### V2's six openers, with their keyword cells

- Injecting pure nitrogen and hydrogen into a heated tank produces no pungent ammonia initially, but a catalytic sensor detects gas molecules reacting instantly toward products. What are the colliding nitrogen and hydrogen particles doing in the absence of product to establish an initial forward surge?
  - keywords: forward, quotient, Q, less, K, collisions
- Blasting excess brown smog gas into a reaction chamber causes the reddish haze to bleach toward colorless gas, recorded by a density sensor. What are the crowded brown particles doing during mutual collisions that forces their total population to diminish spontaneously?
  - keywords: reverse, Q, greater, K, recombine, collide
- Opening an auxiliary chamber suddenly doubles the volume of a reacting gas mixture, and an optical meter records a rapid shift toward smaller molecules. What are the dispersed gas particles doing across the newly expanded space to drive this directional shift?
  - keywords: volume, Q, K, collisions, shift, particles
- Injecting extra reactant vapor into a balanced glass syringe causes a sensor to track a sudden net surge in product molecules. What are the newly added reactant particles doing among the original molecules to shatter the standstill and drive product formation?
  - keywords: forward, collisions, Q, below, K, reactant
- Chilling a condenser rapidly siphons off liquid ester from a fragrant mixture, and an infrared monitor shows starting acids vanishing faster than before. What are the remaining reactant particles doing in the thinned mixture to replenish the siphoned substance?
  - keywords: forward, remove, product, Q, below, K
- Filling a clean flask entirely with pure sulfur trioxide gas causes sulfur dioxide and oxygen to appear spontaneously on a gas sensor. What are the isolated trioxide particles doing among themselves to generate entirely new chemical species without any starting reactants present?
  - keywords: reverse, decompose, Q, infinite, K, reactants

### V2's milestones
```
MILESTONES:
1. Laws and/or principles. A reasonable answer connects some of: the same fraction of products over reactants can be evaluated at any moment, not only at equilibrium; comparing where it is now with where it must end up says which direction the reaction has to move; the shift is what changes the fraction until the two agree.
2. Now that the problem is on screen, have them find the Q expression in the Equations list, then substitute initial conditions into the Q expression.
3. Calculate the numerical value for Q.
4. Compare Q to K and predict the shift direction.
5. Account for what happens next: describe how Q changes as the reaction shifts, and explain what stops the shift. Connect the direction to the arithmetic of the fraction, not just to the rule.
```

### V2's watch list
Watch for: comparing Q with K correctly and then naming the shift direction backwards; and including pure solids or liquids in the expression.

Named errors in V2: `Q_INVERTED` (reactants over products), `COEFFICIENTS_AS_MULTIPLIERS` (coefficients multiplied in rather than used as exponents).

### V2's six fixed problems

- For H2 + I2 <=> 2HI, Kc = 54.3 at 430 °C. At a given moment, [H2] = 0.50 M, [I2] = 0.50 M, and [HI] = 3.0 M. In which direction will the reaction shift?
- For N2O4 <=> 2NO2, Kc = 0.211 at 100 °C. Initial analysis shows [N2O4] = 0.12 M and [NO2] = 0.055 M. Predict the shift direction.
- For 2SO2 + O2 <=> 2SO3, Kc = 280. If [SO2] = 0.020 M, [O2] = 0.010 M, and [SO3] = 0.050 M, determine Q and shift direction.
- At a certain temperature, the equilibrium constant Kc for the Haber process, N2(g) + 3H2(g) <=> 2NH3(g), is 10.0. A reaction mixture contains 0.50 M N2, 0.10 M H2, and 0.20 M NH3. Calculate the reaction quotient, Qc, to determine the direction the reaction will shift.
- The equilibrium constant Kc for the reaction 2SO2(g) + O2(g) <=> 2SO3(g) is 250 at a given temperature. If a flask is charged with 0.020 M SO2, 0.050 M O2, and 0.10 M SO3, calculate the reaction quotient, Qc.
- The synthesis of methanol, CO(g) + 2H2(g) <=> CH3OH(g), has an equilibrium constant Kc of 50.0 at a specific temperature. Calculate the reaction quotient, Qc, for a mixture containing 0.25 M CO, 0.40 M H2, and 0.80 M CH3OH.

In V3 this archetype would be: account_given → relation_chosen (the Q expression, a pick) → Q computed (a number) → direction_predicted (a pick: forward | reverse | no shift, checked deterministically against Q and K) → meaning_given → reflection. The `direction` kind exists in the shell for exactly this step.
