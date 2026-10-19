# Fable list, chapter 16 (SCENARIO_CLAUDE, 18 Oct 2026). Running list for the single send; all five archetypes approved by the instructor, 18 Oct 2026.

## Needs your decision (Fable)

1. **Five new archetypes,** designed by SCENARIO_CLAUDE in the pattern of chapters 13–15, because you were away. Step ids, expected
   values, trap values and right picks are in each problem sheet. Please build to them, or tell the instructor where the design
   doesn't fit the shell:

   | id | archetype |
   |---|---|
   | `ch16_entropy` | entropy and spontaneity |
   | `ch16_free_energy` | free energy calculations |
   | `ch16_spontaneity` | free energy and spontaneity |
   | `ch16_equilibrium_G` | nonstandard free energy and phase equilibrium |
   | `ch16_G_and_K` | free energy and K |

## Engineering

1. **Data:** Appendix G (OpenStax), parsed in full. Ice uses OpenStax Example 16.4's values, since Appendix G has no entry for ice.
   R = 8.314 J/(mol·K); T = 298 K unless stated. Energies are in kJ; ΔS is in J/K, converted for ΔG.
2. **New pick kinds:**
   - `sign_pick` (positive or negative);
   - `case_pick` (always, never, low, high);
   - `direction` (forward, reverse, equilibrium, with |ΔG| < 0.2 kJ counted as equilibrium);
   - `favored` (products, reactants, neither).
3. **Named mistakes,** listed per archetype in the errors files:
   - PRODUCTS_REACTANTS_SWAPPED, COEFFICIENTS_DROPPED, J_FOR_KJ, KJ_NOT_CONVERTED, J_KJ_MISMATCH;
   - CELSIUS_FOR_KELVIN, KELVIN_AS_CELSIUS, SURROUNDINGS_SIGN, TDS_SIGN, COUPLED_SUBTRACTED;
   - Q_INVERTED, LOG_FOR_LN, STANDARD_FOR_NONSTANDARD, SIGN_DROPPED;
   - pick mistakes: SIGN_PICK_WRONG, SPONTANEITY_FROM_SYSTEM, EXTENSIVE_IGNORED, CASE_WRONG.
4. **Pages** (briefs sent to the new SIMULATION_CLAUDE):

   | page | placeholders |
   |---|---|
   | `ch16/entropy_simulator.html` | `process`, `T`, `theme` |
   | `ch16/free_energy_simulator.html` | `reaction`, `T`, `theme` |
   | `ch16/G_and_Q_simulator.html` | `reaction`, one parameter per species, `theme` |

5. **An Appendix G inconsistency:** calcite's ΔH°f and S° don't match its ΔG°f (the two routes differ by 66 kJ for CaCO₃ → CaO + CO₂).
   Calcite is kept out of the two-route problems.
6. **Approved with the archetypes:**
   - the limestone kiln kept with Appendix G's 1350 K crossover;
   - |ΔG| < 0.2 kJ counted as "at equilibrium";
   - iodine's sublimation in the exam;
   - "Kp, standard states 1 bar" for K from ΔG°;
   - Appendix H's Ka values used to find ΔG° from K.
7. **Pictures:** 19 of 20 held in `media/ch16/`, with register rows (`MEDIA_SOURCES_rows_ch16_*_pictures.csv`) and opener cells filled.
   Two were retouched by SCENARIO_CLAUDE, with the instructor's approval (18 Oct): the Haber Revisited board, and the Solvent Shelf
   caption. "Water Boils at 97 °C?" passed on its third try, so all 20 are now held.
8. **Pages, approved by the instructor 18 Oct 2026** (files checked by SCENARIO_CLAUDE: fingerprints match, data in hundredths agree
   with Appendix G, calcite's ΔG°f shown as "—", no network calls). The header comments still read DRAFT; the approval is recorded in
   SIMULATION_CLAUDE's handoff.

   | page | SHA-256 |
   |---|---|
   | `media/ch16/entropy_simulator.html` | 5dbf18b48604a42823bd8af533e0793d33331fd9365c3a8255dae0e941d45210 |
   | `media/ch16/free_energy_simulator.html` | 7fe001a09c83aeabda6ef3f76a29fd400ba0257fd57827eb6d6e6a4103ecda64 |
   | `media/ch16/G_and_Q_simulator.html` | 3d842e35caf6a9d05195d724aa2271fd7febce0cb55f09108738f35316343901 |

   Placeholders:

   | page | placeholders |
   |---|---|
   | entropy | `process`, `T`, `theme` |
   | free energy | `reaction`, `T`, `theme` |
   | ΔG and Q | `reaction`, one parameter per species, `theme` |

   Chapter 16 is complete: five archetypes, twenty pictures, three pages.
