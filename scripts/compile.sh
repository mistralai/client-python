#!/usr/bin/env bash

set -o pipefail  # Ensure pipeline failures are propagated

# Define color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Use temporary files to store outputs and exit statuses
declare -A output_files
declare -A status_files

# Function to run a command with temporary output and status files
run_command() {
    local cmd="$1"
    local key="$2"
    local output_file="$3"
    local status_file="$4"

    # Run the command and store output and exit status
    {
        eval "$cmd"
        echo $? > "$status_file"
    } &> "$output_file" &
}

echo -e "${BLUE}Running prepare-readme.py${NC}"
poetry run python scripts/prepare-readme.py

# Create temporary files for outputs and statuses
for cmd in compileall pylint mypy pyright; do
    output_files[$cmd]=$(mktemp)
    status_files[$cmd]=$(mktemp)
done

# Collect PIDs for background processes
declare -a pids

# Run commands in parallel using temporary files
echo -e "${YELLOW}Running python -m compileall${NC}"
run_command 'poetry run python -m compileall -q . && echo "Success"' 'compileall' "${output_files[compileall]}" "${status_files[compileall]}"
pids+=($!)

echo -e "${YELLOW}Running pylint${NC}"
run_command 'poetry run pylint src' 'pylint' "${output_files[pylint]}" "${status_files[pylint]}"
pids+=($!)

echo -e "${YELLOW}Running mypy${NC}"
run_command 'poetry run mypy src' 'mypy' "${output_files[mypy]}" "${status_files[mypy]}"
pids+=($!)

echo -e "${YELLOW}Running pyright (optional)${NC}"
run_command 'if command -v pyright > /dev/null 2>&1; then pyright src; else echo "pyright not found, skipping"; fi' 'pyright' "${output_files[pyright]}" "${status_files[pyright]}"
pids+=($!)

# Wait for all processes to complete
echo -e "${BLUE}Waiting for processes to complete${NC}"
for pid in "${pids[@]}"; do
    wait "$pid"
done

# Print output sequentially and check for failures
failed=false
for key in "${!output_files[@]}"; do
    echo -e "${BLUE}--- Output from Command: $key ---${NC}"
    echo
    cat "${output_files[$key]}"
    echo  # Empty line for separation
    echo -e "${BLUE}--- End of Output from Command: $key ---${NC}"
    echo

    exit_status=$(cat "${status_files[$key]}")
    if [ "$exit_status" -ne 0 ]; then
        echo -e "${RED}Command $key failed with exit status $exit_status${NC}" >&2
        failed=true
    fi
done

# Clean up temporary files
for tmp_file in "${output_files[@]}" "${status_files[@]}"; do
    rm -f "$tmp_file"
done

if $failed; then
    echo -e "${RED}One or more commands failed.${NC}" >&2
    exit 1
else
    echo -e "${GREEN}All commands completed successfully.${NC}"
    exit 0
fi
