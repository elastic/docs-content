---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/grant-cases-access.html
---

# Configure access to cases [grant-cases-access]

To access and send cases to external systems, you need the [appropriate license](https://www.elastic.co/subscriptions), and your role must have the **Cases** {{kib}} privilege as a user for the **{{observability}}** feature.

::::{note}
If you are using an on-premises {{kib}} deployment and want your email notifications and external incident management systems to contain links back to {{kib}}, configure the [server.publicBaseUrl](../../../deploy-manage/deploy/self-managed/configure.md#server-publicBaseUrl) setting.
::::


For more details, refer to [feature access based on user privileges](../../../deploy-manage/manage-spaces.md#spaces-control-user-access).

:::{image} ../../../images/observability-cases-privileges.png
:alt: cases privileges
:screenshot:
:::

Below are the minimum required privileges for some common use cases.


## Give full access to manage cases and settings [_give_full_access_to_manage_cases_and_settings]

* `All` for the **Cases** feature under **{{observability}}**.
* `All` for the **{{connectors-feature}}** feature under **Management**.

    ::::{note}
    Roles without `All` **{{connectors-feature}}** feature privileges cannot create, add, delete, or modify case connectors.

    By default, `All` for the **Cases** feature includes authority to delete cases, delete alerts and comments from cases, edit case settings, add case comments and attachments, and re-open cases unless you customize the sub-feature privileges.

    ::::



## Give assignee access to cases [_give_assignee_access_to_cases]

* `All` for the **Cases** feature under **{{observability}}**.

    ::::{note}
    Before a user can be assigned to a case, they must log into {{kib}} at least once, which creates a user profile.
    ::::



## Give view-only access for cases [_give_view_only_access_for_cases]

* `Read` for the **Cases** feature under **{{observability}}**.

    ::::{note}
    You can customize sub-feature privileges for deleting cases, deleting alerts and comments from cases, editing case settings, adding case comments and attachements, and re-opening cases.
    ::::



## Give access to add alerts to cases [_give_access_to_add_alerts_to_cases]

* `All` for the **Cases** feature under **{{observability}}**.
* `Read` for an **{{observability}}** feature that has alerts.


## Revoke all access to cases [_revoke_all_access_to_cases]

* `None` for the **Cases** feature under **{{observability}}**.

