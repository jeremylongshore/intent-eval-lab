# Phase A.0 baseline — codespace-runnable targets.
# Run from this directory: `make <target>`. Local box also works.
#
# Provider targets (ADR 030 — NVIDIA NIM is canonical free default):
#   arm-a-free / arm-b-free   — NVIDIA Llama-3.1-405B (zero cost, default)
#   arm-a-haiku / arm-b-haiku — Anthropic Haiku 4.5 ($1-2 spot-check)
#   arm-a-opus  / arm-b-opus  — Anthropic Opus 4.7  ($20 ceiling, full run)
#
# Bare `arm-a` / `arm-b` targets now default to the FREE path.
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
ROOT := $(shell git rev-parse --show-toplevel)
SCRIPTS := $(ROOT)/research/phase-a-0-baseline/scripts
SCORE := $(SCRIPTS)/score-fixture.py
MANIFEST := $(ROOT)/research/phase-a-0-baseline/corpus/manifest.json
RESULTS := $(ROOT)/research/phase-a-0-baseline/results/raw
FIXTURE_DIR := $(HOME)/000-projects/claude-code-plugins/tests/fixtures/skill-frontmatter

.PHONY: help check-env check-env-anthropic fixtures \
        arm-a arm-a-free arm-a-haiku arm-a-opus \
        arm-b arm-b-free arm-b-haiku arm-b-opus \
        clean-results

help:
	@echo "Targets:"
	@echo "  check-env        — verify env + validator present (no key required for free tier)"
	@echo "  check-env-anthropic — verify ANTHROPIC_API_KEY additionally"
	@echo "  fixtures         — generate expected.json for each manifest specimen"
	@echo ""
	@echo "  arm-a-free       — Arm A on NVIDIA Llama-3.1-405B (zero cost, default)"
	@echo "  arm-a-haiku      — Arm A on Anthropic Haiku 4.5 (\$$20 ceiling)"
	@echo "  arm-a-opus       — Arm A on Anthropic Opus 4.7  (\$$20 ceiling)"
	@echo "  arm-a            — alias for arm-a-free"
	@echo ""
	@echo "  arm-b-free       — Arm B on NVIDIA Llama-3.1-405B (zero cost, default)"
	@echo "  arm-b-haiku      — Arm B on Anthropic Haiku 4.5 (\$$20 ceiling)"
	@echo "  arm-b-opus       — Arm B on Anthropic Opus 4.7  (\$$20 ceiling)"
	@echo "  arm-b            — alias for arm-b-free"
	@echo ""
	@echo "  clean-results    — wipe results/raw/ (gitignored)"

check-env:
	@test -f $(SCORE) || (echo "score-fixture.py missing"; exit 1)
	@test -f $(MANIFEST) || (echo "manifest.json missing — run corpus sampler first"; exit 1)
	@echo "env OK (free-tier providers need NVIDIA_API_KEY or GROQ_API_KEY at runtime)"

check-env-anthropic: check-env
	@test -n "$$ANTHROPIC_API_KEY" || (echo "ANTHROPIC_API_KEY not set"; exit 1)
	@echo "Anthropic key present"

fixtures: check-env
	@python3 $(SCRIPTS)/build-fixtures.py \
		--manifest $(MANIFEST) \
		--out $(FIXTURE_DIR) \
		--score-script $(SCORE)

# ---------------------------------------------------------------------------
# Arm A targets
# ---------------------------------------------------------------------------

arm-a-free: check-env
	@python3 $(SCRIPTS)/run-arm-a.py \
		--manifest $(MANIFEST) \
		--out $(RESULTS) \
		--provider nvidia-llama-405b \
		--budget-ceiling-usd 0 \
		--k-sweep 0,3,8,16

arm-a-haiku: check-env-anthropic
	@python3 $(SCRIPTS)/run-arm-a.py \
		--manifest $(MANIFEST) \
		--out $(RESULTS) \
		--provider anthropic-haiku \
		--budget-ceiling-usd $${PHASE_A0_BUDGET_CEILING_USD:-20} \
		--k-sweep 0,3,8,16

arm-a-opus: check-env-anthropic
	@python3 $(SCRIPTS)/run-arm-a.py \
		--manifest $(MANIFEST) \
		--out $(RESULTS) \
		--provider anthropic-opus \
		--budget-ceiling-usd $${PHASE_A0_BUDGET_CEILING_USD:-20} \
		--k-sweep 0,3,8,16

# Default arm-a = free path (ADR 030)
arm-a: arm-a-free

# ---------------------------------------------------------------------------
# Arm B targets
# ---------------------------------------------------------------------------

arm-b-free: check-env
	@python3 $(SCRIPTS)/run-arm-b.py \
		--manifest $(MANIFEST) \
		--out $(RESULTS) \
		--provider nvidia-llama-405b \
		--budget-ceiling-usd 0

arm-b-haiku: check-env-anthropic
	@python3 $(SCRIPTS)/run-arm-b.py \
		--manifest $(MANIFEST) \
		--out $(RESULTS) \
		--provider anthropic-haiku \
		--budget-ceiling-usd $${PHASE_A0_BUDGET_CEILING_USD:-20}

arm-b-opus: check-env-anthropic
	@python3 $(SCRIPTS)/run-arm-b.py \
		--manifest $(MANIFEST) \
		--out $(RESULTS) \
		--provider anthropic-opus \
		--budget-ceiling-usd $${PHASE_A0_BUDGET_CEILING_USD:-20}

# Default arm-b = free path (ADR 030)
arm-b: arm-b-free

# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------

clean-results:
	rm -rf $(RESULTS)/
