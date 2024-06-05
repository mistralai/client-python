.PHONY: lint

lint:
	poetry run ruff check --fix .
	poetry run ruff format .
	poetry run mypy .
