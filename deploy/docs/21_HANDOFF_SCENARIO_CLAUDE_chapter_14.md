# Handoff to SCENARIO_CLAUDE: chapter 14 (approved by the instructor, 15 Oct 2026)

Paste the part between the lines into the SCENARIO_CLAUDE chat with `docs/06_SCENARIO_CLAUDE_role.md`, the four archetype files
(`archetypes/ch14_ph.py`, `ch14_acidbase.py`, `ch14_buffer.py`, `ch14_titration.py`) and the OpenStax appendices from the instructor.

---

Chapter 14 is four archetypes, one per concept: `ch14_ph` (pH & pOH: strong acids and bases), `ch14_acidbase` (Acids & Bases:
weak acids and bases), `ch14_buffer` (Buffers), `ch14_titration` (Titration). Each has its own openers, moves and errors files and
its own scenarios. The step maps, item ids and named wrong turns are in `docs/20_CHAPTER_14_ARCHITECTURE_and_decisions.md`; read it
first. The rules you know hold: a sensor in every scene (here a pH probe or an indicator); the problem hidden until the particle
account; fixed problems, six per scenario across the families; every constant with its source, OpenStax first (Appendix H for Ka,
Appendix I for Kb; the instructor gives you the appendices); plain text, no caret outside `\( \)`; roles (the instructor assigns).

## Scenarios
The instructor sets the count per archetype; the minimum is one each. Scenes with a probe in them: a fish tank or pool (pH & pOH,
buffers), vinegar or a soft drink (weak acid), window cleaner or a fish-market smell (weak base), blood or a swimming pool's
alkalinity (buffer), an acid-base titration in a lab or a brewery (titration).

## Per problem (the sheet, one row each; the archetype computes every number from these)
- `ch14_ph`: the strong acid or base (HCl, HNO3, NaOH, KOH, Ba(OH)2), its concentration, the sentence. Expected: the ion
  concentration, pH, pOH; the dilution answer (acid: pH rises; base: falls).
- `ch14_acidbase`: the acid or base (from `acids_bases.json`, or a new one with its appendix value), the concentration. Expected:
  x, (pOH), pH, percent ionised, whether the 5 % rule holds (so the method is small-x or the quadratic): at least one problem per
  scenario where it fails. Perturbations: dilution (percent rises) and the conjugate salt (acid: pH rises; base: falls).
- `ch14_buffer`: the acid, both concentrations, the buffer's volume, and two additions: a volume and concentration of strong base,
  and of strong acid, each more than 0.75 mL and small next to the buffer, and each moving the pH by more than 0.06 (the tutor
  reads pH to two decimals). Expected: ratio, pH, the two predictions (base: rises; acid: falls) and the two new pH values.
- `ch14_titration`: the acid (weak, from the file, or a strong one), its concentration and volume, the titrant's concentration
  and the volume added. The archetype works out the region from the moles; the problem's kind is `weak_start`, `weak_before`,
  `weak_at`, `weak_after`, `strong_before`, `strong_at` or `strong_after`, and the scenario's kinds column lists every kind its six
  problems cover. Avoid equal concentrations of acid and titrant if you want "the sample volume used instead of the total" to
  be caught: with equal concentrations that wrong value equals a given and the tutor cannot name it.

## Rows to write
Openers (question, model answer, keywords: proton, transfer, water, hydronium, hydroxide, equal rates, fraction, excess; label
words: acid, base, pH, buffer, equivalence, neutral; picture, simulation and media rows). Moves: the states are listed in each
archetype's moves file, all DRAFT; the perturbation rows name the change in the scene's words; `{acid}`, `{base}`, `{formula}`,
`{conjugate}`, `{substance}` fill from the problem. Errors: each archetype's errors file lists its ids with the detectable form;
write the note and the ask.

## Send
One zip per archetype, or one for all four: openers, moves, errors, the problems sheet, new constants with their appendix source,
media rows.

---
