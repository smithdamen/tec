.PHONY: run-server run-client lint type test fmt

run-server:
	python -m tec.server.main

run-client:
	python -m tec.client.tcod_client

lint:
	ruff format src
	ruff check --fix src
	mypy src

type:
	mypy src

test:
	pytest -q

fmt:
	ruff format src
