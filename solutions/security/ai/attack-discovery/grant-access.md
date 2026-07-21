---
navigation_title: Grant feature access
description: "Required Kibana, index, and workflow privileges for Attack Discovery by version."
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Grant access to Attack Discovery [attack-discovery-rbac]

Attack Discovery requires specific {{kib}} feature privileges and, in most versions, index privileges on Attack Discovery alert indices. Some capabilities also require Workflows and {{agent-builder}} access.

After you grant the right access, [choose how to run Attack Discovery](/solutions/security/ai/attack-discovery/run-attack-discovery.md).

## Kibana feature privileges [ad-kibana-privileges]

Your role needs these [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for the **Security** features in your version:

| Available in | Privileges |
|---|---|
| {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` | `All` for **Attack discovery**, and at least `Read` for **Rules** and **Alerts** |
| {applies_to}`stack: ga 9.1-9.3` | `All` for **Security > Attack discovery**, and at least `Read` for **Security > Rules, Alerts, and Exceptions** |
| {applies_to}`stack: ga =9.0` | `All` for **Security > Attack discovery** |

## Index privileges [ad-index-privileges]

{applies_to}`stack: ga 9.1+` {applies_to}`serverless: ga` Your role needs the appropriate [index privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md#adding_index_privileges) based on what it must do with Attack Discovery alerts. Replace `<space-id>` with the {{kib}} space ID.

### Read Attack Discovery alerts

Your role needs the {{es}} privileges `read` and `view_index_metadata` on these indices:

* `.alerts-security.attack.discovery.alerts-<space-id>`
* `.internal.alerts-security.attack.discovery.alerts-<space-id>`
* `.adhoc.alerts-security.attack.discovery.alerts-<space-id>`
* `.internal.adhoc.alerts-security.attack.discovery.alerts-<space-id>`

### Read and modify Attack Discovery alerts

Your role needs the {{es}} privileges `read`, `view_index_metadata`, `write`, and `maintenance` on these indices to generate discoveries manually or with schedules, share manually created alerts with other users, and update a discovery's status:

* `.alerts-security.attack.discovery.alerts-<space-id>`
* `.internal.alerts-security.attack.discovery.alerts-<space-id>`
* `.adhoc.alerts-security.attack.discovery.alerts-<space-id>`
* `.internal.adhoc.alerts-security.attack.discovery.alerts-<space-id>`

## Workflow and Agent Builder privileges [attack-discovery-workflows-privileges]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

When you turn on the [**Attack Discovery Workflows**](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) advanced setting, your role may also need these privileges based on what it must do:

### Build, view, or run Attack Discovery workflows

Your role needs `All` or `Read` for **Analytics > Workflows**, depending on the action. Having `All` for Attack Discovery is not enough.

Serverless roles include Workflows access by default. On self-managed and Elastic Cloud Hosted deployments, you must add Workflows access to custom roles. Refer to [Set up Workflows](/explore-analyze/workflows/get-started/setup.md).

### Run Attack Discovery from Agent Builder

Your role needs {{agent-builder}} in addition to Attack Discovery access to run Attack Discovery from {{agent-builder}}, or to use AI troubleshooting and AI-assisted query editing. Refer to [Run Attack Discovery from {{agent-builder}}](/solutions/security/ai/attack-discovery/run-attack-discovery-from-agent-builder.md).

### Edit built-in Attack Discovery workflows

<!-- FLAG: Confirm the exact privilege name for editing built-in Attack Discovery workflows. -->

Your role needs a separate privilege beyond base Workflows access to edit built-in workflows. Most roles can only view built-in workflows. No role can delete them. Refer to [Built-in workflows](/solutions/security/ai/attack-discovery/run-attack-discovery-in-a-workflow.md#run-ad-workflow-built-in).
