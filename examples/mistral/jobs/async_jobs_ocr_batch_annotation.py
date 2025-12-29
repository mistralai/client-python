#!/usr/bin/env python
import asyncio
import json
import os
from typing import List

import httpx
from pydantic import BaseModel, Field

from mistralai import Mistral
from mistralai.extra import response_format_from_pydantic_model
from mistralai.models import File

SAMPLE_PDF_URL = "https://arxiv.org/pdf/2401.04088"


class Table(BaseModel):
    name: str = Field(description="The name or title of the table")


class TableExtraction(BaseModel):
    tables: List[Table] = Field(description="List of tables found in the document")


def create_ocr_batch_request(custom_id: str, document_url: str) -> dict:
    """Batch requests require custom_id and body wrapper."""
    response_format = response_format_from_pydantic_model(TableExtraction)
    return {
        "custom_id": custom_id,
        "body": {
            "document": {"type": "document_url", "document_url": document_url},
            "document_annotation_format": response_format.model_dump(
                by_alias=True, exclude_none=True
            ),
            "pages": [0, 1, 2, 3, 4, 5, 6, 7],
            "include_image_base64": False,
        },
    }


async def main():
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

    document_urls = [SAMPLE_PDF_URL]

    batch_requests = [
        json.dumps(create_ocr_batch_request(custom_id=str(i), document_url=url))
        for i, url in enumerate(document_urls)
    ]
    batch_content = "\n".join(batch_requests)

    print("Uploading batch file...")
    batch_file = await client.files.upload_async(
        file=File(file_name="ocr_batch.jsonl", content=batch_content.encode()),
        purpose="batch",
    )
    print(f"Batch file uploaded: {batch_file.id}")

    print("Creating batch job...")
    created_job = await client.batch.jobs.create_async(
        model="mistral-ocr-latest",
        input_files=[batch_file.id],
        endpoint="/v1/ocr",
    )
    print(f"Batch job created: {created_job.id}")

    print("Waiting for job completion...")
    job = await client.batch.jobs.get_async(job_id=created_job.id)
    while job.status not in ["SUCCESS", "FAILED", "CANCELLED"]:
        print(f"Status: {job.status}")
        await asyncio.sleep(5)
        job = await client.batch.jobs.get_async(job_id=created_job.id)

    print(f"Job status: {job.status}")

    async with httpx.AsyncClient() as http_client:
        if job.output_file:
            signed_url = await client.files.get_signed_url_async(
                file_id=job.output_file
            )
            response = await http_client.get(signed_url.url)
            for line in response.content.decode().strip().split("\n"):
                result = json.loads(line)
                annotation = result["response"]["body"].get("document_annotation")
                if annotation:
                    tables = TableExtraction.model_validate_json(annotation)
                    for table in tables.tables:
                        print(table.name)

        if job.error_file:
            signed_url = await client.files.get_signed_url_async(file_id=job.error_file)
            response = await http_client.get(signed_url.url)
            print("Errors:", response.content.decode())

    print("\nCleaning up...")
    await client.files.delete_async(file_id=batch_file.id)
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
