import httpx


def test_azure_ocr_endpoint_strips_trailing_ocr_suffix():
    """
    If users copy the full OCR target URI from Azure AI Foundry (ending in /ocr),
    the SDK should not call /ocr/ocr.
    """
    from mistralai.azure.client import MistralAzure

    seen_urls: list[str] = []

    def on_request(request: httpx.Request) -> None:
        seen_urls.append(str(request.url))

    client = httpx.Client(
        params={"api-version": "2024-05-01-preview"},
        event_hooks={"request": [on_request]},
    )

    sdk = MistralAzure(
        api_key="dummy",
        server_url="https://example.com/providers/mistral/azure/ocr",
        client=client,
    )

    # Force request building; it will fail to connect, but the hook captures the URL.
    try:
        sdk.ocr.process(
            model="mistral-document-ai-2505",
            document={
                "type": "document_url",
                "document_url": "data:application/pdf;base64,AA==",
            },
            include_image_base64=False,
        )
    except Exception:
        pass

    assert seen_urls, "expected at least one outgoing request"
    assert "/ocr/ocr" not in seen_urls[0]
    assert seen_urls[0].startswith(
        "https://example.com/providers/mistral/azure/ocr?"
    ), seen_urls[0]

