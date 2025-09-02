.PHONY: run-server run-client lint type test fmt workflow docs-cov docs-cov-gate

PYTHONPATH := src

run-server:
	PYTHONPATH=$(PYTHONPATH) python -m tec.server.main

run-client:
	PYTHONPATH=$(PYTHONPATH) python -m tec.client.tcod_client

lint:
	ruff format src tests
	ruff check --fix src tests
	mypy src tests

type:
	mypy src tests

test:
	pytest -q

fmt:
	ruff format src tests

workflow:
	@${PAGER:-less} docs/WORKFLOW.md

# Generate report + badge without failing locally (so the target always completes).
docs-cov:
	mkdir -p docs/assets
	# Write a text report (never fail this step)
	interrogate -c pyproject.toml --fail-under=0 -o docs/assets/interrogate.txt src/tec || true
	# Generate the SVG badge (never fail this step)
	interrogate -c pyproject.toml --fail-under=0 --generate-badge docs/assets/interrogate.svg src/tec || true
	@echo "Wrote docs/assets/interrogate.txt and docs/assets/interrogate.svg"

# Strict gate: fail if coverage drops below the threshold in pyproject.toml
docs-cov-gate:
	interrogate -c pyproject.toml src/tec
