// Core.gs  --  V3 tutor logic. No Google objects in this file.
// Runs unchanged in Apps Script, in Node (tests), and later on Netlify.
//
// The idea in one paragraph: a problem is a BOARD of states to establish. `requires` is the only
// ordering rule. The computer ticks states from what the student types or picks; the model only
// talks, and judges the two free-text states (the opening account and the closing inference),
// where a second independent reading can overrule it. Two counted wrong tries on a state produce
// a notebook card with no model call. Two more after the student returns parks the state.

// Change 2 (rebuild spec): the verifier guesses nothing. Every number it recognises was declared by the
// generator (`expected`, `traps`); every unit it reads comes from units.json (via Units.gs). No constant
// list, no "small integers are constants", no stray-number closure. A number matching nothing is stray.

var UNITS_DATA = (typeof UNITS_DATA !== "undefined") ? UNITS_DATA : (typeof require !== "undefined" ? require("./Units.gs") : null);

var CORE = (function () {

  // ---------- units as data: dimension vectors, conversion, aliases ----------
  var UNITS = (function (D) {
    var byAlias = {}, aliases = [];
    for (var u in D.units) {
      D.units[u].aliases.forEach(function (a) { byAlias[a.replace(/\s+/g, "").toLowerCase()] = u; aliases.push(a); });
    }
    aliases.sort(function (a, b) { return b.length - a.length; });
    function vecAdd(a, b, sign) { var out = {}, k; for (k in a) out[k] = (out[k] || 0) + a[k]; for (k in b) out[k] = (out[k] || 0) + sign * b[k]; for (k in out) if (Math.abs(out[k]) < 1e-9) delete out[k]; return out; }
    function vecSame(a, b) { return Object.keys(vecAdd(a || {}, b || {}, -1)).length === 0; }
    function dim(u) { var x = D.units[u]; return x ? D.dimensions[x.dimension].dim : null; }
    function convert(x, from, to) {               // value in `from` -> value in `to`, or null when the dimensions differ
      var a = D.units[from], b = D.units[to]; if (!a || !b || a.dimension !== b.dimension) return null;
      return ((x * a.factor + a.offset) - b.offset) / b.factor;
    }
    function canon(alias) { return alias ? (byAlias[alias.replace(/\s+/g, "").toLowerCase()] || null) : null; }
    var esc = function (a) { return a.replace(/[.*+?^${}()|[\]\\\/]/g, "\\$&").replace(/\s+/g, "\\s*"); };
    var unitPattern = aliases.map(esc).join("|");
    return { dim: dim, convert: convert, canon: canon, vecSame: vecSame, unitPattern: unitPattern, aliases: aliases, data: D };
  })(UNITS_DATA);

  var SUP = { "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9", "⁻": "-", "⁺": "+" };
  var GENERIC_MECHANISM = ["molecul", "particl", "atom", "ion", "electron", "collid", "collis", "energ"];   // used only if the archetype lists none

  // ---------- reading what the student typed ----------
  function parseNumbers(msg) {
    var s = String(msg || "").replace(/[−–]/g, "-").replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+/g, function (m) {
      return "^" + m.split("").map(function (c) { return SUP[c]; }).join("");
    });
    var re = new RegExp("(?<![A-Za-z_\\d.^])([-+]?(?:\\d{1,3}(?:,\\d{3})+|\\d+)(?:\\.\\d+)?|[-+]?\\.\\d+)(?:\\s*(?:[eE]|[x×*]\\s*10\\s*\\^?)\\s*([-+]?\\d+))?\\s*(" + UNITS.unitPattern + ")?(?![A-Za-z])", "g");
    var out = [], m;
    while ((m = re.exec(s)) !== null) {
      var x = parseFloat(m[1].replace(/,/g, ""));
      if (m[2]) x = x * Math.pow(10, parseInt(m[2], 10));
      if (!isFinite(x)) continue;
      out.push({ x: x, unit: m[3] ? UNITS.canon(m[3]) : null });
    }
    return out;
  }

  // Ported from V2 unchanged in spirit: three prose words in a row is an account; four if there is an equation.
  // Words that are not prose: every unit alias (units.json), every symbol the archetype lets a student type, and math words.
  var MATH_WORDS = "ln log exp delta eq soln aq min hr sec".split(" ");
  function stopWords(arch) {
    var stop = {};
    UNITS.aliases.forEach(function (a) { stop[a.toLowerCase()] = 1; });
    MATH_WORDS.forEach(function (w) { stop[w] = 1; });
    if (arch && arch.equation_symbols) for (var v in arch.equation_symbols) arch.equation_symbols[v].forEach(function (a) { stop[a.toLowerCase()] = 1; });
    return stop;
  }
  function hasAccount(message, arch) {
    var stop = stopWords(arch);
    var toks = String(message || "").split(/\s+/), run = 0, best = 0;
    for (var i = 0; i < toks.length; i++) {
      var t = toks[i].replace(/[,;:()"'?!]/g, ""), ends = /\.$/.test(t); t = t.replace(/\.$/, "");
      var prose = t.length >= 2 && !/[=×·^]|\d/.test(t) && /^[A-Za-zΔ][A-Za-zΔ°'-]*$/.test(t) && !stop[t.toLowerCase()];
      if (prose) { run++; if (run > best) best = run; if (ends) run = 0; } else run = 0;
    }
    return best >= (/=/.test(String(message || "")) ? 4 : 3);
  }

  function openerCoverage(text, opener, arch) {
    var MECHANISM = (arch && arch.mechanism_words && arch.mechanism_words.length) ? arch.mechanism_words : GENERIC_MECHANISM;
    var low = String(text || "").toLowerCase(), hits = 0;
    (opener.keywords || []).forEach(function (k) {
      var ok = k.toLowerCase().split(/\s+/).every(function (w) { return w.length < 4 || low.indexOf(w.slice(0, Math.min(6, w.length - 1))) > -1; });
      if (ok) hits++;
    });
    var mech = 0; MECHANISM.forEach(function (w) { if (low.indexOf(w) > -1) mech++; });
    return { hits: hits, mech: mech, engaged: hits > 0 || mech >= 2 };
  }


  // ---------- reading a typed equation, and checking it by substitution ----------
  // Never matched against a list of acceptable strings. Any algebraically valid form passes, and a wrong one is
  // named by which bent version of the relation it satisfies. "log" is base 10; "ln" is natural.
  var EQ_FUNCS = { ln: Math.log, log: Math.log10, exp: Math.exp, sqrt: Math.sqrt };
  function eqNormalize(t) {
    return String(t).replace(/[−–—]/g, "-").replace(/[×·⋅•]/g, "*").replace(/÷/g, "/").replace(/[\[{]/g, "(").replace(/[\]}]/g, ")")
      .replace(/[₀-₉]/g, function (c) { return String(c.charCodeAt(0) - 0x2080); })
      .replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+/g, function (m) { return "^(" + m.split("").map(function (c) { return SUP[c]; }).join("") + ")"; });
  }
  function eqTokens(text, arch) {
    var alias = [], s = eqNormalize(text), out = [], i = 0;
    for (var v in arch.equation_symbols) arch.equation_symbols[v].forEach(function (a) { alias.push([a, v]); });
    alias.sort(function (a, b) { return b[0].length - a[0].length; });
    while (i < s.length) {
      var c = s[i];
      if (/\s/.test(c)) { i++; continue; }
      if ("+-*/^()".indexOf(c) > -1) { out.push({ t: c }); i++; continue; }
      var m = /^(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?/.exec(s.slice(i));
      if (m) { out.push({ t: "num", v: parseFloat(m[0]) }); i += m[0].length; continue; }
      var hit = null;
      for (var a = 0; a < alias.length && !hit; a++) if (s.substr(i, alias[a][0].length) === alias[a][0]) hit = alias[a];
      if (hit) { out.push({ t: "var", v: hit[1] }); i += hit[0].length; continue; }
      var w = /^[A-Za-z]+/.exec(s.slice(i));
      if (w) {
        var word = w[0];
        if (EQ_FUNCS[word]) out.push({ t: "fn", v: word });
        else if (arch.equation_constants[word] !== undefined) out.push({ t: "num", v: arch.equation_constants[word] });
        else if (word === "e") out.push({ t: "num", v: Math.E });
        else return null;                                   // a word: this stretch is prose, not algebra
        i += word.length; continue;
      }
      return null;
    }
    return out;
  }
  function eqParse(tokens) {                                  // + -  <  * / implied-multiply  <  unary -  <  ^
    var p = 0;
    function peek() { return tokens[p]; }
    function startsFactor(k) { return k && (k.t === "num" || k.t === "var" || k.t === "fn" || k.t === "("); }
    function expr() { var n = term(); while (peek() && (peek().t === "+" || peek().t === "-")) { var op = tokens[p++].t; n = { op: op, a: n, b: term() }; } return n; }
    function term() {
      var n = unary();
      while (peek() && (peek().t === "*" || peek().t === "/" || startsFactor(peek()))) {
        var op = startsFactor(peek()) ? "*" : tokens[p++].t; n = { op: op, a: n, b: unary() };
      }
      return n;
    }
    function unary() { if (peek() && peek().t === "-") { p++; return { op: "neg", a: unary() }; } if (peek() && peek().t === "+") { p++; return unary(); } return power(); }
    function power() { var b = atom(); if (peek() && peek().t === "^") { p++; return { op: "^", a: b, b: unary() }; } return b; }
    function atom() {
      var k = tokens[p++]; if (!k) throw "end";
      if (k.t === "num") return { num: k.v };
      if (k.t === "var") return { v: k.v };
      if (k.t === "fn") {                                   // ln(x), and the textbook's bare "ln P": the function takes the very next factor, no more
        if (peek() && peek().t === "(") { p++; var a = expr(); if (!peek() || peek().t !== ")") throw "paren"; p++; return { fn: k.v, a: a }; }
        return { fn: k.v, a: power() };
      }
      if (k.t === "(") { var e = expr(); if (!peek() || peek().t !== ")") throw "paren"; p++; return e; }
      throw "unexpected";
    }
    var tree = expr(); if (p !== tokens.length) throw "trailing"; return tree;
  }
  function eqEval(n, env) {
    if (n.num !== undefined) return n.num; if (n.v) return env[n.v]; if (n.fn) return EQ_FUNCS[n.fn](eqEval(n.a, env));
    var a = eqEval(n.a, env); if (n.op === "neg") return -a; var b = eqEval(n.b, env);
    return n.op === "+" ? a + b : n.op === "-" ? a - b : n.op === "*" ? a * b : n.op === "/" ? a / b : Math.pow(a, b);
  }
  function eqVars(n, set) { if (!n) return set; if (n.v) set[n.v] = 1; eqVars(n.a, set); eqVars(n.b, set); return set; }
  // Find the algebra inside a sentence: trim words off the left of the left side and the right of the right side until both parse.
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
  function eqVarsInText(line, arch) {                        // a symbol counts only when it stands apart from other letters
    var f = {}, s = eqNormalize(line);
    for (var v in arch.equation_symbols) arch.equation_symbols[v].forEach(function (al) {
      var i = -1; while ((i = s.indexOf(al, i + 1)) > -1) { if (!/[A-Za-zΔ°]/.test(s[i - 1] || " ") && !/[A-Za-z0-9_]/.test(s[i + al.length] || " ")) f[v] = 1; } });   // "T" inside "T1" is not the symbol T
    return f;
  }

  // A statement whose right side is numbers joined by + - * / ^ and brackets, optionally ending in a unit: its value.
  // Returns null when there is no operator (a plain number is read by parseNumbers) or when a symbol is present (algebra).
  function evalArithmetic(text, arch) {
    var t = eqNormalize(String(text)).replace(/(\d),(?=\d{3}\b)/g, "$1").trim(), unit = null;
    var um = new RegExp("\\s*(" + UNITS.unitPattern + ")\\s*$").exec(t);
    if (um) { unit = UNITS.canon(um[1]); t = t.slice(0, um.index); }
    if (!/[+\-*\/^]/.test(t.replace(/^\s*[-+]/, "")) || !/\d/.test(t)) return null;
    if (!/^[\d.\s+\-*\/^()eE]+$/.test(t) || /[eE](?![+\-]?\d)/.test(t)) return null;
    var toks = eqTokens(t, arch); if (!toks || !toks.length || toks.some(function (k) { return k.t === "var"; })) return null;
    try { var v = eqEval(eqParse(toks), {}); return isFinite(v) ? { x: v, unit: unit, worked: true } : null; } catch (e) { return null; }
  }

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

  // ---------- the table kind: a grid of rows (initial, change, equilibrium) over columns; numbers and expressions in x, checked by substitution ----------
  function parseTableText(msg) {
    var rows = {}, re = /^\s*(I|C|E|initial|change|equilibrium)\b[\s:|]*(.+)$/i;
    String(msg).split(/\n/).forEach(function (line) {
      var m = re.exec(line); if (!m) return;
      var key = m[1][0].toUpperCase();
      rows[key] = m[2].split(/\s*[|,\t]\s*|\s{2,}/).map(function (c) { return c.trim(); }).filter(function (c) { return c.length; });
    });
    return (rows.C || rows.E) ? rows : null;
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

  // ---------- prompts ----------
  var RULES = [
    "You are a General Chemistry II tutor working Socratically with one student. The server checks every number and every pick and tells you below what happened this turn. Trust the server over your own impression.",
    "1. Exactly one question per reply. One question mark.",
    "2. Never do the math, never state a value the student has not produced, never hand over the set-up inside a question.",
    "3. Never call something correct that the server has not confirmed. Acknowledge by naming what was right in the student's own words, not by praising.",
    "4. A name or an analogy is not an account. Ask what the particles are doing.",
    "5. A physical quantity needs its units.",
    "6. Never ask a yes/no question or one answered by reading the problem.",
    "7. Plain text only. No LaTeX, no caret. Unicode superscripts are fine.",
    "8. Name which account the student is in when it helps: particles (never seen, inferred), symbols (the bridge), or measurement (what an instrument reads).",
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

  function unearned(reply, S, V) {      // a number from the answer key that the student has not produced
    var bad = [];
    parseNumbers(reply).forEach(function (n) {
      var c = match(n, V.expected, V.traps, {});
      if ((c.type === "expected" || c.type === "needs_unit" || c.type === "trap") &&
          !S.produced.some(function (p) { return near(p, n.x, 1e-6 * Math.abs(n.x) + 1e-12); })) bad.push(n.x);
    });
    return bad;
  }

  // ---------- one turn ----------
  // model(system, history, message) -> parsed JSON object, or null when no model is available.
  function processTurn(arch, S, input, model) {
    var V = arch.variants[S.variantIndex], msg = String(input.message || ""), history = input.history || [];
    var ev = { event_type: "TURN", entering: progress(S, V).done, active: activeState(S, V), newly: [], traps: [], guards: [],
      counted_fail: false, after_bailout: false, model_accept: "", second_reader: "", fallback_used: false, structured: "" };
    var notes = [], reply = null, card = null;
    S.turns++;
    var active = ev.active, b = active ? entry(V, active) : null, move = active ? moveFor(arch, V, active) : {};

    // --- coming back from the notebook: say what you learned, then carry on. Never counted as a try.
    if (S.awaitingReturn) {
      ev.after_bailout = true; ev.event_type = "RETURN_ACCOUNT";
      if (hasAccount(msg, arch)) { S.awaitingReturn = null; notes.push("The student has just returned from the course notebook and said what they learned. Acknowledge it in a clause, then ask the question for the item above."); }
      else return finish(arch, S, V, ev, moveFor(arch, V, S.awaitingReturn).return_ask || "In your own words, what did the notebook show you?", null);
    }

    // --- a pick: from the Equations list, from an approach/method list, or a direction. Typed direction words count too.
    var pickId = input.pick || null;
    if (!pickId && b && b.kind === "direction" && msg) {
      var hitsDir = optionsOf(arch, V, b).filter(function (o) { return new RegExp("\\b" + o.text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "\\b", "i").test(msg); });
      if (hitsDir.length === 1) pickId = hitsDir[0].id;
    }
    if (pickId) {
      ev.structured = pickId;
      var pb = pickItemFor(arch, S, V, pickId), opt = pb ? optionsOf(arch, V, pb).filter(function (o) { return o.id === pickId; })[0] : null;
      if (!pb) notes.push("The student picked an option that belongs to no open item. Ignore it.");
      else if (opt.right) {
        tick(S, V, pb.id, ev.newly); S.picks[pb.id] = pickId;
        if (pb.id === "relation_chosen") S.pinned.relation = opt.text;
        if (pb.pin) addPin(S, pb.id, pb.label_when_done || pb.id, opt.text);
        notes.push(pb.kind === "direction" ? "The student's prediction is right. Confirmed by the server. Do not explain why; ask them to." : "The student picked the right option. Confirmed by the server.");
      } else {
        notes.push(pb.kind === "direction" ? "The student's prediction is wrong. Do not give the right one. Ask what must be true of the amounts for their prediction to hold."
                                           : "The student picked an option that does not fit this problem. Do not name the right one.");
        if (active === pb.id) ev.counted_fail = true;
      }
    }

    // --- a table: structured from the page, or typed as lines beginning I / C / E
    var tableRows = input.table || (b && b.kind === "table" ? parseTableText(msg) : null), tableSeen = false, tableBad = false;
    if (tableRows && V.table) {
      tableSeen = true; var tr = checkTable(tableRows, V, arch); ev.structured = (ev.structured ? ev.structured + " " : "") + "TABLE:" + (tr.ok ? "OK" : tr.wrong.concat(tr.missing).join(""));
      var tb = V.board.filter(function (x) { return x.kind === "table"; })[0];
      if (tr.ok) {
        if (tb && !isSet(S, tb.id)) { tick(S, V, tb.id, ev.newly); if (tb.pin) addPin(S, tb.id, tb.label_when_done || "table", V.table.species.join(" | ") + "\n" + ["I", "C", "E"].map(function (r) { return r + ": " + V.table.rows[r].join(" | "); }).join("\n")); }
        notes.push("The student's table is right: initial, change and equilibrium rows all check under substitution. Confirmed by the server.");
      } else {
        tableBad = true;
        if (tr.missing.length) notes.push("The table is missing its " + tr.missing.map(function (r) { return ({ C: "change", E: "equilibrium", I: "initial" })[r]; }).join(" and ") + " row. Ask for it; do not supply it.");
        if (tr.wrong.length) notes.push("TABLE CHECK: the " + tr.wrong.map(function (r) { return ({ C: "change", E: "equilibrium", I: "initial" })[r]; }).join(" and ") + " row does not hold under substitution. Do not correct it. Ask about one cell of THEIR row: how many of that species one reaction event makes or uses.");
      }
    }

    // --- typed equations: each mandatory rearrangement or expression, checked by substitution
    var eqs = tableSeen ? [] : checkEquation(msg, V, arch, S), eqBad = false, eqSeen = eqs.length > 0;
    eqs.forEach(function (eqr) {
      ev.structured = (ev.structured ? ev.structured + " " : "") + "EQ:" + eqr.verdict;
      var eb = entry(V, eqr.state);
      if (eqr.verdict === "VALID_ISOLATED") {
        if (!isLive(S, V, eqr.state) || !eb.requires.every(function (r) { return isSet(S, r); })) notes.push("Their equation is valid, but an earlier item is not yet established. Ask them to do that first.");
        else { tick(S, V, eqr.state, ev.newly); (S.pinned.rearranged = S.pinned.rearranged || []).push(eqr.shown); if (eb.pin) addPin(S, eqr.state, eb.label_when_done || eqr.state, eqr.shown); notes.push("The student's equation holds under substitution and the unknown stands alone. Confirmed by the server."); }
      } else if (eqr.verdict === "HOLDS_NOT_ISOLATED") notes.push("Their equation is algebraically true but the unknown does not yet stand alone on the left. That is progress, not an error. Ask what operation is still in the way. Do not do it for them.");
      else if (eqr.verdict === "TRAP") { eqBad = true; ev.traps.push(eqr.trap); notes.push("EQUATION CHECK (" + eqr.trap + "): " + arch.trap_notes[eqr.trap].note + " Work on THEIR expression, one step at a time. Do not write the correct form."); }
      else if (eqr.verdict === "WRONG") { eqBad = true; notes.push("EQUATION CHECK: their equation does not hold when the server substitutes values. Read what they wrote, not what they meant (an unbracketed denominator is a real error). Ask about one step of THEIR algebra. Do not write the correct form."); }
      else notes.push("The server could not read their equation. Ask them to retype it on one line with brackets around every numerator and denominator.");
    });

    // --- numbers: read only from lines that are neither symbolic algebra nor table rows
    // "T1 = 357.15 K, T2 = 320.65 K", "... K T2 = ...", "... K and T2 = ..." are two statements: split before any "name =" that
    // follows a comma, a semicolon, the word "and", or just a space (instructor, 9 Oct). A comma inside 38,600 is left alone.
    var numText = String(msg).split(/\n|;|,?\s+(?:and\s+)?(?=[A-Za-zΔ][A-Za-z0-9_]*\s*=)/i).map(function (line) {
      if (tableSeen && /^\s*(I|C|E|initial|change|equilibrium)\b/i.test(line)) return "";
      if (line.indexOf("=") > -1 && Object.keys(eqVarsInText(line, arch)).length >= 2) {
        var rhs = line.slice(line.lastIndexOf("=") + 1);        // "P2/P1 = 0.587" states a value: read the right side only
        return Object.keys(eqVarsInText(rhs, arch)).length ? "" : rhs;   // "ln P2 - ln P1 = ΔHvap/R (1/T1 - 1/T2)" is algebra: read nothing
      }
      return line; }).join("\n");
    // arithmetic shown in a value statement, "T2 = (273.15 + 47.5) K" or "760 * 0.323 torr": the worked result is what the student
    // means, and the numbers inside it are not read on their own (so a 47.5 inside the sum is not a stray)
    var worked = [], plainLines = [];
    numText.split(/\n/).forEach(function (line) {
      var rhs = line.indexOf("=") > -1 ? line.slice(line.lastIndexOf("=") + 1) : line, a = evalArithmetic(rhs, arch);
      if (a) worked.push(a); else plainLines.push(line);
    });
    var nums = parseNumbers(plainLines.join("\n")).concat(worked), strays = 0, unitOnly = (!nums.length && S.pendingUnit !== null) ? parseNumbers("1 " + msg)[0] : null;
    if (unitOnly && unitOnly.unit) {                       // "K" sent on its own after a bare number
      var pt = V.expected[S.pendingUnit.idx];
      if (unitOnly.unit === S.pendingUnit.unit) { S.matched[S.pendingUnit.idx] = true; S.pendingUnit = null; notes.push(pt.label + ": units supplied. Confirmed."); }
      else if (!UNITS.vecSame(UNITS.dim(unitOnly.unit), UNITS.dim(S.pendingUnit.unit))) { ev.guards.push("WRONG_DIMENSION"); notes.push("The unit they supplied is of a different kind of quantity than the one asked for. Do not accept it. Ask what kind of quantity this value is."); }
    }
    nums.forEach(function (n) {
      S.produced.push(n.x);
      var c = classify(n, S, V);
      if (c.type === "expected" || c.type === "needs_unit") {
        c.ids.forEach(function (ix) { S.matched[ix] = true; });
        if (c.needs && !S.matched[c.needs.idx]) { S.pendingUnit = c.needs; notes.push("The value for '" + V.expected[c.needs.idx].label + "' is right but has no units. Ask for the units. Do not advance."); }
      } else if (c.type === "trap") { ev.traps.push(c.trap.id); var tn = arch.trap_notes[c.trap.id]; notes.push("KNOWN WRONG TURN (" + c.trap.id + "): " + (tn ? tn.note : "") + " Do not name the fix. Ask one question aimed at it."); }
      else if (c.type === "wrong_dimension") { ev.guards.push("WRONG_DIMENSION"); strays++; notes.push("The number is right for one step but carries a unit of a different kind of quantity (" + c.typed + "). Do not accept it. Ask what kind of quantity that value measures."); }
      else if (c.type === "stray") strays++;
    });
    liveItems(S, V).forEach(function (bb) { if (bb.kind === "number" && !isSet(S, bb.id) && stateSatisfied(S, V, bb.id)) tick(S, V, bb.id, ev.newly); });
    ev.newly.forEach(function (st) { var e = entry(V, st); if (e && e.kind === "number") notes.push("Established and checked by the server: " + (e.label_when_done || st.replace(/_/g, " ")) + "."); });
    var keyWaiting = V.expected.some(function (t, i) { return t.role === "key" && S.matched[i] && !isSet(S, t.state); }) &&
                     liveItems(S, V).some(function (bb) { return (bb.kind === "equation" || bb.kind === "table") && !isSet(S, bb.id); });
    if (keyWaiting) notes.push("Their final value is right and is recorded, but it does not count until the symbolic step before it is on the board. Say so plainly and ask for that step.");
    if ((eqBad && b && b.kind === "equation") || (tableBad && b && b.kind === "table")) ev.counted_fail = true;
    else if ((eqSeen && !eqBad) || (tableSeen && !tableBad)) { /* a readable, true equation or table is never a wrong try */ }
    else if (b && b.kind !== "text" && b.kind !== "reflection" && !ev.newly.length && S.pendingUnit === null && (ev.traps.length || strays)) {
      ev.counted_fail = true; if (strays && !ev.traps.length) notes.push("The student's number does not match anything the server expects at this point. Do not confirm it.");
    }

    // --- recompute where we are after deterministic ticking
    active = activeState(S, V); b = active ? entry(V, active) : null; move = active ? moveFor(arch, V, active) : {};
    // the reflection: a sentence of their own closes it; never graded, never a wrong try
    if (b && b.kind === "reflection" && ev.active === active && !pickId && msg) {
      if (hasAccount(msg, arch)) { tick(S, V, active, ev.newly); notes.push("The student has written their reflection. Acknowledge it in a clause; do not grade it."); active = activeState(S, V); b = active ? entry(V, active) : null; move = active ? moveFor(arch, V, active) : {}; }
      else notes.push("The reflection needs a sentence of their own. Ask again, plainly.");
    }
    var judge = !!(b && b.kind === "text" && ev.active === active && !pickId && !tableSeen), gateOK = true;
    if (judge) {
      if (!hasAccount(msg, arch)) { gateOK = false; notes.push("The message is not yet an account: no sentence of their own. Do not accept."); }
      else if (active === "account_given") {
        var cov = openerCoverage(msg, arch.openers[S.openerIndex], arch);
        if (!cov.engaged) { gateOK = false; ev.guards.push("OPENER_NOT_ENGAGED"); notes.push("The account touches nothing in the opening scenario and says nothing about particles. Do not accept. Ask what the particles in THIS scenario are doing."); }
      }
    }

    // --- the model speaks (and, for the text items, judges)
    var lastItem = !!(b && liveItems(S, V).every(function (x) { return x.id === b.id || isSet(S, x.id); }));
    var ctx = { progress: progress(S, V), active: active, register: b ? b.register : "", ask: move.ask, notes: notes, judge: judge && gateOK, lastItem: lastItem };
    var accepted = false, kind = /\?\s*$/.test(msg) && !nums.length ? "question" : "answer";
    var failStage = ev.active ? stageOf(V, ev.active) : null;
    var willBail = ev.counted_fail && b && b.kind !== "text" && ((S.tries[failStage] || 0) + 1) >= 2;   // known before any model call
    if (!willBail) {
      var out = model ? safe(model, buildSystem(arch, S, V, ctx), history, msg) : null;
      if (out) {
        reply = out.socratic_response; kind = out.turn_kind || kind; ev.model_accept = out.accept ? 1 : 0;
        if (judge && gateOK && out.accept) {
          accepted = true;
          var sr = safe(model, "You are checking one student message for a FALSE statement about the chemistry. Reply strict JSON {\"found\":0|1,\"quote\":\"exact words from the message\",\"why\":\"...\"}. If nothing is false, found is 0. Do not judge completeness.", [], msg);
          if (sr && sr.found && sr.quote && msg.indexOf(sr.quote) > -1) {
            accepted = false; ev.second_reader = "FALSE_CLAIM"; ev.guards.push("REPLY_AFFIRMED_ERROR");
            ctx.judge = false; ctx.extra = "A second reader found a false statement in the student's message: \"" + sr.quote + "\" (" + sr.why + "). Do not accept. Do not correct it for them. Ask one question aimed at it.";
            var redo = safe(model, buildSystem(arch, S, V, ctx), history, msg); reply = redo ? redo.socratic_response : null;
          } else ev.second_reader = sr ? "clean" : "unavailable";
        }
      } else if (judge && gateOK) { accepted = true; ev.model_accept = "no_model"; }     // offline: the gates alone decide
      if (accepted) { tick(S, V, active, ev.newly); }
      if (judge && !accepted && hasAccount(msg, arch) && kind === "answer") ev.counted_fail = true;
    }
    if (kind === "question" || kind === "offtopic") ev.counted_fail = false;

    // --- wrong-try ladder, PER STAGE: 1 -> ask from another account, 2 -> notebook card, 2 more after return -> park the stage
    var failState = ev.active;
    if (ev.counted_fail && failState && !isSet(S, failState)) {
      var stg = stageOf(V, failState);
      S.tries[stg] = (S.tries[stg] || 0) + 1;
      var fm = moveFor(arch, V, failState);
      if (S.tries[stg] >= 2 && !S.bailed[stg]) {
        S.bailed[stg] = true; S.tries[stg] = 0; S.away = { state: failState, stage: stg, since: input.now || 0 };
        ev.event_type = "BAILOUT_ISSUED";
        card = { prompt: fm.notebook_prompt || "", url: arch.notebook_url, return_ask: fm.return_ask || "" };
        reply = "Let's pause here. Copy the prompt below into the course notebook, work through what it gives you, then come back and press I'm back.";
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
        reply = (handed.length ? "Here is that piece so you can keep going: " + handed.join(" ; ") + " " : "We will set that piece aside. ") + (nm.ask || "");
      } else if (S.tries[stg] === 1 && !ev.traps.length && fm.switch_ask && !model) reply = fm.switch_ask;
      else if (S.tries[stg] === 1 && fm.switch_ask && model && !ev.traps.length) {
        ctx.extra = "They are stuck inside one account. Move them to a different one. Ask toward this instead: " + fm.switch_ask; ctx.judge = false;
        var sw = safe(model, buildSystem(arch, S, V, ctx), history, msg); if (sw) reply = sw.socratic_response;
      }
    }

    // --- a completed problem does not end on a question (instructor, 9 Oct): one rewrite, then cut the question off
    var nowActive = activeState(S, V), nowMove = nowActive ? moveFor(arch, V, nowActive) : {};
    if (reply && !card && nowActive === null && /\?/.test(reply)) {
      ev.guards.push("QUESTION_AFTER_COMPLETION");
      ctx.active = null; ctx.judge = false; ctx.progress = progress(S, V); ctx.extra = "The problem is complete. Your draft asked a question. Rewrite: acknowledge what the student established, one or two sentences, no question.";
      var r3 = model ? safe(model, buildSystem(arch, S, V, ctx), history, msg) : null;
      reply = (r3 && !/\?/.test(r3.socratic_response)) ? r3.socratic_response
            : reply.split(/(?<=[.!])\s+/).filter(function (sn) { return !/\?/.test(sn); }).join(" ").trim() || null;
    }
    if (reply && !card) {
      var leaked = unearned(reply, S, V);
      if (leaked.length) {
        ev.guards.push("REPLY_STATED_VALUE");
        ctx.active = nowActive; ctx.ask = nowMove.ask; ctx.judge = false; ctx.progress = progress(S, V);
        ctx.extra = "Your draft stated a value the student has not produced (" + leaked.join(", ") + "). Rewrite without it.";
        var r2 = model ? safe(model, buildSystem(arch, S, V, ctx), history, msg) : null;
        reply = (r2 && !unearned(r2.socratic_response, S, V).length) ? r2.socratic_response : null;
      }
    }
    if (!reply) {                                           // offline mode, model failure, or guard failure
      ev.fallback_used = true;
      var ack = ev.newly.length ? "Checked: " + ev.newly.map(function (st) { var e = entry(V, st.replace(/\(parked\)$/, "")); return (e && e.label_when_done) || st.replace(/_/g, " "); }).join(", ") + ". " : "";
      var trapAsk = ev.traps.length && arch.trap_notes[ev.traps[0]] ? arch.trap_notes[ev.traps[0]].ask : "";
      reply = nowActive ? ack + (trapAsk || (S.pendingUnit !== null ? "What are the units of that value?" : (nowMove.ask || arch.openers[S.openerIndex].question)))
                        : ack + "That completes this problem.";
      // words only (no number, no equation, no pick) at a checkable item, or the same question twice with nothing new:
      // say what this item can actually take. Plain mode cannot read a sentence; it should not pretend it did not arrive.
      var nb = nowActive ? entry(V, nowActive) : null;
      var wordsOnly = !!msg.trim() && !nums.length && !eqSeen && !tableSeen && !pickId && S.pendingUnit === null;
      if (nb && !ev.newly.length && !trapAsk && (wordsOnly || reply === S.lastReply)) {
        var hint = { number: "This step is checked on the value: type it, with its unit.", equation: "This step is checked on the equation: type it on one line, the unknown alone on the left.",
                     pick: "This step is a choice: open the Equations list.", direction: "This step is a choice: pick one of the options.", table: "This step is checked on the table: type the three rows I:, C:, E:.",
                     text: "", reflection: "" }[nb.kind] || "";
        if (hint) reply = reply + " " + hint;
      }
    }
    S.lastReply = reply;
    ev.turn_kind = kind;
    return finish(arch, S, V, ev, reply, card);
  }

  function safe(model, system, history, msg) { try { return model(system, history, msg); } catch (e) { return null; } }

  function processBack(arch, S, now) {
    var V = arch.variants[S.variantIndex];
    var ev = { event_type: "BAILOUT_RETURN", entering: progress(S, V).done, active: S.away ? S.away.state : "", newly: [], traps: [], guards: [],
      counted_fail: false, after_bailout: true, seconds_away: S.away ? Math.round(((now || 0) - S.away.since) / 1000) : "" };
    var st = S.away ? S.away.state : null; S.awaitingReturn = st; S.away = null;
    return finish(arch, S, V, ev, (st && moveFor(arch, V, st).return_ask) || "In your own words, what did the notebook show you?", null);
  }

  var GATE_OF_KIND = { text: "G2", pick: "G1", direction: "G1", number: "G0", equation: "G0", table: "G0", reflection: "none" };
  function finish(arch, S, V, ev, reply, card) {
    var res = { reply: reply, progress: progress(S, V), card: card || null, pinned: S.pinned, pins: S.pins, choices: choicesFor(arch, S, V) };
    if (ev.newly.indexOf("account_given") > -1 || ev.newly.indexOf("account_given(parked)") > -1) res.problem = problemPayload(arch, V, S);
    var simState = V.board.filter(function (b) { return b.opens_sim; })[0];
    var simDue = (simState && isSet(S, simState.id)) || (!simState && activeState(S, V) === "meaning_given");
    if (V.sim && !S.simOpen && simDue) { S.simOpen = true; res.sim = V.sim; }
    // the instructor's own simulation page, if the opener names one: opens with the problem, or at the meaning stage
    var med = (arch.openers[S.openerIndex] && arch.openers[S.openerIndex].media) || {};
    if (med.simulation && !S.mediaSimOpen && ((med.simulation_opens === "account" && isSet(S, "account_given")) || (med.simulation_opens !== "account" && simDue))) {
      S.mediaSimOpen = true;                                 // {substance} in the path becomes this problem's substance, so one page can serve many
      var subst = (V.context && (V.context.true_substance || V.context.substance)) || "";
      res.simulation_url = med.simulation.replace(/\{substance\}/g, encodeURIComponent(subst));
    }
    if (!S.done && activeState(S, V) === null) {
      S.done = true; S.credit = S.clean && S.board["meaning_given"] === "ticked"; ev.completed = true;
    }
    res.done = S.done; res.credit = S.credit;
    var a = ev.active ? entry(V, ev.active) : null;
    res.log = { event_type: ev.event_type, attempt_id: S.attemptId, archetype_id: S.archetypeId, variant_id: S.variantId, problem_kind: V.kind,
      content_version: arch.content_version, state: ev.active || "", stage: a ? a.stage : "", register: a ? a.register : "",
      face: a ? a.face : "", gate: a ? GATE_OF_KIND[a.kind] : "",
      entering_done: ev.entering, leaving_done: res.progress.done, newly: ev.newly.join(","), tries_on_stage: a ? (S.tries[a.stage] || 0) : "",
      counted_fail: ev.counted_fail, after_bailout: !!ev.after_bailout, seconds_away: ev.seconds_away || "", trap_ids: (ev.traps || []).join(","),
      structured: ev.structured || "", model_accept: ev.model_accept === undefined ? "" : ev.model_accept, second_reader: ev.second_reader || "",
      guards: (ev.guards || []).join(","), fallback_used: !!ev.fallback_used, turn_kind: ev.turn_kind || "", clean: S.clean, done: S.done, credit: S.credit };
    return res;
  }

  return { parseNumbers: parseNumbers, hasAccount: hasAccount, openerCoverage: openerCoverage, newSession: newSession, match: match, units: UNITS,
    processTurn: processTurn, processBack: processBack, checkEquation: checkEquation, checkTable: checkTable, parseTableText: parseTableText,
    activeState: activeState, liveItems: liveItems, progress: progress, problemPayload: problemPayload, openerMedia: openerMedia, evalArithmetic: evalArithmetic };
})();
if (typeof module !== "undefined") module.exports = CORE;
