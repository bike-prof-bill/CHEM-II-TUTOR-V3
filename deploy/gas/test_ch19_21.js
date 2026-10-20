// Chapters 19 and 21, three sheet-driven archetypes walked in the shell. Run with: node gas/test_ch19_21.js
const CORE = require("./Core.gs"), fs = require("fs");
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const load = (id) => require("./Archetype_" + id + ".gs")[id];
const IDS = ["ch19_cft", "ch21_decay", "ch21_binding"];
const A = Object.fromEntries(IDS.map(id => [id, load(id)]));
for (const id of IDS) ok(A[id].variants.length === 24 && A[id].openers.length === 4 && A[id].variants.every(v => !v.status.startsWith("DRAFT")), id + ": 24 approved problems under 4 scenarios");
const sess = (arch, fid) => { const i = arch.variants.findIndex(v => v.fixed_id === fid), V = arch.variants[i], S = CORE.newSession(arch, { variantIndex: i, openerIndex: V.opener_index, stamp: fid, rung: "independent" }); return { S, V, say: (m, x) => CORE.processTurn(arch, S, Object.assign({ message: m, now: Date.now() }, x || {}), null) }; };
const ACC = "Heat flows into the system and its molecules spread into more arrangements while the surroundings lose a little order; the universe's entropy decides whether it runs.";

// Crystal field MT1: d count from the oxidation state, the picks, t₂g and e_g, unpaired, magnetism
{ const { S, say } = sess(A.ch19_cft, "MT1"); say("Water ligands approach the iron ion and split its d orbitals; a weak field leaves the electrons spread out and unpaired.");
  say("", { pick: "eq_ox" }); say("2"); let r = say("8"); ok(r.log.trap_ids === "D_COUNT_FROM_GROUP", "the group number as the d count: named"); r = say("6"); ok(S.board.d_found === "ticked", "d6 ticks");
  r = say("weak"); ok(S.board.field_pick === "ticked", "weak field ticks"); r = say("high"); ok(S.board.spin_pick === "ticked", "high spin ticks"); say("4"); say("2");
  r = say("0"); ok(r.log.trap_ids === "SPIN_STATE_WRONG", "the low-spin count: named"); r = say("4"); ok(S.board.unpaired_found === "ticked", "four unpaired");
  r = say("paramagnetic"); ok(S.board.magnetic_pick === "ticked", "paramagnetic ticks"); }

// Crystal field CR1: Δoct from the wavelength, nm not converted, Nₐ left out, the colour
{ const { S, say } = sess(A.ch19_cft, "CR1"); say("The titanium ion absorbs green-yellow light to lift a d electron across the splitting; we see the light it leaves, so purple.");
  say("", { pick: "eq_ehc" }); let r = say("3.98e-28 J"); ok(r.log.trap_ids === "NM_NOT_CONVERTED", "the wavelength left in nm: named"); r = say("3.98e-19 J"); ok(S.board.deltaJ_found === "ticked", "Δoct per ion ticks");
  r = say("240 kJ/mol"); ok(S.board.deltakJ_found === "ticked", "per mole ticks"); r = say("purple"); ok(S.board.colour_pick === "ticked", "purple ticks"); }

// Decay CS1: λ, ln vs log, the fraction remaining and the fraction decayed
{ const { S, say } = sess(A.ch21_decay, "CS1"); say("Each cobalt-60 nucleus has the same chance of decaying in each moment, so the same fraction is lost in every half-life.");
  say("", { pick: "eq_halflife" }); let r = say("7.6 y⁻¹"); ok(r.log.trap_ids === "LAMBDA_INVERTED", "λ inverted: named"); r = say("0.1315 y⁻¹"); ok(S.board.lambda_found === "ticked", "λ ticks");
  r = say("0.861"); ok(r.log.trap_ids === "FRACTION_DECAYED", "the fraction decayed: named"); r = say("0.139"); ok(S.board.fraction_found === "ticked", "the fraction left ticks"); }

// Binding HS1: Z, N, the defect without electrons, E in J and MeV, per nucleon divided by Z
{ const { S, say } = sess(A.ch21_binding, "HS1"); say("Two protons and two neutrons are held together by the strong force; the nucleus weighs less than its parts, and that missing mass is the binding energy.");
  say("", { pick: "eq_defect" }); say("2"); say("2"); let r = say("0.0294 amu"); ok(r.log.trap_ids === "ELECTRONS_OMITTED", "the electrons left out: named"); r = say("0.0305 amu"); ok(S.board.defect_found === "ticked", "the defect ticks");
  say("4.55e-12 J"); r = say("2.84e7 MeV"); ok(r.log.trap_ids === "EV_FOR_MEV", "eV for MeV: named"); r = say("28.4 MeV"); ok(S.board.EMeV_found === "ticked", "28.4 MeV ticks");
  r = say("14.2 MeV/nucleon"); ok(r.log.trap_ids === "DIVIDED_BY_Z", "divided by the protons: named"); r = say("7.10 MeV/nucleon"); ok(S.board.per_found === "ticked", "per nucleon ticks");
  r = say("no"); ok(S.board.perturb_1 === "ticked", "no: per nucleon peaks near iron"); }

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
    else if (b.kind === "number") say(V.expected.filter(e => e.state === b.id).map(e => e.value + (e.unit ? " " + (e.unit === "degC" ? "°C" : e.unit === "kJ/mol" ? (b.id === "deltakJ_found" ? "kJ/mol" : "kJ") : e.unit === "J/mol" ? "J" : e.unit === "y" ? "years" : e.unit === "d" ? "days" : e.unit) : "")).join(", "));
    else if (b.kind === "direction") say("", { pick: b.right[0] });
    else if (b.kind === "coefficients") say("coeffs: " + b.right.join(","));
    else if (b.kind === "text") say("The molecules spread into more arrangements and the heat flow sets the balance, so the sign follows.");
  }
  const r = say("The hardest step was keeping the units straight from start to finish.");
  ok(r.done && S.clean === true, id + " " + V.fixed_id + " completable clean: done " + r.done + ", clean " + S.clean + ", at " + CORE.activeState(S, V));
});
console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
