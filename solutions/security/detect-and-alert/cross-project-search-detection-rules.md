---
applies_to:
  serverless: preview
  stack: unavailable
products:
  - id: security
description: Learn how detection rules work with cross-project search to query data across linked projects.
---

# {{cps-cap}} and detection rules [rules-cross-project-search]

When [{{cps}}](/explore-analyze/cross-project-search.md) is enabled and you have [linked projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md), detection rules query data across linked projects based on the **space-level {{cps}} scope**. You cannot set a {{cps}} scope on individual rules.

When you open a rule to create or edit it, the [{{cps-init}} scope selector](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-search-scope) in the header shows the current {{cps}} scope but is read-only. To change which projects rules query, update the [{{cps}} scope configured for the space](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope).

For {{esql}} rules, you can use [`SET project_routing`](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) in the rule query to target specific linked projects, overriding the space-level scope. For non-{{esql}} rules that use index patterns, you can use [qualified index expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions) to scope the rule to specific projects.

:::{note}
{{ml-cap}} rules don't support {{cps}}; they search data in the origin project only. Other {{elastic-sec}} features also have limited or no {{cps}} support. For details, refer to [{{cps-cap}} availability by app](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-availability).
:::
