---
navigation_title: Roles and privileges
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-roles-and-privileges.html
description: Control access to Fleet and Integrations with Kibana built-in and custom roles. Reference tables list what each Fleet privilege allows, including managing integration policies and packages.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# {{fleet}} and Integrations roles and privileges [fleet-roles-and-privileges]

Use {{kib}} roles and privileges to grant users access to {{fleet}} and Integrations. For each of these features, select the type of access you want to allow:

:::{include} /deploy-manage/_snippets/feature-privilege-access-levels.md
:::

In {{fleet}}, **Read** access for **Agents** also allows requesting agent diagnostics.

You can take advantage of these privilege settings by:

* [Using an {{es}} built-in role](#fleet-roles-and-privileges-built-in)
* [Creating a new role](#fleet-roles-and-privileges-create).

To configure access at a more granular level, select a custom set of privileges for individual {{fleet}} features:

* [Customize sub-feature privileges for {{fleet}}](#fleet-roles-and-privileges-sub-features)

Some actions, such as adding an integration to an agent policy, require privileges for both {{fleet}} and Integrations. Refer to [Privileges for integrations and integration policies](#fleet-roles-and-privileges-integrations).


## Built-in roles [fleet-roles-and-privileges-built-in]

{{es}} comes with built-in roles that include default privileges.

`editor`
:   The built-in `editor` role grants these privileges, supporting full read-write access to {{fleet}} and Integrations:

    * {{fleet}}: `all`
    * Integrations: `all`

`viewer`
:   The built-in `viewer` role grants these privileges, supporting read-only access to {{fleet}} and Integrations:

    * {{fleet}}: `read`
    * Integrations: `read`

You can also create a new role that can be assigned to a user to grant more specific levels of access to {{fleet}} and Integrations.


## Create a new role for {{fleet}} [fleet-roles-and-privileges-create]

:::{note}
:applies_to: serverless: ga

In {{serverless-short}} projects, create a custom role as described in [](/deploy-manage/users-roles/serverless-custom-roles.md), then follow steps 4 to 6 to select spaces and set the **Fleet** and **Integrations** privileges.
:::

To create a new role with access to {{fleet}} and Integrations:

1. Go to the **Roles** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Create role**, then enter a **Role name**.
3. Leave the {{es}} settings at their defaults, or refer to [Security privileges](elasticsearch://reference/elasticsearch/security-privileges.md) for descriptions of the available settings.
4. In the {{kib}} section, select **Assign to space**. In the **Select spaces** field, select the spaces where the role needs access to {{fleet}} and Integrations.
    * {applies_to}`serverless: ga` {applies_to}`stack: ga 9.1+` You can grant {{fleet}} privileges in specific spaces. For how agent policies and integration assets behave across spaces, refer to [](/deploy-manage/manage-spaces-fleet.md).
    * {applies_to}`stack: ga =9.0` {{fleet}} privileges apply to all spaces, so select **All Spaces**.
5. Expand the **Management** section, then choose the access level that you'd like the role to have with respect to {{fleet}} and integrations:
    1. To grant the role full access to use and manage {{fleet}} and integrations, set both the **Fleet** and **Integrations** privileges to `All`.
    2. To create a read-only user for {{fleet}} and Integrations, set both the **Fleet** and **Integrations** privileges to `Read`.
    3. If you'd like to define more specialized access to {{fleet}} based on individual components, set **Fleet** to `All` or `Read`, then expand the **Fleet** menu and enable **Customize sub-feature privileges**.

       The sub-feature privileges you select replace the general **Fleet** privilege and determine which {{fleet}} UI features the role can access. For details, refer to [Customize sub-feature privileges for {{fleet}}](#fleet-roles-and-privileges-sub-features).

       Customizing sub-feature privileges is a [subscription feature](https://www.elastic.co/subscriptions).

       To let the role add integrations to agent policies or edit integration policies, also set **Integrations** to `All`. Refer to [Privileges for integrations and integration policies](#fleet-roles-and-privileges-integrations).

6. Select **Assign role**, then select **Create role**.

After you've created a new role, you can assign it to any {{es}} user.
You can edit the role at any time by returning to the **Roles** page in {{kib}}.

## Customize sub-feature privileges for {{fleet}}[fleet-roles-and-privileges-sub-features]

You have more granular control when [creating a new role](#fleet-roles-and-privileges-create) or editing it. This is useful when people in your organization access {{fleet}} for different purposes, and you need to fine-tune the components that they can view and the actions that they can perform.

The {{fleet}} UI varies depending on the privileges granted to the role.

### Example 1: Read access for {{agents}}[fleet-roles-and-privileges-sub-features-example1]

Set `Read` access for {{agents}} only:

* Agents: `Read`
* Agent policies: `None`
* Settings: `None`

With these privileges, the {{fleet}} UI shows only the **Agents** and **Data streams** tabs. 
The **Agent policies**, **Enrollment tokens**, **Uninstall tokens**, and **Settings** tabs are unavailable. 

The set of actions available for an agent are limited to viewing the agent and requesting a diagnostics bundle.

:::{image} images/kibana-fleet-privileges-agents-view.png
:alt: Fleet UI showing only the Agents and Data streams tabs
:screenshot:
:::

Change the **Agents** privilege to `All` to enable the role to perform the [full set of available actions](/reference/fleet/manage-agents.md) on {{agents}}.

### Example 2: Read access for all {{fleet}} features[fleet-roles-and-privileges-sub-features-example2]

Set `Read` access for {{agents}}, agent policies, and {{fleet}} settings:

* Agents: `Read`
* Agent policies: `Read`
* Settings: `Read`

With these privileges, the {{fleet}} UI shows the **Agents**, **Agent policies**, **Data streams**, and **Settings** tabs. 
The **Enrollment tokens** and **Uninstall tokens** tabs are unavailable.

The set of actions available for an agent are limited to viewing the agent and requesting a diagnostics bundle.

You can view agent policies, but you cannot create a new policy.

:::{image} images/kibana-fleet-privileges-all-view.png
:alt: Fleet UI showing four tabs available
:screenshot:
:::

You can view {{fleet}} settings, but they are not editable.

:::{image} images/kibana-fleet-privileges-view-settings.png
:alt: Fleet UI showing settings are non-editable
:screenshot:
:::

### Example 3: All access for {{agents}}[fleet-roles-and-privileges-sub-features-example3]

Set `All` access for {{agents}} only:

* Agents: `All`
* Agent policies: `Read`
* Settings: `Read`

With these privileges, the {{fleet}} UI shows all tabs.

All {{agent}} actions can be performed and new agents can be created. Enrollment tokens and uninstall tokens are both available. Access to {{fleet}} settings is still read-only.

:::{image} images/kibana-fleet-privileges-agent-all.png
:alt: Fleet UI showing all tabs available
:screenshot:
:::

To add a {{fleet-server}}, also set the **Agent policies** and **Settings** privileges to `All`.


## {{fleet}} privileges and available actions [fleet-roles-and-privileges-sub-features-table]

This table shows the set of available actions for the `read` or `all` privilege for each {{fleet}} feature.

|Component |`read` privilege |`all` privilege |
| --- | --- | --- |
| Agents | View-only access to {{agents}}, including:<br><br>* [View a list of all agents and their status](/reference/fleet/monitor-elastic-agent.md#view-agent-status)<br>* [Request agent diagnostic packages](/reference/fleet/monitor-elastic-agent.md#collect-agent-diagnostics) |Full access to manage {{agents}}, including:<br><br>* [Assign agents to a policy](/reference/fleet/agent-policy.md#apply-a-policy)<br>* [Perform upgrades](/reference/fleet/upgrade-elastic-agent.md)<br>* [Migrate agents to a new cluster](/reference/fleet/migrate-elastic-agent.md)<br>* [Unenroll agents from {{fleet}}](/reference/fleet/unenroll-elastic-agent.md)<br>* [Create and revoke enrollment tokens](/reference/fleet/fleet-enrollment-tokens.md) |
| Agent policies | View-only access, including:<br><br>* Agent policies and settings<br>* The integrations associated with a policy, if the role also has `read` or `all` for **Integrations** | Full access to manage agent policies, including:<br><br>* [Create a policy](/reference/fleet/agent-policy.md#create-a-policy)<br>* [Edit or delete a policy](/reference/fleet/agent-policy.md#policy-main-settings)<br>* [Change the output of a policy](/reference/fleet/agent-policy.md#change-policy-output)<br>* [Configure agent monitoring](/reference/fleet/agent-policy.md#change-policy-enable-agent-monitoring)<br>* [Set the inactivity timeout](/reference/fleet/set-inactivity-timeout.md)<br><br>If the role also has `all` for **Integrations**:<br><br>* [Add an integration to a policy](/reference/fleet/agent-policy.md#add-integration)<br>* [Edit or delete an integration policy](/reference/fleet/agent-policy.md#policy-edit-or-delete)<br>* [Copy a policy](/reference/fleet/agent-policy.md#copy-policy) |
| Settings | View-only access, including:<br><br>* Configured {{fleet}} hosts<br>* {{fleet}} output settings<br>* The location to download agent binaries | Full access to manage {{fleet}} settings, including:<br><br>* [Editing hosts](/reference/fleet/fleet-settings.md#fleet-server-hosts-setting)<br>* [Adding or editing outputs](/reference/fleet/fleet-settings.md#output-settings)<br>* [Update the location for downloading agent binaries](/reference/fleet/fleet-settings.md#fleet-agent-binary-download-settings) |
| Generate reports {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` | Not available. This component has an `all` privilege only. | [Export the {{agent}}s list to a CSV file](/reference/fleet/export-agents-csv.md) from the **Agents** tab. The role also needs `read` or `all` for **Agents**. |

## Privileges for integrations and integration policies [fleet-roles-and-privileges-integrations]

When you add an integration to an agent policy, {{fleet}} creates an [integration policy](/reference/fleet/view-integration-policies.md) that stores the integration's settings. Viewing or managing integration policies, and installing integration packages, requires privileges for both {{fleet}} **Agent policies** and **Integrations**. If you don't customize {{fleet}} sub-feature privileges, the **Fleet** privilege sets the **Agent policies** access level.

| Action | {{fleet}} **Agent policies** privilege | **Integrations** privilege |
| --- | --- | --- |
| Browse integrations and view their details | Not required | `read` or `all` |
| View integration policies | `read` or `all` | `read` or `all` |
| Add integrations to agent policies, and edit, upgrade, or delete integration policies | `all` | `all` |
| Install, upgrade, uninstall, or upload integration packages | `all` | `all` |

The **Integrations** feature has no sub-feature privileges. A role that can edit integration policies can also install, upgrade, and uninstall integration packages.
