#!/bin/bash

# List of files to exclude
exclude_files=(
 "examples/chatbot_with_streaming.py"
 "examples/async_conversation_run_mcp_remote_auth.py"
)

# Check if the first argument is "no-extra-dep" then remove all the files that require the extra dependencies
if [ "$1" = "--no-extra-dep" ]; then
    # Add more files to the exclude list
    exclude_files+=(
      "examples/async_conversation_run_mcp_remote.py"
      "examples/async_conversation_run_mcp.py"
      "examples/async_conversation_run_stream.py"
      "examples/async_conversation_run.py"
    )
fi

failed=0

for file in examples/*.py; do
    # Check if the file is not in the exclude list
    if [ -f "$file" ] && [[ ! " ${exclude_files[@]} " =~ " $file " ]]; then
        echo "Running $file"
        # Run the script and capture the exit status
        if python3 "$file" > /dev/null; then
            echo "Success"
        else
            echo "Failed"
            failed=1
        fi
    else
      echo "Skipped $file"
    fi
done

# If one of the example scripts failed, then exit
if [ $failed -ne 0 ]; then
    exit 1
fi
