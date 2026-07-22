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

Attack Discovery requires specific {{kib}} feature privileges and, in most versions, index privileges on Attack Discovery alert indices. Some capabilities also require Workflows privileges.

After you grant the right access, [choose how to run Attack Discovery](/solutions/security/ai/attack-discovery/run-attack-discovery.md).

## {{kib}} feature privileges [ad-kibana-privileges]

Your role needs these [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md#adding_kibana_privileges) for the **Security** features in your version:

| Available in | Privileges |
|---|---|
| {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` | `All` for **Attack discovery**, and at least `Read` for **Rules and Exceptions** and **Alerts** |
| {applies_to}`stack: ga 9.1-9.3` | `All` for **Security > Attack discovery**, and at least `Read` for **Security > Rules, Alerts, and Exceptions** |
| {applies_to}`stack: ga =9.0` | `All` for **Security > Attack discovery** |

## Index privileges [ad-index-privileges]

```{applies_to}
stack: ga 9.1+
serverless:
  security: ga
```

Your role needs the appropriate [index privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md#adding_index_privileges) based on what it must do with Attack Discovery alerts. Replace `<space-id>` with the {{kib}} space ID.

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

## Grant Workflows privileges for Attack Discovery [attack-discovery-workflows-privileges]

```{applies_to}
stack: ga 9.5+
serverless:
  security: ga
```

When you turn on [**Attack Discovery Workflows**](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows), your role needs access to **Analytics > Workflows**. {{serverless-short}} roles include that access by default. On self-managed and {{ech}} deployments, add it to custom roles. For the privilege level each action needs, refer to [Manage access to workflows](/explore-analyze/workflows/get-started/setup.md#workflows-role-access).