#!/bin/bash

# Default retry count
RETRY_COUNT=3

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --no-extra-dep)
            NO_EXTRA_DEP=true
            shift
            ;;
        --retry-count)
            RETRY_COUNT="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [--no-extra-dep] [--retry-count N]"
            echo "  --no-extra-dep: Exclude files that require extra dependencies"
            echo "  --retry-count N: Number of retries for each test (default: 3)"
            echo "  --help: Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# List of files to exclude
exclude_files=(
 "examples/mistral/chat/chatbot_with_streaming.py"
 "examples/mistral/agents/async_conversation_run_mcp_remote_auth.py"
 "examples/mistral/jobs/async_jobs_chat.py"
 "examples/mistral/classifier/async_classifier.py"
 "examples/mistral/mcp_servers/sse_server.py"
 "examples/mistral/mcp_servers/stdio_server.py"
 "examples/mistral/agents/async_conversation_run_stream.py"
 "examples/mistral/agents/async_conversation_run_mcp.py"
 "examples/mistral/agents/async_conversation_run_mcp_remote.py"
)

# Check if the no-extra-dep flag is set
if [ "$NO_EXTRA_DEP" = true ]; then
    # Add more files to the exclude list
    exclude_files+=(
      "examples/mistral/agents/async_conversation_run_mcp_remote.py"
      "examples/mistral/agents/async_conversation_run_stream.py"
      "examples/mistral/agents/async_conversation_run.py"
    )
fi

failed=0

# Function to run a test with retries
run_test_with_retries() {
    local file="$1"
    local attempt=1
    
    while [ $attempt -le $RETRY_COUNT ]; do
        echo "Running $file (attempt $attempt/$RETRY_COUNT)"
        
        # Run the script and capture the exit status
        if python3 "$file" > /dev/null 2>&1; then
            echo "Success"
            return 0
        else
            if [ $attempt -lt $RETRY_COUNT ]; then
                echo "Failed (attempt $attempt/$RETRY_COUNT), retrying..."
                sleep 1  # Brief pause before retry
            else
                echo "Failed after $RETRY_COUNT attempts"
                return 1
            fi
        fi
        
        attempt=$((attempt + 1))
    done
}

for file in examples/mistral/**/*.py; do
    # Check if the file is not in the exclude list
    if [ -f "$file" ] && [[ ! " ${exclude_files[@]} " =~ " $file " ]]; then
        if ! run_test_with_retries "$file"; then
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
