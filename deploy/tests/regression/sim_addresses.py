"""Every scenario with a simulation gets every value its page reads, and every value is one the page knows (19-20 Oct 2026:
"simulations need to be active"). The gaps listed here are problems whose reaction, half-cell or ion is not in the page's data;
they open the page's default with a notice until Simulation_Claude adds the data. A new gap fails the test."""
import json, glob, re, sys
sys.path.insert(0, "."); sys.path.insert(0, "archetypes"); import _sheet as S
KNOWN_GAPS = {("ch16_G_and_K", "SK6", "reaction"), ("ch16_G_and_K", "WC5", "reaction"), ("ch16_entropy", "MI3", "process"),
              ("ch16_free_energy", "ZO1", "reaction"), ("ch16_free_energy", "ZO2", "reaction"), ("ch17_electrolysis", "AB4", "ion")} | {("ch17_E_G_K", f"LA{i}", "right") for i in range(1, 6)} | {("ch17_E_G_K", f"FC{i}", "right") for i in range(1, 7)}
ok = {"reaction": set(S.SIM_IDS["free_energy"]) | set(S.SIM_IDS["G_and_Q"]), "process": set(S.SIM_IDS["entropy"]), "left": set(S.SIM_IDS["cell_metals"]), "right": set(S.SIM_IDS["cell_metals"]),
      "ion": set(S.SIM_IDS["electrolysis_ions"]), "isotope": set(S.SIM_IDS["decay_isotopes"]), "nuclide": set(S.SIM_IDS["binding_nuclides"])}
found, bad, total = set(), [], 0
for f in sorted(glob.glob("output/*.bundle.json")):
    B = json.load(open(f)); aid = f.split("/")[-1].split(".")[0]
    for v in B["variants"]:
        url = (B["openers"][v["opener_index"]].get("media") or {}).get("simulation") or ""
        if not url: continue
        total += 1; sp = v.get("sim_params") or {}
        for k in [k for k in re.findall(r"\{(\w+)\}", url) if k not in ("theme", "substance")]:
            if k not in sp or (k in ok and str(sp[k]) not in ok[k]): found.add((aid, v["fixed_id"], k))
new = sorted(found - KNOWN_GAPS); fixed = sorted(KNOWN_GAPS - found)
for g in fixed: print("  note: a listed gap is now filled (remove it from KNOWN_GAPS):", g)
for g in new: print("  FAIL: simulation value missing or unknown to the page:", g)
print(f"sim_addresses: {total} problems with a page; {len(found)} known data gaps ({len(fixed)} since filled); {len(new)} new" + (" | all pass" if not new else ""))
sys.exit(1 if new else 0)
