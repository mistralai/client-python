import contextlib
import unittest.mock as mock
from typing import Any, Dict, List

import orjson
from httpx import Response


@contextlib.contextmanager
def mock_stream_response(status_code: int, content: List[str], headers: Dict[str, Any] = None):
    response = mock.Mock(Response)
    response.status_code = status_code
    response.headers = headers if headers else {}
    response.iter_lines.return_value = iter(content)
    yield response


@contextlib.asynccontextmanager
async def mock_async_stream_response(status_code: int, content: List[str], headers: Dict[str, Any] = None):
    response = mock.Mock(Response)
    response.status_code = status_code
    response.headers = headers if headers else {}

    async def async_iter(content: List[str]):
        for line in content:
            yield line

    response.aiter_lines.return_value = async_iter(content)
    yield response


def mock_response(
    status_code: int, content: str, headers: Dict[str, Any] = None, is_json: bool = True
) -> mock.MagicMock:
    response = mock.Mock(Response)
    response.status_code = status_code
    response.headers = headers if headers else {}
    if is_json:
        response.json = mock.MagicMock()
        response.json.return_value = orjson.loads(content)
    response.text = content
    return response


def mock_list_models_response_payload() -> str:
    return orjson.dumps(
        {
            "object": "list",
            "data": [
                {
                    "id": "mistral-medium",
                    "object": "model",
                    "created": 1703186988,
                    "owned_by": "mistralai",
                    "root": None,
                    "parent": None,
                    "permission": [
                        {
                            "id": "modelperm-15bebaf316264adb84b891bf06a84933",
                            "object": "model_permission",
                            "created": 1703186988,
                            "allow_create_engine": False,
                            "allow_sampling": True,
                            "allow_logprobs": False,
                            "allow_search_indices": False,
                            "allow_view": True,
                            "allow_fine_tuning": False,
                            "organization": "*",
                            "group": None,
                            "is_blocking": False,
                        }
                    ],
                },
                {
                    "id": "mistral-small-latest",
                    "object": "model",
                    "created": 1703186988,
                    "owned_by": "mistralai",
                    "root": None,
                    "parent": None,
                    "permission": [
                        {
                            "id": "modelperm-d0dced5c703242fa862f4ca3f241c00e",
                            "object": "model_permission",
                            "created": 1703186988,
                            "allow_create_engine": False,
                            "allow_sampling": True,
                            "allow_logprobs": False,
                            "allow_search_indices": False,
                            "allow_view": True,
                            "allow_fine_tuning": False,
                            "organization": "*",
                            "group": None,
                            "is_blocking": False,
                        }
                    ],
                },
                {
                    "id": "mistral-tiny",
                    "object": "model",
                    "created": 1703186988,
                    "owned_by": "mistralai",
                    "root": None,
                    "parent": None,
                    "permission": [
                        {
                            "id": "modelperm-0e64e727c3a94f17b29f8895d4be2910",
                            "object": "model_permission",
                            "created": 1703186988,
                            "allow_create_engine": False,
                            "allow_sampling": True,
                            "allow_logprobs": False,
                            "allow_search_indices": False,
                            "allow_view": True,
                            "allow_fine_tuning": False,
                            "organization": "*",
                            "group": None,
                            "is_blocking": False,
                        }
                    ],
                },
                {
                    "id": "mistral-embed",
                    "object": "model",
                    "created": 1703186988,
                    "owned_by": "mistralai",
                    "root": None,
                    "parent": None,
                    "permission": [
                        {
                            "id": "modelperm-ebdff9046f524e628059447b5932e3ad",
                            "object": "model_permission",
                            "created": 1703186988,
                            "allow_create_engine": False,
                            "allow_sampling": True,
                            "allow_logprobs": False,
                            "allow_search_indices": False,
                            "allow_view": True,
                            "allow_fine_tuning": False,
                            "organization": "*",
                            "group": None,
                            "is_blocking": False,
                        }
                    ],
                },
            ],
        }
    )


def mock_embedding_response_payload(batch_size: int = 1) -> str:
    return orjson.dumps(
        {
            "id": "embd-98c8c60e3fbf4fc49658eddaf447357c",
            "object": "list",
            "data": [
                {
                    "object": "embedding",
                    "embedding": [-0.018585205078125, 0.027099609375, 0.02587890625],
                    "index": 0,
                }
            ]
            * batch_size,
            "model": "mistral-embed",
            "usage": {"prompt_tokens": 90, "total_tokens": 90, "completion_tokens": 0},
        }
    ).decode()


def mock_chat_response_payload():
    return orjson.dumps(
        {
            "id": "chat-98c8c60e3fbf4fc49658eddaf447357c",
            "object": "chat.completion",
            "created": 1703165682,
            "choices": [
                {
                    "finish_reason": "stop",
                    "message": {
                        "role": "assistant",
                        "content": "What is the best French cheese?",
                    },
                    "index": 0,
                }
            ],
            "model": "mistral-small-latest",
            "usage": {"prompt_tokens": 90, "total_tokens": 90, "completion_tokens": 0},
        }
    ).decode()


def mock_chat_response_streaming_payload():
    return [
        "data: "
        + orjson.dumps(
            {
                "id": "cmpl-8cd9019d21ba490aa6b9740f5d0a883e",
                "model": "mistral-small-latest",
                "choices": [
                    {
                        "index": 0,
                        "delta": {"role": "assistant"},
                        "finish_reason": None,
                    }
                ],
            }
        ).decode()
        + "\n\n",
        *[
            "data: "
            + orjson.dumps(
                {
                    "id": "cmpl-8cd9019d21ba490aa6b9740f5d0a883e",
                    "object": "chat.completion.chunk",
                    "created": 1703168544,
                    "model": "mistral-small-latest",
                    "choices": [
                        {
                            "index": i,
                            "delta": {"content": f"stream response {i}"},
                            "finish_reason": None,
                        }
                    ],
                }
            ).decode()
            + "\n\n"
            for i in range(10)
        ],
        "data: [DONE]\n\n",
    ]


def mock_completion_response_payload() -> str:
    return orjson.dumps(
        {
            "id": "chat-98c8c60e3fbf4fc49658eddaf447357c",
            "object": "chat.completion",
            "created": 1703165682,
            "choices": [
                {
                    "finish_reason": "stop",
                    "message": {
                        "role": "assistant",
                        "content": "  a + b",
                    },
                    "index": 0,
                }
            ],
            "model": "mistral-small-latest",
            "usage": {"prompt_tokens": 90, "total_tokens": 90, "completion_tokens": 0},
        }
    ).decode()


def mock_job_response_payload() -> str:
    return orjson.dumps(
        {
            "id": "job_id",
            "hyperparameters": {
                "training_steps": 1800,
                "learning_rate": 1.0e-4,
            },
            "fine_tuned_model": "fine_tuned_model",
            "model": "model",
            "status": "QUEUED",
            "job_type": "job_type",
            "created_at": 1633046400000,
            "modified_at": 1633046400000,
            "training_files": ["training_file_id"],
            "validation_files": ["validation_file_id"],
            "object": "job",
            "integrations": [],
        }
    )


def mock_detailed_job_response_payload() -> str:
    return orjson.dumps(
        {
            "id": "job_id",
            "hyperparameters": {
                "training_steps": 1800,
                "learning_rate": 1.0e-4,
            },
            "fine_tuned_model": "fine_tuned_model",
            "model": "model",
            "status": "QUEUED",
            "job_type": "job_type",
            "created_at": 1633046400000,
            "modified_at": 1633046400000,
            "training_files": ["training_file_id"],
            "validation_files": ["validation_file_id"],
            "object": "job",
            "integrations": [],
            "events": [
                {
                    "name": "event_name",
                    "created_at": 1633046400000,
                }
            ],
        }
    )


def mock_file_response_payload() -> str:
    return orjson.dumps(
        {
            "id": "file_id",
            "object": "file",
            "bytes": 0,
            "created_at": 1633046400000,
            "filename": "file.jsonl",
            "purpose": "fine-tune",
        }
    )


def mock_file_deleted_response_payload() -> str:
    return orjson.dumps(
        {
            "id": "file_id",
            "object": "file",
            "deleted": True,
        }
    )


def mock_model_deleted_response_payload() -> str:
    return orjson.dumps(
        {
            "id": "model_id",
            "object": "model",
            "deleted": True,
        }
    )
