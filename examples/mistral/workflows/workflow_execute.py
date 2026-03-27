#!/usr/bin/env python

import os

from mistralai.client import Mistral

WORKFLOW_NAME = "example-hello-world-workflow"


def main():
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key)

    # Execute workflow and wait for result using wait_for_result parameter
    response = client.workflows.execute_workflow(
        workflow_identifier=WORKFLOW_NAME,
        input={"document_title": "hello world"},
        wait_for_result=True,
        timeout_seconds=60.0,
    )

    print(f"Workflow: {response.workflow_name}")
    print(f"Execution ID: {response.execution_id}")
    print(f"Result: {response.result}")


if __name__ == "__main__":
    main()
