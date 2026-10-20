// logqueue.gs — the log never loses a row (proposed step 6a). Pure logic with injected services so it can be tested in Node;
// Code.gs supplies the real LockService, PropertiesService and the Sheet.
//
// services = { tryLock(ms) -> bool, releaseLock(), append(sheetName, values), getKeys() -> [key], get(key) -> string|null,
//              set(key, value), remove(key), now() -> ms }
// A row that cannot get the lock within WAIT_MS is stored under a PENDING_PREFIX key and written, in arrival order, by the next
// call that does get the lock. Every row carries two extra columns at the end: queued (0/1) and queue_ms (how long it waited),
// so the analysis side can count delays. Nothing is ever dropped silently.
var LOGQ_WAIT_MS = 3000, LOGQ_PENDING_PREFIX = "v3_pending_";

function logqAppend(services, sheetName, values) {
  var t = services.now();
  if (!services.tryLock(LOGQ_WAIT_MS)) {                                 // busy: keep the row, write it later
    services.set(LOGQ_PENDING_PREFIX + String(t) + "_" + Math.random().toString(36).slice(2, 8), JSON.stringify({ sheet: sheetName, values: values, t: t }));
    return { written: false, queued: true };
  }
  try {
    var flushed = logqFlushLocked(services);
    services.append(sheetName, values.concat([0, 0]));
    return { written: true, queued: false, flushed: flushed };
  } finally { services.releaseLock(); }
}
// writes every pending row (oldest first); call only while holding the lock
function logqFlushLocked(services) {
  var keys = services.getKeys().filter(function (k) { return k.indexOf(LOGQ_PENDING_PREFIX) === 0; }).sort(), n = 0;
  keys.forEach(function (k) {
    var raw = services.get(k); if (!raw) { services.remove(k); return; }
    try { var row = JSON.parse(raw); services.append(row.sheet, row.values.concat([1, services.now() - row.t])); n++; } catch (e) { /* unreadable: leave it for a human */ return; }
    services.remove(k);
  });
  return n;
}
// for a manual or scheduled flush when no request has come in
function logqFlush(services) {
  if (!services.tryLock(LOGQ_WAIT_MS)) return { flushed: 0, locked: true };
  try { return { flushed: logqFlushLocked(services), locked: false }; } finally { services.releaseLock(); }
}
function logqPendingCount(services) { return services.getKeys().filter(function (k) { return k.indexOf(LOGQ_PENDING_PREFIX) === 0; }).length; }

if (typeof module !== "undefined") module.exports = { LOGQ_WAIT_MS: LOGQ_WAIT_MS, LOGQ_PENDING_PREFIX: LOGQ_PENDING_PREFIX, logqAppend: logqAppend, logqFlushLocked: logqFlushLocked, logqFlush: logqFlush, logqPendingCount: logqPendingCount };
