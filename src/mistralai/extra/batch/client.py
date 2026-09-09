"""Generic typed wrapper over the Batch API.

The Batch API is one generic mechanism (upload a JSONL of requests, poll the job,
download a JSONL of responses) parameterized by ``endpoint``. Only two things vary
per endpoint: the request body and the response body. Everything else -- the line
envelope (``custom_id``/``body`` on input, ``custom_id``/``response.body``/``error``
on output) and the upload/create/poll/download lifecycle -- is invariant.

The layer is split so it fits any lifecycle shape (blocking loops, Temporal
activities polled by a retry policy, CLIs that create now and retrieve in a later
process):

* Pure wire format -- ``BatchInput`` / ``BatchOutput``. No I/O, fully sync. Build the
  input JSONL from typed bodies (or pass raw bytes through), parse the output JSONL
  into typed responses plus per-``custom_id`` errors. Drop these into any lifecycle;
  serialize now and stash the bytes to run later.
* Job handle -- ``BatchJobHandle``. A pure, serializable snapshot of one created job
  (just the ``BatchJob`` data, no client ref). Drive it through the client:
  ``BatchClient.create``/``get`` return one, and ``wait``/``stream_results``/``output``/
  ``cancel`` take one. Stash ``handle.job`` and rehydrate later via ``get(job_id)``.
* Lifecycle primitives -- ``BatchClient.upload/create/get/refresh/wait/cancel/
  stream_results/output/download/signed_url/delete``. Thin and single-shot (``create``/``get`` do one
  API call then wrap), so an external driver (Temporal, cron) can own the cadence.
* Convenience -- ``BatchClient.run`` composes the primitives into one blocking
  create -> poll -> materialized ``BatchResult`` call, for the single-process case,
  and adds whole-job retry.

``run`` waits for the whole job then materializes the result (random access, sync
accessors); ``stream_results`` yields ``(custom_id, response|error)`` one at a time
without holding the whole file in memory. The contract promises each item exactly
once as an async stream -- NOT *when* -- so if the server later returns results
incrementally, only ``stream_results``'s internals change, not the caller's ``async for``.

Bind the two per-endpoint SDK models at construction::

    client = BatchClient(mistral, endpoint="/v1/embeddings", response_body_type=EmbeddingResponse)

See ``examples/mistral/jobs/async_batch_job_embeddings_typed.py``.
"""

from __future__ import annotations

import asyncio
import json
import math
import time
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Generic,
    Iterable,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

from pydantic import ValidationError

from mistralai.client.models import (
    APIEndpoint,
    BatchJob,
    BatchJobStatus,
    BatchRequest,
    File,
)
from mistralai.client.types import BaseModel, OptionalNullable
from mistralai.client.utils import stream_to_bytes_async

if TYPE_CHECKING:
    from mistralai.client.sdk import Mistral


ReqBodyT = TypeVar("ReqBodyT", bound=BaseModel)
RespBodyT = TypeVar("RespBodyT", bound=BaseModel)

# A job is still in flight while in one of these; anything else (including an
# unrecognized future status) is treated as terminal so a poll loop can stop.
RUNNING_STATUSES = frozenset({"QUEUED", "RUNNING", "CANCELLATION_REQUESTED"})


def is_running(status: BatchJobStatus) -> bool:
    """True while the job is still in flight (see ``RUNNING_STATUSES``)."""
    return status in RUNNING_STATUSES


def is_terminal(status: BatchJobStatus) -> bool:
    """True once the job has settled; unknown/future statuses count as terminal."""
    return status not in RUNNING_STATUSES


def _dump_body(body: BaseModel) -> dict[str, Any]:
    return body.model_dump(mode="json", by_alias=True)


# ---------------------------------------------------------------------------
# Pure wire format (no I/O)
# ---------------------------------------------------------------------------


class BatchInput(Generic[ReqBodyT]):
    """Input JSONL for a batch, in memory. Pure and sync -- owns the input wire
    format and nothing else, so it drops into any lifecycle (serialize now, upload
    and run later).

    Build it via a factory; the object holds the serialized bytes and derives both
    views (``to_jsonl_bytes`` for upload, ``to_requests`` for an inline job)::

        BatchInput.from_payload({custom_id: body})   # typed request bodies
        BatchInput.from_jsonl_bytes(raw)             # already-serialized, verbatim
        BatchInput.from_jsonl_str(raw)

    ``ReqBodyT`` records the request-body type the lines carry (a marker for the
    typed path; passthrough bytes are unchecked).
    """

    def __init__(self, raw: bytes) -> None:
        self._raw = raw

    @classmethod
    def from_payload(cls, payload: dict[str, ReqBodyT]) -> "BatchInput[ReqBodyT]":
        """Serialize typed request bodies (keyed by custom_id) to batch input JSONL."""
        lines = [
            json.dumps(
                {"custom_id": cid, "body": _dump_body(body)}, separators=(",", ":")
            )
            for cid, body in payload.items()
        ]
        return cls("\n".join(lines).encode("utf-8"))

    @classmethod
    def from_jsonl_bytes(cls, raw: bytes) -> "BatchInput[ReqBodyT]":
        """Wrap already-serialized batch input JSONL verbatim."""
        return cls(raw)

    @classmethod
    def from_jsonl_str(cls, raw: str) -> "BatchInput[ReqBodyT]":
        """Wrap already-serialized batch input JSONL verbatim."""
        return cls(raw.encode("utf-8"))

    def to_jsonl_bytes(self) -> bytes:
        return self._raw

    def to_requests(self) -> list[BatchRequest]:
        """The lines as ``BatchRequest`` objects, for an inline (no-upload) job."""
        requests = []
        for line in self._raw.split(b"\n"):
            if not line.strip():
                continue
            obj = json.loads(line)
            requests.append(
                BatchRequest(custom_id=obj.get("custom_id"), body=obj["body"])
            )
        return requests

    def __len__(self) -> int:
        """Number of requests (non-empty lines)."""
        return sum(1 for line in self._raw.split(b"\n") if line.strip())


@dataclass(frozen=True)
class BatchInputFile(Generic[ReqBodyT]):
    """Handle to an uploaded batch input file. Produced by ``BatchClient.upload``, or
    constructed directly to reference a file uploaded elsewhere. ``ReqBodyT`` is a
    phantom marker recording the request-body type the file's lines carry, so
    ``BatchClient`` can type-check it against its endpoint."""

    file_id: str


@dataclass(frozen=True)
class BatchRequestError:
    """The batch API reporting that one request failed (an ``error`` on the line, or a
    ``status_code >= 400``). A server-side per-request failure, distinct from
    ``BatchResponseError`` (a response we couldn't parse)."""

    custom_id: Optional[str]
    status_code: Optional[int]
    error: Any


@dataclass(frozen=True)
class BatchResponseError:
    """A request the batch API executed and returned a success response for, but whose
    body could not be parsed into the bound ``RespBodyT`` -- a client-side schema
    mismatch (SDK model vs. server payload), not a server-reported request failure.
    Kept as data (not raised) so one unparseable line doesn't abort the whole batch;
    ``body`` retains the raw payload for inspection or manual recovery."""

    custom_id: Optional[str]
    status_code: Optional[int]
    body: Any
    error: Exception


class BatchError(Exception):
    """Raised by the strict ``ordered`` accessor when one or more requested custom_ids
    have no successful response. Lets a caller relying on positional alignment fail loud
    instead of silently misaligning results with inputs. ``failures`` maps every failing
    id (not just the first) to its outcome: the ``BatchRequestError``/
    ``BatchResponseError`` the batch reported, or None if the id never appeared in the
    output at all."""

    def __init__(
        self,
        failures: dict[str, Union[BatchRequestError, BatchResponseError, None]],
    ) -> None:
        self.failures = failures
        detail = ", ".join(
            f"{cid!r}: {'missing from output' if outcome is None else outcome!r}"
            for cid, outcome in failures.items()
        )
        super().__init__(f"batch output has no successful result for {detail}")


# custom_id -> one request's outcome: the parsed response body, a server-reported
# request failure, or a response that arrived but didn't match ``RespBodyT``.
BatchItem = Union[RespBodyT, BatchRequestError, BatchResponseError]


def _ordered(
    responses: Mapping[str, RespBodyT],
    errors_by_id: Mapping[str, Union[BatchRequestError, BatchResponseError]],
    custom_ids: Iterable[str],
) -> list[RespBodyT]:
    """Successes aligned positionally to ``custom_ids``. All-or-nothing: if any id has
    no successful response, raise ``BatchError`` reporting every failing id at once --
    each with the error the batch recorded, or None if it never appeared -- rather than
    returning a short or misaligned list. Shared by ``BatchOutput`` and ``BatchResult``."""
    custom_ids = list(custom_ids)
    failures = {
        cid: errors_by_id.get(cid)
        for cid in dict.fromkeys(custom_ids)
        if cid not in responses
    }
    if failures:
        raise BatchError(failures)
    return [responses[cid] for cid in custom_ids]


def _parse_output_obj(
    obj: dict[str, Any], response_body_type: type[RespBodyT]
) -> Tuple[Optional[str], "BatchItem[RespBodyT]"]:
    """One decoded output line -> ``(custom_id, outcome)``, where outcome is a typed
    response, a ``BatchRequestError``, or a ``BatchResponseError``. The single source
    of truth for output-line semantics, shared by the buffered ``BatchOutput`` and the
    one-pass ``BatchClient.stream_results``."""
    custom_id = obj.get("custom_id")
    response = obj.get("response") or {}
    status_code = response.get("status_code")
    error = obj.get("error")
    if error is not None or (status_code is not None and status_code >= 400):
        return custom_id, BatchRequestError(
            custom_id=custom_id, status_code=status_code, error=error
        )
    try:
        return custom_id, response_body_type.model_validate(response.get("body"))
    except ValidationError as exc:
        return custom_id, BatchResponseError(
            custom_id=custom_id,
            status_code=status_code,
            body=response.get("body"),
            error=exc,
        )


def _file_id(value: OptionalNullable[str]) -> Optional[str]:
    """Narrow a generated model's ``OptionalNullable[str]`` file id to ``Optional[str]``.

    The generated ``BatchJob`` types its file ids as ``OptionalNullable``, so they carry
    ``UNSET`` as a third state alongside ``str`` and ``None``. The helpers here take
    ``Optional[str]`` and already treat a missing id as "no file" -- ``UNSET`` is falsy,
    so this changes no behaviour, it just states the collapse where a type checker can
    see it instead of relying on truthiness at every call site."""
    return value if isinstance(value, str) else None


def _merge_disjoint(into: dict[str, Any], items: Iterable[Tuple[str, Any]]) -> None:
    """Add ``(custom_id, outcome)`` pairs to ``into``, failing loud on a collision.
    custom_id is unique across a batch's whole output by contract (one line per
    request, appearing in the output OR error file, never both), so a duplicate means
    a broken emitter; overwriting would silently lose an outcome."""
    for custom_id, item in items:
        assert custom_id not in into, (
            f"duplicate custom_id in batch output: {custom_id!r}"
        )
        into[custom_id] = item


@dataclass(frozen=True)
class BatchOutput(Generic[RespBodyT]):
    """A batch's parsed output, split by outcome. Build it from server JSONL via
    ``from_jsonl_bytes``. The three collections are the reference representation:

    * ``responses`` -- ``custom_id -> parsed RespBodyT`` for every successful request.
      Keyed, because a success is only usable if you can attribute it; ``custom_id`` is
      unique across the output (one line per request), so a duplicate fails loud.
    * ``request_errors`` -- the API reported the request failed (an ``error`` on the
      line, or a ``status_code >= 400``).
    * ``response_errors`` -- a response arrived but didn't parse into ``RespBodyT``
      (client-side schema mismatch).

    Errors are lists, not dicts: a failure can legitimately lack a ``custom_id`` (a
    line-level failure the server couldn't attribute), so there's no key to hang it on.
    ``results()`` gives a unified ``custom_id -> outcome`` view for callers that want
    one, dropping the (rare) error with no id.

    No ordering or completeness guarantee: a strict/ordered consumer (e.g. embeddings
    that must align vectors to inputs by position) should use ``ordered(custom_ids)``,
    which returns successes aligned to its own ids and raises ``BatchError`` on any gap
    rather than indexing ``responses`` blindly."""

    responses: dict[str, RespBodyT]
    request_errors: list[BatchRequestError]
    response_errors: list[BatchResponseError]

    @classmethod
    def from_jsonl_bytes(
        cls, raw: bytes, response_body_type: type[RespBodyT]
    ) -> "BatchOutput[RespBodyT]":
        """Parse batch output JSONL (one line per request) into a ``BatchOutput``."""
        responses: dict[str, RespBodyT] = {}
        request_errors: list[BatchRequestError] = []
        response_errors: list[BatchResponseError] = []
        for line in raw.split(b"\n"):
            if not line.strip():
                continue
            custom_id, item = _parse_output_obj(json.loads(line), response_body_type)
            if isinstance(item, BatchRequestError):
                request_errors.append(item)
            elif isinstance(item, BatchResponseError):
                response_errors.append(item)
            elif custom_id is None:
                # A response that parsed cleanly but carries no custom_id: nothing to
                # key it by, and the API always echoes the id, so treat the missing id
                # as the defect and surface it rather than drop a response silently.
                response_errors.append(
                    BatchResponseError(
                        custom_id=None,
                        status_code=None,
                        body=item,
                        error=ValueError("response missing custom_id"),
                    )
                )
            else:
                assert custom_id not in responses, (
                    f"duplicate custom_id in batch output: {custom_id!r}"
                )
                responses[custom_id] = item
        return cls(responses, request_errors, response_errors)

    def results(self) -> dict[str, "BatchItem[RespBodyT]"]:
        """Unified ``custom_id -> outcome`` across all three collections, for callers
        that want one mapping. Errors with no custom_id are dropped (they can't be
        keyed); read them off ``request_errors``/``response_errors`` directly."""
        merged: dict[str, "BatchItem[RespBodyT]"] = dict(self.responses)
        _merge_disjoint(
            merged,
            (
                (err.custom_id, err)
                for err in self._all_errors()
                if err.custom_id is not None
            ),
        )
        return merged

    def ordered(self, custom_ids: Sequence[str]) -> list[RespBodyT]:
        """Successful responses aligned positionally to ``custom_ids`` -- the caller's
        own ids, in the order they want back. All-or-nothing: raises ``BatchError``
        reporting every id with no successful response (each with its recorded error),
        so results can never silently misalign with inputs. The strict, fail-closed
        counterpart to reading ``responses`` directly."""
        return _ordered(self.responses, self._errors_by_id(), custom_ids)

    def _all_errors(self) -> list[Union[BatchRequestError, BatchResponseError]]:
        """Both error collections as one list. Spreading them inline at the use site
        instead makes mypy join the element types to ``object`` rather than to their
        union, which loses ``custom_id``."""
        return [*self.request_errors, *self.response_errors]

    def _errors_by_id(
        self,
    ) -> dict[str, Union[BatchRequestError, BatchResponseError]]:
        errors_by_id: dict[str, Union[BatchRequestError, BatchResponseError]] = {}
        _merge_disjoint(
            errors_by_id,
            (
                (err.custom_id, err)
                for err in self._all_errors()
                if err.custom_id is not None
            ),
        )
        return errors_by_id


@dataclass(frozen=True)
class BatchJobHandle(Generic[RespBodyT]):
    """Pure, serializable snapshot of one created job -- just the ``BatchJob`` data,
    no client reference, so it survives a process/activity boundary (stash
    ``handle.job``, rehydrate with ``BatchClient.get(job_id)``). Drive it through the
    client: ``create``/``get`` return one, and ``wait``/``stream_results``/``output``/
    ``cancel`` take one. ``RespBodyT`` is a phantom marker recording the response-body
    type so the client can type its readers against the bound endpoint.

    Live and one-pass: reads (``stream_results``/``output``) do I/O and can fail, unlike the
    settled ``BatchResult``, whose accessors are sync over data already in hand."""

    job: BatchJob

    @property
    def id(self) -> str:
        return self.job.id

    @property
    def status(self) -> BatchJobStatus:
        return self.job.status


class BatchResult(Generic[RespBodyT]):
    """Settled outcome of ``run``: the job is terminal and the output/error files are
    already downloaded and parsed, so every accessor is sync (no await, no I/O). This
    is deliberately a different type from ``BatchJobHandle`` -- the handle's reads do
    I/O and can fail; a result's cannot."""

    def __init__(
        self,
        job: BatchJob,
        output: BatchOutput[RespBodyT],
        error_output: Optional[BatchOutput[RespBodyT]],
    ) -> None:
        self.job = job
        self._output = output
        self._error_output = error_output

    @property
    def status(self) -> BatchJobStatus:
        return self.job.status

    @property
    def succeeded(self) -> int:
        return self.job.succeeded_requests

    @property
    def failed(self) -> int:
        return self.job.failed_requests

    def output(self) -> BatchOutput[RespBodyT]:
        """The parsed output file (successful responses + inline per-request errors)."""
        return self._output

    def error_output(self) -> Optional[BatchOutput[RespBodyT]]:
        """The parsed error file, or None if the job produced none. Read failures via
        ``.errors()``; ``.by_id()`` is meaningless on it."""
        return self._error_output

    def by_id(self) -> dict[str, RespBodyT]:
        """custom_id -> parsed response body, successful requests only, merged across the
        output and error files. No ordering or completeness guarantee -- strict/ordered
        consumers should use ``ordered(custom_ids)`` instead of indexing this blindly."""
        merged = dict(self._output.responses)
        if self._error_output is not None:
            _merge_disjoint(merged, self._error_output.responses.items())
        return merged

    def errors(self) -> list[BatchRequestError]:
        """Server-reported request failures, concatenated across the output and error
        files. For responses that arrived but didn't parse, see ``response_errors``."""
        errors = list(self._output.request_errors)
        if self._error_output is not None:
            errors.extend(self._error_output.request_errors)
        return errors

    def response_errors(self) -> list[BatchResponseError]:
        """Responses that arrived but couldn't be parsed into ``RespBodyT``,
        concatenated across the output and error files."""
        errors = list(self._output.response_errors)
        if self._error_output is not None:
            errors.extend(self._error_output.response_errors)
        return errors

    def ordered(self, custom_ids: Sequence[str]) -> list[RespBodyT]:
        """Successful responses aligned positionally to ``custom_ids``, merged across the
        output and error files. All-or-nothing: raises ``BatchError`` reporting every id
        with no successful response (see ``BatchOutput.ordered``)."""
        # Annotated rather than spread inline: mypy joins the two element types to
        # ``object`` in a bare unpack, which loses ``custom_id``.
        all_errors: list[Union[BatchRequestError, BatchResponseError]] = [
            *self.errors(),
            *self.response_errors(),
        ]
        errors_by_id: dict[str, Union[BatchRequestError, BatchResponseError]] = {}
        _merge_disjoint(
            errors_by_id,
            ((err.custom_id, err) for err in all_errors if err.custom_id is not None),
        )
        return _ordered(self.by_id(), errors_by_id, custom_ids)


# ---------------------------------------------------------------------------
# Client: lifecycle primitives + run() convenience
# ---------------------------------------------------------------------------


class BatchClient(Generic[ReqBodyT, RespBodyT]):
    """Generic typed client for ONE Batch-API endpoint. Exposes the lifecycle as
    single-shot primitives (``upload``/``create``/``get``/``refresh``/``wait``/
    ``cancel``/``stream_results``/``output``/``download``/``signed_url``/``delete``) plus a
    blocking ``run`` that composes them. The per-endpoint request/response shapes are
    the two type params, bound at construction to the SDK's own models (e.g.
    ``endpoint="/v1/embeddings"``, ``response_body_type=EmbeddingResponse``)."""

    def __init__(
        self,
        client: "Mistral",
        *,
        endpoint: APIEndpoint,
        response_body_type: type[RespBodyT],
    ) -> None:
        self._client = client
        self._endpoint = endpoint
        self._response_body_type = response_body_type

    # -- file primitives ----------------------------------------------------

    async def upload(
        self,
        input: "BatchInput[ReqBodyT]",
        *,
        file_name: str = "batch_input.jsonl",
        expiry_hours: Optional[int] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> "BatchInputFile[ReqBodyT]":
        """Upload input JSONL and return its file handle."""
        kwargs: dict[str, Any] = {"purpose": "batch"}
        if expiry_hours is not None:
            kwargs["expiry"] = expiry_hours
        if timeout_ms is not None:
            kwargs["timeout_ms"] = timeout_ms
        if http_headers is not None:
            kwargs["http_headers"] = http_headers
        response = await self._client.files.upload_async(
            file=File(file_name=file_name, content=input.to_jsonl_bytes()), **kwargs
        )
        return BatchInputFile(response.id)

    async def download(
        self, file_id: str, *, http_headers: Optional[Mapping[str, str]] = None
    ) -> bytes:
        """Download a result/error file's bytes in full."""
        response = await self._client.files.download_async(
            file_id=file_id, **self._headers_kwarg(http_headers)
        )
        return await stream_to_bytes_async(response)

    async def signed_url(
        self,
        file_id: str,
        *,
        expiry_hours: int = 24,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> str:
        """A temporary signed URL for a file, to stream large results directly."""
        response = await self._client.files.get_signed_url_async(
            file_id=file_id, expiry=expiry_hours, **self._headers_kwarg(http_headers)
        )
        return response.url

    async def delete(
        self, file_id: str, *, http_headers: Optional[Mapping[str, str]] = None
    ) -> None:
        """Delete a batch file (input, output, or error)."""
        await self._client.files.delete_async(
            file_id=file_id, **self._headers_kwarg(http_headers)
        )

    # -- job primitives -----------------------------------------------------

    async def create(
        self,
        input: Union["BatchInput[ReqBodyT]", "BatchInputFile[ReqBodyT]"],
        *,
        model: Optional[str] = None,
        metadata: Optional[dict[str, str]] = None,
        timeout_hours: int = 24,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> "BatchJobHandle[RespBodyT]":
        """Create a job and return a handle. A ``BatchInputFile`` runs from the
        uploaded file; a ``BatchInput`` is sent inline (no upload) -- upload large
        inputs first."""
        kwargs: dict[str, Any] = {
            "endpoint": self._endpoint,
            "timeout_hours": timeout_hours,
        }
        if model is not None:
            kwargs["model"] = model
        if metadata is not None:
            kwargs["metadata"] = metadata
        if http_headers is not None:
            kwargs["http_headers"] = http_headers
        if isinstance(input, BatchInputFile):
            kwargs["input_files"] = [input.file_id]
        else:
            kwargs["requests"] = input.to_requests()
        job = await self._client.batch.jobs.create_async(**kwargs)
        return BatchJobHandle(job)

    async def get(
        self, job_id: str, *, http_headers: Optional[Mapping[str, str]] = None
    ) -> "BatchJobHandle[RespBodyT]":
        """Fetch a job's current state once (no polling) and wrap it in a handle.
        This is how you rehydrate a handle for a job created in a prior process."""
        job = await self._client.batch.jobs.get_async(
            job_id=job_id, **self._headers_kwarg(http_headers)
        )
        return BatchJobHandle(job)

    async def refresh(
        self,
        handle: Union["BatchJobHandle[RespBodyT]", str],
        *,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> "BatchJobHandle[RespBodyT]":
        """Re-fetch a job's state, returning a fresh handle."""
        return await self.get(self._job_id(handle), http_headers=http_headers)

    async def cancel(
        self,
        handle: Union["BatchJobHandle[RespBodyT]", str],
        *,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> "BatchJobHandle[RespBodyT]":
        """Request cancellation of a job. Returns its updated handle: the job first
        moves to CANCELLATION_REQUESTED (still in-flight, see ``RUNNING_STATUSES``)
        then settles on CANCELLED. Poll with ``wait``/``refresh`` to observe it."""
        job = await self._client.batch.jobs.cancel_async(
            job_id=self._job_id(handle), **self._headers_kwarg(http_headers)
        )
        return BatchJobHandle(job)

    async def wait(
        self,
        handle: Union["BatchJobHandle[RespBodyT]", str],
        *,
        poll_interval_seconds: float = 30.0,
        timeout_hours: int = 24,
        deadline: Optional[float] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> "BatchJobHandle[RespBodyT]":
        """Poll until the job reaches a terminal state, returning the terminal handle.
        Pass ``deadline`` (a ``time.monotonic()`` value) to enforce a wall-clock cap
        shared across several calls; otherwise it is derived from ``timeout_hours``."""
        job_id = self._job_id(handle)
        if deadline is None:
            deadline = time.monotonic() + timeout_hours * 3600
        while True:
            current = await self.get(job_id, http_headers=http_headers)
            if is_terminal(current.status):
                return current
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f"Batch job {job_id} timed out while polling")
            await asyncio.sleep(min(poll_interval_seconds, remaining))

    # -- job readers --------------------------------------------------------

    async def stream_results(
        self,
        handle: "BatchJobHandle[RespBodyT]",
        *,
        poll_interval_seconds: float = 30.0,
        timeout_hours: int = 24,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> AsyncIterator[Tuple[Optional[str], "BatchItem[RespBodyT]"]]:
        """Stream ``(custom_id, outcome)`` for an existing job one line at a time,
        without ever holding the whole output file in memory. Each outcome is a typed
        ``RespBodyT``, a ``BatchRequestError``, or a ``BatchResponseError`` (see
        ``BatchOutput``). Waits for the job to settle first if it hasn't.

        Binds to a job the caller already owns (create it via ``create``, or upload +
        ``create``, and pass the handle). It reads only -- it never uploads, creates,
        cancels, or deletes -- so the caller owns the job and its files. This is the
        deliberate split from ``run``: ``run`` composes the whole lifecycle and can
        delete the server files it created because it materializes their bytes first;
        a stream never materializes, so it cannot safely own that lifecycle and does
        not try to.

        For random access (``by_id``) or whole-job retry, use ``run`` instead -- retry
        is transactional and cannot be expressed once results have been yielded out.

        The contract is "every item exactly once, as an async stream" -- NOT *when*.
        Today that means: wait to terminal, then stream the file line by line. If the
        server later exposes results incrementally, only this method's internals
        change; the caller's ``async for`` stays the same."""
        handle = await self._ensure_terminal(
            handle,
            poll_interval_seconds=poll_interval_seconds,
            timeout_hours=timeout_hours,
            http_headers=http_headers,
        )
        async for item in self._stream_file(_file_id(handle.job.output_file), http_headers):
            yield item
        async for item in self._stream_file(_file_id(handle.job.error_file), http_headers):
            yield item

    async def output(
        self,
        handle: "BatchJobHandle[RespBodyT]",
        *,
        poll_interval_seconds: float = 30.0,
        timeout_hours: int = 24,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> BatchOutput[RespBodyT]:
        """Download and parse the whole output file (random access via
        ``by_id()``/``errors()``). Waits for the job to settle first if it hasn't. For
        very large results, prefer ``stream_results`` to avoid loading it all at once."""
        handle = await self._ensure_terminal(
            handle,
            poll_interval_seconds=poll_interval_seconds,
            timeout_hours=timeout_hours,
            http_headers=http_headers,
        )
        raw = await self._download_optional(_file_id(handle.job.output_file), http_headers)
        return BatchOutput.from_jsonl_bytes(raw, self._response_body_type)

    async def error_output(
        self,
        handle: "BatchJobHandle[RespBodyT]",
        *,
        poll_interval_seconds: float = 30.0,
        timeout_hours: int = 24,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> Optional[BatchOutput[RespBodyT]]:
        """The parsed error file, or None if the job produced none. Waits first."""
        handle = await self._ensure_terminal(
            handle,
            poll_interval_seconds=poll_interval_seconds,
            timeout_hours=timeout_hours,
            http_headers=http_headers,
        )
        if not handle.job.error_file:
            return None
        raw = await self.download(handle.job.error_file, http_headers=http_headers)
        return BatchOutput.from_jsonl_bytes(raw, self._response_body_type)

    # -- convenience --------------------------------------------------------

    async def run(
        self,
        input: Union[
            "BatchInput[ReqBodyT]",
            "BatchInputFile[ReqBodyT]",
            dict[str, ReqBodyT],
            bytes,
            str,
        ],
        *,
        model: Optional[str] = None,
        metadata: Optional[dict[str, str]] = None,
        timeout_hours: int = 24,
        poll_interval_seconds: float = 30.0,
        max_failed_job_retries: int = 0,
        inline_threshold: int = 1000,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> BatchResult[RespBodyT]:
        """Run a batch end to end, blocking until the job reaches a terminal state,
        then materialize the output/error files into a ``BatchResult`` (sync access).

        Composes the primitives: small ``BatchInput`` content is sent inline, larger
        content (over ``inline_threshold`` requests) is uploaded first; a
        ``BatchInputFile`` is used as-is. Raw ``dict``/``bytes``/``str`` are accepted
        for convenience and wrapped in a ``BatchInput``. Polls until terminal or the
        ``timeout_hours`` deadline.

        ``inline_threshold`` counts *requests*, not bytes -- the real inline limit is
        payload size, so a modest request count with large bodies can still exceed it.
        Lower the threshold (or ``upload`` first and pass the ``BatchInputFile``) when
        bodies are big.

        ``max_failed_job_retries`` re-runs the WHOLE job on the same input while any
        request failed -- every request is resubmitted and re-billed, not just the
        failures. Leave it at 0 and drive partial retries yourself (rebuild a
        ``BatchInput`` from ``result.errors()``) when that cost matters. The whole-job
        retry is why ``run`` returns a materialized result rather than a handle: it is
        transactional (wait for the whole thing, retry the whole thing), which cannot
        be expressed once results have been streamed out incrementally.

        Cleans up the server-side files it creates: the input file it uploaded (a
        caller-supplied ``BatchInputFile`` is left alone) and every attempt's
        output/error files, whose bytes are already materialized into the result. If
        the job is still running when ``run`` aborts (timeout, or the coroutine is
        cancelled), it best-effort ``cancel``s it so it doesn't keep billing.

        For a decomposed lifecycle (Temporal activity polled by a retry policy, or
        create-now-retrieve-later), use ``create``/``get``/``wait``/``stream_results`` instead.
        """
        source = await self._prepare_source(
            input, inline_threshold=inline_threshold, http_headers=http_headers
        )
        # The input file run() uploaded is ours to clean up (a caller-supplied
        # BatchInputFile is the caller's input -- left alone). Deletion happens on the
        # success path only, once everything is materialized into ``result``: never in
        # a failure path, so an abort leaves the input and every attempt's output/error
        # files recoverable rather than destroying a completed job's only copy.
        created_input = (
            source.file_id
            if isinstance(source, BatchInputFile)
            and not isinstance(input, BatchInputFile)
            else None
        )
        result_files: list[Optional[str]] = []

        deadline = time.monotonic() + timeout_hours * 3600
        handle: Optional[BatchJobHandle[RespBodyT]] = None
        try:
            for _ in range(max_failed_job_retries + 1):
                remaining_hours = math.ceil((deadline - time.monotonic()) / 3600)
                if remaining_hours <= 0:
                    raise TimeoutError("Batch job timed out before completion")
                handle = await self.create(
                    source,
                    model=model,
                    metadata=metadata,
                    timeout_hours=remaining_hours,
                    http_headers=http_headers,
                )
                handle = await self.wait(
                    handle,
                    poll_interval_seconds=poll_interval_seconds,
                    deadline=deadline,
                    http_headers=http_headers,
                )
                result_files += [
                    _file_id(handle.job.output_file),
                    _file_id(handle.job.error_file),
                ]
                if handle.job.failed_requests == 0:
                    break
            assert handle is not None
            output = await self.output(handle, http_headers=http_headers)
            error_output = await self.error_output(handle, http_headers=http_headers)
            result = BatchResult(handle.job, output, error_output)
        except (Exception, asyncio.CancelledError):
            # run() is transactional: on any failure it returns no resumable handle, so
            # cancel a still-running job (stop billing) and delete the input it can no
            # longer read. The result files are left in place -- they may still be
            # downloadable, and a failed download must not destroy a completed job's
            # only copy of its output.
            if handle is not None and is_running(handle.status):
                await self._cancel_quietly(handle, http_headers)
            if created_input is not None:
                await self._delete_quietly(created_input, http_headers)
            raise
        # Success: the result files are materialized into ``result`` (superseded
        # attempts' files are discarded orphans), so the server copies -- and the input
        # file run() uploaded -- are now safe to delete.
        await self._delete_files_quietly([*result_files, created_input], http_headers)
        return result

    # -- internals ----------------------------------------------------------

    @staticmethod
    def _headers_kwarg(
        http_headers: Optional[Mapping[str, str]],
    ) -> dict[str, Any]:
        return {} if http_headers is None else {"http_headers": http_headers}

    @staticmethod
    def _job_id(handle: Union["BatchJobHandle[RespBodyT]", str]) -> str:
        return handle if isinstance(handle, str) else handle.id

    @staticmethod
    def _coerce(
        input: Union[
            "BatchInput[ReqBodyT]",
            "BatchInputFile[ReqBodyT]",
            dict[str, ReqBodyT],
            bytes,
            str,
        ],
    ) -> Union["BatchInput[ReqBodyT]", "BatchInputFile[ReqBodyT]"]:
        if isinstance(input, (BatchInput, BatchInputFile)):
            return input
        if isinstance(input, dict):
            return BatchInput.from_payload(input)
        if isinstance(input, bytes):
            return BatchInput.from_jsonl_bytes(input)
        if isinstance(input, str):
            return BatchInput.from_jsonl_str(input)
        raise TypeError(f"unsupported batch input: {type(input).__name__}")

    async def _prepare_source(
        self,
        input: Union[
            "BatchInput[ReqBodyT]",
            "BatchInputFile[ReqBodyT]",
            dict[str, ReqBodyT],
            bytes,
            str,
        ],
        *,
        inline_threshold: int,
        http_headers: Optional[Mapping[str, str]],
    ) -> Union["BatchInput[ReqBodyT]", "BatchInputFile[ReqBodyT]"]:
        """Coerce raw input to a BatchInput/BatchInputFile, uploading it first when it
        has more than ``inline_threshold`` requests."""
        source = self._coerce(input)
        if isinstance(source, BatchInput) and len(source) > inline_threshold:
            source = await self.upload(source, http_headers=http_headers)
        return source

    async def _ensure_terminal(
        self,
        handle: "BatchJobHandle[RespBodyT]",
        *,
        poll_interval_seconds: float,
        timeout_hours: int,
        http_headers: Optional[Mapping[str, str]],
    ) -> "BatchJobHandle[RespBodyT]":
        if is_terminal(handle.status):
            return handle
        return await self.wait(
            handle,
            poll_interval_seconds=poll_interval_seconds,
            timeout_hours=timeout_hours,
            http_headers=http_headers,
        )

    async def _delete_quietly(
        self, file_id: str, http_headers: Optional[Mapping[str, str]]
    ) -> None:
        """Best-effort file delete for run()'s cleanup -- a failed delete must never
        mask the real result (or the real exception on the abort path)."""
        try:
            await self.delete(file_id, http_headers=http_headers)
        except Exception:
            pass

    async def _delete_files_quietly(
        self,
        file_ids: Iterable[Optional[str]],
        http_headers: Optional[Mapping[str, str]],
    ) -> None:
        """Best-effort delete of several files, skipping the empty/None ones."""
        for file_id in file_ids:
            if file_id:
                await self._delete_quietly(file_id, http_headers)

    async def _cancel_quietly(
        self,
        handle: "BatchJobHandle[RespBodyT]",
        http_headers: Optional[Mapping[str, str]],
    ) -> None:
        """Best-effort cancel when run() aborts. Shielded so that a caller cancelling
        the run() coroutine can't interrupt the cancel request itself (on a plain
        TimeoutError there's nothing to shield against and it runs to completion)."""
        try:
            await asyncio.shield(self.cancel(handle, http_headers=http_headers))
        except Exception:
            pass

    async def _download_optional(
        self, file_id: Optional[str], http_headers: Optional[Mapping[str, str]]
    ) -> bytes:
        if not file_id:
            return b""
        return await self.download(file_id, http_headers=http_headers)

    async def _stream_file(
        self, file_id: Optional[str], http_headers: Optional[Mapping[str, str]]
    ) -> AsyncIterator[Tuple[Optional[str], "BatchItem[RespBodyT]"]]:
        if not file_id:
            return
        response = await self._client.files.download_async(
            file_id=file_id, **self._headers_kwarg(http_headers)
        )
        try:
            async for line in response.aiter_lines():
                if not line.strip():
                    continue
                yield _parse_output_obj(json.loads(line), self._response_body_type)
        finally:
            await response.aclose()
