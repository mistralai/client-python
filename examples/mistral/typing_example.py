#!/usr/bin/env python
"""
Example demonstrating typed SDK usage.

This file is type-checked by mypy in CI to ensure the SDK types are correct.
"""

import os

from mistralai.client import Mistral
from mistralai.client.models import (
    # Entity schemas - the actual resources
    BatchJob,
    FileObject,
    Library,
    # Response schemas - wrappers for list/delete operations
    ListBatchJobsResponse,
    ListFilesResponse,
    ListLibrariesResponse,
    # Request schemas exist but users typically use kwargs instead
)


def demo_batch_jobs(client: Mistral) -> None:
    """Demonstrate BatchJob typing."""
    # list() returns ListBatchJobsResponse
    response: ListBatchJobsResponse = client.batch.jobs.list(page_size=10)

    # response.data is List[BatchJob] (may be None)
    jobs: list[BatchJob] = response.data or []

    for job in jobs:
        # BatchJob has typed attributes
        job_id: str = job.id
        status: str = job.status
        created_at: int = job.created_at
        print(f"Job {job_id}: {status} (created: {created_at})")


def demo_files(client: Mistral) -> None:
    """Demonstrate File typing."""
    # list() returns ListFilesResponse
    response: ListFilesResponse = client.files.list(page_size=10)

    # response.data is List[FileObject]
    files: list[FileObject] = response.data

    for file in files:
        # FileObject has typed attributes
        file_id: str = file.id
        filename: str = file.filename
        size: int = file.size_bytes
        print(f"File {file_id}: {filename} ({size} bytes)")


def demo_libraries(client: Mistral) -> None:
    """Demonstrate Library typing."""
    # list() returns ListLibrariesResponse
    response: ListLibrariesResponse = client.libraries.list()

    # response.data is List[Library]
    libraries: list[Library] = response.data

    for lib in libraries:
        # Library has typed attributes
        lib_id: str = str(lib.id)
        name: str = lib.name
        print(f"Library {lib_id}: {name}")


def main() -> None:
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("MISTRAL_API_KEY not set, skipping runtime demo")
        return

    client = Mistral(api_key=api_key)

    print("=== Batch Jobs ===")
    demo_batch_jobs(client)

    print("\n=== Files ===")
    demo_files(client)

    print("\n=== Libraries ===")
    demo_libraries(client)


if __name__ == "__main__":
    main()
