#!/usr/bin/env bash

ERRORS=0

echo "Checking PEP 420 namespace integrity..."
if [ -f src/mistralai/__init__.py ]; then
  echo "ERROR: PEP 420 violation - src/mistralai/__init__.py must not exist"
  ERRORS=1
else
  echo "-> PEP 420 namespace OK"
fi

echo "Running mypy..."
echo "-> running on examples"
uv run mypy examples/ \
  --exclude 'audio/' || ERRORS=1
echo "-> running on extra"
uv run mypy src/mistralai/extra/ || ERRORS=1
echo "-> running on hooks"
uv run mypy src/mistralai/client/_hooks/ \
  --exclude __init__.py --exclude sdkhooks.py --exclude types.py || ERRORS=1
echo "-> running on scripts"
uv run mypy scripts/ || ERRORS=1

echo "Running pyright..."
# TODO: Uncomment once the examples are fixed
# uv run pyright examples/ || ERRORS=1
echo "-> running on extra"
uv run pyright src/mistralai/extra/ || ERRORS=1
echo "-> running on hooks"
uv run pyright src/mistralai/client/_hooks/ || ERRORS=1
echo "-> running on scripts"
uv run pyright scripts/ || ERRORS=1

echo "Running ruff..."
echo "-> running on examples"
uv run ruff check examples/ || ERRORS=1
echo "-> running on extra"
uv run ruff check src/mistralai/extra/ || ERRORS=1
echo "-> running on hooks"
uv run ruff check src/mistralai/client/_hooks/ \
  --exclude __init__.py --exclude sdkhooks.py --exclude types.py || ERRORS=1
echo "-> running on scripts"
uv run ruff check scripts/ || ERRORS=1

if [ "$ERRORS" -ne 0 ]; then
  echo "❌ One or more linters failed"
  exit 1
else
  echo "✅ All linters passed"
fi
