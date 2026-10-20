# Chapter 13 (ch13_ice): the two scenarios, complete in one zip (13 Oct 2026)

From SCENARIO_CLAUDE. This answers your directive item by item. Everything is approved by the instructor.

| You asked for | File | Notes |
|---|---|---|
| The two opener rows (15 columns plus role) | `ch13_openers.csv` | Haber-Bosch: role **exam**. Martian Fuel: role **worked**. These are for now; they will change when the next two scenarios arrive. They replace V2 openers 1–6. |
| Their keyword lists | in the openers (column 5), with label words in column 13 | The chapter's vocabulary added; "dynamic equilibrium" is a label word. |
| Moves rows, with show cells for the worked one and the offer row | `ch13_moves.csv` | Columns as in ch10 plus `show` and `version`. A blank cell in an opener row means use the archetype row. Martian show cells: version `equal` (the worked problem) and `unequal` (the offer: the SAME problem with the steam changed, so the starts differ). Rows carrying only `show`/`version` add the show cell to that item. The offer row comes after the reflection. |
| Named errors, with any new trap | `ch13_errors.csv` | Ten errors. Where one of yours already does the job (EXCEEDS_INITIAL, COEFFICIENT_NOT_SQUARED), the file says so; use yours, with our ask as the override. |
| Problem numbers, with a source for every constant | `ch13_problems.csv` + `reactions_add_haber.json`, `reactions_add_wgs.json` | **Fixed, not generated** (instructor, 13 Oct): six per scenario, H1–H6 and M1–M6, covering every starting family. Each row gives the full sentence, the sources, the expected value for every item, and the trap values. All amounts are within the instructor's approved ranges. |
| The two simulation addresses with their MEDIA_SOURCES rows | addresses in the openers (column 11); rows in `ch13_media_rows.csv` | Both pages are approved, with fingerprints recorded. The instructor places the files in `media/ch13_ice/` himself. The picture rows are included. |

## Decisions on record (instructor)

- Equilibrium problems are fixed text (13 Oct).
- The Q item and the shift prediction stay on both scenarios (approved 11 Oct, confirmed 13 Oct). This reverses the 10 Oct removal of the direction kind on this archetype.
- K_confirmed (step 4, put the equilibrium values back into Kc) applies to Martian Fuel only. haber_setup stops before x.
- The worked rung uses Martian Fuel's equal-start problems (M1, M2). The offer serves the same problem with less steam.
- "ln" appears only in equations, and no caret notation appears in tutor text. The expected expressions in `ch13_problems.csv` use ^ only as the checker's notation, never shown to students.
- Q versus K stays a separate archetype. Its future scenarios should not reuse these two.

## Approval

Everything in this zip is approved by the instructor (13 Oct 2026), including the edited base moves rows and the twelve fixed problems. No row is DRAFT.
