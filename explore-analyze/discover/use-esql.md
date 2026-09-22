---
navigation_title: Use Discover with ES|QL
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: overview
description: Find the Discover tasks that are specific to ES|QL mode, from a first query to reading results and building lookup indices.
---

# Use Discover with ES|QL

{{esql}} mode in **Discover** lets you explore data with an {{esql}} query. The query chooses the data, so you do not need a data view. Classic mode uses data views with Kibana Query Language (KQL) or Lucene.

The editor itself, time parameters, AI assistance, and Fast mode are covered in [Use {{esql}} in the {{kib}} UI](../query-filter/languages/esql-kibana.md). If you have not run a query in this mode yet, start with [Get started with {{esql}} in Discover](try-esql.md).

## ES|QL tasks in Discover

| When you need this | Guide |
| --- | --- |
| You have not run an {{esql}} query in Discover yet | [Get started with {{esql}} in Discover](try-esql.md) |
| You want to query in {{esql}}, or go back to KQL, and you need to know what happens to the query | [Switch between {{esql}} and classic mode](switch-esql-mode.md) |
| You are writing a query and need an index or a field name | [Browse data sources and fields from the editor](browse-esql-sources.md) |
| You have results and want to read them, sort them, or filter from a value | [Work with {{esql}} results in Discover](esql-results.md) |
| You want to change a value in the query without keeping several copies | [Add variable controls to Discover queries](esql-variable-controls.md) |
| You need enrichment data for a `LOOKUP JOIN` | [Create lookup indices from Discover queries](create-lookup-indices.md) |
| You grouped with `STATS BY` and want to look inside the groups | [Inspect grouped STATS results in Discover](inspect-grouped-stats.md) |
| You want to keep the chart, the table, or the session | [Save a Discover session for reuse](save-open-search.md) |

## Related pages

- [Explore fields and data with Discover](discover-get-started.md)
- [Use {{esql}} in the {{kib}} UI](../query-filter/languages/esql-kibana.md)
- [Lens visualizations using {{esql}} queries](../visualize/esorql.md)
