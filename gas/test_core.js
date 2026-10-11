// node gas/test_core.js  -- scripted students through the real logic. No network, no Google.
const CORE = require("./Core.gs"); const ARCH = require("./Archetype_ch10_cc_test.gs")["ch10_cc"];
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const find = kind => ARCH.variants.findIndex(v => v.kind === kind && v.board.some(b => b.state === "T_in_K"));
const say = (S, m, model, extra) => CORE.processTurn(ARCH, S, Object.assign({ message: m, now: Date.now() }, extra || {}), model || null);
const key = V => V.expected.find(t => t.role === "key");
const fmtU = u => u === "degC" ? "°C" : u;
const predict = (S, V, model) => { const d = V.board.find(b => b.id === "direction_predicted"); if (d) say(S, "", model, { pick: d.right[0] }); };
const REFLECT = "The rearrangement was hardest; I would tell a friend to undo the natural log first.";

// 1. strong student, offline mode (no model): straight through, any order
{ const i = find("T2"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "t1" });
  let r = say(S, "hi"); ok(!r.problem, "greeting must not reveal problem");
  r = say(S, "A larger fraction of the molecules have enough kinetic energy to overcome the attractions and escape.");
  ok(r.problem && r.problem.text === V.text, "account reveals problem"); ok(!JSON.stringify(r).includes("true_substance"), "no hidden fields leak");
  predict(S, V);                                                            // temperature problems carry the prediction too (vent scenario, 10 Oct)
  const k = key(V); r = say(S, "I get " + k.value.toFixed(2));            // bare number, no unit
  ok(!r.done && /units/i.test(r.reply), "bare key asks for units"); r = say(S, fmtU(k.unit));
  ok(S.board.value_found !== "ticked" && S.board.T_in_K === "ticked", "right number is recorded but does NOT count before the rearrangement");
  r = say(S, "", null, { pick: "eq_a" }); ok(r.pinned.relation && r.pinned.relation.indexOf("ln(P2/P1)") === 0, "picked relation is pinned");
  r = say(S, "1/T2 = 1/T1 - (R/ΔHvap) ln(P2/P1)"); ok(S.board.rearranged !== "ticked" && !S.tries.setup && /EQ:HOLDS_NOT_ISOLATED/.test(r.log.structured), "true but not isolated: progress, not a wrong try");
  r = say(S, "so T2 = 1/(1/T1 - R·ln(P2/P1)/ΔHvap)"); ok(S.board.rearranged === "ticked" && r.pinned.rearranged[0].indexOf("T2 =") === 0, "isolated form accepted and pinned");
  ok(S.board.value_found === "ticked", "the number typed earlier now counts, without retyping");
  ok(r.sim && r.sim.measured_degC_torr.length === 6, "sim released on value");
  r = say(S, "The measurement only gives pressure; the energy distribution of molecules is inferred from how steeply it rises.");
  ok(!r.done && S.board.meaning_given === "ticked", "meaning accepted; the reflection still stands between the student and done");
  r = say(S, REFLECT); ok(r.done && r.credit, "clean finish earns credit"); }

// 2. weak student: trap, then stray -> notebook card without a model call; return; two more -> park
{ const i = find("P2") > -1 ? find("P2") : find("T2"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 1, stamp: "t2" });
  let calls = 0; const model = () => { calls++; return { accept: 1, turn_kind: "answer", socratic_response: "What happens next?" }; };
  say(S, "The water molecules at the surface gain energy and escape into the vapor bubbles.", model); predict(S, V, model);
  say(S, "", model, { pick: "eq_c" }); ok(S.tries.setup === 1, "wrong pick counts once (ladder is per stage: setup)");
  say(S, "", model, { pick: "eq_a" }); ok(S.board.relation_chosen === "ticked", "right pick ticks");
  say(S, V.eq_checks[0].park_text, model); ok(S.board.rearranged === "ticked", "canonical rearrangement accepted");
  const trap = V.traps[0]; let before = calls;
  let r = say(S, "answer is " + trap.value + " " + fmtU(trap.unit), model); ok(r.log.trap_ids === trap.id, "trap named: " + trap.id);
  before = calls; r = say(S, "ok then 123456 " + fmtU(trap.unit), model);
  ok(r.card && r.card.url.includes("notebook.google.com") && r.card.prompt.length > 40, "second wrong try gives notebook card");
  ok(calls === before, "no model call on the bailout turn"); ok(r.log.event_type === "BAILOUT_ISSUED", "bailout logged");
  r = CORE.processBack(ARCH, S, Date.now() + 90000); ok(r.log.event_type === "BAILOUT_RETURN" && r.log.seconds_away >= 89, "return logged with time away");
  r = say(S, "ok", model); ok(S.awaitingReturn, "thin return answer is not enough");
  r = say(S, "It showed that temperatures have to be absolute because the relation uses one over T.", model); ok(!S.awaitingReturn && r.log.after_bailout, "return account accepted, flagged after_bailout");
  say(S, "77777 " + fmtU(trap.unit), model); r = say(S, "88888 " + fmtU(trap.unit), model);
  ok(r.log.event_type === "PARK" && S.clean === false, "two more wrong tries parks, attempt no longer clean"); }

// 3. guards: a model that leaks the key is rewritten, then replaced by the authored question
{ const i = find("T2"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "t3" });
  const leaky = () => ({ accept: 1, turn_kind: "answer", socratic_response: "Good. So T2 is " + key(V).value + ", what next?" });
  const r = say(S, "More molecules have enough energy to escape the liquid surface as it warms.", leaky);
  ok(!r.reply.includes(String(key(V).value)) && r.log.fallback_used && r.log.guards.includes("REPLY_STATED_VALUE"), "leaked value never reaches student"); }

// 4. second reader overrules an accepting tutor
{ const i = find("T2"), S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "t4" });
  const m = (sys) => /checking one student message/.test(sys) ? { found: 1, quote: "the bonds inside each water molecule break", why: "evaporation does not break covalent bonds" }
                                                  : { accept: 1, turn_kind: "answer", socratic_response: "What breaks?" };
  const r = say(S, "As it heats up the bonds inside each water molecule break and the atoms fly off as vapor.", m);
  ok(S.board.account_given !== "ticked" && r.log.second_reader === "FALSE_CLAIM" && !r.problem, "second reader blocks a false account"); }

// 5. a name is not an account; a question is not a wrong try
{ const i = find("T2"), S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "t5" });
  say(S, "Clausius-Clapeyron"); ok(S.board.account_given !== "ticked", "bare law name does not clear");
  say(S, "It is at dynamic equilibrium obviously."); ok(S.board.account_given !== "ticked", "label with no particles or scenario does not clear");
  const S2 = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "t5b" });
  say(S2, "Molecules with enough kinetic energy escape the surface of the liquid."); say(S2, "which R do I use?");
  ok(!S2.tries.setup, "a question costs nothing"); }

// 6. slope kind, and number reading
{ const i = ARCH.variants.findIndex(v => v.kind === "slope"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 2, stamp: "t6" });
  let r = say(S, "Alcohol molecules attract each other weakly so a bigger fraction can escape."); ok(r.problem.plots.measured_degC_torr.length === 6, "slope problem arrives with its plots");
  const [dh, bp] = V.expected.filter(t => t.role === "key"); say(S, "", null, { pick: "eq_b" });
  r = say(S, dh.value.toFixed(1) + " kJ/mol"); ok(S.board.dH_found !== "ticked", "slope: right ΔHvap does not count before its rearrangement");
  r = say(S, "ΔHvap = slope·R"); ok(r.log.trap_ids === "EQ_SIGN_FLIPPED", "slope: kept sign in the algebra is named");
  r = say(S, "ΔHvap = -m R / 1000"); ok(S.board.rearranged_dH === "ticked" && S.board.dH_found === "ticked", "slope: kJ form accepted; earlier number now counts");
  const triesBefore = S.tries.setup || 0; r = say(S, "ln P = m/T + b"); ok(S.board.rearranged_T !== "ticked" && (S.tries.setup || 0) === triesBefore, "slope: the line itself is not yet T alone, and not a wrong try");
  r = say(S, "Tb = m / (ln(760) - b)\nTb = " + bp.value.toFixed(1) + " " + fmtU(bp.unit)); ok(S.board.rearranged_T === "ticked" && S.board.bp_found === "ticked", "slope: rearrangement and value in one message");
  ok(r.pinned.rearranged.length === 2, "slope: both rearrangements pinned"); }
{ const n = CORE.parseNumbers("T2 = 351.5 K, P1=394 torr, 3.86×10⁴ J/mol, 1.2e-3 atm, H2O, 38,600 J");
  ok(JSON.stringify(n.map(x => x.x)) === "[351.5,394,38600,0.0012,38600]" && n[0].unit === "K" && n[2].unit === "J/mol", "numbers: " + JSON.stringify(n)); }

// 6b. the equation reader
{ const i = find("T2"), V = ARCH.variants[i], E = t => (CORE.checkEquation(t, V, ARCH)[0] || {}).verdict, T = t => (CORE.checkEquation(t, V, ARCH)[0] || {}).trap;
  ok(E("T2 = 1/(1/T1 - (R/ΔH)*ln(P2/P1))") === "VALID_ISOLATED", "plain form");
  ok(E("T₂ = [ 1/T₁ − R ln(P₂/P₁)/ΔHvap ]⁻¹") === "VALID_ISOLATED", "subscripts, unicode minus, implied multiply, ⁻¹");
  ok(E("T2 = ΔHvap T1 / (ΔHvap - R T1 ln(P2/P1))") === "VALID_ISOLATED", "a different but equal arrangement passes without being listed");
  ok(E("T2 = 1/(1/T1 + (R/ΔH)*ln(P2/P1))") === "TRAP" && T("T2 = 1/(1/T1 + (R/ΔH)*ln(P2/P1))") === "EQ_SIGN_FLIPPED", "sign error is named");
  ok(T("T2 = 1/(1/T1 - (R/ΔH)*log(P2/P1))") === "EQ_LOG_BASE", "log for ln is named");
  ok(E("T2 = 1/1/T1 - R/ΔH*ln(P2/P1)") === "WRONG", "unbracketed denominator is wrong, not a typo");
  ok(E("ln(P2/P1) = -(ΔH/R)(1/T2 - 1/T1)") === "HOLDS_NOT_ISOLATED", "the unrearranged relation is not enough");
  ok(E("T2 = 1/(1/T1 - (R/ΔH) ln P2/P1)") === "WRONG", "bare ln takes only the next factor: ln P2/P1 is (ln P2)/P1");
  ok(E("T2 = T2") !== "VALID_ISOLATED" && E("T1 = 300.8 K") === undefined, "identities and plain assignments are ignored"); }

// 6c. the 1 in 1/T must never be read as an answer or a trap (found in the browser run, 20 Sept)
{ let bad = 0; ARCH.variants.forEach((V, i) => { if (V.kind === "slope") return; const S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "e" + i });
    say(S, "A greater fraction of molecules has the kinetic energy to escape the liquid surface."); say(S, "", null, { pick: "eq_a" });
    const r = say(S, V.eq_checks[0].park_text); if (r.log.trap_ids || r.log.counted_fail) bad++; }); ok(bad === 0, bad + " rearrangements misread as traps"); }

// 6d. openers and variants align (instructor, 20 Sept)
{ let bad = 0; ARCH.variants.forEach((V, i) => { const S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 99, stamp: "o" + i }), op = ARCH.openers[S.openerIndex];
    const liquid = V.context.true_substance || V.context.substance; if (!op || op.liquids.indexOf(liquid) < 0) bad++; }); ok(bad === 0, bad + " problems whose liquid does not fit their scenario"); }

// 6e. the step map is a schema: every item carries id, stage, kind, register, face, requires; labels appear only once ticked
{ let bad = 0; ARCH.variants.forEach(V => V.board.forEach(b => { if (!(b.id && b.stage && b.kind && b.register && b.face && Array.isArray(b.requires) && "branch" in b && "pin" in b && "label_when_done" in b)) bad++; }));
  ok(bad === 0, bad + " items missing schema fields");
  const i = find("T2"), S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "lbl" });
  let r = say(S, "hi"); ok(r.progress.labels.length === 0 && r.progress.of === ARCH.variants[i].board.length, "no labels before anything is ticked");
  r = say(S, "More molecules have enough energy to escape the liquid surface as it warms.");
  ok(r.progress.labels.length === 1 && r.progress.labels[0] === ARCH.moves.account_given.label_when_done, "the ticked item's label appears: " + JSON.stringify(r.progress.labels)); }

// 6f. "T1 = 341.65 K" is a statement of a value, not an equation: the symbol T must not be read inside T1 (found in the first demo, 9 Oct)
{ const i = ARCH.variants.findIndex(v => v.kind === "dH" && v.expected.filter(e => e.state === "T_in_K").length === 2), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "t1" });
  say(S, "More molecules have enough energy to escape the liquid surface as it warms."); say(S, "", null, { pick: "eq_a" }); say(S, V.eq_checks[0].park_text);
  const ts = V.expected.filter(e => e.state === "T_in_K");
  ts.forEach((e, k) => say(S, `T${k + 1} = ${e.value} K`));
  ok(S.board.T_in_K === "ticked", "typed 'T1 = value K' and 'T2 = value K' establish the kelvin temperatures");
  const ratio = V.expected.find(e => e.state === "substituted" && /^P[12]_P[12]$/.test(e.id)) || V.expected.find(e => e.state === "substituted"); say(S, `${ratio.label} = ${ratio.value}${ratio.unit ? " " + ratio.unit : ""}`);
  ok(S.board.substituted === "ticked", "'P2/P1 = value' states a value for an expression: the right side is read as a number");
  const before = Object.keys(S.matched).length; say(S, "ln P2 - ln P1 = ΔHvap/R (1/T1 - 1/T2)");
  ok(Object.keys(S.matched).length === before, "pure algebra on both sides is still not read for numbers (the 1 in 1/T stays a 1)"); }

// 6g. found by the instructor's first live run, 9 Oct: two assignments on one line; words typed at a number item in plain mode
{ const i = ARCH.variants.findIndex(v => v.kind === "dH" && v.expected.filter(e => e.state === "T_in_K").length === 2), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "live1" });
  say(S, "More molecules have enough energy to escape the liquid surface as it warms."); say(S, "", null, { pick: "eq_a" }); say(S, V.eq_checks[0].park_text);
  let r1 = say(S, "Temperature must be in Kelvin"); let r2 = say(S, "must be in K");
  ok(!r1.log.counted_fail && !r2.log.counted_fail, "words at a number item cost nothing");
  ok(/type it, with its unit/i.test(r1.reply) && /type it, with its unit/i.test(r2.reply), "words at a number item get the plain hint at once (instructor's second live run): " + r1.reply);
  const ts = V.expected.filter(e => e.state === "T_in_K");
  r1 = say(S, `T1 = ${ts[0].value} K,  T2 =${ts[1].value}K`);
  ok(S.board.T_in_K === "ticked", "two assignments on one line, comma-separated, both read");
  ok(CORE.parseNumbers("ok then 38,600 J and 1,250 torr").map(n => n.x).join() === "38600,1250", "thousands commas still intact");
  const S2 = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "live2" });
  say(S2, "More molecules have enough energy to escape the liquid surface as it warms."); say(S2, "", null, { pick: "eq_a" }); say(S2, V.eq_checks[0].park_text);
  say(S2, `T1 = ${ts[0].value} K T2 = ${ts[1].value} K`); ok(S2.board.T_in_K === "ticked", "two assignments separated by a space only, both read");
  const S3 = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "live3" });
  say(S3, "More molecules have enough energy to escape the liquid surface as it warms."); say(S3, "", null, { pick: "eq_a" }); say(S3, V.eq_checks[0].park_text);
  say(S3, `T1 = ${ts[0].value} K and T2 = ${ts[1].value} K`); ok(S3.board.T_in_K === "ticked", "two assignments joined by 'and', both read");
  // 6h. arithmetic shown in a value statement (instructor, 9 Oct): the worked result is read, the parts are not strays
  const S4 = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "live4" });
  say(S4, "More molecules have enough energy to escape the liquid surface as it warms."); say(S4, "", null, { pick: "eq_a" }); say(S4, V.eq_checks[0].park_text);
  const g = V.givens, tC = n => g[n].unit === "degC" ? g[n].value : g[n].value - 273.15;
  let r4 = say(S4, `T1 = (273.15 + ${tC("T1")}) K and T2 = (273.15 + ${tC("T2")}) K`);
  ok(S4.board.T_in_K === "ticked" && !r4.log.counted_fail, "T = (273.15 + t) K is worked and accepted: " + r4.log.newly);
  r4 = say(S4, "so 0.5 * 999.9 torr"); ok(r4.log.counted_fail, "a worked value that matches nothing is one stray, not two");
  ok(CORE.evalArithmetic("R ln(2)", ARCH) === null && CORE.evalArithmetic("357.15 K", ARCH) === null, "symbols are algebra, a plain number is a number; neither is arithmetic");
  const b2 = Object.keys(S2.matched).length; say(S2, "ln P2 - ln P1 = ΔHvap/R (1/T1 - 1/T2)"); ok(Object.keys(S2.matched).length === b2, "algebra containing 'P1 =' is still not read for numbers"); }

// 6i. a completed problem never ends on a question (instructor's Google-mode run, 9 Oct): the model's draft is rewritten or cut
{ const i = find("dH"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "q1" });
  const asking = (sys, hist, msg) => ({ socratic_response: "Good. The forces are moderate. And how would you summarize all three accounts together?", accept: 1, turn_kind: "answer" });
  say(S, "More molecules have enough energy to escape the liquid surface as it warms.", asking); say(S, "", asking, { pick: "eq_a" }); say(S, V.eq_checks[0].park_text, asking);
  V.expected.filter(e => e.role === "intermediate" || e.role === "key").forEach(e => say(S, e.value + " " + e.unit, asking));
  say(S, "The value says the attractions are moderate; the measurements support the picture only roughly.", asking);
  const r = say(S, REFLECT, asking);     // the reflection is the last item now
  ok(r.done && !/\?/.test(r.reply) && /QUESTION_AFTER_COMPLETION/.test(r.log.guards), "completion: question cut, guard logged: " + JSON.stringify(r.reply));
  const r2 = say(S, "thanks", asking); ok(r2.done && !/\?/.test(r2.reply), "after completion: still no question"); }

// 6j. a student's question has no question mark (instructor, 9 Oct): read the words
{ const Q = ["what do you mean by infer", "I do not know", "how do i convert this", "which one is the relation", "huh", "not sure what you want here", "explain that", "im lost"];
  const NOTQ = ["the pressures must share a unit", "weaker forces so they escape", "it is in kelvin", "They are moving"];
  ok(Q.every(q => CORE.isAskingForHelp(q)), "help requests without a question mark are read as questions");
  ok(NOTQ.every(q => !CORE.isAskingForHelp(q)), "answers are not mistaken for questions");
  const i = find("dH"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "q2" });
  say(S, "More molecules have enough energy to escape the liquid surface as it warms."); say(S, "", null, { pick: "eq_a" }); say(S, V.eq_checks[0].park_text);
  const r = say(S, "what do you mean by infer"); ok(r.log.turn_kind === "question" && !r.log.counted_fail, "a plea for help costs nothing: " + r.log.turn_kind); }

// 6k. label words (SCENARIO_CLAUDE, approved 9 Oct): naming the phenomenon without a mechanism is asked again and never counted
{ const LIVE = require("./Archetype_ch10_cc.gs")["ch10_cc"];       // the student-facing bundle: label words live on its openers
  const oi = LIVE.openers.findIndex(o => /Rubbing/.test(o.title)), i = LIVE.variants.findIndex(v => v.opener_index === oi), S = CORE.newSession(LIVE, { variantIndex: i, openerIndex: oi, stamp: "lbl" });
  const sayL = (m, x) => CORE.processTurn(LIVE, S, Object.assign({ message: m, now: 1 }, x || {}), null);
  ok(LIVE.openers[oi].label_words.indexOf("volatile") > -1 && LIVE.openers[oi].keywords.indexOf("escape") > -1, "the opener carries label words and the approved keywords");
  let r = sayL("Alcohol is more volatile than water so it evaporates and dries fast.");
  ok(S.board.account_given !== "ticked" && !r.log.counted_fail && /OPENER_LABEL_ONLY/.test(r.log.guards), "a label-only account is not ticked, not counted, flagged: " + r.log.guards);
  r = sayL("Alcohol molecules attract each other weakly, so a larger fraction has the energy to escape the surface.");
  ok(S.board.account_given === "ticked", "a mechanism account is accepted"); }

// 6l. a choice item next: the model may acknowledge but the authored question is asked (instructor's run, 10 Oct)
{ const i = ARCH.variants.findIndex(v => v.kind === "P2"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "ch1" });
  let calls = 0; const wander = (sys, hist, msg) => { calls++; return { socratic_response: "You noted that pressure drops. In terms of energy, why does a cooler liquid need a lower pressure to boil?", accept: 1, turn_kind: "answer" }; };
  let r = say(S, "More molecules have enough energy to escape the liquid surface as it warms.", wander);
  ok(S.board.account_given === "ticked" && /Pick one|higher or lower/.test(r.reply) && !/why does a cooler/.test(r.reply), "account accepted; the model's own question gives way to the authored prediction question: " + r.reply);
  const before = calls; const d = V.board.find(b => b.id === "direction_predicted"); r = say(S, "", wander, { pick: d.right[0] });
  ok(calls === before && /Equations list/.test(r.reply), "after a right prediction nothing is judged and the next item is a pick: no model call, the authored question verbatim: " + r.reply); }

// 6m. instructor, 11 Oct, after the model refused four true accounts: the gates have passed and the second reader finds nothing false,
// so the account is accepted on the first turn whatever the model's accept says; the model's hold-out question never reaches the student.
{ const i = find("T2"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "ho1" });
  const holdout = (sys) => /checking one student message/.test(sys) ? { found: 0 } : { accept: 0, turn_kind: "answer", socratic_response: "What specific interactions hold the water molecules together?" };
  const r = say(S, "Weaker intermolecular attractions in the alcohol mean its molecules need less energy to escape into the vapor.", holdout);
  ok(S.board.account_given === "ticked" && r.problem, "true account accepted although the model held out");
  ok(r.log.model_accept === 0 && r.log.second_reader === "clean" && r.log.guards.includes("MODEL_REFUSED_TRUE_ACCOUNT"), "both verdicts logged, the refusal flagged");
  ok(!/specific interactions/.test(r.reply), "the hold-out question is not shown: " + r.reply); }

// 6n. a checkable item next (the rearrangement): the model may acknowledge but the authored question is asked verbatim; with nothing to
// judge the model is not called at all (instructor's run, 11 Oct: the model asked for the kelvin conversion while the equation was open)
{ const i = find("T2"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "ck1" });
  let calls = 0; const ahead = () => { calls++; return { accept: 1, turn_kind: "answer", socratic_response: "Good. What unit must the temperatures be in, and what does 82.5 °C become?" }; };
  say(S, "More molecules have enough energy to escape the liquid surface as it warms.", ahead); predict(S, V, ahead);
  let r = say(S, "", ahead, { pick: "eq_a" }); const asked = r.reply;
  ok(/rearrange/.test(asked) && !/82\.5/.test(asked), "after the pick the authored rearrangement question is asked, not the model's: " + asked);
  const before = calls; r = say(S, "I think the temperatures matter here", ahead);
  ok(calls === before && /rearrange/.test(r.reply), "words at an equation item: no model call, the authored question (with the hint) again");
  r = say(S, "what do you mean by rearrange", ahead);
  ok(calls === before + 1 && /rearrange/.test(r.reply) && !/82\.5/.test(r.reply), "a question for help still reaches the model, whose own question gives way to the authored one"); }

// 6o. instructor, 11 Oct: "either side is fine with algebra" — the unknown alone on the right is a valid rearrangement, pinned as typed
{ const i = find("T2"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "rs1" });
  say(S, "More molecules have enough energy to escape the liquid surface as it warms."); predict(S, V); say(S, "", null, { pick: "eq_a" });
  const r = say(S, "1/(1/T1 - R·ln(P2/P1)/ΔHvap) = T2");
  ok(S.board.rearranged === "ticked" && /EQ:VALID_ISOLATED/.test(r.log.structured), "unknown alone on the right accepted");
  ok(r.pinned.rearranged[0].indexOf("= T2") > 0, "pinned as typed: " + r.pinned.rearranged[0]);
  const S2 = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "rs2" });
  say(S2, "More molecules have enough energy to escape the liquid surface as it warms."); predict(S2, V); say(S2, "", null, { pick: "eq_a" });
  const r2 = say(S2, "1/T1 - R·ln(P2/P1)/ΔHvap = 1/T2");
  ok(S2.board.rearranged !== "ticked" && /EQ:HOLDS_NOT_ISOLATED/.test(r2.log.structured), "true but 1/T2, not T2, on the right: still progress, not isolated"); }

// 6p. instructor, 11 Oct: a calculated number outside the window but near the expected value, matching no trap, is a near miss:
// counted, and the authored question asks which values they used; the same wrong number typed again costs nothing.
{ const i = find("T2"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "nm1" });
  say(S, "More molecules have enough energy to escape the liquid surface as it warms."); predict(S, V); say(S, "", null, { pick: "eq_a" });
  say(S, V.eq_checks[0].park_text); const k = key(V), low = (k.value * 0.975).toPrecision(5) + " " + fmtU(k.unit);
  let r = say(S, low); const stg = r.log.stage;
  ok(r.log.near_miss === k.id && r.log.counted_fail && !r.card && S.tries[stg] === 1, "2.5 % low: near miss named, one wrong try, no card");
  ok(/Which values did you use/.test(r.reply) && !/close|window/.test(r.reply), "the authored near-miss question, nothing about how close: " + r.reply);
  r = say(S, low);
  ok(r.log.repeat && !r.log.counted_fail && S.tries[stg] === 1 && !r.card, "the same number again: not counted, no card");
  ok(/^That is the same number as before\. Which values did you use/.test(r.reply), "repeat sentence then the question: " + r.reply);
  r = say(S, (k.value * 1.03).toPrecision(5) + " " + fmtU(k.unit));
  ok(r.card && r.log.counted_fail, "a different near miss is the second wrong try: the notebook card");
  const t = V.traps.find(x => x.value !== undefined && !x.openers), S2 = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "nm2" });
  say(S2, "More molecules have enough energy to escape the liquid surface as it warms."); predict(S2, V); say(S2, "", null, { pick: "eq_a" }); say(S2, V.eq_checks[0].park_text);
  r = say(S2, t.value + " " + fmtU(t.unit)); ok(r.log.trap_ids === t.id && !r.log.near_miss, "a trap value is the trap, never a near miss");
  const S3 = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "nm3" });
  say(S3, "More molecules have enough energy to escape the liquid surface as it warms."); predict(S3, V); say(S3, "", null, { pick: "eq_a" }); say(S3, V.eq_checks[0].park_text);
  r = say(S3, (k.value * 0.5).toPrecision(5) + " " + fmtU(k.unit)); ok(!r.log.near_miss && r.log.counted_fail, "half the answer is a stray, not a near miss"); }

// 7. every variant of every kind can be completed by a student who types only the key(s)
{ let bad = 0; ARCH.variants.forEach((V, i) => { const S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: V.opener_index, stamp: "v" + i });
    say(S, "A greater fraction of molecules has the kinetic energy to escape the liquid surface.");
    predict(S, V); say(S, "", null, { pick: V.kind === "slope" ? "eq_b" : "eq_a" });
    V.eq_checks.forEach(k => { say(S, k.park_text); if (S.board[k.state] !== "ticked") { bad++; console.log("   canonical form rejected:", k.park_text); } });
    V.expected.filter(t => t.role === "key").forEach(t => say(S, t.value + " " + fmtU(t.unit)));
    V.expected.filter(t => t.derive).forEach(t => { const k = V.expected.find(e => e.id === t.derive.from); say(S, (t.derive.base - k.value).toPrecision(5) + " " + fmtU(t.unit)); });   // a derived item (the bird's pressure difference)
    say(S, "Only pressure and temperature were measured; what the molecules do is inferred from the fit.");
    const r = say(S, REFLECT);
    if (!(r.done && r.credit)) { bad++; if (bad < 4) console.log("   not completed:", V.variant_id, V.kind, CORE.activeState(S, V)); } }); ok(bad === 0, bad + " variants could not be completed"); }
console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
