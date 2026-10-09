// Random-clicker persona (rebuild spec, definition of done): picks at random, types filler, random numbers, random
// "equations". 200 runs per archetype. It must never earn credit and never pass the credit gate while the attempt is
// still clean. Parks (by design) can carry a stuck student to the final item without credit; that path is counted here.
const CORE = require("../../gas/Core.gs");
const ARCHS = [require("../../gas/Archetype_ch10_cc.gs")["ch10_cc"], require("../../gas/Archetype_ch13_ice.gs")["ch13_ice"]];
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
function rng(seed) { let s = seed >>> 0; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; }
const FILLER = ["the", "thing", "is", "maybe", "later", "okay", "sure", "yes", "no", "fine", "done", "next", "please", "um", "so", "then", "right", "hmm", "what", "this"];
const UNITS = ["", " K", " °C", " atm", " torr", " kPa", " kJ/mol", " J/mol", " M", " mol", " L"];
const SYMS = ["x", "K", "T1", "T2", "P1", "P2", "ΔHvap", "R"];
ARCHS.forEach(ARCH => {
  const options = [].concat(ARCH.equation_picks.map(e => e.id), ...ARCH.variants[0].board.map(b => (b.options || []).map(o => o.id)));
  let credits = 0, cleanPasses = 0, reachedGate = 0, runs = 200, totalTurns = 0, cards = 0, parks = 0;
  for (let run = 0; run < runs; run++) {
    const R = rng(run * 7919 + 17), vi = Math.floor(R() * ARCH.variants.length), V = ARCH.variants[vi];
    const S = CORE.newSession(ARCH, { variantIndex: vi, openerIndex: Math.floor(R() * ARCH.openers.length), stamp: "rc" + run });
    const gate = V.board.find(b => b.credit_gate).id;
    for (let t = 0; t < 60 && !S.done; t++) {
      totalTurns++;
      if (CORE.activeState(S, V) === gate && S.clean) reachedGate++;
      let r;
      if (S.awaitingReturn) { r = CORE.processTurn(ARCH, S, { message: FILLER.slice(0, 3 + Math.floor(R() * 4)).join(" "), now: t }, null); }
      else {
        const roll = R();
        if (roll < 0.25) r = CORE.processTurn(ARCH, S, { message: "", pick: options[Math.floor(R() * options.length)], now: t }, null);
        else if (roll < 0.5) r = CORE.processTurn(ARCH, S, { message: Array.from({ length: 2 + Math.floor(R() * 6) }, () => FILLER[Math.floor(R() * FILLER.length)]).join(" "), now: t }, null);
        else if (roll < 0.8) r = CORE.processTurn(ARCH, S, { message: (Math.pow(10, R() * 7 - 3)).toPrecision(3) + UNITS[Math.floor(R() * UNITS.length)], now: t }, null);
        else r = CORE.processTurn(ARCH, S, { message: SYMS[Math.floor(R() * SYMS.length)] + " = " + SYMS[Math.floor(R() * SYMS.length)] + (R() < 0.5 ? " / " : " * ") + SYMS[Math.floor(R() * SYMS.length)], now: t }, null);
      }
      if (r.card) { cards++; CORE.processBack(ARCH, S, t + 1); }
      if (r.log.event_type === "PARK") parks++;
      if (S.board[gate] === "ticked" && S.clean) cleanPasses++;
      if (r.credit) credits++;
    }
  }
  ok(credits === 0, ARCH.archetype_id + ": a random clicker never earns credit (" + credits + ")");
  ok(cleanPasses === 0, ARCH.archetype_id + ": a random clicker never passes the credit gate on a clean attempt (" + cleanPasses + ")");
  ok(reachedGate === 0, ARCH.archetype_id + ": a random clicker never even reaches the credit gate while the attempt is clean (" + reachedGate + ")");
  console.log(`  ${ARCH.archetype_id}: ${runs} runs, ${totalTurns} turns, ${cards} notebook cards, ${parks} parks, credits ${credits}`);
});
console.log(`random_clicker: ${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
