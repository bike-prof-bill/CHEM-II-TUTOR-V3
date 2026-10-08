# Repository notes (step 1 of docs/02_REBUILD_SPEC_spine_v2.md)

`README.md` is the build's own readme and is unchanged. This file describes the repository around it.

## Layout

The former `build_v3_ch10_cc` folder is the repository root, byte-for-byte. Added:

    docs/                           handoff, spec, accessibility reports, briefs, instructor source material
    reference/v2/                   V2 code and page, read-only; needed in step 3 for the ICE port
    .github/workflows/tests.yml     five CI jobs on every push (see below)
    Makefile                        the same commands locally
    scripts/                        the three checks
    content/BASELINE_authored.txt   the "before" snapshot of every authored string (212). Taken once from
                                    the unchanged files on 8 Oct 2026. Never regenerated during the rebuild.
    tests/regression/               empty; the named regression tests land in steps 2–4
    REPOSITORY.md                   this file

## Commands

    make test            generator + verifier + generated-check + content-check (what CI requires)
    make test-gen        python test_ch10_cc.py              600/600
    make test-verify     node gas/test_core.js               47/47
    make gen-check       committed generated files match `run.py ch10_cc --per-kind 3 --seed 1`
    make generate        regenerate them (after any source or content change; then commit)
    make content-check   every baseline authored string still present, unchanged
    make purity          chemistry words in the shell; reports now, blocks from step 3
    make baseline        rewrite the baseline. Do NOT run during the rebuild.

## What the content check covers

Every non-empty cell of `content_ch10_cc_openers.csv` and `content_ch10_cc_moves.csv`, keyed by row and
column, so adding the step-3 `stage` column adds lines and alters none. From `archetypes/ch10_cc.py`: the
liquids table, equation picks, trap notes, trap ids, problem sentences, title and relation text, keyed by
name so they can move to a data file in step 2 without touching the baseline. Any other prose literal of
20+ characters in that file. Docstrings and code strings are not content.

Edits and removals fail the check. Additions are listed and allowed.

## Shell purity, 8 Oct 2026 count (the step-3 target is zero)

    engine.py      2 hits   pressure unit table (atm)
    gas/Core.gs    5 hits   unit aliases, number regex, stop-word list, one comment
    index.html     2 hits   page title "Clausius-Clapeyron"; problem-point mapping (K, atm)
    total          9

## Not changed, deliberately

`README.md` still says `--per-kind 12` gives 72 problems; the shipped generation is `--per-kind 3 --seed 1`
giving 108 (3 × 6 kinds × 6 openers) and `gen-check` pins that. The readme is the build's text and is left
for the instructor's or Opus's clean-up pass.

