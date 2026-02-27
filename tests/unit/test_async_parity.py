"""Introspection tests verifying every sync public method has an async counterpart."""

import asyncio
import inspect

import pytest


def _collect_pairs():
    """Dynamically collect (class, sync_method, async_method) triples.

    Only includes pairs where the sync method actually exists on the class.
    Gracefully skips classes that cannot be imported.
    """
    pairs = []
    class_specs = [
        (
            "mistralai.client.chat",
            "Chat",
            [
                ("complete", "complete_async"),
                ("stream", "stream_async"),
                ("parse", "parse_async"),
                ("parse_stream", "parse_stream_async"),
            ],
        ),
        (
            "mistralai.client.agents",
            "Agents",
            [
                ("complete", "complete_async"),
                ("stream", "stream_async"),
            ],
        ),
        (
            "mistralai.client.fim",
            "Fim",
            [
                ("complete", "complete_async"),
                ("stream", "stream_async"),
            ],
        ),
        (
            "mistralai.client.embeddings",
            "Embeddings",
            [
                ("create", "create_async"),
            ],
        ),
        (
            "mistralai.client.files",
            "Files",
            [
                ("upload", "upload_async"),
                ("list", "list_async"),
                ("retrieve", "retrieve_async"),
                ("delete", "delete_async"),
                ("download", "download_async"),
                ("get_signed_url", "get_signed_url_async"),
            ],
        ),
        (
            "mistralai.client.models_",
            "Models",
            [
                ("list", "list_async"),
                ("retrieve", "retrieve_async"),
                ("delete", "delete_async"),
                ("update", "update_async"),
                ("archive", "archive_async"),
                ("unarchive", "unarchive_async"),
            ],
        ),
        (
            "mistralai.client.batch_jobs",
            "BatchJobs",
            [
                ("list", "list_async"),
                ("create", "create_async"),
                ("get", "get_async"),
                ("cancel", "cancel_async"),
            ],
        ),
        (
            "mistralai.client.fine_tuning_jobs",
            "FineTuningJobs",
            [
                ("list", "list_async"),
                ("create", "create_async"),
                ("get", "get_async"),
                ("cancel", "cancel_async"),
                ("start", "start_async"),
            ],
        ),
        (
            "mistralai.client.classifiers",
            "Classifiers",
            [
                ("moderate", "moderate_async"),
                ("moderate_chat", "moderate_chat_async"),
                ("classify", "classify_async"),
                ("classify_chat", "classify_chat_async"),
            ],
        ),
        (
            "mistralai.client.ocr",
            "Ocr",
            [
                ("process", "process_async"),
            ],
        ),
        (
            "mistralai.client.beta_agents",
            "BetaAgents",
            [
                ("create", "create_async"),
                ("list", "list_async"),
                ("get", "get_async"),
                ("update", "update_async"),
                ("delete", "delete_async"),
                ("update_version", "update_version_async"),
                ("list_versions", "list_versions_async"),
                ("get_version", "get_version_async"),
                ("create_version_alias", "create_version_alias_async"),
                ("list_version_aliases", "list_version_aliases_async"),
                ("delete_version_alias", "delete_version_alias_async"),
            ],
        ),
        (
            "mistralai.client.conversations",
            "Conversations",
            [
                ("start", "start_async"),
                ("list", "list_async"),
                ("get", "get_async"),
                ("delete", "delete_async"),
                ("append", "append_async"),
                ("get_history", "get_history_async"),
                ("get_messages", "get_messages_async"),
                ("restart", "restart_async"),
                ("start_stream", "start_stream_async"),
                ("append_stream", "append_stream_async"),
                ("restart_stream", "restart_stream_async"),
            ],
        ),
        (
            "mistralai.client.documents",
            "Documents",
            [
                ("list", "list_async"),
                ("upload", "upload_async"),
                ("get", "get_async"),
                ("update", "update_async"),
                ("delete", "delete_async"),
                ("text_content", "text_content_async"),
                ("status", "status_async"),
                ("get_signed_url", "get_signed_url_async"),
                ("extracted_text_signed_url", "extracted_text_signed_url_async"),
                ("reprocess", "reprocess_async"),
            ],
        ),
        (
            "mistralai.client.libraries",
            "Libraries",
            [
                ("list", "list_async"),
                ("create", "create_async"),
                ("get", "get_async"),
                ("delete", "delete_async"),
                ("update", "update_async"),
            ],
        ),
        (
            "mistralai.client.accesses",
            "Accesses",
            [
                ("list", "list_async"),
                ("update_or_create", "update_or_create_async"),
                ("delete", "delete_async"),
            ],
        ),
        (
            "mistralai.client.transcriptions",
            "Transcriptions",
            [
                ("complete", "complete_async"),
                ("stream", "stream_async"),
            ],
        ),
    ]
    for module_path, class_name, methods in class_specs:
        try:
            mod = __import__(module_path, fromlist=[class_name])
            klass = getattr(mod, class_name)
        except (ImportError, AttributeError):
            continue
        for sync_name, async_name in methods:
            if hasattr(klass, sync_name):
                pairs.append((klass, sync_name, async_name))
    return pairs


SYNC_ASYNC_PAIRS = _collect_pairs()


def _pair_id(val):
    """Generate a readable parametrize ID."""
    if isinstance(val, tuple):
        klass, sync_name, _ = val
        return f"{klass.__name__}.{sync_name}"
    return None


@pytest.mark.parametrize(
    "klass,sync_name,async_name",
    SYNC_ASYNC_PAIRS,
    ids=[f"{p[0].__name__}.{p[1]}" for p in SYNC_ASYNC_PAIRS],
)
class TestAsyncParity:
    """Verify that every sync public method has a matching async counterpart."""

    def test_async_method_exists(self, klass, sync_name, async_name):
        """The async counterpart must exist on the class."""
        assert hasattr(klass, async_name), (
            f"{klass.__name__}.{async_name} is missing "
            f"(expected async counterpart of {sync_name})"
        )

    def test_parameter_names_match(self, klass, sync_name, async_name):
        """Parameter names (excluding 'self') must match between sync and async."""
        if not hasattr(klass, async_name):
            pytest.skip(f"{klass.__name__}.{async_name} does not exist")

        sync_method = getattr(klass, sync_name)
        async_method = getattr(klass, async_name)

        sync_sig = inspect.signature(sync_method)
        async_sig = inspect.signature(async_method)

        sync_params = [
            name
            for name in sync_sig.parameters
            if name != "self"
        ]
        async_params = [
            name
            for name in async_sig.parameters
            if name != "self"
        ]

        assert sync_params == async_params, (
            f"{klass.__name__}: parameter mismatch between "
            f"{sync_name}{sync_params} and {async_name}{async_params}"
        )

    def test_async_is_coroutine(self, klass, sync_name, async_name):
        """The async method must be a coroutine function."""
        if not hasattr(klass, async_name):
            pytest.skip(f"{klass.__name__}.{async_name} does not exist")

        async_method = getattr(klass, async_name)
        assert asyncio.iscoroutinefunction(async_method) or inspect.isasyncgenfunction(async_method), (
            f"{klass.__name__}.{async_name} is not a coroutine function "
            f"or async generator function"
        )
