---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-analyze.html
---

# Querying and filtering [search-analyze]

You can use {{es}} as a basic document store to retrieve documents and their metadata. However, the real power of {{es}} comes from its advanced search and analytics capabilities.

You’ll use a combination of an API endpoint and a query language to interact with your data.


## REST API [search-analyze-rest-api]

Use REST APIs to manage your {{es}} cluster, and to index and search your data. For testing purposes, you can submit requests directly from the command line or through the Dev Tools [Console](query-filter/tools/console.md) in {{kib}}. From your applications, you can use a [client](https://www.elastic.co/guide/en/elasticsearch/client/index.md) in your programming language of choice.

Refer to [first steps with Elasticsearch](../solutions/search/get-started.md) for a hands-on example of using the `_search` endpoint, adding data to {{es}}, and running basic searches in Query DSL syntax.


## Query languages [search-analyze-query-languages]

{{es}} provides a number of query languages for interacting with your data.

**Query DSL** is the primary query language for {{es}} today.

**{{esql}}** is a new piped query language and compute engine which was first added in version **8.11**.

{{esql}} does not yet support all the features of Query DSL. Look forward to new {{esql}} features and functionalities in each release.

Refer to [Query languages](#search-analyze-query-languages) for a full overview of the query languages available in {{es}}.


### Query DSL [search-analyze-query-dsl]

[Query DSL](query-filter/languages/querydsl.md) is a full-featured JSON-style query language that enables complex searching, filtering, and aggregations. It is the original and most powerful query language for {{es}} today.

The [`_search` endpoint](../solutions/search/querying-for-search-searching-with-the-search-api.md) accepts queries written in Query DSL syntax.


#### Search and filter with Query DSL [search-analyze-query-dsl-search-filter]

Query DSL support a wide range of search techniques, including the following:

* [**Full-text search**](../solutions/search/full-text.md): Search text that has been analyzed and indexed to support phrase or proximity queries, fuzzy matches, and more.
* [**Keyword search**](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html): Search for exact matches using `keyword` fields.
* [**Semantic search**](../solutions/search/semantic-search/semantic-search-semantic-text.md): Search `semantic_text` fields using dense or sparse vector search on embeddings generated in your {{es}} cluster.
* [**Vector search**](../solutions/search/vector/knn.md): Search for similar dense vectors using the kNN algorithm for embeddings generated outside of {{es}}.
* [**Geospatial search**](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-queries.html): Search for locations and calculate spatial relationships using geospatial queries.

Learn about the full range of queries supported by [Query DSL](query-filter/languages/querydsl.md).

You can also filter data using Query DSL. Filters enable you to include or exclude documents by retrieving documents that match specific field-level criteria. A query that uses the `filter` parameter indicates [filter context](query-filter/languages/querydsl.md#filter-context).


#### Analyze with Query DSL [search-analyze-data-query-dsl]

[Aggregations](aggregations.md) are the primary tool for analyzing {{es}} data using Query DSL. Aggregrations enable you to build complex summaries of your data and gain insight into key metrics, patterns, and trends.

Because aggregations leverage the same data structures used for search, they are also very fast. This enables you to analyze and visualize your data in real time. You can search documents, filter results, and perform analytics at the same time, on the same data, in a single request. That means aggregations are calculated in the context of the search query.

The folowing aggregation types are available:

* [Metric](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics.html): Calculate metrics, such as a sum or average, from field values.
* [Bucket](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket.html): Group documents into buckets based on field values, ranges, or other criteria.
* [Pipeline](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline.html): Run aggregations on the results of other aggregations.

Run aggregations by specifying the [search API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html)'s `aggs` parameter. Learn more in [Run an aggregation](aggregations.md#run-an-agg).


### {{esql}} [search-analyze-data-esql]

[Elasticsearch Query Language ({{esql}})](query-filter/languages/esorql.md) is a piped query language for filtering, transforming, and analyzing data. {{esql}} is built on top of a new compute engine, where search, aggregation, and transformation functions are directly executed within {{es}} itself. {{esql}} syntax can also be used within various {{kib}} tools.

The [`_query` endpoint](query-filter/languages/esql-rest.md) accepts queries written in {{esql}} syntax.

Today, it supports a subset of the features available in Query DSL, but it is rapidly evolving.

It comes with a comprehensive set of [functions and operators](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-functions-operators.html) for working with data and has robust integration with {{kib}}'s Discover, dashboards and visualizations.

Learn more in [Getting started with {{esql}}](../solutions/search/get-started.md), or try [our training course](https://www.elastic.co/training/introduction-to-esql).


## List of available query languages [search-analyze-data-query-languages-table]

The following table summarizes all available {{es}} query languages, to help you choose the right one for your use case.

| Name | Description | Use cases | API endpoint |
| --- | --- | --- | --- |
| [Query DSL](query-filter/languages/querydsl.md) | The primary query language for {{es}}. A powerful and flexible JSON-style language that enables complex queries. | Full-text search, semantic search, keyword search, filtering, aggregations, and more. | [`_search`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html) |
| [{{esql}}](query-filter/languages/esorql.md) | Introduced in **8.11**, the Elasticsearch Query Language ({{esql}}) is a piped query language language for filtering, transforming, and analyzing data. | Initially tailored towards working with time series data like logs and metrics.Robust integration with {{kib}} for querying, visualizing, and analyzing data.Does not yet support full-text search. | [`_query`](query-filter/languages/esql-rest.md) |
| [EQL](query-filter/languages/eql.md) | Event Query Language (EQL) is a query language for event-based time series data. Data must contain the `@timestamp` field to use EQL. | Designed for the threat hunting security use case. | [`_eql`](https://www.elastic.co/guide/en/elasticsearch/reference/current/eql-apis.html) |
| [Elasticsearch SQL](query-filter/languages/sql.md) | Allows native, real-time SQL-like querying against {{es}} data. JDBC and ODBC drivers are available for integration with business intelligence (BI) tools. | Enables users familiar with SQL to query {{es}} data using familiar syntax for BI and reporting. | [`_sql`](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-apis.html) |
| [Kibana Query Language (KQL)](query-filter/languages/kql.md) | {{kib}} Query Language (KQL) is a text-based query language for filtering data when you access it through the {{kib}} UI. | Use KQL to filter documents where a value for a field exists, matches a given value, or is within a given range. | N/A |

