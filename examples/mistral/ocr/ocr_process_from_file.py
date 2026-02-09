from mistralai.client import Mistral
import os
import json
from pathlib import Path
import urllib.request

MIXTRAL_OF_EXPERTS_PDF_URL = "https://arxiv.org/pdf/2401.04088"
MOE_FILENAME = "mixtral_of_experts.pdf"


def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)
    pdf_file = Path(MOE_FILENAME)

    # Download the file if it doesn't exist
    if not pdf_file.is_file():
        urllib.request.urlretrieve(MIXTRAL_OF_EXPERTS_PDF_URL, MOE_FILENAME)

    # Upload the file
    uploaded_file = client.files.upload(
        file={
            "file_name": pdf_file.stem,
            "content": pdf_file.read_bytes(),
        },
        purpose="ocr",
    )

    pdf_response = client.ocr.process(document={
        "type": "file",
        "file_id": uploaded_file.id,
    }, model="mistral-ocr-latest", include_image_base64=True)

    # Print the parsed PDF
    response_dict = json.loads(pdf_response.model_dump_json())
    json_string = json.dumps(response_dict, indent=4)
    print(json_string)

    # Remove the file
    pdf_file.unlink()


if __name__ == "__main__":
    main()
