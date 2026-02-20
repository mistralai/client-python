# ChatCompletionRequestToolChoice

Controls which (if any) tool is called by the model. `none` means the model will not call any tool and instead generates a message. `auto` means the model can pick between generating a message or calling one or more tools. `any` or `required` means the model must call one or more tools. Specifying a particular tool via `{"type": "function", "function": {"name": "my_function"}}` forces the model to call that tool.


## Supported Types

### `models.ToolChoice`

```python
value: models.ToolChoice = /* values here */
```

### `models.ToolChoiceEnum`

```python
value: models.ToolChoiceEnum = /* values here */
```

