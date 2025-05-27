#!/usr/bin/env bash

set -e

ERRORS=0

echo "Running mypy..."
# TODO: Uncomment once the examples are fixed
# poetry run mypy examples/ || ERRORS=1
echo "-> running on extra"
poetry run mypy src/mistralai/extra/ || ERRORS=1
echo "-> running on hooks"
poetry run mypy src/mistralai/_hooks/ \
--exclude __init__.py --exclude sdkhooks.py --exclude types.py || ERRORS=1

echo "Running pyright..."
# TODO: Uncomment once the examples are fixed
# poetry run pyright examples/ || ERRORS=1
echo "-> running on extra"
poetry run pyright src/mistralai/extra/ || ERRORS=1
echo "-> running on hooks"
poetry run pyright src/mistralai/_hooks/ || ERRORS=1

echo "Running ruff..."
echo "-> running on examples"
poetry run ruff check examples/ || ERRORS=1
echo "-> running on extra"
poetry run ruff check src/mistralai/extra/ || ERRORS=1
echo "-> running on hooks"
poetry run ruff check src/mistralai/_hooks/ \
--exclude __init__.py --exclude sdkhooks.py --exclude types.py || ERRORS=1

if [ "$ERRORS" -ne 0 ]; then
echo "❌ One or more linters failed"
exit 1
else
echo "✅ All linters passed"
fi
