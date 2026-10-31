---
navigation_title: AlertZero privileges
description: "Grant the Kibana feature privileges, cluster privilege, and action privileges a role needs to view, set up, and decide in AlertZero in Elastic Security."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# {{alertzero}} privileges [alertzero-privileges]

Access to {{alertzero}} spans three {{kib}} features, a cluster privilege, Workflows, and the privileges of each action that someone approves. Use the tables on this page to give each person only what their work needs: viewing, deciding {{az-proposed-actions}}, or setting up {{az-workers}}.

The **{{alertzero}}**, **Proposed Actions**, and **Agentic Investigations** features all require an Enterprise license. In {{serverless-short}}, {{alertzero}} also requires the Security Analytics Complete feature tier. Refer to [](requirements.md).

## Find the privileges in the role editor [alertzero-privileges-where]

In the [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md#adding_kibana_privileges) section of the role editor, **{{alertzero}}** is in the **Security** group. **Proposed Actions** and **Agentic Investigations** are in the **Analytics** group.

{applies_to}`serverless: preview` In {{serverless-short}} projects with the Security Analytics Complete feature tier, **Agent Builder** and **Workflows** are in the **Security** group.

## Privileges to view and decide [alertzero-privileges-use]

| To do this | The role needs |
| --- | --- |
| See {{alertzero}} in the navigation menu and view {{az-watch}} settings | **{{alertzero}}**: **Read** |
| View the **{{az-proposed-actions-cap}}** page | **{{alertzero}}**: **Read** and **Proposed Actions**: **Read** |
| Approve or decline {{az-proposed-actions}} | **Proposed Actions**: **All**, plus the [privileges for the action](#alertzero-privileges-actions) |
| See impacted entities and filter the page by entity | **Agentic Investigations**: **Read** |
| Assign, close, or reopen {{az-investigations}} | The **Manage investigations** sub-feature privilege of **Agentic Investigations**, which **All** includes |
| Open {{az-investigation}} details or chats | **Agent Builder**: **Read** |
| View {{az-escalations}} | The **View escalations** sub-feature privilege of **Agentic Investigations**, which **Read** and **All** include |
| Open, assign, or link {{az-escalations}} | The **Manage escalations** sub-feature privilege of **Agentic Investigations**. **All** doesn't include it, so assign it explicitly. |

Without **Proposed Actions**: **Read**, the **{{az-proposed-actions-cap}}** page shows a message that names the missing privilege instead of the queue.

## Privileges to set up and configure {{az-workers}} [alertzero-privileges-configure]

| To do this | The role needs |
| --- | --- |
| Turn on the {{alertzero}} advanced setting | **Advanced Settings**: **All** |
| Continue past the first onboarding step | **{{alertzero}}**: **All** |
| Change {{az-worker}} settings, such as {{az-autonomy}} | **{{alertzero}}**: **All** and the `manage_security` cluster privilege |
| Turn {{az-workers}} on or off | **{{alertzero}}**: **All**, the `manage_security` cluster privilege, and the **Workflows** sub-feature privileges **Update** and **Update managed workflows** |
| Run {{az-workers}} on demand from Workflows | The **Workflows** sub-feature privilege **Execute**. Refer to [](run-worker-on-demand.md). |

Granting **All** for **Workflows** doesn't include **Update managed workflows**, so assign it explicitly. For the full list, refer to [Workflows sub-feature privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#kibana-privileges-workflows-subfeatures).

The `manage_security` privilege also lets a user manage users and roles for the whole cluster. Instead of granting it only for {{alertzero}}, ask an admin who already has it to set up {{az-workers}}.

## Privileges for the actions you approve [alertzero-privileges-actions]

Approving an action is separate from being allowed to run it. When you approve {{az-proposed-actions}}, the actions run as you, so your role needs **Proposed Actions**: **All** and the privileges the action itself needs:

| Action | Privileges |
| --- | --- |
| Close alerts | **Alerts**: **All** |
| Create, change, or turn on a detection rule, or add a rule exception | **Rules and Exceptions**: **All** |
| Isolate a host | The [{{elastic-defend}} sub-feature privileges](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md#response-actions) **Host Isolation** and **Response Actions History** |
| Kill or suspend a process | The [{{elastic-defend}} sub-feature privileges](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md#response-actions) **Process Operations** and **Response Actions History** |

When {{az-workers}} approve their own {{az-proposed-actions}} at {{az-supervised}} {{az-autonomy}}, the actions run as each {{az-worker}}'s service account instead.

## {{az-worker}} service accounts [alertzero-privileges-service-accounts]

Each {{az-worker}} runs as its own service account, such as `alertzero_alert_triage` for {{az-alert-triage}}. The account uses a built-in role with the same name, or with a leading underscore in {{serverless-short}}, such as `_alertzero_alert_triage`. You can't edit or delete these roles.

{{alertzero}} creates each {{az-worker}}'s service account when someone turns that {{az-worker}} on, using that person's privileges. That's why turning on {{az-workers}} needs the `manage_security` cluster privilege.

## Predefined roles [alertzero-privileges-predefined-roles]

```{applies_to}
serverless: preview
```

These [{{serverless-short}} predefined roles](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table) include {{alertzero}} privileges:

| Roles | {{alertzero}} privileges |
| --- | --- |
| Editor, SOC manager, Tier 3 analyst, Rule author, Detections admin, Platform engineer | **All** for **{{alertzero}}**, **Proposed Actions**, and **Agentic Investigations**, plus **Manage escalations** and **Update managed workflows** |
| Tier 1 analyst, Tier 2 analyst, Threat intelligence analyst, Endpoint operations analyst, Endpoint policy manager | **Read** for **{{alertzero}}**, and **All** for **Proposed Actions** and **Agentic Investigations**, plus **Manage escalations** |
| Viewer | **Read** for **{{alertzero}}**, **Proposed Actions**, and **Agentic Investigations** |

None of these roles includes the `manage_security` cluster privilege, so none of them can change {{az-worker}} settings or turn {{az-workers}} on or off.
