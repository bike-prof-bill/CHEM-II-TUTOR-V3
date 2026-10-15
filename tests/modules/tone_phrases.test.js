// The instructor's tone phrases (15 Oct): offered to the model only for the situation of the turn, only from approved rows,
// a phrase written for the named error first, rotating by turn, never more than three; nothing offered when no row is approved.
const CORE = require("../../gas/Core.gs");
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const P = require("../../gas/prompt.gs");
const SHIPPED = require("../../gas/Tone.gs");
ok(SHIPPED.length === 31 && !SHIPPED.some(t => t.id === "T05") && !SHIPPED.some(t => /spot-on|nailed|I love|Close!/.test(t.phrase)), "31 approved rows ship (the seven edits confirmed); the struck row does not; no flattery remains");
ok(SHIPPED.filter(t => t.probe).length >= 4, "the instructor's matrix probes ride with their phrases");
global.TONE = [
  { id: "T01", phrase: "common intuition", situation: "wrong_try", errors: [], conditional: false },
  { id: "T04", phrase: "trickiest hurdle", situation: "second_wrong_try", errors: [], conditional: false },
  { id: "T21", phrase: "two-way street", situation: "named_error", errors: ["EXCEEDS_INITIAL"], conditional: false },
  { id: "T02", phrase: "almost everyone trips", situation: "wrong_try", errors: [], conditional: false },
  { id: "T06", phrase: "picture the beaker", situation: "account_rejected", errors: [], conditional: false },
  { id: "T30", phrase: "hydration", situation: "wrong_try", errors: [], chapters: ["11"], conditional: false },
];
const f = (s, e, n, ch) => P.tonePhrasesFor({ tone_situation: s, tone_errors: e || [], turn_count: n || 0, chapter: ch || "13" }).map(t => t.id);
ok(f("wrong_try", [], 0, "11").indexOf("T30") > -1 && f("wrong_try", [], 0, "13").indexOf("T30") < 0, "a phrase mapped to chapter 11 is offered there and not in chapter 13");
ok(f("wrong_try").join() === "T01,T02", "a wrong try offers the wrong-try phrases");
ok(f("wrong_try", [], 1).join() === "T02,T01", "the order rotates with the turn");
ok(f("second_wrong_try").join() === "T04", "the second wrong try in a stage has its own phrases");
ok(f("named_error", ["EXCEEDS_INITIAL"]).join() === "T21", "a named error offers the phrase written for it");
ok(f("named_error", ["Q_INVERTED"]).join() === "T01,T02", "a named error with no phrase of its own falls back to the plain wrong-try phrases");
ok(f("account_rejected").join() === "T06" && f("right_step").length === 0 && f("").length === 0, "account rejected has its phrase; a right step with none offers none; no situation, nothing");
const sys = P.buildSystem({ openers: [{ question: "q" }], variants: [] }, { openerIndex: 0, board: {} }, { text: "t" }, { progress: { done: 0, of: 1 }, active: "x", register: "symbolic", ask: "ask", notes: ["n"], judge: false, tone_situation: "wrong_try", tone_errors: [], turn_count: 0 });
ok(/REGISTER FOR YOUR FIRST SENTENCE/.test(sys) && /common intuition/.test(sys) && /only if the server verdict above shows it true/.test(sys), "the system prompt carries the register block with the guard");
global.TONE = [];
ok(!/REGISTER FOR YOUR FIRST SENTENCE/.test(P.buildSystem({ openers: [{ question: "q" }], variants: [] }, { openerIndex: 0, board: {} }, { text: "t" }, { progress: { done: 0, of: 1 }, active: "x", register: "", ask: "", notes: [], judge: false, tone_situation: "wrong_try", tone_errors: [], turn_count: 0 })), "no block when nothing is approved");
console.log(`tone_phrases: ${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
