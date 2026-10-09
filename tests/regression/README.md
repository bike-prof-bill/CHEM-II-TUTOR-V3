# Regression tests named for the faults they catch

Each lands with the step that fixes its fault and is never deleted. `make test-regression` runs them.

| File | Fault | Landed |
| --- | --- | --- |
| `integer_answer_accepted.test.js` | a bare small integer typed as the answer was ignored as a constant | step 2 |
| `collision_rejected_by_generator.py` | the fortuitous filter guarded only the final key; an intermediate or a trap could land on another declared number | step 2 |
| `one_stage_one_notebook_card.test.js` | two fails on different items of one stage produced two notebook cards | step 3 (planned) |
| `random_clicker.test.js` | 200 random-input runs per archetype must never reach a credit gate | step 3 (planned) |

`tests/modules/` holds the per-module tests (units so far; parse, match, stepmap, ladder, guards, prompt, log arrive with the step-4 split).
