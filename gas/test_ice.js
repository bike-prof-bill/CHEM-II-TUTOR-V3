// node gas/test_ice.js  -- scripted students through the second archetype. Same Core.gs; no chemistry shared with ch10_cc.
const CORE = require("./Core.gs"); const ARCH = require("./Archetype_ch13_ice.gs")["ch13_ice"];
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const say = (S, m, model, extra) => CORE.processTurn(ARCH, S, Object.assign({ message: m, now: Date.now() }, extra || {}), model || null);
const byFixed = id => ARCH.variants.findIndex(v => v.fixed_id === id);
const key = V => V.expected.find(t => t.role === "key");
const ACCOUNT = "The forward and reverse reactions run at the same rate, so particles keep reacting both ways while the amounts stop changing.";
const tableText = V => "I: " + V.table.rows.I.join(" | ") + "\nC: " + V.table.rows.C.join(" | ") + "\nE: " + V.table.rows.E.join(" | ");

// 1. find-K problem, straight through: branch opens on the approach pick; table; x; K (unitless key); direction; meaning; reflection
{ const i = byFixed("hi_findK"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "i1" });
  let r = say(S, "hi"); ok(!r.problem, "greeting must not reveal the problem");
  r = say(S, ACCOUNT); ok(r.problem && r.problem.text === V.text && r.problem.title === ARCH.title, "account reveals the problem, with the archetype title");
  const liveBefore = CORE.liveItems(S, V).map(b => b.id);
  ok(liveBefore.indexOf("x_found") < 0 && liveBefore.indexOf("method") < 0 && r.progress.of === liveBefore.length, "branch items are not live, not counted, before the pick: " + r.progress.of);
  r = say(S, "", null, { pick: "eq_k" }); ok(S.board.relation_chosen === "ticked" && r.pins.some(p => p.id === "relation_chosen"), "relation picked and pinned");
  ok(r.choices && r.choices.item === "approach" && r.choices.options.length === 2, "the page is offered the approach buttons");
  r = say(S, "", null, { pick: "approach:solveX" }); ok(S.tries.setup === 1 && S.board.approach !== "ticked", "wrong approach is a wrong try on the setup stage");
  r = say(S, "", null, { pick: "approach:findK" }); ok(S.board.approach === "ticked", "right approach ticks");
  const live = CORE.liveItems(S, V).map(b => b.id);
  ok(live.indexOf("x_found") > -1 && live.indexOf("method") < 0 && live.indexOf("expression_set") < 0, "find-K branch opens x_found only; solve-for-x items stay hidden");
  ok(r.progress.of === live.length, "progress counts live items only: " + r.progress.of);
  r = say(S, "C: -x | -x | +x"); ok(S.board.table !== "ticked" && r.log.counted_fail && /TABLE:/.test(r.log.structured), "a change row without the coefficient is a wrong table, counted");
  r = say(S, tableText(V)); ok(S.board.table === "ticked" && r.pins.some(p => p.id === "table"), "right table ticks and is pinned; " + r.log.structured);
  r = say(S, "so x = 0.78 M"); ok(S.board.x_found === "ticked", "x found");
  const k = key(V); r = say(S, "Kc = " + k.value.toFixed(1)); ok(S.board.value_found === "ticked" && !k.require_unit, "a unitless K is accepted bare (declared, no unit required)");
  r = say(S, "About a fifth of the hydrogen is left, so the reaction went most of the way before the two rates matched.");
  ok(S.board.meaning_given === "ticked" && !r.done, "meaning accepted; the reflection still stands between the student and done");
  r = say(S, "ok"); ok(S.board.reflection !== "ticked" && !r.log.counted_fail, "a one-word reflection is asked again, never counted");
  r = say(S, "The change row was hardest because I kept forgetting the coefficient on HI.");
  ok(r.done && r.credit && S.board.reflection === "ticked", "reflection closes the problem; clean run earns credit"); }

// 2. solve-for-x, perfect square: method branch; "49 = (2x)^2/(0.2-x)^2" read as K = ...; coefficient trap in the algebra and in the number
{ const i = byFixed("hi_ps"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 4, stamp: "i2" });
  say(S, ACCOUNT); say(S, "", null, { pick: "eq_k" }); say(S, "", null, { pick: "approach:solveX" });
  let r = say(S, tableText(V)); ok(S.board.table === "ticked", "table");
  r = say(S, "", null, { pick: "method:smallx" }); ok(S.tries.solve === 1, "small-x is not a method here: wrong try on the solve stage");
  r = say(S, "", null, { pick: "method:sqrt" }); ok(S.board.method === "ticked", "square root is a right method for a perfect square");
  r = say(S, "K = 2x^2/(0.2-x)^2"); ok(r.log.trap_ids === "EQ_COEFFICIENT_NOT_SQUARED" && S.board.expression_set !== "ticked", "2x^2 for (2x)^2 is named in the algebra: " + r.log.trap_ids);
  r = say(S, "49 = (2x)^2/(0.2-x)^2"); ok(S.board.expression_set === "ticked", "the literal K on the left is read as K: expression accepted; " + r.log.structured);
  const xt = V.traps.find(t => t.id === "COEFFICIENT_NOT_SQUARED" && t.state === "x_found");
  r = say(S, "x = " + xt.value + " M"); ok(r.log.trap_ids === "COEFFICIENT_NOT_SQUARED", "the x from the unsquared coefficient is named");
  const x = V.expected.find(e => e.state === "x_found"); r = say(S, "x = " + x.value.toFixed(4) + " M"); ok(S.board.x_found === "ticked", "x");
  const k = key(V); r = say(S, "[HI] = " + k.value.toFixed(3)); ok(/units/i.test(r.reply) && S.board.value_found !== "ticked", "a bare concentration asks for its unit");
  r = say(S, "M"); ok(S.board.value_found === "ticked", "unit supplied: the small number with units is accepted (integer-bug regression, second archetype)"); }

// 3. quadratic: the unbracketed denominator in the algebra and the number it produces; conservation bound
{ const i = byFixed("pcl5_quad"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 1, stamp: "i3" });
  say(S, ACCOUNT); say(S, "", null, { pick: "eq_k" }); say(S, "", null, { pick: "approach:solveX" }); say(S, tableText(V));
  let r = say(S, "", null, { pick: "method:sqrt" }); ok(S.board.method !== "ticked" && S.tries.solve === 1, "square root does not fit a non-square problem");
  say(S, "", null, { pick: "method:quadratic" }); ok(S.board.method === "ticked", "quadratic fits");
  r = say(S, "K = x^2/0.80-x"); ok(r.log.trap_ids === "EQ_ORDER_OF_OPERATIONS", "unbracketed denominator named in the algebra: " + r.log.trap_ids);
  ok(S.bailed.solve, "two wrong tries on the solve stage (wrong method, then the algebra) gave the notebook card: ladder is per stage");
  CORE.processBack(ARCH, S, Date.now() + 5000); say(S, "The notebook showed that the denominator has to be bracketed so the whole 0.80 minus x is divided.");
  r = say(S, "0.042 = x^2/(0.80-x)"); ok(S.board.expression_set === "ticked", "expression with K's value on the left accepted after return");
  const oo = V.traps.find(t => t.id === "ORDER_OF_OPERATIONS"); r = say(S, oo.value + " M"); ok(r.log.trap_ids === "ORDER_OF_OPERATIONS", "the number from the unbracketed form is named, before the conservation bound");
  r = say(S, "1.5 M"); ok(r.log.trap_ids === "EXCEEDS_INITIAL", "a concentration above the starting amount is the conservation trap");
  ok(r.log.event_type === "PARK" && S.board.value_found === "parked", "two more wrong tries after the return park the stage"); }

// 4. every fixed problem can be completed by a student who gives the canonical table, expression, numbers and sentences
{ let bad = 0; ARCH.variants.forEach((V, i) => { const S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "c" + i });
    say(S, ACCOUNT); say(S, "", null, { pick: "eq_k" }); say(S, "", null, { pick: V.kind === "findK" ? "approach:findK" : "approach:solveX" });
    say(S, tableText(V));
    if (V.kind !== "findK") { say(S, "", null, { pick: "method:quadratic" }); V.eq_checks.forEach(k => { say(S, k.park_text); if (S.board[k.state] !== "ticked") { bad++; console.log("   canonical expression rejected:", k.park_text); } }); }
    V.expected.filter(e => e.role === "intermediate" && e.state === "x_found").forEach(e => say(S, e.value + " " + e.unit));
    V.expected.filter(e => e.role === "key").forEach(e => say(S, e.value + (e.unit ? " " + e.unit : "")));
    say(S, "Most of the reactant is still there, so the reaction did not go far before the rates matched.");
    const r = say(S, "Setting up the change row was the hardest step because the coefficients decide the multiples of x.");
    if (!(r.done && r.credit)) { bad++; console.log("   not completed:", V.fixed_id, JSON.stringify(S.board), CORE.activeState(S, V)); } });
  ok(bad === 0, bad + " fixed problems could not be completed"); }

// 5. the table reader
{ const i = byFixed("n2o4_findK"), V = ARCH.variants[i];
  ok(CORE.checkTable(CORE.parseTableText("Initial 0.500, 0\nChange −x, +2x\nEquilibrium 0.500 − x, 2x"), V, ARCH).ok, "words, commas, unicode minus");
  ok(CORE.checkTable(CORE.parseTableText("I: 0.5 | 0\nC: -x | 2x\nE: 0.5-x | 2 x"), V, ARCH).ok, "pipes, no plus sign, spaced 2 x");
  const t = CORE.checkTable(CORE.parseTableText("C: -x | +x\nE: 0.5 - x | x"), V, ARCH); ok(!t.ok && t.wrong.join("") === "CE", "coefficient dropped in both rows is wrong, rows named");
  ok(CORE.parseTableText("the answer is 42") === null, "prose is not a table"); }

console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
