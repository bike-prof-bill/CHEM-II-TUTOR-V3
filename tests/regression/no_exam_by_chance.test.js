// An unstepped student is never served the exam scenario by chance (instructor, 13 Oct); a faculty preview may ask for it (15 Oct).
// The filters are built exactly as Code.gs and local_server.js build them.
const CORE = require("../../gas/Core.gs"), ARCH = require("../../gas/Archetype_ch13_eq.gs")["ch13_eq"];
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const roles = {}; ARCH.openers.forEach((o, i) => { roles[i] = o.role || "floater"; });
const examIdx = ARCH.openers.findIndex(o => o.role === "exam"); ok(examIdx >= 0, "chapter 13 has an exam scenario");
let drawn = 0;
for (let i = 0; i < 500; i++) { const p = CORE.chooseVariant(ARCH.variants, { kind: undefined, opener: undefined, rolesByOpener: roles, excludeRole: "exam" }, []); if (ARCH.variants[p.index].opener_index === examIdx) drawn++; }
ok(drawn === 0, "500 unstepped starts: the exam scenario never drawn (" + drawn + ")");
const p = CORE.chooseVariant(ARCH.variants, { kind: undefined, opener: String(examIdx) }, []);
ok(p && ARCH.variants[p.index].opener_index === examIdx, "a preview naming the exam scenario gets it");
const bad = CORE.chooseVariant(ARCH.variants, { kind: undefined, opener: String(examIdx), rolesByOpener: roles, excludeRole: "exam" }, []);
ok(bad === null, "a student naming the exam scenario in the menu still does not get it");
console.log(`no_exam_by_chance: ${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
