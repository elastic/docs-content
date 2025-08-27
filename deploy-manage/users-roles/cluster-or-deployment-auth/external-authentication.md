---
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
---

# External authentication

External authentication in Elastic is any form of authentication that requires interaction with parties and components external to {{es}}, typically with enterprise grade identity management systems. 

Elastic offers several external [realm](authentication-realms.md) types, each of which represents a common authentication provider. You can have as many external realms as you would like, each with its own unique name and configuration.

If the authentication provider that you want to use is not currently supported, then you can create your own [custom realm plugin](custom.md) to integrate with additional systems.

In this section, you'll learn how to configure different types of external realms, and use them to grant access to Elastic resources.

:::{{tip}}
For many external realms, you need to perform extra steps to use the realm to log in to {{kib}}. [Learn more](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-authentication.md).
:::

## Available external realms

{{es}} provides the following built-in external realms:

:::{include} ../_snippets/external-realms.md
:::