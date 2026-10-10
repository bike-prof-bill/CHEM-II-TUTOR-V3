// Phase A is a pure function of the message and the session: the same input on two identical sessions gives identical results and
// identical sessions afterwards. This is what makes logged turns replayable.
const CORE = require("../../gas/Core.gs"); const ARCH = require("../../gas/Archetype_ch10_cc.gs")["ch10_cc"];
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const clone = o => JSON.parse(JSON.stringify(o));
const V = ARCH.variants.find(v => v.kind === "dH"), i = ARCH.variants.indexOf(V);
const script = ["More molecules have enough energy to escape the liquid surface as it warms.", { pick: "eq_a" }, V.eq_checks[0].park_text, "T1 = 300 K and T2 = 350 K", "I get 123456", "what do you mean", "9999 torr"];
const S1 = CORE.newSession(ARCH, { variantIndex: i, openerIndex: 0, stamp: "r" }), S2 = clone(S1);
let same = true;
script.forEach(step => {
  const input = typeof step === "string" ? { message: step, now: 7 } : Object.assign({ message: "", now: 7 }, step);
  const a1 = CORE.verdict(ARCH, S1, clone(input)), a2 = CORE.verdict(ARCH, S2, clone(input));
  const strip = r => { const c = clone(r); delete c.log; if (c.log) delete c.log.verdict_ms; return c; };
  if (JSON.stringify(strip(a1)) !== JSON.stringify(strip(a2))) same = false;
  const s1 = clone(S1), s2 = clone(S2); if (s1.pending) s1.pending.p.verdict_ms = 0; if (s2.pending) s2.pending.p.verdict_ms = 0;
  if (JSON.stringify(s1) !== JSON.stringify(s2)) same = false;
  CORE.say(ARCH, S1, input, null); CORE.say(ARCH, S2, input, null);
});
ok(same, "verdict is deterministic across identical sessions and inputs");
ok(JSON.stringify(S1.board) === JSON.stringify(S2.board), "sessions end identical");
console.log(`replay: ${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
