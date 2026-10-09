# WhoamiServiceAccountPrincipal

Identity of a service-account principal.

Carries service-account-only fields. Service accounts have no user profile
(no email or name of a person); ``name`` is the service account's own display
name. Resolved independently of the authentication mechanism.


## Fields

| Field                                                  | Type                                                   | Required                                               | Description                                            | Example                                                |
| ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ |
| `principal_type`                                       | *Literal["service_account"]*                           | :heavy_check_mark:                                     | Discriminator identifying a service-account principal. | service_account                                        |
| `service_account_id`                                   | *str*                                                  | :heavy_check_mark:                                     | The service account's unique identifier.               | 3b241101-e2bb-4255-8caf-4136c566a962                   |
| `name`                                                 | *OptionalNullable[str]*                                | :heavy_minus_sign:                                     | The service account's display name, when known.        | ci-deploy-bot                                          |