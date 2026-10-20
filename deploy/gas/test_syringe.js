// node gas/test_syringe.js -- The Syringe Boiling Trick (SCENARIO_CLAUDE, approved 10 Oct): scenario overrides, the direction
// item on pressure problems, the two named errors, the reflection, the picture credit.
const CORE = require("./Core.gs"); const ARCH = require("./Archetype_ch10_cc.gs")["ch10_cc"];
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const say = (S, m, model, extra) => CORE.processTurn(ARCH, S, Object.assign({ message: m, now: 1 }, extra || {}), model || null);
const oi = ARCH.openers.findIndex(o => o.title === "The Syringe Boiling Trick"); const OP = ARCH.openers[oi];
const SYR = ARCH.variants.filter(v => v.opener_index === oi);
ok(oi > -1 && SYR.length === 6 && SYR.every(v => v.kind === "P1" || v.kind === "P2"), "the scenario exists and draws only pressure problems: " + SYR.map(v => v.kind).join(","));
ok(OP.label_words.indexOf("vacuum") > -1 && /syringe/i.test(OP.media.image_with_question) && /CC BY-SA/.test(OP.media.credit), "label words, picture and licence credit on the opener");

// every syringe problem: one point is the normal boiling point at 1 atm (or 760 torr), the other temperature is cooler
SYR.forEach(V => {
  const g = V.givens, P = g.P1 || g.P2, T1 = g.T1, T2 = g.T2;
  const known1atm = (P.unit === "atm" && Math.abs(P.value - 1) < 1e-9) || (P.unit === "torr" && Math.abs(P.value - 760) < 0.5);
  ok(known1atm, V.variant_id + ": the known pressure is one atmosphere: " + P.value + " " + P.unit);
  const k = n => n.unit === "degC" ? n.value + 273.15 : n.value;
  const Tknown = V.kind === "P2" ? k(T1) : k(T2), Tother = V.kind === "P2" ? k(T2) : k(T1);
  ok(Tother < Tknown, V.variant_id + ": the other temperature is below the boiling point");
  const d = V.board.find(b => b.id === "direction_predicted"); ok(d && d.right[0] === "direction:lower" && d.explicit && d.pin, V.variant_id + ": prediction item present, answer 'lower', explicit, pinned");
});

// the scenario's own words replace the archetype's for the three overridden items, and only those
{ const V = SYR[0];
  const mv = (st) => require("./stepmap.gs").moveFor(ARCH, V, st);
  ok(/pressure gauge inside the syringe/.test(mv("account_given").switch_ask), "account_given switch question is the scenario's");
  ok(/inverse function removes it/.test(mv("value_found").ask) && /prediction pinned/.test(mv("value_found").switch_ask), "value_found ask and switch question are the scenario's");
  ok(/inside the syringe/.test(mv("meaning_given").ask) && mv("meaning_given").notebook_prompt === ARCH.moves.meaning_given.notebook_prompt && !/syringe/.test(mv("meaning_given").notebook_prompt), "meaning_given: ask overridden, notebook prompt shared");
  ok(mv("rearranged").ask === ARCH.moves.rearranged.ask, "rearranged is the shared archetype row");
  const V2 = ARCH.variants.find(v => v.opener_index !== oi && v.kind === "P2");
  ok(!/syringe/.test(require("./stepmap.gs").moveFor(ARCH, V2, "value_found").ask), "another scenario's P2 problem does not get the syringe words");
  const tn = require("./stepmap.gs").trapNote;
  ok(/Think about the syringe/.test(tn(ARCH, V, "SIGN_FLIPPED").ask) && !/syringe/.test(tn(ARCH, V2, "SIGN_FLIPPED").ask), "SIGN_FLIPPED's question is the scenario's here and generic elsewhere"); }

// a student through a syringe problem: prediction, relation, rearrangement, wrong-side answer named, ratio-as-answer named, right answer, meaning, reflection
{ const V = SYR.find(v => v.traps.some(t => t.id === "RATIO_NOT_SCALED")) || SYR[0]; const i = ARCH.variants.indexOf(V), S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: oi, stamp: "s1" });
  let r = say(S, "The water is more volatile under vacuum."); ok(S.board.account_given !== "ticked" && /OPENER_LABEL_ONLY/.test(r.log.guards), "a label-only account ('vacuum') is held, not counted");
  r = say(S, "Pulling the plunger lowers the pressure on the water, so molecules with enough energy can escape and form bubbles inside the liquid.");
  ok(r.problem && r.problem.media.credit, "account accepted; the picture's credit travels with the problem");
  ok(r.choices && r.choices.kind === "direction" && r.choices.options.length === 3, "the prediction buttons are offered first");
  r = say(S, "", null, { pick: "direction:higher" }); ok(S.tries.setup === 1 && S.board.direction_predicted !== "ticked", "a wrong prediction is a counted wrong try");
  r = say(S, "", null, { pick: "direction:lower" }); ok(S.board.direction_predicted === "ticked" && r.pins.some(p => p.id === "direction_predicted"), "the right prediction ticks and is pinned");
  say(S, "", null, { pick: "eq_a" }); say(S, V.eq_checks[0].park_text); ok(S.board.rearranged === "ticked", "rearranged");
  V.expected.filter(e => e.role === "intermediate" && e.state !== "substituted").forEach(e => say(S, e.value + " " + (e.unit === "degC" ? "°C" : e.unit)));
  const sub = V.expected.find(e => e.state === "substituted"); say(S, sub.label + " = " + sub.value + (sub.unit ? " " + sub.unit : ""));
  const key = V.expected.find(e => e.role === "key"), sf = V.traps.find(t => t.id === "SIGN_FLIPPED"), rt = V.traps.find(t => t.id === "RATIO_NOT_SCALED");
  r = say(S, sf.value + " " + sf.unit); ok(r.log.trap_ids === "SIGN_FLIPPED" && /syringe/i.test(r.reply), "the wrong-side answer is named with the scenario's question: " + r.reply);
  if (rt) { r = say(S, rt.value + " " + rt.unit); ok(r.log.trap_ids === "RATIO_NOT_SCALED" && r.card, "the ratio typed as the answer is named; second wrong try on the solve stage gives the notebook card"); } else pass++;
  ok(S.bailed.solve === true || S.tries.solve >= 1, "wrong tries counted on the solve stage");
  if (S.awaitingReturn || S.away) { CORE.processBack(ARCH, S, 2); say(S, "The notebook showed me that undoing the ln gives the ratio and the known pressure scales it."); }
  r = say(S, key.value + " " + key.unit); ok(S.board.value_found === "ticked" && /syringe_boiling_simulator\.html\?substance=[^&]+&T=[-\d.]+&unit=(atm|torr)&theme=\{theme\}$/.test(r.simulation_url || ""), "right answer; the simulation opens with the problem's liquid, temperature and unit: " + r.simulation_url);
  say(S, "The pressure I found is where the water starts to boil in the syringe; it says the molecules already had the energy, and I trust it as far as a constant heat of vaporization holds.");
  r = say(S, "The sign was hardest; I would tell a friend to predict the direction first."); ok(r.done && S.clean, "meaning and reflection close the problem; clean (credit-eligibility is the Independent rung's, 13 Oct)"); }
console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
