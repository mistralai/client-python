# WhoamiUserPrincipal

Identity of a human user principal.

Carries user-only fields. The ``principal_type`` discriminator makes this
variant mutually exclusive with the service-account variant, so a payload can
never carry both a user id and a service-account id.


## Fields

| Field                                             | Type                                              | Required                                          | Description                                       | Example                                           |
| ------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------- |
| `principal_type`                                  | *Literal["user"]*                                 | :heavy_check_mark:                                | Discriminator identifying a human user principal. | user                                              |
| `id`                                              | *str*                                             | :heavy_check_mark:                                | The user's unique identifier.                     | 8f14e45f-ceea-4e0a-9b0e-8f7d3c2a1b4e              |
| `email`                                           | *OptionalNullable[str]*                           | :heavy_minus_sign:                                | The user's email address, when known.             | ada@example.com                                   |
| `first_name`                                      | *OptionalNullable[str]*                           | :heavy_minus_sign:                                | The user's first name, when known.                | Ada                                               |
| `last_name`                                       | *OptionalNullable[str]*                           | :heavy_minus_sign:                                | The user's last name, when known.                 | Lovelace                                          |