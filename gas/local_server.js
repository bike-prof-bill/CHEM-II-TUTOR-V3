// node gas/local_server.js   -> a stand-in for Apps Script on http://localhost:8787/exec  (token: local)
// Same Core.gs, same archetype file, no Google, no model (plain mode). Log rows print to the terminal.
const http = require("http"), fs = require("fs"), path = require("path"), CORE = require("./Core.gs");
const ARCHETYPES = {};                                       // every generated gas/Archetype_*.gs file, found by name
fs.readdirSync(__dirname).filter(f => /^Archetype_.*\.gs$/.test(f)).forEach(f => Object.assign(ARCHETYPES, require(path.join(__dirname, f))));
const sessions = {}, turns = {};
http.createServer((req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*"); res.setHeader("Access-Control-Allow-Headers", "*"); res.setHeader("Content-Type", "application/json");
  if (req.method === "OPTIONS") return res.end();
  if (req.method === "GET") return res.end(JSON.stringify({ alive: true, build: "LOCAL-plain-mode", archetypes: Object.keys(ARCHETYPES).map(k => ({ id: k, title: ARCHETYPES[k].title, kinds: ARCHETYPES[k].kinds, content_version: ARCHETYPES[k].content_version, openers: ARCHETYPES[k].openers.map(o => o.title) })) }));
  let body = ""; req.on("data", c => body += c); req.on("end", () => {
    let out; try {
      const q = JSON.parse(body), arch = ARCHETYPES[q.archetypeId] || ARCHETYPES[Object.keys(ARCHETYPES)[0]];
      if (q.authToken !== "local") out = { error: "unauthorized (token is: local)" };
      else if (q.turnId && turns[q.turnId]) out = turns[q.turnId];
      else {
        let S = sessions[q.sessionId], r;
        if (q.action === "start" || q.action === "reset") {
          const pool = arch.variants.map((v, i) => i).filter(i => (!q.kind || arch.variants[i].kind === q.kind) && (q.opener === undefined || q.opener === "" || arch.variants[i].opener_index === Number(q.opener)));
          if (!pool.length) return res.end(JSON.stringify({ error: "no problem matches that opener and kind" }));
          S = sessions[q.sessionId] = CORE.newSession(arch, { variantIndex: pool[Math.floor(Math.random() * pool.length)], openerIndex: Math.floor(Math.random() * arch.openers.length), stamp: Date.now().toString(36) });
          r = { reply: arch.openers[S.openerIndex].question, progress: CORE.progress(S, arch.variants[S.variantIndex]), notebook_url: arch.notebook_url, title: arch.title, media: CORE.openerMedia(arch, S), log: { event_type: "PROBLEM_OPEN", variant_id: S.variantId } };
        } else if (!S) r = { error: "no session; press New problem", log: {} };
        else if (q.action === "back") r = CORE.processBack(arch, S, Date.now());
        else r = CORE.processTurn(arch, S, { message: q.message || "", pick: q.pick || null, table: q.table || null, history: q.history || [], now: Date.now() }, null);
        (q.simEvents || []).forEach(e => console.log("SIM", JSON.stringify(e)));
        const L = r.log || {}; console.log([L.event_type, L.variant_id, L.state, L.stage, L.face, L.gate, "newly=" + (L.newly || ""), "fail=" + L.counted_fail, "traps=" + (L.trap_ids || ""), "guards=" + (L.guards || "")].join(" | "));
        delete r.log; out = r; if (q.turnId) turns[q.turnId] = out;
      }
    } catch (e) { out = { error: String(e) }; }
    res.end(JSON.stringify(out));
  });
}).listen(8787, () => console.log("V3 local stand-in: URL http://localhost:8787/exec   token: local"));
