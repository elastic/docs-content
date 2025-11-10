---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-roles-and-privileges.html
products:
  - id: fleet
  - id: elastic-agent
---

# Roles and privileges [fleet-roles-and-privileges]

Use {{kib}} roles and privileges to grant users access to {{fleet}} and Integrations.
{{fleet}} and integrations privileges can be set to:

`all`
:   Grants full read-write access.

`read`
:   Grants read-only access.

`none`
:   No access is granted.

You can take advantage of these privilege settings by:

* [Using an {{es}} built-in role](#fleet-roles-and-privileges-built-in)
* [Creating a new role](#fleet-roles-and-privileges-create).

To configure access at a more granular level, select a custom set of privileges for individual {{fleet}} features:

* [Customize sub-feature privileges for {{fleet}}](#fleet-roles-and-privileges-sub-features) {applies_to}`stack: ga 9.1`


## Built-in roles [fleet-roles-and-privileges-built-in]

{{es}} comes with built-in roles that include default privileges.

`editor`
:   The built-in `editor` role grants these privileges, supporting full read-write access to {{fleet}} and Integrations:
* {{Fleet}}: `all`
* Integrations: `all`

`viewer`
:   The built-in `viewer` role grants these privileges, supporting read-only access to {{fleet}} and Integrations:

* {{Fleet}}:: `read`
* Integrations:: `read`

You can also create a new role that can be assigned to a user, in order to grant more specific levels of access to {{fleet}} and Integrations.


## Create a new role for {{fleet}} [fleet-roles-and-privileges-create]

To create a new role with access to {{fleet}} and Integrations:

1. In {{kib}}, go to **Management → Stack Management**.
2. In the **Security** section, select **Roles**.
3. Select **Create role**.
4. Specify a name for the role.
5. Leave the {{es}} settings at their defaults, or refer to [Security privileges](elasticsearch://reference/elasticsearch/security-privileges.md) for descriptions of the available settings.
6. In the {{kib}} section, select **Assign to space**.
7. In the **Spaces** menu, select **All Spaces**. 
  Because many Integrations assets are shared across spaces, users need the {{kib}} privileges in all spaces.
8. Expand the **Management** section.
9. Set **Fleet** privileges to **All**.
10. Choose the access level that you'd like the role to have with respect to {{fleet}} and integrations:
    1. To grant the role full access to use and manage {{fleet}} and integrations, set both the **Fleet** and **Integrations** privileges to `All`.
    :::{image} images/kibana-fleet-privileges-all.png
    :alt: Kibana privileges flyout showing Fleet and Integrations access set to All
    :screenshot:
    :::
    2. To create a read-only user for {{fleet}} and Integrations, set both the **Fleet** and **Integrations** privileges to `Read`.
    :::{image} images/kibana-fleet-privileges-read.png
    :alt: Kibana privileges flyout showing Fleet and Integrations access set to All
    :screenshot:
    :::
    3. If you'd like to define more specialized access to {{fleet}} based on individual components, expand the **Fleet** menu and enable **Customize sub-feature privileges**.
    :::{image} images/kibana-fleet-privileges-enable.png
    :alt: Kibana customize sub-feature privileges UI
    :screenshot:
    :::
    <br>
    Any setting for individual {{fleet}} components that you specify here takes precedence over the general `All`, `Read`, or `None` privilege set for {{fleet}}.
    
    Based on your selections, access to features in the {{fleet}} UI are enabled or disabled for the role. 
    Those details are covered in the next section: [Customize access to {{fleet}} features](#fleet-roles-and-privileges-sub-features).

After you've created a new role, you can assign it to any {{es}} user.
You can edit the role at any time by returning to the **Roles** page in {{kib}}.

## Customize sub-feature privileges for {{fleet}}[fleet-roles-and-privileges-sub-features]

```{applies_to}
stack: ga 9.1
```

Beginning with {{stack}} version 9.1, you have more granular control when [creating a new role](#fleet-roles-and-privileges-create) or editing it. This is useful when people in your organization access {{fleet}} for different purposes, and you need to fine-tune the components that they can view and the actions that they can perform.

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

All {{agent}} actions can be performed and new agents can be created. Enrollment tokens and uninstall tokens are both available.

:::{image} images/kibana-fleet-privileges-agent-all.png
:alt: Fleet UI showing all tabs available
:screenshot:
:::

Access to {{fleet}} settings is still read-only. 
To enable actions such as creating a new {{fleet-server}}, set the **Fleet Settings** privilege to `All`.


## {{fleet}} privileges and available actions [fleet-roles-and-privileges-sub-features-table]

```{applies_to}
stack: ga 9.1
```


This table shows the set of available actions for the `read` or `all` privilege for each {{fleet}} feature.

|Component |`read` privilege |`all` privilege |
| --- | --- | --- |
| Agents | View-only access to {{agents}}, including:<br><br>* [View a list of all agents and their status](/reference/fleet/monitor-elastic-agent.md#view-agent-status)<br>* [Request agent diagnostic packages](/reference/fleet/monitor-elastic-agent.md#collect-agent-diagnostics) |Full access to manage {{agents}}, including:<br><br>* [Perform upgrades](/reference/fleet/upgrade-elastic-agent.md)<br>* [Configure monitoring](/reference/fleet/monitor-elastic-agent.md)<br>* [Migrate agents to a new cluster](/reference/fleet/migrate-elastic-agent.md)<br>* [Unenroll agents from {{fleet}}](/reference/fleet/unenroll-elastic-agent.md)<br>* [Set the inactivity timeout](/reference/fleet/set-inactivity-timeout.md)<br>* [Create and revoke enrollment tokens](/reference/fleet/fleet-enrollment-tokens.md) |
| Agent policies | View-only access, including:<br><br>* Agent policies and settings<br>* The integrations associated with a policy | Full access to manage agent policies, including:<br><br>* [Create a policy](/reference/fleet/agent-policy.md#create-a-policy)<br>* [Add an integration to a policy](/reference/fleet/agent-policy.md#add-integration)<br>* [Apply a policy](/reference/fleet/agent-policy.md#apply-a-policy)<br>* [Edit or delete an integration](/reference/fleet/agent-policy.md#policy-edit-or-delete)<br>* [Copy a policy](/reference/fleet/agent-policy.md#copy-policy)<br>* [Edit or delete a policy](/reference/fleet/agent-policy.md#policy-main-settings)<br>* [Change the output of a policy](/reference/fleet/agent-policy.md#change-policy-output) |
| Fleet settings | View-only access, including:<br><br>* Configured {{fleet}} hosts<br>* {{fleet}} output settings<br>* The location to download agent binaries | Full access to manage {{fleet}} settings, including:<br><br>* [Editing hosts](/reference/fleet/fleet-settings.md#fleet-server-hosts-setting)<br>* [Adding or editing outputs](/reference/fleet/fleet-settings.md#output-settings)<br>* [Update the location for downloading agent binaries](/reference/fleet/fleet-settings.md#fleet-agent-binary-download-settings) |
