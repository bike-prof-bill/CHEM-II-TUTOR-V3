// The equilibrium archetype (ch13_ice): twelve fixed problems, two scenarios (SCENARIO_CLAUDE, instructor-approved 13 Oct 2026).
// Run with: node gas/test_ice.js
const CORE = require("./Core.gs"), ARCH = require("./Archetype_ch13_ice.gs")["ch13_ice"];
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const byFixed = (id) => ARCH.variants.findIndex(v => v.fixed_id === id);
const say = (S, m, extra) => CORE.processTurn(ARCH, S, Object.assign({ message: m, now: Date.now() }, extra || {}), null);
const roles = {}; ARCH.openers.forEach((o, i) => { roles[i] = o.role || "floater"; });
const ACC_H = "Nitrogen and hydrogen molecules collide and form ammonia while ammonia molecules break apart; the forward and reverse rates become equal.";
const ACC_M = "Carbon monoxide and steam molecules collide and swap atoms to make carbon dioxide and hydrogen; those swap back; the two rates become equal.";

// 1. the bundle
ok(ARCH.variants.length === 12 && ARCH.openers.length === 2, "twelve problems, two scenarios");
ok(ARCH.openers.find(o => o.title === "The Martian Fuel Factory").role === "worked" && ARCH.openers.find(o => o.title === "The Haber-Bosch Harvest").role === "exam", "roles: Martian worked, Haber exam");
ok(CORE.workedVersion(ARCH) === "equal", "the worked rung starts on the equal-start version");
ok(ARCH.variants.filter(v => v.kind === "haber_setup").every(v => !v.board.some(b => b.id === "x_found")), "Haber problems stop before x");
ok(ARCH.variants.filter(v => v.kind === "wgs_equilibrium").every(v => ["x_found", "other_root_checked", "value_found", "leftover_found", "K_confirmed"].every(s => v.board.some(b => b.id === s))), "Martian problems solve through to the check");
ok(!ARCH.variants.find(v => v.fixed_id === "H3").board.some(b => b.id === "Q_found") && ARCH.variants.find(v => v.fixed_id === "H5").expected.some(e => e.state === "Q_found" && e.value === 4), "no Q item when a reactant is absent; H5's Q is 4");
ok(!ARCH.variants.find(v => v.fixed_id === "H1").board.some(b => b.id === "conc_found") && ARCH.variants.find(v => v.fixed_id === "H2").board.some(b => b.id === "conc_found"), "the concentration step only when the vessel is not one litre");

// 2. Haber H3 at Independent: the shift, named wrong tables, the expression's named errors, no x
{ const i = byFixed("H3"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: V.opener_index, stamp: "h3", rung: "independent" });
  let r = say(S, "Ammonia molecules break apart into nitrogen and hydrogen while nitrogen and hydrogen collide to re-form ammonia; the rates become equal.");
  ok(S.board.account_given === "ticked" && r.problem, "account accepted, problem revealed");
  say(S, "", { pick: "eq_k" }); say(S, "", { pick: "approach:solveX" });
  r = say(S, "", { pick: "direction:more" }); ok(S.board.shift_predicted !== "ticked" && r.log.counted_fail, "the wrong shift (more ammonia when only ammonia is present) is a wrong try");
  r = say(S, "", { pick: "direction:less" }); ok(S.board.shift_predicted === "ticked", "shift toward less ammonia: ticked");
  r = say(S, "I: 0 | 0 | 0.500\nC: +x | +x | -x\nE: x | x | 0.500 - x"); ok(r.log.trap_ids === "CHANGE_COEFF_IGNORED" && /three times as fast/.test(r.reply), "change row ignoring the coefficients is named with the approved question: " + r.reply.slice(0, 60));
  r = say(S, "I: 0 | 0 | 0.500\nC: -x | -3x | +2x\nE: -x | -3x | 0.500 + 2x"); ok(r.log.trap_ids === "CHANGE_SIGNS_REVERSED" && /signs in your change row agree/.test(r.reply), "signs against the shift are named");
  r = say(S, "I: 0 | 0 | 0.500\nC: +x | +3x | -2x\nE: x | 3x | 0.500 - 2x"); ok(S.board.table === "ticked" && /TABLE:OK/.test(r.log.structured), "the right table ticks");
  r = say(S, "0.060 = (0.500 - 2x) / ((x)(3x))"); ok(/EQ:TRAP/.test(r.log.structured) && r.log.trap_ids === "EQ_COEFF_NOT_EXPONENT" && /double duty/.test(r.reply), "coefficients not used as exponents: named: " + r.reply.slice(0, 60));
  r = say(S, "0.060 = (0.500 - x)^2 / ((x)(x)^3)"); ok(r.log.trap_ids === "EQ_EXPONENT_NOT_IN_TABLE" && /also in the change row/.test(r.reply), "exponents present, the table's multiples missing: named");
  r = say(S, "0.060 = (0.500 - 2x)^2 / ((x)(3x)^3)"); ok(S.board.expression_set === "ticked", "the right expression ticks");
  r = say(S, "", { pick: "method:sqrt" }); ok(r.log.counted_fail, "the square root is wrong for a quartic");
  r = say(S, "", { pick: "method:solver" }); ok(S.board.method === "ticked", "a graph or a solver: right");
  say(S, "No species runs out: the molecules keep reacting both ways at equal rates, so all three are present.");
  r = say(S, "The signs in the change row were hardest; predict the shift first."); ok(r.done && !r.credit && S.clean === false, "done at Independent; not clean after the wrong tries, so not credit-eligible"); }

// 3. Haber H2 at Faded: concentrations with units, Q = 0, the initial row in moles, a product given a start it did not have
{ const i = byFixed("H2"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: V.opener_index, stamp: "h2" });
  say(S, ACC_H); say(S, "", { pick: "eq_k" }); say(S, "", { pick: "approach:solveX" });
  let r = say(S, "0.500 M, 1.500 M, 0 M"); ok(S.board.conc_found === "ticked", "three concentrations on one line: ticked");
  r = say(S, "0"); ok(S.board.Q_found === "ticked", "Q = 0 with no products: ticked");
  say(S, "", { pick: "direction:more" });
  r = say(S, "I: 1.00 | 3.00 | 0\nC: -x | -3x | +2x\nE: 1.00 - x | 3.00 - 3x | 2x"); ok(r.log.trap_ids === "MOLES_NOT_CONCENTRATION" && /Is your vessel 1.00 L/.test(r.reply), "moles in the initial row: named");
  r = say(S, "I: 0.500 | 1.500 | 0.100\nC: -x | -3x | +2x\nE: 0.500 - x | 1.500 - 3x | 0.100 + 2x"); ok(r.log.trap_ids === "START_ZERO_MISSING", "a start given to the absent product: named: " + r.log.trap_ids);
  ok(r.card, "two wrong tries on the table stage at Faded: the notebook card"); }

// 4. Martian M1 on the Worked rung: show cells, every named error, the roots in order, the check after the leftover, the offer
{ const i = byFixed("M1"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: V.opener_index, stamp: "m1", rung: "worked" });
  ok(/collide and swap atoms/.test(CORE.showFor(ARCH, V, S, "account_given")), "the account show cell is found");
  let r = say(S, ACC_M); ok(/puts products over reactants/.test(r.reply), "the relation show cell is the next prompt");
  say(S, "", { pick: "eq_k" }); say(S, "", { pick: "approach:solveX" }); say(S, "0.500 M & 0.500 M & 0 M & 0 M"); say(S, "0"); say(S, "", { pick: "direction:more" });
  say(S, "I: 0.500 | 0.500 | 0 | 0\nC: -x | -x | +x | +x\nE: 0.500 - x | 0.500 - x | x | x");
  r = say(S, "4 = x^2/(0.500-x)^2"); ok(S.board.expression_set === "ticked" && /perfect square/.test(r.reply) || S.board.expression_set === "ticked", "the expression ticks");
  say(S, "", { pick: "method:sqrt" });
  r = say(S, "1.0"); ok(r.log.trap_ids === "PHANTOM_ROOT" && /What concentration of carbon monoxide does it leave/.test(r.reply), "the phantom root typed as x: named, before x is known");
  r = say(S, "0.4"); ok(r.log.trap_ids === "SQRT_ONE_SIDE" && /both sides, K included/.test(r.reply), "the square root of one side: named");
  ok(!r.card, "no notebook card on the Worked rung after two named errors");
  r = say(S, "0.3333"); ok(S.board.x_found === "ticked" && /negative value/.test(r.reply), "x ticks; the other-root show cell follows");
  r = say(S, "1.0"); ok(S.board.other_root_checked === "ticked", "the same number after x is known is the other root");
  r = say(S, "0.1667 M"); ok(S.board.value_found !== "ticked" && S.board.leftover_found !== "ticked", "the leftover typed at the hydrogen step is kept but ticks nothing yet");
  r = say(S, "3.3333 M"); ok(r.log.trap_ids === "MOLES_NOT_CONCENTRATION" && /Kc uses concentrations/.test(r.reply), "hydrogen in moles: named");
  r = say(S, "0.3333 M"); ok(S.board.value_found === "ticked" && S.board.leftover_found === "ticked", "the hydrogen ticks, and the kept leftover with it");
  r = say(S, "4.00"); ok(S.board.K_confirmed === "ticked", "K put back together, after the leftover: ticked");
  say(S, "No: the molecules keep swapping both ways at equal rates, so the amounts hold.");
  r = say(S, "The roots were hardest; keep the one that leaves every concentration positive.");
  ok(r.done && r.offer && /less steam/.test(r.offer.text) && r.offer.want.version === "unequal" && r.offer.want.extra, "done; the offer of the unequal-start version: " + (r.offer && r.offer.want.version));
  const p2 = CORE.chooseVariant(ARCH.variants, Object.assign({ rolesByOpener: roles }, r.offer.want), []);
  ok(p2 && ["M3", "M4"].indexOf(ARCH.variants[p2.index].fixed_id) > -1, "the offered problem is one of the unequal-start pair"); }

// 5. M3: the quadratic, the square root misapplied; M5: the shift to the left, the negative other root in either sign
{ const i = byFixed("M3"), V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: V.opener_index, stamp: "m3", rung: "independent" });   // Independent: no card after the wrong method pick
  say(S, ACC_M); say(S, "", { pick: "eq_k" }); say(S, "", { pick: "approach:solveX" }); say(S, "0.500 M, 0.300 M, 0 M, 0 M"); say(S, "0"); say(S, "", { pick: "direction:more" });
  say(S, "I: 0.500 | 0.300 | 0 | 0\nC: -x | -x | +x | +x\nE: 0.500 - x | 0.300 - x | x | x"); say(S, "4 = x^2/((0.500-x)(0.300-x))");
  let r = say(S, "", { pick: "method:sqrt" }); ok(r.log.counted_fail, "the square root is wrong when the starts differ");
  say(S, "", { pick: "method:quadratic" });
  r = say(S, "0.3333"); ok(r.log.trap_ids === "SQRT_ON_NONSQUARE" && /one thing times itself/.test(r.reply), "x from a square root on a non-square: named");
  r = say(S, "0.2427"); ok(S.board.x_found === "ticked", "x from the quadratic: ticked");
  r = say(S, "0.8239"); ok(S.board.other_root_checked === "ticked", "the other root");
  const j = byFixed("M5"), W = ARCH.variants[j], T = CORE.newSession(ARCH, { variantIndex: j, openerIndex: W.opener_index, stamp: "m5" });
  say(T, ACC_M); say(T, "", { pick: "eq_k" }); say(T, "", { pick: "approach:solveX" }); say(T, "0 M, 0 M, 0.500 M, 0.500 M");
  r = say(T, "", { pick: "direction:less" }); ok(T.board.shift_predicted === "ticked", "products only: the shift is toward less hydrogen");
  say(T, "I: 0 | 0 | 0.500 | 0.500\nC: +x | +x | -x | -x\nE: x | x | 0.500 - x | 0.500 - x"); say(T, "4 = (0.500-x)^2/x^2"); say(T, "", { pick: "method:sqrt" }); say(T, "0.1667");
  r = say(T, "0.5"); ok(T.board.other_root_checked === "ticked", "the other root typed as its magnitude counts");
  r = say(T, "0.3333 M"); ok(T.board.value_found === "ticked", "[H2] at equilibrium when hydrogen is consumed"); }

// 6. every problem completable at Independent, clean
{ let bad = 0; ARCH.variants.forEach((V, i) => { const S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: V.opener_index, stamp: "all" + i, rung: "independent" });
    const wgs = V.kind === "wgs_equilibrium"; say(S, wgs ? ACC_M : ACC_H); say(S, "", { pick: "eq_k" }); say(S, "", { pick: "approach:solveX" });
    if (V.board.some(b => b.id === "conc_found")) say(S, V.expected.filter(e => e.state === "conc_found").map(e => e.value + " M").join(", "));
    const q = V.expected.find(e => e.state === "Q_found"); if (q) say(S, String(q.value));
    say(S, "", { pick: V.board.find(b => b.id === "shift_predicted").right[0] });
    say(S, ["I", "C", "E"].map(r => r + ": " + V.table.rows[r].join(" | ")).join("\n"));
    say(S, V.eq_checks[0].park_text);
    say(S, "", { pick: V.board.find(b => b.id === "method").right[0] });
    if (wgs) { const g = s => V.expected.find(e => e.state === s); say(S, String(g("x_found").value)); say(S, String(g("other_root_checked").value)); say(S, g("value_found").value + " M"); say(S, g("leftover_found").value + " M"); say(S, String(g("K_confirmed").value)); }
    say(S, "The molecules keep reacting both ways at equal rates, so every species is present and the amounts hold.");
    const r = say(S, "The table was hardest; write the change row from the coefficients.");
    if (!(r.done && S.clean && r.credit)) { bad++; console.log("   not completed:", V.fixed_id, JSON.stringify(S.board), CORE.activeState(S, V)); } });
  ok(bad === 0, bad + " problems could not be completed clean"); }

console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
