---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: cloud-serverless
navigation_title: "Impacts and limitations"
---

# {{cps-cap}} impacts and limitations [cps-impacts-and-limitations]

This page explains how setting up {{cps}} ({{cps-init}}) affects features in the origin project, and lists overall limitations of {{cps-init}}.

For more details about {{cps-init}} configuration, refer to [](/deploy-manage/cross-project-search-config.md). For information about _using_ {{cps-init}}, refer to [](/explore-analyze/cross-project-search.md).

## Feature impacts [cps-feature-impacts]

% TODO billing, subscriptions, licensing

- **Alerts:** By default, rules in the origin project run against the **combined dataset** of the origin and all linked projects. Rules tuned for a single project's data might produce false positives when they evaluate a larger dataset. This is one reason we recommend using a dedicated [overview project](/deploy-manage/cross-project-search-config.md#cps-arch-overview), so that existing rules on data projects are not affected. Make sure to also consider the [default {{cps}} scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope) for each space, or save explicit project routing on individual rules.

- **Dashboards and visualizations:** Existing dashboards and visualizations in the origin project will query all linked projects by default. To control this, set the [default {{cps}} scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope) for each space, or save explicit project routing on individual dashboard panels.

- **User permissions:** {{cps-cap}} results are filtered by each user's role assignments across projects. Users with different roles will see different results from the same query. Refer to [Manage user access](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#manage-user-access).

## Limitations [cps-limitations]

::::{include} /deploy-manage/_snippets/cps-limitations-core.md
::::
