.PHONY: help test-generate update-speakeasy-version

help:
	@echo "Available targets:"
	@echo "  make test-generate                            Test SDK generation locally"
	@echo "  make update-speakeasy-version VERSION=x.y.z   Update Speakeasy CLI version"
	@echo ""
	@echo "Note: Production SDK generation is done via GitHub Actions:"
	@echo "  .github/workflows/sdk_generation_mistralai_sdk.yaml"

# Test SDK generation locally.
# For production, use GitHub Actions: .github/workflows/sdk_generation_mistralai_sdk.yaml
# This uses the Speakeasy CLI version defined in .speakeasy/workflow.yaml
test-generate:
	speakeasy run --skip-versioning

# Update the Speakeasy CLI version (the code generator tool).
# This modifies speakeasyVersion in .speakeasy/workflow.yaml and regenerates the SDK.
# Usage: make update-speakeasy-version VERSION=1.685.0
update-speakeasy-version:
ifndef VERSION
	$(error VERSION is required. This is the Speakeasy CLI version (e.g., 1.685.0))
endif
	uv run inv update-speakeasy --version "$(VERSION)" --targets "all"
