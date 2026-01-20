# Speakeasy Codegen Feature Requests for Namespace Package Support

These issues should be filed with the Speakeasy team to improve namespace package support in Python SDK generation.

---

## Issue 1: Preserve Custom Code Regions When Changing moduleName

**Title**: `[Python] Custom code regions lost when changing moduleName configuration`

**Description**:
When updating the `moduleName` configuration in `gen.yaml` (e.g., from `mistralai` to `mistralai.sdk` for namespace package support), all custom code regions are removed during regeneration.

**Current Behavior**:
According to documentation: "Custom code regions will be removed by updating the ModuleName."

**Expected Behavior**:
Custom code regions should be preserved (with updated import paths) when `moduleName` changes, or a migration tool should be provided.

**Use Case**:
Migrating to PEP 420 implicit namespace packages requires changing `moduleName` to include a dot (e.g., `mistralai.sdk`). This is a breaking change that loses all custom code:

```python
# region imports
from mistralai.extra import my_custom_function
# endregion imports

# region sdk-class-body
def my_custom_method(self):
    # This entire block is lost when moduleName changes
    pass
# endregion sdk-class-body
```

**Workaround**:
Manual backup and re-application of custom code after regeneration.

**Priority**: High (blocks namespace package adoption for SDKs with custom code)

---

## Issue 2: Namespace Package pyproject.toml Configuration

**Title**: `[Python] Add namespace package support in generated pyproject.toml`

**Description**:
When using `moduleName` with dots for PEP 420 namespace packages, the generated `pyproject.toml` should be configured correctly for namespace package discovery.

**Current Behavior**:
Generated `pyproject.toml` uses standard package discovery which may not correctly handle namespace packages.

**Expected Behavior**:
When `moduleName` contains dots, generate `pyproject.toml` with:
- Correct hatchling configuration for namespace packages
- Proper source mappings for nested structure
- `find_namespace_packages()` equivalent if using setuptools

**Example Configuration**:
```toml
# For moduleName: company.sdk
[tool.hatch.build.targets.wheel]
packages = ["src/company"]  # Include namespace root

[tool.hatch.build.targets.wheel.sources]
"src/company/sdk" = "company/sdk"
```

**Priority**: Medium

---

## Issue 3: Optional Re-export Shim at Namespace Root

**Title**: `[Python] Add option to generate re-exports at namespace root for backward compatibility`

**Description**:
When migrating to namespace packages, provide an option to generate a thin `__init__.py` at the namespace root with re-exports for backward compatibility.

**Proposed Configuration**:
```yaml
python:
  moduleName: mistralai.sdk
  namespaceReexports: true  # Generate mistralai/__init__.py with re-exports
  namespaceReexportsDeprecationWarning: true  # Emit deprecation warning
```

**Generated Code**:
```python
# mistralai/__init__.py (generated when namespaceReexports: true)
"""Backward compatibility re-exports. Deprecated: use mistralai.sdk instead."""
import warnings
warnings.warn(
    "Importing from 'mistralai' is deprecated. Use 'mistralai.sdk' instead.",
    DeprecationWarning,
    stacklevel=2
)
from mistralai.sdk import *
```

**Use Case**:
Allows gradual migration with deprecation period instead of hard breaking change.

**Priority**: Medium

---

## Issue 4: Multi-target Namespace Coordination in Workflows

**Title**: `[Workflow] Coordinate namespace packages across multiple SDK targets`

**Description**:
When multiple targets in a workflow should share a namespace (e.g., `mistralai.sdk`, `mistralai.azure`, `mistralai.gcp`), provide workflow-level coordination.

**Current Challenge**:
Each target generates independently. There's no coordination to ensure:
- Consistent namespace root handling
- No conflicting `__init__.py` files
- Proper `py.typed` marker placement

**Proposed Configuration**:
```yaml
# workflow.yaml
namespaces:
  mistralai:
    packages:
      - mistralai-sdk      # → mistralai.sdk
      - mistralai-azure    # → mistralai.azure
      - mistralai-gcp      # → mistralai.gcp

targets:
  mistralai-sdk:
    namespace: mistralai
    # ...
  mistralai-azure:
    namespace: mistralai
    # ...
```

**Priority**: Low (can be handled manually)

---

## Issue 5: py.typed Marker Placement for Namespace Packages

**Title**: `[Python] Correct py.typed placement for PEP 420 namespace packages`

**Description**:
For namespace packages, `py.typed` markers need to be placed at both the namespace root and each subpackage per PEP 561.

**Current Behavior**:
`py.typed` is placed at the module root only.

**Expected Behavior**:
When `moduleName` contains dots:
- Place `py.typed` at namespace root (`mistralai/py.typed`)
- Place `py.typed` at SDK root (`mistralai/sdk/py.typed`)

**Reference**: [PEP 561 - Distributing and Packaging Type Information](https://peps.python.org/pep-0561/)

**Priority**: Low

---

## Issue 6: Documentation for Namespace Package Migration

**Title**: `[Docs] Add guide for migrating Python SDKs to namespace packages`

**Description**:
Provide documentation for migrating existing SDKs to PEP 420 implicit namespace packages.

**Suggested Content**:
1. When to use namespace packages
2. Configuration changes required
3. Breaking change considerations
4. Custom code preservation strategies
5. Testing namespace package installations
6. Rollback procedures

**Priority**: Medium

---

## Summary Table

| Issue | Title | Priority | Workaround Available |
|-------|-------|----------|---------------------|
| 1 | Custom code region preservation | High | Manual backup/restore |
| 2 | pyproject.toml namespace config | Medium | Manual editing |
| 3 | Re-export shim generation | Medium | Manual creation |
| 4 | Multi-target namespace coordination | Low | Manual coordination |
| 5 | py.typed placement | Low | Manual placement |
| 6 | Documentation | Medium | N/A |
