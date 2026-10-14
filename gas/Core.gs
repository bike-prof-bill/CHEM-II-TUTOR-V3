// Core.gs  --  the thin thing that orders the modules (rebuild spec, step 4). Chemistry-free: everything about a chapter arrives
// through Archetype_*.gs. The modules: parse (reading what was typed), match (verdicts on numbers, equations, tables),
// stepmap (items, branches, stages, pins), ladder (wrong tries), guards (what may reach the student), prompt (what the model
// is told), log (one row per turn). In Apps Script all files share one scope; in Node, Core loads them and makes them global.
//
// Every turn runs in two phases:
//   Phase A, verdict(arch, S, input)      deterministic only: parse, match, tick, branch, ladder, pins, card or park, progress.
//                                         No model call. A pure function of the message and the session: the thing replay tests.
//   Phase B, say(arch, S, input, model)   the model's draft, with the second reader run in parallel when the model offers batch;
//                                         text items are judged here; then the cheap checks, one rewrite, then the authored fallback.
// The page sends A, renders it at once, then sends B. Notebook-card and park turns skip B. processTurn = A then B, for callers
// that want one call (the test suites, the local server's plain mode).

if (typeof require !== "undefined") ["parse", "match", "stepmap", "ladder", "guards", "prompt", "log", "logqueue"].forEach(function (m) { Object.assign(global, require("./" + m + ".gs")); });

var CORE = (function () {

  // ---------- Phase A ----------
  function verdict(arch, S, input) {
    var t0 = Date.now();
    var V = arch.variants[S.variantIndex], msg = String(input.message || "");
    var ev = { event_type: "TURN", entering: progress(S, V).done, active: activeState(S, V), newly: [], traps: [], guards: [],
      counted_fail: false, after_bailout: false, model_accept: "", second_reader: "", fallback_used: false, structured: "", near_miss: "", repeat: false, second_reader_quote: "", units_check: "", units_fail: "", units_fn: "", wrong_unknown: null, demote: false };
    var notes = [];
    S.turns++;
    var active = ev.active, b = active ? entry(V, active) : null;

    // coming back from the notebook: a sentence on what they learned, then carry on. Never counted.
    if (S.awaitingReturn) {
      ev.after_bailout = true; ev.event_type = "RETURN_ACCOUNT";
      if (hasAccount(msg, arch)) { S.awaitingReturn = null; notes.push("The student has just returned from the course notebook and said what they learned. Acknowledge it in a clause, then ask the question for the item above."); }
      else return finishA(arch, S, V, ev, { reply: moveFor(arch, V, S.awaitingReturn).return_ask || "In your own words, what did the notebook show you?", card: null, needsSay: false }, t0);
    }

    // a pick: Equations list, an approach/method list, or a direction (typed direction words count too)
    var pickId = input.pick || null;
    if (!pickId && b && b.kind === "direction" && msg) {
      var esc = function (t) { return t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); };
      var hitsDir = optionsOf(arch, V, b).filter(function (o) { return new RegExp("\\b" + esc(o.text) + "\\b", "i").test(msg); });
      if (!hitsDir.length) hitsDir = optionsOf(arch, V, b).filter(function (o) { var w = o.text.split(/\s+/).filter(function (x) { return x.toLowerCase() !== "the"; })[0]; w = w && w.replace(/[:,.;!?]+$/, ""); return w && new RegExp("\\b" + esc(w) + "\\b", "i").test(msg); });   // the direction word alone ("the head pressure is lower", 11 Oct); a colon or comma after it is not part of the word (14 Oct)
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
        if (opt.names) { ev.traps.push(opt.names); notes.push("KNOWN WRONG TURN (" + opt.names + "): " + trapNote(arch, V, opt.names).note + " Do not name the fix. Ask one question aimed at it."); }   // a wrong option the archetype names (errors file carries the ask)
        if (active === pb.id) ev.counted_fail = true;
      }
    }

    // a table: structured from the page, or typed as lines beginning I / C / E
    var tableRows = input.table || (b && b.kind === "table" ? parseTableText(msg) : null), tableSeen = false, tableBad = false;
    if (tableRows && V.table) {
      tableSeen = true; var tr = checkTable(tableRows, V, arch); ev.structured = (ev.structured ? ev.structured + " " : "") + "TABLE:" + (tr.ok ? "OK" : tr.wrong.concat(tr.missing).join(""));
      var tb = V.board.filter(function (x) { return x.kind === "table"; })[0];
      if (tr.ok) {
        if (tb && !isSet(S, tb.id)) { tick(S, V, tb.id, ev.newly); if (tb.pin) addPin(S, tb.id, tb.label_when_done || "table", V.table.species.join(" | ") + "\n" + ["I", "C", "E"].map(function (r) { return r + ": " + V.table.rows[r].join(" | "); }).join("\n")); }
        notes.push("The student's table is right: initial, change and equilibrium rows all check under substitution. Confirmed by the server.");
      } else {
        tableBad = true;
        if (tr.trap) { ev.traps.push(tr.trap); notes.push("TABLE CHECK (" + tr.trap + "): " + trapNote(arch, V, tr.trap).note + " Do not correct it for them."); }
        if (tr.missing.length) notes.push("The table is missing its " + tr.missing.map(function (r) { return ({ C: "change", E: "equilibrium", I: "initial" })[r]; }).join(" and ") + " row. Ask for it; do not supply it.");
        if (tr.wrong.length) notes.push("TABLE CHECK: the " + tr.wrong.map(function (r) { return ({ C: "change", E: "equilibrium", I: "initial" })[r]; }).join(" and ") + " row does not hold under substitution. Do not correct it. Ask about one cell of THEIR row: how many of that species one reaction event makes or uses.");
      }
    }

    // typed equations: each mandatory rearrangement or expression, checked by substitution
    var eqs = tableSeen ? [] : checkEquation(msg, V, arch, S), eqBad = false, eqSeen = eqs.length > 0;
    eqs.forEach(function (eqr) {
      ev.structured = (ev.structured ? ev.structured + " " : "") + "EQ:" + eqr.verdict;
      var eb = entry(V, eqr.state);
      if (eqr.verdict === "VALID_ISOLATED") {
        if (!isLive(S, V, eqr.state) || !eb.requires.every(function (r) { return isSet(S, r); })) notes.push("Their equation is valid, but an earlier item is not yet established. Ask them to do that first.");
        else { tick(S, V, eqr.state, ev.newly); (S.pinned.rearranged = S.pinned.rearranged || []).push(eqr.shown); if (eb.pin) addPin(S, eqr.state, eb.label_when_done || eqr.state, eqr.shown); notes.push("The student's equation holds under substitution and the unknown stands alone. Confirmed by the server."); }
      } else if (eqr.verdict === "WRONG_UNKNOWN") {
        ev.wrong_unknown = { isolated: symbolShown(arch, eqr.isolated), unknown: symbolShown(arch, eqr.unknown) };
        notes.push("Their equation is true but solved for " + ev.wrong_unknown.isolated + "; this problem asks for " + ev.wrong_unknown.unknown + ". Say which quantity is the unknown here; do not rearrange it for them.");
      } else if (eqr.verdict === "HOLDS_NOT_ISOLATED") notes.push("Their equation is algebraically true but the unknown does not yet stand alone on one side. That is progress, not an error. Ask what operation is still in the way. Do not do it for them.");
      else if (eqr.verdict === "TRAP") { eqBad = true; ev.traps.push(eqr.trap); notes.push("EQUATION CHECK (" + eqr.trap + "): " + trapNote(arch, V, eqr.trap).note + " Work on THEIR expression, one step at a time. Do not write the correct form."); }
      else if (eqr.verdict === "WRONG") { eqBad = true; notes.push("EQUATION CHECK: their equation does not hold when the server substitutes values. Read what they wrote, not what they meant (an unbracketed denominator is a real error). Ask about one step of THEIR algebra. Do not write the correct form."); }
      else notes.push("The server could not read their equation. Ask them to retype it on one line with brackets around every numerator and denominator.");
    });

    // numbers: read only from lines that are neither symbolic algebra nor table rows. "T1 = 357.15 K, T2 = 320.65 K",
    // "... K T2 = ...", "... K and T2 = ..." are two statements (instructor, 9 Oct). A comma inside 38,600 is left alone.
    var numText = msg.split(/\n|;|,?\s+(?:and\s+)?(?=[A-Za-zΔ][A-Za-z0-9_]*\s*=)/i).map(function (line) {
      if (tableSeen && /^\s*(I|C|E|initial|change|equilibrium)\b/i.test(line)) return "";
      if (line.indexOf("=") > -1 && Object.keys(eqVarsInText(line, arch)).length >= 2) {
        var rhs = line.slice(line.lastIndexOf("=") + 1);        // "P2/P1 = 0.587" states a value: read the right side only
        return Object.keys(eqVarsInText(rhs, arch)).length ? "" : rhs;   // algebra on both sides: read nothing (the 1 in 1/T stays a 1)
      }
      return line; }).join("\n");
    // arithmetic in a value statement, "T2 = (273.15 + 47.5) K": the worked result is the value; its parts are not strays
    var worked = [], plainLines = [];
    var unitsFail = null;
    numText.split(/\n/).forEach(function (line) {
      var rhs = line.indexOf("=") > -1 ? line.slice(line.lastIndexOf("=") + 1) : line, a = evalArithmetic(rhs, arch);
      if (a) { worked.push(a); return; }
      // the setup typed in full with its units (instructor, 11 Oct: "units cancel algebraically"): a value in the unit the units cancel to,
      // or a failure (units that do not cancel inside ln, unlike units added) that is reported, not read for numbers.
      // "… = ΔHvap" puts the setup on the left: whichever side of the = works out is the setup
      var sides = line.indexOf("=") > -1 ? line.split("=") : [line];
      for (var si = 0; si < sides.length; si++) { if (!/[A-Za-z]/.test(sides[si])) continue; var wu = evalWithUnits(sides[si], arch); if (wu && wu.fail) { unitsFail = wu; return; } if (wu) { worked.push(wu); return; } }
      // several values on one line joined by &, "and", ";" or ", " (instructor's run, 11 Oct: "283.1K & (273.15 + 72.8)K"): each chunk
      // that works out is a value; the rest of the line is read as plain numbers
      // a chunk may carry words before it and a full stop after it ("it must be absolute. (273.15 + 46.7) K."): read from its first digit or bracket
      var chunks = rhs.split(/\s*&\s*|\s+and\s+|\s*;\s*|,\s+/i), rest = [];
      var trimmed = function (c) { var m = /[-+]?(?:\d|\()/.exec(c); return (m ? c.slice(m.index) : c).replace(/[.\s]+$/, ""); };
      if (chunks.length > 1) chunks.forEach(function (c) { var w = evalArithmetic(c, arch) || evalArithmetic(trimmed(c), arch); if (w) worked.push(w); else rest.push(c); });
      else { var w1 = evalArithmetic(trimmed(rhs), arch); if (w1) worked.push(w1); else rest.push(line); }
      if (rest.length) plainLines.push(rest.join(" "));
    });
    var nums = parseNumbers(plainLines.join("\n")).concat(worked), strays = 0, unitOnly = (!nums.length && S.pendingUnit !== null) ? parseNumbers("1 " + msg)[0] : null;
    if (unitOnly && unitOnly.unit) {                       // "K" sent on its own after a bare number
      var pt = V.expected[S.pendingUnit.idx];
      if (unitOnly.unit === S.pendingUnit.unit) { S.matched[S.pendingUnit.idx] = true; S.values = S.values || {}; S.values[S.pendingUnit.idx] = S.pendingUnit.x; S.pendingUnit = null; notes.push(pt.label + ": units supplied. Confirmed."); }
      else if (!UNITS.vecSame(UNITS.dim(unitOnly.unit), UNITS.dim(S.pendingUnit.unit))) { ev.guards.push("WRONG_DIMENSION"); notes.push("The unit they supplied is of a different kind of quantity than the one asked for. Do not accept it. Ask what kind of quantity this value is."); }
    }
    S.refused = S.refused || {};
    var repeats = 0, wrongs = 0;                            // instructor, 11 Oct: the same wrong number typed again is not a new attempt
    nums.forEach(function (n) {
      S.produced.push(n.x);
      var c = classify(n, S, V);
      if (c.type === "trap" || c.type === "near_miss" || c.type === "stray" || c.type === "wrong_dimension") {
        var rk = n.x + "|" + (n.unit || ""); wrongs++;
        if (S.refused[rk]) { repeats++; notes.push("This is the same number they typed before, refused then. It costs nothing this time. Say it is the same number; ask which values they used."); }
        S.refused[rk] = true;
      }
      if (c.type === "expected" || c.type === "needs_unit") {
        c.ids.forEach(function (ix) { S.matched[ix] = true; S.values = S.values || {};      // the student's own accepted value, in the entry's unit
          var e = V.expected[ix], v = n.x; if (n.unit && e.unit && n.unit !== e.unit) { var cv = UNITS.convert(n.x, n.unit, e.unit); if (cv !== null) v = cv; } S.values[ix] = v; });
        // a bare number that IS a declared intermediate is that intermediate; it does not also leave the key waiting for a unit
        // (a unitless ratio can equal the answer's value in another unit when the known quantity is 1 in that unit: found by the second scenario, 10 Oct)
        if (c.type === "needs_unit" && c.needs && !S.matched[c.needs.idx]) { S.pendingUnit = c.needs; notes.push("The value for '" + V.expected[c.needs.idx].label + "' is right but has no units. Ask for the units. Do not advance."); }
      } else if (c.type === "trap") { ev.traps.push(c.trap.id); notes.push("KNOWN WRONG TURN (" + c.trap.id + "): " + trapNote(arch, V, c.trap.id).note + " Do not name the fix. Ask one question aimed at it."); }
      else if (c.type === "wrong_dimension") { ev.guards.push("WRONG_DIMENSION"); strays++; notes.push("The number is right for one step but carries a unit of a different kind of quantity (" + c.typed + "). Do not accept it. Ask what kind of quantity that value measures."); }
      else if (c.type === "near_miss") { ev.near_miss = c.id; strays++; notes.push("The number is near '" + V.expected[c.idx].label + "' but outside the grading window: most likely an arithmetic slip. Do not say how close it is. Do not confirm it. Ask which values they used."); }
      else if (c.type === "stray") strays++;
    });
    if (wrongs && repeats === wrongs) { ev.repeat = true; strays = 0; ev.traps = []; }   // only repeats: no new wrong try, no new trap
    liveItems(S, V).forEach(function (bb) { if (bb.kind === "number" && !isSet(S, bb.id) && stateSatisfied(S, V, bb.id)) tick(S, V, bb.id, ev.newly); });
    ev.newly.forEach(function (st) { var e = entry(V, st); if (e && e.kind === "number") notes.push("Established and checked by the server: " + (e.label_when_done || st.replace(/_/g, " ")) + "."); });
    // units judged (instructor, 11 Oct): the target is what the active number item asks for, in any of its declared unit forms
    var targetUnits = [], anyUnits = [];                   // the active item's units; and every unmet number item's, since a full setup may land on a later one
    if (b && b.kind === "number") V.expected.forEach(function (e) {
      if (e.role !== "intermediate" && e.role !== "key" || !e.state || isSet(S, e.state)) return;
      var eb = entry(V, e.state); if (!eb || eb.kind !== "number" || !isLive(S, V, e.state)) return;
      [{ unit: e.unit }].concat(e.also || []).forEach(function (f) { var u = f.unit || ""; if (anyUnits.indexOf(u) < 0) anyUnits.push(u); if (e.state === b.id && targetUnits.indexOf(u) < 0) targetUnits.push(u); }); });
    S.calcWarned = S.calcWarned || {};
    if (unitsFail && b && b.kind === "number") {            // units that do not cancel: a wrong setup, counted, named by the unit produced
      ev.units_check = "dont_cancel:" + (unitsFail.produced || unitsFail.fail); ev.units_produced = unitsFail.produced || ""; ev.units_target = targetUnits.filter(Boolean).join(" or ");
      ev.units_fail = unitsFail.fail; ev.units_fn = unitsFail.fn || "";   // "function" (units left inside ln) or "mixed" (unlike units added)
      strays++; notes.push("The student typed the setup in full, but its units do not cancel (" + ev.units_check + "). The setup is wrong. Do not confirm. Ask which quantity is in the wrong place or the wrong unit.");
    }
    worked.forEach(function (n) {
      if (!n.units || !b || b.kind !== "number" || !targetUnits.length) return;
      var hit = ev.newly.length || (S.matched && V.expected.some(function (e, ix) { return S.matched[ix] && e.state === b.id; }));
      if (hit) return;                                        // the value was right: nothing to say about units
      if (anyUnits.indexOf(n.unit) > -1) {                    // units cancel to a unit some unmet step asks for: the setup is sound, the arithmetic is not
        ev.units_check = "ok_value_wrong"; ev.units_produced = n.unit; ev.units_target = n.unit;
        if (!S.calcWarned[b.id] && !ev.repeat) { S.calcWarned[b.id] = true; ev.units_free = true; }   // not a wrong try the first time
        notes.push("The student's setup has the right units (" + n.unit + "), so the setup is sound and the slip is in the arithmetic. Say the units come out right; ask them to check the calculation" + (ev.traps.length ? " (a known error is named above: say so)" : "") + ".");
      } else {                                                // a value, but not in the unit asked for
        ev.units_check = "dont_cancel:" + n.unit; ev.units_produced = n.unit; ev.units_target = targetUnits.filter(Boolean).join(" or ");
        notes.push("The student's setup works out in " + n.unit + ", not the unit this step asks for (" + ev.units_target + "). The setup is wrong. Ask which quantity is in the wrong place or the wrong unit.");
      }
    });
    var keyWaiting = V.expected.some(function (t, i) { return t.role === "key" && S.matched[i] && !isSet(S, t.state); }) &&
                     liveItems(S, V).some(function (bb) { return (bb.kind === "equation" || bb.kind === "table") && !isSet(S, bb.id); });
    if (keyWaiting) notes.push("Their final value is right and is recorded, but it does not count until the symbolic step before it is on the board. Say so plainly and ask for that step.");
    if ((eqBad && b && b.kind === "equation") || (tableBad && b && b.kind === "table")) ev.counted_fail = true;
    else if ((eqSeen && !eqBad) || (tableSeen && !tableBad)) { /* a readable, true equation or table is never a wrong try */ }
    else if (b && b.kind !== "text" && b.kind !== "reflection" && b.kind !== "pick" && b.kind !== "direction" && !ev.newly.length && S.pendingUnit === null && (ev.traps.length || strays)) {
      // units right, value wrong: free the first time on this item (instructor, 11 Oct)
      ev.counted_fail = !ev.units_free; if (strays && !ev.traps.length && !ev.units_check) notes.push("The student's number does not match anything the server expects at this point. Do not confirm it.");
    }

    // where we are after deterministic ticking
    active = activeState(S, V); b = active ? entry(V, active) : null;
    // the reflection: a sentence of their own closes it; never graded, never a wrong try
    if (b && b.kind === "reflection" && ev.active === active && !pickId && msg) {
      if (hasAccount(msg, arch)) { tick(S, V, active, ev.newly); notes.push("The student has written their reflection. Acknowledge it in a clause; do not grade it."); active = activeState(S, V); b = active ? entry(V, active) : null; }
      else notes.push("The reflection needs a sentence of their own. Ask again, plainly.");
    }
    // a text item: the gates decide what the model may judge
    var judge = !!(b && b.kind === "text" && ev.active === active && !pickId && !tableSeen), gateOK = true, labelOnly = false;
    if (judge) {
      if (!hasAccount(msg, arch)) { gateOK = false; notes.push("The message is not yet an account: no sentence of their own. Do not accept."); }
      else if (active === "account_given") {
        var cov = openerCoverage(msg, arch.openers[S.openerIndex], arch);
        if (cov.labelOnly) { gateOK = false; labelOnly = true; ev.guards.push("OPENER_LABEL_ONLY"); notes.push("The student named the phenomenon (a label such as volatile or evaporates) without saying what the particles are doing. That is a name, not an account. Do not accept; ask what the particles are doing. This turn costs them nothing."); }
        else if (!cov.engaged) { gateOK = false; ev.guards.push("OPENER_NOT_ENGAGED"); notes.push("The account touches nothing in the opening scenario and says nothing about particles. Do not accept. Ask what the particles in THIS scenario are doing."); }
      }
    }
    // a question or a plea for help, whatever its punctuation (instructor, 9 Oct): costs nothing
    var asking = !nums.length && !eqSeen && !tableSeen && !pickId && isAskingForHelp(msg);
    if (asking) { ev.counted_fail = false; notes.push("The student is asking for help or saying they are stuck, not answering. Answer their question plainly in one sentence, then ask the question for the item above. This turn costs them nothing."); }

    // the ladder on what Phase A counted (a text item's verdict waits for Phase B)
    var lad = applyLadder(arch, S, V, ev, input);
    var p = { notes: notes, judge: judge, gateOK: gateOK, labelOnly: labelOnly, asking: asking, pickId: pickId, eqSeen: eqSeen, tableSeen: tableSeen, numsSeen: nums.length,
              wordsOnly: !!msg.trim() && !nums.length && !eqSeen && !tableSeen && !pickId && S.pendingUnit === null,
              switchAsk: (ev.near_miss || ev.units_check) ? null : lad.switchAsk,     // a near miss is tutored by its own question, not the switch (instructor, 11 Oct)
              history: input.history || [], msg: msg, now: input.now || 0, verdict_ms: 0 };
    return finishA(arch, S, V, ev, { reply: lad.reply, card: lad.card, needsSay: !lad.card && !lad.reply, p: p }, t0);
  }

  // what Phase A returns: the page renders this at once. If needsSay, the turn waits in S.pending for Phase B.
  function finishA(arch, S, V, ev, a, t0) {
    var ms = Date.now() - t0;
    if (a.needsSay) {
      ev.turn_kind = a.p.asking ? "question" : "answer";
      S.pending = { ev: ev, p: a.p }; S.pending.p.verdict_ms = ms;
      var res = assemble(arch, S, V, ev, null, null, true);
      res.needs_say = true; res.checked = checkedLabels(V, ev); return res;
    }
    S.pending = null; S.lastReply = a.reply; ev.turn_kind = ev.turn_kind || "answer";
    var done = assemble(arch, S, V, ev, a.reply, a.card, false);
    done.needs_say = false; done.checked = checkedLabels(V, ev);
    done.log = logRow(arch, S, V, ev, done, { verdict_ms: ms, say_ms: 0 });
    return done;
  }
  function checkedLabels(V, ev) { return ev.newly.map(function (st) { var e = entry(V, st.replace(/\(parked\)$/, "")); return (e && e.label_when_done) || st.replace(/_/g, " "); }); }

  // ---------- Phase B ----------
  // model(system, history, msg) -> parsed JSON, or null. If model.batch([{system, history, msg}, ...]) exists, the draft and the
  // second reader go out together (fetchAll on Apps Script). With no model, the authored fallback speaks (plain mode).
  var CHECKABLE = { equation: true, number: true, table: true };
  function symbolShown(arch, v) { var a = arch.equation_symbols && arch.equation_symbols[v]; return (a && a[0]) || v; }
  // true: a false statement found by the second reader blocks acceptance even when the model accepts (the handoff's recorded decision,
  // "the second reader can overrule the first"). false: the instructor's 11 Oct wording read literally, one of the two readers suffices.
  var SECOND_READER_VETO = true;   // items the verifier decides; the authored question is what the tutor says there
  function say(arch, S, input, model) {
    var t0 = Date.now(), V = arch.variants[S.variantIndex];
    if (!S.pending) { var evx = { event_type: "SAY_WITHOUT_VERDICT", entering: progress(S, V).done, active: activeState(S, V), newly: [], traps: [], guards: [] }; var rx = assemble(arch, S, V, evx, "Press New problem.", null, false); rx.needs_say = false; return rx; }
    var ev = S.pending.ev, p = S.pending.p, msg = p.msg, history = p.history, notes = p.notes, reply = null, accepted = false, kind = ev.turn_kind;
    var active = activeState(S, V), b = active ? entry(V, active) : null, move = active ? moveFor(arch, V, active) : {};
    var lastItem = !!(b && liveItems(S, V).every(function (x) { return x.id === b.id || isSet(S, x.id); }));
    var ctx = { progress: progress(S, V), active: active, register: b ? b.register : "", ask: move.ask, notes: notes, judge: p.judge && p.gateOK, lastItem: lastItem };
    if (p.switchAsk) { ctx.extra = "They are stuck inside one account. Move them to a different one. Ask toward this instead: " + p.switchAsk; ctx.judge = false; }

    // A choice item (a pick from the Equations list, a prediction) is answered with buttons: the authored question is the whole of
    // what the tutor should say there, so the model is not asked to improvise one (instructor's run, 10 Oct: after a right prediction
    // the model asked its own "why" instead of sending the student to the Equations list).
    var choiceNext = !!(b && (b.kind === "pick" || b.kind === "direction") && !p.switchAsk && !ev.traps.length);
    // instructor, 11 Oct: the same for a checkable item (equation, number, table): the authored question is asked, the model may
    // acknowledge but not question (his run of the four: the model asked for the next step's unit conversion while the rearrangement was open).
    // A student asking for help still gets the model's one-sentence answer before the authored question.
    var checkNext = !!(b && (CHECKABLE[b.kind] || b.kind === "reflection") && !p.switchAsk && (!ev.traps.length || ev.units_check === "ok_value_wrong"));   // a near miss, a repeat or a units verdict: the authored question speaks
    var out = null, sr = null;
    if (model && (choiceNext || checkNext) && !ctx.judge && !p.asking) { model = null; }     // nothing to judge, nothing to answer: deterministic
    if (model) {
      if (model.batch && ctx.judge) { var both = safeBatch(model, [{ system: buildSystem(arch, S, V, ctx), history: history, msg: msg }, { system: SECOND_READER, history: [], msg: secondReaderMsg(arch, S, msg) }]); out = both[0]; sr = both[1]; }
      else { out = safe(model, buildSystem(arch, S, V, ctx), history, msg); if (ctx.judge) sr = safe(model, SECOND_READER, [], secondReaderMsg(arch, S, msg)); }
    }
    if (out) { reply = out.socratic_response; kind = out.turn_kind || kind; ev.model_accept = out.accept ? 1 : 0; }
    else if (ctx.judge) ev.model_accept = "no_model";
    if (ctx.judge) {
      // The computer gates have passed (a sentence of their own, engaging the scene, naming a mechanism). Instructor, 11 Oct, after the
      // model refused four true accounts in a row: the account is accepted when the gates and ONE of the two readers agree, i.e. the
      // model says accept, or the second reader finds nothing false. Both verdicts are logged. In plain mode the gates alone decide.
      var modelYes = !!(out && out.accept), srFalse = !!(sr && sr.found && sr.quote && msg.indexOf(sr.quote) > -1);
      ev.second_reader = sr ? (srFalse ? "FALSE_CLAIM" : "clean") : "unavailable";
      ev.second_reader_quote = (sr && sr.found) ? String(sr.quote || "") + " — " + String(sr.why || "") : "";   // so a disputed refusal can be read
      accepted = SECOND_READER_VETO ? !srFalse : (modelYes || !srFalse);
      if (!accepted && model) {                   // both readers against it: the model asks one question aimed at the false claim
        ev.guards.push("REPLY_AFFIRMED_ERROR");
        var c2 = Object.assign({}, ctx, { judge: false, extra: "A second reader found a false statement in the student's message: \"" + sr.quote + "\" (" + sr.why + "). Do not accept. Do not correct it for them. Ask one question aimed at it." });
        var redo = safe(model, buildSystem(arch, S, V, c2), history, msg); reply = redo ? redo.socratic_response : null;
      }
      if (accepted && srFalse) ev.guards.push("SECOND_READER_OVERRULED");          // the model accepted what the second reader flagged
      if (accepted && out && !modelYes) { ev.guards.push("MODEL_REFUSED_TRUE_ACCOUNT"); reply = null; }   // its draft was a hold-out question: the authored line speaks instead
    }
    if (accepted) tick(S, V, active, ev.newly);
    if (p.judge && !accepted && hasAccount(msg, arch) && kind === "answer") ev.counted_fail = true;
    if (kind === "question" || kind === "offtopic" || p.labelOnly) ev.counted_fail = false;    // a label is asked again, never counted
    ev.turn_kind = kind;

    // a text item's wrong try goes up the ladder here
    var card = null;
    if (ev.counted_fail && p.judge) { var lad = applyLadder(arch, S, V, ev, { now: p.now }); if (lad.card || lad.reply) { card = lad.card; reply = lad.reply; } else if (lad.switchAsk) p.switchAsk = lad.switchAsk; }

    // the cheap checks and the leak guard on the draft: one rewrite, then the authored fallback
    var done = activeState(S, V) === null;
    if (reply && !card) {
      var fails = checkDraft(reply, S, V, done, S.lastReply);
      if (fails.length) {
        fails.forEach(function (f) { if (ev.guards.indexOf(f) < 0) ev.guards.push(f); });
        var na = activeState(S, V);
        var c3 = Object.assign({}, ctx, { active: na, ask: na ? moveFor(arch, V, na).ask : "", judge: false, progress: progress(S, V), extra: rewriteInstruction(fails, reply, S, V) });
        var r2 = model ? safe(model, buildSystem(arch, S, V, c3), history, msg) : null;
        if (r2 && !checkDraft(r2.socratic_response, S, V, done, S.lastReply).length) reply = r2.socratic_response;
        else if (done && fails.length === 1 && fails[0] === "QUESTION_AFTER_COMPLETION") reply = cutQuestions(reply);
        else reply = null;
      }
    }
    if (!reply) { ev.fallback_used = true; reply = fallbackReply(arch, S, V, ev, p); }
    // a choice item next (after any acceptance this turn): the model's acknowledgement stays, its question gives way to the authored one
    var nowA = activeState(S, V), nowB = nowA ? entry(V, nowA) : null;
    // instructor, 11 Oct: the authored question everywhere. The model keeps its own question only where that question IS the tutoring:
    // a free-text attempt the gates or readers refused (nothing ticked, the same text item still active), a plea for help, a trap, a switch.
    var refusedText = nowB && nowB.kind === "text" && nowA === ev.active && !ev.newly.length;
    if (reply && !card && !ev.fallback_used && nowB && !refusedText && !p.switchAsk && (!ev.traps.length || ev.units_check === "ok_value_wrong")) {
      var nowAsk = (ev.units_check || ev.near_miss || ev.repeat || ev.wrong_unknown) ? nearMissAsk(arch, V, ev) : moveFor(arch, V, nowA).ask;
      var showB = (ev.newly.length && !ev.units_check && !ev.near_miss && !ev.repeat && !ev.wrong_unknown) ? showFor(arch, V, S, nowA) : "";
      if (nowAsk) { var ackOnly = cutQuestions(reply); reply = (ackOnly ? ackOnly + " " : "") + (showB || nowAsk); }   // Worked rung: the show cell is the whole prompt
    }
    S.lastReply = reply; S.pending = null;
    var res = assemble(arch, S, V, ev, reply, card, false);
    res.needs_say = false; res.checked = checkedLabels(V, ev);
    res.log = logRow(arch, S, V, ev, res, { verdict_ms: p.verdict_ms, say_ms: Date.now() - t0 });
    return res;
  }

  function safe(model, system, history, msg) { try { return model(system, history, msg); } catch (e) { return null; } }
  function safeBatch(model, reqs) { try { var r = model.batch(reqs); return reqs.map(function (_, i) { return (r && r[i]) || null; }); } catch (e) { return reqs.map(function () { return null; }); } }

  // ---------- both phases in one call (tests, plain-mode local server) ----------
  function processTurn(arch, S, input, model) {
    var a = verdict(arch, S, input);
    if (!a.needs_say) return a;
    var bres = say(arch, S, input, model);
    ["problem", "sim", "simulation_url"].forEach(function (k) { if (a[k] && !bres[k]) bres[k] = a[k]; });
    return bres;
  }

  function processBack(arch, S, now) {
    var V = arch.variants[S.variantIndex];
    var ev = { event_type: "BAILOUT_RETURN", entering: progress(S, V).done, active: S.away ? S.away.state : "", newly: [], traps: [], guards: [],
      counted_fail: false, after_bailout: true, seconds_away: S.away ? Math.round(((now || 0) - S.away.since) / 1000) : "" };
    var st = S.away ? S.away.state : null; S.awaitingReturn = st; S.away = null; S.pending = null;
    var res = assemble(arch, S, V, ev, (st && moveFor(arch, V, st).return_ask) || "In your own words, what did the notebook show you?", null, false);
    res.needs_say = false; res.log = logRow(arch, S, V, ev, res, { verdict_ms: 0, say_ms: 0 }); return res;
  }

  // ---------- the response, both phases ----------
  function assemble(arch, S, V, ev, reply, card, provisional) {
    var nextId = activeState(S, V), nextItem = nextId ? entry(V, nextId) : null;
    var res = { reply: reply, progress: progress(S, V), card: card || null, pinned: S.pinned, pins: S.pins, choices: choicesFor(arch, S, V),
                next: nextItem ? { id: nextItem.id, kind: nextItem.kind } : null };      // what the page may shape its input to
    if (ev.newly.indexOf("account_given") > -1 || ev.newly.indexOf("account_given(parked)") > -1) res.problem = problemPayload(arch, V, S);
    var simState = V.board.filter(function (x) { return x.opens_sim; })[0];
    var simDue = (simState && isSet(S, simState.id)) || (!simState && activeState(S, V) === "meaning_given");
    if (V.sim && !S.simOpen && simDue) { S.simOpen = true; res.sim = V.sim; }
    var med = (arch.openers[S.openerIndex] && arch.openers[S.openerIndex].media) || {};
    if (med.simulation && !S.mediaSimOpen && ((med.simulation_opens === "account" && isSet(S, "account_given")) || (med.simulation_opens !== "account" && simDue))) {
      S.mediaSimOpen = true; var subst = (V.context && (V.context.true_substance || V.context.substance)) || "";
      var params = Object.assign({ substance: subst }, V.sim_params || {});      // the archetype's own placeholders ({T}, {unit}, ...)
      res.simulation_url = med.simulation.replace(/\{(\w+)\}/g, function (m, k) { return k === "theme" ? m : (params[k] !== undefined ? encodeURIComponent(String(params[k])) : m); });
    }
    if (!provisional && !S.done && activeState(S, V) === null) {
      S.done = true; S.credit = S.rung === "independent" && S.clean && S.board["meaning_given"] === "ticked"; ev.completed = true;   // credit-eligible only at Independent (instructor, 11 Oct)
      var offer = offerFor(arch, V, S); if (offer) { S.offer = offer; res.offer = offer; }   // the offered second worked problem (instructor, 12 Oct)
    }
    res.done = S.done; res.credit = S.credit; res.rung = S.rung;
    return res;
  }

  // A fingerprint of the code that is actually running: the source text of one function per module, hashed. Compared with the
  // value run.py computed from the repository (SHELL_VERSION), it shows a stale paste in Apps Script, which a pasted constant cannot.
  function shellFingerprint() {
    var parts = [verdict, say, parseNumbers, evalArithmetic, match, checkEquation, liveItems, optionsOf, moveFor, applyLadder, checkDraft, buildSystem, fallbackReply, nearMissAsk, symbolShown, showFor, offerFor, logRow, logqAppend];
    var text = parts.map(function (f) { return String(f).replace(/\s+/g, " "); }).join("|"), h = 5381;
    for (var i = 0; i < text.length; i++) h = ((h * 33) ^ text.charCodeAt(i)) >>> 0;
    return h.toString(16);
  }

  return { shellFingerprint: shellFingerprint, verdict: verdict, say: say, processTurn: processTurn, processBack: processBack,
    parseNumbers: parseNumbers, hasAccount: hasAccount, openerCoverage: openerCoverage, newSession: newSession, newRecord: newRecord, nextAssignment: nextAssignment, workedVersion: workedVersion, advance: advance, openerRole: openerRole, showFor: showFor, offerFor: offerFor, match: match, units: UNITS,
    checkEquation: checkEquation, checkTable: checkTable, parseTableText: parseTableText, activeState: activeState, liveItems: liveItems,
    progress: progress, problemPayload: problemPayload, openerMedia: openerMedia, evalArithmetic: evalArithmetic, isAskingForHelp: isAskingForHelp,
    checkDraft: checkDraft, buildSystem: buildSystem, logRow: logRow, chooseVariant: chooseVariant, logqAppend: logqAppend, logqFlush: logqFlush };
})();

if (typeof module !== "undefined") module.exports = CORE;
