// stepmap.gs — one module of the tutor shell (rebuild spec, step 4). Apps Script shares one global scope across files;
// in Node, Core.gs loads every module and makes its exports global, so plain function declarations work in both.
// ---------- the step map (Change 1): live items, branches, stages ----------
function entry(V, state) { for (var i = 0; i < V.board.length; i++) if (V.board[i].id === state) return V.board[i]; return null; }
function isSet(S, state) { return S.board[state] === "ticked" || S.board[state] === "parked"; }
// An item named under a branch option exists only once that option has been picked. Everything else is live.
function liveItems(S, V) {
  var latent = {}, opened = {};
  V.board.forEach(function (b) {
    for (var opt in (b.branch || {})) b.branch[opt].forEach(function (id) { latent[id] = 1; if (S.picks[b.id] === opt) opened[id] = 1; });
  });
  return V.board.filter(function (b) { return !latent[b.id] || opened[b.id]; });
}
function isLive(S, V, state) { return liveItems(S, V).some(function (b) { return b.id === state; }); }
function activeState(S, V) {
  var live = liveItems(S, V);
  for (var i = 0; i < live.length; i++) {
    var b = live[i];
    if (!isSet(S, b.id) && b.requires.every(function (r) { return isSet(S, r); })) return b.id;
  }
  return null;
}
// Correct later work implies the symbolic steps before it. Text items and `explicit` items are never implied.
function tick(S, V, state, newly) {
  if (isSet(S, state)) return;
  var b = entry(V, state); if (!b || !isLive(S, V, state)) return;
  b.requires.forEach(function (r) { var rb = entry(V, r); if (rb && rb.kind !== "text" && rb.kind !== "reflection" && !rb.explicit) tick(S, V, r, newly); });
  if (!b.requires.every(function (r) { return isSet(S, r); })) return;
  S.board[state] = "ticked"; newly.push(state);
  if (b.pin && b.kind === "number") {                        // the accepted value stays on screen
    var txt = [];
    V.expected.forEach(function (e, i) { if (e.state === state && S.matched[i]) txt.push(e.label + " = " + e.value + (e.unit ? " " + e.unit : "")); });
    if (txt.length) addPin(S, state, b.label_when_done || state, txt.join("; "));
  }
}
function stateSatisfied(S, V, state) {
  var b = entry(V, state), idx = [];
  V.expected.forEach(function (t, i) { if (t.state === state && (t.role === "intermediate" || t.role === "key")) idx.push(i); });
  if (!idx.length) return false;
  var got = idx.filter(function (i) { return S.matched[i]; }).length;
  return (b.rule === "any") ? got >= 1 : got === idx.length;
}
function stageOf(V, state) { var b = entry(V, state); return b ? (b.stage || b.id) : state; }
// The instructor's moves file: the item's row, with the stage row (`stage:<name>`) filling any empty column.
function moveFor(arch, V, state) {
  var item = arch.moves[state] || {}, st = arch.moves["stage:" + stageOf(V, state)] || {}, out = {};
  [item, st].forEach(function (src) { for (var k in src) if (src[k] && !out[k]) out[k] = src[k]; });
  return out;
}
function addPin(S, id, label, text) {
  S.pins = S.pins.filter(function (p) { return p.id !== id; }); S.pins.push({ id: id, label: label, text: text });
}
// Options of a pick or direction item: the archetype's Equations list, or the item's own list.
function optionsOf(arch, V, b) {
  if (b.options_from === "equation_picks") return arch.equation_picks.map(function (e) { return { id: e.id, text: e.text, right: e.fits.indexOf(V.kind) > -1 }; });
  return (b.options || []).map(function (o) { return { id: o.id, text: o.text, right: (b.right || []).indexOf(o.id) > -1 }; });
}
function pickItemFor(arch, S, V, optionId) {              // which live, unmet pick/direction item owns this option
  var live = liveItems(S, V);
  for (var i = 0; i < live.length; i++) {
    var b = live[i]; if ((b.kind !== "pick" && b.kind !== "direction") || isSet(S, b.id)) continue;
    if (optionsOf(arch, V, b).some(function (o) { return o.id === optionId; })) return b;
  }
  return null;
}


// ---------- sessions ----------
function newSession(arch, pick) {
  var V = arch.variants[pick.variantIndex];
  return { attemptId: "A" + pick.stamp, archetypeId: arch.archetype_id, variantId: V.variant_id, variantIndex: pick.variantIndex,
    openerIndex: (V.opener_index !== undefined ? V.opener_index : pick.openerIndex), board: {}, matched: {}, pendingUnit: null, tries: {}, bailed: {}, away: null,
    awaitingReturn: null, pinned: {}, pins: [], picks: {}, clean: true, turns: 0, produced: [], done: false, credit: false, simOpen: false, mediaSimOpen: false, lastReply: null };
}
function problemPayload(arch, V, S) {     // what the browser is allowed to have once the account is given
  var med = (S && arch.openers[S.openerIndex] && arch.openers[S.openerIndex].media) || {};
  return { title: arch.title, text: V.text, givens: V.givens, plots: V.reveal_with_problem || null,
    media: { image: med.image_after_account || "", alt: med.image_alt || "" },
    equations: arch.equation_picks.map(function (e) { return { id: e.id, text: e.text }; }) };
}
function openerMedia(arch, S) {           // what the browser may show WITH the opening question, before anything is earned
  var med = (arch.openers[S.openerIndex] && arch.openers[S.openerIndex].media) || {};
  return { image: med.image_with_question || "", alt: med.image_alt || "" };
}
// Progress counts live items only. Labels are shown for ticked items only; labels ahead stay hidden.
function progress(S, V) {
  var live = liveItems(S, V), n = 0, labels = [];
  live.forEach(function (b) { if (isSet(S, b.id)) { n++; if (b.label_when_done) labels.push(b.label_when_done + (S.board[b.id] === "parked" ? " (set aside)" : "")); } });
  return { done: n, of: live.length, labels: labels };
}
function choicesFor(arch, S, V) {         // the buttons the page shows when the active item is a pick or direction with its own options
  var a = activeState(S, V), b = a ? entry(V, a) : null;
  if (!b || (b.kind !== "pick" && b.kind !== "direction") || b.options_from === "equation_picks") return null;
  return { item: b.id, kind: b.kind, options: optionsOf(arch, V, b).map(function (o) { return { id: o.id, text: o.text }; }) };
}


// A student never draws the same problem twice while others remain (proposed step 6b). Pure: callers keep `served` per student
// and archetype. filters = { kind, opener } as the page sends them. When every matching variant has been served, the list is
// reset and `reset` is true so the caller can log it. Returns null when nothing matches the filters at all.
function chooseVariant(variants, filters, served, rand) {
  rand = rand || Math.random; served = served || [];
  var match = function (v) { return (!filters.kind || v.kind === filters.kind) && (filters.opener === undefined || filters.opener === "" || filters.opener === null || v.opener_index === Number(filters.opener)); };
  var pool = []; variants.forEach(function (v, i) { if (match(v)) pool.push(i); });
  if (!pool.length) return null;
  var fresh = pool.filter(function (i) { return served.indexOf(variants[i].variant_id) < 0; }), reset = false;
  if (!fresh.length) { fresh = pool; reset = true; }
  var idx = fresh[Math.floor(rand() * fresh.length)];
  return { index: idx, variant_id: variants[idx].variant_id, reset: reset, remaining: fresh.length - 1 };
}

if (typeof module !== "undefined") module.exports = { chooseVariant: chooseVariant, entry: entry, isSet: isSet, liveItems: liveItems, isLive: isLive, activeState: activeState, tick: tick, stateSatisfied: stateSatisfied, stageOf: stageOf, moveFor: moveFor, addPin: addPin, optionsOf: optionsOf, pickItemFor: pickItemFor, newSession: newSession, problemPayload: problemPayload, openerMedia: openerMedia, progress: progress, choicesFor: choicesFor };
