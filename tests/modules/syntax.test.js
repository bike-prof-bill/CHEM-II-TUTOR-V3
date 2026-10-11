// Every file pasted into Apps Script must at least parse. Code.gs is never loaded by the Node tests (it is Google wiring),
// so a syntax error there reached the instructor's paste on 11 Oct 2026 unseen. This check reads each file as a script.
const fs = require("fs"), path = require("path");
const dir = path.join(__dirname, "..", "..", "gas");
let pass = 0, fail = 0;
for (const f of fs.readdirSync(dir).filter(n => n.endsWith(".gs"))) {
  try { new Function(fs.readFileSync(path.join(dir, f), "utf8")); pass++; }
  catch (e) { fail++; console.log(`  ${f}: ${e.message}`); }
}
console.log(`syntax: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
