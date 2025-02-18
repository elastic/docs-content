# External authentication

Internal authentication is managed by [realms](authentication-realms.md) that require interaction with parties and components external to {{es}}, typically, with enterprise grade identity management systems. Unlike internal realms, you can have as many external realms as you would like, each with its own unique name and configuration.

In this section, you'll learn how to configure external realms, and use them to grant access to Elastic resources.

## Available external realms

{{es}} provides the following built-in external realms:

:::{include} ../_snippets/external-realms.md
:::

## Custom realms

If you need to integrate with another authentication system, you can build a custom realm plugin. For more information, see [Integrating with other authentication systems](custom.md).