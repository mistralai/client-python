import sys

try:
    import mistralai_workflows
    sys.modules[__name__] = mistralai_workflows
except ImportError as exc:
    raise ImportError(
        "mistralai-workflows not installed. Run: pip install 'mistralai-workflows'"
    ) from exc
