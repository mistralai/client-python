#!/usr/bin/env bash
export UV_PUBLISH_TOKEN=${PYPI_TOKEN}

uv run python scripts/prepare_readme.py -- uv build
uv publish
