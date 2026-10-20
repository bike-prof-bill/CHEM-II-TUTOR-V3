# Fable list, chapters 19 and 21 (SCENARIO_CLAUDE, 18 Oct 2026). For the single send; all approved by the instructor, 18 Oct 2026.

## Needs your decision (Fable)

1. **Three new archetypes,** designed by SCENARIO_CLAUDE in the pattern of chapters 13–17. Step ids, expected values, trap values
   and right picks are in each problem sheet (`Ch19_Ch21_package/rows/`).

   | id | chapter | archetype |
   |---|---|---|
   | `ch19_cft` | 19 | crystal field splitting |
   | `ch21_decay` | 21 | radioactive decay and half-life |
   | `ch21_binding` | 21 | nuclear binding energy |

2. **The "+" in crystal field ids must be sent encoded:** `complex=Fe(H2O)6_2%2B`. The page also reads a space as "+".

## Engineering

1. **Data:**
   - OpenStax chapters 19 and 21 and Appendix M;
   - Cr(III) absorption wavelengths and colours from the instructor;
   - 21 isotope masses from NIST, confirmed by the instructor;
   - the textbook's particle masses (1.0073, 1.0087, 0.00055 amu).
2. **Tolerance:** ±1% on these answers (instructor).
3. **Pages, approved by the instructor 18 Oct 2026** (fingerprints and data checked by SCENARIO_CLAUDE; no network calls):

   | page | SHA-256 | placeholders |
   |---|---|---|
   | `media/ch19/crystal_field_simulator.html` | 860f2b1619fbe6f2cee065137d0f52431a5a4253a837f46353c6ac031d39b63e | `complex`, `field`, `theme` |
   | `media/ch21/decay_simulator.html` | f482ed304bb0039f1609532d670b5c4c0618294323b4974881600b39d120c5df | `mode`, `isotope`, `t`, `ratio`, `m0`, `parent`, `gp`, `gd`, `theme` |
   | `media/ch21/binding_energy_simulator.html` | 11fd5489687a33c56b933e15bb1fe92c6d033584a62fe3b725ed141d9b3a7ff6 | `nuclide`, `arrows`, `theme` |

   Mass-left checks need `m0` in the address (CS5 and HI1–HI6). The binding page's arrows default to on.
4. **Crystal field page changes approved with it:**
   - the magnet view replaced by a colour view, since the course has no measured magnetic moments;
   - ten complexes carry the instructor's seen and absorbed colours (check rows IC1–IC10), five of them new to the page
     (`Cu(H2O)6_2+`, `Cu(NH3)4_2+` square planar, `Co(H2O)6_2+`, `Ni(H2O)6_2+`, `Ni(NH3)6_2+`). The instructor may revise them later.
5. **Media:** twelve pictures and three pages held in `media/ch19/` and `media/ch21/`, with register rows and opener cells filled.
   Chapters 19 and 21 are complete.
