# Oauth2MetadataSecrets

OAuth2 client credentials stored alongside a connector's authentication method.

Used by OAuth2 and Slack App auth types for token exchange and refresh flows.
Contains the client credentials obtained during OAuth2 Dynamic Client Registration
or provided at connector creation time.


## Fields

| Field                      | Type                       | Required                   | Description                |
| -------------------------- | -------------------------- | -------------------------- | -------------------------- |
| `client_id`                | *OptionalNullable[str]*    | :heavy_minus_sign:         | N/A                        |
| `client_secret`            | *OptionalNullable[str]*    | :heavy_minus_sign:         | N/A                        |
| `client_id_issued_at`      | *OptionalNullable[int]*    | :heavy_minus_sign:         | N/A                        |
| `client_secret_expires_at` | *OptionalNullable[int]*    | :heavy_minus_sign:         | N/A                        |