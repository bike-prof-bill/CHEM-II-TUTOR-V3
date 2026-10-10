// guards.gs — one module of the tutor shell (rebuild spec, step 4). Apps Script shares one global scope across files;
// in Node, Core.gs loads every module and makes its exports global, so plain function declarations work in both.
function unearned(reply, S, V) {      // a number from the answer key that the student has not produced
  var bad = [];
  parseNumbers(reply).forEach(function (n) {
    var c = match(n, V.expected, V.traps, {});
    if ((c.type === "expected" || c.type === "needs_unit" || c.type === "trap") &&
        !S.produced.some(function (p) { return near(p, n.x, 1e-6 * Math.abs(n.x) + 1e-12); })) bad.push(n.x);
  });
  return bad;
}


// Three cheap checks that moved out of the prompt (rebuild spec): run on the model's draft before the leak guard.
var BANNED_OPENERS = ["Spot on", "Exactly right", "Perfect", "Great job", "You nailed it", "Excellent work"];   // instructor's V2 list
function firstThreeWords(t) { return String(t || "").toLowerCase().replace(/[^a-z0-9\s]/g, " ").trim().split(/\s+/).slice(0, 3).join(" "); }
// -> list of failures: [] when the draft passes. `done` = the problem is complete after this turn (then zero questions is right).
function checkDraft(reply, S, V, done, lastReply) {
  var f = [], r = String(reply || "");
  var q = (r.match(/\?/g) || []).length;
  if (done ? q > 0 : q !== 1) f.push(done ? "QUESTION_AFTER_COMPLETION" : (q === 0 ? "NO_QUESTION" : "MANY_QUESTIONS"));
  if (BANNED_OPENERS.some(function (b) { return r.trim().toLowerCase().indexOf(b.toLowerCase()) === 0; })) f.push("BANNED_OPENER");
  if (lastReply && firstThreeWords(r) && firstThreeWords(r) === firstThreeWords(lastReply)) f.push("SAME_OPENING");
  if (unearned(r, S, V).length) f.push("REPLY_STATED_VALUE");
  return f;
}
function rewriteInstruction(failures, reply, S, V) {
  var parts = [];
  if (failures.indexOf("QUESTION_AFTER_COMPLETION") > -1) parts.push("The problem is complete. Your draft asked a question. Acknowledge what the student established, one or two sentences, no question.");
  if (failures.indexOf("NO_QUESTION") > -1) parts.push("Your draft asked no question. End with exactly one question.");
  if (failures.indexOf("MANY_QUESTIONS") > -1) parts.push("Your draft asked more than one question. Ask exactly one.");
  if (failures.indexOf("BANNED_OPENER") > -1) parts.push("Your draft opened with praise. Do not praise; name what was right in the student's words.");
  if (failures.indexOf("SAME_OPENING") > -1) parts.push("Your draft began with the same words as your last reply. Begin differently.");
  if (failures.indexOf("REPLY_STATED_VALUE") > -1) parts.push("Your draft stated a value the student has not produced (" + unearned(reply, S, V).join(", ") + "). Rewrite without it.");
  return parts.join(" ");
}
// the cut: a completed problem's draft loses its question sentences; anything else failing falls back to the authored line
function cutQuestions(reply) { return String(reply).split(/(?<=[.!])\s+/).filter(function (sn) { return !/\?/.test(sn); }).join(" ").trim() || null; }

if (typeof module !== "undefined") module.exports = { unearned: unearned, BANNED_OPENERS: BANNED_OPENERS, checkDraft: checkDraft, rewriteInstruction: rewriteInstruction, cutQuestions: cutQuestions };
