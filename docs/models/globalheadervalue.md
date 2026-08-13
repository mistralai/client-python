# GlobalHeaderValue

Value of a connector-wide header. ``value`` is plaintext in memory so create
round-trips and encryption-at-rest keep the real value; secrets are redacted only
on JSON serialization (API responses).


## Fields

| Field              | Type               | Required           | Description        |
| ------------------ | ------------------ | ------------------ | ------------------ |
| `is_secret`        | *Optional[bool]*   | :heavy_minus_sign: | N/A                |
| `value`            | *str*              | :heavy_check_mark: | N/A                |