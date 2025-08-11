import re
from invoke.context import Context
from invoke.tasks import task
from scripts.update_speakeasy import (
    pin_speakeasy_version,
    OpenAPISpecsPinned,
    SpeakeasyTargets,
    WORKFLOW_PATH,
    WORKFLOW_LOCK_PATH,
)


@task(iterable=["targets"])
def update_speakeasy(
    ctx: Context,
    version: str,
    targets: list[SpeakeasyTargets] = [SpeakeasyTargets.ALL],
    workflow_path: str = WORKFLOW_PATH,
    workflow_lock_path: str = WORKFLOW_LOCK_PATH,
    verbose: bool = False,
):
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        raise ValueError(f"Invalid version format: {version}. Expected format: X.Y.Z (e.g., 1.2.3)")
    """
    Update the speakeasy version and pin the openapi specs to the current revision.

    Usage:
        inv update-speakeasy --version "1.580.2" --targets "all"
        inv update-speakeasy --version "1.580.2" --targets "mistralai-azure-sdk" --targets "mistralai-gcp-sdk" --verbose
        inv update-speakeasy --version "1.580.2" --targets "mistralai-sdk" --workflow-path ".speakeasy/workflow.yaml" --workflow-lock-path ".speakeasy/workflow.lock.yaml"
        inv update-speakeasy --version "1.580.2" --targets "mistralai-sdk" --workflow-path ".speakeasy/workflow.yaml" --workflow-lock-path ".speakeasy/workflow.lock.yaml" --verbose
    """
    for target in targets:
        try:
            SpeakeasyTargets(target)
        except ValueError:
            raise ValueError(
                f"Invalid target: {target}. Your targets must be one of {SpeakeasyTargets.list()}"
            )
    cmd = (
        "speakeasy run"
        + " --skip-versioning"
        + "".join(f" -t {target}" for target in targets)
        + (" --verbose" if verbose else "")
    )
    pin_speakeasy_version(workflow_path=workflow_path, version=version)
    with OpenAPISpecsPinned(workflow_path, workflow_lock_path):
        ctx.run(cmd)
