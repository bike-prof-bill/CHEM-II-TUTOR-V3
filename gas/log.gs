// log.gs — one module of the tutor shell (rebuild spec, step 4). Apps Script shares one global scope across files;
// in Node, Core.gs loads every module and makes its exports global, so plain function declarations work in both.
var GATE_OF_KIND = { text: "G2", pick: "G1", direction: "G1", number: "G0", equation: "G0", table: "G0", reflection: "none" };
// One log row per turn, carrying both phases' timings. The analysis side reads these columns; add, never rename.
function logRow(arch, S, V, ev, res, timing) {
  var a = ev.active ? entry(V, ev.active) : null;
  return { event_type: ev.event_type, attempt_id: S.attemptId, archetype_id: S.archetypeId, variant_id: S.variantId, problem_kind: V.kind,
    content_version: arch.content_version, state: ev.active || "", stage: a ? a.stage : "", register: a ? a.register : "",
    face: a ? a.face : "", gate: a ? GATE_OF_KIND[a.kind] : "",
    entering_done: ev.entering, leaving_done: res.progress.done, newly: ev.newly.join(","), tries_on_stage: a ? (S.tries[a.stage] || 0) : "",
    counted_fail: ev.counted_fail, after_bailout: !!ev.after_bailout, seconds_away: ev.seconds_away || "", trap_ids: (ev.traps || []).join(","),
    structured: ev.structured || "", model_accept: ev.model_accept === undefined ? "" : ev.model_accept, second_reader: ev.second_reader || "",
    guards: (ev.guards || []).join(","), fallback_used: !!ev.fallback_used, turn_kind: ev.turn_kind || "", clean: S.clean, done: S.done, credit: S.credit,
    verdict_ms: timing && timing.verdict_ms !== undefined ? timing.verdict_ms : "", say_ms: timing && timing.say_ms !== undefined ? timing.say_ms : "" };
}

if (typeof module !== "undefined") module.exports = { GATE_OF_KIND: GATE_OF_KIND, logRow: logRow };
