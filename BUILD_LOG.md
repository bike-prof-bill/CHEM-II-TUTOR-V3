# Build log: the verifier spine rebuild (docs/02_REBUILD_SPEC_spine_v2.md)

One entry per step. Numbers are from the run that shipped the step. Nothing here is a decision; decisions are the instructor's and live in the handoff.

## Step 1 (8 Oct 2026): repository and continuous tests

- Build folder is the repository root; documents under `docs/`; V2 under `reference/v2/`.
- CI: generator 600/600, verifier 47/47, generated files reproducible, authored content 212 strings baselined, shell purity 9 hits (advisory).

## Step 2 (8 Oct 2026): the generator declares every number; the verifier guesses nothing

**What changed**

- `units.json` is the only place a unit is named: dimension vectors, conversion factor and offset, and the aliases a student may type. `engine.py` reads it; `run.py` writes `gas/Units.gs` from it for the verifier. The hard-coded unit tables in `engine.py` and `Core.gs` are gone.
- Every variant now carries `expected`: one table of every number that may legitimately appear, each with `id`, `role` (intermediate / key / given / constant), `state`, `value`, `unit`, `dim`, `abs_tol`, alternative forms (`also`), and `require_unit`. `traps` carry `state`. The old `targets` field is gone. 14 to 24 declared numbers per variant.
- `Core.gs` has one pure matcher, `CORE.match(parsedNumber, expected, traps, ticked) → {type, …}`, exported and tested on its own. Types: `expected`, `needs_unit`, `wrong_dimension`, `trap`, `given`, `constant`, `stray`. Removed: the constant list, "small integers are constants", the stray-number closure, the hard-coded unit regex, the chemistry words in the prose-detector's stop list (now derived from `units.json` and the archetype's own symbol aliases).
- Matching never converts units silently. A typed unit must equal the declared form's unit; a bare number matches by value but cannot tick an entry that requires its unit. Converting a given is the student's step, so "39.9 kJ/mol" does not satisfy "ΔHvap in J/mol". A right value with a unit of another dimension ("357 atm" for a temperature) is `wrong_dimension`: refused, logged under guards as `WRONG_DIMENSION`, counted like a stray.
- Generator validation on every variant (`engine.validate`), replacing the key-only fortuitous filter: (1) no two declared entries of different state within the larger tolerance of each other; (2) no trap within three tolerances of any same-state entry (intermediates included, not just the key); (3) no given, after unit conversion, within three tolerances of the key. Rejections are counted by rule. Shipped bundle: 4 of 112 tries rejected, all by rule 1; rules 2 and 3 rejected nothing, as the old filter also rejected nothing.
- Constants the archetype declares for Clausius: R (8.314, 8.3145), 0.08206, 273.15, 273, 760, 101.325, 101.3, 1000, 1 (the 1 in 1/T), and, per the instructor (8 Oct), 0, 2 and 3 for integers written in prose. Not 100, and not 0.008314 (the latter is already an accepted alternative form of the ΔHvap-in-J step, per the shipped design).

**Two readings of rule 1, both switchable in `engine.py`**

Read literally, rule 1 rejected 20% of all variants and 48% of those with a normal-boiling-point given (the instructor's `ONE_ATM_POINT = 0.35`), because in those problems the pressure conversion equals a conversion factor (760, 101.325, 1) and the pressure ratio equals a given. Two policies, both defaulting to the reading that keeps those problems:

- `CONSTANT_COLLISIONS_REJECT = False`: an intermediate equal to a declared constant does not reject the variant. The matcher checks intermediates before constants, so the student who types 760 after converting 1 atm gets the conversion step credited, which is what happened. Keys are never exempt: a key within tolerance of a constant still rejects.
- `DROP_INTERMEDIATE_EQUAL_TO_GIVEN = True`: an intermediate equal to a number on the page (the ratio P2/P1 when P1 = 1 atm) is not evidence and is removed from that variant's declaration, recorded in `dropped`; the state must keep another route or the variant is rejected. 12 of the 108 shipped variants have one such removal.

Measured on 1,200 tries: literal reading 20% rejected; recommended reading 6%; normal-boiling-point share falls from 35% to about 31% instead of to about 18%.

**Tests**

- `test_ch10_cc.py`: 600/600; every shipped variant passes validation; every declared number carries `dim`. Field names updated, meaning unchanged.
- `gas/test_core.js`: 47/47, field names updated, meaning unchanged.
- New: `tests/regression/integer_answer_accepted.test.js` (10 checks), `tests/regression/collision_rejected_by_generator.py` (9), `tests/modules/units.test.js` (8), `tests/modules/test_units.py`.
- Authored content: 212/212 baseline strings present and unchanged.
- Shell purity: 9 → 2 (both in `index.html`, untouched by design until step 3).

**Behaviour change to watch in the logs**

A number in prose that matches nothing declared is now a stray, and a stray on a number item counts as a wrong try, exactly as before for strays. Undeclared small integers are strays rather than constants; 0, 1, 2 and 3 are declared for this archetype. The instructor's standing position (8 Oct): collisions of this kind are solved per archetype, by better problems and by declaring what is harmless there; the same question will arise for Raoult's law. The two validate() switches stay at their defaults. Declaring 2 exposed a precedence question at once: in one shipped problem the kJ-for-J slip produces T2 ≈ 1.9 K, whose ±1 K window covers 2, so "step 2" was read as that trap. Resolved in the matcher: a bare number equal to a declared constant is the constant, before traps; the same number typed with a unit cannot be a constant and still reaches the trap. Tested.

**Not done in this step**

- Dimensional checking inside typed equations (V2's `eqDim`): the equation checker still reads symbols only; a number with a unit inside an equation line is not parsed. Belongs with the `parse`/`match` split in step 4.
- `index.html` keeps its two chemistry references (subtitle, plot field names); step 3.
