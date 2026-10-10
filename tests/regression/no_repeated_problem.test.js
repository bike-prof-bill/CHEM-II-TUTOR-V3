// Regression (step 6b): a student could draw the same problem twice. Now the draw skips problems already served to that
// student until none remain, then resets and says so.
const CORE = require("../../gas/Core.gs"); const ARCH = require("../../gas/Archetype_ch10_cc.gs")["ch10_cc"];
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
function rng(seed) { let s = seed >>> 0; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; }
const N = ARCH.variants.length, served = [], R = rng(3); let resets = 0;
for (let i = 0; i < N; i++) { const p = CORE.chooseVariant(ARCH.variants, {}, served, R); if (p.reset) resets++; served.push(p.variant_id); }
ok(new Set(served).size === N && resets === 0, `${N} draws by one student cover all ${N} problems with no repeat (${new Set(served).size} distinct, ${resets} resets)`);
const p = CORE.chooseVariant(ARCH.variants, {}, served, R); ok(p.reset === true && served.indexOf(p.variant_id) > -1, "draw N+1 is a repeat and is flagged as a reset");
// filters are honoured inside the history: the dH problems of one scenario, exhausted in three draws
const oi = ARCH.openers.findIndex(o => /Rubbing/.test(o.title)), s2 = []; let q;
for (let i = 0; i < 3; i++) { q = CORE.chooseVariant(ARCH.variants, { kind: "dH", opener: String(oi) }, s2, R); s2.push(q.variant_id); }
ok(new Set(s2).size === 3 && !q.reset && ARCH.variants.filter(v => v.kind === "dH" && v.opener_index === oi).length === 3, "three dH draws from the scenario are the three distinct problems");
q = CORE.chooseVariant(ARCH.variants, { kind: "dH", opener: String(oi) }, s2, R); ok(q.reset, "the fourth resets");
ok(CORE.chooseVariant(ARCH.variants, { kind: "T2", opener: String(oi) }, [], R) === null, "a kind the scenario does not draw returns null, not a wrong problem");
console.log(`no_repeated_problem: ${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
