---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-roles-and-privileges.html
---

# Required roles and privileges [fleet-roles-and-privileges]

Beginning with {{stack}} version 8.1, you no longer require the built-in `elastic` superuser credentials to use {{fleet}} and Integrations.

Assigning the {{kib}} feature privileges `Fleet` and `Integrations` grants access to these features:

`all`
:   Grants full read-write access.

`read`
:   Grants read-only access.

The built-in `editor` role grants the following privileges, supporting full read-write access to {{fleet}} and Integrations:

* {{Fleet}}: `All`
* Integrations: `All`

The built-in `viewer` role grants the following privileges, supporting read-only access to {{fleet}} and Integrations:

* {{Fleet}}:: `None`
* Integrations:: `Read`

You can also create a new role that can be assigned to a user to grant access to {{fleet}} and Integrations.


## Create a role for {{fleet}} [fleet-roles-and-privileges-create]

To create a new role with full access to use and manage {{fleet}} and Integrations:

1. In {{kib}}, go to **Management → Stack Management**.
2. In the **Security** section, select **Roles**.
3. Select **Create role**.
4. Specify a name for the role.
5. Leave the {{es}} settings at their defaults, or refer to [Security privileges](elasticsearch://docs/reference/elasticsearch/security-privileges.md) for descriptions of the available settings.
6. In the {{kib}} section, select **Add Kibana privilege**.
7. In the **Spaces** menu, select *** All Spaces**. Since many Integrations assets are shared across spaces, the users needs the {{kib}} privileges in all spaces.
8. Expand the **Management** section.
9. Set **Fleet** privileges to **All**.
10. Set **Integrations** privileges to **All**.

:::{image} images/kibana-fleet-privileges.png
:alt: Kibana privileges flyout showing Fleet and Integrations set to All
:class: screenshot
:::

To create a read-only user for Integrations, follow the same steps as above but set the **Fleet** privileges to **None*** and the ***Integrations** privileges to **Read**.

Read-only access to {{fleet}} is not currently supported but is planned for development in a later release.
