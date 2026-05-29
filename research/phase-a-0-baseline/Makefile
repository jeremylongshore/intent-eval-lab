# Phase A.0 baseline — codespace-runnable targets.
# Run from this directory: `make <target>`. Local box also works.
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
ROOT := $(shell git rev-parse --show-toplevel)
SCORE := $(ROOT)/research/phase-a-0-baseline/scripts/score-fixture.py
MANIFEST := $(ROOT)/research/phase-a-0-baseline/corpus/manifest.json
FIXTURE_DIR := $(HOME)/000-projects/claude-code-plugins/tests/fixtures/skill-frontmatter

.PHONY: help check-env fixtures arm-a arm-b clean-results

help:
	@echo "Targets:"
	@echo "  check-env   — verify ANTHROPIC_API_KEY + validator present"
	@echo "  fixtures    — generate expected.json for each manifest specimen"
	@echo "  arm-a       — run naive-Opus arm (requires ANTHROPIC_API_KEY)"
	@echo "  arm-b       — run proposed-Refiner arm"
	@echo "  clean-results — wipe results/raw/ (gitignored)"

check-env:
	@test -n "$$ANTHROPIC_API_KEY" || (echo "ANTHROPIC_API_KEY not set"; exit 1)
	@test -f $(SCORE) || (echo "score-fixture.py missing"; exit 1)
	@test -f $(MANIFEST) || (echo "manifest.json missing — run corpus sampler first"; exit 1)
	@echo "env OK"

fixtures: check-env
	@python3 $(ROOT)/research/phase-a-0-baseline/scripts/build-fixtures.py \
		--manifest $(MANIFEST) \
		--out $(FIXTURE_DIR) \
		--score-script $(SCORE)

arm-a: check-env
	@python3 $(ROOT)/research/phase-a-0-baseline/scripts/run-arm-a.py \
		--manifest $(MANIFEST) \
		--out $(ROOT)/research/phase-a-0-baseline/results/raw/arm-a/ \
		--k-sweep 0,3,8,16 \
		--budget-ceiling-usd $${PHASE_A0_BUDGET_CEILING_USD:-200}

arm-b: check-env
	@python3 $(ROOT)/research/phase-a-0-baseline/scripts/run-arm-b.py \
		--manifest $(MANIFEST) \
		--out $(ROOT)/research/phase-a-0-baseline/results/raw/arm-b/ \
		--budget-ceiling-usd $${PHASE_A0_BUDGET_CEILING_USD:-200}

clean-results:
	rm -rf $(ROOT)/research/phase-a-0-baseline/results/raw/
