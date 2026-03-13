---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: cloud-serverless
navigation_title: "Impacts and limitations"
---

# {{cps-cap}} impacts and limitations [cps-impacts-and-limitations]

This page explains how setting up {{cps}} affects features in the origin project, and lists overall limitations of {{cps}}.

## Feature impacts [cps-feature-impacts]

% TODO billing: {{cps-init}} generates network egress when the origin project queries linked projects. Data transfer fees may apply, especially for cross-region or cross-cloud-provider queries.
% TODO link to billing docs (D3B) when available. Exact billing SKU may still be TBD.

- **Alerting:** By default, alerting rules in the origin project run against the **combined dataset** of the origin and all linked projects. Alerting rules tuned for a single project's data might produce false positives when they evaluate a larger dataset. This is one reason we recommend using a dedicated [overview project](/deploy-manage/cross-project-search-config.md#cps-arch-overview), so that existing alerting rules on data projects are not affected.

% TODO link to alerting impacts doc when available

- **Dashboards and visualizations:** Existing dashboards and visualizations in the origin project will query all linked projects by default. To control this, set the [default {{cps}} scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope) for each space, or save explicit project routing on individual dashboard panels.

- **User permissions:** {{cps}} results are filtered by each user's role assignments across projects. Users with different roles will see different results from the same query. Refer to [Manage user access](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#manage-user-access).

## Limitations [cps-limitations]

::::{include} /deploy-manage/_snippets/cps-limitations-core.md
::::
