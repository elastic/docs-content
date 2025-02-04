# {{esql}} [esql]

The {{es}} Query Language ({{esql}}) provides a powerful way to filter, transform, and analyze data stored in {{es}}, and in the future in other runtimes. It is designed to be easy to learn and use, by end users, SRE teams, application developers, and administrators.

Users can author {{esql}} queries to find specific events, perform statistical analysis, and generate visualizations. It supports a wide range of commands and functions that enable users to perform various data operations, such as filtering, aggregation, time-series analysis, and more.

The {{es}} Query Language ({{esql}}) makes use of "pipes" (|) to manipulate and transform data in a step-by-step fashion. This approach allows users to compose a series of operations, where the output of one operation becomes the input for the next, enabling complex data transformations and analysis.


## The {{esql}} Compute Engine [_the_esql_compute_engine] 

{{esql}} is more than a language: it represents a significant investment in new compute capabilities within {{es}}. To achieve both the functional and performance requirements for {{esql}}, it was necessary to build an entirely new compute architecture. {{esql}} search, aggregation, and transformation functions are directly executed within Elasticsearch itself. Query expressions are not transpiled to Query DSL for execution. This approach allows {{esql}} to be extremely performant and versatile.

The new {{esql}} execution engine was designed with performance in mind — it operates on blocks at a time instead of per row, targets vectorization and cache locality, and embraces specialization and multi-threading. It is a separate component from the existing Elasticsearch aggregation framework with different performance characteristics.

The {{esql}} documentation is organized in these sections:

[Getting started](../../../explore-analyze/query-filter/languages/esorql.md)
:   A tutorial to help you get started with {{esql}}.

[{{esql}} reference](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-language.html)
:   Reference documentation for the [{{esql}} syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-syntax.html), [commands](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-commands.html), and [functions and operators](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-functions-operators.html). Information about working with [metadata fields](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-metadata-fields.html) and [multivalued fields](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-multivalued-fields.html). And guidance for [data processing with DISSECT and GROK](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-process-data-with-dissect-and-grok.html) and [data enrichment with ENRICH](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-enrich-data.html).

[*Using {{esql}}*](../../../explore-analyze/query-filter/languages/esorql.md)
:   An overview of using the [REST API](../../../explore-analyze/query-filter/languages/esql-rest.md), [Using {{esql}} in {{kib}}](../../../explore-analyze/query-filter/languages/esql-kibana.md), [Using {{esql}} in {{elastic-sec}}](../../../explore-analyze/query-filter/languages/esql-elastic-security.md), [Using {{esql}} across clusters](../../../explore-analyze/query-filter/languages/esql-cross-clusters.md), and [Task management](../../../explore-analyze/query-filter/languages/esql-task-management.md).

[Limitations](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-limitations.html)
:   The current limitations of {{esql}}.

[Examples](../../../explore-analyze/query-filter/languages/esorql.md)
:   A few examples of what you can do with {{esql}}.

