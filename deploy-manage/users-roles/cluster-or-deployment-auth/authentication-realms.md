---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/realms.html
applies_to:
  stack: all
products:
  - id: elasticsearch
---

# Authentication realms [realms]

Elastic authenticates users by using realms and one or more [token-based authentication services](token-based-authentication-services.md).

A *realm* is used to resolve and authenticate users based on authentication tokens. There are two types of realms: 

Internal
:   Realms that are internal to {{es}} and don’t require any communication with external parties. They are fully managed by {{es}}. There can only be a maximum of one configured realm per internal realm type. {{es}} provides two internal realm types: `native` and `file`.

External
:   Realms that require interaction with parties and components external to {{es}}, typically with enterprise grade identity management systems. Unlike internal realms, you can have as many external realms as you would like, each with its own unique name and configuration. [View external realm types](#external-realms).

## Configuring realms

To learn how to configure and use a specific realm, follow the documentation for the realm that you want to use. You can also configure a custom realm by building a [custom realm plugin](/deploy-manage/users-roles/cluster-or-deployment-auth/custom.md).

You can also perform the following tasks to further configure your realms:

* Prioritize your realms using [realm chains](/deploy-manage/users-roles/cluster-or-deployment-auth/realm-chains.md).
* Allow a single user to authenticate using multiple realms by grouping them together in a [security domain](/deploy-manage/users-roles/cluster-or-deployment-auth/security-domains.md).

## Internal realms

{{es}} provides the following built-in internal realms:

:::{include} ../_snippets/internal-realms.md
:::

## External realms

{{es}} provides the following built-in external realms:

:::{include} ../_snippets/external-realms.md
:::

## Custom realms

If you need to integrate with another authentication system, you can build a custom realm plugin. For more information, see [Integrating with other authentication systems](custom.md).