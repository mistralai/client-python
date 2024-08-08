#!/usr/bin/env bash

set -o pipefail  # Ensure pipeline failures are propagated

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

poetry run python scripts/prepare-readme.py

# Create temporary files for outputs and statuses
for cmd in compileall pylint mypy pyright; do
    output_files[$cmd]=$(mktemp)
    status_files[$cmd]=$(mktemp)
done

# Collect PIDs for background processes
declare -a pids

# Run commands in parallel using temporary files
echo "Running python -m compileall"
run_command 'poetry run python -m compileall -q . && echo "Success"' 'compileall' "${output_files[compileall]}" "${status_files[compileall]}"
pids+=($!)

echo "Running pylint"
run_command 'poetry run pylint src' 'pylint' "${output_files[pylint]}" "${status_files[pylint]}"
pids+=($!)

echo "Running mypy"
run_command 'poetry run mypy src' 'mypy' "${output_files[mypy]}" "${status_files[mypy]}"
pids+=($!)

echo "Running pyright (optional)"
run_command 'if command -v pyright > /dev/null 2>&1; then pyright src; else echo "pyright not found, skipping"; fi' 'pyright' "${output_files[pyright]}" "${status_files[pyright]}"
pids+=($!)

# Wait for all processes to complete
echo "Waiting for processes to complete"
for pid in "${pids[@]}"; do
    wait "$pid"
done

# Print output sequentially and check for failures
failed=false
for key in "${!output_files[@]}"; do
    echo "--- Output from Command: $key ---"
    echo
    cat "${output_files[$key]}"
    echo  # Empty line for separation
    echo "--- End of Output from Command: $key ---"
    echo

    exit_status=$(cat "${status_files[$key]}")
    if [ "$exit_status" -ne 0 ]; then
        echo "Command $key failed with exit status $exit_status" >&2
        failed=true
    fi
done

# Clean up temporary files
for tmp_file in "${output_files[@]}" "${status_files[@]}"; do
    rm -f "$tmp_file"
done

if $failed; then
    echo "One or more commands failed." >&2
    exit 1
else
    echo "All commands completed successfully."
    exit 0
fi
