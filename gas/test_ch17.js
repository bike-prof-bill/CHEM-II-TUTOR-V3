// Chapter 17s five sheet-driven archetypes walked in the shell. Run with: node gas/test_ch17.js
const CORE = require("./Core.gs"), fs = require("fs");
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const load = (id) => require("./Archetype_" + id + ".gs")[id];
const IDS = ["ch17_balancing", "ch17_cell", "ch17_E_G_K", "ch17_nernst", "ch17_electrolysis"];
const A = Object.fromEntries(IDS.map(id => [id, load(id)]));
for (const id of IDS) ok(A[id].variants.length === 24 && A[id].openers.length === 4 && A[id].variants.every(v => !v.status.startsWith("DRAFT")), id + ": 24 approved problems under 4 scenarios");
const sess = (arch, fid) => { const i = arch.variants.findIndex(v => v.fixed_id === fid), V = arch.variants[i], S = CORE.newSession(arch, { variantIndex: i, openerIndex: V.opener_index, stamp: fid, rung: "independent" }); return { S, V, say: (m, x) => CORE.processTurn(arch, S, Object.assign({ message: m, now: Date.now() }, x || {}), null) }; };
const ACC = "Heat flows into the system and its molecules spread into more arrangements while the surroundings lose a little order; the universe's entropy decides whether it runs.";

// Balancing CN1: the oxidized element, the electron counts, N_ADDED, the coefficient boxes, the lowest-whole-number error, OH⁻ typed
{ const { S, say } = sess(A.ch17_balancing, "CN1"); say("Copper atoms lose electrons to become ions while nitrate gains them and becomes NO; electrons transfer between the half-reactions.");
  let r = say("Cu"); ok(S.board.oxidized_pick === "ticked", "Cu typed: the oxidised element ticks"); say("2"); say("3");
  r = say("5"); ok(r.log.trap_ids === "N_ADDED", "the electrons added: named"); r = say("6"); ok(S.board.n_found === "ticked", "n = 6 ticks");
  ok(r.choices && r.choices.kind === "coefficients" && r.choices.species.length === 6 && r.choices.arrow_after === 3, "the page is sent six coefficient boxes, three before the arrow");
  r = say("coeffs: 6,4,12,6,4,8"); ok(r.log.trap_ids === "NOT_LOWEST_WHOLE_NUMBERS", "a balanced multiple: named");
  r = say("coeffs: 3,2,6,3,2,3"); ok(r.log.counted_fail && !r.log.trap_ids, "an unbalanced set: a plain wrong try");
  r = say("coeffs: 3,2,6,3,2,4"); ok(S.board.coeffs_found === "ticked", "the balanced coefficients tick");
  r = say("OH⁻"); ok(S.board.perturb_1 === "ticked", "OH⁻ typed: the base condition ticks"); }

// Cell DN1: anode, electrons, bridge, E°cell, the swapped sign and the added potentials
{ const { S, say } = sess(A.ch17_cell, "DN1"); say("Zinc atoms lose electrons and become ions; copper ions gain them and plate out; electrons flow through the wire and ions through the bridge.");
  say("", { pick: "eq_ecell" }); let r = say("Cu"); ok(r.log.counted_fail, "Cu as the anode: wrong"); r = say("Zn"); ok(S.board.anode_pick === "ticked", "Zn as the anode ticks");
  r = say("", { pick: "electron_pick:from Zn to Cu" }); ok(S.board.electron_pick === "ticked", "electrons from Zn to Cu"); r = say("", { pick: "bridge_pick:toward Zn" }); ok(S.board.bridge_pick === "ticked", "anions toward Zn");
  r = say("-1.099 V"); ok(r.log.trap_ids === "ANODE_CATHODE_SWAPPED", "the sign swapped: named"); r = say("-0.425 V"); ok(r.log.trap_ids === "POTENTIALS_ADDED", "potentials added: named");
  r = say("1.10 V"); ok(S.board.Ecell_found === "ticked", "E°cell within 0.01 V ticks"); }

// E, G and K AF1: n, E°, ΔG° in kJ, K as a power of ten, ln for log
{ const { S, say } = sess(A.ch17_E_G_K, "AF1"); say("Iron atoms lose electrons to silver ions, which gain them and deposit as metal; two electrons transfer per iron."); say("", { pick: "eq_dg_nfe" });
  say("2"); say("1.247 V"); let r = say("-240600 kJ"); ok(r.log.trap_ids === "J_FOR_KJ", "joules for kilojoules: named"); r = say("-240.6 kJ"); ok(S.board.dG_found === "ticked", "ΔG° ticks");
  r = say("1.95e18"); ok(r.log.trap_ids === "LN_FOR_LOG", "ln for log: named"); r = say("1e42"); ok(S.board.K_found === "ticked", "K typed as a power of ten ticks (1e42 for 1.3 × 10⁴²)"); }

// Nernst DR1: E°, n, Q, E within 0.01 V; Q inverted
{ const { S, say } = sess(A.ch17_nernst, "DR1"); say("Zinc gives electrons to copper ions; with more zinc ions and fewer copper ions the push through the wire is a little weaker."); say("", { pick: "eq_nernst" });
  say("1.099 V"); say("2"); say("30"); let r = say("1.143 V"); ok(/Q_INVERTED|NERNST_SIGN/.test(r.log.trap_ids), "Q inverted or the sign flipped: named"); r = say("1.05 V"); ok(S.board.E_found === "ticked", "E within 0.01 V ticks");
  r = say("yes"); ok(S.board.verdict === "ticked", "spontaneous: ticked"); }

// Electrolysis SP1: charge, the time left in hours, moles, mass within 0.5 %
{ const { S, say } = sess(A.ch17_electrolysis, "SP1"); say("Silver ions gain electrons at the cathode and plate out as metal; the current sets how many electrons arrive."); say("", { pick: "eq_charge" });
  let r = say("10.23 C"); ok(r.log.trap_ids === "TIME_NOT_CONVERTED", "the time left in hours: named"); r = say("36830 C"); ok(S.board.charge_found === "ticked", "Q = It ticks");
  say("0.3817 mol"); say("0.3817 mol"); r = say("40.5 g"); ok(r.log.counted_fail, "a mass 1.6 % off: outside 0.5 %"); r = say("41.2 g"); ok(S.board.mass_found === "ticked", "the mass within 0.5 % ticks"); }

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
    if (b.id === "relation_chosen") { const e = arch.equation_picks.find(e => e.fits.indexOf(V.kind) > -1); say("", { pick: e.id }); }
    else if (b.kind === "number") say(V.expected.filter(e => e.state === b.id).map(e => e.value + (e.unit ? " " + (e.unit === "degC" ? "°C" : e.unit === "kJ/mol" ? "kJ" : e.unit) : "")).join(", "));
    else if (b.kind === "direction") say("", { pick: b.right[0] });
    else if (b.kind === "coefficients") say("coeffs: " + b.right.join(","));
    else if (b.kind === "text") say("The molecules spread into more arrangements and the heat flow sets the balance, so the sign follows.");
  }
  const r = say("The hardest step was matching the electrons between the two half-reactions.");
  ok(r.done && S.clean === true, id + " " + V.fixed_id + " completable clean: done " + r.done + ", clean " + S.clean + ", at " + CORE.activeState(S, V));
});
console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
