---
applies_to:
  stack: all
---

# Internal authentication

Internal authentication methods are fully managed by {{es}}, and don't require any communication with external parties.

{{es}} offers two internal authentication [realms](authentication-realms.md), both of which are enabled by default. There can only be a maximum of one configured realm per internal realm type. 

In this section, you'll learn how to configure internal realms, and manage users that authenticate using internal realms.

## Available internal realms

{{es}} provides two internal realm types:

:::{include} ../_snippets/internal-realms.md
:::
