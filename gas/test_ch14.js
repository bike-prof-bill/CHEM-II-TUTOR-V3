// The four chapter 14 archetypes walked in the shell on their harness fixtures. Run with: node gas/test_ch14.js
const CORE = require("./Core.gs"), fs = require("fs");
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const load = (id) => require("./Archetype_" + id + "_test.gs")[id];
const PH = load("ch14_ph"), AB = load("ch14_acidbase"), BU = load("ch14_buffer"), TI = load("ch14_titration");
for (const [id, A, n] of [["ch14_ph", PH, 3], ["ch14_acidbase", AB, 5], ["ch14_buffer", BU, 2], ["ch14_titration", TI, 7]])
  ok(A.variants.length === n && !fs.existsSync(__dirname + "/Archetype_" + id + ".gs") && A.variants.every(v => v.status.startsWith("DRAFT")), id + ": " + n + " DRAFT placeholders, nothing shipped");
const sess = (A, fid) => { const i = A.variants.findIndex(v => v.fixed_id === fid), V = A.variants[i], S = CORE.newSession(A, { variantIndex: i, openerIndex: V.opener_index, stamp: fid, rung: "independent" }); return { S, V, say: (m, x) => CORE.processTurn(A, S, Object.assign({ message: m, now: Date.now() }, x || {}), null) }; };
const ACC = "Some molecules hand a proton to water, making hydronium ions, while some hydronium ions hand it back; the two rates are equal so the fraction ionised holds.";

// pH & pOH: S3 barium hydroxide, typed calculations, dilution
{ const { S, say } = sess(PH, "S3"); say("Every formula unit splits into one barium ion and two hydroxide ions; all of it, nothing comes back."); say("", { pick: "eq_ph" });
  let r = say("0.010 M"); ok(S.board.ion_found === "ticked", "[OH-] 0.010 M counts both hydroxides");
  r = say("14 + log(0.010)"); ok(S.board.pH_found === "ticked", "pH typed as 14 + log(0.010): read and ticked");
  r = say("2.0"); ok(S.board.pOH_found === "ticked", "pOH 2.0 ticks");
  r = say("rises"); ok(r.log.counted_fail, "dilution raises a base's pH: wrong"); r = say("falls"); ok(S.board.perturb_1 === "ticked", "falls: ticked"); }

// Acids & Bases: W1 full walk with the named errors
{ const { S, say } = sess(AB, "W1"); say(ACC); say("", { pick: "eq_ka" });
  let r = say("I: 0.1 | 0 | 0\nC: -x | +x | +x\nE: 0.1 - x | x | x"); ok(S.board.table === "ticked", "the table ticks");
  r = say("1.8e-5 = x*x/((0.1 - x)*55.5)"); ok(/WATER_IN_EXPRESSION/.test(r.log.trap_ids), "water in the expression: named");
  say("1.8e-5 = x*x/(0.1 - x)"); r = say("", { pick: "method:quadratic" }); ok(r.log.counted_fail, "the quadratic where small-x holds: a wrong try");
  say("", { pick: "method:smallx" }); r = say("1.8e-6 M"); ok(r.log.trap_ids === "SQRT_FORGOTTEN", "x = Ka·c: named");
  say("sqrt(1.8e-5*0.1) M"); r = say("4.74"); ok(r.log.trap_ids === "PKA_TYPED_AS_PH", "pKa as pH: named"); say("2.87");
  r = say("0.013"); ok(r.log.trap_ids === "PERCENT_AS_FRACTION", "fraction for percent: named"); say("1.3 %"); say("", { pick: "approx:holds" });
  r = say("", { pick: "p1:falls" }); ok(r.log.trap_ids === "DILUTION_IONIZATION_FALLS", "percent falls on dilution: a named wrong pick"); say("rises"); say("More water per molecule, so a larger fraction ionises.");
  r = say("", { pick: "p2:falls" }); ok(r.log.trap_ids === "CONJUGATE_LOWERS_PH", "pH falls on added acetate: a named wrong pick"); say("rises"); say("The added acetate pushes the equilibrium back.");
  say("About one molecule in seventy-five has given up its proton."); r = say("The 5 percent check was hardest."); ok(r.done, "done"); }

// Buffers: F1, the pH after each addition, the free-base error named
{ const { S, say } = sess(BU, "F1"); say("Acetic acid molecules and acetate ions share the water; protons move between them and water so the hydronium level holds."); say("", { pick: "eq_hh" }); say("1.0"); say("4.74");
  let r = say("", { pick: "p1:unchanged" }); ok(r.log.trap_ids === "BUFFER_PH_FIXED", "no change at all: named"); say("rises"); say("The hydroxide takes a proton from acetic acid, making more acetate; the ratio moves a little.");
  r = say("12.0"); ok(r.log.trap_ids === "ADDED_NOT_CONSUMED", "the added base treated as free: named (" + r.reply.slice(0, 50) + ")");
  r = say("4.83"); ok(S.board.pH_after_1 === "ticked", "pH after the base: 4.83 ticks");
  say("falls"); say("The hydronium is taken up by acetate, making acetic acid."); r = say("4.66"); ok(S.board.pH_after_2 === "ticked", "pH after the acid: 4.66 ticks");
  say("Both partners are present in quantity, so the ratio barely moves."); r = say("Seeing what the added base reacts with was hardest."); ok(r.done, "done"); }

// Titration: T2 at equivalence; T3 after; U2 strong at 7
{ const { S, say } = sess(TI, "T2"); say("Every acetic acid molecule has given its proton to hydroxide; what is left is acetate, which takes a few protons back from water.");
  let r = say("", { pick: "region:before" }); ok(r.log.counted_fail, "before equivalence: wrong region"); r = say("", { pick: "region:at" }); ok(S.board.region_chosen === "ticked", "at equivalence: ticked");
  r = say("", { pick: "eq_hh" }); ok(r.log.counted_fail, "Henderson-Hasselbalch at equivalence: wrong relation"); say("", { pick: "eq_kakb" });
  r = say("0.0025 mol, 0.0025 mol"); ok(S.board.moles_found === "ticked", "both moles tick");
  r = say("0.1 M"); ok(!r.log.counted_fail && S.board.conc_found !== "ticked", "the sample volume alone gives 0.1 M, which is the given restated: not a tick, not a wrong try");
  say("0.050 M"); r = say("5.6e-10"); ok(S.board.Kb_found === "ticked", "Kb = Kw/Ka ticks");
  r = say("9.5e-4 M"); ok(r.log.trap_ids === "KA_FOR_HYDROLYSIS", "x from Ka instead of Kb: named");
  say("5.3e-6 M"); say("5.28"); r = say("7.0"); ok(r.log.trap_ids === "PH_7_AT_EQUIVALENCE", "pH 7 at a weak acid's equivalence: named");
  r = say("8.72"); ok(S.board.pH_found === "ticked", "pH 8.72 ticks (OpenStax Example 14.21)");
  say("Above 7, because the acetate left in the flask takes protons from water and leaves hydroxide behind."); say("The salt is not neutral."); r = say("Choosing Kb instead of Ka at the end was the hardest step for me."); ok(r.done, "done"); }
{ const { S, say } = sess(TI, "T3"); say("The acid is gone and hydroxide is piling up; it dominates."); say("", { pick: "region:after" }); say("", { pick: "eq_excess" }); say("0.0025 mol, 0.00375 mol");
  let r = say("0.05 M"); ok(r.log.trap_ids === "VOLUME_NOT_TOTALED", "excess over the sample volume alone: named"); say("0.020 M"); say("1.70"); r = say("12.30"); ok(S.board.pH_found === "ticked", "pH 12.30 ticks"); }
{ const { S, say } = sess(TI, "U2"); say("Every hydronium has met a hydroxide; only water and spectator ions are left."); say("", { pick: "region:at" }); say("", { pick: "eq_ph" }); say("0.0025 mol, 0.0025 mol");
  let r = say("7.00"); ok(S.board.pH_found === "ticked", "strong-strong equivalence: pH 7.00"); }

// every placeholder of every archetype completable clean
for (const A of [PH, AB, BU, TI]) A.variants.forEach((V, i) => {
  const S = CORE.newSession(A, { variantIndex: i, openerIndex: V.opener_index, stamp: "c" + i, rung: "independent" });
  const say = (m, x) => CORE.processTurn(A, S, Object.assign({ message: m, now: Date.now() }, x || {}), null);
  const ex = (st) => V.expected.filter(e => e.state === st);
  say(ACC);
  for (const b of V.board) {
    if (b.id === "account_given") continue;
    if (b.id === "relation_chosen") { const right = A.equation_picks.find(e => e.fits.indexOf(V.kind) > -1); say("", { pick: right.id }); }
    else if (b.kind === "number") say(ex(b.id).map(e => e.value + (e.unit ? " " + e.unit : "")).join(", "));
    else if (b.kind === "table") { const t = V.table.rows; say("I: " + t.I.join(" | ") + "\nC: " + t.C.join(" | ") + "\nE: " + t.E.join(" | ")); }
    else if (b.kind === "equation") say(V.eq_checks[0].park_text);
    else if ((b.kind === "pick" || b.kind === "direction") && b.right) say("", { pick: b.right[0] });
    else if (b.kind === "text") say("The particles keep trading protons both ways at equal rates, so the amounts hold.");
  }
  const r = say("The hardest step was the check.");
  ok(r.done && S.clean === true, A.archetype_id + " " + V.fixed_id + " completable clean: done " + r.done + ", clean " + S.clean + ", at " + CORE.activeState(S, V));
});
console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
