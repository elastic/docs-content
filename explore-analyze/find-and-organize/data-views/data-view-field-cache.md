---
description: How Kibana caches a data view's field list in the browser, and how to refresh it with the Refresh control.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Data view field cache

The browser caches {{data-source}} field lists to improve performance. Caching matters most for {{data-sources}} with a high field count that span many indices and clusters.

In typical {{kib}} usage, the field list updates every few minutes. To get an updated list immediately, select **Refresh** on the {{data-source}} management detail page. Reloading {{kib}} has the same effect.

The field list might change after updates to indices or user permissions.

## Related pages

* [Data views](../data-views.md)
* [Customize data view fields](customize-data-view-fields.md)
