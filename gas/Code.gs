// Code.gs  --  V3 tutor, Google wiring only. All tutoring logic is in Core.gs and its modules (parse, match, stepmap, ladder,
// guards, prompt, log); all content is in Archetype_*.gs; units in Units.gs.
// ONE-TIME SET-UP: paste every file from the gas/ folder into a NEW Apps Script project, run setupV3() once, read the log it
// prints, add GEMINI_API_KEY under Project Settings > Script properties, then Deploy > Web app (execute as me, anyone).

var BUILD_STAMP    = "V3-0.1-20260919-01";        // project-version-date-sequence. Change on every deploy.
var PRIMARY_MODEL  = "gemini-3.6-flash";          // as V2
var FALLBACK_MODEL = "gemini-3.5-flash";

var LOG_HEADERS = ["ts", "build_stamp", "content_version", "event_type", "session_id", "student_id", "attempt_id", "archetype_id", "variant_id", "problem_kind", "state", "register", "face", "gate", "entering_done", "leaving_done", "newly", "tries_on_state", "counted_fail", "after_bailout", "seconds_away", "trap_ids", "structured", "model_accept", "second_reader", "guards", "fallback_used", "turn_kind", "clean", "done", "credit", "student_text", "reply_text", "model_name", "model_ms", "server_ms", "verdict_ms", "say_ms", "stage", "tries_on_stage", "near_miss", "repeat", "second_reader_quote", "units_check", "rung", "role", "version", "extra", "demote", "queued", "queue_ms"];   // queued and queue_ms last: the log queue appends them to every row
var MASTERY_HEADERS = ["ts", "student_id", "archetype_id", "variant_id", "problem_kind", "attempt_id", "turns", "clean", "credit", "outcome", "build_stamp", "content_version", "rung", "role", "version", "extra", "queued", "queue_ms"];

function setupV3() {
  var props = PropertiesService.getScriptProperties();
  var ss = SpreadsheetApp.create("V3 Tutor Log");
  ss.getSheets()[0].setName("Log").appendRow(LOG_HEADERS);
  ss.insertSheet("Mastery").appendRow(MASTERY_HEADERS);
  var token = Utilities.getUuid().replace(/-/g, "");
  props.setProperty("SHEET_ID", ss.getId()); props.setProperty("APP_TOKEN", token);
  Logger.log("Sheet: " + ss.getUrl()); Logger.log("APP_TOKEN for index.html: " + token);
  Logger.log("Now add GEMINI_API_KEY in Script properties. Without it the tutor runs in plain mode: authored questions only.");
}

// Run this from the editor to see which Gemini models your key can use today. Names move fast.
function checkModels() {
  var key = PropertiesService.getScriptProperties().getProperty("GEMINI_API_KEY");
  var r = UrlFetchApp.fetch("https://generativelanguage.googleapis.com/v1beta/models?pageSize=200&key=" + key, { muteHttpExceptions: true });
  var names = (JSON.parse(r.getContentText()).models || []).filter(function (m) { return (m.supportedGenerationMethods || []).indexOf("generateContent") > -1; })
    .map(function (m) { return m.name.replace("models/", ""); });
  Logger.log("PRIMARY " + PRIMARY_MODEL + (names.indexOf(PRIMARY_MODEL) > -1 ? " : available" : " : NOT FOUND"));
  Logger.log("FALLBACK " + FALLBACK_MODEL + (names.indexOf(FALLBACK_MODEL) > -1 ? " : available" : " : NOT FOUND"));
  Logger.log("All usable models:\n" + names.join("\n"));
}

function doGet() { var expected = (typeof SHELL_VERSION !== "undefined") ? SHELL_VERSION : "not pasted", actual = CORE.shellFingerprint();
  // a stale paste shows as shell_ok false
  return json_({ alive: true, build: BUILD_STAMP, shell_expected: expected, shell_actual: actual, shell_ok: expected === actual, archetypes: Object.keys(ARCHETYPES).map(function (k) { return { id: k, title: ARCHETYPES[k].title, kinds: ARCHETYPES[k].kinds, content_version: ARCHETYPES[k].content_version, openers: ARCHETYPES[k].openers.map(function (o) { return o.title; }) }; }) }); }

function doPost(e) {
  var t0 = Date.now();
  try {
    var props = PropertiesService.getScriptProperties(), req = JSON.parse(e.postData.contents), cache = CacheService.getScriptCache();
    if (req.authToken !== props.getProperty("APP_TOKEN")) return json_({ error: "unauthorized" });
    if (req.turnId) { var seen = cache.get("v3turn_" + req.turnId); if (seen) return text_(seen); }    // a retry replays, never regrades
    var sid = String(req.sessionId || ""), student = req.studentId || "Guest (No Extra Credit)";
    var arch = ARCHETYPES[req.archetypeId] || ARCHETYPES[Object.keys(ARCHETYPES)[0]]; if (!arch) return json_({ error: "unknown archetype" });
    var S = sid ? JSON.parse(cache.get("v3s_" + sid) || "null") : null, res, meta = { model: "", ms: 0 };

    if (req.action === "start" || req.action === "reset") {
      if (S && !S.done && S.turns > 0) mastery_(props, student, arch, S, "abandoned");
      var isGuest = /^Guest/.test(student), histKey = "v3hist_" + arch.archetype_id + "_" + student.replace(/[^A-Za-z0-9_@.\-]/g, "_");
      var served = isGuest ? [] : JSON.parse(props.getProperty(histKey) || "[]");
      // rungs (instructor, 11-13 Oct): a student with a row in the Rungs sheet is stepped Worked -> Faded -> Independent and the
      // tutor picks the scenario by role; the offered second worked problem (req.want) rides the same path. Without a row: as before.
      var rec = isGuest ? null : rungRecord_(props, student, arch.archetype_id), filters = { kind: req.kind, opener: req.opener }, rung = "faded", extra = false;
      var rolesByOpener = {}; arch.openers.forEach(function (o, i) { rolesByOpener[i] = o.role || "floater"; });
      if (req.want && req.want.extra) { filters = { kind: req.want.kind, role: req.want.role, version: req.want.version, substance: req.want.substance, rolesByOpener: rolesByOpener }; rung = "worked"; extra = true; }
      else if (rec) { var w = CORE.nextAssignment(rec); filters = { role: w.role, version: w.version, rolesByOpener: rolesByOpener }; rung = w.rung; }
      else filters.excludeRole = "exam";                                                                  // the exam scenario is never served by chance
      var pick = CORE.chooseVariant(arch.variants, filters, served);        // never the same problem twice while others remain (step 6a/6b)
      if (!pick) return json_({ error: "no problem matches that opener and kind" });
      if (!isGuest) { if (pick.reset) served = []; served.push(pick.variant_id); props.setProperty(histKey, JSON.stringify(served.slice(-500))); }
      if (pick.reset) log_(props, { event_type: "HISTORY_RESET", archetype_id: arch.archetype_id, content_version: arch.content_version, structured: "all " + served.length + " matching problems served; list reset" }, sid, student, "", "", meta, 0);
      S = CORE.newSession(arch, { variantIndex: pick.index, rung: rung, extra: extra,
        openerIndex: Math.floor(Math.random() * arch.openers.length), stamp: Date.now().toString(36) + Math.floor(Math.random() * 1296).toString(36) });
      res = { reply: CORE.showFor(arch, arch.variants[S.variantIndex], S, "account_given") || arch.openers[S.openerIndex].question, rung: S.rung, progress: CORE.progress(S, arch.variants[S.variantIndex]), notebook_url: arch.notebook_url, title: arch.title, media: CORE.openerMedia(arch, S),
        log: { event_type: "PROBLEM_OPEN", attempt_id: S.attemptId, archetype_id: S.archetypeId, variant_id: S.variantId,
               problem_kind: arch.variants[S.variantIndex].kind, content_version: arch.content_version } };
    } else {
      if (!S) return json_({ error: "no session; press New Problem" });
      var rate = parseInt(cache.get("v3rate_" + sid) || "0", 10); if (rate >= 60) return json_({ error: "rate limit reached, please wait" });
      cache.put("v3rate_" + sid, String(rate + 1), 3600);
      var input = { message: req.message || "", pick: req.pick || null, table: req.table || null, history: (req.history || []).slice(-10), now: Date.now() };
      var model = props.getProperty("GEMINI_API_KEY") ? function (sys, hist, msg) { return gemini_(props, sys, hist, msg, meta); } : null;
      if (model) model.batch = function (reqs) { return geminiBatch_(props, reqs, meta); };          // draft + second reader in one round trip
      if (req.action === "back") res = CORE.processBack(arch, S, Date.now());
      else if (req.action === "verdict") res = CORE.verdict(arch, S, input);                          // Phase A: deterministic, returns at once
      else if (req.action === "say") res = CORE.say(arch, S, input, model);                           // Phase B: the model's sentence
      else res = CORE.processTurn(arch, S, input, model);                                             // both in one call
      (req.simEvents || []).slice(0, 20).forEach(function (ev) {
        log_(props, { event_type: "SIM", attempt_id: S.attemptId, archetype_id: S.archetypeId, variant_id: S.variantId, content_version: arch.content_version,
                      structured: JSON.stringify(ev) }, sid, student, "", "", meta, 0); });
      if (res.log && res.log.done && res.log.event_type !== "BAILOUT_RETURN" && S.done && !S.recorded) { S.recorded = true; mastery_(props, student, arch, S, "finished"); }
      if (res.log && res.log.demote && !isGuest_(student)) { var rd = rungRecord_(props, student, arch.archetype_id); if (rd) { CORE.advance(rd, { rung: S.rung, role: S.role, bailed: true, extra: S.extra }); saveRung_(props, student, arch.archetype_id, rd); } }
    }
    if (sid) cache.put("v3s_" + sid, JSON.stringify(S), 21600);
    if (res.log) { log_(props, res.log, sid, student, req.message || (req.pick ? "[pick " + req.pick + "]" : ""), res.reply, meta, Date.now() - t0); delete res.log; }   // one row per turn, written by whichever phase ends it
    var body = JSON.stringify(res);
    if (req.turnId) cache.put("v3turn_" + req.turnId, body, 600);
    return text_(body);
  } catch (err) { return json_({ error: String(err) }); }
}

function gemini_(props, system, history, message, meta) {
  var contents = (history || []).map(function (t) { return { role: t.role === "model" ? "model" : "user", parts: [{ text: t.text }] }; });
  contents.push({ role: "user", parts: [{ text: message || "(no text)" }] });
  var payload = JSON.stringify({ system_instruction: { parts: [{ text: system }] }, contents: contents, generationConfig: { response_mime_type: "application/json" } });
  var models = [PRIMARY_MODEL, FALLBACK_MODEL], t = Date.now();
  for (var i = 0; i < models.length; i++) {
    var r = UrlFetchApp.fetch("https://generativelanguage.googleapis.com/v1beta/models/" + models[i] + ":generateContent?key=" + props.getProperty("GEMINI_API_KEY"),
      { method: "post", contentType: "application/json", payload: payload, muteHttpExceptions: true });
    if (r.getResponseCode() === 200) {
      meta.model = models[i] + (i ? " (fallback)" : ""); meta.ms += Date.now() - t;
      return JSON.parse(JSON.parse(r.getContentText()).candidates[0].content.parts[0].text);
    }
  }
  meta.ms += Date.now() - t; throw new Error("model unavailable");
}

// several prompts in one round trip (UrlFetchApp.fetchAll): the draft and the second reader run in parallel
function geminiBatch_(props, reqs, meta) {
  var key = props.getProperty("GEMINI_API_KEY"), t = Date.now();
  var mk = function (r) { var contents = (r.history || []).map(function (h) { return { role: h.role === "model" ? "model" : "user", parts: [{ text: h.text }] }; });
    contents.push({ role: "user", parts: [{ text: r.msg || "(no text)" }] });
    return { url: "https://generativelanguage.googleapis.com/v1beta/models/" + PRIMARY_MODEL + ":generateContent?key=" + key, method: "post", contentType: "application/json", muteHttpExceptions: true,
             payload: JSON.stringify({ system_instruction: { parts: [{ text: r.system }] }, contents: contents, generationConfig: { response_mime_type: "application/json" } }) }; };
  var out = UrlFetchApp.fetchAll(reqs.map(mk)).map(function (resp, i) {
    if (resp.getResponseCode() === 200) { try { return JSON.parse(JSON.parse(resp.getContentText()).candidates[0].content.parts[0].text); } catch (e) { return null; } }
    try { return gemini_(props, reqs[i].system, reqs[i].history, reqs[i].msg, meta); } catch (e) { return null; }   // one failed: retry it alone with the fallback model
  });
  meta.model = meta.model || PRIMARY_MODEL; meta.ms += Date.now() - t; return out;
}

function log_(props, row, sid, student, studentText, reply, meta, serverMs) {
  row.ts = new Date(); row.build_stamp = BUILD_STAMP; row.session_id = sid; row.student_id = student; row.student_text = studentText;
  row.reply_text = reply; row.model_name = meta.model; row.model_ms = meta.ms; row.server_ms = serverMs;
  append_(props, "Log", LOG_HEADERS.slice(0, -2).map(function (h) { return row[h] === undefined ? "" : row[h]; }));   // the queue adds queued, queue_ms
}
function isGuest_(student) { return /^Guest/.test(student); }
function sheet_(props, name, headers) {            // a named sheet, created with its headers the first time it is needed
  var ss = SpreadsheetApp.openById(props.getProperty("SHEET_ID")), sh = ss.getSheetByName(name);
  if (!sh) { sh = ss.insertSheet(name); sh.appendRow(headers); }
  return sh;
}
// Rungs sheet: one row per student and archetype (student_id, archetype_id, rung assigned by the instructor); the record of progress
// lives in script properties and is written back to the sheet's "record" column so the instructor can read it.
function rungRecord_(props, student, archId) {
  var key = "v3rung_" + archId + "_" + student.replace(/[^A-Za-z0-9_@.\-]/g, "_"), saved = props.getProperty(key);
  if (saved) return JSON.parse(saved);
  var sh = sheet_(props, "Rungs", ["student_id", "archetype_id", "assigned", "record", "updated"]), rows = sh.getDataRange().getValues();
  for (var i = 1; i < rows.length; i++) if (String(rows[i][0]) === student && String(rows[i][1]) === archId) { var rec = CORE.newRecord(String(rows[i][2] || "faded").toLowerCase()); props.setProperty(key, JSON.stringify(rec)); return rec; }
  // no row: the script property DEFAULT_RUNG decides (instructor, 13 Oct). "worked" or "faded" steps every student from that rung with
  // no row needed, the sheet then holding only exceptions; unset or "none" means the student is served as before (not stepped).
  var d = String(props.getProperty("DEFAULT_RUNG") || "none").toLowerCase();
  if (d === "worked" || d === "faded") { var r0 = CORE.newRecord(d); props.setProperty(key, JSON.stringify(r0)); sh.appendRow([student, archId, d, JSON.stringify(r0), new Date()]); return r0; }
  return null;
}
function saveRung_(props, student, archId, rec) {
  var key = "v3rung_" + archId + "_" + student.replace(/[^A-Za-z0-9_@.\-]/g, "_"); props.setProperty(key, JSON.stringify(rec));
  var sh = sheet_(props, "Rungs", ["student_id", "archetype_id", "assigned", "record", "updated"]), rows = sh.getDataRange().getValues();
  for (var i = 1; i < rows.length; i++) if (String(rows[i][0]) === student && String(rows[i][1]) === archId) { sh.getRange(i + 1, 4, 1, 2).setValues([[JSON.stringify(rec), new Date()]]); return; }
}
function mastery_(props, student, arch, S, outcome) {
  if (!isGuest_(student)) { var rec = rungRecord_(props, student, S.archetypeId); if (rec) { CORE.advance(rec, { rung: S.rung, role: S.role, clean: S.clean, finished: outcome === "finished", extra: S.extra }); saveRung_(props, student, S.archetypeId, rec); } }
  append_(props, "Mastery", [new Date(), student, S.archetypeId, S.variantId, arch.variants[S.variantIndex].kind, S.attemptId, S.turns, S.clean, S.credit, outcome, BUILD_STAMP, arch.content_version, S.rung || "", S.role || "", S.version || "", !!S.extra]);
}
// The log never loses a row (step 6a): a row that cannot get the lock in 3 s is kept in script properties and written by the next
// request that does; every row carries queued (0/1) and queue_ms. Run flushLog() from the editor to write anything still pending.
function services_(props) {
  var lock = LockService.getScriptLock();
  return { tryLock: function (ms) { return lock.tryLock(ms); }, releaseLock: function () { lock.releaseLock(); },
    append: function (sheetName, values) { SpreadsheetApp.openById(props.getProperty("SHEET_ID")).getSheetByName(sheetName).appendRow(values); },
    getKeys: function () { return Object.keys(props.getProperties()); }, get: function (k) { return props.getProperty(k); },
    set: function (k, v) { props.setProperty(k, v); }, remove: function (k) { props.deleteProperty(k); }, now: function () { return Date.now(); } };
}
function append_(props, sheetName, values) { return logqAppend(services_(props), sheetName, values); }
// Run once after pasting a new version: relabel row 1 of Log and Mastery with the current column names. Columns are only ever
// appended, so existing rows keep their meaning; the new columns gain their labels.
function refreshHeaders() {
  var props = PropertiesService.getScriptProperties(), ss = SpreadsheetApp.openById(props.getProperty("SHEET_ID"));
  ss.getSheetByName("Log").getRange(1, 1, 1, LOG_HEADERS.length).setValues([LOG_HEADERS]);
  ss.getSheetByName("Mastery").getRange(1, 1, 1, MASTERY_HEADERS.length).setValues([MASTERY_HEADERS]);
  Logger.log("Headers refreshed: Log " + LOG_HEADERS.length + " columns, Mastery " + MASTERY_HEADERS.length + " columns.");
}
function flushLog() { var props = PropertiesService.getScriptProperties(); var r = logqFlush(services_(props)); Logger.log("flushed " + r.flushed + " pending row(s)" + (r.locked ? " (lock busy; try again)" : "") + "; still pending: " + logqPendingCount(services_(props))); }
function json_(o) { return text_(JSON.stringify(o)); }
function text_(s) { return ContentService.createTextOutput(s).setMimeType(ContentService.MimeType.JSON); }
