// The combined chapter 13 archetype (ch13_eq) walked in the shell on the harness fixture: Q first, the ICE work, two perturbations.
// Run with: node gas/test_eq.js
const CORE = require("./Core.gs"), ARCH = require("./Archetype_ch13_eq_test.gs")["ch13_eq"];
const fs = require("fs");
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const byFixed = (id) => ARCH.variants.findIndex(v => v.fixed_id === id);
const say = (S, m, extra) => CORE.processTurn(ARCH, S, Object.assign({ message: m, now: Date.now() }, extra || {}), null);
const ACC_H = "Nitrogen and hydrogen molecules collide and form ammonia while ammonia molecules break apart; the forward and reverse rates become equal.";
const ACC_M = "Carbon monoxide and steam molecules collide and swap atoms to make carbon dioxide and hydrogen; those swap back; the two rates become equal.";
const ACC_A = "Silver and chloride ions leave the solid crystal into the water while ions in the water collide and settle back onto the solid; the two rates are equal, so the ions keep trading places.";
const WHY = "The added change makes one set of collisions outrun the other until the ratio of products to reactants is back at K.";

ok(ARCH.variants.length === 13 && ARCH.openers.length === 3, "thirteen problems, three harness openers");
ok(!fs.existsSync(__dirname + "/Archetype_ch13_eq.gs"), "no shipped bundle while no scenario is approved");
ok(ARCH.variants.every(v => v.board.slice(-6).map(b => b.id).join(">") === "perturb_1>perturb_1_why>perturb_2>perturb_2_why>meaning_given>reflection"), "every problem ends with two perturbations, the meaning, the reflection");

// 1. the tracer A1 at Independent: Q = K, no shift, the common ion, heat
{ const i = byFixed("A1"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: V.opener_index, stamp: "a1", rung: "independent" });
  let r = say(S, ACC_A); ok(S.board.account_given === "ticked" && r.problem, "account accepted, problem revealed");
  r = say(S, "", { pick: "eq_q" }); ok(S.board.relation_chosen === "ticked", "the Q expression counts as the pick");
  r = say(S, "1.8e-10"); ok(S.board.Q_found !== "ticked", "K restated as Q (1.8e-10) does not tick: Q from the data is 1.7e-10");
  r = say(S, "1.7e-10"); ok(S.board.Q_found === "ticked", "Q = 1.7e-10, two figures, ticks; the direction item then reads it as equal to K");
  r = say(S, "", { pick: "direction:forward" }); ok(S.board.shift_predicted !== "ticked" && r.log.counted_fail, "forward at Q = K: a wrong try");
  r = say(S, "neither"); ok(S.board.shift_predicted === "ticked", "typed 'neither': ticked");
  r = say(S, "", { pick: "p1:forward" }); ok(S.board.perturb_1 !== "ticked" && r.log.counted_fail, "common ion added, forward: wrong");
  r = say(S, "", { pick: "p1:reverse" }); ok(S.board.perturb_1 === "ticked", "common ion added, reverse: ticked");
  r = say(S, WHY); ok(S.board.perturb_1_why === "ticked", "the explanation in words ticks the why item");
  r = say(S, "forward"); ok(S.board.perturb_2 === "ticked", "warming an endothermic dissolution, typed forward: ticked");
  say(S, WHY);
  say(S, "Adding solid changed nothing because the solid is not in the expression; the tracer shows ions still trading places.");
  r = say(S, "Leaving the solid out was hardest."); ok(r.done && S.clean === true && r.credit, "done at Independent; one wrong try per stage keeps the run clean (two in one stage would not)"); }

// 2. Haber H3 at Independent: the ICE work unchanged, then the perturbations
{ const i = byFixed("H3"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: V.opener_index, stamp: "h3", rung: "independent" });
  say(S, "Ammonia molecules break apart into nitrogen and hydrogen while nitrogen and hydrogen collide to re-form ammonia; the rates become equal.");
  say(S, "", { pick: "eq_k" });
  let r = say(S, "", { pick: "direction:less" }); ok(!S.board.shift_predicted, "an option id from the old archetype is not a pick here");
  r = say(S, "", { pick: "direction:reverse" }); ok(S.board.shift_predicted === "ticked", "only ammonia present: reverse ticks");
  r = say(S, "I: 0 | 0 | 0.500\nC: +x | +x | -x\nE: x | x | 0.500 - x"); ok(r.log.trap_ids === "CHANGE_COEFF_IGNORED", "change row ignoring the coefficients: named");
  r = say(S, "I: 0 | 0 | 0.500\nC: +x | +3x | -2x\nE: x | 3x | 0.500 - 2x"); ok(S.board.table === "ticked", "the right table ticks");
  r = say(S, "0.060 = (0.500 - 2x)^2 / ((x)(3x)^3)"); ok(S.board.expression_set === "ticked", "the right expression ticks");
  r = say(S, "", { pick: "method:solver" }); ok(S.board.method === "ticked", "a solver for the quartic");
  r = say(S, "", { pick: "p1:forward" }); ok(S.board.perturb_1 === "ticked", "ammonia drawn off: forward");
  say(S, WHY);
  r = say(S, "", { pick: "p2:forward" }); ok(r.log.counted_fail && S.board.perturb_2 !== "ticked", "heating an exothermic reaction, forward: wrong");
  r = say(S, "", { pick: "p2:reverse" }); ok(S.board.perturb_2 === "ticked", "reverse: ticked");
  say(S, WHY); say(S, "No species runs out: both directions keep running at equal rates.");
  r = say(S, "Predict the shift before the table."); ok(r.done, "done"); }

// 3. Martian M1 on the Worked rung: the solve chain, then no shift on compression (equal gas moles)
{ const i = byFixed("M1"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: V.opener_index, stamp: "m1", rung: "worked" });
  say(S, ACC_M); say(S, "", { pick: "eq_k" }); say(S, "0.500 M & 0.500 M & 0 M & 0 M"); say(S, "0"); say(S, "", { pick: "direction:forward" });
  say(S, "I: 0.500 | 0.500 | 0 | 0\nC: -x | -x | +x | +x\nE: 0.500 - x | 0.500 - x | x | x");
  say(S, "4 = x^2/(0.500-x)^2"); say(S, "", { pick: "method:sqrt" });
  let r = say(S, "1.0"); ok(r.log.trap_ids === "PHANTOM_ROOT", "the phantom root named before x is known");
  r = say(S, "0.3333"); ok(S.board.x_found === "ticked", "x ticks");
  say(S, "1.0"); say(S, "0.3333 M"); r = say(S, "0.1667 M"); ok(S.board.leftover_found === "ticked", "the leftover ticks");
  r = say(S, "4.00"); ok(S.board.K_confirmed === "ticked", "K put back together");
  r = say(S, "", { pick: "p1:forward" }); ok(S.board.perturb_1 === "ticked", "more steam: forward");
  say(S, WHY);
  r = say(S, "", { pick: "p2:neither" }); ok(S.board.perturb_2 === "ticked", "squeezing the chamber with equal gas moles each side: no shift");
  say(S, WHY); say(S, "The amounts hold because the swaps run both ways at the same rate.");
  r = say(S, "The roots were hardest."); ok(r.done, "done on the worked rung"); }

// 4. every problem completable clean at Independent
ARCH.variants.forEach((V, i) => {
  const S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: V.opener_index, stamp: "c" + i, rung: "independent" });
  const acc = V.kind === "haber_setup" ? ACC_H : (V.kind === "wgs_equilibrium" ? ACC_M : ACC_A);
  say(S, acc); say(S, "", { pick: "eq_k" });
  const ex = (st) => V.expected.filter(e => e.state === st);
  if (V.board.some(b => b.id === "conc_found")) say(S, ex("conc_found").map(e => e.value + " M").join(", "));
  if (V.board.some(b => b.id === "Q_found")) say(S, String(ex("Q_found")[0].value));
  say(S, "", { pick: V.board.find(b => b.id === "shift_predicted").right[0] });
  if (V.table) {
    const t = V.table.rows; say(S, "I: " + t.I.join(" | ") + "\nC: " + t.C.join(" | ") + "\nE: " + t.E.join(" | "));
    say(S, V.eq_checks[0].park_text); say(S, "", { pick: V.board.find(b => b.id === "method").right[0] });
    if (V.board.some(b => b.id === "x_found")) { say(S, String(ex("x_found")[0].value)); say(S, String(ex("other_root_checked")[0].value)); say(S, ex("value_found")[0].value + " M"); say(S, ex("leftover_found")[0].value + " M"); say(S, String(ex("K_confirmed")[0].value)); }
  }
  say(S, "", { pick: V.board.find(b => b.id === "perturb_1").right[0] }); say(S, WHY);
  say(S, "", { pick: V.board.find(b => b.id === "perturb_2").right[0] }); say(S, WHY);
  say(S, "The amounts hold because the particles keep reacting both ways at equal rates.");
  const r = say(S, "Setting up the fraction was hardest.");
  ok(r.done && S.clean === true, V.fixed_id + " completable clean: done " + r.done + ", clean " + S.clean + ", at " + CORE.activeState(S, V));
});
console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
