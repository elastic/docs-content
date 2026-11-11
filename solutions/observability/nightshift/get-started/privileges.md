---
applies_to:
  serverless:
    observability: preview
description: Give each person on your team the Elastic nightshift access their work needs, with a serverless predefined role or a custom role for analysts and administrators.
products:
  - id: observability
  - id: cloud-serverless
---

# Grant access to Elastic nightshift [nightshift-privileges]

Give each person on your team the Elastic nightshift access their work needs, whether they view investigations, start them, decide proposed actions, or set up and manage Elastic nightshift.

## Assign a predefined role [nightshift-privileges-predefined]

To give someone Elastic nightshift access without creating a custom role, assign one of the [predefined roles](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table) for {{serverless-short}} projects.

| Predefined role | What they can do in Elastic nightshift |
| --- | --- |
| Admin | Enable Elastic nightshift, manage engines, add connectors, and create and edit automations |
| Editor | Start investigations, chat with Elastic nightshift, and mark proposed actions as applied or declined |
| Viewer | View the home page, investigations, and proposed actions without making changes |

## Build a custom role [nightshift-privileges-custom]

% TODO(verify): Do we want to allow users to create custom roles?

Build a [custom role](/deploy-manage/users-roles/serverless-custom-roles.md) from the privileges for each job the person does. For the other privileges in the **Observability** group, refer to [Observability {{kib}} privileges](/solutions/observability/get-started/observability-kibana-privileges.md).

### Let people review and decide on investigations [nightshift-privileges-analyst]

Every person needs the privileges in the first row. Add the privileges in the other rows for each task they do.

| To let someone | Add |
| --- | --- |
| View the home page, investigations, and proposed actions | **Nightshift**: **Read** |
| Start an investigation | **Nightshift**: **All**, **Agent Builder**: **All**, permission to run workflows, and read access to connectors |
| Mark a proposed action as applied or declined | **Nightshift**: **All** |
| Open an investigation in chat | Access to **Agent Builder** |

% TODO(verify): What level of **Agent Builder** does opening an investigation in chat need, and does an investigation also need the Workflows execute and connector read privileges listed for starting one?

The **Read** and **All** privileges cover every investigation and proposed action in the space, including ones that other solutions create, not only Elastic nightshift's.

### Let administrators set up and manage Elastic nightshift [nightshift-privileges-admin]

Add the privileges for each task the administrator does.

| To let someone | The role needs |
| --- | --- |
| Enable Elastic nightshift for a space | **Nightshift**: **Manage engines** and the `manage_security` cluster privilege |
| Pause, resume, or turn off engines, edit settings, and manage limits | **Nightshift**: **Manage engines** |
| Create, edit, turn on, turn off, or delete sources | **Nightshift**: **Manage engines** |
| Connect a Slack channel | **Nightshift**: **Manage engines** |
| Create, edit, turn on, turn off, or delete an automation | **Nightshift**: **All** and the `manage_security` cluster privilege. The space must also be enabled. |

**Manage engines** isn't part of **All**, so add it explicitly. Sources decide which indices the Elastic nightshift service account reads, and the significant events and detections it finds are shown to everyone with Elastic nightshift access in the space.

The `manage_security` cluster privilege lets anyone who has it manage users and roles for the whole cluster, so don't grant it only for Elastic nightshift. Instead, have an administrator who already has it enable Elastic nightshift and manage automations.

## Privileges that Elastic nightshift runs with [nightshift-privileges-accounts]

Elastic nightshift runs investigations and automations as service accounts, not as the person who started them. For the accounts and what they can do, refer to [What enabling sets up](../get-started.md#nightshift-get-started-enable-sets-up).

## Next steps [nightshift-privileges-nav]

- [Get started](../get-started.md#nightshift-get-started-steps): Enable Elastic nightshift and run your first investigation
- [Connect your data and tools](./connect-your-data-and-tools.md): Add the connectors that investigations use
