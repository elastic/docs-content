---
navigation_title: Use Discover with ES|QL
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: overview
description: Find the Discover tasks that are specific to ES|QL mode, from running a first query to reading results and building lookup indices.
---

# Use Discover with {{esql}}

In {{esql}} mode, you write a query in [{{esql}}](elasticsearch://reference/query-languages/esql.md), the {{es}} query language, and **Discover** shows the results. The query says which data to read, and it can also filter that data, calculate new fields, and summarize it. For example, `FROM kibana_sample_data_logs | WHERE bytes > 5000` returns the entries in the sample web logs that transferred more than 5,000 bytes. You don't need to set anything up first. Name an index or data stream in the query and run it.

If you'd rather pick a saved definition of your data, called a [data view](../find-and-organize/data-views.md), and search it with KQL or Lucene, two search syntaxes, use classic mode. Refer to [Use Discover in classic mode](use-classic-mode.md).

For the editor itself, time parameters, AI assistance, and Fast mode, refer to [](../query-filter/languages/esql-kibana.md). If you haven't run a query in this mode yet, start with [Get started with {{esql}} in Discover](try-esql.md).

## {{esql}} tasks in Discover

| When you need this | Guide |
| --- | --- |
| You haven't run an {{esql}} query in Discover yet | [Get started with {{esql}} in Discover](try-esql.md) |
| You want to switch between {{esql}} and classic mode, and need to know what happens to your query | [Switch between {{esql}} and classic mode](switch-esql-mode.md) |
| You're writing a query and need an index or a field name | [Browse data sources and fields from the {{esql}} editor in Discover](browse-esql-sources.md) |
| You have results and want to read them, sort them, or filter from a value | [Work with {{esql}} results in Discover](esql-results.md) |
| You want to change a value in the query without keeping several copies | [Add variable controls to Discover queries](esql-variable-controls.md) |
| You need enrichment data for a `LOOKUP JOIN` | [Create lookup indices from Discover queries](create-lookup-indices.md) |
| You grouped with `STATS BY` and want to look inside the groups | [Inspect grouped STATS results in Discover](inspect-grouped-stats.md) |
| You want to find a spike, dip, or shift in a time series | [Detect change points in Discover](detect-change-points.md) |
| You want an AI agent to analyze the data behind your query | [Analyze your data with AI in Discover](analyze-discover-data-with-ai.md) |
| You want to keep the chart, the table, or the session | [Save a Discover session for reuse](save-open-search.md) |

## Related pages

- [How Discover works](discover-get-started.md)
- [](../query-filter/languages/esql-kibana.md)
- [Lens visualizations using {{esql}} queries](../visualize/esorql.md)
