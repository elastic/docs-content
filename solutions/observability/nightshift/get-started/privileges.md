---
navigation_title: Grant access
applies_to:
  serverless:
    observability: preview
description: Give each person on your team the Elastic nightshift access their work needs, with a predefined role or a custom role, and learn which privileges Elastic nightshift itself runs with.
products:
  - id: observability
  - id: cloud-serverless
---

# Grant access to {{nightshift}} [nightshift-privileges]

Give each person the {{nightshift}} access their work needs: viewing investigations, starting investigations, deciding on proposed actions, or setting up and managing {{nightshift}}. This page also explains the privileges that {{nightshift}} itself runs with, so you know what it can access.

## Assign a predefined role [nightshift-privileges-predefined]

Use [predefined roles](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table) to give access for {{serverless-short}} projects.

| Predefined role | {{nightshift}} access |
| --- | --- |
| **Admin** | Enable {{nightshift}}, manage engines and settings, add connectors, and create and edit automations |
| **Editor** | Start investigations, chat with {{nightshift}}, and mark proposed actions as applied or declined |
| **Viewer** | View the home page, investigations, and proposed actions without making changes |

## Build a custom role [nightshift-privileges-custom]

To give access based on the job a specific person does, build a [custom role](/deploy-manage/users-roles/serverless-custom-roles.md). The {{nightshift}} privileges are in the **Observability** group. For the other privileges in that group, refer to [Observability {{kib}} privileges](/solutions/observability/get-started/observability-kibana-privileges.md).

### Review and decide on investigations [nightshift-privileges-analyst]

The **Nightshift**: **Read** privilege is required for all {{nightshift}}. Add additional privileges to meet user needs.

| Privilege | Access |
| --- | --- |
| **Nightshift**: **Read** | View the home page, investigations, and proposed actions |
| **Nightshift**: **All**, **Agent Builder**: **All**, permission to run workflows, and read access to connectors | Start an investigation |
| **Nightshift**: **All** | Mark a proposed action as applied or declined |
| Access to **Agent Builder** | Open an investigation in chat |
| **Nightshift**: **Read** | View the **Knowledge** page |
| **Nightshift**: **All** | Archive, restore, or delete entries on the **Knowledge** page |

**Read** and **All** cover every investigation and proposed action in the space, including ones that other solutions create.

### Let admins set up and manage {{nightshift}} [nightshift-privileges-admin]

Add the privileges for each task the admin does.

| Privilege | Access |
| --- | --- |
| **Nightshift**: **Manage engines**, and the `manage_security` cluster privilege | Enable {{nightshift}} for a space |
| **Nightshift**: **All** and **Manage engines** | Open **Settings**, pause or resume engines, and change limits |
| **Nightshift**: **Manage engines** | Create, edit, turn on or off, or delete detection sources |
| **Nightshift**: **All** and **Manage engines** | Connect a Slack workspace or channel |
| **Advanced Settings**: **All** | Turn developer mode on or off |
| **Nightshift**: **All**, and the `manage_security` cluster privilege. {{nightshift}} must be enabled for the space. | Create, edit, turn on or off, or delete an automation |

- **Manage engines** isn't part of **All**. Add it explicitly.
- Sources decide which data detection reads, and the significant events it finds are visible to everyone with {{nightshift}} access in the space. Give **Manage engines** only to people who should make that choice.
- `manage_security` lets its holder manage users and roles for the whole project. Don't grant it only for {{nightshift}}. Instead, have an admin who already has it enable {{nightshift}} and manage automations.

## Privileges that {{nightshift}} runs with [nightshift-privileges-accounts]

{{nightshift}} runs investigations and automations as two service accounts. This way, they keep working no matter who set them up, and they can reach the same data for everyone.

| Account | Runs | What it can do |
| --- | --- | --- |
| `nightshift_agent` | Investigations, their sandbox tools, and chats with the investigation agent, including `@Elastic` in Slack | Read and write the Wiki, Memory, and decision trees. Use {{nightshift}} and **Agent Builder**. Run the connectors in the space. |
| `nightshift_automations` | Automation workflows | Read alerts and alerting rules. Start investigations. Use **Agent Builder**. Run the connectors in the space. |

Investigations reach your data and code through the connectors in the space, with the credentials stored in each connector. The access you give a connector matters. A read-only API key or a token for selected repositories limits what every investigation can read. Detection reads the data that your detection sources select.

This also means that anyone who can start an investigation, or mention `@Elastic` in a connected Slack channel, gets answers based on what these accounts and connectors can reach, not on their own privileges.

:::{dropdown} What enabling {{nightshift}} sets up
When an admin selects **Enable {{nightshift}}**, {{nightshift}}:

- Finds or creates the `nightshift_agent` and `nightshift_automations` service accounts. There is one of each per deployment, shared by every space.
- Installs the investigation agent in the space and binds it to `nightshift_agent`, so every run of it executes as that account.
- Installs the workflows that run investigations and Slack threads in the space, bound to `nightshift_agent`.
- Creates a **Local Elasticsearch** connector for the data in your project. It uses a managed API key with the role `nightshift_local_read`: `read` and `view_index_metadata` on `logs-*`, `metrics-*`, and `traces-*`, and no cluster privileges.

Each account has a predefined {{serverless-short}} role, `_nightshift_agent` or `_nightshift_automations`. {{nightshift}} doesn't create or change these roles. Don't assign them to users.

Each automation's workflow runs as `nightshift_automations`, and starts its investigations through the space's workflow, which runs them as `nightshift_agent`.

On **Settings** > **Investigations**, the **Service account** row shows whether the space is **Set up**.
:::

To stop {{nightshift}} from running, refer to [Stop or pause {{nightshift}}](../settings.md#nightshift-settings-stop).

## Next steps [nightshift-privileges-next]

- [Get started](./investigations.md): Enable {{nightshift}} and run your first investigation.
- [Connect your data and tools](../investigation/set-up.md): Add connectors with the least access that investigations need.
- [Cost and models](../cost-and-models.md#nightshift-data): Find out what {{nightshift}} sends to models and what it stores.
