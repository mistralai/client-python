#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# Run all test suites for the Mistral Python SDK.
#
# Usage:
#   ./scripts/run_all_tests.sh                              # unit + parity + contract (integration skipped if no keys)
#   MISTRAL_API_KEY=xxx ./scripts/run_all_tests.sh          # also runs main SDK integration
#   ./scripts/run_all_tests.sh --mistral-api-key xxx        # same, via argument
#   ./scripts/run_all_tests.sh --azure-api-key xxx          # also runs Azure integration
#   ./scripts/run_all_tests.sh --gcp-project-id xxx         # also runs GCP integration
#
# All flags can be combined. Environment variables and arguments can be mixed;
# arguments take precedence.
# ---------------------------------------------------------------------------

# -- Parse arguments --------------------------------------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --mistral-api-key)  export MISTRAL_API_KEY="$2";  shift 2 ;;
        --azure-api-key)    export AZURE_API_KEY="$2";    shift 2 ;;
        --azure-endpoint)   export AZURE_ENDPOINT="$2";   shift 2 ;;
        --azure-model)      export AZURE_MODEL="$2";      shift 2 ;;
        --gcp-project-id)   export GCP_PROJECT_ID="$2";   shift 2 ;;
        --gcp-region)       export GCP_REGION="$2";       shift 2 ;;
        --gcp-model)        export GCP_MODEL="$2";        shift 2 ;;
        -h|--help)
            sed -n '4,15p' "$0"   # print the usage block above
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# -- Helpers ----------------------------------------------------------------
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}✓ $1${NC}"; }
fail() { echo -e "${RED}✗ $1${NC}"; FAILURES=$((FAILURES + 1)); }
skip() { echo -e "${YELLOW}⊘ $1 (skipped)${NC}"; }

FAILURES=0

# -- Mock server management ------------------------------------------------
MOCKSERVER_PID=""
MOCKSERVER_CONTAINER=""
MOCKSERVER_STARTED_BY_US=false

cleanup_mockserver() {
    if [ "$MOCKSERVER_STARTED_BY_US" = true ]; then
        echo ""
        echo "Cleaning up mock server..."
        if [ -n "$MOCKSERVER_CONTAINER" ]; then
            docker stop "$MOCKSERVER_CONTAINER" &>/dev/null || true
        fi
        if [ -n "$MOCKSERVER_PID" ]; then
            kill "$MOCKSERVER_PID" &>/dev/null || true
        fi
    fi
}

# Ensure cleanup on exit (normal or crash)
trap cleanup_mockserver EXIT

start_mockserver_if_needed() {
    # Check if mock server is already running
    if curl -sf http://localhost:18080/_mockserver/health &>/dev/null; then
        echo "Mock server already running on port 18080 (reusing)"
        return 0
    fi

    # Try Docker first (if available)
    if command -v docker &>/dev/null && docker info &>/dev/null 2>&1; then
        echo "Starting mock server via Docker..."
        MOCKSERVER_CONTAINER="mistral-mockserver-$$"

        if docker build -t mistral-mockserver tests/mockserver -q &>/dev/null; then
            docker run -d -p 18080:18080 --name "$MOCKSERVER_CONTAINER" --rm mistral-mockserver &>/dev/null
            sleep 2
            if curl -sf http://localhost:18080/_mockserver/health &>/dev/null; then
                MOCKSERVER_STARTED_BY_US=true
                return 0
            fi
        fi
        echo "Docker failed, trying Go..."
    fi

    # Fall back to Go
    if command -v go &>/dev/null; then
        echo "Starting mock server via Go..."
        (cd tests/mockserver && go run . -address :18080) &
        MOCKSERVER_PID=$!
        sleep 3
        if curl -sf http://localhost:18080/_mockserver/health &>/dev/null; then
            MOCKSERVER_STARTED_BY_US=true
            return 0
        fi
        echo "Go mock server failed to start"
    fi

    return 1
}

echo "========================================"
echo " Running all test suites"
echo "========================================"
echo ""

# -- 1. Extra package unit tests -------------------------------------------
echo "── Extra package unit tests ──"
if uv run python3 -m unittest discover -s src/mistralai/extra/tests -t src 2>&1; then
    pass "Extra package tests"
else
    fail "Extra package tests"
fi
echo ""

# -- 2. Main SDK unit tests ------------------------------------------------
echo "── Main SDK unit tests ──"
if uv run pytest tests/unit/ -v --tb=short; then
    pass "Main SDK unit tests"
else
    fail "Main SDK unit tests"
fi
echo ""

# -- 3. Azure unit tests ---------------------------------------------------
echo "── Azure unit tests ──"
if uv run pytest packages/azure/tests/unit/ -v --tb=short; then
    pass "Azure unit tests"
else
    fail "Azure unit tests"
fi
echo ""

# -- 4. GCP unit tests -----------------------------------------------------
echo "── GCP unit tests ──"
if uv run pytest packages/gcp/tests/unit/ -v --tb=short; then
    pass "GCP unit tests"
else
    fail "GCP unit tests"
fi
echo ""

# -- 5. Azure parity tests -------------------------------------------------
echo "── Azure parity tests ──"
if uv run pytest packages/azure/tests/test_azure_v2_parity.py -v; then
    pass "Azure parity tests"
else
    fail "Azure parity tests"
fi
echo ""

# -- 6. GCP parity tests ---------------------------------------------------
echo "── GCP parity tests ──"
if uv run pytest packages/gcp/tests/test_gcp_v2_parity.py -v; then
    pass "GCP parity tests"
else
    fail "GCP parity tests"
fi
echo ""

# -- 7. Speakeasy contract tests -------------------------------------------
echo "── Speakeasy contract tests ──"

if start_mockserver_if_needed; then
    if uv run pytest tests/ --ignore=tests/unit/ -m "not integration" --tb=short; then
        pass "Speakeasy contract tests (main)"
    else
        fail "Speakeasy contract tests (main)"
    fi
else
    skip "Speakeasy contract tests (no Docker or Go available)"
fi
echo ""

# -- 8. Integration tests --------------------------------------------------
# Each test file uses pytest.mark.skipif internally, so pytest will skip
# gracefully when the required env var is not set.
echo "── Integration tests ──"

if [ -n "${MISTRAL_API_KEY:-}" ]; then
    if uv run pytest tests/test_integration.py -v; then
        pass "Main SDK integration tests"
    else
        fail "Main SDK integration tests"
    fi
else
    skip "Main SDK integration (MISTRAL_API_KEY not set)"
fi

if [ -n "${AZURE_API_KEY:-}" ]; then
    if uv run pytest packages/azure/tests/test_azure_integration.py -v; then
        pass "Azure integration tests"
    else
        fail "Azure integration tests"
    fi
else
    skip "Azure integration (AZURE_API_KEY not set)"
fi

if [ -n "${GCP_PROJECT_ID:-}" ]; then
    if uv run pytest packages/gcp/tests/test_gcp_integration.py -v; then
        pass "GCP integration tests"
    else
        fail "GCP integration tests"
    fi
else
    skip "GCP integration (GCP_PROJECT_ID not set)"
fi

echo ""
echo "========================================"
if [ $FAILURES -eq 0 ]; then
    echo -e "${GREEN} All test suites passed${NC}"
else
    echo -e "${RED} $FAILURES test suite(s) failed${NC}"
    exit 1
fi
