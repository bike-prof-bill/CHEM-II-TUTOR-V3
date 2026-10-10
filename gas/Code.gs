// Code.gs  --  V3 tutor, Google wiring only. All tutoring logic is in Core.gs and its modules (parse, match, stepmap, ladder,
// guards, prompt, log); all content is in Archetype_*.gs; units in Units.gs.
// ONE-TIME SET-UP: paste every file from the gas/ folder into a NEW Apps Script project, run setupV3() once, read the log it
// prints, add GEMINI_API_KEY under Project Settings > Script properties, then Deploy > Web app (execute as me, anyone).

var BUILD_STAMP    = "V3-0.1-20260919-01";        // project-version-date-sequence. Change on every deploy.
var PRIMARY_MODEL  = "gemini-3.6-flash";          // as V2
var FALLBACK_MODEL = "gemini-3.5-flash";

var LOG_HEADERS = ["ts", "build_stamp", "content_version", "event_type", "session_id", "student_id", "attempt_id", "archetype_id",
  "variant_id", "problem_kind", "state", "register", "face", "gate", "entering_done", "leaving_done", "newly", "tries_on_state",
  "counted_fail", "after_bailout", "seconds_away", "trap_ids", "structured", "model_accept", "second_reader", "guards",
  "fallback_used", "turn_kind", "clean", "done", "credit", "student_text", "reply_text", "model_name", "model_ms", "server_ms", "verdict_ms", "say_ms", "queued", "queue_ms"];
var MASTERY_HEADERS = ["ts", "student_id", "archetype_id", "variant_id", "problem_kind", "attempt_id", "turns", "clean", "credit", "outcome", "build_stamp", "content_version", "queued", "queue_ms"];

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

function doGet() { return json_({ alive: true, build: BUILD_STAMP, archetypes: Object.keys(ARCHETYPES).map(function (k) { return { id: k, title: ARCHETYPES[k].title, kinds: ARCHETYPES[k].kinds, content_version: ARCHETYPES[k].content_version, openers: ARCHETYPES[k].openers.map(function (o) { return o.title; }) }; }) }); }

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
      var pick = CORE.chooseVariant(arch.variants, { kind: req.kind, opener: req.opener }, served);        // never the same problem twice while others remain (step 6a/6b)
      if (!pick) return json_({ error: "no problem matches that opener and kind" });
      if (!isGuest) { if (pick.reset) served = []; served.push(pick.variant_id); props.setProperty(histKey, JSON.stringify(served.slice(-500))); }
      if (pick.reset) log_(props, { event_type: "HISTORY_RESET", archetype_id: arch.archetype_id, content_version: arch.content_version, structured: "all " + served.length + " matching problems served; list reset" }, sid, student, "", "", meta, 0);
      S = CORE.newSession(arch, { variantIndex: pick.index,
        openerIndex: Math.floor(Math.random() * arch.openers.length), stamp: Date.now().toString(36) + Math.floor(Math.random() * 1296).toString(36) });
      res = { reply: arch.openers[S.openerIndex].question, progress: CORE.progress(S, arch.variants[S.variantIndex]), notebook_url: arch.notebook_url, title: arch.title, media: CORE.openerMedia(arch, S),
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
  append_(props, "Log", LOG_HEADERS.map(function (h) { return row[h] === undefined ? "" : row[h]; }));
}
function mastery_(props, student, arch, S, outcome) {
  append_(props, "Mastery", [new Date(), student, S.archetypeId, S.variantId, arch.variants[S.variantIndex].kind, S.attemptId, S.turns, S.clean, S.credit, outcome, BUILD_STAMP, arch.content_version]);
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
function flushLog() { var props = PropertiesService.getScriptProperties(); var r = logqFlush(services_(props)); Logger.log("flushed " + r.flushed + " pending row(s)" + (r.locked ? " (lock busy; try again)" : "") + "; still pending: " + logqPendingCount(services_(props))); }
function json_(o) { return text_(JSON.stringify(o)); }
function text_(s) { return ContentService.createTextOutput(s).setMimeType(ContentService.MimeType.JSON); }
