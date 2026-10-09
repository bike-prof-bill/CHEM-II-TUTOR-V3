# Same commands locally and in CI. Repository root = the former build_v3_ch10_cc folder.
PY   ?= python3
NODE ?= node

.PHONY: test test-gen test-verify test-modules test-regression gen-check content-check baseline purity generate

test: test-gen test-verify test-modules test-regression gen-check content-check

test-gen:
	$(PY) test_ch10_cc.py

test-verify:
	$(NODE) gas/test_core.js

test-modules:
	$(NODE) tests/modules/units.test.js
	$(PY) tests/modules/test_units.py

test-regression:
	$(NODE) tests/regression/integer_answer_accepted.test.js
	$(PY) tests/regression/collision_rejected_by_generator.py

generate:
	$(PY) run.py ch10_cc --per-kind 3 --seed 1

gen-check:
	sh scripts/check_generated.sh

baseline:
	$(PY) scripts/snapshot_content.py content/BASELINE_authored.txt

content-check:
	sh scripts/check_content.sh

purity:
	sh scripts/check_shell_purity.sh
