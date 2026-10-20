# Regression tests named for the faults they catch

Each lands with the step that fixes its fault and is never deleted. `make test-regression` runs them.

| File | Fault | Landed |
| --- | --- | --- |
| `integer_answer_accepted.test.js` | a bare small integer typed as the answer was ignored as a constant | step 2 |
| `collision_rejected_by_generator.py` | the fortuitous filter guarded only the final key; an intermediate or a trap could land on another declared number | step 2 |
| `one_stage_one_notebook_card.test.js` | the ladder counted per item when per stage was decided: two fails on different items of one stage gave two notebook cards | step 3 |
| `random_clicker.test.js` | a persona that picks at random and types filler; 200 runs per archetype; never earns credit, never passes or reaches the credit gate on a clean attempt | step 3 |
| `log_row_never_dropped.test.js` | a log row that could not get the sheet lock within 3 s was thrown away silently | step 6a |
| `no_repeated_problem.test.js` | a student could draw the same problem twice while others remained | step 6b |

`tests/modules/` holds the per-module tests: units, substances, the seven shell modules (parse, match, stepmap, ladder, guards, prompt, log), and the replay test that proves Phase A is deterministic.
