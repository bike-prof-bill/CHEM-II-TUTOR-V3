// Per-module tests for the split shell (rebuild spec, step 4). Each module is exercised on its own surface; test_core.js stays
// the integration suite. Loading Core makes every module's functions global, which is how Apps Script sees them too.
const CORE = require("../../gas/Core.gs");
const P = require("../../gas/parse.gs"), M = require("../../gas/match.gs"), SM = require("../../gas/stepmap.gs"), LD = require("../../gas/ladder.gs"),
      G = require("../../gas/guards.gs"), PR = require("../../gas/prompt.gs"), LG = require("../../gas/log.gs");
const ARCH = require("../../gas/Archetype_ch10_cc.gs")["ch10_cc"];
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const V = ARCH.variants.find(v => v.kind === "dH" && v.expected.filter(e => e.state === "T_in_K").length === 2);
const fresh = () => CORE.newSession(ARCH, { variantIndex: ARCH.variants.indexOf(V), openerIndex: V.opener_index, stamp: "m" });

// parse
ok(P.parseNumbers("38,600 J/mol and 1.2e-3 atm").map(n => n.x + n.unit).join() === "38600J/mol,0.0012atm", "parse: numbers and units");
ok(P.hasAccount("the molecules escape faster", ARCH) && !P.hasAccount("K atm torr", ARCH), "parse: prose detector ignores units");
ok(P.evalArithmetic("(273.15 + 47.5) K", ARCH).x === 320.65 && P.evalArithmetic("357 K", ARCH) === null, "parse: arithmetic vs plain number");
ok(P.isAskingForHelp("what do you mean") && !P.isAskingForHelp("it is in kelvin"), "parse: questions by words");
ok(P.parseTableText("I: 1 | 0\nC: -x | +2x\nE: 1 - x | 2x").E.length === 2, "parse: table rows");
ok(Object.keys(P.eqVarsInText("T1 = 300 K", ARCH)).join() === "T1", "parse: T inside T1 is not T");

// match
const key = V.expected.find(e => e.role === "key");
ok(M.match({ x: key.value, unit: null }, V.expected, V.traps, {}).type === "needs_unit", "match: bare key value needs its unit");
ok(M.match({ x: key.value, unit: key.unit }, V.expected, V.traps, {}).type === "expected", "match: key with unit");
ok(M.match({ x: 123456, unit: null }, V.expected, V.traps, {}).type === "stray", "match: stray");
ok(M.checkEquation(V.eq_checks[0].park_text, V, ARCH, fresh())[0].verdict === "VALID_ISOLATED", "match: canonical rearrangement valid");

// stepmap
{ const S = fresh(); const newly = [];
  ok(SM.activeState(S, V) === "account_given", "stepmap: first active item");
  SM.tick(S, V, "value_found", newly); ok(newly.length === 0, "stepmap: a key cannot be ticked before its explicit prerequisite");
  S.board.account_given = "ticked"; S.board.relation_chosen = "ticked"; S.board.rearranged = "ticked";
  SM.tick(S, V, "value_found", newly); ok(newly.indexOf("substituted") > -1 && newly.indexOf("value_found") > -1, "stepmap: later work implies non-explicit steps");
  ok(SM.progress(S, V).labels.length === newly.length + 3, "stepmap: labels only for ticked items");
  ok(SM.stageOf(V, "T_in_K") === "units" && SM.moveFor(ARCH, V, "T_in_K").ask.length > 0, "stepmap: stage and moves by item id"); }

// ladder
{ const S = fresh(); S.board.account_given = "ticked"; S.board.relation_chosen = "ticked"; S.board.rearranged = "ticked";
  const ev = () => ({ event_type: "TURN", active: "T_in_K", newly: [], traps: [], guards: [], counted_fail: true });
  let r = LD.applyLadder(ARCH, S, V, ev(), { now: 1 }); ok(!r.card && !r.reply && r.switchAsk, "ladder: first fail on a stage offers the switch question");
  r = LD.applyLadder(ARCH, S, V, ev(), { now: 1 }); ok(r.card && S.bailed.units && S.tries.units === 0, "ladder: second fail on the stage gives the card");
  S.awaitingReturn = null; r = LD.applyLadder(ARCH, S, V, ev(), { now: 1 }); r = LD.applyLadder(ARCH, S, V, ev(), { now: 1 });
  ok(r.reply && S.board.T_in_K === "parked" && S.board.P_same_units === "parked" && !S.clean, "ladder: two more park the whole stage"); }

// guards: the three cheap checks and the leak guard
{ const S = fresh();
  ok(G.checkDraft("What is the temperature in kelvin?", S, V, false, "").length === 0, "guards: a clean draft passes");
  ok(G.checkDraft("Spot on. What next?", S, V, false, "").indexOf("BANNED_OPENER") > -1, "guards: banned opener");
  ok(G.checkDraft("Why? And how? And when?", S, V, false, "").indexOf("MANY_QUESTIONS") > -1, "guards: more than one question");
  ok(G.checkDraft("Convert the temperature.", S, V, false, "").indexOf("NO_QUESTION") > -1, "guards: no question");
  ok(G.checkDraft("You noted that twice. What now?", S, V, false, "You noted that before. Why?").indexOf("SAME_OPENING") > -1, "guards: same first three words as last reply");
  ok(G.checkDraft("The answer is " + key.value + " " + key.unit + ". Why?", S, V, false, "").indexOf("REPLY_STATED_VALUE") > -1, "guards: unearned value");
  ok(G.checkDraft("Well done, that completes it.", S, V, true, "").length === 0 && G.checkDraft("Done. Anything else?", S, V, true, "").indexOf("QUESTION_AFTER_COMPLETION") > -1, "guards: zero questions after completion");
  ok(G.cutQuestions("Good. That is moderate. And now?") === "Good. That is moderate.", "guards: cut"); }

// prompt: the rules moved into checks are gone; the system prompt carries the verdict and the last-item note
ok(!/Exactly one question/.test(PR.RULES) && !/not by praising/.test(PR.RULES), "prompt: moved rules deleted");
{ const S = fresh(); const sys = PR.buildSystem(ARCH, S, V, { progress: { done: 0, of: 8 }, active: "account_given", register: "submicro", ask: "x", notes: ["NOTE1"], judge: true, lastItem: false });
  ok(/OPENING QUESTION/.test(sys) && /NOTE1/.test(sys) && /YOU JUDGE THIS TURN/.test(sys) && !/PROBLEM on the student/.test(sys), "prompt: hidden problem, verdict, judging");
  ok(/LAST item/.test(PR.buildSystem(ARCH, S, V, { progress: { done: 7, of: 8 }, active: "meaning_given", register: "inference", ask: "x", notes: [], judge: true, lastItem: true })), "prompt: last-item note");
  ok(/type it, with its unit/.test(PR.fallbackReply(ARCH, Object.assign(S, { board: { account_given: "ticked", relation_chosen: "ticked", rearranged: "ticked" } }), V, { newly: [], traps: [] }, { wordsOnly: true })), "prompt: fallback hint"); }

// log: one row, both timings, every column present
{ const S = fresh(); const row = LG.logRow(ARCH, S, V, { event_type: "TURN", active: "account_given", newly: [], traps: [], guards: [], entering: 0 }, { progress: { done: 0 } }, { verdict_ms: 12, say_ms: 340 });
  ok(row.verdict_ms === 12 && row.say_ms === 340 && row.gate === "G2" && row.stage === "opening", "log: timings, gate, stage"); }

console.log(`shell modules: ${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
