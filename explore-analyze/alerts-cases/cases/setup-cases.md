---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/setup-cases.html
---

# Configure access to cases [setup-cases]

To access cases in **{{stack-manage-app}}**, you must have the appropriate {{kib}} privileges:

## Give full access to manage cases and settings [_give_full_access_to_manage_cases_and_settings]

**{{kib}} privileges**

* `All` for the **Cases** feature under **Management**.
* `All` for the **{{connectors-feature}}** feature under **Management**.

::::{note}
The **{{connectors-feature}}** feature privilege is required to create, add, delete, and modify case connectors and to send updates to external systems.

By default, `All` for the **Cases** feature includes authority to delete cases and comments, edit case settings, add case comments and attachments, and re-open cases unless you customize the sub-feature privileges.

::::

## Give assignee access to cases [_give_assignee_access_to_cases]

**{{kib}} privileges**

* `All` for the **Cases** feature under **Management**.

::::{note}
Before a user can be assigned to a case, they must log into {{kib}} at least once, which creates a user profile.

This privilege is also required to add [case actions](https://www.elastic.co/guide/en/kibana/current/cases-action-type.html) to rules.

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
If you are using an on-premises {{kib}} deployment and you want the email notifications and the external incident management systems to contain links back to {{kib}}, you must configure the [`server.publicBaseUrl`](../../../deploy-manage/deploy/self-managed/configure.md#server-publicBaseUrl) setting.
::::
