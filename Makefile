.PHONY: help generate test-generate update-speakeasy-version check-config

help:
	@echo "Available targets:"
	@echo "  make generate                                 Generate all SDKs (main, Azure, GCP)"
	@echo "  make test-generate                            Test SDK generation locally"
	@echo "  make update-speakeasy-version VERSION=x.y.z   Update Speakeasy CLI version"
	@echo "  make check-config                             Check gen.yaml against recommended defaults"
	@echo ""
	@echo "Note: Production SDK generation and release run in the Buildkite pipeline eng-sdk-codegen"
	@echo "  (dashboard monorepo); see openapi/.agents/skills/deploy-public-sdk/SKILL.md"

# Generate all SDKs (main, Azure, GCP)
generate:
	speakeasy run -t all

# Test SDK generation locally.
# For production, use the Buildkite pipeline eng-sdk-codegen (see the help target).
# This uses the Speakeasy CLI version defined in .speakeasy/workflow.yaml
test-generate:
	speakeasy run --skip-versioning

# Check gen.yaml configuration against Speakeasy recommended defaults
check-config:
	speakeasy configure generation check

# Update the Speakeasy CLI version (the code generator tool).
# This modifies speakeasyVersion in .speakeasy/workflow.yaml and regenerates the SDK.
# Usage: make update-speakeasy-version VERSION=1.685.0
update-speakeasy-version:
ifndef VERSION
	$(error VERSION is required. This is the Speakeasy CLI version (e.g., 1.685.0))
endif
	uv run inv update-speakeasy --version "$(VERSION)" --targets "all"
