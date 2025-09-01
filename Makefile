.PHONY: run-server run-client lint type test fmt workflow

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
