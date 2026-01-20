# Migration to PEP 420 Implicit Namespace Packages

## Overview

This document outlines the migration strategy for converting the `mistralai` Python SDK to use PEP 420 implicit namespace packages. This change enables a separate `mistralai.workflows` subpackage to be manually managed outside of Speakeasy code generation.

## Background

- **PEP 420**: Defines implicit namespace packages in Python 3.3+, allowing multiple distributions to contribute to the same namespace without requiring `__init__.py` files at the namespace level.
- **Goal**: Enable `mistralai.workflows` to exist as a separate, manually-managed package while `mistralai.sdk` remains Speakeasy-generated.

## Migration Strategy

### Option A: Full Namespace Migration (Recommended)

**Configuration Change:**
```yaml
# .speakeasy/gen.yaml
python:
  packageName: mistralai        # PyPI package name (unchanged)
  moduleName: mistralai.sdk     # Module becomes a namespace subpackage
```

**Resulting Structure:**
```
src/
└── mistralai/                  # Namespace package (NO __init__.py)
    ├── sdk/                    # Speakeasy-generated SDK
    │   ├── __init__.py
    │   ├── models/
    │   ├── types/
    │   ├── utils/
    │   └── ...
    └── workflows/              # Manually-managed (separate package)
        ├── __init__.py
        └── ...
```

**Import Changes (Breaking):**
```python
# Before
from mistralai import Mistral
from mistralai.models import ChatCompletionRequest

# After
from mistralai.sdk import Mistral
from mistralai.sdk.models import ChatCompletionRequest
```

### Option B: pkgutil-style Namespace (Backward Compatible)

Keep current structure but add namespace extension capability:

```python
# In mistralai/__init__.py (via custom code region)
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

# Existing exports remain
from .sdk import *
from .models import *
```

**Pros:** Backward compatible
**Cons:** Requires manual maintenance, not pure PEP 420

## Recommended Approach: Option A with Compatibility Shim

1. **Phase 1**: Migrate to `moduleName: mistralai.sdk`
2. **Phase 2**: Create optional `mistralai-compat` package providing old import paths (deprecated)
3. **Phase 3**: Remove compatibility shim after deprecation period

## Configuration Changes Required

### 1. `.speakeasy/gen.yaml`

```yaml
configVersion: 2.0.0
generation:
  sdkClassName: Mistral
  # ... existing settings ...
python:
  version: 2.0.0                    # Major version bump for breaking change
  packageName: mistralai
  moduleName: mistralai.sdk         # NEW: Namespace subpackage
  # ... rest of config ...
```

### 2. `pyproject.toml`

```toml
[project]
name = "mistralai"
version = "2.0.0"

[tool.hatch.build.targets.wheel]
packages = ["src/mistralai"]        # Include namespace root

[tool.hatch.build.targets.wheel.sources]
"src/mistralai/sdk" = "mistralai/sdk"
```

### 3. Workflow Output Path

```yaml
# .speakeasy/workflow.yaml
targets:
  mistralai-sdk:
    target: python
    source: mistral-openapi
    output: ./                      # Root (SDK goes to src/mistralai/sdk/)
```

## Gaps Requiring Speakeasy Team Input

### Gap 1: Custom Code Region Preservation During moduleName Change

**Issue**: According to Speakeasy documentation, "Custom code regions will be removed by updating the ModuleName."

**Current Custom Code:**
- `src/mistralai/chat.py` - Structured outputs feature (`# region imports`, `# region sdk-class-body`)
- `src/mistralai/conversations.py` - Run context functionality
- `src/mistralai/extra/` - Entire custom extension package

**Request**: Provide mechanism to preserve custom code regions when changing `moduleName`, or provide migration tooling.

**Workaround**: Manual backup and re-application of custom code after regeneration.

### Gap 2: Namespace Package pyproject.toml Generation

**Issue**: Speakeasy-generated `pyproject.toml` may not correctly configure namespace packages for hatchling.

**Request**: Option to generate namespace-package-aware `pyproject.toml` with:
- `find_namespace_packages()` equivalent for hatchling
- Correct source mapping for nested namespace structure

### Gap 3: Re-export Shim Generation

**Issue**: No built-in way to generate backward-compatible re-exports at the namespace root.

**Request**: Optional configuration to generate a thin `__init__.py` at the namespace root with re-exports:
```yaml
python:
  moduleName: mistralai.sdk
  namespaceReexports: true    # Would generate mistralai/__init__.py with re-exports
```

### Gap 4: Multi-package Namespace Coordination

**Issue**: When multiple Speakeasy targets share a namespace (e.g., `mistralai.sdk`, `mistralai.azure`, `mistralai.gcp`), coordination is needed.

**Request**: Workflow-level configuration for coordinated namespace package generation across targets.

### Gap 5: py.typed Marker Placement

**Issue**: For namespace packages, `py.typed` markers need to be in the right location per PEP 561.

**Request**: Automatic `py.typed` placement at both namespace root and subpackage levels.

## Files to be Modified

| File | Change Type | Description |
|------|-------------|-------------|
| `.speakeasy/gen.yaml` | Config | Add `moduleName: mistralai.sdk` |
| `pyproject.toml` | Config | Update for namespace packages |
| `src/mistralai/__init__.py` | Remove | Becomes namespace (no file) |
| `src/mistralai/sdk/__init__.py` | Generated | New SDK root |
| `packages/mistralai_azure/.speakeasy/gen.yaml` | Config | Consider `moduleName: mistralai.azure` |
| `packages/mistralai_gcp/.speakeasy/gen.yaml` | Config | Consider `moduleName: mistralai.gcp` |

## Testing Plan

1. **Unit Tests**: Update imports in all test files
2. **Integration Tests**: Verify namespace package discovery
3. **Type Checking**: Ensure `py.typed` works with namespace structure
4. **Installation Test**: Verify `pip install mistralai` and `pip install mistralai-workflows` coexist

## Rollback Plan

If issues arise:
1. Revert `moduleName` to `mistralai`
2. Regenerate SDK
3. Re-apply custom code regions manually

## References

- [PEP 420 - Implicit Namespace Packages](https://peps.python.org/pep-0420/)
- [Speakeasy Python Configuration](https://www.speakeasy.com/docs/speakeasy-reference/generation/python-config)
- [Python Packaging User Guide - Namespace Packages](https://packaging.python.org/guides/packaging-namespace-packages/)
