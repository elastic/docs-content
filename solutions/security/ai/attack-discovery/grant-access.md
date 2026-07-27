---
navigation_title: Grant feature access
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Grant access to Attack Discovery [attack-discovery-rbac]

To use Attack Discovery, your role needs specific privileges.

::::{applies-switch}

:::{applies-item} { "stack": "ga 9.4+", "serverless": "ga" }

Ensure your role has:

* Minimum [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for these **Security** features:

  - `All` for **Attack discovery**
  - At least `Read` for **Rules**
  - At least `Read` for **Alerts**

* The appropriate [index privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md#adding_index_privileges), based on what you want to do with Attack Discovery alerts:

| Action | Indices | {{es}} privileges |
|---------|---------|--------------------------|
| Read Attack Discovery alerts | - `.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.alerts-security.attack.discovery.alerts-<space-id>`<br> - `.adhoc.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.adhoc.alerts-security.attack.discovery.alerts-<space-id>`| `read` and `view_index_metadata` |
| Read and modify Attack Discovery alerts. This includes:<br>- Generating discovery alerts manually<br>- Generating discovery alerts using schedules<br>- Sharing manually created alerts with other users<br>- Updating a discovery's status |- `.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.adhoc.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.adhoc.alerts-security.attack.discovery.alerts-<space-id>`| `read`, `view_index_metadata`, `write`, and `maintenance`|

:::

:::{applies-item} { "stack": "ga 9.3"}

Ensure your role has:

* `All` [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for the **Security > Attack discovery** {{kib}} feature and at least `Read` privileges for the **Security > Rules, Alerts, and Exceptions** {{kib}} feature.

    ![attack-discovery-rules-rbac](/solutions/images/attack-discovery-rules-rbac.png "elasticsearch =60%x60%")

* The appropriate [index privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md#adding_index_privileges), based on what you want to do with Attack Discovery alerts:

| Action | Indices | {{es}} privileges |
|---------|---------|--------------------------|
| Read Attack Discovery alerts | - `.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.alerts-security.attack.discovery.alerts-<space-id>`<br> - `.adhoc.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.adhoc.alerts-security.attack.discovery.alerts-<space-id>`| `read` and `view_index_metadata` |
| Read and modify Attack Discovery alerts. This includes:<br>- Generating discovery alerts manually<br>- Generating discovery alerts using schedules<br>- Sharing manually created alerts with other users<br>- Updating a discovery's status |- `.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.adhoc.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.adhoc.alerts-security.attack.discovery.alerts-<space-id>`| `read`, `view_index_metadata`, `write`, and `maintenance`|

:::

:::{applies-item} stack: ga 9.1-9.2

Ensure your role has:

* `All` [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for the **Security > Attack discovery** {{kib}} feature and at least `Read` privileges for the **Security > Rules, Alerts, and Exceptions** {{kib}} feature.

    ![attack-discovery-rbac](/solutions/images/security-attck-disc-rbac.png "elasticsearch =60%x60%")

* The appropriate [index privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md#adding_index_privileges), based on what you want to do with Attack Discovery alerts:

| Action | Indices | {{es}} privileges |
|---------|---------|--------------------------|
| Read Attack Discovery alerts | - `.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.alerts-security.attack.discovery.alerts-<space-id>`<br> - `.adhoc.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.adhoc.alerts-security.attack.discovery.alerts-<space-id>`| `read` and `view_index_metadata` |
| Read and modify Attack Discovery alerts. This includes:<br>- Generating discovery alerts manually<br>- Generating discovery alerts using schedules<br>- Sharing manually created alerts with other users<br>- Updating a discovery's status |- `.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.adhoc.alerts-security.attack.discovery.alerts-<space-id>`<br>- `.internal.adhoc.alerts-security.attack.discovery.alerts-<space-id>`| `read`, `view_index_metadata`, `write`, and `maintenance`|

:::

:::{applies-item} stack: ga =9.0

Ensure your role has `All` [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for the **Security > Attack discovery** {{kib}} feature.

![attack-discovery-rbac](/solutions/images/security-attck-disc-rbac.png "elasticsearch =60%x60%")

:::

::::
