// node gas/test_vent.js -- The Deep-Sea Vent (SCENARIO_CLAUDE, approved 10 Oct): the first unknown-temperature scenario.
// Depth as the given, the pressure at the vent as a declared step, the prediction on a temperature problem, the reciprocal error.
const CORE = require("./Core.gs"); const ARCH = require("./Archetype_ch10_cc.gs")["ch10_cc"]; const SM = require("./stepmap.gs");
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const say = (S, m, model, extra) => CORE.processTurn(ARCH, S, Object.assign({ message: m, now: 1 }, extra || {}), model || null);
const oi = ARCH.openers.findIndex(o => o.title === "The Deep-Sea Vent"); const OP = ARCH.openers[oi]; const VENT = ARCH.variants.filter(v => v.opener_index === oi);
ok(oi > -1 && VENT.length === 6 && VENT.every(v => v.kind === "T1" || v.kind === "T2"), "the scenario exists with six temperature problems");
ok(/\.mp4$/.test(OP.media.image_with_question) && /NOAA/.test(OP.media.credit), "video with the NOAA credit");
VENT.forEach(V => {
  ok(/^A hydrothermal vent sits on the sea floor, \d+ m below the surface\./.test(V.text) && /100\.0 °C/.test(V.text) && !/ atm from the vent| atm at the vent/.test(V.text), V.variant_id + ": depth is the given; the vent pressure is not printed");
  const ids = V.board.map(b => b.id); ok(ids.indexOf("P_from_depth") > -1 && ids.indexOf("P_from_depth") < ids.indexOf("substituted") && !ids.includes("P_same_units"), V.variant_id + ": P_from_depth before substitution; no unit-matching item");
  const d = V.board.find(b => b.id === "direction_predicted"); ok(d && d.right[0] === "direction:higher" && /temperature/.test(d.options[0].text), V.variant_id + ": the prediction is 'higher', in temperature words");
  ok(V.traps.some(t => t.id === "RECIPROCAL_NOT_TAKEN"), V.variant_id + ": reciprocal error declared");
});
const mv = st => SM.moveFor(ARCH, VENT[0], st);
ok(/pressure gauge at the vent/.test(mv("account_given").switch_ask) && /1\/T, what is one more step/.test(mv("value_found").ask) && /Use the depth/.test(mv("P_from_depth").ask), "the scenario's words: account switch, the temperature value_found default, P_from_depth");
ok(/Before any math, compare the two pressures/.test(mv("direction_predicted").ask), "the temperature wording of the prediction (archetype default for temperature problems)");
const P2 = ARCH.variants.find(v => v.kind === "P2"); ok(/compare the two temperatures/.test(SM.moveFor(ARCH, P2, "direction_predicted").ask), "pressure problems keep the pressure wording");
ok(/Does your answer make sense\? More water presses down/.test(SM.trapNote(ARCH, VENT[0], "SIGN_FLIPPED").ask), "SIGN_FLIPPED carries the vent's own question here");

// a student through a vent problem
{ const V = VENT.find(v => v.givens.dH.unit === "kJ/mol") || VENT[0]; const i = ARCH.variants.indexOf(V), S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: oi, stamp: "v1" });
  let r = say(S, "The water is superheated past its boiling point."); ok(/OPENER_LABEL_ONLY/.test(r.log.guards), "a label-only account (superheated, boiling point) is held");
  r = say(S, "The weight of the water above squeezes the molecules together, so a bubble cannot push back until the water is much hotter and its vapor pressure is far higher.");
  ok(r.problem, "account accepted");
  r = say(S, "", null, { pick: "direction:lower" }); ok(S.tries.setup === 1, "a wrong prediction counts");
  r = say(S, "", null, { pick: "direction:higher" }); ok(S.board.direction_predicted === "ticked", "higher: right");
  say(S, "", null, { pick: "eq_a" }); r = say(S, V.eq_checks[0].park_text); ok(S.board.rearranged === "ticked", "rearranged for the temperature");
  const depth = V.givens.depth.value; r = say(S, (depth / 10) + " atm");
  if (depth >= 500) ok(S.board.P_from_depth === "ticked", "leaving out the air's 1 atm at " + depth + " m falls inside the 2 % window: accepted, not caught (by design)");
  else ok(S.board.P_from_depth !== "ticked" && r.log.counted_fail, "leaving out the air's 1 atm at " + depth + " m is a stray, counted");
  if (S.board.P_from_depth !== "ticked") { r = say(S, (1 + depth / 10) + " atm"); }
  ok(S.board.P_from_depth === "ticked" && r.pins.some(p => p.id === "P_from_depth"), "the pressure at the vent, 1 atm + depth/10, is accepted and pinned");
  say(S, "373.15 K"); if (V.givens.dH.unit === "kJ/mol") say(S, (V.givens.dH.value * 1000) + " J/mol");
  const inv = V.expected.find(e => e.state === "substituted" && /^1\/T/.test(e.label)); r = say(S, inv.label + " = " + inv.value + " 1/K"); ok(S.board.substituted === "ticked", "1/T of the unknown establishes substitution");
  const key = V.expected.find(e => e.role === "key"), rt = V.traps.find(t => t.id === "RECIPROCAL_NOT_TAKEN");
  r = say(S, rt.value + " " + rt.unit); ok(r.log.trap_ids === "RECIPROCAL_NOT_TAKEN" && /one more step/.test(r.reply), "1/T typed as the temperature is named");
  r = say(S, key.value + " " + (key.unit === "degC" ? "°C" : key.unit)); ok(S.board.value_found === "ticked", "the boiling temperature at depth accepted");
  ok(new RegExp("deep_sea_vent_simulator\\.html\\?depth=" + depth + "&unit=(C|K)&theme=\\{theme\\}$").test(r.simulation_url || ""), "the simulation opens at the problem's depth and unit: " + r.simulation_url);
  ok(V.sim_params.T === String((key.unit === "degC" ? key.value : key.value - 273.15).toFixed(1)) && V.sim_params.T_known === "100.0", "sim_params: T is the vent temperature, T_known the boiling point at 1 atm");
  say(S, "At that depth the water must be far hotter before its vapor pressure can open a bubble, and the rule of thumb for pressure makes the number rough.");
  r = say(S, "Remembering the minus sign in front of 1/T was hardest."); ok(r.done && S.clean, "meaning and reflection close the problem; clean (credit-eligibility is the Independent rung's, 13 Oct)"); }
console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
