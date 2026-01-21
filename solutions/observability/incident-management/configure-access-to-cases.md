---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/grant-cases-access.html
products:
  - id: observability
navigation_title: Configure access to cases
---

# Configure access to cases in Elastic {{observability}} [grant-cases-access]

To access and send cases to external systems, you need the [appropriate license](https://www.elastic.co/subscriptions), and your role must have the **Cases** {{kib}} privilege as a user for the **{{observability}}** feature.

::::{note}
If you are using an on-premises {{kib}} deployment and want your email notifications and external incident management systems to contain links back to {{kib}}, configure the [server.publicBaseUrl](kibana://reference/configuration-reference/general-settings.md#server-publicbaseurl) setting.
::::


For more details, refer to [feature access based on user privileges](/deploy-manage/manage-spaces.md#spaces-control-user-access).

:::{image} /solutions/images/observability-cases-privileges.png
:alt: cases privileges
:screenshot:
:::

Below are the minimum required privileges for some common use cases.


## Give full access to manage cases and settings [_give_full_access_to_manage_cases_and_settings]

* `All` for the **Cases** feature under **{{observability}}**.
* `All` for the **{{connectors-feature}}** feature under **Management**.

    ::::{note}
    Roles without `All` **{{connectors-feature}}** feature privileges cannot create, add, delete, or modify case connectors.

    By default, `All` for the **Cases** feature allows you to have full control over cases, including deleting them, editing case settings, and more. You can customize the sub-feature privileges to limit feature access.

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

