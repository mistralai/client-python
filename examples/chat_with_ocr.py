from mistralai import Mistral
import os
import json

MISTRAL_7B_PDF_URL = "https://arxiv.org/pdf/2310.06825"
MIXTRAL_OF_EXPERTS_PDF_URL = "https://arxiv.org/pdf/2401.04088"
MOE_FILENAME = "mixtral_of_experts.pdf"

def ocr_with_url():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    # Using an URL
    pdf_response = client.ocr.process(document={
        "document_url": MISTRAL_7B_PDF_URL,
        "type": "document_url",
        "document_name": "mistral-7b-pdf",
    }, model="mistral-ocr-latest", include_image_base64=True)

    # Print the parsed PDF
    response_dict = json.loads(pdf_response.model_dump_json())
    json_string = json.dumps(response_dict, indent=4)
    print(json_string)


def ocr_with_file():
    from pathlib import Path
    import urllib.request

    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    pdf_file = Path(MOE_FILENAME)
    # Download the file if it doesn't exist
    if not pdf_file.is_file():
        urllib.request.urlretrieve(MIXTRAL_OF_EXPERTS_PDF_URL, MOE_FILENAME)

    uploaded_file = client.files.upload(
        file={
            "file_name": pdf_file.stem,
            "content": pdf_file.read_bytes(),
        },
        purpose="ocr",
    )

    signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)

    pdf_response = client.ocr.process(document={
        "document_url": signed_url.url,
        "type": "document_url",
        "document_name": "mistral-7b-pdf",
    }, model="mistral-ocr-latest", include_image_base64=True)

    # Print the parsed PDF
    response_dict = json.loads(pdf_response.model_dump_json())
    json_string = json.dumps(response_dict, indent=4)
    print(json_string)

    # Remove the file
    pdf_file.unlink()


if __name__ == "__main__":
    ocr_with_url()
    ocr_with_file()
