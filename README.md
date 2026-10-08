# V3 — one archetype, end to end (Clausius-Clapeyron). Pieces 1 and 2.

## NEEDS YOUR DECISION
1. **Gemini model.** I carried V2's names (`gemini-3.6-flash`, fallback `gemini-3.5-flash`). Two lines at the top of `Code.gs` if yours differ.
2. **Equations list.** Six unnamed equations in `ch10_cc.py` (`EQUATION_PICKS`), including two-point Arrhenius as the look-alike. For the single-archetype test only. Yours to set.
3. **The narrative.** `content_ch10_cc_moves.csv` — one row per board item: the question, the other-angle question, the notebook prompt, the question on return, what is shown if the item is parked. All ten rows are my DRAFT. Open it in Sheets, rewrite, set `status` to `approved`, re-run the factory. The tutor runs today on the drafts.
4. **Trap questions.** `TRAP_NOTES` in `ch10_cc.py`. DRAFT.

## Added 20 Sept
- **The picked relation stays on screen** ("Your symbols") to the end of the problem.
- **Rearranging for the unknown is mandatory** on the five two-point kinds. A right number typed early is recorded but does not count until the rearrangement is in. Once accepted, the student's own rearranged equation is pinned under the relation.
- **Checked by substitution, not by matching.** Any valid arrangement passes. True-but-not-isolated is progress, not a wrong try. A dropped sign and log-for-ln are named. An unbracketed denominator is wrong, as in V2.
- **Greek and math keys** above the message box. ΔHvap, subscripts, ⁻¹, ×10ⁿ are all read correctly by the checker.
- **Slope-from-data problems demand two rearrangements**: ΔHvap from the slope, and T alone from the line. Each gates its own number. Both get pinned. `ΔHvap = -mR` and `= -mR/1000` both pass. `T = m/(ln P - b)` and `T = m/(ln(760) - b)` both pass. Bare `ln P`, textbook style, is read; it takes only the next factor, so `ln P2/P1` is (ln P2)/P1 and is wrong.

## STILL YOURS — reminder
`content_ch10_cc_moves.csv`: **13 rows, all DRAFT.** New since you last looked: `rearranged`, `rearranged_dH`, `rearranged_T`. Also DRAFT: `TRAP_NOTES`, `EQUATION_PICKS`, `ASK` sentences, liquids table (in `archetypes/ch10_cc.py`). The factory prints the DRAFT count every run.

## What runs now
- **Factory (Python, your machine):** `python run.py ch10_cc --per-kind 12` → 72 problems (12 each: T2, P2, T1, P1, ΔHvap, slope-from-data), your six Ch 10 openers with their keywords, the narrative rows, all in one file `gas/Archetype_ch10_cc.gs`.
- **Core.gs:** the tutor's logic. No Google in it. Tested under Node.
- **Code.gs:** Google wiring. Sheet, cache, Gemini, log.
- **Plain mode:** with no API key the tutor still works, using only authored questions. Useful for testing the checks without the model in the way.

## Tests (both pass)
- `python test_ch10_cc.py` — 600 problems; every key agrees with a separately written solution; no wrong method lands near a key.
- `node gas/test_core.js` — 46 checks with scripted students: strong student straight through; bare number asks for units; key implies the symbolic steps; wrong pick; trap named; second wrong try gives the notebook card **with no model call**; return logged with time away; thin return answer refused; two more wrong tries parks and ends credit; a model that leaks the key never reaches the student; a second reader overrules an accepting tutor; a law name is not an account; a question costs nothing; slope problems; all 72 problems completable.
- The tests found one real bug, now fixed: with P1 = 1 atm, the answer P2 in atm is the same number as the ratio P2/P1, and the ratio was swallowing the answer.

## Set-up (ten minutes, once)
1. script.google.com → New project → name it V3.
2. Create three files and paste: `Archetype_ch10_cc.gs`, `Core.gs`, `Code.gs`.
3. Run `setupV3`. The log prints the new Sheet's address and an `APP_TOKEN`.
4. Project Settings → Script properties → add `GEMINI_API_KEY`.
5. Deploy → New deployment → Web app → execute as me, access anyone. Copy the URL.
6. Open the URL in a browser: you should see `{"alive":true,...}`.
Piece 3 (`index.html`) will ask for that URL and token.

## ENGINEERING (skippable)
- Not yet ported from V2, for Opus: the units-through-arithmetic engine (the substitution checker is now in, written fresh and smaller than V2's); the handed-over-setup guard; freshness note; State sheet backup (sessions live in cache, six hours).
- Students never receive the board's item names, only "3 of 7". Item names are hints.
- `true_substance` for slope problems stays on the server.
- Every log row carries: build stamp, content fingerprint, board item, register, face (choice / check / why), gate, tries, trap IDs, guards, after-notebook flag.
