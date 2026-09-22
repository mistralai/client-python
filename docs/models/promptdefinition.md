# PromptDefinition

Versioned prompt content.


## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `content`                                                  | *str*                                                      | :heavy_check_mark:                                         | Prompt template content.                                   |
| `variables`                                                | List[[models.PromptVariable](../models/promptvariable.md)] | :heavy_minus_sign:                                         | Variables used by the prompt.                              |