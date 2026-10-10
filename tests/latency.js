// Latency of Phase A (the deterministic verdict) and of Phase B without a model, over a scripted run of every Clausius variant.
// Prints p50 / p95 / max in milliseconds. The model's own time is measured on the server (say_ms, model_ms in the log).
const CORE = require("../gas/Core.gs"); const ARCH = require("../gas/Archetype_ch10_cc.gs")["ch10_cc"];
const tA = [], tB = [];
ARCH.variants.forEach((V, i) => {
  const S = CORE.newSession(ARCH, { variantIndex: i, openerIndex: V.opener_index, stamp: "lat" });
  const steps = ["More molecules have enough energy to escape the liquid surface as it warms.", { pick: "eq_a" }];
  V.eq_checks.forEach(k => steps.push(k.park_text));
  V.expected.filter(e => e.role === "intermediate" || e.role === "key").forEach(e => steps.push(e.value + " " + e.unit));
  steps.push("The number says the attractions are moderate; the measurements support the picture only roughly.");
  steps.forEach(step => {
    const input = typeof step === "string" ? { message: step, now: 1 } : Object.assign({ message: "", now: 1 }, step);
    let t = process.hrtime.bigint(); const a = CORE.verdict(ARCH, S, input); tA.push(Number(process.hrtime.bigint() - t) / 1e6);
    if (a.needs_say) { t = process.hrtime.bigint(); CORE.say(ARCH, S, input, null); tB.push(Number(process.hrtime.bigint() - t) / 1e6); }
  });
});
const q = (arr, p) => { const s = [...arr].sort((a, b) => a - b); return s[Math.min(s.length - 1, Math.floor(p * s.length))].toFixed(2); };
console.log(`Phase A verdict: n=${tA.length}  p50 ${q(tA, .5)} ms  p95 ${q(tA, .95)} ms  max ${q(tA, 1)} ms`);
console.log(`Phase B (no model): n=${tB.length}  p50 ${q(tB, .5)} ms  p95 ${q(tB, .95)} ms  max ${q(tB, 1)} ms`);
