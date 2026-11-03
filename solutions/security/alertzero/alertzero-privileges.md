---
navigation_title: AlertZero privileges
description: "Give each person on your team the AlertZero access their work needs in Elastic Security, with a serverless predefined role or a custom role for analysts and administrators."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Grant access to {{alertzero}} [alertzero-privileges]

Give each person on your team only the {{alertzero}} access their work needs, whether they view {{alertzero}}, approve or decline {{az-proposed-actions}}, or set up {{az-workers}}.

Most {{alertzero}} access comes from the **{{alertzero}}**, **Proposed Actions**, and **Agentic Investigations** features in {{kib}}. A [predefined role](#alertzero-assign-predefined-role) already includes these features, so it's the quickest way to give someone access. To grant narrower access, [build a custom role](#alertzero-build-custom-role) from the privileges for each job.

## Assign a predefined role [alertzero-assign-predefined-role]

To give someone {{alertzero}} access without creating a custom role, assign a predefined role.

### {{serverless-short}} predefined roles [alertzero-predefined-roles-serverless]

```{applies_to}
stack: unavailable
serverless: preview
```

In {{serverless-short}}, assign one of these [predefined roles](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table):

| Predefined roles | What they can do in {{alertzero}} |
| --- | --- |
| - Admin | - Everything, including turning {{az-workers}} on or off and changing their settings |
| - Editor<br>- SOC manager<br>- Tier 3 analyst<br>- Rule author<br>- Detections admin<br>- Platform engineer | - Approve or decline {{az-proposed-actions}}, if they also have the [privileges for each action](#alertzero-action-privileges)<br>- Manage {{az-investigations}}<br>- Manage {{az-escalations}}<br>- Start onboarding, but not turn on {{az-workers}} |
| - Tier 1 analyst<br>- Tier 2 analyst<br>- Threat intelligence analyst<br>- Endpoint operations analyst<br>- Endpoint policy manager | - Approve or decline {{az-proposed-actions}}, if they also have the [privileges for each action](#alertzero-action-privileges)<br>- Manage {{az-investigations}}<br>- Manage {{az-escalations}} |
| - Viewer | - View {{alertzero}} without making changes |

### {{stack}} built-in roles [alertzero-predefined-roles-stack]

```{applies_to}
stack: preview 9.6
serverless: unavailable
```

On {{stack}}, assign one of these [built-in roles](elasticsearch://reference/elasticsearch/roles.md):

| Built-in role | What they can do in {{alertzero}} |
| --- | --- |
| superuser | - Everything, including turning {{az-workers}} on or off and changing their settings |
| editor | - Approve or decline {{az-proposed-actions}}. To approve host isolation and process actions, they also need the [{{elastic-defend}} privileges](#alertzero-action-privileges).<br>- Manage {{az-investigations}}<br>- View {{az-escalations}}, but not open, assign, or link them<br>- Turn on {{alertzero}} in a space and start onboarding, but not turn on {{az-workers}} |
| viewer | - View {{alertzero}} without making changes |

## Build a custom role [alertzero-build-custom-role]

Build a [custom role](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md#adding_kibana_privileges) from the privileges for each job the analayst does.

### Let analysts review proposed actions and investigations [alertzero-analyst-access]

Every analyst needs the privileges in the first row. Add the privileges in the other rows for each task the analyst does.

| To let someone | Add |
| --- | --- |
| View {{alertzero}}, its {{az-watch}} settings, and the **{{az-proposed-actions-cap}}** page | **{{alertzero}}**: **Read** and **Proposed Actions**: **Read** |
| Approve or decline {{az-proposed-actions}} | **Proposed Actions**: **All**, plus the [privileges for each action](#alertzero-action-privileges) they approve |
| See impacted entities, and filter {{az-proposed-actions}} by entity | **Agentic Investigations**: **Read** |
| Open {{az-investigation}} details or chats | **Agent Builder**: **Read** |
| Assign, close, or reopen {{az-investigations}} | **Agentic Investigations**: **All**, or its **Manage investigations** sub-feature privilege |
| View {{az-escalations}} | **Agentic Investigations**: **Read**, or its **View escalations** sub-feature privilege |
| Open, assign, or link {{az-escalations}} | **Agentic Investigations**: **Manage escalations** sub-feature privilege, which **All** doesn't include |

### Let analysts run the actions they approve [alertzero-action-privileges]

Approving an action doesn't grant the privileges to run it. An approved action runs as the person who approved it, so grant each analyst the privileges for the actions they approve. Without them, the action fails.

| Action | Privileges |
| --- | --- |
| Close alerts | **Alerts**: **All** |
| Create, edit, or turn on a detection rule, or add a rule exception | **Rules and Exceptions**: **All** |
| Isolate a host | **Security**: **All**, with the [{{elastic-defend}} sub-feature privileges](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md#response-actions) **Host Isolation** and **Response Actions History** |
| Kill or suspend a process | **Security**: **All**, with the [{{elastic-defend}} sub-feature privileges](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md#response-actions) **Process Operations** and **Response Actions History** |

A detection rule that an analyst creates, changes, installs, or turns on by approving an action runs with that analyst's privileges, as it does after any rule edit. Refer to [Rule authorization](/solutions/security/detect-and-alert/detection-rule-concepts.md#rule-authorization-concept).

At {{az-supervised}} {{az-autonomy}}, a {{az-worker}} approves its own {{az-proposed-actions}}, and they run as the {{az-worker}}'s [service account](#alertzero-worker-privileges). Analysts don't need the action privileges for those actions.

### Let administrators set up and manage {{az-workers}} [alertzero-admin-access]

Add the privileges for each task the administrator does.

| To let someone | The role needs |
| --- | --- |
| Turn on {{alertzero}} in a space | **Advanced Settings**: **All** |
| Start {{alertzero}} onboarding | **{{alertzero}}**: **All** |
| Change the models the {{az-workers}} use | The privileges for **Feature Settings**. Refer to [Manage access to AI features](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#requirements). |
| Edit {{az-worker}} settings, such as {{az-autonomy}} | **{{alertzero}}**: **All** and the `manage_security` cluster privilege |
| Turn {{az-workers}} on or off | **{{alertzero}}**: **All**, the `manage_security` cluster privilege, and **Workflows**: **Update** and **Update managed workflows**, which **All** doesn't include |
| Run {{az-workers}} on demand from Workflows | **Workflows**: **Execute**. Refer to [](run-worker-on-demand.md). |
| View {{az-worker}} execution history | **Workflows**: **Read**, or its **Read Workflow Execution** and **Read managed workflow execution** sub-feature privileges. Refer to [](view-execution-history.md). |

The `manage_security` cluster privilege lets anyone who has it manage users and roles for the whole cluster, so don't grant it only for {{alertzero}}. Instead, have an administrator who already has it set up the {{az-workers}}.

## Privileges the {{az-workers}} run with [alertzero-worker-privileges]

Each {{az-worker}} runs as its own service account with a built-in role of the same name, such as `alertzero_alert_triage` for {{az-alert-triage}}. In {{serverless-short}}, the role name starts with an underscore, such as `_alertzero_alert_triage`. You can't edit or delete these roles.

{{alertzero}} creates the service accounts with the privileges of the person who turns on the {{az-workers}}. Creating a service account requires the `manage_security` cluster privilege, so that person needs it.
