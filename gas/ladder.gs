// ladder.gs — one module of the tutor shell (rebuild spec, step 4). Apps Script shares one global scope across files;
// in Node, Core.gs loads every module and makes its exports global, so plain function declarations work in both.
// The wrong-try ladder, PER STAGE (instructor, 21 Oct 2026, replacing the 11 Oct ladder):
//   try 1 -> ask from another account (the step's switch question);
//   try 2 -> the PIVOT: the step's pivot question sends the student back to the particles; their answer is judged loosely (Core) and
//            never counted; then the step is asked again;
//   try 3 and after -> HELP, by the session's policy (S.policy, logged):
//     A  notebook card, then park;
//     B  the worked companion (the same step in a companion problem of the same scenario and rank), then the notebook card as the
//        last straw, then park;                                                                   (the instructor's pilot default)
//     C  the step is done for them (parked with its park text) at once.
//   A step without a pivot question (the particle account is itself the particle step) skips the pivot rung.
// Pure bookkeeping on S; returns { card, reply, switchAsk } for Phase A, or {} when nothing fired. Phase B uses switchAsk with the model.
var POLICIES = { A: ["notebook", "park"], B: ["companion", "notebook", "park"], C: ["park"] };
function policyOf(S) { var p = String(S.policy || "B").toUpperCase(); return POLICIES[p] ? p : "B"; }
function helpOrder(arch, S, V, failState) {
  var fm = moveFor(arch, V, failState), b = entry(V, failState) || {};
  var order = [];
  if (fm.pivot_question && failState !== "account_given") order.push("pivot");
  POLICIES[policyOf(S)].forEach(function (r) {
    if (r === "companion" && !(companionFor(arch, V) && (b.kind === "number" || b.kind === "pick" || b.kind === "direction" || b.kind === "coefficients"))) return;   // a text step has no worked companion: the notebook follows
    order.push(r);
    if (r === "notebook" && order.indexOf("pivot") < 0) order.push("retry");   // the 11 Oct ladder for archetypes without a pivot question: two more tries after the return, then park
  });
  return order;
}
function companionFor(arch, V) {        // the companion problem named by the sheet (brief 32), among this archetype's variants
  if (!V.companion) return null;
  for (var i = 0; i < arch.variants.length; i++) if (arch.variants[i].fixed_id === V.companion) return arch.variants[i];
  return null;
}
// The same step, worked, in the companion problem: its sentence and the value or option that step holds there. Never this problem's numbers.
function companionText(arch, S, V, state) {
  var C = companionFor(arch, V); if (!C) return "";
  var b = entry(C, state) || entry(V, state) || {}, lab = b.label_when_done || state.replace(/_/g, " "), shown = [];
  (C.expected || []).forEach(function (e) { if (e.state === state && (e.role === "intermediate" || e.role === "key")) shown.push(e.label + " = " + e.value + (e.unit ? " " + e.unit : "")); });
  if (!shown.length && (b.kind === "pick" || b.kind === "direction")) { var r = optionsOf(arch, C, b).filter(function (o) { return o.right; })[0]; if (r) shown.push(r.text); }
  if (!shown.length && b.kind === "coefficients" && b.right) shown.push((b.species || []).map(function (s, i) { return (b.right[i] === 1 ? "" : b.right[i] + " ") + s; }).join(" + "));
  if (!shown.length) return "";
  return "Here is the same step worked in a companion problem. " + C.text + " For this step (" + lab + "): " + shown.join("; ") + ". Now yours:";
}
function applyLadder(arch, S, V, ev, input) {
  var out = { card: null, reply: null, switchAsk: null }, failState = ev.active;
  if (!(ev.counted_fail && failState && !isSet(S, failState))) return out;
  // rungs (instructor, 11 Oct): no ladder on the Worked rung (the tutor is showing the way) or the Independent rung (no help);
  // the try is still counted and logged, and an Independent student who fails twice on one stage is demoted by the record
  if (S.rung === "worked") return out;
  if (S.rung === "independent") { var stg0 = stageOf(V, failState); S.tries[stg0] = (S.tries[stg0] || 0) + 1; if (S.tries[stg0] >= 2 && !S.bailed[stg0]) { S.bailed[stg0] = true; S.clean = false; ev.demote = true; } return out; }
  var stg = stageOf(V, failState);
  S.tries[stg] = (S.tries[stg] || 0) + 1;
  var fm = moveFor(arch, V, failState), n = S.tries[stg];
  if (n === 1) { if (!ev.traps.length && fm.switch_ask) out.switchAsk = fm.switch_ask; return out; }
  var order = helpOrder(arch, S, V, failState), rung = order[Math.min(n - 2, order.length - 1)] || "park";
  S.helpUsed = S.helpUsed || {}; (S.helpUsed[stg] = S.helpUsed[stg] || []).push(rung); ev.help_rung = rung;
  if (rung === "retry") { if (!ev.traps.length && fm.switch_ask) out.switchAsk = fm.switch_ask; return out; }
  if (rung === "pivot") {
    S.pivot = { state: failState, stage: stg }; ev.event_type = "PIVOT_ASKED";
    out.reply = fm.pivot_question;
  } else if (rung === "companion") {
    var ct = companionText(arch, S, V, failState); ev.event_type = "COMPANION_SHOWN";
    out.reply = ct ? ct + " " + (fm.ask || "") : (fm.ask || "");
  } else if (rung === "notebook") {
    S.bailed[stg] = true; S.away = { state: failState, stage: stg, since: input.now || 0 };
    ev.event_type = "BAILOUT_ISSUED";
    out.card = { prompt: fm.notebook_prompt || "", url: arch.notebook_url, return_ask: fm.return_ask || "" };
    out.reply = "Let's pause here. Copy the prompt below into the course notebook, work through what it gives you, then come back and press I'm back.";
  } else {
    ev.event_type = "PARK"; S.clean = false;
    var handed = [];
    liveItems(S, V).forEach(function (bb) {
      if (isSet(S, bb.id) || stageOf(V, bb.id) !== stg) return;
      S.board[bb.id] = "parked"; ev.newly.push(bb.id + "(parked)");
      var pk = (V.eq_checks || []).filter(function (k) { return k.state === bb.id; })[0];
      var pm = moveFor(arch, V, bb.id);
      if (pk) { (S.pinned.rearranged = S.pinned.rearranged || []).push(pk.park_text); addPin(S, bb.id, bb.label_when_done || bb.id, pk.park_text); handed.push(pk.park_text); }
      else if (bb.kind === "table" && V.table) { var tt = ["I", "C", "E"].map(function (r) { return r + ": " + V.table.rows[r].join(" | "); }).join("  "); addPin(S, bb.id, bb.label_when_done || "table", tt); handed.push(tt); }
      else if (bb.kind === "pick" || bb.kind === "direction") { var right = optionsOf(arch, V, bb).filter(function (o) { return o.right; })[0]; if (right) { S.picks[bb.id] = right.id; if (bb.id === "relation_chosen") S.pinned.relation = right.text; if (bb.pin) addPin(S, bb.id, bb.label_when_done || bb.id, right.text); handed.push(right.text); } }
      else if (pm.park_text) handed.push(pm.park_text);
    });
    liveItems(S, V).forEach(function (bb) { if (bb.kind === "number" && !isSet(S, bb.id) && stateSatisfied(S, V, bb.id)) tick(S, V, bb.id, ev.newly); });
    var nxt = activeState(S, V), nm = nxt ? moveFor(arch, V, nxt) : {};
    out.reply = (handed.length ? "Here is that piece so you can keep going: " + handed.join(" ; ") + " " : "We will set that piece aside. ") + (nm.ask || "");
  }
  return out;
}

if (typeof module !== "undefined") module.exports = { applyLadder: applyLadder, POLICIES: POLICIES, policyOf: policyOf, helpOrder: helpOrder, companionFor: companionFor, companionText: companionText };
