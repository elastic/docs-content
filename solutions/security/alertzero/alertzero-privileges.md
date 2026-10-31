---
description: "Find the Kibana feature privileges, cluster privilege, and action privileges each AlertZero task needs in Elastic Security, and which serverless predefined roles include them."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# {{alertzero}} privileges [alertzero-privileges]

Use the tables on this page to give each person only the access their work needs: viewing {{alertzero}}, acting on {{az-proposed-actions}}, or setting up {{az-workers}}. {{alertzero}} uses three {{kib}} features: **{{alertzero}}**, **Proposed Actions**, and **Agentic Investigations**. Some tasks also need **Agent Builder**, **Workflows**, or **Advanced Settings** privileges, the `manage_security` cluster privilege, or the privileges of each action you approve.

On {{stack}} deployments, these features require an Enterprise license. In {{serverless-short}}, {{alertzero}} requires the Security Analytics Complete feature tier instead. Refer to [](requirements.md).

## Find the privileges in the role editor [alertzero-privileges-where]

In the [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md#adding_kibana_privileges) section of the role editor, **{{alertzero}}** is in the **Security** group. **Proposed Actions**, **Agentic Investigations**, **Agent Builder**, and **Workflows** are in the **Analytics** group. To grant a sub-feature privilege, such as **Manage escalations**, turn on **Customize sub-feature privileges** for that feature.

{applies_to}`serverless: preview` With the Security Analytics Complete feature tier, **Agent Builder** and **Workflows** are in the **Security** group instead.

## Privileges to use {{alertzero}} [alertzero-privileges-use]

| To do this | The role needs |
| --- | --- |
| See {{alertzero}} in the navigation menu and view {{az-watch}} settings | **{{alertzero}}**: **Read** |
| View the **{{az-proposed-actions-cap}}** page | **{{alertzero}}**: **Read** and **Proposed Actions**: **Read** |
| Approve or decline {{az-proposed-actions}} | **Proposed Actions**: **All**, plus the [privileges for the action](#alertzero-privileges-actions) |
| See impacted entities and filter the **{{az-proposed-actions-cap}}** page by entity | **Agentic Investigations**: **Read** |
| Assign, close, or reopen {{az-investigations}} | The **Manage investigations** sub-feature privilege of **Agentic Investigations**, which **All** includes |
| Open {{az-investigation}} details or chats | **Agent Builder**: **Read** |
| View {{az-escalations}} | The **View escalations** sub-feature privilege of **Agentic Investigations**, which **Read** and **All** include |
| Open, assign, or link {{az-escalations}} | The **Manage escalations** sub-feature privilege of **Agentic Investigations**. **All** doesn't include it, so grant it separately. |

Without **Proposed Actions**: **Read**, the **{{az-proposed-actions-cap}}** page shows a message that names the missing privilege instead of the list of {{az-proposed-actions}}.

## Privileges to set up and configure {{az-workers}} [alertzero-privileges-configure]

| To do this | The role needs |
| --- | --- |
| Turn on the {{alertzero}} advanced setting | **Advanced Settings**: **All** |
| Select **Continue** on the first setup step | **{{alertzero}}**: **All** |
| Edit {{az-worker}} settings, such as {{az-autonomy}} | **{{alertzero}}**: **All** and the `manage_security` cluster privilege |
| Turn {{az-workers}} on or off | **{{alertzero}}**: **All**, the `manage_security` cluster privilege, and the **Workflows** sub-feature privileges **Update** and **Update managed workflows** |
| Run {{az-workers}} on demand from Workflows | The **Workflows** sub-feature privilege **Execute**. Refer to [](run-worker-on-demand.md). |

Granting **All** for **Workflows** doesn't include **Update managed workflows**, so grant it separately. For the full list, refer to [Workflows sub-feature privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#kibana-privileges-workflows-subfeatures).

The `manage_security` privilege also lets a user manage users and roles for the whole cluster. Instead of granting it only for {{alertzero}}, ask an administrator who already has it to set up {{az-workers}}.

## Privileges for the actions you approve [alertzero-privileges-actions]

The privilege to approve an action doesn't include the privileges to run it. When you approve {{az-proposed-actions}}, the actions run as you, so your role needs **Proposed Actions**: **All** and the privileges the action itself needs:

| Action | Privileges |
| --- | --- |
| Close alerts | **Alerts**: **All** |
| Create, edit, or turn on a detection rule, or add a rule exception | **Rules and Exceptions**: **All** |
| Isolate a host | **Security**: **All**, with the [{{elastic-defend}} sub-feature privileges](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md#response-actions) **Host Isolation** and **Response Actions History** |
| Kill or suspend a process | **Security**: **All**, with the [{{elastic-defend}} sub-feature privileges](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md#response-actions) **Process Operations** and **Response Actions History** |

When {{az-workers}} approve their own {{az-proposed-actions}} at {{az-supervised}} {{az-autonomy}}, the actions run as each {{az-worker}}'s service account instead.

## {{az-worker}} service accounts [alertzero-privileges-service-accounts]

Each {{az-worker}} runs as its own service account, such as `alertzero_alert_triage` for {{az-alert-triage}}. The account uses a built-in role with the same name, or with a leading underscore in {{serverless-short}}, such as `_alertzero_alert_triage`. You can't edit or delete these roles.

When you turn on a {{az-worker}}, {{alertzero}} creates its service account with your privileges. That's why turning on {{az-workers}} needs the `manage_security` cluster privilege.

## Predefined roles [alertzero-privileges-predefined-roles]
```{applies_to}
serverless: preview
```

These [{{serverless-short}} predefined roles](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table) include {{alertzero}} privileges:

| Roles | {{alertzero}} privileges |
| --- | --- |
| Editor, SOC manager, Tier 3 analyst, Rule author, Detections admin, Platform engineer | **All** for **{{alertzero}}**, **Proposed Actions**, and **Agentic Investigations**, plus **Manage escalations** and **Update managed workflows** |
| Tier 1 analyst, Tier 2 analyst, Threat intelligence analyst, Endpoint operations analyst, Endpoint policy manager | **Read** for **{{alertzero}}** and **All** for **Proposed Actions** and **Agentic Investigations**, plus **Manage escalations** |
| Viewer | **Read** for **{{alertzero}}**, **Proposed Actions**, and **Agentic Investigations** |

None of these roles includes the `manage_security` cluster privilege, so none of them can edit {{az-worker}} settings or turn {{az-workers}} on or off.
