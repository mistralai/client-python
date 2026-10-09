# WhoamiResponse

Principal-agnostic identity of the authenticated caller.

Supersedes the user-centric ``/v1/users/me`` and ``/api/users/v2/me`` by
resolving any principal (user or service account) through a single call. The
``principal`` field is a discriminated union; the remaining fields are the
shared session context and apply to either principal kind.


## Fields

| Field                                                                                | Type                                                                                 | Required                                                                             | Description                                                                          |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| `principal`                                                                          | [models.Principal](../models/principal.md)                                           | :heavy_check_mark:                                                                   | The authenticated principal: either a user or a service account.                     |
| `organization`                                                                       | [OptionalNullable[models.WhoamiOrganization]](../models/whoamiorganization.md)       | :heavy_minus_sign:                                                                   | The organization the caller's session is scoped to, when set.                        |
| `workspace`                                                                          | [OptionalNullable[models.UserIdentityWorkspace]](../models/useridentityworkspace.md) | :heavy_minus_sign:                                                                   | The workspace the caller's session is scoped to, when set.                           |