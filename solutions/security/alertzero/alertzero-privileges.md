---
description: "Build roles that give each person on your team the AlertZero access their work needs in Elastic Security: Kibana feature privileges, the cluster privilege, action privileges, and serverless predefined roles."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{alertzero}} privileges [alertzero-privileges]

Give each person on your team only the {{alertzero}} access their work needs, whether they view {{alertzero}}, decide {{az-proposed-actions}}, or set up {{az-workers}}. Most {{alertzero}} privileges come from three {{kib}} features: **{{alertzero}}**, **Proposed Actions**, and **Agentic Investigations**. These features require an Enterprise license on {{stack}}, or the Security Analytics Complete feature tier in {{serverless-short}}.

Keep two rules in mind when you build roles:

- Approving an action doesn't grant the privileges to run it. An approved action runs as the person who approved it, so anyone who approves actions also needs the [privileges for those actions](#alertzero-privileges-actions).
- Changing {{az-workers}} needs the `manage_security` cluster privilege. This includes turning {{az-workers}} on or off and changing their {{az-autonomy}}. Refer to [](#alertzero-privileges-configure).

## Find the privileges in the role editor [alertzero-privileges-where]

In the [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md#adding_kibana_privileges) section of the role editor, **{{alertzero}}** is in the **Security** group. **Proposed Actions**, **Agentic Investigations**, **Agent Builder**, and **Workflows** are in the **Analytics** group. To grant a sub-feature privilege, such as **Manage escalations**, turn on **Customize sub-feature privileges** for that feature.

{applies_to}`serverless: preview` In {{serverless-short}}, **Agent Builder** and **Workflows** are in the **Security** group instead.

## Privileges for analysts who use {{alertzero}} [alertzero-privileges-use]

Analysts who review and decide {{az-proposed-actions}} need some or all of the following privileges, depending on their work.

| To let someone | The role needs |
| --- | --- |
| See {{alertzero}} in the navigation menu and view {{az-watch}} settings | **{{alertzero}}**: **Read** |
| View the **{{az-proposed-actions-cap}}** page | **{{alertzero}}**: **Read** and **Proposed Actions**: **Read** |
| Approve or decline {{az-proposed-actions}} | **Proposed Actions**: **All**. To approve, the role also needs the [privileges for the action](#alertzero-privileges-actions). |
| See impacted entities and filter the **{{az-proposed-actions-cap}}** page by entity | **Agentic Investigations**: **Read** |
| Open {{az-investigation}} details or chats | **Agent Builder**: **Read** |
| Assign, close, or reopen {{az-investigations}} | **Agentic Investigations**: **All**, or its **Manage investigations** sub-feature privilege |
| View {{az-escalations}} | **Agentic Investigations**: **Read** or **All**, or its **View escalations** sub-feature privilege |
| Open, assign, or link {{az-escalations}} | The **Manage escalations** sub-feature privilege of **Agentic Investigations**. **All** doesn't include it, so grant it separately. |

## Privileges for the actions analysts approve [alertzero-privileges-actions]

Grant each analyst the privileges for the actions they approve. Without them, the action fails.

| Action | Privileges |
| --- | --- |
| Close alerts | **Alerts**: **All** |
| Create, edit, or turn on a detection rule, or add a rule exception | **Rules and Exceptions**: **All** |
| Isolate a host | **Security**: **All**, with the [{{elastic-defend}} sub-feature privileges](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md#response-actions) **Host Isolation** and **Response Actions History** |
| Kill or suspend a process | **Security**: **All**, with the [{{elastic-defend}} sub-feature privileges](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md#response-actions) **Process Operations** and **Response Actions History** |

When an analyst approves a change that creates, changes, installs, or turns on a detection rule, the rule then runs with that analyst's privileges, as it does after any rule edit. Refer to [Rule authorization](/solutions/security/detect-and-alert/detection-rule-concepts.md#rule-authorization-concept).

At {{az-supervised}} {{az-autonomy}}, {{az-workers}} approve their own {{az-proposed-actions}}, and the actions run as each {{az-worker}}'s [service account](#alertzero-privileges-service-accounts) instead.

## Privileges for administrators who set up {{az-workers}} [alertzero-privileges-configure]

Changing how {{az-workers}} run takes the `manage_security` cluster privilege. Without it, the {{az-watch}} pages are read-only. Because `manage_security` also lets anyone who has it manage users and roles for the whole cluster, don't grant it only for {{alertzero}}. Instead, have an administrator who already has it set up {{az-workers}}.

| To let someone | The role needs |
| --- | --- |
| Turn on the {{alertzero}} advanced setting | **Advanced Settings**: **All** |
| Select **Continue** on the first onboarding step | **{{alertzero}}**: **All** |
| Edit {{az-worker}} settings, such as {{az-autonomy}} | **{{alertzero}}**: **All** and the `manage_security` cluster privilege |
| Turn {{az-workers}} on or off | **{{alertzero}}**: **All**, the `manage_security` cluster privilege, and the **Workflows** sub-feature privileges **Update** and **Update managed workflows**. **All** for **Workflows** doesn't include **Update managed workflows**, so grant it separately. |
| Run {{az-workers}} on demand from Workflows | The **Workflows** sub-feature privilege **Execute**. Refer to [](run-worker-on-demand.md). |

For the full list of **Workflows** privileges, refer to [Workflows sub-feature privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#kibana-privileges-workflows-subfeatures).

## {{az-worker}} service accounts [alertzero-privileges-service-accounts]

Each {{az-worker}} runs as its own service account with a built-in role of the same name, such as `alertzero_alert_triage` for {{az-alert-triage}}. In {{serverless-short}}, the role name starts with an underscore, such as `_alertzero_alert_triage`. You can't edit or delete these roles.

When someone turns on {{az-workers}}, {{alertzero}} uses that person's privileges to create the service accounts. That's why turning on {{az-workers}} needs `manage_security`.

## {{serverless-short}} predefined roles [alertzero-privileges-predefined-roles]
```{applies_to}
serverless: preview
```

To give someone {{alertzero}} access without creating a custom role, assign one of these [{{serverless-short}} predefined roles](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table):

| Roles | {{alertzero}} privileges |
| --- | --- |
| Editor, SOC manager, Tier 3 analyst, Rule author, Detections admin, Platform engineer | **All** for **{{alertzero}}**, **Proposed Actions**, and **Agentic Investigations**, plus **Manage escalations** and **Update managed workflows** |
| Tier 1 analyst, Tier 2 analyst, Threat intelligence analyst, Endpoint operations analyst, Endpoint policy manager | **Read** for **{{alertzero}}** and **All** for **Proposed Actions** and **Agentic Investigations**, plus **Manage escalations** |
| Viewer | **Read** for **{{alertzero}}**, **Proposed Actions**, and **Agentic Investigations** |

None of these roles includes the `manage_security` cluster privilege, so none of them can edit {{az-worker}} settings or turn {{az-workers}} on or off.
