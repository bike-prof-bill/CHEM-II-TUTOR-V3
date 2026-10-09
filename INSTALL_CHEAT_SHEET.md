# V3 install cheat sheet

Two ways to run. Do A first: two minutes, no Google, proves the page and the checks work.

## A. On your machine only (plain mode, no AI)
Needs Node (nodejs.org, any recent version).
1. Unzip. Open a terminal in the `v3_ch10_cc` folder.
2. `node gas/local_server.js` → it prints a URL and a token.
3. Double-click `index.html`.
4. Settings box opens. URL: `http://localhost:8787/exec` · Token: `local` · **Test** → "Server alive" · **Save**.
5. **New problem.** Log rows print in the terminal as you go.
Plain mode asks only the authored questions. It is the right mode for testing the checks.

## B. On Google (with Gemini)
1. script.google.com → **New project** → rename to `V3 Tutor`.
2. Make five script files (＋ → Script) and paste from the `gas` folder:
   `Units` · `Archetype_ch10_cc` · `Archetype_ch13_ice` · `Core` · `Code`  (delete the empty `myFunction` stub).
3. Pick `setupV3` in the function menu → **Run** → approve permissions.
   **Execution log** shows: the new Sheet's address, and `APP_TOKEN`. Copy the token.
4. ⚙ **Project Settings → Script properties → Add**: `GEMINI_API_KEY` = your key.
5. Run `checkModels`. The log says whether the two model names at the top of `Code.gs` exist today, and lists the ones that do. Edit the two lines if needed.
6. **Deploy → New deployment → Web app** · Execute as: **Me** · Who has access: **Anyone** → **Deploy**. Copy the URL ending in `/exec`.
7. Paste that URL in a browser. You should see `{"alive":true,...}`.
8. Open `index.html` → **Settings** → paste URL and token → **Test** → **Save** → **New problem**.

**After any code change:** Deploy → **Manage deployments** → pencil → Version: **New version** → Deploy. The URL stays the same. Forgetting this is the usual reason "my change did nothing."

## Changing content
1. Edit `content_ch10_cc_moves.csv` (your narrative), `content_ch10_cc_openers.csv`, or `archetypes/ch10_cc.py` (liquids, equations, traps). Units live in `units.json`.
2. `python run.py all --per-kind 3 --seed 1`   (or `make generate`)
3. `make test` — everything should pass.
4. Re-paste the changed `gas/Archetype_*.gs` (and `gas/Units.gs` if units changed) into Apps Script. New version. (For route A, just restart the local server.)

## Ten-minute hand test
Use the archetype and kind menus (filled from the server) to force a problem type. Add `?debug=1` to the page address to see the raw server reply.
For the equilibrium archetype, type the table as three lines: `I: 0.80 | 0 | 0`, `C: -x | +x | +x`, `E: 0.80 - x | x | x`.
| Try this | You should see |
|---|---|
| Type "hi", then "Clausius-Clapeyron" | Problem stays hidden |
| Give a particle account | Problem appears; meter moves |
| Equations → pick the Arrhenius look-alike | Not accepted; asked from another angle |
| Pick a second wrong one | Notebook card; input locked; no wait |
| Copy → Open notebook → I'm back → type "ok" | Asked again what you learned |
| Say what you learned | Carries on |
| Equations → pick the right one | It stays on the left under "Your symbols" for the rest of the problem |
| Type the right number before rearranging | Recorded, but does not count yet; asked for the rearrangement |
| Type `1/T2 = 1/T1 - (R/ΔHvap) ln(P2/P1)` on a T2 problem | True but not isolated: nudged, not marked wrong |
| Type it with the unknown alone on the left, any valid form | Accepted, pinned under the relation; an earlier right number now counts |
| Flip a sign, or write log for ln | The error is named to the tutor; you get a question about your own algebra |
| Type the right answer with no units | Asked for units, not marked wrong |
| Type just the unit | Accepted; several meter segments fill at once; plots open |
| Leave a temperature in °C on purpose | A question aimed at the temperature scale, no fix given |
| Move the probe, then send a message | A `SIM` row in the log |
| Two wrong numbers, notebook, two more wrong | Item parked and shown; finish says no credit |
| Finish cleanly | "Clean run recorded"; a Mastery row |
| slope kind | Plots arrive with the problem; two answers wanted |

## If something is off
- "unauthorized" → token mismatch. Re-copy from the `setupV3` log (or Script properties).
- "Could not reach the server" → URL is not the `/exec` one, or access is not "Anyone".
- Replies are only the plain authored questions on Google → no `GEMINI_API_KEY`, or the model name is stale. Run `checkModels`. The Log sheet's `fallback_used` column says which turns.
- "no session" → more than six hours idle. New problem.
