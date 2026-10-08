# Clausius-Clapeyron archetype: the narrative file, and the full decision flow

20 Sept 2026. Describes the build in the zip of the same date. Nothing here is fixed.

---

## 1. Needs your decision

1. **Opener-to-liquid pairing.** Done as you said: openers and problems now align. Your openers file has two new columns, *liquids* and *kinds*. I filled *liquids* with a first guess (below). Yours to correct.

   | Opener | Liquid I assigned |
   |---|---|
   | Bulging Sunlit Bottle | water |
   | Boiling Bell Jar Flash | water |
   | Rubbing Alcohol Chill | 2-propanol |
   | Crushed Cooled Flask | water |
   | Ten-Degree Vapor Surge | ethanol |
   | Sealed Syringe Standoff | water |

   Consequence: **14 of the 17 liquids are never asked**, because no scenario names them. The factory lists them on every run. A liquid enters the course when you write it a scenario.
2. **"Unidentified liquid" clashes with a named scenario.** When ΔHvap is the unknown, and in slope-from-data problems, my draft sentence says "an unidentified liquid" so the value cannot be looked up. After an opener about rubbing alcohol that reads oddly. Options: use the *kinds* column to keep those two kinds off named-liquid scenarios; or write one "mystery liquid" scenario that owns them; or name the liquid and accept the look-up risk.
3. **Tutor-led versus student-recall mode.** Section 4. No build until you say.
4. **Your keyword lists let labels through.** I tested the tree's examples against the real gates. "It is more volatile" passes the computer's check on the Rubbing Alcohol opener, because *volatility* and *evaporate* are keywords and they are names, not mechanisms. Only the AI then stands in the way. Two fixes, either or both: keep only mechanism words in the keyword column (weaker, attractions, fraction, energy, escape); or require two keyword hits instead of one. Your call; it is one number in `Core.gs`.

---

## 2. The narrative file: `content_ch10_cc_moves.csv`

One row for each thing the student must establish. One column for each thing the tutor may need to say about it. You write the cells. The computer decides *when* a cell is used; it never writes one.

### Columns

| Column | What it is | When it is used |
|---|---|---|
| **state** | The name of the board item. Do not edit; the code looks rows up by it. | — |
| **ask** | The tutor's normal question for this item. | Whenever this item is the next thing to establish. With Gemini on, it is given to the model as the *intent* and the model phrases it to fit the conversation. With Gemini off, or when the model's wording fails a check, the student sees your words exactly. |
| **switch_ask** | The same item approached from a different one of Johnstone's three accounts (particles, symbols, measurement). | After the **first** counted wrong try on this item. |
| **notebook_prompt** | The text the student copies into the course notebook. Asks for the idea and an example with a *different* liquid. Must never contain this problem's numbers. | After the **second** counted wrong try. Shown on a card with Copy, Open notebook, I'm back. No AI call is made on this turn. |
| **return_ask** | What the student is asked on pressing I'm back. They must answer in a sentence of their own before work resumes. Not graded for correctness; graded for being an actual sentence. | Once, on return from the notebook. |
| **park_text** | What is shown if the student fails twice more *after* the notebook. The item is handed over, the problem continues, and the attempt earns no credit. | At most once per item. For the three rearrangement rows leave it blank: the factory supplies the correct rearranged equation for that problem's unknown. |
| **status** | `DRAFT` or `approved`. | The factory counts DRAFT rows on every run. Later, a production build can refuse to ship any. |

### Rows

| Row (state) | Plain meaning | Who decides it is done |
|---|---|---|
| **account_given** | The student has said, in their own sentence, what the particles are doing in the opener scenario. The problem is hidden until this is done. *The `ask` cell is blank on purpose: the question is the opener itself.* | Computer gates (is it a sentence? does it touch the scenario's key ideas or talk about particles?) → then the AI judges → then a second AI reading looks for a false statement and can overrule. |
| **relation_chosen** | The student has picked the right relation from the unnamed Equations list. It is then pinned on screen. | Computer alone. |
| **rearranged** | The student has typed the relation rearranged with the unknown alone on the left. Mandatory. Pinned on screen. (Two-point problems.) | Computer alone, by substituting values. |
| **T_in_K** | Every Celsius temperature in the problem has appeared in kelvin. *Exists only if this problem shows a temperature in °C.* | Computer alone. |
| **dH_in_J** | ΔHvap has appeared in J/mol, or R has been restated in kJ. *Exists only if ΔHvap is shown in kJ.* | Computer alone. |
| **P_same_units** | One of the two pressures has appeared converted to the other's unit. *Exists only if the two pressures are shown in different units.* | Computer alone. |
| **substituted** | A legitimate in-between number has appeared: the pressure ratio, its natural log, the difference of reciprocal temperatures, or ΔHvap/R. | Computer alone. Also filled automatically when the final value is right. |
| **value_found** | The final value, with units, inside the grading window. Opens the simulation. | Computer alone. |
| **rearranged_dH** | Slope problems: ΔHvap written in terms of the slope. Mandatory. Pinned. | Computer alone. |
| **dH_found** | Slope problems: ΔHvap value with units. | Computer alone. |
| **rearranged_T** | Slope problems: the line rearranged for T alone. Mandatory. Pinned. | Computer alone. |
| **bp_found** | Slope problems: normal boiling point with units. | Computer alone. |
| **meaning_given** | The closing inference, in the student's own sentence. Carries the credit. | Same three layers as account_given. |

A two-point problem uses 6 to 9 of these rows, depending on which unit conversions its numbers call for. A slope problem uses 7.

Other text that is yours, not in this file: the **openers** (their own CSV), and inside `archetypes/ch10_cc.py` the **trap questions** (`TRAP_NOTES`), the **Equations list**, the **problem sentences**, and the **liquids table**.

---

## 3. The decision flow

### 3a. What happens to *every* message (the inner loop)

```
STUDENT SENDS SOMETHING
│
├─ Is it a repeat of a message already answered (network retry)?
│     └─ YES → send the stored reply again. Nothing is regraded. END
│
├─ Are we waiting for them to say what the notebook taught them?
│     ├─ Message is not a sentence of their own → ask return_ask again. Not a wrong try. END
│     └─ It is → note it, carry on below. Row is flagged "after notebook".
│
├─ THE COMPUTER READS THE MESSAGE (no AI yet)
│     ├─ An equation pick?         right → tick relation_chosen, pin it
│     │                            wrong → counted wrong try
│     ├─ Lines of algebra?         checked by substituting values:
│     │       unknown alone on left, and true      → tick the rearrangement, pin their own equation
│     │       true, but unknown not yet alone      → progress. Not a wrong try.
│     │       true only if a sign is dropped       → named: EQ_SIGN_FLIPPED. Counted wrong try.
│     │       true only with log base 10           → named: EQ_LOG_BASE. Counted wrong try.
│     │       not true                             → counted wrong try
│     │       cannot be read                       → asked to retype with brackets. Not a wrong try.
│     └─ Numbers (read only from lines that are not algebra)
│             matches a legitimate value           → remembered
│             matches the final value, no units    → asked for units. Not a wrong try.
│             matches what a known wrong turn gives→ that trap is named to the tutor
│             a given, a constant, a small integer → ignored
│             anything else                        → "stray"
│
├─ TICK whatever is now established. A right final value also fills the symbolic
│  items before it, EXCEPT the opening account, the closing inference, and any
│  rearrangement. A right number typed before its rearrangement is kept, and
│  counts the moment the rearrangement is accepted.
│
├─ Was this a COUNTED WRONG TRY?   (only these count)
│     • a wrong pick
│     • a wrong or trap-form rearrangement, while a rearrangement is the next item
│     • a trap number, or a stray number, with nothing new ticked
│     • on the two free-text items: a real sentence that the gates, the AI, or the
│       second reader did not accept
│     NEVER counted: questions, a missing unit on a right number, true-but-unfinished
│     algebra, unreadable algebra, greetings, network retries.
│
├─ WRONG-TRY LADDER, per item
│     1st  → tutor asks your switch_ask (a different account of the same thing)
│     2nd  → NOTEBOOK CARD. Your notebook_prompt, Copy, Open notebook, I'm back.
│            Input is locked. No AI call. Logged with a timestamp.
│            … student presses I'm back → time away is logged → your return_ask
│     then, after the return:
│     1st  → switch_ask again
│     2nd  → PARKED. The item is shown (park_text, or the correct rearrangement).
│            The problem continues. This attempt earns no credit.
│
├─ THE TUTOR SPEAKS  (skipped on notebook and park turns)
│     The AI is given: the rules, the problem (or only the opener, before the account),
│     the next item's `ask`, and the computer's verdict on this message.
│     It is never given the answer key.
│     Its draft is checked: does it state any value the student has not produced?
│         clean → sent
│         not   → one rewrite → still not → YOUR `ask` is sent, word for word
│
└─ ONE LOG ROW: build, content fingerprint, problem, item, Johnstone account,
   face (choice / check / why), how it was checked, wrong-try count, trap names,
   guard names, after-notebook flag, both AI verdicts, timings, the texts.
```

### 3b. One problem, start to finish: *The Rubbing Alcohol Chill*

Real output from the factory (problem `ch10_cc:38`). Your scenario, my draft problem sentence.

```
START ─ server picks a scenario, then a problem MADE FOR that scenario.
│       Scenario: The Rubbing Alcohol Chill  →  liquid: 2-propanol  →  kind drawn: solve for T2
│
▼
[1] ACCOUNT  (particles · "why" · computer gates + AI + second reader)
│   Screen: "Dabbing rubbing alcohol onto skin produces intense cold and rapid drying compared
│            to water … What are the liquid alcohol molecules doing compared to water molecules
│            that lets them flee into vapor so eagerly?"
│   The problem is hidden. The AI has not been shown it either.
│
│   ├─ "hi" / "Clausius-Clapeyron"
│   │      → not a sentence of their own → asked again. Not counted.
│   ├─ "It dries quickly because it reaches a dynamic balance sooner than water does."
│   │      → a sentence, but touches none of your keywords (weaker, intermolecular attractions,
│   │        cohesive forces, fraction, evaporate, volatility) and has fewer than two particle
│   │        words → refused by the computer, whatever the AI thinks. Counted.
│   │        → switch_ask → notebook → park.
│   ├─ "It is more volatile."
│   │      → WEAK SPOT. A label, not an account, but "volatile" hits your keyword "volatility",
│   │        so the computer lets it through to the AI. With Gemini on, rule 4 ("a name is not
│   │        an account") should refuse it. In plain mode it is ACCEPTED. See decision 4.
│   ├─ "The alcohol molecules break apart into atoms that fly off."
│   │      → passes the gates; AI may accept; SECOND READER quotes "break apart into atoms",
│   │        overrules. Counted. Tutor asks about that claim without correcting it.
│   └─ "Alcohol molecules attract each other more weakly than water molecules do, so a larger
│       fraction have enough energy to escape the surface."
│          → accepted. ✔ 1 of 9.
▼
    PROBLEM APPEARS:
    "2-propanol has a vapor pressure of 107.5 kPa at 83.9 °C. Its heat of vaporization is
     39.9 kJ/mol. At what temperature will its vapor pressure be 66.4 torr? Report the answer in K."
    This problem's numbers call for ALL THREE conversions, so its board has 9 items.
    From here the student may work in any order. The tutor asks about the first open item.
│
▼
[2] RELATION  (symbols · "choice" · computer alone)
│   ├─ picks ln(k2/k1) = −(Ea/R)(…)   or   ln(K2/K1) = −(ΔH°/R)(…)   → wrong try 1 → switch_ask
│   │      picks another wrong one                                     → wrong try 2 → NOTEBOOK
│   └─ picks ln(P2/P1) = −(ΔH/R)(1/T2 − 1/T1)   → ✔ PINNED on screen to the end.
▼
[3] REARRANGE FOR T2  (symbols · "check" · computer alone, by substitution) — MANDATORY
│   ├─ 1/T2 = 1/T1 − (R/ΔHvap) ln(P2/P1)          → true, not alone yet → nudge. Not counted.
│   ├─ T2 = 1/(1/T1 + (R/ΔHvap) ln(P2/P1))        → EQ_SIGN_FLIPPED. Counted.
│   ├─ T2 = 1/(1/T1 − (R/ΔHvap) log(P2/P1))       → EQ_LOG_BASE. Counted.
│   ├─ T2 = 1/1/T1 − R/ΔHvap·ln(P2/P1)            → not true as written. Counted.
│   └─ T2 = 1/(1/T1 − (R/ΔHvap)·ln(P2/P1))   or any equal form → ✔ PINNED under the relation.
│
▼   ── the next three may be done in any order, or all at once ──
[4] T IN KELVIN        357.05 K appears                                   → ✔
[5] ΔHvap WITH R       39 900 J/mol appears, or R given as 0.008314        → ✔
[6] PRESSURES MATCHED  806 torr appears (107.5 kPa), or 8.85 kPa (66.4 torr) → ✔
│
▼
[7] SUBSTITUTED        any one of:  P2/P1 = 0.0823 · ln(P2/P1) = −2.497 ·
│                      1/T2 − 1/T1 = 5.20×10⁻⁴ K⁻¹ · ΔHvap/R = 4799 K      → ✔
▼
[8] VALUE  (measurement · "check" · computer alone)      KEY: 301.1 K  (±1 K; 28.0 °C also accepted)
│   ├─ 301                → right, no units → "what are the units?"  Not counted.  "K" → ✔
│   ├─  80.4 K            → CELSIUS_NOT_CONVERTED  (83.9 put in as if kelvin)
│   ├─   1.9 K            → KJ_WITH_R_IN_J         (39.9 against 8.314)
│   ├─ 438.5 K            → SIGN_FLIPPED
│   ├─ 330.4 K            → LOG10_FOR_LN
│   ├─ 344.7 K            → PRESSURE_UNITS_MIXED   (66.4 / 107.5 taken as it stands)
│   │      each: named to the tutor, who asks your trap question and never states the fix. Counted.
│   ├─ any other number   → stray. Counted.
│   └─ 301.1 K            → ✔  and any of [4]–[7] still open are filled with it.
│                            (Typed before [3]? It is kept, and counts when [3] is done.)
▼
    SIMULATION OPENS: six "measured" points for this very liquid, the straight-line fit,
    the curve, this problem's two points marked, and a probe to drag. Probe use is logged.
│
▼
[9] MEANING  (inference · "why" · computer gates + AI + second reader) — CARRIES THE CREDIT
│   Your closing question. Same three layers as [1]. Same ladder.
▼
DONE
    ├─ nothing parked  → "Clean run recorded."            Mastery row: clean, credit.
    └─ anything parked → "Recorded without credit."       Mastery row: not clean.
    New problem = a fresh scenario and a fresh problem made for it.
```

### 3c. How the other kinds differ

```
solve for P2 or P1 → [6] disappears (only one pressure is given). Answer accepted in atm, torr or kPa, with units.
solve for T1       → same as T2.
solve for ΔHvap    → [5] disappears. Draft sentence says "an unidentified liquid" (see decision 2).
slope from data    → plots arrive WITH the problem (they are the data). Board:
                     account → pick  ln P = −(ΔH/R)(1/T) + C
                             → rearrange for ΔHvap (mandatory) → ΔHvap value
                             → rearrange for T     (mandatory) → boiling point value
                             → meaning.   The probe appears only at the closing item.
```

---

## 4. Tutor-led or student-recall: what there is to decide

**What already exists.** The board does not care about order. A student who simply works the problem, saying nothing to the tutor, is already followed correctly. What makes today's build *tutor-led* is one thing only: after every message the tutor asks about the next open item.

**So a recall mode is a small change, not a second system.** In recall mode the tutor stops asking. It confirms what the computer checked ("kelvin temperature checked"), answers questions, and otherwise waits. Everything that protects the learning stays on: the hidden problem, the mandatory rearrangement, units, traps, the wrong-try ladder, the closing inference. A stuck student still reaches the switch question, then the notebook.

**Things to weigh:**

| | Tutor-led | Student-recall |
|---|---|---|
| Retrieval practice (recalling the sequence yourself) | Little. The tutor's questions *are* the sequence. | Strong. This is the decision-based-learning goal: "what do I do next?" is the student's to answer. |
| Risk for a weak student | Low | Flounders sooner; but the ladder catches them at two wrong tries |
| What the log can tell you | Where each item fails | Also **which order** students choose, and **which items they skip until forced**. That is new information about how they see the problem. |
| Research value | — | The mode is logged on every row, so it becomes a variable you can compare on the exam. |

**Who chooses?** Three options.
1. *Student chooses, per problem.* Simple. But students choose comfort; expect most to stay tutor-led.
2. *Earned.* Recall unlocks for an archetype after one clean tutor-led run. This is fading of support, and it gives a natural progression: led → recall → exam.
3. *You assign*, by student or by week. Cleanest for research; least flexible for them.

My suggestion when you are ready: build the mode as a single switch that is logged, start with option 2, keep option 3 available for a study. It touches two places in `Core.gs` and adds one column to the log.
