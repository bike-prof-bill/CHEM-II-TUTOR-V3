// Regression (step 6a): if the sheet lock was not free within 3 seconds, the row was thrown away silently and the analysis side
// never knew. Now the row is kept and written by the next call that gets the lock, marked queued with its wait in ms.
const CORE = require("../../gas/Core.gs"); const Q = require("../../gas/logqueue.gs");
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
function fakeServices(lockPlan) {     // lockPlan: array of booleans, what tryLock returns on successive calls
  const sheet = [], props = {}; let t = 1000, calls = 0;
  return { sheet, props, tryLock: () => lockPlan[Math.min(calls++, lockPlan.length - 1)], releaseLock: () => {}, append: (s, v) => sheet.push([s].concat(v)),
           getKeys: () => Object.keys(props), get: k => props[k], set: (k, v) => { props[k] = v; }, remove: k => { delete props[k]; }, now: () => (t += 500) };
}
// 1. a burst where the lock is busy for the first three rows, then free: all four rows land, in arrival order, three marked queued
{ const sv = fakeServices([false, false, false, true]);
  ["r1", "r2", "r3", "r4"].forEach(r => Q.logqAppend(sv, "Log", [r]));
  const rows = sv.sheet.map(x => x[1]);
  ok(rows.join() === "r1,r2,r3,r4", "every row written, oldest first: " + rows.join());
  ok(sv.sheet.slice(0, 3).every(x => x[2] === 1 && x[3] > 0) && sv.sheet[3][2] === 0, "the three delayed rows are marked queued with their wait; the fourth is not");
  ok(Q.logqPendingCount(sv) === 0, "nothing left pending"); }
// 2. the lock is never free during the burst: nothing is lost; a later manual flush writes it all
{ const sv = fakeServices([false]);
  ["a", "b"].forEach(r => Q.logqAppend(sv, "Log", [r])); ok(sv.sheet.length === 0 && Q.logqPendingCount(sv) === 2, "busy throughout: rows held, none dropped");
  sv.tryLock = () => true; const r = Q.logqFlush(sv); ok(r.flushed === 2 && sv.sheet.map(x => x[1]).join() === "a,b" && Q.logqPendingCount(sv) === 0, "manual flush writes them in order"); }
// 3. two sheets interleaved keep their sheet names
{ const sv = fakeServices([false, true]); Q.logqAppend(sv, "Mastery", ["m"]); Q.logqAppend(sv, "Log", ["l"]);
  ok(sv.sheet.map(x => x[0]).join() === "Mastery,Log", "pending rows go to their own sheets"); }
console.log(`log_row_never_dropped: ${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
