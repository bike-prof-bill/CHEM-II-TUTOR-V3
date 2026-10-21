# Contract: how a simulation page reports what the student does (v1, Fable, 21 Oct 2026)

Approved by the instructor 21 Oct 2026. This is the `postMessage` contract that `docs/04` (Simulation_Claude's role, "Nothing is
sent anywhere") said Fable would specify if the tutor ever wanted events from a page. It replaces that one line; every other
rule in `docs/04` stands: one file, nothing fetched, nothing stored, no network calls, no analytics.

## What changes and what does not
- A page still makes **no network calls and stores nothing**. It speaks only to the tutor page that holds it, through the
  browser's own `window.parent.postMessage`. The tutor page is the only listener; the message never leaves the browser until the
  tutor sends its next turn to the shell, which logs it as a `SIM` row (the shell already does this for chapter 10's probe).
- A page opened on its own (from disk, from the gallery, with no parent) must work exactly as before: `postMessage` to a
  missing parent is harmless, and the page must never wait for a reply. There is no reply.
- A page sends nothing until a control comes to rest or a reading is taken. No stream of mouse moves, no heartbeat.

## The messages
Every message is one plain object with `type: "sim"` and `v: 1`. Two kinds:

**A control came to rest** (sent once per interaction, when the slider, dial or button is released or stops):
```js
window.parent.postMessage({ type: "sim", v: 1, kind: "control", id: "piston",
  start: 1.00, end: 0.50, min: 0.50, max: 1.00, moves: 7, seconds: 4, unit: "L" }, "*");
```
`id` is the control's fixed id from the page's id list (the one SCENARIO_CLAUDE put in the Fable list); `start` and `end` are
the values at the first touch and at rest; `min` and `max` the extremes passed through; `moves` the number of steps;
`seconds` the time held; `unit` as the page shows it. These are the same fields the chapter 10 probe already reports.

**A reading was taken** (sent when the student does something deliberate to read a value: presses a "read" button, pins a
point, or stops on a value for a second; never on every repaint):
```js
window.parent.postMessage({ type: "sim", v: 1, kind: "reading", id: "P_readout",
  value: 2.03, unit: "atm", at: { piston: 0.50, T_slider: 298 } }, "*");
```
`id` is the reading's fixed id; `value` and `unit` what the page displayed; `at` the current value of every control, by id, so
the reading can be checked against the model later.

**A menu, switch or view changed** (a control whose values are names, not numbers): same `kind: "control"`, with `choice`
instead of the numeric fields:
```js
window.parent.postMessage({ type: "sim", v: 1, kind: "control", id: "solute", choice: "CaCl2", previous: "NaCl" }, "*");
window.parent.postMessage({ type: "sim", v: 1, kind: "control", id: "view", choice: "surface", previous: "graph" }, "*");
```
A Play button that changes the view reports the view change this way; it need not report the press itself. (Added 21 Oct at
Simulation_Claude's request.)

Optional, once per load: `{ type: "sim", v: 1, kind: "ready", page: "ch11_colligative", controls: ["piston", ...],
readings: ["P_readout", ...] }`, so the tutor can confirm the ids match the sheet. Send it after the page has read its
parameters.

## Rules
1. Ids are the ones in the page's header comment and in SCENARIO_CLAUDE's Fable list; a renamed id is a change brief.
2. Values are numbers, not strings, for sliders, dials and readings; a menu or switch reports its `choice` as the menu's value, as written in the URL parameter (`CaCl2`, not the displayed `CaCl₂`; instructor, 21 Oct); units are strings as shown on screen.
3. At most one message per control rest and one per reading; a page that posts more than about twenty messages a minute
   under ordinary use is sending too much.
4. Nothing in a message identifies the student; the tutor adds the attempt and the archetype when it logs.
5. A page must not read messages from the parent; the channel is one way. (If the tutor ever needs to set a page's state,
   that is a second contract.)
6. The target origin is `"*"` because the tutor is served from Netlify and opened from disk in testing; the tutor page, not
   the simulation, checks the sender (`event.source` must be the simulation frame) before accepting a message.

## What the tutor does with it (Fable's side, not the page's)
The tutor page listens for `message`, accepts only messages whose source is its simulation frame and whose `type` is `"sim"`,
and adds each to the events it sends with the student's next turn. The shell logs each as a `SIM` row with the attempt,
archetype, variant and step, as it does for the probe today, capped at twenty per turn. Later, an instrument step's expected
reading can be checked against the `reading` message's `value`; that is a shell change and a separate brief.

## For the page being built now (SCENARIO_CLAUDE's recommendation stands)
Build the chapter 11 page with fixed ids on every control and reading and post the two message kinds above. The messages do
nothing until the tutor page listens, so there is no risk in sending them now, and no second visit to the page later.
Header comment: add the list of control ids (with ranges and units) and reading ids (with units) under the URL parameters.
