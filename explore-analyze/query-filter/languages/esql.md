---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-getting-started.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-using.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-examples.html
  - https://www.elastic.co/guide/en/kibana/current/esql.html
---

# ES|QL [esql]

## What's {{esql}}? [_the_esql_compute_engine]

**Elasticsearch Query Language ({{esql}})** is a piped query language for filtering, transforming, and analyzing data.

You can author {{esql}} queries to find specific events, perform statistical analysis, and generate visualizations. It supports a wide range of [commands, functions and operators](elasticsearch://reference/query-languages/esql/esql-functions-operators.md) to perform various data operations, such as filtering, aggregation, time-series analysis, and more. Today, it supports a subset of the features available in Query DSL, but it is rapidly evolving.

::::{note}
**{{esql}}'s compute architecture**

{{esql}} is built on top of a new compute architecture within {{es}}, designed to achieve high functional and performance requirements for {{esql}}. {{esql}} search, aggregation, and transformation functions are directly executed within Elasticsearch itself. Query expressions are not transpiled to Query DSL for execution. This approach allows {{esql}} to be extremely performant and versatile.

The new {{esql}} execution engine was designed with performance in mind — it operates on blocks at a time instead of per row, targets vectorization and cache locality, and embraces specialization and multi-threading. It is a separate component from the existing Elasticsearch aggregation framework with different performance characteristics.
::::

## How does it work? [search-analyze-data-esql]

The {{es}} Query Language ({{esql}}) makes use of "pipes" (|) to manipulate and transform data in a step-by-step fashion. This approach allows you to compose a series of operations, where the output of one operation becomes the input for the next, enabling complex data transformations and analysis.

You can use it:
- In your queries to {{es}} APIs, using the [`_query` endpoint](/explore-analyze/query-filter/languages/esql-rest.md) that accepts queries written in {{esql}} syntax.
- Within various {{kib}} tools such as Discover and Dashboards, to explore your data and build powerful visualizations.

Learn more about using {{esql}} for Search use cases in this tutorial: [Search and filter with {{esql}}](/solutions/search/esql-search-tutorial.md).

## Next steps

Find more details about {{esql}} in the following documentation pages:
- [{{esql}} reference](elasticsearch://reference/query-languages/esql.md):
  - Reference documentation for the [{{esql}} syntax](elasticsearch://reference/query-languages/esql/esql-syntax.md):
    - Reference for [commands](elasticsearch://reference/query-languages/esql/esql-commands.md), and [functions and operators](elasticsearch://reference/query-languages/esql/esql-functions-operators.md)
    - How to work with [metadata fields](elasticsearch://reference/query-languages/esql/esql-metadata-fields.md) and [multivalued fields](elasticsearch://reference/query-languages/esql/esql-multivalued-fields.md)
    - How to work with [DISSECT and GROK](elasticsearch://reference/query-languages/esql/esql-process-data-with-dissect-grok.md), [ENRICH](elasticsearch://reference/query-languages/esql/esql-enrich-data.md), and [LOOKUP join](elasticsearch://reference/query-languages/esql/esql-lookup-join.md)


- Using {{esql}}:
  - An overview of using the [`_query` API endpoint](/explore-analyze/query-filter/languages/esql-rest.md).
  - [Using {{esql}} for search](/solutions/search/esql-for-search.md).
  - [Using {{esql}} in {{kib}}](../../../explore-analyze/query-filter/languages/esql-kibana.md).
  - [Using {{esql}} in {{elastic-sec}}](/explore-analyze/query-filter/languages/esql-elastic-security.md).
  - [Using {{esql}} with multiple indices](/explore-analyze/query-filter/languages/esql-multi-index.md).
  - [Using {{esql}} across clusters](/explore-analyze/query-filter/languages/esql-cross-clusters.md).
  - [Task management](/explore-analyze/query-filter/languages/esql-task-management.md).


- [Limitations](elasticsearch://reference/query-languages/esql/limitations.md): The current limitations of {{esql}}.

- [Examples](/explore-analyze/query-filter/languages/esql.md): A few examples of what you can do with {{esql}}.

To get started, you can also try [our ES|QL training course](https://www.elastic.co/training/introduction-to-esql).