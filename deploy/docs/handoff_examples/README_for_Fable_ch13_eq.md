# ch13_eq: both scenarios, with their simulations (14 Oct 2026)

From SCENARIO_CLAUDE. One zip, as the instructor asked: both scenarios' rows and both pages linked. Everything in it is approved by the instructor. No row is DRAFT.

| File | What it is |
|---|---|
| `ch13_eq_openers.csv` | The two opener rows (15 columns plus role), unchanged: Martian Fuel **worked**, Haber-Bosch **exam**. |
| `ch13_eq_moves.csv` | All rows. Unchanged rows are re-approved; `approach` is dropped. New and changed rows, approved 13 Oct: `perturb_1`, `perturb_1_why`, `perturb_2` and `perturb_2_why` for each scenario (Martian with show cells); `shift_predicted` as forward / reverse / neither; `relation_chosen` accepting Q or K. |
| `ch13_eq_errors.csv` | The ten existing errors, re-approved, plus `EXO_HEATED_FORWARD` and `SQUEEZE_SHIFT_EQUAL_MOLES`. |
| `ch13_eq_media_rows.csv` | MEDIA_SOURCES rows: the three pictures and both revised pages, with fingerprints and checks. |
| `reactions_add_haber.json`, `reactions_add_wgs.json` | Kc and its sources. Haber-Bosch now carries ΔH° = −91.8 kJ/mol and Kc at other temperatures, for the page's temperature slider. |

## The perturbations

| Scenario | perturb_1 | perturb_2 |
|---|---|---|
| Haber-Bosch | ammonia drawn off: forward | reactor heated: reverse, K falls |
| Martian Fuel | more steam: forward | squeezed to half the volume: neither |

## Simulations (approved 14 Oct 2026)

| Page | SHA-256 starts | Address (link settings unchanged) |
|---|---|---|
| haber_simulator.html | 6e6c554c | `…/haber_simulator.html?nN2={nN2}&nH2={nH2}&nNH3={nNH3}&V={V}&theme={theme}` |
| martian_fuel_simulator.html | 47fc365d | `…/martian_fuel_simulator.html?nCO={nCO}&nH2O={nH2O}&nCO2={nCO2}&nH2={nH2}&V={V}&theme={theme}` |

Both pages now let the student make each scenario's two changes and watch the mixture re-settle:
- **Haber-Bosch:** "Draw off NH3" and a temperature slider from 450 to 600 °C.
- **Martian Fuel:** "Squeeze to half" and "Add a little H2O".

The instructor places the files himself.

**Folder: please confirm.** The rows say `media/ch13_ice/`, because the earlier pages went there. Now that the archetype is `ch13_eq` (another chat's Silent Beaker brief names `media/ch13_eq/`), tell the instructor which folder to use. The openers' simulation column follows your answer.
