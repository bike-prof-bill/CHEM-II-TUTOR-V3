# Handoff to SCENARIO_CLAUDE: chapter 15 (DRAFT by Fable, 16–17 Oct 2026; the instructor approves before it is sent)

Paste the part between the lines into the SCENARIO_CLAUDE chat with `docs/06_SCENARIO_CLAUDE_role.md`, the four archetype files
(`archetypes/ch15_ksp.py`, `ch15_common_ion.py`, `ch15_qsp.py`, `ch15_complex.py`), `archetypes/_solubility.py`,
`archetypes/data/salts.json` and Appendices J and K from the instructor.

---

Chapter 15 is four archetypes: `ch15_ksp` (Ksp and molar solubility, two kinds: Ksp given, or solubility in grams per litre
given), `ch15_common_ion` (two kinds: the common ion is the cation or the anion), `ch15_qsp` (will a precipitate form on mixing;
the kind is computed from the numbers), `ch15_complex` (the free metal ion left when a ligand in excess binds it). The step maps, item ids and named wrong turns are in
`docs/22_CHAPTER_15_ARCHITECTURE_and_decisions.md`; read it first. The rules you know hold: a sensor in every scene (a turbidity
probe, a conductivity probe, an ion-selective electrode, a balance); the problem hidden until the particle account; fixed
problems, six per scenario across the families; every constant with its source, Appendix J first; plain text, no caret outside
`\( \)`; roles (the instructor assigns).

## Per problem (one row each; the archetype computes every number)
- `ch15_ksp`: the salt (from `salts.json`, or a new one with its Appendix J value and molar mass), and either Ksp or the grams per
  litre; the sentence. Expected: s, the ion that forms more than once per unit, grams per litre or Ksp. Mix 1:1, 1:2 and 2:1 salts
  across the six.
- `ch15_common_ion`: the salt, which ion is common, its concentration and the salt that supplies it; the sentence. Expected: s with
  the common ion, s in pure water, the ratio, whether small-s holds. Choose at least one problem where it does not.
- `ch15_qsp`: the salt, the two solutions (concentration and volume of each); the sentence. Expected: both concentrations after
  mixing, Qsp, the verdict. Use unequal volumes in some problems so "the other solution's volume" can be named, and keep Q away
  from Ksp by more than a factor of two so the verdict is clear.
- `ch15_complex`: the complex (from `salts.json`'s complexes, or a new one with its Appendix K Kf), the metal and ligand solutions
  (concentration and volume of each; the ligand in excess). Expected: the complex and the ligand left after complete formation,
  Kd, the free metal ion, how many times smaller than before. Choose at least one problem with a small Kf where dropping x fails.
- The s table has two columns, the two ions; the solid is present and has no column. Students may write s or x.

## Rows to write
Openers (question, model answer, keywords: ion, lattice, dissolve, settle, equal rates, saturated, collide; label words: Ksp,
solubility, saturated, precipitate, equilibrium; picture, simulation and media rows). Moves: the states are listed in each
archetype's moves file, all DRAFT; `{salt}`, `{formula}`, `{cation}`, `{anion}`, and for the common ion `{common_ion}` and
`{source_salt}`, fill from the problem. Errors: each archetype's errors file lists its ids with the detectable form.

## Send
One zip per archetype, or one for all four: openers, moves, errors, the problems sheet, new salts and complexes with their Appendix J or K source (and molar mass for salts), media rows.

---
