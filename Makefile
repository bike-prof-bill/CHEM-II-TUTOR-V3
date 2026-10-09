# Same commands locally and in CI. Repository root = the former build_v3_ch10_cc folder.
PY   ?= python3
NODE ?= node

.PHONY: test test-gen test-verify test-modules test-regression gen-check content-check baseline purity generate

test: test-gen test-verify test-modules test-regression gen-check content-check purity

test-gen:
	$(PY) test_ch10_cc.py
	$(PY) test_ch13_ice.py

test-verify:
	$(NODE) gas/test_core.js
	$(NODE) gas/test_ice.js

test-modules:
	$(NODE) tests/modules/units.test.js
	$(PY) tests/modules/test_units.py
	$(PY) tests/modules/test_substances.py

test-regression:
	$(NODE) tests/regression/integer_answer_accepted.test.js
	$(PY) tests/regression/collision_rejected_by_generator.py
	$(NODE) tests/regression/one_stage_one_notebook_card.test.js
	$(NODE) tests/regression/random_clicker.test.js

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
