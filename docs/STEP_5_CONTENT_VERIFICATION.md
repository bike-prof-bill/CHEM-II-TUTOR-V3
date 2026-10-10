# Step 5: content verified unchanged (9 Oct 2026)

Every authored string in the step-1 baseline (212, taken from the untouched bundle on 8 Oct) was compared with every authored string the repository holds now (412).
**27 original strings are no longer present as written. Every one traces to an instruction from the instructor, recorded in BUILD_LOG.md on the day it was given.** No string was changed on the architect's or constructor's initiative.

## The 27, grouped, with the instruction each traces to

| strings | instruction |
| --- | --- |
| content_ch10_cc_moves.csv, `ask` of T_in_K, dH_in_J, P_same_units, dH_found, bp_found (5 cells) | 9 Oct: 'Both: keep the conceptual sentence and add the action in the same cell.' The sentence was appended; the original words are intact at the start of each cell. |
| content_ch10_cc_openers.csv, Rubbing Alcohol Chill, liquids it fits (1 cell) | 9 Oct: 'Let's fill it out with 7, nix the t-butyl'; earlier the same day, the four alcohols for the enthalpy problems. |
| ch10_cc.ASK dH and its prose literal (2 lines, one string) | 9 Oct: 'of the alcohol' rather than 'of the liquid' (class-aware wording). |
| ch10_cc prose: 'An unidentified liquid' and the slope-problem sentence (2 lines) | 9 Oct: 'Have the question read unidentified alcohol rather than unidentified liquid.' Class-aware; other liquids unchanged. |
| ch10_cc.SUBSTANCES, 17 rows | 9 Oct: the NIST lists (ΔHvap at the normal boiling point, boiling points, then melting points as a fifth column, which changed every row's shape; water's values are unchanged). The three four-carbon isomers were additions. |

## The 227 additions, by kind (additions were allowed throughout; none alters an existing string)

| count | kind |
| --- | --- |
| 100 | Equilibrium openers and moves (new archetype, all DRAFT) |
| 31 | Clausius moves: new stage and label_when_done columns, amended ask cells |
| 29 | Equilibrium prose literals (trap questions, option texts, prompts) |
| 20 | Universal substance table records |
| 20 | Clausius liquids table rows in the new five-field shape, plus the three isomers |
| 14 | Equilibrium archetype objects (title, relation, equation picks, trap notes) |
| 7 | Clausius openers: media columns, the amended fits cell |
| 5 | Clausius prose literals in their new split form, plus the class-aware sentence |
| 1 | Clausius ASK dH, class-aware |

## How it is kept this way

`make content-check` runs on every push: any baseline string changed or removed fails the build. An instructor-directed change is applied by replacing exactly the affected baseline lines, by hand, and recording it in BUILD_LOG.md; the baseline is never regenerated. `content/BASELINE_authored.txt` is the reference; `git show bae4fc6:content/BASELINE_authored.txt` is the untouched step-1 original.
