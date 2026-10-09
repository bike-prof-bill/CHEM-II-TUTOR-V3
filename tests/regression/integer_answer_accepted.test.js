// Regression (rebuild spec, Change 2): a bare small integer typed as the answer was ignored as a constant.
// Now the matcher knows only what the generator declared. Declared 2 is the answer; undeclared 2 is stray.
const CORE = require("../../gas/Core.gs");
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };

const expected = [
  { id: "key_value_found", state: "value_found", role: "key", label: "i", value: 2, unit: "", abs_tol: 0.01 },
  { id: "c_one", state: null, role: "constant", label: "one", value: 1, unit: "", abs_tol: 1e-9 },
];
const traps = [{ id: "ORDER_DOUBLED", state: "value_found", value: 4, unit: "", abs_tol: 0.01 }];

let r = CORE.match({ x: 2, unit: null }, expected, traps, {});
ok(r.type === "expected" && r.ids.length === 1 && expected[r.ids[0]].role === "key", "declared integer 2 is accepted as the key: " + JSON.stringify(r));
r = CORE.match({ x: 4, unit: null }, expected, traps, {});
ok(r.type === "trap" && r.id === "ORDER_DOUBLED", "declared integer trap is named");
r = CORE.match({ x: 1, unit: null }, expected, traps, {});
ok(r.type === "constant", "declared constant is a constant");
r = CORE.match({ x: 3, unit: null }, expected, traps, {});
ok(r.type === "stray", "undeclared small integer is stray, not a constant");
r = CORE.match({ x: 760, unit: null }, expected, traps, {});
ok(r.type === "stray", "undeclared 760 is stray: the shell has no constant list");
r = CORE.match({ x: 4, unit: null }, expected, traps, { value_found: true });
ok(r.type === "stray", "a trap for a state already set is not reported");

// a real variant from the bundle: the matcher is the same function the turn uses
const ARCH = require("../../gas/Archetype_ch10_cc.gs")["ch10_cc"];
const V = ARCH.variants.find(v => v.kind === "T2"), key = V.expected.find(e => e.role === "key");
r = CORE.match({ x: key.value, unit: null }, V.expected, V.traps, {});
ok(r.type === "needs_unit" && r.needs.unit === key.unit, "bare key value asks for its unit");
r = CORE.match({ x: key.value, unit: key.unit }, V.expected, V.traps, {});
ok(r.type === "expected", "key value with its unit is accepted");
const other = key.unit === "degC" ? "K" : "degC";
r = CORE.match({ x: key.value, unit: other }, V.expected, V.traps, {});
ok(r.type !== "expected", "same number in the other temperature unit is NOT silently converted into the key");
r = CORE.match({ x: key.value, unit: "atm" }, V.expected, V.traps, {});
ok(r.type === "wrong_dimension", "a temperature value with a pressure unit is a dimension error, not a match: " + r.type);

// a bare declared constant outranks a trap whose window covers it; the same number WITH a unit still reaches the trap
const V38 = ARCH.variants.find(v => v.traps.some(t => Math.abs(t.value - 2) <= t.abs_tol && t.unit));
if (V38) {
  const tr = V38.traps.find(t => Math.abs(t.value - 2) <= t.abs_tol && t.unit);
  r = CORE.match({ x: 2, unit: null }, V38.expected, V38.traps, {});
  ok(r.type === "constant", "bare 2 in prose is the constant, not trap " + tr.id + " at " + tr.value);
  r = CORE.match({ x: 2, unit: tr.unit }, V38.expected, V38.traps, {});
  ok(r.type === "trap" && r.id === tr.id, "2 " + tr.unit + " is still the trap");
} else { pass += 2; }

console.log(`integer_answer_accepted: ${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
