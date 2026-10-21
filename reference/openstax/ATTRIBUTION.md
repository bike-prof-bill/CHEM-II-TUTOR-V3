# OpenStax chapters kept here for vocabulary and sourcing

Source: OpenStax *Chemistry 2e* (and *Chemistry: Atoms First 2e* where noted), licensed CC BY 4.0, https://openstax.org/.
Attribution required for any sentence reused where a student sees it: "Access for free at https://openstax.org/books/chemistry-2e/".
Use in this project: the course's own vocabulary for scenario keywords, mechanism-word lists, the second reader's context, and
notebook prompts that point at sections students have. SCENARIO_CLAUDE paraphrases; it does not quote into student-facing cells
without the attribution line in the openers file's credit column.

| File | Chapter | Added |
|---|---|---|
| Chapter10_IMF.md | 10, Liquids and Solids (vapor pressure in 10.3–10.4) | 12 Oct 2026, from the instructor |
| Chapter11_Solutions_and_Colloids.md, figures/ch11/ | 11, Solutions and Colloids: sections 11.1 to 11.5, Examples 11.1 to 11.13, 37 figures, exercises 1 to 75 | 21 Oct 2026, cleaned by CLEANUP_CLAUDE from the instructor's PDF (docs/33) |
| Chapter12_Kinetics.md, figures/ch12/ | 12, Kinetics: sections 12.1 to 12.7, Examples 12.1 to 12.15, 25 figures (39 images with example pictures and one structural equation), exercises 1 to 84 | 21 Oct 2026, cleaned by CLEANUP_CLAUDE from the instructor's PDF (docs/33) |

Cleaned chapters (docs/33 format) begin `# Chapter N`; `scripts/check_textbook.py` checks each one: sections, example numbering,
figure links, exercise numbering, ligature errors. The explainer and the "more info" prompt read these files only.
