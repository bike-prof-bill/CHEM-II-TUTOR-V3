// Core.gs  --  V3 tutor logic. No Google objects in this file.
// Runs unchanged in Apps Script, in Node (tests), and later on Netlify.
//
// The idea in one paragraph: a problem is a BOARD of states to establish. `requires` is the only
// ordering rule. The computer ticks states from what the student types or picks; the model only
// talks, and judges the two free-text states (the opening account and the closing inference),
// where a second independent reading can overrule it. Two counted wrong tries on a state produce
// a notebook card with no model call. Two more after the student returns parks the state.

var CORE = (function () {

  var CONSTANTS = [8.314, 8.3145, 0.008314, 273.15, 273, 760, 101.325, 101.3, 0.08206, 1000, 100];
  var UNIT_ALIASES = { "k": "K", "kelvin": "K", "°c": "degC", "c": "degC", "degc": "degC", "celsius": "degC",
    "atm": "atm", "torr": "torr", "mmhg": "torr", "kpa": "kPa", "kj/mol": "kJ/mol", "kj": "kJ/mol", "j/mol": "J/mol", "j": "J/mol" };
  var SUP = { "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9", "⁻": "-", "⁺": "+" };
  var MECHANISM = ["molecul", "particl", "atom", "ion", "electron", "collid", "collis", "energ", "attract", "escap",
    "vapor", "vapour", "condens", "surface", "kinetic", "bond", "force", "fraction", "distribut"];

  // ---------- reading what the student typed ----------
  function parseNumbers(msg) {
    var s = String(msg || "").replace(/[−–]/g, "-").replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+/g, function (m) {
      return "^" + m.split("").map(function (c) { return SUP[c]; }).join("");
    });
    var re = /(?<![A-Za-z_\d.^])([-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|[-+]?\.\d+)(?:\s*(?:[eE]|[x×*]\s*10\s*\^?)\s*([-+]?\d+))?\s*(kJ\/mol|J\/mol|kelvin|celsius|°\s*C|degC|mmHg|torr|kPa|atm|kJ|K|C|J)?(?![A-Za-z])/g;
    var out = [], m;
    while ((m = re.exec(s)) !== null) {
      var x = parseFloat(m[1].replace(/,/g, ""));
      if (m[2]) x = x * Math.pow(10, parseInt(m[2], 10));
      if (!isFinite(x)) continue;
      var u = m[3] ? UNIT_ALIASES[m[3].replace(/\s/g, "").toLowerCase()] : null;
      out.push({ x: x, unit: u || null });
    }
    return out;
  }

  // Ported from V2 unchanged in spirit: three prose words in a row is an account; four if there is an equation.
  function hasAccount(message) {
    var stop = {}; ("atm mol mmol kg mg torr mmhg pa kpa bar kj mj kelvin celsius min hr sec mm cm ml " +
      "kf kb ka kc kp kw ksp dh ds dg dt dhvap ph poh pka delta eq soln aq ln log exp").split(" ").forEach(function (w) { stop[w] = 1; });
    var toks = String(message || "").split(/\s+/), run = 0, best = 0;
    for (var i = 0; i < toks.length; i++) {
      var t = toks[i].replace(/[,;:()"'?!]/g, ""), ends = /\.$/.test(t); t = t.replace(/\.$/, "");
      var prose = t.length >= 2 && !/[=×·^]|\d/.test(t) && /^[A-Za-zΔ][A-Za-zΔ°'-]*$/.test(t) && !stop[t.toLowerCase()];
      if (prose) { run++; if (run > best) best = run; if (ends) run = 0; } else run = 0;
    }
    return best >= (/=/.test(String(message || "")) ? 4 : 3);
  }

  function openerCoverage(text, opener) {
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
      var i = -1; while ((i = s.indexOf(al, i + 1)) > -1) { if (!/[A-Za-zΔ°]/.test(s[i - 1] || " ") && !/[A-Za-z]/.test(s[i + al.length] || " ")) f[v] = 1; } });
    return f;
  }

  // ---------- the board ----------
  function entry(V, state) { for (var i = 0; i < V.board.length; i++) if (V.board[i].state === state) return V.board[i]; return null; }
  function isSet(S, state) { return S.board[state] === "ticked" || S.board[state] === "parked"; }
  function activeState(S, V) {
    for (var i = 0; i < V.board.length; i++) {
      var b = V.board[i];
      if (!isSet(S, b.state) && b.requires.every(function (r) { return isSet(S, r); })) return b.state;
    }
    return null;
  }
  // Correct later work implies the symbolic steps before it. The two free-text bookends are never implied.
  function tick(S, V, state, newly) {
    if (isSet(S, state)) return;
    var b = entry(V, state); if (!b) return;
    b.requires.forEach(function (r) { var rb = entry(V, r); if (rb && rb.kind !== "text" && !rb.explicit) tick(S, V, r, newly); });
    if (!b.requires.every(function (r) { return isSet(S, r); })) return;
    S.board[state] = "ticked"; newly.push(state);
  }
  function stateSatisfied(S, V, state) {
    var b = entry(V, state), idx = [];
    V.targets.forEach(function (t, i) { if (t.state === state) idx.push(i); });
    if (!idx.length) return false;
    var got = idx.filter(function (i) { return S.matched[i]; }).length;
    return (b.rule === "any") ? got >= 1 : got === idx.length;
  }

  // ---------- matching one number against everything the factory said could appear ----------
  function near(x, v, tol) { return Math.abs(x - v) <= tol; }
  function classify(n, S, V) {
    // One number can be two things at once (P2 in atm IS the ratio P2/P1 when P1 is 1 atm). Collect every match.
    var hits = [], needs = null;
    for (var i = 0; i < V.targets.length; i++) {
      var t = V.targets[i];
      var forms = [{ value: t.value, unit: t.unit, abs_tol: t.abs_tol }].concat(t.also || []);
      for (var f = 0; f < forms.length; f++) {
        var F = forms[f];
        if (!near(n.x, F.value, F.abs_tol)) continue;
        if (n.unit && F.unit && n.unit !== F.unit) continue;
        if (!n.unit && t.require_unit && F.unit) { if (!needs) needs = { idx: i, unit: F.unit }; break; }
        hits.push(i); break;
      }
    }
    if (hits.length || needs) return { type: needs && !hits.length ? "needs_unit" : "target", idxs: hits, needs: needs };
    if (!n.unit && Math.abs(n.x) <= 10 && n.x === Math.round(n.x)) return { type: "const" };      // the 1 in 1/T is not an answer
    for (var k = 0; k < V.traps.length; k++) {
      var tr = V.traps[k];
      if (!isSet(S, tr.for_state) && near(n.x, tr.value, tr.abs_tol)) return { type: "trap", trap: tr };
    }
    for (var g in V.givens) if (near(n.x, V.givens[g].value, 1e-9 + 1e-6 * Math.abs(V.givens[g].value))) return { type: "given" };
    for (var c = 0; c < CONSTANTS.length; c++) if (near(n.x, CONSTANTS[c], 1e-3 * CONSTANTS[c])) return { type: "const" };
    if (!n.unit && Math.abs(n.x) <= 10 && n.x === Math.round(n.x)) return { type: "const" };
    return { type: "stray" };
  }

  // ---------- sessions ----------
  function newSession(arch, pick) {
    var V = arch.variants[pick.variantIndex];
    return { attemptId: "A" + pick.stamp, archetypeId: arch.archetype_id, variantId: V.variant_id, variantIndex: pick.variantIndex,
      openerIndex: (V.opener_index !== undefined ? V.opener_index : pick.openerIndex), board: {}, matched: {}, pendingUnit: null, tries: {}, bailed: {}, away: null,
      awaitingReturn: null, pinned: {}, clean: true, turns: 0, produced: [], done: false, credit: false, simOpen: false };
  }
  function problemPayload(arch, V) {        // what the browser is allowed to have once the account is given
    return { text: V.text, givens: V.givens, plots: V.reveal_with_problem || null,
      equations: arch.equation_picks.map(function (e) { return { id: e.id, text: e.text }; }) };
  }
  function progress(S, V) {
    var n = 0; V.board.forEach(function (b) { if (isSet(S, b.state)) n++; });
    return { done: n, of: V.board.length };
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
    else out += "\nEverything is established. Say so in one sentence. Ask nothing.";
    if (ctx.notes.length) out += "\n\nSERVER VERDICT THIS TURN:\n- " + ctx.notes.join("\n- ");
    if (ctx.judge) out += "\n\nYOU JUDGE THIS TURN: set accept to 1 only if the student's message establishes the item above. If you correct or redirect, accept is 0.";
    if (ctx.extra) out += "\n\n" + ctx.extra;
    return out;
  }

  function unearned(reply, S, V) {      // a number from the answer key that the student has not produced
    var bad = [];
    parseNumbers(reply).forEach(function (n) {
      var c = classify(n, { board: {}, matched: {} }, V);
      if ((c.type === "target" || c.type === "needs_unit" || c.type === "trap") &&
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
    var active = ev.active, b = active ? entry(V, active) : null, move = active ? (arch.moves[active] || {}) : {};

    // --- coming back from the notebook: say what you learned, then carry on. Never counted as a try.
    if (S.awaitingReturn) {
      ev.after_bailout = true; ev.event_type = "RETURN_ACCOUNT";
      if (hasAccount(msg)) { S.awaitingReturn = null; notes.push("The student has just returned from the course notebook and said what they learned. Acknowledge it in a clause, then ask the question for the item above."); }
      else return finish(arch, S, V, ev, (arch.moves[S.awaitingReturn] || {}).return_ask || "In your own words, what did the notebook show you?", null);
    }

    // --- a pick from the Equations list
    if (input.pick) {
      ev.structured = input.pick;
      var eq = arch.equation_picks.filter(function (e) { return e.id === input.pick; })[0];
      if (eq && eq.fits.indexOf(V.kind) > -1) { tick(S, V, "relation_chosen", ev.newly); S.pinned.relation = eq.text; notes.push("The student picked the right relation from the Equations list. Confirmed."); }
      else { notes.push("The student picked a relation that does not fit this problem. Do not name the right one."); if (active === "relation_chosen") ev.counted_fail = true; }
    }

    // --- typed equations: each mandatory rearrangement, checked by substitution
    var eqs = checkEquation(msg, V, arch, S), eqBad = false, eqSeen = eqs.length > 0;
    eqs.forEach(function (eqr) {
      ev.structured = (ev.structured ? ev.structured + " " : "") + "EQ:" + eqr.verdict;
      if (eqr.verdict === "VALID_ISOLATED") {
        if (isSet(S, "relation_chosen")) { tick(S, V, eqr.state, ev.newly); (S.pinned.rearranged = S.pinned.rearranged || []).push(eqr.shown); notes.push("The student's rearranged equation holds under substitution and the unknown stands alone. Confirmed by the server."); }
        else notes.push("Their rearranged equation is valid, but they have not yet picked the relation from the Equations list. Ask them to do that first.");
      } else if (eqr.verdict === "HOLDS_NOT_ISOLATED") notes.push("Their equation is algebraically true but the unknown does not yet stand alone on the left. That is progress, not an error. Ask what operation is still in the way. Do not do it for them.");
      else if (eqr.verdict === "TRAP") { eqBad = true; ev.traps.push(eqr.trap); notes.push("EQUATION CHECK (" + eqr.trap + "): " + arch.trap_notes[eqr.trap].note + " Work on THEIR expression, one step at a time. Do not write the correct form."); }
      else if (eqr.verdict === "WRONG") { eqBad = true; notes.push("EQUATION CHECK: their rearrangement does not hold when the server substitutes values. Read what they wrote, not what they meant (an unbracketed denominator is a real error). Ask about one step of THEIR algebra. Do not write the correct form."); }
      else notes.push("The server could not read their equation. Ask them to retype it on one line with brackets around every numerator and denominator.");
    });

    // --- numbers
    // numbers are read only from lines that are not symbolic algebra
    var numText = String(msg).split(/\n|;/).filter(function (line) { return !(line.indexOf("=") > -1 && Object.keys(eqVarsInText(line, arch)).length >= 2); }).join("\n");
    var nums = parseNumbers(numText), strays = 0, unitOnly = (!nums.length && S.pendingUnit !== null) ? parseNumbers("1 " + msg)[0] : null;
    if (unitOnly && unitOnly.unit) {                       // "K" sent on its own after a bare number
      var pt = V.targets[S.pendingUnit.idx];
      if (unitOnly.unit === S.pendingUnit.unit) { S.matched[S.pendingUnit.idx] = true; S.pendingUnit = null; notes.push(pt.label + ": units supplied. Confirmed."); }
    }
    nums.forEach(function (n) {
      S.produced.push(n.x);
      var c = classify(n, S, V);
      if (c.type === "target" || c.type === "needs_unit") {
        c.idxs.forEach(function (ix) { S.matched[ix] = true; });
        if (c.needs && !S.matched[c.needs.idx]) { S.pendingUnit = c.needs; notes.push("The value for '" + V.targets[c.needs.idx].label + "' is right but has no units. Ask for the units. Do not advance."); }
      } else if (c.type === "trap") { ev.traps.push(c.trap.id); var tn = arch.trap_notes[c.trap.id]; notes.push("KNOWN WRONG TURN (" + c.trap.id + "): " + (tn ? tn.note : "") + " Do not name the fix. Ask one question aimed at it."); }
      else if (c.type === "stray") strays++;
    });
    V.board.forEach(function (bb) { if (bb.kind === "number" && !isSet(S, bb.state) && stateSatisfied(S, V, bb.state)) tick(S, V, bb.state, ev.newly); });
    ev.newly.forEach(function (s) { if (entry(V, s).kind === "number") notes.push("Established and checked by the server: " + s.replace(/_/g, " ") + "."); });
    var keyWaiting = V.targets.some(function (t, i) { return t.is_key && S.matched[i] && !isSet(S, t.state); }) &&
                     V.board.some(function (bb) { return bb.kind === "equation" && !isSet(S, bb.state); });
    if (keyWaiting) notes.push("Their final value is right and is recorded, but it does not count until the rearranged relation is on the board. Say so plainly and ask for the rearrangement.");
    if (eqBad && b && b.kind === "equation") ev.counted_fail = true;
    else if (eqSeen && !eqBad) { /* a readable, true equation is never a wrong try */ }
    else if (b && b.kind !== "text" && !ev.newly.length && S.pendingUnit === null && (ev.traps.length || strays)) {
      ev.counted_fail = true; if (strays && !ev.traps.length) notes.push("The student's number does not match anything the server expects at this point. Do not confirm it.");
    }

    // --- recompute where we are after deterministic ticking
    active = activeState(S, V); b = active ? entry(V, active) : null; move = active ? (arch.moves[active] || {}) : {};
    var judge = !!(b && b.kind === "text" && ev.active === active && !input.pick), gateOK = true;
    if (judge) {
      if (!hasAccount(msg)) { gateOK = false; notes.push("The message is not yet an account: no sentence of their own. Do not accept."); }
      else if (active === "account_given") {
        var cov = openerCoverage(msg, arch.openers[S.openerIndex]);
        if (!cov.engaged) { gateOK = false; ev.guards.push("OPENER_NOT_ENGAGED"); notes.push("The account touches nothing in the opening scenario and says nothing about particles. Do not accept. Ask what the particles in THIS scenario are doing."); }
      }
    }

    // --- the model speaks (and, for the two text states, judges)
    var ctx = { progress: progress(S, V), active: active, register: b ? b.register : "", ask: move.ask, notes: notes, judge: judge && gateOK };
    var accepted = false, kind = /\?\s*$/.test(msg) && !nums.length ? "question" : "answer";
    var willBail = ev.counted_fail && b && b.kind !== "text" && ((S.tries[ev.active] || 0) + 1) >= 2;   // known before any model call
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
      if (judge && !accepted && hasAccount(msg) && kind === "answer") ev.counted_fail = true;
    }
    if (kind === "question" || kind === "offtopic") ev.counted_fail = false;

    // --- wrong-try ladder: 1 -> ask from another account, 2 -> notebook card, 2 more after return -> park
    var failState = ev.active;
    if (ev.counted_fail && failState && !isSet(S, failState)) {
      S.tries[failState] = (S.tries[failState] || 0) + 1;
      var fm = arch.moves[failState] || {};
      if (S.tries[failState] >= 2 && !S.bailed[failState]) {
        S.bailed[failState] = true; S.tries[failState] = 0; S.away = { state: failState, since: input.now || 0 };
        ev.event_type = "BAILOUT_ISSUED";
        card = { prompt: fm.notebook_prompt || "", url: arch.notebook_url, return_ask: fm.return_ask || "" };
        reply = "Let's pause here. Copy the prompt below into the course notebook, work through what it gives you, then come back and press I'm back.";
      } else if (S.tries[failState] >= 2) {
        S.board[failState] = "parked"; S.clean = false; ev.event_type = "PARK"; ev.newly.push(failState + "(parked)");
        var pk = (V.eq_checks || []).filter(function (k) { return k.state === failState; })[0];
        if (pk) { fm = { park_text: pk.park_text }; (S.pinned.rearranged = S.pinned.rearranged || []).push(pk.park_text); }
        if (failState === "relation_chosen") { var right = arch.equation_picks.filter(function (e) { return e.fits.indexOf(V.kind) > -1; })[0]; if (right) S.pinned.relation = right.text; }
        V.board.forEach(function (bb) { if (bb.kind === "number" && !isSet(S, bb.state) && stateSatisfied(S, V, bb.state)) tick(S, V, bb.state, ev.newly); });
        var nxt = activeState(S, V), nm = nxt ? (arch.moves[nxt] || {}) : {};
        reply = (fm.park_text ? "Here is that piece so you can keep going: " + fm.park_text + " " : "We will set that piece aside. ") + (nm.ask || "");
      } else if (S.tries[failState] === 1 && !ev.traps.length && fm.switch_ask && !model) reply = fm.switch_ask;
      else if (S.tries[failState] === 1 && fm.switch_ask && model && !ev.traps.length) {
        ctx.extra = "They are stuck inside one account. Move them to a different one. Ask toward this instead: " + fm.switch_ask; ctx.judge = false;
        var sw = safe(model, buildSystem(arch, S, V, ctx), history, msg); if (sw) reply = sw.socratic_response;
      }
    }

    // --- nothing unchecked reaches the student: leak guard, one rewrite, then the authored question
    var nowActive = activeState(S, V), nowMove = nowActive ? (arch.moves[nowActive] || {}) : {};
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
      var ack = ev.newly.length ? "Checked: " + ev.newly.map(function (s) { return s.replace(/_/g, " "); }).join(", ") + ". " : "";
      var trapAsk = ev.traps.length && arch.trap_notes[ev.traps[0]] ? arch.trap_notes[ev.traps[0]].ask : "";
      reply = nowActive ? ack + (trapAsk || (S.pendingUnit !== null ? "What are the units of that value?" : (nowMove.ask || arch.openers[S.openerIndex].question)))
                        : ack + "That completes this problem.";
    }
    ev.turn_kind = kind;
    return finish(arch, S, V, ev, reply, card);
  }

  function safe(model, system, history, msg) { try { return model(system, history, msg); } catch (e) { return null; } }

  function processBack(arch, S, now) {
    var V = arch.variants[S.variantIndex];
    var ev = { event_type: "BAILOUT_RETURN", entering: progress(S, V).done, active: S.away ? S.away.state : "", newly: [], traps: [], guards: [],
      counted_fail: false, after_bailout: true, seconds_away: S.away ? Math.round(((now || 0) - S.away.since) / 1000) : "" };
    var st = S.away ? S.away.state : null; S.awaitingReturn = st; S.away = null;
    return finish(arch, S, V, ev, (st && arch.moves[st] && arch.moves[st].return_ask) || "In your own words, what did the notebook show you?", null);
  }

  function finish(arch, S, V, ev, reply, card) {
    var res = { reply: reply, progress: progress(S, V), card: card || null, pinned: S.pinned };
    if (ev.newly.indexOf("account_given") > -1 || ev.newly.indexOf("account_given(parked)") > -1) res.problem = problemPayload(arch, V);
    var simState = V.board.filter(function (b) { return b.opens_sim; })[0];
    if (!S.simOpen && ((simState && isSet(S, simState.state)) || (!simState && activeState(S, V) === "meaning_given"))) { S.simOpen = true; res.sim = V.sim; }
    if (!S.done && activeState(S, V) === null) {
      S.done = true; S.credit = S.clean && S.board["meaning_given"] === "ticked"; ev.completed = true;
    }
    res.done = S.done; res.credit = S.credit;
    var a = ev.active ? entry(V, ev.active) : null;
    res.log = { event_type: ev.event_type, attempt_id: S.attemptId, archetype_id: S.archetypeId, variant_id: S.variantId, problem_kind: V.kind,
      content_version: arch.content_version, state: ev.active || "", register: a ? a.register : "",
      face: a ? ({ pick: "choice", number: "check", equation: "check", text: "why" })[a.kind] : "", gate: a ? (a.kind === "text" ? "G2" : (a.kind === "pick" ? "G1" : "G0")) : "",
      entering_done: ev.entering, leaving_done: res.progress.done, newly: ev.newly.join(","), tries_on_state: ev.active ? (S.tries[ev.active] || 0) : "",
      counted_fail: ev.counted_fail, after_bailout: !!ev.after_bailout, seconds_away: ev.seconds_away || "", trap_ids: (ev.traps || []).join(","),
      structured: ev.structured || "", model_accept: ev.model_accept === undefined ? "" : ev.model_accept, second_reader: ev.second_reader || "",
      guards: (ev.guards || []).join(","), fallback_used: !!ev.fallback_used, turn_kind: ev.turn_kind || "", clean: S.clean, done: S.done, credit: S.credit };
    return res;
  }

  return { parseNumbers: parseNumbers, hasAccount: hasAccount, openerCoverage: openerCoverage, newSession: newSession,
    processTurn: processTurn, processBack: processBack, checkEquation: checkEquation, activeState: activeState, progress: progress, problemPayload: problemPayload };
})();
if (typeof module !== "undefined") module.exports = CORE;
