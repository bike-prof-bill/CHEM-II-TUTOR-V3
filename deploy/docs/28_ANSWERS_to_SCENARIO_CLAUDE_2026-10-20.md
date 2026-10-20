# Answers to SCENARIO_CLAUDE's questions (Fable, 20 Oct 2026)

**Units.** mmHg was already there (it is torr). Added today and in the tutor now: mol/kg (also "molal"), M/s, M/min, M⁻¹ s⁻¹,
M⁻¹ min⁻¹, M⁻² s⁻¹ (also written M^-1 s^-1, L/(mol·s) and so on); s⁻¹ and min⁻¹ were there. `units_the_tutor_reads.txt` in the
kit is updated. Anything else, ask.

**Tolerance column.** Keep it. Blank means the default (2 %, or half a unit in the last written place). Otherwise write `±1 %`,
`±0.01 V`, `0.5 g` or `exact`; the tutor now reads that column for each problem. The column order is: id, scenario, kind,
problem sentence, constants and their sources, expected item by item, trap values, right picks, tolerance, simulation
parameters, status.

**Chapter 13 format.** Keep the chapter 13 sheet's own format (the Silent Beaker sheet) for the sixth scenario, and add a
`simulation parameters` column. `ch13_eq` is coded by hand from that sheet, not read by the sheet converter, so its own columns
are the right ones. Its kinds are in `ch13_eq.py` (in the kit); a new reaction needs its K, ΔH sign and source.

**New pick option sets.** zero/first/second, into/out/neither and disappearing/appearing are now built in, with option texts
that begin with the bare word. The Fable list need only name them; list in full any set beyond these.

**Chapter 10 materials.** In `for_SCENARIO_CLAUDE_chapter_10_materials.zip`: `ch10_cc.py` (the archetype: the step map, the
kinds, how a problem is drawn from the data, and the three scenario rules already coded, in `draw_state`), `substances.json`
(every liquid's normal boiling point, ΔHvap, melting point and source), and the five content files: openers, moves, errors,
`content_ch10_cc_limits.csv` (per scenario and liquid, the temperature and pressure ranges a problem may use) and
`content_ch10_cc_sentences.csv`. A new chapter 10 scenario is an opener row plus limits rows for the liquids it uses; a rule the
limits cannot express (like the Bird's room-temperature body), write in words and I code it.
