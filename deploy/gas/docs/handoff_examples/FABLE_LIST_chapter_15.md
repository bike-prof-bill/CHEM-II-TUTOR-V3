# Fable list, chapter 15 (SCENARIO_CLAUDE, 17 Oct 2026). Running list for the single send; everything is DRAFT until the instructor approves.

## Needs your decision (Fable)

Nothing yet.

## Engineering

1. **The rows,** staged for all four archetypes: openers (16 scenarios), the shared moves rows, scene rows, show cells and offer rows
   for the four worked scenarios, the named mistakes' notes and asks, and the problem sheets (96 problems). They replace your
   placeholder problems.
2. **`salts.json` changes:**
   - every Ksp was confirmed against the instructor's Appendix J;
   - new salts, from Appendix J: CaC2O4 (as the monohydrate, 1.96 × 10⁻⁹, 146.11 g/mol), AgI (1.5 × 10⁻¹⁶, 234.77), Ca(OH)2 (1.3 ×
     10⁻⁶, 74.09), Ag2CO3 (8.1 × 10⁻¹², 275.75), BaF2 (2.4 × 10⁻⁵, 175.32).
3. **Complexes:**
   - from the instructor's chapter 15 text: Ag(NH3)2+ 1.7 × 10⁷ (15.2), Ag(S2O3)2^3- 4.7 × 10¹³ (15.3, Example 15.16), Al(OH)4-
     1.1 × 10³³ (15.3);
   - Cu(NH3)4^2+: Appendix K gives 1.7 × 10¹³; your draft had 1.1 × 10¹³. Please correct it;
   - Fe(SCN)^2+ 8.9 × 10² matches Appendix K (unused so far);
   - Zn(NH3)4^2+ (2.9 × 10⁹ in your draft) is not in Appendix K; unconfirmed and unused.
4. **Carets in tutor text:** your placeholder problem sentences ("10^-10") and the complex archetype's `park_text` ("x)^2") put
   carets outside `\( \)`. The new problem sentences are clean; the park_text needs your fix.
5. **Simulation addresses.** Two pages; `mode` is fixed in each opener row:
   - `ch15/solubility_simulator.html?mode=dissolve|common|mix&salt={salt}&common={common}&c_common={c_common}&c_cat={c_cat}&c_an={c_an}&theme={theme}`;
   - `ch15/complex_simulator.html?complex={complex}&C={C}&L={L}&theme={theme}`.
6. **Ion display forms:** `{cation}` and `{anion}` filled from `salts.json` would show carets ("SO4^2-") in tutor text; please keep a
   display form for each ion.
7. **The solubility unknown is x, not s** (the instructor's ruling, 17 Oct 2026), to match the OpenStax text (Examples 15.4 and 15.6). All
   SCENARIO_CLAUDE wording in `ch15_ksp` and `ch15_common_ion` now says x, "x, the molar solubility". Your code's student-facing labels
   still say s, for example the expected-item label "s (the molar solubility)", and should change to x. Internal ids (`s_found`,
   `s_from_ksp`) can stay. The shell already reads s and x as the same unknown.
8. **Both pages are approved** (instructor, 17 Oct 2026; files checked by SCENARIO_CLAUDE: the Appendix J and K constants, no network calls):

   | page | SHA-256 | placeholders |
   |---|---|---|
   | `media/ch15/solubility_simulator.html` | afabb987c94f1c9fe42ce0449ff1b4e1def831571f211ecfe42dca4f56d273d4 | `mode`, `salt`, `common`, `c_common`, `c_cat`, `c_an`, `v_cat`, `v_an`, `theme`; `Ksp` ignored |
   | `media/ch15/complex_simulator.html` | 25646c2ba60c65173f10f3980dca1617585db0d914b4f491ffc47248e4337150 | `complex`, `C`, `L`, `theme`; `Kf` ignored |

9. **Media:** sixteen chapter 15 pictures, held with their register rows (`MEDIA_SOURCES_rows_ch15_*_pictures.csv`) and the openers' picture
   cells filled. Chapter 15 is complete: four archetypes, sixteen scenarios, 96 problems, two pages and sixteen pictures, all approved.
