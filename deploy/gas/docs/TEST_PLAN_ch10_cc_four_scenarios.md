# Run-through plan: the four Clausius-Clapeyron scenarios (11 Oct 2026)

For the instructor, running in Google mode (Gemini engaged). Plain mode only if Google mode will not connect.

## Before the first problem

1. The checklist from 10 Oct is done: repository zip dropped in and pushed; `media/ch10_cc/` holds the nine files; Apps Script re-pasted (`Units`, `parse`, `match`, `stepmap`, `prompt`, `Core`, `Code`, `Archetype_ch10_cc`, `Archetype_ch13_ice`, new `logqueue`) and a new version deployed; `refreshHeaders` run once; `index.html` opened from the repository folder.
2. Settings → Test → "Server alive". Hover "V3 · Clausius-Clapeyron": the tooltip's content code must match the one in the latest report. A different code means a stale Archetype paste; stop and re-paste.
3. Type a Student ID (any word) before the first New problem. It turns on no-repeat history and labels your rows in the log sheet.
4. Have the Google Sheet open in another tab; refresh it after each problem.

## Order

Rubbing Alcohol Chill (two kinds: ΔHvap from two points, ΔHvap from a line) → Syringe Boiling Trick → Drinking Bird → Deep-Sea Vent. The first is the one you have run before; differences there are differences in the tutor, not the scenario. Use the Scenario menu; leave the kind menu on "any kind" except where a probe below says otherwise.

Work each problem twice if time allows: once straight (the right thing at every step), once with the probes.

## What matters most, in order

1. **Wrong or unsafe content reaches the student.** The model states something false and the second reader lets it through; a reply names the answer or an intermediate before you typed it; a simulator shows a number that disagrees with the problem by more than rounding. Stop, copy the exchange, send it. Nothing else matters until this is clean.
2. **Grading wrong.** A true account refused (yesterday's fault); a right value with the right unit refused; a wrong value accepted; credit granted after a park; a named error misnamed (the question does not fit the slip you made). Copy the exchange.
3. **Flow stalls or wanders.** The model asks its own question at a choice item instead of the authored one (fixed yesterday; confirm); the same question twice in a row with nothing new; a step you cannot get past by doing the right thing; the simulation does not open, opens too early, or opens on the wrong liquid, temperature or depth.
4. **Wording.** The model's phrasing above the students' reading level; your own authored text reading badly in context; the problem sentence awkward for some liquid or unit combination. Note it for SCENARIO_CLAUDE; nothing to send me unless the shell is implicated.
5. **Cosmetic.** Layout, a value printed as 40 rather than 40.0, pin order, label wording. Note and move on.

## Probes to type (compliance), each with what should happen

Opener (first turn of any scenario):
- A label only: "It's volatile, it evaporates" (alcohol) / "The vacuum makes it boil" (syringe) / "It's a heat engine" (bird) / "The water is superheated" (vent) → held, not counted, asked what the particles are doing. The log row shows `OPENER_LABEL_ONLY`.
- A true minimal account: "Molecules escape the surface" (alcohol) / "Lower pressure lets molecules with enough energy escape as bubbles" (syringe) / "Fewer molecules escape from the cooler head" (bird) / "The water above presses the molecules together" (vent) → accepted on the first try; the problem appears. If it takes more than one try, copy the exchange: that is yesterday's fault still present.
- A false account: "The bonds inside the molecules break and the atoms fly off" → refused by the second reader; the log row shows `FALSE_CLAIM`.
- A question without a question mark: "what do you mean" → answered, costs nothing (`turn_kind` question in the log).

Choice items (prediction, Equations list):
- After the account on a pressure or temperature problem the reply must be the authored prediction question with three buttons; after you press the right one the reply must be "The problem is on your screen. Open the Equations list…" verbatim, with no model question in front of it.
- Press a wrong prediction first: one wrong try on the setup stage, the switch question, no card.
- Pick a wrong equation: counted once; pick the right one: pinned under Your symbols and placed in the box.

Rearrangement:
- Type a true but not-isolated form (the relation with both sides swapped): "progress, not a wrong try".
- Type the unknown alone on the left: "Checked: Rearranged".
- Type it with a dropped minus sign: named (`EQ_SIGN_FLIPPED`), counted.

Values:
- "T1 = 357.15 K and T2 = 320.65 K" on one line (use your problem's values): both read.
- "T2 = (273.15 + 47.5) K": the sum read, the parts not counted as strays.
- "P2/P1 = 0.35" (your ratio): substitution ticked.
- The right answer with no unit: "What are the units of that value?" Then the unit alone: accepted.
- The right number with a wrong-dimension unit ("357 atm" for a temperature): refused; `WRONG_DIMENSION` in the log.
- A number that matches nothing: one stray, counted; the second stray on the same stage: the notebook card.

Named errors (one per scenario is enough):
- Syringe or bird: type the known pressure times the ratio instead of divided by it (the answer on the wrong side): `SIGN_FLIPPED`, with that scenario's own question.
- Syringe, when the known pressure is 760 torr: type the ratio with a unit ("0.35 torr"): `RATIO_NOT_SCALED`.
- Bird: a head pressure above the body pressure: `SIGN_FLIPPED` in the bird's words; or the pressure difference with either sign: accepted.
- Vent: type your 1/T value with °C or K as the temperature: `RECIPROCAL_NOT_TAKEN`; type the depth/10 without the air's 1 atm at a shallow depth: a stray; at depth, accepted (by design).

The ladder:
- Two wrong tries on one stage → notebook card; press I'm back without typing → asked what the notebook showed, not counted; type a sentence → carry on.
- Two more wrong tries on that stage → the stage is parked and handed over; the problem continues; at the end: "Problem complete. Recorded without credit for this attempt."

Simulation:
- Opens exactly when the meaning question becomes active (after the answer; after the pressure difference on the bird), never earlier.
- Preselected to the problem: the alcohol's liquid; the syringe's liquid and temperature; the bird's liquid and both temperatures, the difference matching yours; the vent's depth and unit. The credit line sits under the picture or video.

Completion:
- After the reflection sentence: "Problem complete. Clean run recorded." and no question in the reply. Type one more line: acknowledged, no question.

History and log:
- With a Student ID, New problem within one scenario gives a different problem each time (3 for the alcohol kinds, 6 for the others), then a reset row in the log.
- One row per turn in the sheet; `verdict_ms` small, `say_ms` the model's time; `queued` 0.

## What to send me

For anything in tiers 1 to 3: the exchange as text (select the chat, copy), the scenario and the problem sentence, and if the server errored, the Executions page entry in Apps Script. For tier 4 and 5: a list, whenever convenient.
