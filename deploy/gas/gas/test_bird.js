// node gas/test_bird.js -- The Drinking Bird (SCENARIO_CLAUDE, approved 10 Oct): a drawn known temperature, a cooler head,
// the pressure difference graded against the student's own head pressure, the water-ΔHvap error, a video with credit.
const CORE = require("./Core.gs"); const ARCH = require("./Archetype_ch10_cc.gs")["ch10_cc"]; const SM = require("./stepmap.gs");
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const say = (S, m, model, extra) => CORE.processTurn(ARCH, S, Object.assign({ message: m, now: 1 }, extra || {}), model || null);
const oi = ARCH.openers.findIndex(o => o.title === "The Drinking Bird"); const OP = ARCH.openers[oi]; const BIRD = ARCH.variants.filter(v => v.opener_index === oi);
ok(oi > -1 && BIRD.length === 6, "the scenario exists with six pressure problems");
ok(/\.mp4$/.test(OP.media.image_with_question) && /CC BY 4\.0/.test(OP.media.credit) && /adapted/.test(OP.media.credit), "video in the picture column with licence credit and the adaptation note");
BIRD.forEach(V => {
  const g = V.givens, kT = V.kind === "P2" ? "T1" : "T2", uT = V.kind === "P2" ? "T2" : "T1", c = n => n.unit === "degC" ? n.value : n.value - 273.15;
  ok(c(g[kT]) >= 19.9 && c(g[kT]) <= 28.1, V.variant_id + ": body temperature within 20 to 28 °C: " + c(g[kT]).toFixed(1));
  const gap = c(g[kT]) - c(g[uT]); ok(gap >= 1.9 && gap <= 6.1, V.variant_id + ": head 2 to 6 °C cooler: " + gap.toFixed(1));
  ok(/^A drinking bird has (an? [a-z]+) sealed inside its glass\./.test(V.text) && /How much higher is the pressure in the body\?/.test(V.text), V.variant_id + ": the scenario's sentence");
  const ids = V.board.map(b => b.id); ok(ids.indexOf("dP_found") === ids.indexOf("value_found") + 1 && V.board.find(b => b.id === "meaning_given").requires[0] === "dP_found", V.variant_id + ": dP_found sits between the answer and the meaning");
  const d = V.expected.find(e => e.state === "dP_found"); ok(d && d.derive && d.derive.from === "key_value_found" && d.require_unit, V.variant_id + ": the difference is graded against the student's own head pressure");
});
ok(BIRD.some(V => V.traps.some(t => t.id === "WATER_DH_USED")), "the water-ΔHvap error is declared on bird problems");
ok(!ARCH.variants.some(V => V.opener_index !== oi && V.traps.some(t => t.id === "WATER_DH_USED")), "and on no other scenario's problems");
ok(/Think about the bird/.test(SM.trapNote(ARCH, BIRD[0], "SIGN_FLIPPED").ask) && /straw/.test(SM.moveFor(ARCH, BIRD[0], "meaning_given").ask) && /two ends of the bird/.test(SM.moveFor(ARCH, BIRD[0], "dP_found").ask), "the scenario's own words on its items");

// a student: head pressure slightly off but within the window, then the difference computed from THEIR head pressure is accepted
{ const V = BIRD.find(v => v.traps.some(t => t.id === "WATER_DH_USED")) || BIRD[0]; const i = ARCH.variants.indexOf(V), S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: oi, stamp: "b1" });
  let r = say(S, "The bird is a heat engine under suction."); ok(/OPENER_LABEL_ONLY/.test(r.log.guards), "label words (heat engine, suction) hold the account");
  r = say(S, "Water evaporating from the felt cools the head, so fewer molecules escape there and vapor condenses; the warmer body's higher vapor pressure pushes liquid up the neck.");
  ok(r.problem && /\.mp4$/.test(r.problem.media.image) === false || r.problem, "account accepted");
  r = say(S, "", null, { pick: "direction:lower" }); ok(S.board.direction_predicted === "ticked", "prediction: lower (the head is cooler)");
  say(S, "", null, { pick: "eq_a" }); say(S, V.eq_checks[0].park_text);
  V.expected.filter(e => e.role === "intermediate" && ["T_in_K", "dH_in_J", "P_same_units"].indexOf(e.state) > -1).forEach(e => say(S, e.value + " " + (e.unit === "degC" ? "°C" : e.unit)));
  const sub = V.expected.find(e => e.state === "substituted"); say(S, sub.label + " = " + sub.value + (sub.unit ? " " + sub.unit : ""));
  const w = V.traps.find(t => t.id === "WATER_DH_USED"); if (w) { r = say(S, w.value + " " + w.unit); ok(r.log.trap_ids === "WATER_DH_USED" && /Which liquid/.test(r.reply), "water's ΔHvap used: named with the scenario's question"); } else pass++;
  const key = V.expected.find(e => e.role === "key"), off = key.value * 1.015;          // 1.5 % high: inside the window
  r = say(S, off.toPrecision(5) + " " + key.unit); ok(S.board.value_found === "ticked", "a head pressure 1.5 % high is accepted"); const simUrl = r.simulation_url || "";
  const d = V.expected.find(e => e.state === "dP_found");
  const theirs = d.derive.base - Number(off.toPrecision(5));                              // the difference THEY would compute
  const strict = d.derive.base - key.value;
  r = say(S, theirs.toPrecision(5) + " " + d.unit); ok(S.board.dP_found === "ticked" && !r.log.counted_fail, "their own difference is accepted, though it differs from the strict one by " + (100 * Math.abs(theirs - strict) / Math.abs(strict)).toFixed(0) + " %");
  { const g = V.givens, c = n => (n.unit === "degC" ? n.value : n.value - 273.15).toFixed(1), kT = V.kind === "P2" ? "T1" : "T2", uT = V.kind === "P2" ? "T2" : "T1";
    ok(new RegExp("T=" + c(g[uT]).replace(".", "\\.") + "&T_known=" + c(g[kT]).replace(".", "\\.") + "&unit=").test(simUrl), "the simulation address carries the head temperature as T and the body temperature as T_known: " + simUrl); }
  say(S, "The warm body's vapor pushes liquid up the neck like a straw, until the head is heavy enough to tip the bird.");
  r = say(S, "The sign was hardest; predicting first helped."); ok(r.done && S.clean, "meaning and reflection close the problem; clean (credit-eligibility is the Independent rung's, 13 Oct)"); }
// the difference typed with the opposite sign is also accepted (either sign, as approved)
{ const V = BIRD[1]; const i = ARCH.variants.indexOf(V), S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: oi, stamp: "b2" });
  say(S, "Fewer molecules escape from the cooler head, so its vapor pressure is lower and the body pushes liquid up the neck."); say(S, "", null, { pick: "direction:lower" }); say(S, "", null, { pick: "eq_a" }); say(S, V.eq_checks[0].park_text);
  V.expected.filter(e => e.role === "intermediate" && ["T_in_K", "dH_in_J", "P_same_units", "substituted"].indexOf(e.state) > -1).slice(0, 4).forEach(e => say(S, e.label + " = " + e.value + (e.unit ? " " + (e.unit === "degC" ? "°C" : e.unit) : "")));
  const key = V.expected.find(e => e.role === "key"); say(S, key.value + " " + key.unit);
  const d = V.expected.find(e => e.state === "dP_found"); const r = say(S, (-(d.derive.base - key.value)).toPrecision(5) + " " + d.unit);
  ok(S.board.dP_found === "ticked", "head minus body (negative) is accepted too"); }
console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
