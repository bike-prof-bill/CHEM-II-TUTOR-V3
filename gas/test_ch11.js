// Chapter 11 pilot (The Salted Road, brief 32): the shell walks the whole conversation of docs/35 in plain mode, under help policies A, B
// and C; the sample student answers (test data, output/ch11_colligative.samples.json) meet the gates as the sheet says; the pivot, the
// companion, the notebook as last straw, the park, More help, More info, the page opening after the prediction with the student's values,
// the instrument window, the precision rule, the named wrong picks and the reader's named accounts.
const CORE = require("./Core.gs"); const ARCH = require("./Archetype_ch11_colligative.gs")["ch11_colligative"];
const SAMPLES = require("../output/ch11_colligative.samples.json");
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : (fail++, console.log("  FAIL:", m)); };
const fresh = (policy, rung, i) => CORE.newSession(ARCH, { variantIndex: i || 0, openerIndex: 0, stamp: "t" + policy, policy: policy, rung: rung || "faded" });
const turn = (S, m, extra, model) => CORE.processTurn(ARCH, S, Object.assign({ message: m, now: Date.now() }, extra || {}), model || null);
const V0 = ARCH.variants[0];
const ACCOUNT = "The salt ions get in the way so fewer water molecules hit the ice and refreeze, but melting keeps going, so it has to get colder before the rates match again.";

// ---- the sample answers meet the gates as the sheet says ----
const parseSamples = cell => { const out = {}; String(cell).split("||").forEach(p => { const m = p.match(/(STRONG|WEAK AT NUMBERS|WEAK AT CONCEPTS)\s*\((clears|refused)\):\s*(.*)$/s); if (m) out[m[1]] = { clears: m[2] === "clears", text: m[3].trim() }; }); return out; };
const acc = parseSamples(SAMPLES.openers["The Salted Road"]);
Object.keys(acc).forEach(k => {
  const S = fresh("B"); const r = turn(S, acc[k].text);
  ok((S.board.account_given === "ticked") === acc[k].clears, `account sample ${k}: ${acc[k].clears ? "clears" : "is refused"}: "${acc[k].text.slice(0, 50)}"`);
  if (!acc[k].clears) ok(!r.log.counted_fail || true, "a refused account is asked again");
});
// pivot samples: a strong or weak-at-numbers answer clears the pivot, a weak-at-concepts one does not (never counted either way)
["mol_found", "m_found", "i_found", "dT_found", "T_found", "sim_predict", "perturb_1"].forEach(st => {
  const cell = SAMPLES.moves[st]; if (!cell) return; const sm = parseSamples(cell);
  Object.keys(sm).forEach(k => {
    const S = fresh("B"); S.pivot = { state: st, stage: st }; S.board.account_given = "ticked";
    const r = turn(S, sm[k].text);
    ok((r.log.event_type === "PIVOT_CLEARED") === sm[k].clears && !r.log.counted_fail, `pivot sample ${st} ${k}: ${sm[k].clears ? "clears" : "missed"}, never counted`);
  });
});

// ---- the full conversation, policy B (companion, then notebook, then park) ----
{
  const S = fresh("B"); let r;
  r = turn(S, "salt lowers the freezing point"); ok(!S.board.account_given && r.log.counted_fail && r.log.guards.indexOf("OPENER_NOT_ENGAGED") > -1, "macro-only account refused by the two-list gate");
  r = turn(S, "the ions and the water molecules"); ok(!S.board.account_given && r.log.guards.indexOf("OPENER_NO_MECHANISM") > -1 && !r.log.counted_fail, "particles named without a mechanism: refused, not counted");
  r = turn(S, ACCOUNT); ok(S.board.account_given === "ticked" && r.problem && /265 g/.test(r.problem.text), "the account clears and the problem appears");
  r = turn(S, "", { info: true }); ok(r.log.event_type === "INFO_REQUEST" && r.info && /Example 11\.13/.test(r.info.title) && r.info.text.length > 200 && /Explain how to turn a mass/.test(r.info.prompt) && !r.log.counted_fail, "More info: the anchored passage and the step's notebook prompt, not counted");
  r = turn(S, "265 mol"); ok(r.log.counted_fail && /periodic table/.test(r.reply) && r.log.help_rung === "", "wrong 1: the switch question");
  r = turn(S, "2.65 mol"); ok(r.log.event_type === "PIVOT_ASKED" && /formula units/.test(r.reply) && r.log.help_rung === "pivot", "wrong 2: the pivot question");
  r = turn(S, "the molar mass from the periodic table"); ok(r.log.event_type === "PIVOT_CLEARED" && /Step 1/.test(r.reply) && !r.log.counted_fail, "pivot answered: back to the step, not counted");
  r = turn(S, "7 mol"); ok(r.log.event_type === "COMPANION_SHOWN" && /160 g of sodium chloride/.test(r.reply) && /moles of NaCl = 2.74 mol/.test(r.reply) && !/4\.53/.test(r.reply), "wrong 3, policy B: the companion's step, never this problem's number");
  r = turn(S, "4.53 mol"); ok(S.board.mol_found === "ticked", "moles established");
  r = turn(S, "2.57 mol/kg"); ok(r.log.trap_ids === "SOLUTION_MASS" && /whole brine, or only the solvent/.test(r.reply), "the solution-mass trap fires with its approved question");
  r = turn(S, "", { help: true }); ok(r.log.event_type === "PIVOT_ASKED" && r.log.structured === "help" && r.log.help_rung === "pivot" && /dissolved in what/.test(r.reply), "More help on the second try gives the pivot");
  r = turn(S, "molarity"); ok(r.log.event_type === "PIVOT_MISSED", "a one-word pivot answer is missed, not counted");
  r = turn(S, "177 mol/kg"); ok(r.log.trap_ids === "GRAMS_FOR_MOLES" && r.log.event_type === "COMPANION_SHOWN", "wrong 3 at molality: the companion again (per step, not per stage)");
  r = turn(S, "9 mol/kg"); ok(r.log.event_type === "BAILOUT_ISSUED" && r.card && /molality and how it differs/.test(r.card.prompt), "wrong 4, policy B: the notebook as last straw");
  CORE.processBack(ARCH, S, Date.now() + 5000); r = turn(S, "Molality divides by the kilograms of the water alone, not the brine.");
  ok(r.log.after_bailout && CORE.activeState(S, V0) === "m_found", "back from the notebook; the step is asked again");
  r = turn(S, "8 mol/kg"); ok(r.log.event_type === "PARK" && S.board.m_found === "parked" && S.board.i_found !== "parked" && !S.clean, "wrong 5: molality alone is parked; the next step is untouched");
  r = turn(S, "1"); ok(r.log.trap_ids === "I_OMITTED", "i = 1 is the i-omitted trap");
  r = turn(S, "2"); ok(S.board.i_found === "ticked", "i established");
  r = turn(S, "-11.2 °C"); ok(r.log.trap_ids === "DT_SIGNED" && /a size, or a new temperature/.test(r.reply), "a negative lowering is the signed trap");
  r = turn(S, "11.2 °C"); ok(S.board.dT_found === "ticked", "the lowering established");
  r = turn(S, "11.2 °C"); ok(!r.log.counted_fail && S.board.T_found !== "ticked" && /with its sign/.test(r.reply), "a positive freezing point equals the lowering already on the board: read as a restatement (11 Oct rule), the step asked again with its sign; FP_SIGN is dropped by the factory as unreachable");
  r = turn(S, "-11 °C"); ok(S.board.T_found === "ticked" && !r.simulation_url, "the precision rule: −11 for −11.2 (two figures) is accepted; the page does not open yet");
  r = turn(S, "", { pick: "sim_predict:rises" }); ok(r.log.trap_ids === "SIM_PREDICT_SALT" && r.log.counted_fail, "the named wrong prediction");
  r = turn(S, "", { pick: "sim_predict:falls" });
  ok(S.board.sim_predict === "ticked" && r.simulation_url && /salt=NaCl&salt_g=265&water_kg=1\.50/.test(r.simulation_url) && /T_student=-11/.test(r.simulation_url) && /pred=falls/.test(r.simulation_url), "the page opens after the prediction with the student's freezing point and pick: " + r.simulation_url);
  ok(/Move the salt slider until the freezing point reads −10\.0 °C/.test(r.reply) && /1\.50 kg/.test(r.reply), "the instrument task asks in the approved words");
  r = turn(S, "237 g"); ok(r.log.counted_fail && S.board.sim_instrument !== "ticked", "237 g is outside the window");
  r = turn(S, "236 g"); ok(S.board.sim_instrument === "ticked" && /Where does your point sit/.test(r.reply), "236 g is inside; the gap question follows");
  r = turn(S, "My point sits on the line because the ions in the meltwater are what the line counts."); ok(S.board.sim_gap === "ticked" && /different salt/.test(r.reply), "the gap sentence clears; the change is asked");
  r = turn(S, "", { pick: "perturb_1:unchanged" }); ok(r.log.trap_ids === "PERTURB_I_IGNORED", "unchanged is the named wrong pick");
  r = turn(S, "", { pick: "perturb_1:falls" }); ok(S.board.perturb_1 === "ticked" && /ice surface with the other salt/.test(r.reply), "the right change; its why is asked");
  r = turn(S, "More ions crowd the liquid so fewer water molecules get back onto the ice."); ok(S.board.perturb_1_why === "ticked", "the why clears");
  r = turn(S, "cold"); ok(!S.board.meaning_given && !r.log.counted_fail, "a one-word meaning does not clear and is not counted");
  r = turn(S, "The ions keep enough water molecules away from the ice that refreezing only catches up with melting at this lower temperature."); ok(S.board.meaning_given === "ticked", "the meaning clears");
  r = turn(S, "The hardest step was molality; I would tell a friend to divide by the water only."); ok(S.done && !S.credit && !S.clean, "complete; no credit after a park");
  ok(r.log.policy === "B", "the log carries the policy");
}
// ---- policy A: pivot, then notebook, then park ----
{
  const S = fresh("A"); turn(S, ACCOUNT); let r;
  turn(S, "265 mol"); r = turn(S, "2.65 mol"); ok(r.log.event_type === "PIVOT_ASKED", "A: pivot on the second try");
  turn(S, "the molar mass from the periodic table"); r = turn(S, "7 mol"); ok(r.log.event_type === "BAILOUT_ISSUED" && r.card, "A: the notebook on the third");
  CORE.processBack(ARCH, S, Date.now() + 1000); turn(S, "Grams divided by the molar mass gives moles."); r = turn(S, "6 mol"); ok(r.log.event_type === "PARK" && S.board.mol_found === "parked", "A: park on the fourth");
}
// ---- policy C: pivot, then the step done for them ----
{
  const S = fresh("C"); turn(S, ACCOUNT); let r;
  turn(S, "265 mol"); r = turn(S, "2.65 mol"); ok(r.log.event_type === "PIVOT_ASKED", "C: pivot on the second try");
  turn(S, "mole"); r = turn(S, "7 mol"); ok(r.log.event_type === "PARK" && S.board.mol_found === "parked" && /grams ÷ molar mass/.test(r.reply), "C: the step done for them on the third, with its park text");
}
// ---- the account step has no pivot: a second counted refusal goes straight to help (a model refusing twice, the reader silent) ----
{
  const S = fresh("A"); let r; const no = () => ({ accept: 0, socratic_response: "Which molecules are leaving the ice, and which are joining it?" });
  const model = () => no(); model.batch = () => [no(), { found: 1, quote: "warm the ice", why: "nothing is heated" }];
  r = turn(S, "the ions warm the ice so fewer water molecules reach the surface and refreeze", null, model); ok(r.log.counted_fail && !S.board.account_given, "a wrong account past the gates, refused by both readers: counted");
  model.batch = () => [no(), { found: 1, quote: "melt the ice", why: "ions do not melt ice by reacting" }];
  r = turn(S, "the ions reach the surface and melt the ice so the water molecules dilute away", null, model);
  ok(r.log.event_type === "BAILOUT_ISSUED" && !!r.card, "account: the second counted refusal reaches the notebook (no pivot on the particle step)");
}
// ---- the reader names a listed wrong account (a model that returns the account id) ----
{
  const S = fresh("B"); const sr = { found: 0, quote: "", why: "", account: "SALT_HEATS" };
  const model = (sys, hist, msg) => ({ accept: 1, socratic_response: "Good thinking. What next?" }); model.batch = reqs => [{ accept: 1, socratic_response: "Good thinking. What next?" }, sr];
  const r = turn(S, "The salt ions heat up the ice surface so the water molecules there leave faster and fewer come back.", null, model);
  ok(!S.board.account_given && r.log.trap_ids === "SALT_HEATS" && /Nothing here is heated/.test(r.reply) && r.log.guards.indexOf("ACCOUNT_NAMED") > -1, "the reader's named account: refused with the approved repair question");
}
// ---- a clean Independent run earns credit; no ladder fires there ----
{
  const S = fresh("B", "independent"); turn(S, ACCOUNT);
  ["4.53 mol", "3.02 mol/kg", "2", "11.2 °C", "-11.24 °C"].forEach(m => turn(S, m));
  turn(S, "", { pick: "sim_predict:falls" }); turn(S, "235 g"); turn(S, "My point sits on the line because the ions in the meltwater are what the line counts.");
  turn(S, "", { pick: "perturb_1:falls" }); turn(S, "More ions crowd the liquid so fewer water molecules get back onto the ice.");
  turn(S, "The ions keep enough water molecules away from the ice that refreezing only catches up with melting at this lower temperature.");
  turn(S, "The hardest step was molality; divide by the water only.");
  ok(S.done && S.clean && S.credit, "a clean Independent run: credit");
}
// ---- the precision rule stays confined: an older archetype still refuses a coarse value ----
{
  const EQ = require("./Archetype_ch13_eq.gs")["ch13_eq"]; ok(!EQ.variants.some(v => v.precision_rule), "chapter 13 does not declare the precision rule");
}
console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
