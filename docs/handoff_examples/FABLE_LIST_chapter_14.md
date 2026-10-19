# Work saved for Fable: chapter 14 (running list, kept by SCENARIO_CLAUDE)

Started 15 Oct 2026 on the instructor's instruction: Fable is contacted once, when the chapter 14 archetype sequence is finished.
Each item says what to build and which approved rows depend on it. When the time comes, this list becomes the README of a single
zip with every staged row.

## Needs your decision

Nothing now. `ch13_eq_three_floaters_for_Fable.zip` was rebuilt on 16 Oct with the repaired page fingerprints. It travels with this
list unless the instructor sends it sooner.

## Engineering

### pH & pOH (`ch14_ph`): "Off the Scale" (floater, approved 15 Oct)
1. **Moles and volume as givens (N6a–N6c, barium hydroxide).** Each problem gives moles in 0.500 L. The archetype takes only a
   concentration today. Needed: givens `n` and `V`; ion_found = n / V × ions per formula. Then the formula concentration is not a
   given, and IONS_PER_FORMULA_IGNORED can be caught.
2. **Five new named mistakes** (approved), all values. The trap values are in the problems sheet.

   | error | where | the value the tutor sees |
   |---|---|---|
   | PH_SIGN_DROPPED | N1, pH_found | −pH (the pH is below zero) |
   | POH_SIGN_DROPPED | N5, pOH_found and pH_found | −pOH; 28.00 − pH |
   | LN_FOR_LOG | pH_found, all problems | the pH from the natural logarithm |
   | DILUTION_AWAY_FROM_7 | perturb_1 | named wrong pick: "falls" for an acid, "rises" for a base (the archetype passes no named picks today) |
   | MOLES_NOT_CONCENTRATION | N6, ion_found | the moles typed as M |

3. **Shared moves rows.** The nine base rows are written to be shared by every pH scenario. Two override rows (account_given,
   meaning_given) belong to this opener. The ion_found ask uses `{substance}` and `{formula}`.
4. **Simulation address.** `ch14_ph/off_the_scale_simulator.html?strong={strong}&c={c}&theme={theme}`. These follow your
   sim_params; `strong` and `c` are new placeholders. For N6, `c` is the formula concentration.
5. **Media:** register rows for the picture and the page follow when the instructor approves them.

### pH & pOH: "The Corn Soak" (worked, approved 15 Oct), "The Stockroom Morning" (floater, approved 15 Oct), "Concrete Burn" (exam, DRAFT)
6. **Calcium hydroxide** joins `acids_bases.json` → strong. Entry: name "calcium hydroxide", kind base, ions_per_formula 2.
   Source: OpenStax Table 14.6 (strong bases) and Exercise 18(d). Note the ceiling: Appendix J, Ksp 1.3 × 10⁻⁶, about 0.0069 M saturated. Problems stay
   below it.
7. **Show cells with two versions** for the worked scenario ("one hydroxide": NaOH; "two hydroxides": Ca(OH)₂), plus an offer
   row, as in the Martian moves file.
8. **Moles and volume as givens** (item 1) also cover W1, W2, W5, R1, R2, R3 and all six exam problems, E1–E6.
9. **Simulation pages.**
   - `off_the_scale_simulator.html`, third version: approved 16 Oct 2026, repaired the same day (SHA-256 now 803bd330; see item 15). It has a slider from 1.0 × 10⁻⁴ M
     to each substance's ceiling and a substance menu. It serves Off the Scale, the Stockroom Morning and Concrete Burn.
   - `corn_soak_simulator.html`: approved 16 Oct 2026, repaired the same day (SHA-256 now 6eae2cbf; see item 15). Placeholders `strong`, `c`, `theme`, as on Off the Scale.
     Accepted: the drawing rule for the scarce ion and the even middle of the slider.

### Acids & Bases (`ch14_acidbase`): "Same Label, Different pH" (worked, approved 16 Oct)
10. **Data corrections in `acids_bases.json`, against the Appendix H the instructor supplied:**
    - hydrofluoric acid 7.2 × 10⁻⁴ → 6.4 × 10⁻⁴;
    - nitrous acid 4.5 × 10⁻⁴ → 4.6 × 10⁻⁴;
    - new: formic acid, HCOOH, Ka 1.8 × 10⁻⁴ (Appendix H).
11. **The placeholder problems W1–W3 and B1–B2 in `ch14_acidbase.py`** are replaced by K1–K6. W1's "household vinegar is about
    0.10 M" is wrong: 5 % vinegar is about 0.8 M (Exercise 62).
12. **Show cells with two versions,** "holds" and "fails", plus an offer row.
13. **The shared moves rows** use `{substance}` and `{conjugate}`.
14. **Simulation:** `ch14_acidbase/weak_acid_base_simulator.html?species={species}&c={c}&theme={theme}`, now the two-amine version,
    SHA-256 444fc0c53097329c5575d44245146f3479c7a13ab0ce8d127c136e417124e40e (checked by SCENARIO_CLAUDE; approved by the instructor 16 Oct 2026). It replaces 6119d977. `c` runs from 1.0 × 10⁻⁵ to 2.0 M; the page ignores `K` and uses its own
    Appendix H/I table. `species` and `c` are new placeholders for this archetype. If the archetype holds a concentration range,
    widen it to match.
15. **Pages repaired for a Safari fault** (Pause ignored), 16 Oct 2026. SCENARIO_CLAUDE checked each against its approved version:
    only the screen-writing code changed, no chemistry. New SHA-256:

    | page | was | now |
    |---|---|---|
    | `off_the_scale_simulator.html` | 6454711d | 803bd330d922e2aeb1112127df9656ddf7fbbbdcbee007e39baff2cc7df9c5ec |
    | `corn_soak_simulator.html` | 02ee8929 | 6eae2cbf3de464732d00385391f0cd268294ff96ff3d63fe9a9fa3301cf815a9 |
    | `weak_acid_base_simulator.html` | 6119d977 (built with the fix; that file never reached SCENARIO_CLAUDE) | 444fc0c53097329c5575d44245146f3479c7a13ab0ce8d127c136e417124e40e (two amines added; checked; approved 16 Oct) |

    The three chapter 13 pages, and the Haber-Bosch and Martian pages (`ch13_ice`), are updated inside the rebuilt
    `ch13_eq_three_floaters_for_Fable.zip`. The chapter 10 pages are done too: syringe, drinking bird and deep-sea vent repaired and approved
    (in the same zip); the alcohol page needed no repair (no running loop, no buttons) and stays at 07adade5.

### Acids & Bases: "The Fishy Bowl" (exam, approved 16 Oct)
16. **New bases in `acids_bases.json`** (Appendix I):
    - trimethylamine, (CH3)3N, conjugate (CH3)3NH+, Kb 6.3 × 10⁻⁵;
    - dimethylamine, (CH3)2NH, conjugate (CH3)2NH2+, Kb 5.9 × 10⁻⁴.
17. **POH_TYPED_AS_PH for weak bases** (approved 16 Oct): the pOH typed at pH_found. Its row is in `content_ch14_acidbase_errors.csv`, and the
    value is in the sheet.
18. **The exam's six problems all hold the 5 % rule,** an exception to "at least one fails per scenario" (approved 16 Oct).

### Buffers (`ch14_buffer`): "The Stubborn Beaker" (worked, approved 17 Oct)
19. **The rows replace your placeholders F1–F2.** Opener, shared moves rows, show cells ("equal", "unequal"), offer row, the five
    named mistakes' notes and asks, and problems B1–B6.
20. **Simulation:** `ch14_buffer/buffer_simulator.html?species={species}&ca={ca}&cb={cb}&V={V}&theme={theme}`, approved 17 Oct 2026,
    SHA-256 7c6137bcc94d3ce4801caad2203747f175cada0dbb3c2976f401b180bf538b5d. A change brief adds three species (blood, phosphate,
    ammonium), so this fingerprint will be replaced. `ca`,
    `cb` and `V` are new placeholders; `species` exists.
21. **Placeholder problems in your files used carets in student text** ("Ka = 1.8 × 10^-5"). The replacements use `\( \)`.

22. **"The Sprint"** (buffer exam, approved 17 Oct). It needs a blood entry in `acids_bases.json`: carbonic acid at body temperature,
    pKa 6.1 (Ka = 10⁻⁶·¹ = 7.9 × 10⁻⁷). Source: OpenStax 14.6, How Sciences Interconnect: The Buffer System in Blood, with
    [H₂CO₃] about 0.0012 M and [HCO₃⁻] about 0.024 M. Keep it separate from Appendix H's carbonic acid at 25 °C (4.3 × 10⁻⁷). Its
    problems S1–S6 are in `ch14_buffer_problems_sprint.csv`. The buffer page needs this species too.

23. **Buffer floaters** (approved 17 Oct): "The Eye Drops" (phosphate, P1–P6) and "Half a Buffer" (ammonia/ammonium, A1–A6).
    New data:
    - dihydrogen phosphate as an acid, Ka 6.2 × 10⁻⁸ (Appendix H);
    - the ammonium ion as an acid, Ka = Kw ÷ Kb = 5.6 × 10⁻¹⁰. In the archetype, ca is the acid partner (NH₄Cl) and cb the base partner (NH₃).
24. **New named mistake KB_USED_AS_KA** (approved 17 Oct): pH = pKb + log(ratio) for a basic buffer, at pH_found and pH_after_n. Its row is
    in `content_ch14_buffer_errors.csv`.

25. **Current chapter 14 page versions** (17 Oct 2026). These supersede the fingerprints above once the instructor approves them:

    | page | SHA-256 | what changed |
    |---|---|---|
    | `ch14_ph/off_the_scale_simulator.html` | 6b5481970a0d6eeaa2b5413a359aa930db71203d5b93ea4cfdba32e8ce767895 (approved 17 Oct) | scale labeled 0, 7, 14; quick start; dilution caption; formulas fit their labels |
    | `ch14_acidbase/weak_acid_base_simulator.html` | f494309a8bf4509e794f399846101b60e3966d4b414ef838bf155a15bac5c1ce (approved 17 Oct) | the same scale; quick start ("the partner"); salt caption; hypochlorite and acetate added; formulas fit their labels |
    | `ch14_buffer/buffer_simulator.html` | 98b62a534ab65acc1a2fd7f1ccd4947ffb2a3a45e75d0f11bc3ce32a2d5acd71 | blood, phosphate and ammonium added; 0.10 M strength; quick start; the same scale |

    Chemistry values are unchanged; SCENARIO_CLAUDE checked the files.

26. **Acids & Bases floaters** (approved 17 Oct): "The Weak Acid That Eats Glass" (H1–H6) and "The Bleach Puzzle" (C1–C6), in
    `ch14_acidbase_problems_glass_and_bleach.csv`. New bases for `acids_bases.json`, each with Kb = Kw ÷ Ka (Appendix H; 14.3):
    hypochlorite 3.4 × 10⁻⁷; acetate 5.6 × 10⁻¹⁰. The Bleach Puzzle overrides perturb_2's wording ("a little
    hypochlorous acid is added"), since the shared "a salt containing …" does not fit an acid partner.
27. **New step `Kb_found`** (approved 17 Oct). For a weak-base problem that gives Ka of the partner acid (C1–C4, C6), the student finds
    Kb = Kw ÷ Ka as a number, checked before the expression is set. Suggested named mistake: Ka typed as Kb (KA_USED_AS_KB).

28. **Titrations: "The Vinegar Lab"** (worked, approved 17 Oct). Opener, the shared rows for all 19 states, show cells ("weak",
    "strong"), offer row, notes and asks for the 13 named mistakes, and problems V1–V6 (`ch14_titration_problems_vinegar_lab.csv`). The
    shared meaning question asks about choosing an indicator. Simulation: `ch14_titration/titration_simulator.html?species={species}&pair={pair}&ca={ca}&va={va}&cb={cb}&vb={vb}&theme={theme}`
    (brief sent 17 Oct). `species` names the weak acid; the others are your sim_params.

29. **Titrations: "The Kombucha Check"** (exam, approved 17 Oct). The opener is the instructor's own wording. Six versions, all at
    equivalence: a 20.00 mL aliquot, 0.0300–0.0450 M acetic acid, 0.100 M NaOH (K1–K6, `ch14_titration_problems_kombucha.csv`).

30. **Titration floaters** (approved 17 Oct): "The Stockroom Standard" (S1–S6, strong acid before, at and after) and "The Sour Whey"
    (W1–W6, lactic acid, all four regions, W5 at halfway), in `ch14_titration_problems_floaters.csv`. Lactic acid is new to
    `acids_bases.json`: Ka 1.36 × 10⁻⁴, from OpenStax Exercise 63. Chapter 14 is complete: four archetypes, sixteen scenarios.

31. **Titration page:** `ch14_titration/titration_simulator.html`, approved by the instructor 17 Oct 2026, SHA-256
    6125425113b14df868b54e5cbce02bd5f5759dad29f829de7b3be06e7b220f94 (file received and checked by SCENARIO_CLAUDE). It replaces bbf77fa1 and adds captions, a quick start, burette drops and a curve that draws as the
    student goes. Placeholders: `pair`, `species` (acetic, lactic, HCl), `ca` (0.0010 to 2.00 M), `va`, `cb` (0.0010 to 1.000 M), `vb`, `theme`.


### Carried from chapter 13 (already in `ch13_eq_three_floaters_for_Fable.zip`)
- The inherited Haber-Bosch moves rows carry carets outside `\( \)`.

### Next
- Simulation plan (instructor, 16 Oct 2026): four pages for chapter 14, reused through their addresses.
  - Off the Scale: strong acid or base.
  - Corn Soak: water's two ions.
  - A weak acid or base page, built from Off the Scale.
  - One page extended first for buffers and then for titration.

  New addresses may need new placeholders; they will be listed here as they arise.
- The other `ch14_ph` scenarios, then Acids & Bases, Buffers and Titration: items are added here as they arise.
