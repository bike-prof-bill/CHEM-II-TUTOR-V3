# Fable list, chapter 11 pilot: `ch11_colligative`, scenario The Salted Road (SCENARIO_CLAUDE, 21 Oct 2026). Approved 21 Oct 2026.

## Needs your decision (Fable)

1. **Step order, kind `freezing`:**
   `account_given` → `mol_found` (mol) → `m_found` (mol/kg) → `i_found` (exact count) → `dT_found` (°C) → `T_found` (°C) →
   `sim_predict` (pick; page opens after it) → [page: reveal, instrument, gap question] → `perturb_1` (pick) →
   `perturb_1_why` (text) → `meaning_given` (text).
   `kg_found` from document 27 is skipped: the meltwater is given in kg (see Departures).
2. **Option sets:** `sim_predict` and `perturb_1` use rises/falls/unchanged. No new set.
3. **Difficulty count:** 3 (steps 4, conv 1). `i_found` is its own board step, so it counts once, as a step (Fable, 21 Oct).
4. **Account and meaning gates:** one particle noun and one mechanism word, the two lists in the opener's keyword cell
   (Fable, 21 Oct). "freezing" and "lowers" are in neither. "Salt lowers the freezing point" is in the wrong-accounts list
   (MACRO_ONLY).
5. **Worked companions** (variations of this scenario, until six scenarios exist): RS1↔RS5 (NaCl), RS2↔RS6 (CaCl₂), RS3↔RS4
   (KCl, MgCl₂). Each pair is the same rank, with a different context.
6. **New page `ch11/freezing_point_simulator.html`** (Simulation_Claude builds it once the instructor approves). Ids:

   | id | kind | range / values | unit |
   |---|---|---|---|
   | `salt_select` | control (set by parameters; student may change) | NaCl, KCl, CaCl2, MgCl2 | — |
   | `salt_g` | control, slider | 0 to 500, step 1 | g |
   | `water_kg` | control, set by parameters (shown, may be changed) | 0.50 to 2.50, step 0.05 | kg |
   | `m_readout` | reading | — | mol/kg |
   | `i_readout` | reading | 2 or 3 | — |
   | `dT_readout` | reading | — | °C |
   | `Tf_readout` | reading | — | °C |
   | `Tf_twice_salt_marker` | reading: the page's freezing point for twice the salt, shown at the reveal | — | °C |

   Parameters: `salt`, `salt_g`, `water_kg`, `theme`. Add to `sim_ids.json` as `"freezing_point_salts": ["NaCl", "KCl", "CaCl2", "MgCl2"]`.
   The page uses K_f = 1.86 °C·kg/mol and ideal i (2 or 3), as the problems do.
7. **Registry coverage in this scenario:** GC2-M-06 (i omitted: at `i_found`, `dT_found`, `perturb_1`), GC2-M-07 (solution mass:
   at `m_found`), GC2-M-08 (sign: at `T_found`). Own ids: GRAMS_FOR_MOLES, PERTURB_I_IGNORED,
   SIM_PREDICT_SALT, DT_SIGNED (GC2-M-08 at `dT_found`).
8. **Sign convention (Fable, 21 Oct):** `dT_found` is the lowering as a magnitude, as the book writes it; its ask says "a
   positive number", and DT_SIGNED (GC2-M-08) catches −ΔT there. `T_found` is signed; FP_SIGN (GC2-M-08) catches +ΔT there.

## Engineering

**Wrong particle accounts the reader should name** (repair prompts await the instructor):

| id | registry | the account | repair prompt (tutor's voice) |
|---|---|---|---|
| SALT_HEATS | — | the salt warms or heats the ice | Nothing here is heated; the road stays at −5 °C. At the ice surface, which molecules leave the ice, and which arrive? |
| LAW_NAME | — | "freezing point depression" / "colligative property" | That names what happens. What are the water molecules and the ions doing at the ice surface to make it happen? |
| MACRO_ONLY | — | the salt lowers the freezing point, so the ice melts | That is true of the road. Look closer: at the ice surface, which molecules leave the ice, and which return to it? |
| SALT_BREAKS_WATER | nearest GC2-M-01 (chapter 10) | the salt breaks the water molecules apart, or reacts with the ice | When ice melts, do water molecules come apart, or do they only leave the solid? What do the ions change about that? |

**Notebook prompt (the "more info" button):** I'm studying freezing point depression for solutions of ionic compounds (OpenStax
Chemistry 2e, section 11.4, Example 11.13). Explain how dissolved ions lower the freezing point of water, how the van 't Hoff factor
counts them, and why molality, not molarity, is used. Then give me three more problems like this, each worked in full.

**OpenStax anchors:** all in 11.4, held in the chapter file the instructor sent (Example 11.4, 11.9, 11.13; Table 11.3;
Figure 11.21). Whether the repository's `reference/openstax` holds the same text, I cannot check; please confirm.

**Tolerance:** the precision rule of 21 Oct. Every trap differs from the right value at two figures and from every given.
`sim instrument` ±2 %.

**Tutor cannot yet do:** nothing known.

## Departures from document 27
1. **`kg_found` skipped.** The meltwater is given in kilograms, which keeps the scenario at rank 3. A rank-4 scenario will give
   grams of water.
2. **The perturbation is a change of salt** at the same moles (rises or falls, by i), not "more solute". "Twice the salt" is the
   simulation's prediction instead, so it is not asked twice.
