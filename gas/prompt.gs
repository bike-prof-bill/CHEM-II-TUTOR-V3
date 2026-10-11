// prompt.gs — one module of the tutor shell (rebuild spec, step 4). Apps Script shares one global scope across files;
// in Node, Core.gs loads every module and makes its exports global, so plain function declarations work in both.
var RULES = [
  "You are a General Chemistry II tutor working Socratically with one student. The server checks every number and every pick and tells you below what happened this turn. Trust the server over your own impression.",
  "1. Never do the math, never state a value the student has not produced, never hand over the set-up inside a question.",
  "2. Never call something correct that the server has not confirmed. Acknowledge by naming what was right in the student's own words.",
  "3. A name or an analogy is not an account. Ask what the particles are doing.",
  "4. A physical quantity needs its units.",
  "5. Never ask a yes/no question or one answered by reading the problem.",
  "6. Plain text only. No LaTeX, no caret. Unicode superscripts are fine.",
  "7. Name which account the student is in when it helps: particles (never seen, inferred), symbols (the bridge), or measurement (what an instrument reads).",
  "OUTPUT strict JSON: {\"accept\": 0 or 1, \"turn_kind\": \"answer\"|\"question\"|\"offtopic\", \"socratic_response\": \"...\"}. accept matters only when the server says YOU JUDGE THIS TURN."
].join("\n");

function buildSystem(arch, S, V, ctx) {
  var out = RULES, opener = arch.openers[S.openerIndex];
  if (!isSet(S, "account_given")) out += "\n\nOPENING QUESTION on the student's screen: " + opener.question +
    "\nThe problem is hidden from the student and from you until this clears. What clears it: one TRUE clause about what the PARTICLES are doing that engages this scenario. Rough is fine. Incomplete is fine. " +
    "A true statement is accepted even if it leaves out the mechanism you would have named; the second reader checks only for FALSE statements. Reject only what is false, empty of particles, or about a different scene.";
  else out += "\n\nPROBLEM on the student's screen: " + V.text;
  out += "\n\nWHERE THE STUDENT IS: " + ctx.progress.done + " of " + ctx.progress.of + " established.";
  if (ctx.active) out += "\nNEXT THING TO ESTABLISH (" + ctx.register + " account): ask toward this, in your own words: " + (ctx.ask || "(no authored question; ask plainly)");
  else out += "\nEverything is established. The problem is over. Respond to what the student just said in one sentence. Ask nothing.";
  if (ctx.active && ctx.lastItem) out += "\nThis is the LAST item. If you accept it, the problem is complete: acknowledge their account in one or two sentences and ask nothing. A question after acceptance is wrong.";
  if (ctx.notes.length) out += "\n\nSERVER VERDICT THIS TURN:\n- " + ctx.notes.join("\n- ");
  if (ctx.judge) out += "\n\nYOU JUDGE THIS TURN: set accept to 1 if the student's message is a TRUE statement that establishes the item above, however brief or incomplete. Do not hold out for the fuller account you have in mind: completeness is not the test, truth is. Set accept to 0 only for a false statement, no statement, or a different scene; if you correct or redirect, accept is 0.";
  if (ctx.extra) out += "\n\n" + ctx.extra;
  return out;
}


var SECOND_READER = "You are checking one student message for a FALSE statement about the chemistry. The message answers the scenario given first; " +
  "comparisons in it (weaker, stronger, faster, less energy) are relative to the other substance or condition in that scenario, not absolute claims. " +
  "Reply strict JSON {\"found\":0|1,\"quote\":\"exact words from the message\",\"why\":\"...\"}. found is 1 only for a statement that is false as chemistry. " +
  "Not for incompleteness, informality, an unstated comparison, or a mechanism left out. If nothing is false, found is 0.";
// the second reader's input: the scenario, then the message, so a relative claim is read in context (instructor's run, 11 Oct)
function secondReaderMsg(arch, S, msg) { var o = arch.openers[S.openerIndex]; return "Scenario: " + (o ? o.question : "") + "\n\nStudent message: " + msg; }

// The authored fallback: what the student reads when there is no model, the model failed, or every guard failed.
// Plus the plain hint when words arrived at a checkable item (instructor, 9 Oct).
var HINT_OF_KIND = { number: "This step is checked on the value: type it, with its unit.", equation: "This step is checked on the equation: type it on one line, the unknown by itself on one side.",
                     pick: "This step is a choice: open the Equations list.", direction: "This step is a choice: pick one of the options.", table: "This step is checked on the table: type the three rows I:, C:, E:.", text: "", reflection: "" };
// The near-miss question: the archetype's errors file may give it (row NEAR_MISS); otherwise the instructor's default wording (11 Oct).
var NEAR_MISS_ASK = "Which values did you use to get that number?", REPEAT_SENTENCE = "That is the same number as before.";
// Units verdicts (instructor, 11 Oct): the setup typed in full. Right units, wrong value: "check your calculation", a known error named if
// one matched. Units that do not cancel: the unit produced is named, and the question tutors toward the setup. Archetype rows
// UNITS_OK_VALUE_WRONG and UNITS_DONT_CANCEL may replace the words; {produced} and {target} are filled in.
var UNITS_OK_ASK = "Your units come out as {produced}, as they should, so the setup is sound. Check your calculation for errors.";
var UNITS_DONT_CANCEL_ASK = "Your units come out as {produced}, which is not the unit of anything in this problem. Which quantity is in the wrong place, or in the wrong unit?";
var UNITS_IN_LOG_ASK = "Inside {fn}, your units come out as {produced}; a logarithm takes a pure number. Which quantity is in the wrong place, or in the wrong unit?";
var UNITS_MIXED_ASK = "You are adding or subtracting {produced}, which cannot be combined. Which quantity is in the wrong place, or in the wrong unit?";
function nearMissAsk(arch, V, ev) {
  var a;
  if (ev.units_check === "ok_value_wrong") a = (ev.traps.length ? trapNote(arch, V, ev.traps[0]).ask + " " : "") + (trapNote(arch, V, "UNITS_OK_VALUE_WRONG").ask || UNITS_OK_ASK);
  else if (ev.units_check) a = trapNote(arch, V, "UNITS_DONT_CANCEL").ask || (ev.units_fail === "function" ? UNITS_IN_LOG_ASK : ev.units_fail === "mixed" ? UNITS_MIXED_ASK : UNITS_DONT_CANCEL_ASK);
  else a = trapNote(arch, V, "NEAR_MISS").ask || NEAR_MISS_ASK;
  a = a.replace(/\{produced\}/g, ev.units_produced || "no unit").replace(/\{target\}/g, ev.units_target || "the unit asked for").replace(/\{fn\}/g, ev.units_fn || "the logarithm");
  return (ev.repeat ? REPEAT_SENTENCE + " " : "") + a;
}
function fallbackReply(arch, S, V, ev, p) {
  var nowActive = activeState(S, V), nowMove = nowActive ? moveFor(arch, V, nowActive) : {};
  var ack = ev.newly.length ? "Checked: " + ev.newly.map(function (st) { var e = entry(V, st.replace(/\(parked\)$/, "")); return (e && e.label_when_done) || st.replace(/_/g, " "); }).join(", ") + ". " : "";
  var trapAsk = (ev.units_check || ev.near_miss || ev.repeat) && !ev.newly.length ? nearMissAsk(arch, V, ev) : (ev.traps.length ? trapNote(arch, V, ev.traps[0]).ask : "");
  var reply = nowActive ? ack + (trapAsk || (p.switchAsk && !ev.traps.length ? p.switchAsk : (S.pendingUnit !== null ? "What are the units of that value?" : (nowMove.ask || arch.openers[S.openerIndex].question))))
                        : ack + "That completes this problem.";
  var nb = nowActive ? entry(V, nowActive) : null;
  if (nb && !ev.newly.length && !trapAsk && (p.wordsOnly || reply === S.lastReply)) { var hint = HINT_OF_KIND[nb.kind] || ""; if (hint) reply = reply + " " + hint; }
  return reply;
}

if (typeof module !== "undefined") module.exports = { RULES: RULES, buildSystem: buildSystem, SECOND_READER: SECOND_READER, HINT_OF_KIND: HINT_OF_KIND, fallbackReply: fallbackReply, secondReaderMsg: secondReaderMsg, nearMissAsk: nearMissAsk, NEAR_MISS_ASK: NEAR_MISS_ASK };
