#!/usr/bin/env bash

export POETRY_PYPI_TOKEN_PYPI=${PYPI_TOKEN}

poetry run python scripts/prepare-readme.py

poetry publish --build --skip-existing
