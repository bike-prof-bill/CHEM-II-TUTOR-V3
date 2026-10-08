# Regression tests named for the faults they catch

Empty at step 1. Each lands with the step that fixes its fault and is never deleted.

| File (planned) | Fault | Lands at |
| --- | --- | --- |
| `integer_answer_accepted.test.js` | a bare small integer typed as the answer was ignored as a constant | step 2 |
| `collision_rejected_by_generator.py` | an intermediate value within three windows of a trap, or a trap of a non-key intermediate, was not rejected | step 2 |
| `one_stage_one_notebook_card.test.js` | two fails on different items of one stage produced two notebook cards | step 3 |
| `random_clicker.test.js` | 200 random-input runs per archetype must never reach a credit gate | step 3 |
