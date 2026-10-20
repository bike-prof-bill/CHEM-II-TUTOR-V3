// Chapter 16's five sheet-driven archetypes walked in the shell. Run with: node gas/test_ch16.js
const CORE = require("./Core.gs"), fs = require("fs");
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const load = (id) => require("./Archetype_" + id + ".gs")[id];
const IDS = ["ch16_entropy", "ch16_free_energy", "ch16_spontaneity", "ch16_equilibrium_G", "ch16_G_and_K"];
const A = Object.fromEntries(IDS.map(id => [id, load(id)]));
for (const id of IDS) ok(A[id].variants.length === 24 && A[id].openers.length === 4 && A[id].variants.every(v => !v.status.startsWith("DRAFT")), id + ": 24 approved problems under 4 scenarios");
const sess = (arch, fid) => { const i = arch.variants.findIndex(v => v.fixed_id === fid), V = arch.variants[i], S = CORE.newSession(arch, { variantIndex: i, openerIndex: V.opener_index, stamp: fid, rung: "independent" }); return { S, V, say: (m, x) => CORE.processTurn(arch, S, Object.assign({ message: m, now: Date.now() }, x || {}), null) }; };
const ACC = "Heat flows into the system and its molecules spread into more arrangements while the surroundings lose a little order; the universe's entropy decides whether it runs.";

// Entropy MI1: the sign of the surroundings' change, kJ not converted, verdict, perturbation
{ const { S, say } = sess(A.ch16_entropy, "MI1"); say(ACC); say("", { pick: "eq_dssurr" });
  let r = say("-0.0212 J/K"); ok(r.log.trap_ids === "KJ_NOT_CONVERTED", "ΔH left in kJ: named");
  r = say("21.19 J/K"); ok(r.log.trap_ids === "SURROUNDINGS_SIGN", "the surroundings' sign wrong: named");
  r = say("-21.2 J/K"); ok(S.board.dSsurr_found === "ticked", "ΔS(surr) ticks");
  r = say("0.91 J/K"); ok(S.board.dSuniv_found === "ticked", "ΔS(univ) ticks");
  r = say("no"); ok(r.log.trap_ids === "SPONTANEITY_FROM_SYSTEM" && r.log.counted_fail, "the wrong verdict is a named pick");
  r = say("yes"); ok(S.board.verdict === "ticked", "yes: ticked"); r = say("rises"); ok(S.board.perturb_1 === "ticked", "the perturbation ticks"); }

// Free energy WB1: two routes, J mixed with kJ, TΔS added
{ const { S, say } = sess(A.ch16_free_energy, "WB1"); say("Liquid water molecules escape into the gas; bonds between them break and the molecules spread out; it costs heat and gains disorder."); say("", { pick: "eq_dg" });
  let r = say("-44.01 kJ"); ok(r.log.trap_ids === "PRODUCTS_REACTANTS_SWAPPED", "reactants minus products: named");
  r = say("44.01 kJ"); ok(S.board.dH_found === "ticked", "ΔH° ticks"); say("118.8 J/K");
  r = say("-35358 kJ"); ok(r.log.trap_ids === "J_FOR_KJ", "J mixed with kJ: named"); r = say("79.4 kJ"); ok(r.log.trap_ids === "TDS_SIGN", "TΔS added: named");
  r = say("8.6 kJ"); ok(S.board.dG_found === "ticked", "ΔG° by the first route ticks"); r = say("8.5 kJ"); ok(S.board.dGf_found === "ticked", "ΔG° by the second route ticks, told apart by its own step");
  r = say("no"); ok(S.board.verdict === "ticked", "not spontaneous: ticked"); r = say("unchanged"); ok(r.log.trap_ids === "EXTENSIVE_IGNORED", "no change on doubling: named"); r = say("doubles"); ok(S.board.perturb_1 === "ticked", "doubles: ticked"); }

// Spontaneity LK1: the case pick, the crossover temperature in kelvins
{ const { S, say } = sess(A.ch16_spontaneity, "LK1"); say("Heating the stone breaks the carbonate into oxide and a gas whose molecules spread out; it takes heat and gains disorder."); say("", { pick: "eq_dg" });
  let r = say("", { pick: "case_pick:always" }); ok(r.log.trap_ids === "CASE_WRONG", "the wrong sign case is named"); r = say("high"); ok(S.board.case_pick === "ticked", "high: ticked");
  r = say("1.35 K"); ok(r.log.trap_ids === "J_KJ_MISMATCH", "kJ over J/K without converting: named"); r = say("1350 K"); ok(S.board.Tcross_found === "ticked", "1350 K ticks");
  r = say("149 kJ"); ok(S.board.dG_found === "ticked", "ΔG° at 298 K ticks"); r = say("no"); ok(S.board.verdict === "ticked", "verdict ticks"); }

// Equilibrium PB1: the boiling point in kelvins and Celsius; the kelvin value offered as Celsius
{ const { S, say } = sess(A.ch16_equilibrium_G, "PB1"); say("Liquid molecules leave for the gas at the same rate gas molecules return when ΔG is zero; that is the boiling point."); say("", { pick: "eq_dg" });
  say("44.01 kJ"); say("118.8 J/K"); let r = say("0.37 K"); ok(r.log.trap_ids === "J_KJ_MISMATCH", "kJ over J/K: named"); r = say("370.5 K"); ok(S.board.Teq_found === "ticked", "370.5 K ticks");
  r = say("370.5 °C"); ok(r.log.trap_ids === "KELVIN_AS_CELSIUS", "kelvins offered as Celsius: named"); r = say("97.3 °C"); ok(S.board.TeqC_found === "ticked", "97.3 °C ticks"); }

// G and K SK1: ΔG° then K, log for ln, the sign dropped
{ const { S, say } = sess(A.ch16_G_and_K, "SK1"); say("A few silver and chloride ions leave the crystal and as many return; the energy cost keeps the dissolved amount tiny."); say("", { pick: "eq_dgf" });
  say("55.71 kJ"); let r = say("3.3e-23"); ok(r.log.trap_ids === "LOG_FOR_LN", "log for ln: named"); r = say("5.8e9"); ok(r.log.trap_ids === "SIGN_DROPPED", "the sign dropped: named");
  r = say("1.7e-10"); ok(S.board.K_found === "ticked", "Ksp from ΔG° ticks"); r = say("reactants"); ok(S.board.favored === "ticked", "reactants favored: ticked"); }

// every problem completable clean
for (const id of IDS) A[id].variants.forEach((V, i) => {
  const arch = A[id], S = CORE.newSession(arch, { variantIndex: i, openerIndex: V.opener_index, stamp: "c" + i, rung: "independent" });
  const say = (m, x) => CORE.processTurn(arch, S, Object.assign({ message: m, now: Date.now() }, x || {}), null);
  const kw = (arch.openers[V.opener_index].keywords || []).filter(k => /^[A-Za-z][A-Za-z -]*$/.test(k)).slice(0, 4).join(", ");
  say("At the particle level the " + kw + " are what matter here; the molecules keep moving both ways and the balance of heat and spreading decides which way they settle.");
  if (S.board.account_given !== "ticked") say(String(arch.openers[V.opener_index].model_answer || "").replace(/[-+−]?\d[\d.,]*\s*(×\s*10\S*)?/g, "").replace(/[=≈]/g, " "));   // fallback stand-in: the scenario's own model answer with its numbers removed
  if (S.board.account_given !== "ticked") say("The " + (arch.openers[V.opener_index].keywords || []).map(k => k.replace(/[-+−]?\d[\d.,]*/g, "").replace(/[=≈]/g, " ").trim()).filter(Boolean).join(", ") + " matter here: " + (arch.mechanism_words || []).slice(0, 6).join(", ") + ", each one at the particle level, at equal rates both ways.");   // a third stand-in from every keyword without its numbers
  for (const b of V.board) {
    if (b.id === "account_given") continue;
    if (b.id === "relation_chosen") { say("", { pick: arch.equation_picks.find(e => e.fits.indexOf(V.kind) > -1).id }); }
    else if (b.kind === "number") say(V.expected.filter(e => e.state === b.id).map(e => e.value + (e.unit ? " " + (e.unit === "degC" ? "°C" : e.unit === "kJ/mol" ? "kJ" : e.unit) : "")).join(", "));
    else if (b.kind === "direction") say("", { pick: b.right[0] });
    else if (b.kind === "text") say("The molecules spread into more arrangements and the heat flow sets the balance, so the sign follows.");
  }
  const r = say("The hardest step was keeping joules and kilojoules apart.");
  ok(r.done && S.clean === true, id + " " + V.fixed_id + " completable clean: done " + r.done + ", clean " + S.clean + ", at " + CORE.activeState(S, V));
});
console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
