#!/usr/bin/env bash

export UV_PUBLISH_TOKEN=${PYPI_TOKEN}

uv build
uv publish
