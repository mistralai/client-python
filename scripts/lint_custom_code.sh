#!/usr/bin/env bash

ERRORS=0

echo "Running mypy..."
# TODO: Uncomment once the examples are fixed
# uv run mypy examples/ || ERRORS=1
echo "-> running on extra"
uv run mypy src/mistralai/extra/ || ERRORS=1
echo "-> running on hooks"
uv run mypy src/mistralai/_hooks/ \
  --exclude __init__.py --exclude sdkhooks.py --exclude types.py || ERRORS=1

echo "Running pyright..."
# TODO: Uncomment once the examples are fixed
# uv run pyright examples/ || ERRORS=1
echo "-> running on extra"
uv run pyright src/mistralai/extra/ || ERRORS=1
echo "-> running on hooks"
uv run pyright src/mistralai/_hooks/ || ERRORS=1

echo "Running ruff..."
echo "-> running on examples"
uv run ruff check examples/ || ERRORS=1
echo "-> running on extra"
uv run ruff check src/mistralai/extra/ || ERRORS=1
echo "-> running on hooks"
uv run ruff check src/mistralai/_hooks/ \
  --exclude __init__.py --exclude sdkhooks.py --exclude types.py || ERRORS=1

if [ "$ERRORS" -ne 0 ]; then
  echo "❌ One or more linters failed"
  exit 1
else
  echo "✅ All linters passed"
fi
