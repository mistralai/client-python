from pathlib import Path

import pytest
from aiohttp import web
from gcloud.aio.auth import token as gcloud_auth_token
from pydantic import HttpUrl

from mistralai.extra.workflows import BlobStorageConfig, StorageProvider
from mistralai.extra.workflows.encoding.storage.blob_storage import get_blob_storage

METADATA_SERVER_TOKEN = "metadata-server-token"
METADATA_TOKEN_PATH = "/computeMetadata/v1/instance/service-accounts/default/token"
OFFLOADED_PAYLOAD = b"offloaded-payload"


@pytest.mark.asyncio
async def test_gcs_api_root_round_trips_payload_with_metadata_server_token(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    authorization_headers_seen_by_storage: list[str | None] = []
    blobs_by_name: dict[str, bytes] = {}

    async def serve_metadata_token(_request: web.Request) -> web.Response:
        return web.json_response(
            {"access_token": METADATA_SERVER_TOKEN, "expires_in": 3600}
        )

    async def upload_object(request: web.Request) -> web.Response:
        authorization_headers_seen_by_storage.append(
            request.headers.get("Authorization")
        )
        blob_name = request.query["name"]
        blobs_by_name[blob_name] = await request.read()
        return web.json_response({"name": blob_name, "selfLink": blob_name})

    async def download_object(request: web.Request) -> web.Response:
        authorization_headers_seen_by_storage.append(
            request.headers.get("Authorization")
        )
        return web.Response(body=blobs_by_name[request.match_info["name"]])

    fake_gcs_universe = web.Application()
    fake_gcs_universe.router.add_get(METADATA_TOKEN_PATH, serve_metadata_token)
    fake_gcs_universe.router.add_post(
        "/upload/storage/v1/b/{bucket}/o", upload_object
    )
    fake_gcs_universe.router.add_get(
        "/storage/v1/b/{bucket}/o/{name}", download_object
    )
    fake_gcs_universe_runner = web.AppRunner(fake_gcs_universe)
    await fake_gcs_universe_runner.setup()
    await web.TCPSite(fake_gcs_universe_runner, "127.0.0.1", 0).start()
    fake_gcs_universe_port = fake_gcs_universe_runner.addresses[0][1]
    fake_gcs_api_root = f"http://127.0.0.1:{fake_gcs_universe_port}"

    monkeypatch.setattr(
        gcloud_auth_token,
        "GCE_ENDPOINT_TOKEN",
        f"{fake_gcs_api_root}{METADATA_TOKEN_PATH}",
    )
    monkeypatch.delenv("GOOGLE_APPLICATION_CREDENTIALS", raising=False)
    monkeypatch.delenv("STORAGE_EMULATOR_HOST", raising=False)
    monkeypatch.delenv("CLOUDSDK_CONFIG", raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))

    gcs_storage_config = BlobStorageConfig(
        storage_provider=StorageProvider.GCS,
        bucket_id="payloads",
        api_root=HttpUrl(fake_gcs_api_root),
    )
    try:
        async with get_blob_storage(gcs_storage_config) as gcs_blob_storage:
            await gcs_blob_storage.upload_blob("payload-key", OFFLOADED_PAYLOAD)
            downloaded_payload = await gcs_blob_storage.get_blob("payload-key")
    finally:
        await fake_gcs_universe_runner.cleanup()

    assert downloaded_payload == OFFLOADED_PAYLOAD
    assert authorization_headers_seen_by_storage == [
        f"Bearer {METADATA_SERVER_TOKEN}",
        f"Bearer {METADATA_SERVER_TOKEN}",
    ]
