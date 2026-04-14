#!/usr/bin/env bash

ERRORS=0

echo "Checking PEP 420 namespace integrity..."
if [ -f src/mistralai/__init__.py ]; then
  echo "ERROR: PEP 420 violation - src/mistralai/__init__.py must not exist"
  ERRORS=1
else
  echo "-> PEP 420 namespace OK (core)"
fi
if [ -f packages/azure/src/mistralai/__init__.py ]; then
  echo "ERROR: PEP 420 violation - packages/azure/src/mistralai/__init__.py must not exist"
  ERRORS=1
else
  echo "-> PEP 420 namespace OK (azure)"
fi
if [ -f packages/gcp/src/mistralai/__init__.py ]; then
  echo "ERROR: PEP 420 violation - packages/gcp/src/mistralai/__init__.py must not exist"
  ERRORS=1
else
  echo "-> PEP 420 namespace OK (gcp)"
fi

echo "Running mypy..."
echo "-> running on examples"
uv run mypy examples/ \
  --exclude 'audio/' || ERRORS=1
echo "-> running on extra"
uv run --all-extras mypy src/mistralai/extra/ || ERRORS=1
echo "-> running on hooks"
uv run mypy src/mistralai/client/_hooks/ \
  --exclude __init__.py --exclude sdkhooks.py --exclude types.py || ERRORS=1
echo "-> running on azure hooks"
uv run mypy packages/azure/src/mistralai/azure/client/_hooks/ \
  --exclude __init__.py --exclude sdkhooks.py --exclude types.py || ERRORS=1
echo "-> running on azure sdk"
uv run mypy packages/azure/src/mistralai/azure/client/sdk.py || ERRORS=1
echo "-> running on gcp hooks"
uv run mypy packages/gcp/src/mistralai/gcp/client/_hooks/ \
  --exclude __init__.py --exclude sdkhooks.py --exclude types.py || ERRORS=1
echo "-> running on gcp sdk"
uv run mypy packages/gcp/src/mistralai/gcp/client/sdk.py || ERRORS=1
echo "-> running on scripts"
uv run mypy scripts/ || ERRORS=1

echo "Running pyright..."
# TODO: Uncomment once the examples are fixed
# uv run pyright examples/ || ERRORS=1
echo "-> running on extra"
uv run --all-extras pyright src/mistralai/extra/ || ERRORS=1
echo "-> running on hooks"
uv run pyright src/mistralai/client/_hooks/ || ERRORS=1
echo "-> running on azure hooks"
uv run pyright packages/azure/src/mistralai/azure/client/_hooks/ || ERRORS=1
echo "-> running on azure sdk"
uv run pyright packages/azure/src/mistralai/azure/client/sdk.py || ERRORS=1
echo "-> running on gcp hooks"
uv run pyright packages/gcp/src/mistralai/gcp/client/_hooks/ || ERRORS=1
echo "-> running on gcp sdk"
uv run pyright packages/gcp/src/mistralai/gcp/client/sdk.py || ERRORS=1
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
echo "-> running on azure hooks"
uv run ruff check packages/azure/src/mistralai/azure/client/_hooks/ \
  --exclude __init__.py --exclude sdkhooks.py --exclude types.py || ERRORS=1
echo "-> running on azure sdk"
uv run ruff check packages/azure/src/mistralai/azure/client/sdk.py || ERRORS=1
echo "-> running on gcp hooks"
uv run ruff check packages/gcp/src/mistralai/gcp/client/_hooks/ \
  --exclude __init__.py --exclude sdkhooks.py --exclude types.py || ERRORS=1
echo "-> running on gcp sdk"
uv run ruff check packages/gcp/src/mistralai/gcp/client/sdk.py || ERRORS=1
echo "-> running on scripts"
uv run ruff check scripts/ || ERRORS=1

if [ "$ERRORS" -ne 0 ]; then
  echo "❌ One or more linters failed"
  exit 1
else
  echo "✅ All linters passed"
fi
