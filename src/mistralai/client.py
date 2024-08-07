from typing import Optional

MIGRATION_MESSAGE = "This client is deprecated starting v1.0.0, pin your version to 0.4.2. Or migrate by following this documentation: TODO add link"


class MistralClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: str = "",
        max_retries: int = 5,
        timeout: int = 120,
    ):
        raise NotImplementedError(MIGRATION_MESSAGE)
