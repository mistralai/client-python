# gen.yaml Diff: Main vs Azure vs GCP

## `generation` section

| Setting | Main | Azure | GCP |
|---------|------|-------|-----|
| `sdkClassName` | `Mistral` | `MistralAzure` | `MistralGCP` |
| `nameResolutionDec2023` | `true` | `true` | `true` |
| `nameResolutionFeb2025` | `true` | `true` | `true` |
| `parameterOrderingFeb2024` | `true` | `true` | `true` |
| `requestResponseComponentNamesFeb2024` | `true` | `true` | `true` |
| `securityFeb2025` | `true` | `true` | `true` |
| `sharedErrorComponentsApr2025` | `true` | `true` | `true` |
| `methodSignaturesApr2024` | `true` | `true` | `true` |
| `sharedNestedComponentsJan2026` | `true` | `true` | `true` |

## `python` section

| Setting | Main | Azure | GCP |
|---------|------|-------|-----|
| `version` | `2.0.0a4` | `2.0.0a4` | `2.0.0a4` |
| `additionalDependencies.main` | *none* | *none* | *none* |
| `baseErrorName` | `MistralError` | `MistralAzureError` | `MistralGcpError` |
| `description` | `...Mistral AI API.` | `...in Azure.` | `...in GCP.` |
| `enableCustomCodeRegions` | `true` | `false` | `false` |
| `envVarPrefix` | `MISTRAL` | *missing* | *missing* |
| `responseRequiredSep2024` | `true` | `true` | `true` |
| `flatAdditionalProperties` | `true` | `true` | `true` |
| `forwardCompatibleEnumsByDefault` | `true` | `true` | `true` |
| `forwardCompatibleUnionsByDefault` | `tagged-only` | `tagged-only` | `tagged-only` |
| `preApplyUnionDiscriminators` | `true` | `true` | `true` |
| `moduleName` | `mistralai.client` | `mistralai.azure.client` | `mistralai.gcp.client` |
| `packageName` | `mistralai` | `mistralai-azure` | `mistralai-gcp` |

## Remaining intentional differences

All fix flags and feature flags are now aligned. The only remaining differences are expected per-target values:

- **`version`** -- all at 2.0.0a4 (versions may diverge independently)
- **`baseErrorName`** / `description` -- per-target identity
- **`enableCustomCodeRegions`** -- `false` in Azure/GCP (they have no custom code regions)
- **`envVarPrefix`** -- absent in Azure/GCP (only the main SDK reads `MISTRAL_*` env vars)
- **`moduleName`** / `packageName` -- per-target namespace
