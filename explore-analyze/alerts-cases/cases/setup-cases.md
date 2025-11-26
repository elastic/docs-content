---
navigation_title: Configure access to cases
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/setup-cases.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Instructions for configuring user privileges and access permissions for case management.
---

# Configure access to cases [setup-cases]

To access and manage cases in **{{stack-manage-app}}**, users must have the appropriate {{kib}} feature privileges. You can grant full access to manage cases and settings, assignee access to work on cases, or read-only access to view cases.

## Give full access to manage cases and settings [_give_full_access_to_manage_cases_and_settings]

**{{kib}} privileges**

* `All` for the **Cases** feature under **Management**.
* `All` for the **{{connectors-feature}}** feature under **Management**.

::::{note}
The **{{connectors-feature}}** feature privilege is required to create, add, delete, and modify case connectors and to send updates to external systems.

By default, `All` for the **Cases** feature allows you to have full control over cases, including deleting them, editing case settings, and more. You can customize the sub-feature privileges to limit feature access.

::::

## Give assignee access to cases [_give_assignee_access_to_cases]

**{{kib}} privileges**

* `All` for the **Cases** feature under **Management**.

::::{note}
Before a user can be assigned to a case, they must log into {{kib}} at least once, which creates a user profile.

This privilege is also required to add [case actions](kibana://reference/connectors-kibana/cases-action-type.md) to rules.

::::

## Give view-only access to cases [_give_view_only_access_to_cases]

**{{kib}} privileges**

* `Read` for the **Cases** feature under **Management**.

::::{note}
You can customize sub-feature privileges for deleting cases and comments, editing case settings, adding case comments and attachments, and re-opening cases.
::::

## Revoke all access to cases [_revoke_all_access_to_cases]

**{{kib}} privileges**

`None` for the **Cases** feature under **Management**.

## More details [_more_details_2]

For more details, refer to [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

::::{note}
If you are using an on-premises {{kib}} deployment and you want the email notifications and the external incident management systems to contain links back to {{kib}}, you must configure the [`server.publicBaseUrl`](kibana://reference/configuration-reference/general-settings.md#server-publicbaseurl) setting.
::::
