// Regression (rebuild spec, Change 1): the wrong-try ladder counted per item when per stage was decided, so two fails
// on different items of one stage produced two notebook cards (one per item). Now tries are keyed by stage.
const CORE = require("../../gas/Core.gs"); const ARCH = require("../../gas/Archetype_ch10_cc.gs")["ch10_cc"];
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const say = (S, m, extra) => CORE.processTurn(ARCH, S, Object.assign({ message: m, now: Date.now() }, extra || {}), null);
const fmtU = u => u === "degC" ? "°C" : u;

// a problem whose units stage has two items: a temperature to convert and a ΔHvap to convert
const i = ARCH.variants.findIndex(v => v.board.some(b => b.id === "T_in_K") && v.board.some(b => b.id === "dH_in_J") && v.kind !== "slope");
const V = ARCH.variants[i], S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "stage" });
ok(V.board.find(b => b.id === "T_in_K").stage === V.board.find(b => b.id === "dH_in_J").stage, "both conversions belong to one stage: " + V.board.find(b => b.id === "T_in_K").stage);
say(S, "A larger fraction of the molecules has enough kinetic energy to escape the liquid surface.");
say(S, "", { pick: "eq_a" }); say(S, V.eq_checks[0].park_text);
ok(CORE.activeState(S, V) === "T_in_K", "setup done; the first units item is active");
let r = say(S, "I get 123456"); ok(r.log.counted_fail && r.log.state === "T_in_K" && !r.card, "first stray, attributed to T_in_K: no card yet");
const tK = V.expected.find(e => e.state === "T_in_K"); r = say(S, tK.value.toFixed(1) + " K"); ok(S.board.T_in_K === "ticked" && !r.log.counted_fail, "T in K established");
ok(CORE.activeState(S, V) === "dH_in_J", "the active item is now the other item of the same stage");
r = say(S, "then 98765"); ok(r.log.state === "dH_in_J" && r.card && r.log.event_type === "BAILOUT_ISSUED", "second stray, on a DIFFERENT item of the same stage: ONE notebook card");
ok(S.bailed.units === true && S.tries.units === 0 && Object.keys(S.bailed).length === 1, "the stage, not the item, is marked bailed; counts reset once");
CORE.processBack(ARCH, S, Date.now() + 1000); say(S, "It showed that both conversions are about putting every quantity in the units the relation expects.");
r = say(S, "55555"); ok(!r.card && r.log.counted_fail && S.tries.units === 1, "after the return, a fail on the stage counts toward parking, not a second card");
r = say(S, "44444"); ok(r.log.event_type === "PARK" && S.board.dH_in_J === "parked" && !r.card, "the second fail parks the stage; no second card ever");
console.log(`one_stage_one_notebook_card: ${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
