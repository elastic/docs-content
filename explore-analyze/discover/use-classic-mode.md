---
navigation_title: How to query in classic mode
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: overview
description: "Query your data in Discover's classic mode: select a data view, search with KQL or Lucene, filter results, and add runtime fields."
---

# How to query in Discover's classic mode

Classic mode in **Discover** works on a [data view](../find-and-organize/data-views.md), a definition of the data to query, usually saved, such as all your web logs. You search the data with [Kibana Query Language (KQL)](../query-filter/languages/kql.md) or [Lucene](../query-filter/languages/lucene-query-syntax.md), two search syntaxes, and narrow the results with filters.

## Set up and run a classic query

* [Select a data view and a time range](search-and-filter-classic.md#find-the-data-you-want-to-use) to select the data you explore.
* [Search with KQL or Lucene and narrow the results with filters](search-and-filter-classic.md).
* Add [runtime fields](add-fields-to-data-views.md) to your data views.
* [Switch to {{esql}} mode](switch-esql-mode.md) and see how Discover converts your search and filters into an {{esql}} query.

## Related pages

- [How Discover works](discover-get-started.md)
- [Explore your data in Discover](explore-data.md)
- [Manage your Discover view and sessions](manage-discover.md)
- [Data views](../find-and-organize/data-views.md)
