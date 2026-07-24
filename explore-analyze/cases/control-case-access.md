---
navigation_title: Control access
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/setup-cases.html
  - https://www.elastic.co/guide/en/security/current/case-permissions.html
  - https://www.elastic.co/guide/en/observability/current/grant-cases-access.html
  - https://www.elastic.co/guide/en/serverless/current/security-cases-requirements.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: cloud-serverless
description: Create custom roles and configure Kibana feature privileges to control access to cases.
---

# Control access to cases [setup-cases]

To manage cases, users need the appropriate {{kib}} feature privileges. You can grant different levels of access depending on what users need to do, from full control over cases to view-only access.

## Quick reference [cases-quick-reference]

The following table shows the minimum privileges required for each activity. Higher privilege levels include the access shown here. Set **Cases** privileges under your solution (**{{stack-manage-app}}**, **Security**, or **{{observability}}**). Refer to the following sections for the full breakdown.

| To... | Minimum required |
|---|---|
| View cases | **Cases: Read** |
| Create and manage cases | **Cases: All** |
| Be assigned to cases | **Cases: All** (user must also log in at least once) |
| Manage connectors and push cases externally | **Cases: All** + **{{connectors-feature}}: All** (under **Management**) |
| Manage case templates and the field library {applies_to}`stack: ga 9.5` {applies_to}`serverless: ga` | **Cases: All** + **Manage templates** sub-feature privilege |
| Add alerts to cases | **Cases: All** + alert privileges for your solution (see [Give access to add alerts to cases](#give-alerts-access)) |

## Create custom roles for cases [create-custom-roles]

::::{applies-switch}

:::{applies-item} stack: ga

[Create or update a role](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md), then set **Cases** privileges under your solution (**{{stack-manage-app}}**, **Security**, or **{{observability}}**). To grant individual privileges, turn on **Customize sub-feature privileges**. For details about feature and sub-feature privileges, refer to [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

:::

:::{applies-item} serverless: ga

[Create a custom role](/deploy-manage/users-roles/serverless-custom-roles.md), then set **Cases** privileges under your solution (**Security** or **{{observability}}**). To grant individual privileges, turn on **Customize sub-feature privileges**.

:::

::::

## Customize sub-feature privileges for cases [cases-sub-feature-privileges]

When **Customize sub-feature privileges** is on for **Cases**, you can grant these privileges individually:

| Privilege | Description |
| --- | --- |
| **Delete** | Delete cases and comments. |
| **Case settings** | Edit case settings. |
| **Create comments & attachments** | Add comments to cases. |
| **Re-open** | Re-open closed cases. |
| **Assign users** | Assign users to cases. |
| **Manage templates** {applies_to}`stack: ga 9.5` {applies_to}`serverless: ga` | Manage case templates. |

## Give full access to manage cases and settings [give-full-access]

::::{applies-switch}

:::{applies-item} stack: ga

* `All` for the **Cases** feature under the appropriate solution (**{{stack-manage-app}}**, **Security**, or **{{observability}}**). This grants full control over cases, including creating, deleting, and editing case settings. You can turn on **Customize sub-feature privileges** to limit access.
* `All` for the **{{connectors-feature}}** feature under **Management**. This is required to create, add, delete, and modify connectors that push cases to external systems.

:::

:::{applies-item} serverless: ga

* `All` for the **Cases** feature under the appropriate solution (**Security** or **{{observability}}**).
* `All` for the **{{connectors-feature}}** feature under **Management**. This is required to create, add, delete, and modify case connectors and send updates to external systems.
:::

::::

## Give assignee access to cases [give-assignee-access]

::::{applies-switch}

:::{applies-item} stack: ga

`All` for the **Cases** feature under the appropriate solution (**{{stack-manage-app}}**, **Security**, or **{{observability}}**).

Users must log in to their deployment at least once before they can be assigned to cases. Logging in creates the required user profile.

:::

:::{applies-item} serverless: ga

`All` for the **Cases** feature under the appropriate solution (**Security** or **{{observability}}**).

Users must log in to their deployment at least once before they can be assigned to cases. Logging in creates the required user profile.
:::

::::

## Give view-only access to cases [give-view-access]


::::{applies-switch}

:::{applies-item} stack: ga

`Read` for the **Cases** feature under the appropriate solution (**{{stack-manage-app}}**, **Security**, or **{{observability}}**). 

:::

:::{applies-item} serverless: ga
`Read` for the **Cases** feature under the appropriate solution (**Security** or **{{observability}}**).
:::

::::

## Give access to manage case templates [give-manage-templates-access]

```{applies_to}
stack: ga 9.5
serverless: ga
```

To create, edit, delete, import, and export [case templates](create-case-templates.md) and [field library entries](create-case-field-library.md), grant the following privileges. Users without **Manage templates** can still select and apply enabled templates when creating or updating a case.

::::{applies-switch}

:::{applies-item} stack: ga

1. Set `All` for the **Cases** feature under the appropriate solution (**{{stack-manage-app}}**, **Security**, or **{{observability}}**).
2. Turn on **Customize sub-feature privileges**.
3. Enable **Manage templates**.

:::

:::{applies-item} serverless: ga

1. Set `All` for the **Cases** feature under the appropriate solution (**Security** or **{{observability}}**).
2. Turn on **Customize sub-feature privileges**.
3. Enable **Manage templates**.

:::

::::

## Give access to add alerts to cases [give-alerts-access] 

::::{applies-switch} 

:::{applies-item} { stack: ga 9.4+, serverless: ga }

* `All` for the **Cases** feature under the appropriate solution (**Security** or **{{observability}}**).
* To work with alerts in cases:
  - **Security**: `Read` or `All` for the **Security > Alerts** feature. For what each level allows, refer to [Detections privileges](/solutions/security/detect-and-alert/detections-privileges.md#manage-alerts).
  - **{{observability}}**: `Read` for **{{observability}}** 

:::

:::{applies-item} stack: ga 9.0-9.3

* `All` for the **Cases** feature under the appropriate solution (**Security** or **{{observability}}**).
* `Read` for a solution that has alerts (for example, **{{observability}}** or **Security**).

:::

::::


## Revoke all access to cases [revoke-access]

::::{applies-switch}

:::{applies-item} stack: ga

`None` for the **Cases** feature under the appropriate solution (**{{stack-manage-app}}**, **Security**, or **{{observability}}**). 

:::

:::{applies-item} serverless: ga
`None` for the **Cases** feature under the appropriate solution (**Security** or **{{observability}}**).

:::

::::
