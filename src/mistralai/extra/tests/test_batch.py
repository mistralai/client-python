import asyncio
import json
from typing import Any, Optional, Sequence, cast

import pytest

from mistralai.client.models import (
    BatchJob,
    BatchJobStatus,
    BatchRequest,
    EmbeddingRequest,
    EmbeddingResponse,
)
from mistralai.extra.batch import (
    RUNNING_STATUSES,
    BatchClient,
    BatchInput,
    BatchInputFile,
    BatchJobHandle,
    BatchError,
    BatchOutput,
    BatchRequestError,
    BatchResponseError,
    BatchResult,
    is_running,
    is_terminal,
)


# ---------------------------------------------------------------------------
# Fakes for the Mistral client surface the wrapper touches
# ---------------------------------------------------------------------------


def _make_job(
    status: BatchJobStatus = "SUCCESS", *, failed=0, succeeded=1, job_id="job-1"
):
    return BatchJob(
        id=job_id,
        input_files=["file-in"],
        endpoint="/v1/embeddings",
        errors=[],
        status=status,
        created_at=0,
        total_requests=succeeded + failed,
        completed_requests=succeeded + failed,
        succeeded_requests=succeeded,
        failed_requests=failed,
        output_file="file-out",
        error_file="file-err" if failed else None,
    )


class _FakeDownload:
    """Mimics the streaming httpx.Response the SDK's download_async returns:
    stream_to_bytes_async calls aread(); BatchClient.stream_results calls aiter_lines()."""

    def __init__(self, chunks):
        self._chunks = chunks

    async def aread(self):
        return b"".join(self._chunks)

    async def aiter_lines(self):
        for line in b"".join(self._chunks).decode().split("\n"):
            yield line

    async def aclose(self):
        pass


class _FakeFiles:
    def __init__(self, downloads=None):
        self.calls = []
        self._downloads = downloads or {}

    async def upload_async(self, **kwargs):
        self.calls.append(("upload", kwargs))
        return type("Resp", (), {"id": "file-uploaded"})()

    async def download_async(self, **kwargs):
        self.calls.append(("download", kwargs))
        chunks = self._downloads.get(kwargs["file_id"], [b""])
        return _FakeDownload(chunks)

    async def get_signed_url_async(self, **kwargs):
        self.calls.append(("signed_url", kwargs))
        return type("Resp", (), {"url": "https://signed/x"})()

    async def delete_async(self, **kwargs):
        self.calls.append(("delete", kwargs))


class _FakeJobs:
    def __init__(
        self, create_jobs, poll_statuses: Optional[Sequence[BatchJobStatus]] = None
    ):
        # create_jobs: list of BatchJob returned by successive create_async calls
        # poll_statuses: list of statuses returned by successive get_async calls.
        # get_async reports the last-created job's counts under the polled status,
        # mirroring the API (poll returns the same job's evolving state).
        self.calls: list[Any] = []
        self._create_jobs = list(create_jobs)
        default_statuses: Sequence[BatchJobStatus] = ["SUCCESS"]
        self._poll_statuses: list[BatchJobStatus] = list(
            poll_statuses or default_statuses
        )
        self._last_create: Optional[BatchJob] = None

    async def create_async(self, **kwargs):
        self.calls.append(("create", kwargs))
        self._last_create = self._create_jobs.pop(0)
        return self._last_create

    async def cancel_async(self, **kwargs):
        self.calls.append(("cancel", kwargs))
        return _make_job(status="CANCELLATION_REQUESTED")

    async def get_async(self, **kwargs):
        self.calls.append(("get", kwargs))
        status = self._poll_statuses.pop(0)
        job = self._last_create
        if job is None:  # get() called directly, without a prior create
            return _make_job(status=status)
        return _make_job(
            status=status,
            failed=job.failed_requests,
            succeeded=job.succeeded_requests,
            job_id=job.id,
        )


class _FakeClient:
    def __init__(self, files, jobs):
        self.files = files
        self.batch = type("Batch", (), {"jobs": jobs})()


def _embed_client(files, jobs):
    return BatchClient(
        # A stand-in for the handful of `Mistral` attributes the wrapper touches
        # (`.files`, `.batch.jobs`); building a real client here would need
        # credentials and a transport.
        cast(Any, _FakeClient(files, jobs)),
        endpoint="/v1/embeddings",
        response_body_type=EmbeddingResponse,
    )


def _embed_req(text="hi"):
    return EmbeddingRequest(model="mistral-embed", inputs=text)


def _ok_line(cid: Optional[str] = "a"):
    return json.dumps(
        {
            "custom_id": cid,
            "response": {
                "status_code": 200,
                "body": {
                    "id": "x",
                    "object": "list",
                    "model": "mistral-embed",
                    "usage": {
                        "prompt_tokens": 1,
                        "total_tokens": 1,
                        "completion_tokens": 0,
                    },
                    "data": [
                        {"object": "embedding", "embedding": [0.1, 0.2], "index": 0}
                    ],
                },
            },
            "error": None,
        }
    )


def _err_line(cid="b"):
    return json.dumps(
        {
            "custom_id": cid,
            "response": {"status_code": 429, "body": None},
            "error": "rate limited",
        }
    )


def _bad_body_line(cid="c"):
    # A successful (200, no error) response whose body doesn't match EmbeddingResponse.
    return json.dumps(
        {
            "custom_id": cid,
            "response": {"status_code": 200, "body": {"wrong": "shape"}},
            "error": None,
        }
    )


# ---------------------------------------------------------------------------
# Pure wire format: BatchInput
# ---------------------------------------------------------------------------


def test_batch_input_from_payload_serializes_with_alias():
    bi = BatchInput.from_payload({"a": _embed_req("hi")})
    (line,) = bi.to_jsonl_bytes().decode().splitlines()
    obj = json.loads(line)
    assert obj["custom_id"] == "a"
    # EmbeddingRequest.inputs serializes under its alias "input"
    assert obj["body"]["input"] == "hi"
    assert obj["body"]["model"] == "mistral-embed"


def test_batch_input_len_counts_requests():
    bi = BatchInput.from_payload({"a": _embed_req(), "b": _embed_req()})
    assert len(bi) == 2


def test_batch_input_to_requests():
    bi = BatchInput.from_payload({"a": _embed_req("hi")})
    reqs = bi.to_requests()
    assert len(reqs) == 1
    assert isinstance(reqs[0], BatchRequest)
    assert reqs[0].custom_id == "a"
    assert reqs[0].body["model"] == "mistral-embed"


def test_batch_input_jsonl_bytes_passthrough_verbatim():
    raw = b'{"custom_id":"a","body":{"model":"m","input":"hi"}}'
    assert BatchInput.from_jsonl_bytes(raw).to_jsonl_bytes() == raw
    assert BatchInput.from_jsonl_str(raw.decode()).to_jsonl_bytes() == raw


def test_batch_input_len_ignores_blank_lines():
    bi = BatchInput.from_jsonl_bytes(b'{"custom_id":"a","body":{}}\n\n')
    assert len(bi) == 1
    assert len(bi.to_requests()) == 1


# ---------------------------------------------------------------------------
# Pure wire format: BatchOutput
# ---------------------------------------------------------------------------


def test_batch_output_parses_ok_and_errors():
    raw = (_ok_line("a") + "\n" + _err_line("b")).encode()
    out = BatchOutput.from_jsonl_bytes(raw, EmbeddingResponse)

    ok = out.responses
    assert list(ok) == ["a"]
    assert isinstance(ok["a"], EmbeddingResponse)
    assert ok["a"].data[0].embedding == [0.1, 0.2]

    errors = out.request_errors
    assert [e.custom_id for e in errors] == ["b"]
    err = errors[0]
    assert isinstance(err, BatchRequestError)
    assert err.status_code == 429
    assert err.error == "rate limited"


def test_batch_output_status_400_without_error_field_is_error():
    line = json.dumps({"custom_id": "b", "response": {"status_code": 500, "body": {}}})
    out = BatchOutput.from_jsonl_bytes(line.encode(), EmbeddingResponse)
    assert out.responses == {}
    assert out.request_errors[0].status_code == 500


def test_batch_output_duplicate_custom_id_raises():
    # custom_id is unique per contract; a duplicate would silently overwrite, so
    # parsing (eager, at construction) fails loud rather than losing a result.
    raw = (_ok_line("a") + "\n" + _ok_line("a")).encode()
    with pytest.raises(AssertionError, match="duplicate custom_id"):
        BatchOutput.from_jsonl_bytes(raw, EmbeddingResponse)


def test_batch_output_unparseable_body_is_response_error():
    # A 200 whose body doesn't match RespBodyT is a client-side schema mismatch:
    # surfaced as data (BatchResponseError), not raised, so good lines still parse and
    # one bad line never aborts the whole batch.
    raw = (_ok_line("a") + "\n" + _bad_body_line("c")).encode()
    out = BatchOutput.from_jsonl_bytes(raw, EmbeddingResponse)

    assert list(out.responses) == ["a"]  # good result survives
    assert out.request_errors == []  # not a server-reported request failure

    resp_errs = out.response_errors
    assert [e.custom_id for e in resp_errs] == ["c"]
    err = resp_errs[0]
    assert isinstance(err, BatchResponseError)
    assert err.status_code == 200
    assert err.body == {"wrong": "shape"}
    assert isinstance(err.error, Exception)


def test_batch_output_results_covers_all_variants():
    raw = (_ok_line("a") + "\n" + _err_line("b") + "\n" + _bad_body_line("c")).encode()
    results = BatchOutput.from_jsonl_bytes(raw, EmbeddingResponse).results()
    assert isinstance(results["a"], EmbeddingResponse)
    assert isinstance(results["b"], BatchRequestError)
    assert isinstance(results["c"], BatchResponseError)


def test_batch_output_ordered_aligns_to_custom_ids():
    # ordered() returns successes positionally, in the caller's requested id order,
    # regardless of the order they appear in the output.
    raw = (_ok_line("b") + "\n" + _ok_line("a")).encode()
    out = BatchOutput.from_jsonl_bytes(raw, EmbeddingResponse)
    ordered = out.ordered(["a", "b"])
    assert [r.data[0].embedding for r in ordered] == [[0.1, 0.2], [0.1, 0.2]]
    assert len(ordered) == 2


def test_batch_output_ordered_reports_all_failures_with_reasons():
    # An id that errored and an id that never appeared both fail alignment; ordered()
    # is all-or-nothing and reports every failing id at once, each with its recorded
    # error (or None if the id never appeared in the output).
    raw = (_ok_line("a") + "\n" + _err_line("b")).encode()
    out = BatchOutput.from_jsonl_bytes(raw, EmbeddingResponse)
    with pytest.raises(BatchError) as exc:
        out.ordered(["a", "b", "missing"])
    assert list(exc.value.failures) == ["b", "missing"]
    assert isinstance(exc.value.failures["b"], BatchRequestError)
    assert exc.value.failures["missing"] is None


def test_batch_output_ordered_duplicate_error_id_raises():
    # custom_id is unique across the whole output; a request- and response-error sharing
    # one would silently overwrite in the error lookup, so ordered() fails loud.
    out = BatchOutput(
        {},
        [BatchRequestError(custom_id="b", status_code=500, error="boom")],
        [
            BatchResponseError(
                custom_id="b", status_code=200, body={}, error=ValueError()
            )
        ],
    )
    with pytest.raises(AssertionError, match="duplicate custom_id"):
        out.ordered(["b"])


def test_batch_output_success_missing_custom_id_is_response_error():
    # A response that parses cleanly but has no custom_id can't be keyed into
    # responses; rather than drop it silently it's surfaced as a response error.
    out = BatchOutput.from_jsonl_bytes(_ok_line(None).encode(), EmbeddingResponse)
    assert out.responses == {}
    (err,) = out.response_errors
    assert err.custom_id is None
    assert isinstance(err.body, EmbeddingResponse)
    # a null-id error has no key, so the unified view drops it
    assert out.results() == {}


def test_batch_output_error_missing_custom_id_dropped_from_results():
    line = json.dumps({"response": {"status_code": 500, "body": {}}, "error": "boom"})
    out = BatchOutput.from_jsonl_bytes(line.encode(), EmbeddingResponse)
    (err,) = out.request_errors
    assert err.custom_id is None
    assert out.results() == {}  # can't key a null-id error


# ---------------------------------------------------------------------------
# Status helpers
# ---------------------------------------------------------------------------


def test_running_statuses_membership():
    assert RUNNING_STATUSES == {"QUEUED", "RUNNING", "CANCELLATION_REQUESTED"}


@pytest.mark.parametrize("status", ["QUEUED", "RUNNING", "CANCELLATION_REQUESTED"])
def test_is_running_true(status):
    assert is_running(status)
    assert not is_terminal(status)


@pytest.mark.parametrize(
    "status", ["SUCCESS", "FAILED", "TIMEOUT_EXCEEDED", "CANCELLED", "SOMETHING_NEW"]
)
def test_is_terminal_true(status):
    # unknown/future status treated as terminal so a poll loop can stop
    assert is_terminal(status)
    assert not is_running(status)


# ---------------------------------------------------------------------------
# File primitives
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_upload_returns_handle_and_sets_purpose():
    files = _FakeFiles()
    client = _embed_client(files, _FakeJobs([_make_job()]))
    handle = await client.upload(BatchInput.from_payload({"a": _embed_req()}))
    assert isinstance(handle, BatchInputFile)
    assert handle.file_id == "file-uploaded"
    _, kwargs = files.calls[0]
    assert kwargs["purpose"] == "batch"
    assert kwargs["file"].file_name == "batch_input.jsonl"
    # optional knobs omitted when not provided
    assert "expiry" not in kwargs
    assert "timeout_ms" not in kwargs
    assert "http_headers" not in kwargs


@pytest.mark.asyncio
async def test_upload_forwards_optional_knobs():
    files = _FakeFiles()
    client = _embed_client(files, _FakeJobs([_make_job()]))
    await client.upload(
        BatchInput.from_payload({"a": _embed_req()}),
        file_name="custom.jsonl",
        expiry_hours=48,
        timeout_ms=1000,
        http_headers={"x": "y"},
    )
    _, kwargs = files.calls[0]
    assert kwargs["file"].file_name == "custom.jsonl"
    assert kwargs["expiry"] == 48
    assert kwargs["timeout_ms"] == 1000
    assert kwargs["http_headers"] == {"x": "y"}


@pytest.mark.asyncio
async def test_download_concatenates_stream():
    files = _FakeFiles(downloads={"file-out": [b"foo", b"bar"]})
    client = _embed_client(files, _FakeJobs([]))
    assert await client.download("file-out") == b"foobar"


@pytest.mark.asyncio
async def test_signed_url_returns_url_and_forwards_expiry():
    files = _FakeFiles()
    client = _embed_client(files, _FakeJobs([]))
    url = await client.signed_url("file-out", expiry_hours=12)
    assert url == "https://signed/x"
    _, kwargs = files.calls[0]
    assert kwargs["expiry"] == 12


@pytest.mark.asyncio
async def test_delete_calls_delete_async():
    files = _FakeFiles()
    client = _embed_client(files, _FakeJobs([]))
    await client.delete("file-out")
    assert files.calls[0][0] == "delete"
    assert files.calls[0][1]["file_id"] == "file-out"


# ---------------------------------------------------------------------------
# Job primitives (handle in / handle out)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_from_input_returns_handle_and_sends_inline_requests():
    jobs = _FakeJobs([_make_job(job_id="j9")])
    client = _embed_client(_FakeFiles(), jobs)
    handle = await client.create(
        BatchInput.from_payload({"a": _embed_req()}),
        model="mistral-embed",
        metadata={"k": "v"},
    )
    assert isinstance(handle, BatchJobHandle)
    assert handle.id == "j9"
    assert handle.status == "SUCCESS"
    _, kwargs = jobs.calls[0]
    assert "requests" in kwargs
    assert "input_files" not in kwargs
    assert kwargs["endpoint"] == "/v1/embeddings"
    assert kwargs["model"] == "mistral-embed"
    assert kwargs["metadata"] == {"k": "v"}
    assert isinstance(kwargs["requests"][0], BatchRequest)


@pytest.mark.asyncio
async def test_create_from_file_sends_input_files():
    jobs = _FakeJobs([_make_job()])
    client = _embed_client(_FakeFiles(), jobs)
    await client.create(BatchInputFile("file-xyz"))
    _, kwargs = jobs.calls[0]
    assert kwargs["input_files"] == ["file-xyz"]
    assert "requests" not in kwargs


@pytest.mark.asyncio
async def test_get_returns_handle():
    jobs = _FakeJobs([], poll_statuses=["RUNNING"])
    client = _embed_client(_FakeFiles(), jobs)
    handle = await client.get("job-1", http_headers={"a": "b"})
    assert isinstance(handle, BatchJobHandle)
    assert handle.status == "RUNNING"
    _, kwargs = jobs.calls[0]
    assert kwargs["job_id"] == "job-1"
    assert kwargs["http_headers"] == {"a": "b"}


@pytest.mark.asyncio
async def test_refresh_refetches_state():
    jobs = _FakeJobs(
        [_make_job(status="QUEUED", job_id="jx")], poll_statuses=["RUNNING"]
    )
    client = _embed_client(_FakeFiles(), jobs)
    handle = await client.create(BatchInput.from_payload({"a": _embed_req()}))
    assert handle.status == "QUEUED"
    refreshed = await client.refresh(handle)
    assert refreshed.status == "RUNNING"


@pytest.mark.asyncio
async def test_cancel_accepts_id_and_returns_handle():
    jobs = _FakeJobs([])
    client = _embed_client(_FakeFiles(), jobs)
    handle = await client.cancel("job-1", http_headers={"a": "b"})
    assert isinstance(handle, BatchJobHandle)
    assert handle.status == "CANCELLATION_REQUESTED"
    _, kwargs = jobs.calls[0]
    assert jobs.calls[0][0] == "cancel"
    assert kwargs["job_id"] == "job-1"
    assert kwargs["http_headers"] == {"a": "b"}


@pytest.mark.asyncio
async def test_cancel_accepts_handle():
    jobs = _FakeJobs([])
    client = _embed_client(_FakeFiles(), jobs)
    handle = BatchJobHandle(_make_job(status="RUNNING", job_id="jz"))
    await client.cancel(handle)
    assert jobs.calls[0][1]["job_id"] == "jz"


@pytest.mark.asyncio
async def test_wait_polls_until_terminal():
    jobs = _FakeJobs(
        [_make_job(status="QUEUED")], poll_statuses=["QUEUED", "RUNNING", "SUCCESS"]
    )
    client = _embed_client(_FakeFiles(), jobs)
    handle = await client.create(BatchInput.from_payload({"a": _embed_req()}))
    terminal = await client.wait(handle, poll_interval_seconds=0)
    assert terminal.status == "SUCCESS"
    assert len([c for c in jobs.calls if c[0] == "get"]) == 3


@pytest.mark.asyncio
async def test_wait_raises_timeout():
    jobs = _FakeJobs([_make_job(status="QUEUED")], poll_statuses=["QUEUED"])
    client = _embed_client(_FakeFiles(), jobs)
    handle = await client.create(BatchInput.from_payload({"a": _embed_req()}))
    with pytest.raises(TimeoutError):
        await client.wait(handle, poll_interval_seconds=0, timeout_hours=0)


# ---------------------------------------------------------------------------
# stream_results() — one-pass, line by line
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_stream_yields_ok_and_errors():
    files = _FakeFiles(
        downloads={
            "file-out": [_ok_line("a").encode()],
            "file-err": [_err_line("b").encode()],
        }
    )
    jobs = _FakeJobs([_make_job(failed=1, succeeded=1)])
    client = _embed_client(files, jobs)
    handle = await client.create(BatchInput.from_payload({"a": _embed_req()}))
    items = [item async for item in client.stream_results(handle)]
    by_id = dict(items)
    assert isinstance(by_id["a"], EmbeddingResponse)
    assert isinstance(by_id["b"], BatchRequestError)
    assert by_id["b"].status_code == 429


@pytest.mark.asyncio
async def test_stream_yields_response_error_for_unparseable_body():
    files = _FakeFiles(downloads={"file-out": [_bad_body_line("c").encode()]})
    jobs = _FakeJobs([_make_job()])
    client = _embed_client(files, jobs)
    handle = await client.create(BatchInput.from_payload({"c": _embed_req()}))
    items = dict([item async for item in client.stream_results(handle)])
    assert isinstance(items["c"], BatchResponseError)
    assert items["c"].body == {"wrong": "shape"}


@pytest.mark.asyncio
async def test_stream_is_read_only_and_never_deletes():
    # stream_results binds to a job the caller owns: it reads only, never uploading,
    # creating, or deleting -- cleanup of the job and its files stays the caller's.
    files = _FakeFiles(
        downloads={
            "file-out": [_ok_line("a").encode()],
            "file-err": [_err_line("b").encode()],
        }
    )
    jobs = _FakeJobs([_make_job(failed=1, succeeded=1)])
    client = _embed_client(files, jobs)
    handle = await client.create(BatchInput.from_payload({"a": _embed_req()}))
    _ = [item async for item in client.stream_results(handle)]
    assert not any(c[0] in ("upload", "delete") for c in files.calls)
    assert not any(c[0] == "cancel" for c in jobs.calls)


@pytest.mark.asyncio
async def test_stream_waits_when_not_terminal():
    files = _FakeFiles(downloads={"file-out": [_ok_line("a").encode()]})
    jobs = _FakeJobs([_make_job(status="QUEUED")], poll_statuses=["QUEUED", "SUCCESS"])
    client = _embed_client(files, jobs)
    handle = await client.create(BatchInput.from_payload({"a": _embed_req()}))
    items = [
        item async for item in client.stream_results(handle, poll_interval_seconds=0)
    ]
    assert [cid for cid, _ in items] == ["a"]
    assert len([c for c in jobs.calls if c[0] == "get"]) == 2


@pytest.mark.asyncio
async def test_stream_forwards_http_headers_to_download():
    files = _FakeFiles(downloads={"file-out": [_ok_line("a").encode()]})
    jobs = _FakeJobs([_make_job()])
    client = _embed_client(files, jobs)
    handle = await client.create(BatchInput.from_payload({"a": _embed_req()}))
    _ = [item async for item in client.stream_results(handle, http_headers={"x": "y"})]
    download = next(c for c in files.calls if c[0] == "download")
    assert download[1]["http_headers"] == {"x": "y"}


# ---------------------------------------------------------------------------
# run() — blocking, materialized BatchResult
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_run_small_input_inline_no_upload():
    files = _FakeFiles(downloads={"file-out": [_ok_line("a").encode()]})
    jobs = _FakeJobs([_make_job()], poll_statuses=["QUEUED", "SUCCESS"])
    client = _embed_client(files, jobs)
    result = await client.run(
        BatchInput.from_payload({"a": _embed_req()}), poll_interval_seconds=0
    )
    assert result.status == "SUCCESS"
    assert result.succeeded == 1
    assert result.failed == 0
    # inline: no upload happened, create used requests=
    assert not any(c[0] == "upload" for c in files.calls)
    assert jobs.calls[0][0] == "create"
    assert "requests" in jobs.calls[0][1]


@pytest.mark.asyncio
async def test_run_uploads_when_over_inline_threshold():
    files = _FakeFiles()
    jobs = _FakeJobs([_make_job()], poll_statuses=["SUCCESS"])
    client = _embed_client(files, jobs)
    await client.run(
        BatchInput.from_payload({"a": _embed_req(), "b": _embed_req()}),
        inline_threshold=1,
        poll_interval_seconds=0,
    )
    assert files.calls[0][0] == "upload"
    _, create_kwargs = jobs.calls[0]
    assert create_kwargs["input_files"] == ["file-uploaded"]


@pytest.mark.asyncio
async def test_run_input_file_passthrough_no_upload():
    files = _FakeFiles()
    jobs = _FakeJobs([_make_job()], poll_statuses=["SUCCESS"])
    client = _embed_client(files, jobs)
    await client.run(BatchInputFile("file-pre"), poll_interval_seconds=0)
    assert not any(c[0] == "upload" for c in files.calls)
    assert jobs.calls[0][1]["input_files"] == ["file-pre"]


@pytest.mark.asyncio
async def test_run_retries_whole_job_on_failed_requests():
    files = _FakeFiles()
    jobs = _FakeJobs(
        [_make_job(failed=1, succeeded=0), _make_job(failed=0, succeeded=1)],
        poll_statuses=["SUCCESS", "SUCCESS"],
    )
    client = _embed_client(files, jobs)
    result = await client.run(
        BatchInput.from_payload({"a": _embed_req()}),
        max_failed_job_retries=1,
        poll_interval_seconds=0,
    )
    assert result.failed == 0
    creates = [c for c in jobs.calls if c[0] == "create"]
    assert len(creates) == 2


@pytest.mark.asyncio
async def test_run_stops_retrying_after_budget_exhausted():
    files = _FakeFiles()
    jobs = _FakeJobs(
        [_make_job(failed=1, succeeded=0), _make_job(failed=1, succeeded=0)],
        poll_statuses=["SUCCESS", "SUCCESS"],
    )
    client = _embed_client(files, jobs)
    result = await client.run(
        BatchInput.from_payload({"a": _embed_req()}),
        max_failed_job_retries=1,
        poll_interval_seconds=0,
    )
    # still failed after using all retries; returns last job rather than looping
    assert result.failed == 1
    assert len([c for c in jobs.calls if c[0] == "create"]) == 2


@pytest.mark.asyncio
async def test_run_coerces_raw_dict():
    files = _FakeFiles()
    jobs = _FakeJobs([_make_job()], poll_statuses=["SUCCESS"])
    client = _embed_client(files, jobs)
    result = await client.run({"a": _embed_req()}, poll_interval_seconds=0)
    assert result.status == "SUCCESS"
    assert "requests" in jobs.calls[0][1]


@pytest.mark.asyncio
async def test_run_coerces_raw_bytes_and_str():
    raw = BatchInput.from_payload({"a": _embed_req()}).to_jsonl_bytes()
    for payload in (raw, raw.decode()):
        jobs = _FakeJobs([_make_job()], poll_statuses=["SUCCESS"])
        client = _embed_client(_FakeFiles(), jobs)
        result = await client.run(payload, poll_interval_seconds=0)
        assert result.status == "SUCCESS"


@pytest.mark.asyncio
async def test_run_rejects_unsupported_input():
    client = _embed_client(_FakeFiles(), _FakeJobs([]))
    with pytest.raises(TypeError):
        await client.run(123)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_run_raises_timeout_when_deadline_passed():
    client = _embed_client(_FakeFiles(), _FakeJobs([_make_job()]))
    with pytest.raises(TimeoutError):
        await client.run(
            BatchInput.from_payload({"a": _embed_req()}),
            timeout_hours=0,
            poll_interval_seconds=0,
        )


# ---------------------------------------------------------------------------
# BatchResult — materialized, sync accessors
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_run_materializes_output_downloaded_once():
    files = _FakeFiles(downloads={"file-out": [_ok_line("a").encode()]})
    jobs = _FakeJobs([_make_job()], poll_statuses=["SUCCESS"])
    client = _embed_client(files, jobs)
    result = await client.run(
        BatchInput.from_payload({"a": _embed_req()}), poll_interval_seconds=0
    )
    # sync accessors, no await
    assert list(result.by_id()) == ["a"]
    assert list(result.output().responses) == ["a"]
    # output downloaded exactly once, during run() (no error file to fetch)
    downloads = [c for c in files.calls if c[0] == "download"]
    assert len(downloads) == 1


@pytest.mark.asyncio
async def test_run_error_output_none_when_no_error_file():
    files = _FakeFiles(downloads={"file-out": [_ok_line("a").encode()]})
    jobs = _FakeJobs([_make_job(failed=0)], poll_statuses=["SUCCESS"])
    client = _embed_client(files, jobs)
    result = await client.run(
        BatchInput.from_payload({"a": _embed_req()}), poll_interval_seconds=0
    )
    assert result.error_output() is None


@pytest.mark.asyncio
async def test_run_error_output_parsed_and_merged():
    files = _FakeFiles(
        downloads={"file-out": [b""], "file-err": [_err_line("b").encode()]}
    )
    jobs = _FakeJobs([_make_job(failed=1, succeeded=0)], poll_statuses=["SUCCESS"])
    client = _embed_client(files, jobs)
    result = await client.run(
        BatchInput.from_payload({"a": _embed_req()}), poll_interval_seconds=0
    )
    eo = result.error_output()
    assert eo is not None
    assert [e.custom_id for e in eo.request_errors] == ["b"]
    # errors() merges the output and error files
    assert [e.custom_id for e in result.errors()] == ["b"]


@pytest.mark.asyncio
async def test_run_response_errors_merged_across_files():
    # An unparseable body in each of the output and error files surfaces via
    # response_errors(), merged across both.
    files = _FakeFiles(
        downloads={
            "file-out": [_bad_body_line("c").encode()],
            "file-err": [_bad_body_line("d").encode()],
        }
    )
    jobs = _FakeJobs([_make_job(failed=1, succeeded=1)], poll_statuses=["SUCCESS"])
    client = _embed_client(files, jobs)
    result = await client.run(
        BatchInput.from_payload({"a": _embed_req()}), poll_interval_seconds=0
    )
    # `custom_id` is Optional on the error models; the filter keeps this sortable
    # without weakening the assertion -- a dropped None still fails the compare.
    assert sorted(e.custom_id for e in result.response_errors() if e.custom_id) == [
        "c",
        "d",
    ]


def test_result_ordered_aligns_and_fails_closed():
    out = BatchOutput.from_jsonl_bytes(_ok_line("a").encode(), EmbeddingResponse)
    err_out = BatchOutput.from_jsonl_bytes(_err_line("b").encode(), EmbeddingResponse)
    result = BatchResult(_make_job(), out, err_out)
    # success comes back positionally...
    assert len(result.ordered(["a"])) == 1
    # ...and an errored id (in the error file) fails closed rather than misaligning
    with pytest.raises(BatchError) as exc:
        result.ordered(["a", "b"])
    assert list(exc.value.failures) == ["b"]
    assert isinstance(exc.value.failures["b"], BatchRequestError)


def test_by_id_same_custom_id_across_files_raises():
    # custom_id is unique across the whole output (output OR error file, never both);
    # a collision when merging the two files means a broken emitter, so fail loud
    # rather than silently drop one response.
    out = BatchOutput.from_jsonl_bytes(_ok_line("a").encode(), EmbeddingResponse)
    err_out = BatchOutput.from_jsonl_bytes(_ok_line("a").encode(), EmbeddingResponse)
    result = BatchResult(_make_job(), out, err_out)
    with pytest.raises(AssertionError, match="duplicate custom_id"):
        result.by_id()


@pytest.mark.asyncio
async def test_run_download_uses_http_headers():
    files = _FakeFiles(downloads={"file-out": [_ok_line("a").encode()]})
    jobs = _FakeJobs([_make_job()], poll_statuses=["SUCCESS"])
    client = _embed_client(files, jobs)
    await client.run(
        BatchInput.from_payload({"a": _embed_req()}),
        poll_interval_seconds=0,
        http_headers={"x": "y"},
    )
    download = next(c for c in files.calls if c[0] == "download")
    assert download[1]["http_headers"] == {"x": "y"}


# ---------------------------------------------------------------------------
# run() cleans up the server-side files/jobs it creates internally
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_run_deletes_input_it_uploaded_and_result_files():
    files = _FakeFiles(downloads={"file-out": [_ok_line("a").encode()]})
    jobs = _FakeJobs([_make_job()], poll_statuses=["SUCCESS"])
    client = _embed_client(files, jobs)
    await client.run(
        BatchInput.from_payload({"a": _embed_req(), "b": _embed_req()}),
        inline_threshold=1,  # force an upload
        poll_interval_seconds=0,
    )
    deleted = {c[1]["file_id"] for c in files.calls if c[0] == "delete"}
    # the input file run() uploaded + the job's output file are all cleaned up
    assert deleted == {"file-uploaded", "file-out"}


@pytest.mark.asyncio
async def test_run_deletes_output_and_error_files():
    files = _FakeFiles(
        downloads={"file-out": [b""], "file-err": [_err_line("b").encode()]}
    )
    jobs = _FakeJobs([_make_job(failed=1, succeeded=0)], poll_statuses=["SUCCESS"])
    client = _embed_client(files, jobs)
    await client.run(
        BatchInput.from_payload({"a": _embed_req()}), poll_interval_seconds=0
    )
    deleted = {c[1]["file_id"] for c in files.calls if c[0] == "delete"}
    # inline input (nothing uploaded); both result files cleaned up
    assert deleted == {"file-out", "file-err"}


@pytest.mark.asyncio
async def test_run_does_not_delete_caller_supplied_input_file():
    files = _FakeFiles(downloads={"file-out": [_ok_line("a").encode()]})
    jobs = _FakeJobs([_make_job()], poll_statuses=["SUCCESS"])
    client = _embed_client(files, jobs)
    await client.run(BatchInputFile("file-pre"), poll_interval_seconds=0)
    deleted = {c[1]["file_id"] for c in files.calls if c[0] == "delete"}
    assert "file-pre" not in deleted  # the caller owns their input file
    assert "file-out" in deleted


@pytest.mark.asyncio
async def test_run_delete_uses_http_headers():
    files = _FakeFiles(downloads={"file-out": [_ok_line("a").encode()]})
    jobs = _FakeJobs([_make_job()], poll_statuses=["SUCCESS"])
    client = _embed_client(files, jobs)
    await client.run(
        BatchInput.from_payload({"a": _embed_req()}),
        poll_interval_seconds=0,
        http_headers={"x": "y"},
    )
    delete = next(c for c in files.calls if c[0] == "delete")
    assert delete[1]["http_headers"] == {"x": "y"}


@pytest.mark.asyncio
async def test_run_cancels_running_job_on_timeout(monkeypatch):
    files = _FakeFiles()
    jobs = _FakeJobs([_make_job(status="RUNNING")])
    client = _embed_client(files, jobs)

    async def _timeout(*args, **kwargs):
        raise TimeoutError("polling timed out")

    monkeypatch.setattr(client, "wait", _timeout)
    with pytest.raises(TimeoutError):
        await client.run(
            BatchInput.from_payload({"a": _embed_req()}), poll_interval_seconds=0
        )
    # the created job (still RUNNING) is cancelled rather than left billing
    assert any(c[0] == "cancel" for c in jobs.calls)


@pytest.mark.asyncio
async def test_run_cancels_running_job_on_coroutine_cancel(monkeypatch):
    files = _FakeFiles()
    jobs = _FakeJobs([_make_job(status="RUNNING")])
    client = _embed_client(files, jobs)

    async def _cancelled(*args, **kwargs):
        raise asyncio.CancelledError()

    monkeypatch.setattr(client, "wait", _cancelled)
    with pytest.raises(asyncio.CancelledError):
        await client.run(
            BatchInput.from_payload({"a": _embed_req()}), poll_interval_seconds=0
        )
    assert any(c[0] == "cancel" for c in jobs.calls)


@pytest.mark.asyncio
async def test_run_does_not_cancel_when_no_job_created():
    files = _FakeFiles()
    jobs = _FakeJobs([_make_job()])
    client = _embed_client(files, jobs)
    with pytest.raises(TimeoutError):
        await client.run(
            BatchInput.from_payload({"a": _embed_req()}),
            timeout_hours=0,  # deadline passes before the first create
            poll_interval_seconds=0,
        )
    assert not any(c[0] == "cancel" for c in jobs.calls)
    assert not any(c[0] == "create" for c in jobs.calls)


@pytest.mark.asyncio
async def test_run_keeps_result_files_when_download_fails():
    # A failed output download must NOT delete the server-side result files: a
    # completed job's output stays recoverable rather than being destroyed.
    files = _FakeFiles()

    async def _boom(**kwargs):
        files.calls.append(("download", kwargs))
        raise RuntimeError("download blip")

    files.download_async = _boom
    jobs = _FakeJobs([_make_job()], poll_statuses=["SUCCESS"])
    client = _embed_client(files, jobs)
    with pytest.raises(RuntimeError):
        await client.run(
            BatchInput.from_payload({"a": _embed_req()}), poll_interval_seconds=0
        )
    deleted = {c[1]["file_id"] for c in files.calls if c[0] == "delete"}
    assert "file-out" not in deleted
    assert "file-err" not in deleted


@pytest.mark.asyncio
async def test_run_keeps_prior_result_files_when_retry_fails():
    # A superseded attempt's files must not be deleted the moment run() decides to
    # retry: if the next create/wait then fails, the abort path must still leave
    # them recoverable rather than having destroyed them eagerly.
    files = _FakeFiles(
        downloads={"file-out": [b""], "file-err": [_err_line("b").encode()]}
    )
    # one failing attempt; run() wants a retry, but the 2nd create has no job to pop
    jobs = _FakeJobs([_make_job(failed=1, succeeded=0)], poll_statuses=["SUCCESS"])
    client = _embed_client(files, jobs)
    with pytest.raises(IndexError):
        await client.run(
            BatchInput.from_payload({"a": _embed_req()}),
            max_failed_job_retries=1,
            poll_interval_seconds=0,
        )
    deleted = {c[1]["file_id"] for c in files.calls if c[0] == "delete"}
    assert "file-out" not in deleted  # prior attempt's files stay recoverable
    assert "file-err" not in deleted


@pytest.mark.asyncio
async def test_run_cancels_and_deletes_input_on_unexpected_error(monkeypatch):
    # A non-timeout blip in wait() (connection reset, 5xx) must still stop a running
    # job before deleting the input it is reading -- not orphan a billing job.
    files = _FakeFiles()
    jobs = _FakeJobs([_make_job(status="RUNNING")])
    client = _embed_client(files, jobs)

    async def _boom(*args, **kwargs):
        raise RuntimeError("connection reset")

    monkeypatch.setattr(client, "wait", _boom)
    with pytest.raises(RuntimeError):
        await client.run(
            BatchInput.from_payload({"a": _embed_req(), "b": _embed_req()}),
            inline_threshold=1,  # force an upload so there is an input to clean up
            poll_interval_seconds=0,
        )
    assert any(c[0] == "cancel" for c in jobs.calls)
    deleted = {c[1]["file_id"] for c in files.calls if c[0] == "delete"}
    assert "file-uploaded" in deleted
