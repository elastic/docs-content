---
navigation_title: Configure access
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

# Configure access to cases [setup-cases]

To manage cases, users need the appropriate {{kib}} feature privileges. You can grant different levels of access depending on what users need to do, from full control over cases to view-only access.

## Give full access to manage cases and settings [give-full-access]

::::{applies-switch}

:::{applies-item} stack: ga
{{kib}} privileges

* `All` for the **Cases** feature under the appropriate solution (**Management**, **Security**, or **{{observability}}**).
* `All` for the **{{connectors-feature}}** feature under **Management**.

The **{{connectors-feature}}** feature privilege is required to create, add, delete, and modify case connectors and to send updates to external systems.

By default, `All` for the **Cases** feature allows you to have full control over cases, including deleting them, editing case settings, and more. You can customize the sub-feature privileges to limit feature access.

:::

:::{applies-item} serverless: ga
{{kib}} privileges

* `All` for the **Cases** feature under the appropriate solution (**Security** or **{{observability}}**).
* `All` for the **{{connectors-feature}}** feature under **Management**.

Roles without `All` **{{connectors-feature}}** feature privileges cannot create, add, delete, or modify case connectors.
:::

::::

## Give assignee access to cases [give-assignee-access]

::::{applies-switch}

:::{applies-item} stack: ga

{{kib}} privileges
* `All` for the **Cases** feature under the appropriate solution.

Before a user can be assigned to a case, they must log into {{kib}} at least once, which creates a user profile.

This privilege is also required to add [case actions](kibana://reference/connectors-kibana/cases-action-type.md) to rules.

:::

:::{applies-item} serverless: ga
* `All` for the **Cases** feature under the appropriate solution.

Before a user can be assigned to a case, they must log in at least once, which creates a user profile.
:::

::::

## Give view-only access to cases [give-view-access]


::::{applies-switch}

:::{applies-item} stack: ga

{{kib}} privileges

* `Read` for the **Cases** feature under the appropriate solution.


You can customize sub-feature privileges for deleting cases and comments, editing case settings, adding case comments and attachments, and re-opening cases.

:::

:::{applies-item} serverless: ga
* `Read` for the **Cases** feature under the appropriate solution.

You can customize sub-feature privileges for deleting cases, deleting alerts and comments from cases, editing case settings, adding case comments and attachments, and re-opening cases.
:::

::::

## Give access to add alerts to cases [give-alerts-access]

{applies_to}`serverless:` {applies_to}`stack:`

**{{kib}} privileges**

* `All` for the **Cases** feature under the appropriate solution.
* `Read` for a feature that has alerts (for example, **{{observability}}** or **Security**).

## Revoke all access to cases [revoke-access]

**{{kib}} privileges**

* `None` for the **Cases** feature under the appropriate solution.
