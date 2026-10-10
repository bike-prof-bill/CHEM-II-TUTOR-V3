// parse.gs — one module of the tutor shell (rebuild spec, step 4). Apps Script shares one global scope across files;
// in Node, Core.gs loads every module and makes its exports global, so plain function declarations work in both.
var UNITS_DATA = (typeof UNITS_DATA !== "undefined") ? UNITS_DATA : (typeof require !== "undefined" ? require("./Units.gs") : null);

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
  // label words are removed before the mechanism count, so "evaporates" does not count as the mechanism word "vapor"
  var labels = 0, rest = low; (opener.label_words || []).forEach(function (w) { var lw = w.toLowerCase(); if (rest.indexOf(lw) > -1) { labels++; rest = rest.split(lw).join(" "); } });
  var mech = 0; MECHANISM.forEach(function (w) { if (rest.indexOf(w) > -1) mech++; });
  // a label word (volatile, evaporates) with no mechanism word names the phenomenon without saying what particles do: not an account
  var labelOnly = labels > 0 && mech === 0;
  return { hits: hits, mech: mech, labels: labels, labelOnly: labelOnly, engaged: !labelOnly && (hits > 0 || mech >= 2) };
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

function eqVarsInText(line, arch) {                        // a symbol counts only when it stands apart from other letters
  var f = {}, s = eqNormalize(line);
  for (var v in arch.equation_symbols) arch.equation_symbols[v].forEach(function (al) {
    var i = -1; while ((i = s.indexOf(al, i + 1)) > -1) { if (!/[A-Za-zΔ°]/.test(s[i - 1] || " ") && !/[A-Za-z0-9_]/.test(s[i + al.length] || " ")) f[v] = 1; } });   // "T" inside "T1" is not the symbol T
  return f;
}

// Is this message a question or a plea for help, whatever its punctuation? "what do you mean", "i do not know", "how do I",
// "which one", "huh", "help", "explain", "not sure", "confused", "lost", "stuck". Used only when the message carries no
// number, equation, table or pick; a sentence that answers is never mistaken for a question by this test.
function isAskingForHelp(msg) {
  var m = String(msg || "").trim().toLowerCase(); if (!m) return false;
  if (/\?\s*$/.test(m)) return true;
  if (/^(what|why|how|which|where|when|who|do|does|did|is|are|am|can|could|should|would|will|was|were|have|has|isn't|aren't|don't|doesn't|didn't|can't|couldn't|shouldn't|wouldn't)\b/.test(m)) return true;
  return /\b(what do you mean|i (do not|don't|dont) (know|understand|get it|follow)|not sure|no idea|confused|i'?m lost|stuck|help( me)?|explain|huh|pardon|say (that )?again|meaning of|what is a|what's a)\b/.test(m);
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

if (typeof module !== "undefined") module.exports = { UNITS: UNITS, SUP: SUP, GENERIC_MECHANISM: GENERIC_MECHANISM, MATH_WORDS: MATH_WORDS, parseNumbers: parseNumbers, stopWords: stopWords, hasAccount: hasAccount, openerCoverage: openerCoverage, EQ_FUNCS: EQ_FUNCS, eqNormalize: eqNormalize, eqTokens: eqTokens, eqParse: eqParse, eqEval: eqEval, eqVars: eqVars, eqVarsInText: eqVarsInText, isAskingForHelp: isAskingForHelp, evalArithmetic: evalArithmetic, parseTableText: parseTableText };
