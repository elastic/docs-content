---
navigation_title: How to query in ES|QL mode
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: overview
description: Query your data in Discover with ES|QL, browse data sources and fields, add variable controls, and enrich results with lookup indices.
---

# How to query in Discover's {{esql}} mode

In {{esql}} mode, you write a query in [{{esql}}](elasticsearch://reference/query-languages/esql.md), the {{es}} query language, and **Discover** shows the results. The query says which data to read and can also filter, calculate, and summarize it. For example, `FROM kibana_sample_data_logs | WHERE bytes > 5000` returns the sample web log entries that transferred more than 5,000 bytes.

## Write and refine your queries

* Learn by running your [first {{esql}} query](try-esql.md) step by step on sample data.
* [Browse data sources and fields](browse-esql-sources.md) from the editor to find an index or a field name while you write a query.
* Use the [{{esql}} editor](../query-filter/languages/esql-kibana.md) to get suggestions as you type, error fixes, and, when an AI model is configured, AI-generated queries.
* Add [variable controls](esql-variable-controls.md) to make a query dynamic without having to duplicate it.
* Read, sort, and filter [{{esql}} results](esql-results.md) in the table.
* Create [lookup indices](create-lookup-indices.md) to enrich your results with `LOOKUP JOIN`.
* [Switch to classic mode](switch-esql-mode.md) and see what happens to your query.

## Related pages

- [How Discover works](discover-get-started.md)
- [Explore your data in Discover](explore-data.md)
- [Manage your Discover view and sessions](manage-discover.md)
- [Lens visualizations using {{esql}} queries](../visualize/esorql.md)
