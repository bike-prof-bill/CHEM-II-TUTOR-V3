# For Fable, from SCENARIO_CLAUDE, 17 Oct 2026: opener rewrites (a correction to the chapter 13 and 14 sends)

The instructor approved these on 17 Oct 2026, after his test run of The Corn Soak. Three opener files replace the ones you hold.
In nine scenario rows, only three cells changed:
- the opening question's last sentence: no longer "What are the … doing?", now a precise question about the process;
- the model answer: terse and technical, for the model;
- the keywords: technical terms, each with a plain synonym.

Nothing else in the scenarios changes.

## Needs your decision

Nothing from the instructor. Three requests:

1. **Keyword matching.** "proton" matched inside "protonated", so a definition was accepted as the particle account. Please
   match whole words or whole phrases for every keyword, not only those under four letters.
2. **`06_SCENARIO_CLAUDE_role.md`** still tells scenario writers to end the opening question with "what the particles are doing".
   The instructor calls that wording meaningless, since in chemistry the answer is often "nothing". Please replace it with: the
   question names the process the problem is about (for example, "What microscopic processes are taking place?", "Which species
   does each solute form in water, and how completely?"), and the model answer is terse and technical. The instructor's
   Johnstone probe bank is the source of the question types.
3. **Ion formulas in `salts.json`** (chapter 15) are written with carets ("SO4^2-"). If they fill `{cation}` and `{anion}` in tutor
   text, please keep a display form without the caret.

## Engineering

| file | rows changed |
|---|---|
| `content_ch13_eq_openers.csv` | The Silent Beaker, The Purple Piston, The Fading Brown |
| `content_ch14_ph_openers.csv` | Off the Scale, The Corn Soak (model answer and keywords; its question was rewritten earlier), The Stockroom Morning, Concrete Burn |
| `content_ch14_acidbase_openers.csv` | Same Label, Different pH; The Fishy Bowl |

The chapter 14 opener files also carry the picture cells from the 17 Oct picture update.
