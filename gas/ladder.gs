// ladder.gs — one module of the tutor shell (rebuild spec, step 4). Apps Script shares one global scope across files;
// in Node, Core.gs loads every module and makes its exports global, so plain function declarations work in both.
// The wrong-try ladder, PER STAGE: try 1 -> ask from another account; try 2 -> notebook card; two more after the return -> park the stage.
// Pure bookkeeping on S; returns { card, reply, switchAsk } for Phase A, or {} when nothing fired. Phase B uses switchAsk with the model.
function applyLadder(arch, S, V, ev, input) {
  var out = { card: null, reply: null, switchAsk: null }, failState = ev.active;
  if (!(ev.counted_fail && failState && !isSet(S, failState))) return out;
  var stg = stageOf(V, failState);
  S.tries[stg] = (S.tries[stg] || 0) + 1;
  var fm = moveFor(arch, V, failState);
  if (S.tries[stg] >= 2 && !S.bailed[stg]) {
    S.bailed[stg] = true; S.tries[stg] = 0; S.away = { state: failState, stage: stg, since: input.now || 0 };
    ev.event_type = "BAILOUT_ISSUED";
    out.card = { prompt: fm.notebook_prompt || "", url: arch.notebook_url, return_ask: fm.return_ask || "" };
    out.reply = "Let's pause here. Copy the prompt below into the course notebook, work through what it gives you, then come back and press I'm back.";
  } else if (S.tries[stg] >= 2) {
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
  } else if (S.tries[stg] === 1 && !ev.traps.length && fm.switch_ask) out.switchAsk = fm.switch_ask;
  return out;
}

if (typeof module !== "undefined") module.exports = { applyLadder: applyLadder };
