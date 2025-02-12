---
applies:
  stack:
  serverless:
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-getting-started.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-using.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-examples.html
  - https://www.elastic.co/guide/en/kibana/current/esql.html
---

# ES|QL [esql]

% What needs to be done: Refine

% Scope notes: everything but language reference. Merge the pages about Kibana. Add links to reference's new location

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/esql.md
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/esql-getting-started.md
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/esql-using.md
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/esql-examples.md
% - [ ] ./raw-migrated-files/kibana/kibana/esql.md

## What's {{esql}}? [_the_esql_compute_engine]

**Elasticsearch Query Language ({{esql}})** is a piped query language for filtering, transforming, and analyzing data. 

You can author {{esql}} queries to find specific events, perform statistical analysis, and generate visualizations. It supports a wide range of [commands, functions and operators](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-functions-operators.html) to perform various data operations, such as filtering, aggregation, time-series analysis, and more. Today, it supports a subset of the features available in Query DSL, but it is rapidly evolving.

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

% Learn more in [Getting started with {{esql}}](/solutions/search/get-started.md), or try [our training course](https://www.elastic.co/training/introduction-to-esql).

## Next steps

Find more details about {{esql}} in the following documentation pages:
- [{{esql}} reference](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-language.html): 
  - Reference documentation for the [{{esql}} syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-syntax.html), [commands](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-commands.html), and [functions and operators](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-functions-operators.html).
  - Information about working with [metadata fields](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-metadata-fields.html) and [multivalued fields](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-multivalued-fields.html). 
  - Guidance for [data processing with DISSECT and GROK](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-process-data-with-dissect-and-grok.html) and [data enrichment with ENRICH](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-enrich-data.html).

- Using {{esql}}:
  - An overview of using the [`_query` API endpoint](/explore-analyze/query-filter/languages/esql-rest.md).
  - [Using {{esql}} in {{kib}}](../../../explore-analyze/query-filter/languages/esql-kibana.md).
  - [Using {{esql}} in {{elastic-sec}}](/explore-analyze/query-filter/languages/esql-elastic-security.md).
  - [Using {{esql}} across clusters](/explore-analyze/query-filter/languages/esql-cross-clusters.md).
  - [Task management](/explore-analyze/query-filter/languages/esql-task-management.md).

- [Limitations](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-limitations.html): The current limitations of {{esql}}.

- [Examples](/explore-analyze/query-filter/languages/esql.md): A few examples of what you can do with {{esql}}.

To get started, you can also try [our ES|QL training course](https://www.elastic.co/training/introduction-to-esql).