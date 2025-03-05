---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-roles-and-privileges.html
---

# Required roles and privileges [fleet-roles-and-privileges]

Assigning the {{kib}} feature privileges `Fleet` and `Integrations` grants access to use {{fleet}} and Integrations.

`all`
:   Grants full read-write access.

`read`
:   Grants read-only access.

`none`
:   No access is granted.

Take advantage of these privilege settings by:

* [Using an {{es}} built-in role](#fleet-roles-and-privileges-built-in)
* [Creating a new role](#fleet-roles-and-privileges-create)

## Built-in roles [fleet-roles-and-privileges-built-in]

{{es}} comes with built-in roles that include default privileges.

`editor`
:   The built-in `editor` role grants the following privileges, supporting full read-write access to {{fleet}} and Integrations:
* {{Fleet}}: `all`
* Integrations: `all`

`viewer`
:   The built-in `viewer` role grants the following privileges, supporting read-only access to {{fleet}} and Integrations:

* {{Fleet}}:: `read`
* Integrations:: `read`

You can also create a new role that can be assigned to a user, in order to grant more specific levels of access to {{fleet}} and Integrations.


## Create a role for {{fleet}} [fleet-roles-and-privileges-create]

To create a new role with access to {{fleet}} and Integrations:

1. In {{kib}}, go to **Management → Stack Management**.
2. In the **Security** section, select **Roles**.
3. Select **Create role**.
4. Specify a name for the role.
5. Leave the {{es}} settings at their defaults, or refer to [Security privileges](asciidocalypse://docs/reference/elasticsearch/security-privileges.md) for descriptions of the available settings.
6. In the {{kib}} section, select **Assign to space**.
7. In the **Spaces** menu, select *** All Spaces**. Since many Integrations assets are shared across spaces, the users need the {{kib}} privileges in all spaces.
8. Expand the **Management** section.
9. Set **Fleet** privileges to **All**.
10. Choose the access level that you'd like the role to have with respect to {{fleet}} and integrations:
    1. To grant the role full access to use and manage {{fleet}} and integrations, set both the **Fleet** and **Integrations** privileges to `All`.
    :::{image} images/kibana-fleet-privileges-all.png
    :alt: Kibana privileges flyout showing Fleet and Integrations access set to All
    :class: screenshot
    :::
    2. Similarly, to create a read-only user for {{fleet}} and Integrations, set both the **Fleet** and **Integrations** privileges to `Read`.
    :::{image} images/kibana-fleet-privileges-read.png
    :alt: Kibana privileges flyout showing Fleet and Integrations access set to All
    :class: screenshot
    :::

Once you've created a new role you can assign it to any {{es}} user. You can edit the role at any time by returning to the **Roles** page in {{kib}}.