# OAuth2TokenEndpointAuthMethod

## Example Usage

```python
from mistralai.client.models import OAuth2TokenEndpointAuthMethod

# Open enum: unrecognized values are captured as UnrecognizedStr
value: OAuth2TokenEndpointAuthMethod = "client_secret_post"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"client_secret_post"`
- `"client_secret_basic"`
- `"private_key_jwt"`
