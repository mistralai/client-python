# Migration Guide: v1 to v2

## Import Changes

### Main Client

```python
# v1
from mistralai import Mistral

# v2
from mistralai.client import Mistral
```

### Models and Types

```python
# v1
from mistralai.models import UserMessage

# v2
from mistralai.client.models import UserMessage
```

## Quick Reference

| v1 | v2 |
|----|-----|
| `from mistralai import` | `from mistralai.client import` |
| `from mistralai.models` | `from mistralai.client.models` |
| `from mistralai.types` | `from mistralai.client.types` |
