# Internal authentication

Internal authentication is managed by [realms](authentication-realms.md) that don’t require any communication with external parties. They are fully managed by {{es}}. There can only be a maximum of one configured realm per internal realm type. 

In this section, you'll learn how to configure internal realms, and manage users that authenticate using internal realms.

## Available internal realms

{{es}} provides two internal realm types:

:::{include} ../_snippets/internal-realms.md
:::