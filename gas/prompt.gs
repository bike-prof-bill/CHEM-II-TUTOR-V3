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
    "\nThe problem is hidden from the student and from you until this clears. What clears it: one clause about what the PARTICLES are doing that engages this scenario. Rough is fine.";
  else out += "\n\nPROBLEM on the student's screen: " + V.text;
  out += "\n\nWHERE THE STUDENT IS: " + ctx.progress.done + " of " + ctx.progress.of + " established.";
  if (ctx.active) out += "\nNEXT THING TO ESTABLISH (" + ctx.register + " account): ask toward this, in your own words: " + (ctx.ask || "(no authored question; ask plainly)");
  else out += "\nEverything is established. The problem is over. Respond to what the student just said in one sentence. Ask nothing.";
  if (ctx.active && ctx.lastItem) out += "\nThis is the LAST item. If you accept it, the problem is complete: acknowledge their account in one or two sentences and ask nothing. A question after acceptance is wrong.";
  if (ctx.notes.length) out += "\n\nSERVER VERDICT THIS TURN:\n- " + ctx.notes.join("\n- ");
  if (ctx.judge) out += "\n\nYOU JUDGE THIS TURN: set accept to 1 only if the student's message establishes the item above. If you correct or redirect, accept is 0.";
  if (ctx.extra) out += "\n\n" + ctx.extra;
  return out;
}


var SECOND_READER = "You are checking one student message for a FALSE statement about the chemistry. Reply strict JSON {\"found\":0|1,\"quote\":\"exact words from the message\",\"why\":\"...\"}. If nothing is false, found is 0. Do not judge completeness.";

// The authored fallback: what the student reads when there is no model, the model failed, or every guard failed.
// Plus the plain hint when words arrived at a checkable item (instructor, 9 Oct).
var HINT_OF_KIND = { number: "This step is checked on the value: type it, with its unit.", equation: "This step is checked on the equation: type it on one line, the unknown alone on the left.",
                     pick: "This step is a choice: open the Equations list.", direction: "This step is a choice: pick one of the options.", table: "This step is checked on the table: type the three rows I:, C:, E:.", text: "", reflection: "" };
function fallbackReply(arch, S, V, ev, p) {
  var nowActive = activeState(S, V), nowMove = nowActive ? moveFor(arch, V, nowActive) : {};
  var ack = ev.newly.length ? "Checked: " + ev.newly.map(function (st) { var e = entry(V, st.replace(/\(parked\)$/, "")); return (e && e.label_when_done) || st.replace(/_/g, " "); }).join(", ") + ". " : "";
  var trapAsk = ev.traps.length && arch.trap_notes[ev.traps[0]] ? arch.trap_notes[ev.traps[0]].ask : "";
  var reply = nowActive ? ack + (trapAsk || (p.switchAsk && !ev.traps.length ? p.switchAsk : (S.pendingUnit !== null ? "What are the units of that value?" : (nowMove.ask || arch.openers[S.openerIndex].question))))
                        : ack + "That completes this problem.";
  var nb = nowActive ? entry(V, nowActive) : null;
  if (nb && !ev.newly.length && !trapAsk && (p.wordsOnly || reply === S.lastReply)) { var hint = HINT_OF_KIND[nb.kind] || ""; if (hint) reply = reply + " " + hint; }
  return reply;
}

if (typeof module !== "undefined") module.exports = { RULES: RULES, buildSystem: buildSystem, SECOND_READER: SECOND_READER, HINT_OF_KIND: HINT_OF_KIND, fallbackReply: fallbackReply };
