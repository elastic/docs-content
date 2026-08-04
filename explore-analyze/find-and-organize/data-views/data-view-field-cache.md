---
description: How Kibana caches a data view's field list in the browser, and how to force a refresh.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Data view field cache [data-view-field-cache]

The browser caches {{data-source}} field lists for increased performance. This is particularly impactful for {{data-sources}} with a high field count that span a large number of indices and clusters. The field list is updated every couple of minutes in typical {{kib}} usage. Alternatively, use the refresh button on the {{data-source}} management detail page to get an updated field list. A force reload of {{kib}} has the same effect.

The field list might be impacted by changes in indices and user permissions.

## Related pages

* [Data views](../data-views.md)
* [Customize data view fields](customize-data-view-fields.md)
