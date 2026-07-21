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

Attack Discovery requires specific {{kib}} feature privileges and, in most versions, index privileges on Attack Discovery alert indices. Additional Workflows and {{agent-builder}} access is required for some 9.5 capabilities.

Use this page to grant the right access for your version:

* [Kibana feature privileges](#attack-discovery-kibana-privileges)
* [Index privileges](#attack-discovery-index-privileges)
* [Workflow and Agent Builder privileges](#attack-discovery-workflows-privileges)

## Kibana feature privileges [attack-discovery-kibana-privileges]

Grant these [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for the **Security** features in your version:

| Available in | Privileges |
|---|---|
| {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` | `All` for **Attack discovery**, and at least `Read` for **Rules** and **Alerts** |
| {applies_to}`stack: ga 9.1-9.3` | `All` for **Security > Attack discovery**, and at least `Read` for **Security > Rules, Alerts, and Exceptions** |
| {applies_to}`stack: ga =9.0` | `All` for **Security > Attack discovery** |

## Index privileges [attack-discovery-index-privileges]

```{applies_to}
stack: ga 9.1+
serverless: ga
```

Grant the appropriate [index privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md#adding_index_privileges) based on what users need to do with Attack Discovery alerts. Replace `<space-id>` with the {{kib}} space ID.

| Action | Indices | {{es}} privileges |
|---------|---------|--------------------------|
| Read Attack Discovery alerts | - `.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.adhoc.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.adhoc.alerts-security.attack.discovery.alerts-<space-id>` | `read` and `view_index_metadata` |
| Read and modify Attack Discovery alerts, including:<br>- Generating discoveries manually<br>- Generating discoveries using schedules<br>- Sharing manually created alerts with other users<br>- Updating a discovery's status | - `.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.adhoc.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.adhoc.alerts-security.attack.discovery.alerts-<space-id>` | `read`, `view_index_metadata`, `write`, and `maintenance` |

## Workflow and Agent Builder privileges [attack-discovery-workflows-privileges]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

When [`securitySolution:enableAttackDiscoveryWorkflows`](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) is turned on, some Attack Discovery capabilities also require Workflows access, and {{agent-builder}} for conversational runs and AI troubleshooting:

| Capability | Privileges |
|---|---|
| Build, view, or run workflows that call Attack Discovery | `All` or `Read` for **Analytics > Workflows**, depending on the action. This privilege is separate from Attack Discovery access. The Attack Discovery `All` privilege alone does not include it. Serverless roles already grant Workflows access by default. On self-managed and Elastic Cloud Hosted deployments, add it explicitly to custom roles. Refer to [Set up Workflows](/explore-analyze/workflows/get-started/setup.md). |
| Run Attack Discovery from {{agent-builder}}, or use AI troubleshooting and AI-assisted query editing | {{agent-builder}} in addition to Attack Discovery access. Refer to [Run Attack Discovery from {{agent-builder}}](/solutions/security/ai/attack-discovery/run-attack-discovery-from-agent-builder.md). |
| Edit Elastic's built-in Attack Discovery workflows | A separate privilege beyond base Workflows access. Built-in workflows are read-only for most users. Deletion is always blocked. Refer to [Built-in workflows](/solutions/security/ai/attack-discovery/run-attack-discovery-in-a-workflow.md#run-ad-workflow-built-in). |

<!-- FLAG: Confirm the exact privilege name for editing built-in Attack Discovery workflows. -->
