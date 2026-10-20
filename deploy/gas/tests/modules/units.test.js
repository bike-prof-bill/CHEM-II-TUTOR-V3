// Units as data: the verifier's units module, read from units.json via Units.gs.
const CORE = require("../../gas/Core.gs"), U = CORE.units;
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const close = (a, b, t) => Math.abs(a - b) <= (t || 1e-9);
ok(close(U.convert(100, "degC", "K"), 373.15), "degC -> K");
ok(close(U.convert(1, "atm", "torr"), 760), "atm -> torr");
ok(close(U.convert(101.325, "kPa", "atm"), 1), "kPa -> atm");
ok(close(U.convert(39.9, "kJ/mol", "J/mol"), 39900), "kJ/mol -> J/mol");
ok(U.convert(1, "atm", "K") === null, "pressure -> temperature is null");
ok(U.vecSame(U.dim("K"), U.dim("degC")) && !U.vecSame(U.dim("K"), U.dim("atm")), "dimension vectors");
ok(U.canon("mmHg") === "torr" && U.canon("kelvin") === "K" && U.canon("°C") === "degC" && U.canon("kJ") === "kJ/mol", "aliases canonicalise");
const n = CORE.parseNumbers("T2 = 351.5 K, P1=394 mmHg, 3.86×10⁴ J/mol, 1.2e-3 atm, H2O, 38,600 J, 8.314 J/(mol·K), 25 °C");
ok(JSON.stringify(n.map(x => [x.x, x.unit])) === JSON.stringify([[351.5, "K"], [394, "torr"], [38600, "J/mol"], [0.0012, "atm"], [38600, "J/mol"], [8.314, "J/(mol·K)"], [25, "degC"]]), "number reader uses the data: " + JSON.stringify(n));
console.log(`units: ${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
