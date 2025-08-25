#!/usr/bin/env bash

export POETRY_PYPI_TOKEN_PYPI=${PYPI_TOKEN}

poetry publish --build --skip-existing
