import sys
from pathlib import Path
import httpx

# Add the mistralai_gcp package to the path for imports
gcp_package_path = Path(__file__).parent.parent.parent.parent.parent / "packages" / "mistralai_gcp" / "src"
sys.path.insert(0, str(gcp_package_path))

from mistralai_gcp.sdk import GoogleCloudBeforeRequestHook

def test_gcp_before_request_preserves_timeout_extension():
    hook = GoogleCloudBeforeRequestHook(region="europe-west4", project_id="proj")

    req = httpx.Request(
        "POST",
        "https://europe-west4-aiplatform.googleapis.com/v1/dummy",
        content=b'{"model":"mistral-large-2407"}',
        headers={"content-type": "application/json"},
    )
    timeout = httpx.Timeout(30.0)
    req.extensions["timeout"] = timeout

    out = hook.before_request(None, req)
    assert isinstance(out, httpx.Request)
    assert out.extensions.get("timeout") == timeout
