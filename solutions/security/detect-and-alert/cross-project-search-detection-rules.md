---
applies_to:
  serverless: preview
  stack: unavailable
products:
  - id: security
description: Learn how detection rules work with cross-project search to query data across linked projects.
---

# {{cps-cap}} and detection rules [rules-cross-project-search]

When [{{cps}}](/explore-analyze/cross-project-search.md) is enabled and you have [linked projects](/explore-analyze/cross-project-search/cross-project-search-link-projects.md), detection rules query data across linked projects based on the **space-level {{cps}} scope**. You cannot set a {{cps}} scope on individual rules. However, you can define [project routing](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) directly in a rule query to target specific linked projects.

:::{note}
{{anomaly-detect-cap}} rules don't support {{cps}}.
:::
