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
---

# Control access to cases [setup-cases]

To manage cases, users need the appropriate {{kib}} feature privileges. You can grant different levels of access depending on what users need to do, from full control over cases to view-only access.

## Create custom roles for cases [create-custom-roles]

To grant users the appropriate case privileges, create a custom role with the required {{kib}} feature privileges.

::::{applies-switch}

:::{applies-item} stack: ga
1. Go to the **Roles** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Create role**.
3. Enter a role name and (optional) description.
4. Under **{{kib}} privileges**, click **Add {{kib}} privilege**.
5. Select the appropriate spaces or **All Spaces** and expand the feature privileges for **Cases** under your solution (**Management**, **Security**, or **{{observability}}**).
6. Set the privilege level (`All`, `Read`, or `None`) and customize sub-feature privileges as needed.
7. Click **Create role**.
:::

:::{applies-item} serverless: ga
1. Go to the **Custom Roles** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Create role**.
3. Enter a role name and (optional) description.
4. Select the appropriate spaces or **All Spaces** and expand the feature privileges for **Cases** under your solution (**Security** or **{{observability}}**).
5. Set the privilege level (`All`, `Read`, or `None`) and customize sub-feature privileges as needed.
6. Click **Create role**.
:::

::::

## Give full access to manage cases and settings [give-full-access]

::::{applies-switch}

:::{applies-item} stack: ga

* `All` for the **Cases** feature under the appropriate solution (**Management**, **Security**, or **{{observability}}**). This grants full control over cases, including creating, deleting, and editing case settings. You can customize sub-feature privileges to limit access.
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

`All` for the **Cases** feature under the appropriate solution (**Management**, **Security**, or **{{observability}}**).

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

`Read` for the **Cases** feature under the appropriate solution (**Management**, **Security**, or **{{observability}}**). 

:::

:::{applies-item} serverless: ga
`Read` for the **Cases** feature under the appropriate solution (**Security** or **{{observability}}**).
:::

::::

## Give access to add alerts to cases [give-alerts-access] 

::::{applies-switch} 

:::{applies-item} stack: ga

* `All` for the **Cases** feature under the appropriate solution (**Management**, **Security**, or **{{observability}}**). 
* `Read` for a solution that has alerts (for example, **{{observability}}** or **Security**).

:::

:::{applies-item} serverless: ga

* `All` for the **Cases** feature under the appropriate solution (**Security** or **{{observability}}**).
* `Read` for a solution that has alerts (for example, **{{observability}}** or **Security**).

:::

::::


## Revoke all access to cases [revoke-access]

::::{applies-switch}

:::{applies-item} stack: ga

`None` for the **Cases** feature under the appropriate solution (**Management**, **Security**, or **{{observability}}**). 

:::

:::{applies-item} serverless: ga
`None` for the **Cases** feature under the appropriate solution (**Security** or **{{observability}}**).

:::

::::
