---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/runtime.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Runtime fields [runtime]

A *runtime field* is a field that is evaluated at query time. Runtime fields enable you to:

* Add fields to existing documents without reindexing your data
* Start working with your data without understanding how it’s structured
* Override the value returned from an indexed field at query time
* Define fields for a specific use without modifying the underlying schema

You access runtime fields from the search API like any other field, and {{es}} sees runtime fields no differently. You can define runtime fields in the [index mapping](map-runtime-field.md) or in the [search request](define-runtime-fields-in-search-request.md). Your choice, which is part of the inherent flexibility of runtime fields.

Use the [`fields`](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md) parameter on the `_search` API to [retrieve the values of runtime fields](retrieve-runtime-field.md). Runtime fields won’t display in `_source`, but the `fields` API works for all fields, even those that were not sent as part of the original `_source`.

Runtime fields are useful when working with log data (see [examples](explore-data-with-runtime-fields.md)), especially when you’re unsure about the data structure. Your search speed decreases, but your index size is much smaller and you can more quickly process logs without having to index them.


## Benefits [runtime-benefits]

Because runtime fields aren’t indexed, adding a runtime field doesn’t increase the index size. You define runtime fields directly in the index mapping, saving storage costs and increasing ingestion speed. You can more quickly ingest data into the Elastic Stack and access it right away. When you define a runtime field, you can immediately use it in search requests, aggregations, filtering, and sorting.

If you change a runtime field into an indexed field, you don’t need to modify any queries that refer to the runtime field. Better yet, you can refer to some indices where the field is a runtime field, and other indices where the field is an indexed field. You have the flexibility to choose which fields to index and which ones to keep as runtime fields.

At its core, the most important benefit of runtime fields is the ability to add fields to documents after you’ve ingested them. This capability simplifies mapping decisions because you don’t have to decide how to parse your data up front, and can use runtime fields to amend the mapping at any time. Using runtime fields allows for a smaller index and faster ingest time, which combined use less resources and reduce your operating costs.


## Incentives [runtime-incentives]

Runtime fields can replace many of the ways you can use scripting with the `_search` API. How you use a runtime field is impacted by the number of documents that the included script runs against. For example, if you’re using the `fields` parameter on the `_search` API to [retrieve the values of a runtime field](retrieve-runtime-field.md), the script runs only against the top hits just like script fields do.

You can use [script fields](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md#script-fields) to access values in `_source` and return calculated values based on a script valuation. Runtime fields have the same capabilities, but provide greater flexibility because you can query and aggregate on runtime fields in a search request. Script fields can only fetch values.

Similarly, you could write a [script query](elasticsearch://reference/query-languages/query-dsl/query-dsl-script-query.md) that filters documents in a search request based on a script. Runtime fields provide a very similar feature that is more flexible. You write a script to create field values and they are available everywhere, such as [`fields`](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md), [all queries](../../../explore-analyze/query-filter/languages/querydsl.md), and [aggregations](../../../explore-analyze/query-filter/aggregations.md).

You can also use scripts to [sort search results](elasticsearch://reference/elasticsearch/rest-apis/sort-search-results.md#script-based-sorting), but that same script works exactly the same in a runtime field.

If you move a script from any of these sections in a search request to a runtime field that is computing values from the same number of documents, the performance should be about the same. The performance for these features is largely dependent upon the calculations that the included script is running and how many documents the script runs against.


## Compromises [runtime-compromises]

Runtime fields use less disk space and provide flexibility in how you access your data, but can impact search performance based on the computation defined in the runtime script.

To balance search performance and flexibility, index fields that you’ll frequently search for and filter on, such as a timestamp. {{es}} automatically uses these indexed fields first when running a query, resulting in a fast response time. You can then use runtime fields to limit the number of fields that {{es}} needs to calculate values for. Using indexed fields in tandem with runtime fields provides flexibility in the data that you index and how you define queries for other fields.

Use the [asynchronous search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit) to run searches that include runtime fields. This method of search helps to offset the performance impacts of computing values for runtime fields in each document containing that field. If the query can’t return the result set synchronously, you’ll get results asynchronously as they become available.

::::{important}
Queries against runtime fields are considered expensive. If [`search.allow_expensive_queries`](../../../explore-analyze/query-filter/languages/querydsl.md#query-dsl-allow-expensive-queries) is set to `false`, expensive queries are not allowed and {{es}} will reject any queries against runtime fields.
::::








