// Q versus K (ch13_q_vs_k): the skeleton walked in the shell on the test fixture (the shipped bundle is empty until a scenario is approved).
// Run with: node gas/test_q_vs_k.js
const CORE = require("./Core.gs"), ARCH = require("./Archetype_ch13_q_vs_k_test.gs")["ch13_q_vs_k"];
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const byFixed = (id) => ARCH.variants.findIndex(v => v.fixed_id === id);
const say = (S, m, extra) => CORE.processTurn(ARCH, S, Object.assign({ message: m, now: Date.now() }, extra || {}), null);
const ACC = "Hydrogen and iodine molecules collide and form hydrogen iodide while hydrogen iodide molecules collide and break apart; the forward rate is faster until the ratio reaches K.";
const fs = require("fs");

// 1. the bundles
ok(ARCH.variants.length === 4, "four placeholder problems in the test fixture");
ok(!fs.existsSync(__dirname + "/Archetype_ch13_q_vs_k.gs"), "no shipped bundle while no scenario is approved");
ok(ARCH.variants.every(v => v.status && /^DRAFT/.test(v.status)), "every placeholder carries DRAFT");
ok(ARCH.variants.every(v => v.board.map(b => b.id).join(">") === "account_given>relation_chosen>Q_found>shift_predicted>meaning_given>reflection"), "the six steps");

// 2. Q1 (H2 + I2, Q < K) at Independent: the expression, Q as a number, the named errors, the direction, done
{ const i = byFixed("Q1"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: V.opener_index, stamp: "q1", rung: "independent" });
  let r = say(S, ACC); ok(S.board.account_given === "ticked" && r.problem, "account accepted, problem revealed");
  r = say(S, "36"); ok(S.board.Q_found !== "ticked", "a number before the expression is picked does not tick Q");
  r = say(S, "", { pick: "eq_k" }); ok(S.board.relation_chosen !== "ticked" && r.log.counted_fail, "K's expression is the look-alike, not the pick for Q");
  r = say(S, "", { pick: "eq_q" }); ok(S.board.relation_chosen === "ticked", "the Q expression picked");
  r = say(S, "0.0278"); ok(r.log.trap_ids === "Q_INVERTED", "1/Q typed as Q: named (" + r.log.trap_ids + ")");
  r = say(S, "12"); ok(r.log.trap_ids === "EXPONENTS_DROPPED", "exponents dropped: named (" + r.log.trap_ids + ")");
  r = say(S, "36"); ok(S.board.Q_found === "ticked", "Q = 36 ticks");
  r = say(S, "", { pick: "direction:reverse" }); ok(S.board.shift_predicted !== "ticked" && r.log.counted_fail, "reverse with Q < K: a wrong try");
  r = say(S, "", { pick: "direction:forward" }); ok(S.board.shift_predicted === "ticked", "forward: ticked");
  say(S, "Q is below K, so the forward collisions outrun the reverse ones until the ratio of products to reactants climbs to 54.3.");
  r = say(S, "Keeping top and bottom straight was hardest."); ok(r.done && !r.credit && S.clean === false, "done at Independent; not clean after wrong tries"); }

// 3. Q3 (sulfur trioxide, Q > K): reverse is right; typed direction words count
{ const i = byFixed("Q3"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: V.opener_index, stamp: "q3", rung: "independent" });
  say(S, "Sulfur dioxide and oxygen molecules collide to make sulfur trioxide while trioxide molecules collide and break apart; the rates differ until the ratio reaches K.");
  say(S, "", { pick: "eq_q" });
  let r = say(S, "625"); ok(S.board.Q_found === "ticked", "Q = 625 ticks");
  r = say(S, "reverse"); ok(S.board.shift_predicted === "ticked", "the word reverse alone is read as the pick");
  ok(V.board.find(b => b.id === "shift_predicted").right[0] === "direction:reverse", "Q > K: reverse is the right answer"); }

// 4. every placeholder completable clean at Independent
ARCH.variants.forEach((V, i) => {
  const S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: V.opener_index, stamp: "c" + i, rung: "independent" });
  say(S, ACC); say(S, "", { pick: "eq_q" }); say(S, String(V.context.Q));
  const right = V.board.find(b => b.id === "shift_predicted").right[0]; say(S, "", { pick: right });
  say(S, "The collisions in one direction outrun the other until the ratio of products to reactants equals K.");
  const r = say(S, "Setting up the fraction was hardest.");
  ok(r.done && S.clean === true, V.fixed_id + " completable clean: " + (r.done ? "done" : "not done") + ", clean " + S.clean);
});
console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
