---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-getting-started.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-using.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-examples.html
  - https://www.elastic.co/guide/en/kibana/current/esql.html
products:
  - id: elasticsearch
  - id: kibana
---

# {{esql}} [esql]

:::{tip}
Looking for the {{esql}} syntax reference? Refer to the [reference documentation](elasticsearch://reference/query-languages/esql.md).
:::

**Elasticsearch Query Language ({{esql}})** is a piped query language for filtering, transforming, and analyzing data.

## What's {{esql}}? [_the_esql_compute_engine]

You can author {{esql}} queries to find specific events, perform statistical analysis, and create visualizations. It supports a wide range of commands, functions, and operators to perform various data operations, such as filter, aggregation, time-series analysis, and more. It initially supported a subset of the features available in Query DSL, but it is rapidly evolving with every {{serverless-full}} and Stack release.

{{esql}} is designed to be easy to read and write, making it accessible for users with varying levels of technical expertise. It is particularly useful for data analysts, security professionals, and developers who need to work with large datasets in Elasticsearch.

## How does it work? [search-analyze-data-esql]

{{esql}} uses pipes (`|`) to manipulate and transform data in a step-by-step fashion. This approach allows you to compose a series of operations, where the output of one operation becomes the input for the next, enabling complex data transformations and analysis.

Here's a simple example of an {{esql}} query:

```esql
FROM sample_data
| SORT @timestamp DESC
| LIMIT 3
```

Note that each line in the query represents a step in the data processing pipeline:
- The `FROM` clause specifies the index or data stream to query
- The `SORT` clause sorts the data by the `@timestamp` field in descending order
- The `LIMIT` clause restricts the output to the top 3 results

### User interfaces

You can interact with {{esql}} in two ways:

- **Programmatic access**: Use {{esql}} syntax with the {{es}} `_query` endpoint.

- **Interactive interfaces**: Work with {{esql}} through Elastic user interfaces including Kibana Discover, Dashboards, Dev Tools, and analysis tools in Elastic Security and Observability.

## Documentation

### Usage guides
- **Get started**
  - [Get started in docs](/explore-analyze/query-filter/languages/esql-getting-started.md)
  - [Training course](https://www.elastic.co/training/introduction-to-esql)
- **{{esql}} interfaces**
  - [Use the query API](/explore-analyze/query-filter/languages/esql-rest.md)
  - [Use {{esql}} in Kibana](/explore-analyze/query-filter/languages/esql-kibana.md)
  - [Use {{esql}} in Elastic Security](/explore-analyze/query-filter/languages/esql-elastic-security.md)
- **{{esql}} for search use cases**
  - [{{esql}} for search landing page](/solutions/search/esql-for-search.md)
  - [{{esql}} for search tutorial](/solutions/search/esql-search-tutorial.md)
- **Query multiple sources**
  - [Query multiple indices](/explore-analyze/query-filter/languages/esql-multi-index.md)
  - [Query across clusters](/explore-analyze/query-filter/languages/esql-cross-clusters.md)

### Reference documentation

#### Core references
* [{{esql}} reference](elasticsearch://reference/query-languages/esql.md)
* [{{esql}} syntax](elasticsearch://reference/query-languages/esql/esql-syntax.md)

#### Commands, functions, and operators
* [Commands](elasticsearch://reference/query-languages/esql/esql-commands.md)
* [Functions and operators](elasticsearch://reference/query-languages/esql/esql-functions-operators.md)

#### Field types
* [Metadata fields](elasticsearch://reference/query-languages/esql/esql-metadata-fields.md)
* [Multivalued fields](elasticsearch://reference/query-languages/esql/esql-multivalued-fields.md)

#### Advanced features
* [DISSECT and GROK](elasticsearch://reference/query-languages/esql/esql-process-data-with-dissect-grok.md)
* [ENRICH](elasticsearch://reference/query-languages/esql/esql-enrich-data.md)
* [LOOKUP JOIN](elasticsearch://reference/query-languages/esql/esql-lookup-join.md)

#### Limitations
* [Limitations](elasticsearch://reference/query-languages/esql/limitations.md)

::::{note}
**{{esql}}'s compute architecture**

{{esql}} is built on top of a new compute architecture within {{es}}, designed to achieve high functional and performance requirements for {{esql}}. {{esql}} search, aggregation, and transformation functions are directly executed within Elasticsearch itself. Query expressions are not transpiled to Query DSL for execution. This approach allows {{esql}} to be extremely performant and versatile.

The new {{esql}} execution engine was designed with performance in mind — it operates on blocks at a time instead of per row, targets vectorization and cache locality, and embraces specialization and multi-threading. It is a separate component from the existing Elasticsearch aggregation framework with different performance characteristics.
::::
