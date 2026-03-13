---
applies_to:
  serverless: preview
  stack: unavailable
products:
  - id: security
description: Learn how detection rules work with cross-project search to query data across linked projects.
---

# {{cps-cap}} and detection rules [rules-cross-project-search]

When [{{cps}}](/explore-analyze/cross-project-search.md) is enabled and you have [linked projects](/explore-analyze/cross-project-search/cross-project-search-link-projects.md), detection rules query data across linked projects based on the **space-level {{cps}} scope**. You cannot set a {{cps}} scope on individual rules.

When you open a rule to create or edit it, the [{{cps-init}} scope selector](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-in-kibana) in the header shows the current {{cps}} scope but is read-only. To change which projects rules query, update the [{{cps}} scope configured for the space](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope).

For {{esql}} rules, you can use [`SET project_routing`](/explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-cps) in the rule query to target specific linked projects, overriding the space-level scope.

:::{note}
{{ml}} rules don't support {{cps}}. {{ml}} rules search data in the origin project only.
:::
