// The three chapter 15 skeletons walked in the shell on their harness fixtures. Run with: node gas/test_ch15.js
const CORE = require("./Core.gs"), fs = require("fs");
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const load = (id) => require("./Archetype_" + id + "_test.gs")[id];
const KS = load("ch15_ksp"), CI = load("ch15_common_ion"), QS = load("ch15_qsp"), CX = load("ch15_complex");
for (const [id, A] of [["ch15_ksp", KS], ["ch15_common_ion", CI], ["ch15_qsp", QS], ["ch15_complex", CX]])
  ok(A.variants.length === 24 && A.openers.length === 4 && fs.existsSync(__dirname + "/Archetype_" + id + ".gs") && A.variants.every(v => !v.status.startsWith("DRAFT")), id + ": 24 approved problems under 4 scenarios, shipped");
const sess = (A, fid) => { const i = A.variants.findIndex(v => v.fixed_id === fid), V = A.variants[i], S = CORE.newSession(A, { variantIndex: i, openerIndex: V.opener_index, stamp: fid, rung: "independent" }); return { S, V, say: (m, x) => CORE.processTurn(A, S, Object.assign({ message: m, now: Date.now() }, x || {}), null) }; };
const ACC = "Ions leave the crystal lattice into the water while ions in the water collide with the solid and settle back; the two rates are equal, so the amounts hold.";

// Ksp S2: CaF2, the s table, the 4s^3 expression, the named roots, the ion step, grams, the common-ion prediction
{ const { S, say } = sess(KS, "MK3"); say(ACC); say("", { pick: "eq_ksp" });
  let r = say("I: 0 | 0\nC: +x | +x\nE: x | x"); ok(r.log.trap_ids === "COEFFICIENT_DROPPED_IN_TABLE", "a change row of +s for fluoride: named");
  r = say("I: 0 | 0\nC: +x | +2x\nE: x | 2x"); ok(S.board.table === "ticked", "the s table ticks");
  r = say("4e-11 = x * (2x)"); ok(/COEFF_NOT_EXPONENT/.test(r.log.trap_ids), "the exponent dropped from (2s)^2: named");
  r = say("4e-11 = x * (2x)^2"); ok(S.board.expression_set === "ticked", "Ksp = 4s^3 ticks");
  r = say("1e-11 M"); ok(r.log.trap_ids === "ROOT_FORGOTTEN", "Ksp/4 without the cube root: named");
  r = say("3.42e-4 M"); ok(r.log.trap_ids === "COEFFICIENT_FORGOTTEN", "the cube root of Ksp alone: named");
  r = say("2.15e-4 M"); ok(S.board.s_found === "ticked", "s ticks");
  r = say("2.15e-4 M"); ok(!r.log.counted_fail && S.board.conc_found !== "ticked", "s typed where [F-] = 2s is asked reads as a restatement, not a wrong try");
  r = say("4.3e-4 M"); ok(S.board.conc_found === "ticked", "[F-] = 2s ticks");
  r = say("2.15e-4 g/L"); ok(r.log.trap_ids === "GRAMS_WITHOUT_MOLAR_MASS", "moles per litre offered as grams per litre: named");
  r = say("0.0168 g/L"); ok(S.board.grams_found === "ticked", "grams per litre ticks (molar mass 78.07)");
  r = say("", { pick: "p1:rises" }); ok(r.log.trap_ids === "SOLUBILITY_RISES_WITH_COMMON_ION", "more dissolving with a common ion: a named wrong pick");
  r = say("falls"); ok(S.board.perturb_1 === "ticked", "falls: ticked"); }

// Common ion C3: the common cation, small-s, the pure-water value named
{ const { S, say } = sess(CI, "SW3"); say(ACC); say("", { pick: "eq_ksp" });
  say("I: 0.02 | 0\nC: +x | +2x\nE: 0.02 + x | 2x"); let r = say("4e-11 = (0.02 + x) * (2x)^2"); ok(S.board.expression_set === "ticked", "the expression with the common ion ticks");
  r = say("", { pick: "method:pure" }); ok(r.log.counted_fail, "solving as in pure water: wrong"); say("", { pick: "method:smalls" });
  r = say("2.15e-4 M"); ok(r.log.trap_ids === "COMMON_ION_IGNORED", "the pure-water s where the common ion sits: named");
  r = say("2.24e-5 M"); ok(S.board.s_found === "ticked", "s with the common ion ticks");
  say("2.15e-4 M"); r = say("9.6"); ok(S.board.ratio_found === "ticked", "about ten times smaller"); }

// Qsp Q3: dilution on mixing, the undiluted concentration named, Q below Ksp, no precipitate
{ const { S, say } = sess(QS, "CT5"); say("Lead ions and iodide ions are mixed; if they meet often enough they lock into a lattice, otherwise they stay apart in the water."); say("", { pick: "eq_qsp" });
  let r = say("1.0e-3 M, 2.0e-3 M"); ok(!r.log.counted_fail && S.board.conc_found !== "ticked", "the concentrations before mixing are the givens restated: no tick, no wrong try (the Q built from them is named at the Q step)");
  r = say("2.5e-4 M, 1.5e-3 M"); ok(S.board.conc_found === "ticked", "both diluted concentrations tick");
  r = say("4e-9"); ok(/DILUTION_IGNORED/.test(r.log.trap_ids), "Q from the undiluted concentrations: named");
  r = say("5.6e-10"); ok(S.board.Q_found === "ticked", "Q ticks");
  r = say("", { pick: "v:forms" }); ok(r.log.trap_ids === "PRECIPITATE_WHEN_Q_LESS", "a precipitate predicted with Q below Ksp: named");
  r = say("none"); ok(S.board.verdict === "ticked", "none: ticked"); r = say("rises"); ok(S.board.perturb_1 === "ticked", "more iodide: Q rises"); }

// Complex M1: complete formation, Kd, the dissociation table, the ligand-left and exponent errors, more ligand lowers the free metal
{ const { S, say } = sess(CX, "DP1"); say("Ammonia molecules bind to each silver ion through their lone pairs, two to a silver; a few complexes let an ammonia go and take it back; the rates are equal."); say("", { pick: "eq_kf" });
  let r = say("0.005 M, 0.5 M"); ok(S.board.complete_found === "ticked", "the complex, and the ligand left within the amount consumed (0.50 for 0.49 with a large excess), tick");
  r = say("5.9e-8"); ok(S.board.Kd_found === "ticked", "Kd = 1/Kf ticks");
  r = say("I: 0.005 | 0 | 0.49\nC: -x | +x | +x\nE: 0.005 - x | x | 0.49 + x"); ok(r.log.trap_ids === "COEFFICIENT_DROPPED_IN_TABLE", "+x for two ammonias: named");
  r = say("I: 0.005 | 0 | 0.49\nC: -x | +x | +2x\nE: 0.005 - x | x | 0.49 + 2x"); ok(S.board.table === "ticked", "the dissociation table ticks");
  r = say("5.9e-8 = x * (0.49 + 2x)^2 / (0.005 - x)"); ok(S.board.expression_set === "ticked", "the Kd expression ticks");
  say("", { pick: "method:smallx" }); r = say("6.0e-10 M"); ok(r.log.trap_ids === "LIGAND_EXPONENT_DROPPED", "the ligand to the first power: named");
  r = say("1.2e-9 M"); ok(S.board.x_found === "ticked", "free [Ag+] ticks");
  r = say("4.1e6"); ok(S.board.ratio_found === "ticked", "four million times smaller");
  r = say("", { pick: "p1:rises" }); ok(r.log.trap_ids === "FREE_METAL_RISES_WITH_LIGAND", "more free metal with more ligand: named"); r = say("falls"); ok(S.board.perturb_1 === "ticked", "falls: ticked"); }

// every placeholder completable clean
for (const A of [KS, CI, QS, CX]) A.variants.forEach((V, i) => {
  const S = CORE.newSession(A, { variantIndex: i, openerIndex: V.opener_index, stamp: "c" + i, rung: "independent" });
  const say = (m, x) => CORE.processTurn(A, S, Object.assign({ message: m, now: Date.now() }, x || {}), null);
  const ex = (st) => V.expected.filter(e => e.state === st);
  say(ACC);
  for (const b of V.board) {
    if (b.id === "account_given") continue;
    if (b.id === "relation_chosen") { say("", { pick: A.equation_picks.find(e => e.fits.indexOf(V.kind) > -1).id }); }
    else if (b.kind === "number") say(ex(b.id).map(e => e.value + (e.unit ? " " + e.unit : "")).join(", "));
    else if (b.kind === "table") { const t = V.table.rows; say("I: " + t.I.join(" | ") + "\nC: " + t.C.join(" | ") + "\nE: " + t.E.join(" | ")); }
    else if (b.kind === "equation") say(V.eq_checks[0].park_text);
    else if ((b.kind === "pick" || b.kind === "direction") && b.right) say("", { pick: b.right[0] });
    else if (b.kind === "text") say("The ions keep leaving and rejoining the crystal or the complex at equal rates, so the amounts hold.");
  }
  const r = say("The hardest step was the table.");
  ok(r.done && S.clean === true, A.archetype_id + " " + V.fixed_id + " completable clean: done " + r.done + ", clean " + S.clean + ", at " + CORE.activeState(S, V));
});
console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
