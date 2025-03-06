from mistralai import Mistral
import os
import json

MISTRAL_7B_PDF = "https://arxiv.org/pdf/2310.06825"

def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    pdf_response = client.ocr.process(document={
        "document_url": MISTRAL_7B_PDF,
        "type": "document_url",
        "document_name": "mistral-7b-pdf",
    }, model="mistral-ocr-latest", include_image_base64=True)

    response_dict = json.loads(pdf_response.model_dump_json())
    json_string = json.dumps(response_dict, indent=4)
    print(json_string)


if __name__ == "__main__":
    main()
