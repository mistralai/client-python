# ConnectorsQueryFilters


## Fields

| Field                                                                        | Type                                                                         | Required                                                                     | Description                                                                  |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `active`                                                                     | *OptionalNullable[bool]*                                                     | :heavy_minus_sign:                                                           | Filter for active connectors for a given user, workspace and organization.   |
| `protocol`                                                                   | [OptionalNullable[models.ConnectorProtocol]](../models/connectorprotocol.md) | :heavy_minus_sign:                                                           | Filter connectors by protocol.                                               |