"""
This script:
- pins the OpenAPI specs,
- runs speakeasy to update the SDKs' files,
- and then unpins the OpenAPI specs.

It is advised to often run this script to avoid getting unrelated changes (due to updates) when modifying the OpenAPI specs.
"""

import yaml
from io import TextIOWrapper
import copy
import subprocess

WORKFLOW_PATH = ".speakeasy/workflow.yaml"
WORKFLOW_LOCK_PATH = ".speakeasy/workflow.lock"


def set_location_rev(yaml_content: dict, source_name: str, new_rev: str) -> None:
    registry = yaml_content["sources"][source_name]["inputs"][0]["location"].split(":")[0]
    yaml_content["sources"][source_name]["inputs"][0]["location"] = f"{registry}:{new_rev}"


def write_yaml(yaml_content: dict, file: TextIOWrapper) -> None:
    return yaml.dump(
        yaml_content, file, default_flow_style=False, sort_keys=False, indent=4
    )

def pin_speakeasy_version(workflow_path: str, version: str):
    with open(workflow_path, "r") as file:
        workflow_yaml = yaml.safe_load(file)
    workflow_yaml["speakeasyVersion"] = version
    with open(workflow_path, "w") as file:
        write_yaml(workflow_yaml, file)

class OpenAPISpecsPinned:
    def __init__(self, workflow_path: str, workflow_lock_path: str):
        self.workflow_path = workflow_path
        self.workflow_lock_path = workflow_lock_path
        with open(workflow_path, "r") as file:
            self.workflow_yaml = yaml.safe_load(file)

    def __enter__(self):
        print("OpenAPI specs pinned to current revision")
        self.pin_to_current_rev()

    def __exit__(self, exc_type, exc_value, traceback):
        self.unpin()
        print("OpenAPI specs unpinned")

    def pin_to_current_rev(self):
        yaml_copy = copy.deepcopy(self.workflow_yaml)
        # Getting the current revisions of the OpenAPI specs
        with open(self.workflow_lock_path, "r") as lock_file:
            yaml_lock = yaml.safe_load(lock_file)
            rev_azure = yaml_lock["sources"]["mistral-azure-source"]["sourceRevisionDigest"]
            rev_google_cloud = yaml_lock["sources"]["mistral-google-cloud-source"]["sourceRevisionDigest"]
            rev_mistralai = yaml_lock["sources"]["mistral-openapi"]["sourceRevisionDigest"]

        # Pinning the OpenAPI specs to the current revisions
        with open(self.workflow_path, "w") as file:
            set_location_rev(yaml_copy, "mistral-azure-source", rev_azure)
            set_location_rev(yaml_copy, "mistral-google-cloud-source", rev_google_cloud)
            set_location_rev(yaml_copy, "mistral-openapi", rev_mistralai)
            write_yaml(yaml_content=yaml_copy, file=file)


    def unpin(self):
        with open(self.workflow_path, "w") as file:
            write_yaml(yaml_content=self.workflow_yaml, file=file)

if __name__ == "__main__":
    pin_speakeasy_version(workflow_path=WORKFLOW_PATH, version="1.580.2")
    with OpenAPISpecsPinned(WORKFLOW_PATH, WORKFLOW_LOCK_PATH):
        subprocess.run(["speakeasy", "run", "-t", "mistralai-sdk", "--skip-versioning", "--verbose"])
