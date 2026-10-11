# Universal substance table

`substances.json` is the one place a substance's physical data lives. Chemistry archetype files read it through
`archetypes/_substances.py`; the tutor shell never reads it (the purity check keeps the shell free of chemistry).

- One record per substance. Every numeric field names its source and date under `source`.
- Fields are optional. An archetype asks for the fields it needs with `_substances.get(name, field, ...)`, which raises if a field
  is missing; nothing defaults silently. So a colligative-properties archetype that needs `Kf_K_kg_mol` fails at build time until
  the instructor supplies the value, rather than running on a guess.
- Convention: `dHvap_at_Tb_kJ_mol` is the enthalpy of vaporization at the normal boiling point (instructor, 9 Oct 2026).
- Teaching parameters do not belong here. The coldest temperature a Clausius-Clapeyron problem may use, for example, is a range the
  instructor chooses per archetype and lives in that archetype's file (`LIQUIDS` in `ch10_cc.py`), tested against the melting point here.
- The content check (`make content-check`) guards every record: a changed value fails the build unless the baseline line is replaced on
  the instructor's instruction.

Fields today: `formula`, `melting_point_C`, `boiling_point_C`, `dHvap_at_Tb_kJ_mol`.
Planned, instructor to supply: `molar_mass_g_mol`, `density_g_mL` (with its temperature), `Kf_K_kg_mol`, `Kb_K_kg_mol`, `dHfus_kJ_mol`.
