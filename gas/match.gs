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
    var valid = checks.filter(function (ck) { return L.tree.v === ck.unknown && !rhs[ck.unknown] && holdsAny(L.tree, R.tree, ck); })[0];
    if (valid) { out.push({ verdict: "VALID_ISOLATED", state: valid.state, shown: shown }); return; }
    var ck = checks.filter(function (k) { return L.tree.v === k.unknown; })[0] || checks[0];  // judge it against the one it is aiming at
    var res = { verdict: "WRONG", state: ck.state, shown: shown };
    if (holdsAny(L.tree, R.tree, ck)) res.verdict = "HOLDS_NOT_ISOLATED";
    else for (var id in ck.bent) if (holdsOn(L.tree, R.tree, ck.bent[id])) { res.verdict = "TRAP"; res.trap = id; }
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
function match(n, expected, traps, ticked) {
  var hits = [], needs = null, wrongDim = null, given = null, constant = null;
  for (var i = 0; i < expected.length; i++) {
    var t = expected[i];
    var forms = [{ value: t.value, unit: t.unit, abs_tol: t.abs_tol }].concat(t.also || []);
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
      if (!n.unit && t.require_unit && fu) { if (!needs) needs = { idx: i, unit: fu }; break; }
      hits.push(i); break;
    }
  }
  if (hits.length) return { type: "expected", ids: hits, needs: needs };
  if (needs) return { type: "needs_unit", ids: [], needs: needs };
  // A bare number that is a declared constant is that constant, before any trap: "step 2" is not the 1.9 K
  // a kJ-for-J slip produces. Typed WITH a unit, the same number cannot be a constant and reaches the traps.
  if (constant !== null && !n.unit) return { type: "constant", id: expected[constant].id };
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
  if (given !== null) return { type: "given", id: expected[given].id };
  if (constant !== null) return { type: "constant", id: expected[constant].id };
  if (wrongDim) return { type: "wrong_dimension", id: expected[wrongDim.idx].id, unit: wrongDim.unit, typed: n.unit };
  return { type: "stray" };
}
function tickedSet(S) { var t = {}; for (var st in S.board) if (isSet(S, st)) t[st] = true; return t; }
function classify(n, S, V) { return match(n, V.expected, V.traps, tickedSet(S)); }

if (typeof module !== "undefined") module.exports = { eqSide: eqSide, holdsOn: holdsOn, holdsAny: holdsAny, checkEquation: checkEquation, cellEqual: cellEqual, checkTable: checkTable, near: near, match: match, tickedSet: tickedSet, classify: classify };
