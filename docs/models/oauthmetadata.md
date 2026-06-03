# OAuthMetadata

RFC 8414 OAuth 2.0 Authorization Server Metadata.
See https://datatracker.ietf.org/doc/html/rfc8414#section-2


## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `issuer`                                                   | *str*                                                      | :heavy_check_mark:                                         | N/A                                                        |
| `authorization_endpoint`                                   | *str*                                                      | :heavy_check_mark:                                         | N/A                                                        |
| `token_endpoint`                                           | *str*                                                      | :heavy_check_mark:                                         | N/A                                                        |
| `registration_endpoint`                                    | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | N/A                                                        |
| `scopes_supported`                                         | List[*str*]                                                | :heavy_minus_sign:                                         | N/A                                                        |
| `response_types_supported`                                 | List[*str*]                                                | :heavy_minus_sign:                                         | N/A                                                        |
| `response_modes_supported`                                 | List[*str*]                                                | :heavy_minus_sign:                                         | N/A                                                        |
| `grant_types_supported`                                    | List[*str*]                                                | :heavy_minus_sign:                                         | N/A                                                        |
| `token_endpoint_auth_methods_supported`                    | List[*str*]                                                | :heavy_minus_sign:                                         | N/A                                                        |
| `token_endpoint_auth_signing_alg_values_supported`         | List[*str*]                                                | :heavy_minus_sign:                                         | N/A                                                        |
| `service_documentation`                                    | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | N/A                                                        |
| `ui_locales_supported`                                     | List[*str*]                                                | :heavy_minus_sign:                                         | N/A                                                        |
| `op_policy_uri`                                            | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | N/A                                                        |
| `op_tos_uri`                                               | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | N/A                                                        |
| `revocation_endpoint`                                      | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | N/A                                                        |
| `revocation_endpoint_auth_methods_supported`               | List[*str*]                                                | :heavy_minus_sign:                                         | N/A                                                        |
| `revocation_endpoint_auth_signing_alg_values_supported`    | List[*str*]                                                | :heavy_minus_sign:                                         | N/A                                                        |
| `introspection_endpoint`                                   | *OptionalNullable[str]*                                    | :heavy_minus_sign:                                         | N/A                                                        |
| `introspection_endpoint_auth_methods_supported`            | List[*str*]                                                | :heavy_minus_sign:                                         | N/A                                                        |
| `introspection_endpoint_auth_signing_alg_values_supported` | List[*str*]                                                | :heavy_minus_sign:                                         | N/A                                                        |
| `code_challenge_methods_supported`                         | List[*str*]                                                | :heavy_minus_sign:                                         | N/A                                                        |
| `client_id_metadata_document_supported`                    | *OptionalNullable[bool]*                                   | :heavy_minus_sign:                                         | N/A                                                        |