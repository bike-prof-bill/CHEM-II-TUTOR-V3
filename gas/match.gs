// match.gs — one module of the tutor shell (rebuild spec, step 4). Apps Script shares one global scope across files;
// in Node, Core.gs loads every module and makes its exports global, so plain function declarations work in both.
function eqSide(text, arch, fromLeft) {
  var words = text.trim().split(/\s+/);
  for (var k = 0; k < words.length; k++) {
    var piece = (fromLeft ? words.slice(k) : words.slice(0, words.length - k)).join(" ").replace(/[.,;:]+$/, "");
    var tk = eqTokens(piece, arch); if (!tk || !tk.length) continue;
    try { return { tree: eqParse(tk), text: piece }; } catch (e) { }
  }
  return null;
}
function holdsOn(L, R, states) {
  return states.every(function (env) { var l = eqEval(L, env), r = eqEval(R, env);
    return isFinite(l) && isFinite(r) && Math.abs(l - r) <= 1e-6 * Math.max(Math.abs(l), Math.abs(r), 1e-12); });
}
function holdsAny(L, R, ck) { return holdsOn(L, R, ck["true"]) || (ck.alt || []).some(function (st) { return holdsOn(L, R, st); }); }
// Returns one result per typed equation line: which rearrangement it settles, or what is wrong with it.
function checkEquation(msg, V, arch, S) {
  var checks = (V.eq_checks || []).filter(function (ck) { return !S || !isSet(S, ck.state); });
  if (!checks.length || String(msg).indexOf("=") < 0) return [];
  var out = [];
  String(msg).split(/\n|;|(?<=[a-z])\.\s/).forEach(function (line) {
    checks.forEach(function (ck) {                          // "49 = (2x)^2/(0.2-x)^2" is read as "K = ..." when 49 is K
      for (var sym in (ck.literal_for || {})) {
        var val = ck.literal_for[sym], m = /^\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*=/.exec(line);
        if (m && Math.abs(parseFloat(m[1]) - val) <= 0.01 * Math.abs(val) + 1e-12) line = line.replace(m[1], " " + sym + " ");
      }
    });
    var parts = line.split("="); if (parts.length < 2) return;
    var looksSymbolic = Object.keys(eqVarsInText(line, arch)).length >= 2;
    var L = eqSide(parts[parts.length - 2], arch, true), R = eqSide(parts[parts.length - 1], arch, false);
    if (!L || !R) { if (looksSymbolic) out.push({ verdict: "UNREADABLE", state: checks[0].state }); return; }
    if (Object.keys(eqVars(R.tree, eqVars(L.tree, {}))).length < 2) return;                 // "T1 = 300.8" is not a rearrangement
    var shown = (L.text + " = " + R.text).replace(/\s+/g, " "), rhs = eqVars(R.tree, {});
    // instructor, 11 Oct: "either side is fine with algebra". The unknown alone on the left OR on the right, the other side free of it.
    var lhs = eqVars(L.tree, {});
    var alone = function (ck) { return (L.tree.v === ck.unknown && !rhs[ck.unknown]) || (R.tree.v === ck.unknown && !lhs[ck.unknown]); };
    var valid = checks.filter(function (ck) { return alone(ck) && holdsAny(L.tree, R.tree, ck); })[0];
    if (valid) { out.push({ verdict: "VALID_ISOLATED", state: valid.state, shown: shown }); return; }
    var ck = checks.filter(function (k) { return L.tree.v === k.unknown || R.tree.v === k.unknown; })[0] || checks[0];  // judge it against the one it is aiming at
    var res = { verdict: "WRONG", state: ck.state, shown: shown };
    if (holdsAny(L.tree, R.tree, ck)) {
      // true, but solved for a different symbol than the one this problem asks for (the instructor's syringe and vent runs, 11 Oct:
      // P2 isolated when P1 was unknown; T2 when T1 was). Named, so the student is told which quantity is the unknown, not just "again".
      var other = (L.tree.v && L.tree.v !== ck.unknown && !rhs[L.tree.v]) ? L.tree.v : (R.tree.v && R.tree.v !== ck.unknown && !lhs[R.tree.v]) ? R.tree.v : null;
      res.verdict = other ? "WRONG_UNKNOWN" : "HOLDS_NOT_ISOLATED"; if (other) { res.isolated = other; res.unknown = ck.unknown; }
    }
    else for (var id in ck.bent) if (holdsOn(L.tree, R.tree, ck.bent[id])) { res.verdict = "TRAP"; res.trap = id; }
    // instructor, 11 Oct: the subscripts are relative; a student who calls the unknown by its partner's name and keeps every pair
    // swapped consistently has the right equation. The check's "relabel" pairs (data from the archetype) say which symbols pair.
    if (res.verdict !== "VALID_ISOLATED" && res.verdict !== "TRAP" && ck.relabel && ck.relabel.length) {
      var swap = {}; ck.relabel.forEach(function (pr) { swap[pr[0]] = pr[1]; swap[pr[1]] = pr[0]; });
      var partner = swap[ck.unknown];
      var isoL = L.tree.v === partner && !rhs[partner], isoR = R.tree.v === partner && !lhs[partner];
      if (partner && (isoL || isoR)) {
        var permute = function (env) { var o = {}; for (var k in env) o[swap[k] || k] = env[k]; return o; };
        var ck2 = { "true": ck["true"].map(permute), alt: (ck.alt || []).map(function (st) { return st.map(permute); }) };
        if (holdsAny(L.tree, R.tree, ck2)) { res.verdict = "VALID_ISOLATED"; res.relabeled = partner; delete res.isolated; delete res.unknown; }
      }
    }
    out.push(res);
  });
  return out;
}

function cellEqual(a, b, arch) {                            // two expressions in x agree on three values of x; numbers compare directly
  var ta = eqTokens(String(a), arch), tb = eqTokens(String(b), arch); if (!ta || !tb || !ta.length || !tb.length) return false;
  try {
    var A = eqParse(ta), B = eqParse(tb);
    return [0.013, 0.027, 0.041].every(function (x) { var va = eqEval(A, { x: x }), vb = eqEval(B, { x: x }); return isFinite(va) && isFinite(vb) && Math.abs(va - vb) <= 1e-9 * Math.max(1, Math.abs(vb)); });
  } catch (e) { return false; }
}
function checkTable(rows, V, arch) {                        // -> { ok, wrong: [row letters], missing: [row letters] }
  var want = V.table, wrong = [], missing = [];
  ["C", "E"].forEach(function (r) {
    if (!rows[r]) { missing.push(r); return; }
    if (rows[r].length !== want.species.length || !rows[r].every(function (c, i) { return cellEqual(c, want.rows[r][i], arch); })) wrong.push(r);
  });
  if (rows.I && (rows.I.length !== want.species.length || !rows.I.every(function (c, i) { return cellEqual(c, want.rows.I[i], arch); }))) wrong.push("I");
  return { ok: !wrong.length && !missing.length, wrong: wrong, missing: missing };
}


// ---------- matching one number against everything the generator declared ----------
function near(x, v, tol) { return Math.abs(x - v) <= tol; }
// match(parsedNumber, expected, traps, ticked) -> { type, ids, id, needs, dimension }
//   type: "expected" (an intermediate or key; ids lists every declared entry hit, by index)
//         "needs_unit" (right value for an entry that requires its unit; needs = {idx, unit})
//         "wrong_dimension" (right value, but the typed unit is of another dimension; id = the entry)
//         "trap" (a known wrong turn for a state not yet set; id = trap id)
//         "given" | "constant" (a declared number that establishes nothing; a bare constant outranks a trap)
//         "stray" (matches nothing)
// A typed unit must equal the declared form's unit (no silent conversion: converting IS the student's step).
// A bare number matches any form by value, but cannot tick an entry that requires a unit.
// Pure: reads only its arguments. `ticked` is the set of states already set, as {state: true}.
// `accepted` (optional): values the student has already had accepted, by entry id. An entry with `derive` is graded against them:
// expected = derive.base - accepted[derive.from] (The Drinking Bird's pressure difference, graded against the student's own head
// pressure so its allowance is not counted twice). Such an entry is skipped until the entry it depends on has been accepted.
function match(n, expected, traps, ticked, accepted) {
  var hits = [], needs = null, wrongDim = null, given = null, constant = null; accepted = accepted || {};
  for (var i = 0; i < expected.length; i++) {
    var t = expected[i], forms;
    if (t.derive) {
      if (accepted[t.derive.from] === undefined) continue;
      var dv = t.derive.base - accepted[t.derive.from];
      forms = [{ value: dv, unit: t.unit, abs_tol: t.abs_tol }, { value: -dv, unit: t.unit, abs_tol: t.abs_tol }];
    } else forms = [{ value: t.value, unit: t.unit, abs_tol: t.abs_tol }].concat(t.also || []);
    for (var f = 0; f < forms.length; f++) {
      var F = forms[f], fu = F.unit || "";
      if (!near(n.x, F.value, F.abs_tol)) continue;
      if (n.unit && fu && n.unit !== fu) {                       // same value, other unit: conversion or dimension error
        if (!UNITS.vecSame(UNITS.dim(n.unit), UNITS.dim(fu)) && !wrongDim) wrongDim = { idx: i, unit: fu };
        continue;
      }
      if (n.unit && !fu) continue;                                 // a unit on a unitless quantity is not that quantity
      if (t.role === "given") { given = given || i; break; }
      if (t.role === "constant") { constant = constant || i; break; }
      if (!n.unit && t.require_unit && fu) { if (!needs) needs = { idx: i, unit: fu, x: n.x }; break; }
      hits.push(i); break;
    }
  }
  if (hits.length) return { type: "expected", ids: hits, needs: needs };
  if (needs) return { type: "needs_unit", ids: [], needs: needs };
  // A bare number that is a declared constant is that constant, before any trap: "step 2" is not the 1.9 K
  // a kJ-for-J slip produces. Typed WITH a unit, the same number cannot be a constant and reaches the traps.
  if (constant !== null && !n.unit) return { type: "constant", id: expected[constant].id };
  if (given !== null) return { type: "given", id: expected[given].id };   // a restated given is the given, before any trap (11 Oct)
  for (var k = 0; k < traps.length; k++) {                 // value traps first, then bounds
    var tr = traps[k];
    if (ticked[tr.state] || tr.value === undefined) continue;
    if (!near(n.x, tr.value, tr.abs_tol)) continue;
    if (n.unit && tr.unit && n.unit !== tr.unit) continue;
    return { type: "trap", id: tr.id, trap: tr };
  }
  for (var k2 = 0; k2 < traps.length; k2++) {
    var tb = traps[k2];
    if (ticked[tb.state] || tb.above === undefined) continue;
    if (n.unit && tb.unit && n.unit !== tb.unit) continue;
    if (n.x > tb.above) return { type: "trap", id: tb.id, trap: tb };
  }
  if (constant !== null) return { type: "constant", id: expected[constant].id };
  if (wrongDim) return { type: "wrong_dimension", id: expected[wrongDim.idx].id, unit: wrongDim.unit, typed: n.unit };
  // instructor, 11 Oct: a calculated number outside the window but near an unmet intermediate or key, matching no trap, is a near miss
  // (a calculator slip): the tutor asks which values they used. The nearest such entry is named; nothing is accepted.
  var best = null;
  for (var j = 0; j < expected.length; j++) {
    var e = expected[j]; if (e.derive || ticked[e.state] || (e.role !== "intermediate" && e.role !== "key")) continue;
    var fs = [{ value: e.value, unit: e.unit }].concat(e.also || []);
    for (var g = 0; g < fs.length; g++) {
      var G = fs[g], gu = G.unit || ""; if (!G.value) continue;
      if (n.unit && gu && n.unit !== gu) continue; if (n.unit && !gu) continue;
      var rel = Math.abs(n.x - G.value) / Math.abs(G.value);
      if (rel <= NEAR_MISS_FRACTION && (!best || rel < best.rel)) best = { idx: j, rel: rel };
    }
  }
  if (best) return { type: "near_miss", id: expected[best.idx].id, idx: best.idx, state: expected[best.idx].state };
  return { type: "stray" };
}
var NEAR_MISS_FRACTION = 0.10;   // outside the grading window, within this fraction of the expected value (instructor, 11 Oct)
function tickedSet(S) { var t = {}; for (var st in S.board) if (isSet(S, st)) t[st] = true; return t; }
function acceptedValues(S, V) { var a = {}; V.expected.forEach(function (e, i) { if (S.values && S.values[i] !== undefined) a[e.id] = S.values[i]; }); return a; }
function classify(n, S, V) { return match(n, V.expected, V.traps, tickedSet(S), acceptedValues(S, V)); }

if (typeof module !== "undefined") module.exports = { NEAR_MISS_FRACTION: NEAR_MISS_FRACTION, acceptedValues: acceptedValues, eqSide: eqSide, holdsOn: holdsOn, holdsAny: holdsAny, checkEquation: checkEquation, cellEqual: cellEqual, checkTable: checkTable, near: near, match: match, tickedSet: tickedSet, classify: classify };
