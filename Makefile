# Same commands locally and in CI. Repository root = the former build_v3_ch10_cc folder.
PY   ?= python3
NODE ?= node

.PHONY: test test-gen test-verify test-modules test-regression gen-check content-check baseline purity generate latency

test: test-gen test-verify test-modules test-regression gen-check content-check purity

test-gen:
	$(PY) test_ch10_cc.py
	$(PY) test_ch13_eq.py
	$(PY) test_ch14.py
	$(PY) test_ch15.py
	$(PY) test_ch16.py
	$(PY) test_ch17.py
	$(PY) test_ch19_21.py

test-verify:
	$(NODE) gas/test_core.js
	$(NODE) gas/test_syringe.js
	$(NODE) gas/test_bird.js
	$(NODE) gas/test_vent.js
	$(NODE) gas/test_eq.js
	$(NODE) gas/test_ch14.js
	$(NODE) gas/test_ch15.js
	$(NODE) gas/test_ch16.js
	$(NODE) gas/test_ch17.js
	$(NODE) gas/test_ch19_21.js

test-modules:
	$(NODE) tests/modules/units.test.js
	$(NODE) tests/modules/shell_modules.test.js
	$(NODE) tests/modules/replay.test.js
	$(NODE) tests/modules/syntax.test.js
	$(PY) tests/modules/test_units.py
	$(PY) tests/modules/test_substances.py

latency:
	$(NODE) tests/latency.js

test-regression:
	$(NODE) tests/regression/integer_answer_accepted.test.js
	$(PY) tests/regression/collision_rejected_by_generator.py
	$(NODE) tests/regression/one_stage_one_notebook_card.test.js
	$(NODE) tests/regression/random_clicker.test.js
	$(NODE) tests/regression/no_exam_by_chance.test.js
	$(PY) tests/regression/sim_addresses.py
	$(NODE) tests/modules/tone_phrases.test.js
	$(NODE) tests/regression/log_row_never_dropped.test.js
	$(NODE) tests/regression/no_repeated_problem.test.js

generate:
	$(PY) run.py all --per-kind 3 --seed 1

gen-check:
	sh scripts/check_generated.sh

baseline:
	$(PY) scripts/snapshot_content.py content/BASELINE_authored.txt

content-check:
	sh scripts/check_content.sh

purity:
	sh scripts/check_shell_purity.sh

report:
	$(PY) scripts/build_report.py
