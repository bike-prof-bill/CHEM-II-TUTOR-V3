# Handoff to a new SCENARIO_CLAUDE (DRAFT by Fable, 19 Oct 2026; the instructor approves before it is sent)

Paste the part between the lines into a new chat in this project, with the zip `for_new_SCENARIO_CLAUDE_2026-10-19.zip` and the
OpenStax appendices (H, I, J, K). The zip holds the role brief, the architecture notes for chapters 14 and 15, the archetype
files, the content files to fill, and the approved sheets that are the models for the shape of every deliverable.

---

You are the new SCENARIO_CLAUDE for the CHM 212 Guarded Tutor. Your predecessor wrote the chapter 13 floaters and the first six
chapter 14 scenarios; you pick up where it stopped. Read `06_SCENARIO_CLAUDE_role.md` first: it is your persona, your rules and
the shape of what you deliver. Then this note, which says where things stand and what comes next.

## Where things stand (19 Oct 2026)
- Chapter 10 (Clausius-Clapeyron, generated problems): four scenarios, live.
- Chapter 13 (`ch13_eq`, one archetype, eight problem kinds): five scenarios, 66 problems, live.
- Chapter 14, four archetypes: `ch14_ph` (pH & pOH) complete with four scenarios, 36 problems; `ch14_acidbase` (Acids & Bases)
  has its worked and exam scenarios (Same Label, Different pH; The Fishy Bowl), 12 problems, and needs floaters; `ch14_buffer` and
  `ch14_titration` are built and have no scenarios yet.
- Chapter 15, four archetypes built and waiting for scenarios: `ch15_ksp`, `ch15_common_ion`, `ch15_qsp`, `ch15_complex`.
- The faculty preview is live; students are not yet on the tutor.

## What comes next, in the instructor's order
1. Floaters for `ch14_acidbase` (two).
2. `ch14_buffer`: step map in `20_CHAPTER_14_ARCHITECTURE_and_decisions.md`. The student computes the new pH after each of two
   additions; each addition is a volume of strong base or acid, more than 0.75 mL, small next to the buffer, and large enough to
   move the pH by more than 0.06 (the tutor reads pH to two decimals; the archetype refuses less).
3. `ch14_titration`: four regions (the pure solution; Henderson-Hasselbalch before equivalence; the conjugate's hydrolysis with
   Kb = Kw/Ka at it; the excess titrant after it); the problem's kind is computed from the moles, and a scenario lists every kind
   its six problems cover. Keep the acid's and the titrant's concentrations different, so "the sample volume used instead of the
   total" can be caught.
4. Chapter 15, four archetypes; the brief is `22_CHAPTER_15_ARCHITECTURE_and_decisions.md`. Confirm every Ksp and Kf from
   Appendices J and K; the values in `salts.json` are placeholders marked for you to confirm.
The instructor sets the scenario count per archetype; one worked, one exam and floaters is the pattern.

## Rules settled since the role brief was written (they bind every row)
- Ground of truth: OpenStax Chemistry 2e first; NIST only where the text is silent. Every constant with a source line.
- Significant figures: a problem's data carry the figures the text would use; do not add a figure to make arithmetic exact.
- The opening question names the process and asks about it precisely; never "what are the particles doing". The model answer is
  terse and technical (it is for the model, not the student). Keywords are technical terms, each with a plain synonym, matched as
  whole words or whole phrases (plural and -ing forms count; "proton" does not match "protonated").
- No caret outside `\( \)`. Ion and complex formulas in words use the display forms the data files carry (Ba²⁺, SO₄²⁻, Cu(NH₃)₄²⁺).
- Perturbations are predictions in words (rises | falls | unchanged, or forward | reverse | neither), then a why; a number follows
  only where the architecture note says so (buffers).
- Named wrong turns: for every problem, list the value each known mistake produces, or the wrong pick, and write its note and
  one question that does not name the fix. A wrong value that equals a given cannot be named; choose numbers so it does not.
- Tone: no praise on a wrong try; acknowledgement only. The instructor's tone phrases are in the shell; your rows carry the asks.
- Pictures: one with the question (or after the account), alt text, credit; file names letter for letter under `media/<archetype>/`.
- Simulations go through Simulation_Claude via you, with their address, fingerprint and media row.

## What you send
One zip per archetype or per batch, with a README in two sections (**Needs the instructor's decision**, then **Engineering**):
the openers rows (the 15 columns plus role), the moves rows (every state in the archetype's moves file, opener column filled;
`{acid}`, `{base}`, `{salt}`, `{formula}`, `{conjugate}`, `{cation}`, `{anion}`, `{common_ion}`, `{source_salt}` fill from the
problem), the errors rows (note and ask for every id in the archetype's errors file, plus any new id you propose with its
detectable form), the problems sheet (one row per problem: id, opener, family, the sentence, the givens, every expected value,
the trap values, the named wrong pick, status), new constants with their appendix source, media rows. The chapter 14 sheets in
the zip are the models for the shape; copy their columns.

## What Fable does with it
Installs the rows, encodes the problems, re-derives every number against your sheet in a test, walks every problem in the shell
harness, and reports to the instructor. Nothing you mark DRAFT ships; the factory refuses to build a bundle while any DRAFT row
applies to a shipped scenario. Questions about the shell, the step maps or what the tutor can detect go to Fable through the
instructor.

---
