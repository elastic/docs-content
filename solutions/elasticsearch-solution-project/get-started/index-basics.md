---
applies_to:
  stack:
  serverless:
---
# Index and search basics

This quickstart provides a hands-on introduction to the fundamental concepts of {{es}}: [indices, documents, and field type mappings](../../../manage-data/data-store/index-basics.md). You'll learn how to create an index, add documents, work with dynamic and explicit mappings, and perform your first basic searches.

::::{tip}
The code examples are in [Console](/explore-analyze/query-filter/tools/console.md) syntax by default.
You can [convert into other programming languages](/explore-analyze/query-filter/tools/console.md#import-export-console-requests) in the Console UI.
::::

## Requirements [getting-started-requirements]

You can follow this guide using any {{es}} deployment.
To see all deployment options, refer to [](/deploy-manage/deploy.md#choosing-your-deployment-type).
To get started quickly, spin up a cluster [locally in Docker](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md).

## Add data to {{es}} [getting-started-index-creation]

::::{tip}
This quickstart uses {{es}} APIs, but there are many other ways to [add data to {{es}}](/solutions/search/ingest-for-search.md).
::::

You add data to {{es}} as JSON objects called documents.
{{es}} stores these documents in searchable indices.

:::::{stepper}
::::{step} Create an index

Create a new index named `books`:

```console
PUT /books
```

The following response indicates the index was created successfully.

:::{dropdown} Example response

```console-result
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "books"
}
```

:::
::::
::::{step} Add a single document

Use the following request to add a single document to the `books` index.
If the index doesn't already exist, this request will automatically create it.

```console
POST books/_doc
{
  "name": "Snow Crash",
  "author": "Neal Stephenson",
  "release_date": "1992-06-01",
  "page_count": 470
}
```

The response includes metadata that {{es}} generates for the document, including a unique `_id` for the document within the index.

:::{dropdown} Example response

```console-result
{
  "_index": "books", <1>
  "_id": "O0lG2IsBaSa7VYx_rEia", <2>
  "_version": 1, <3>
  "result": "created", <4>
  "_shards": { <5>
    "total": 2, <6>
    "successful": 2, <7>
    "failed": 0 <8>
  },
  "_seq_no": 0, <9>
  "_primary_term": 1 <10>
}
```

1. `_index`: The index the document was added to.
2. `_id`: The unique identifier for the document.
3. `_version`: The version of the document.
4. `result`: The result of the indexing operation.
5. `_shards`: Information about the number of [shards](/deploy-manage/distributed-architecture/clusters-nodes-shards.md) that the indexing operation was executed on and the number that succeeded.
6. `total`: The total number of shards for the index.
7. `successful`: The number of shards that the indexing operation was performed on.
8. `failed`: The number of shards that failed during the indexing operation. *0* indicates no failures.
9. `_seq_no`: A monotonically increasing number incremented for each indexing operation on a shard.
10. `_primary_term`: A monotonically increasing number incremented each time a primary shard is assigned to a different node.
:::
::::
::::{step} Add multiple documents

Use the [`_bulk` endpoint]({{es-apis}}operation/operation-bulk) to add multiple documents in a single request.
Bulk data must be formatted as newline-delimited JSON (NDJSON).

```console
POST /_bulk
{ "index" : { "_index" : "books" } }
{"name": "Revelation Space", "author": "Alastair Reynolds", "release_date": "2000-03-15", "page_count": 585}
{ "index" : { "_index" : "books" } }
{"name": "1984", "author": "George Orwell", "release_date": "1985-06-01", "page_count": 328}
{ "index" : { "_index" : "books" } }
{"name": "Fahrenheit 451", "author": "Ray Bradbury", "release_date": "1953-10-15", "page_count": 227}
{ "index" : { "_index" : "books" } }
{"name": "Brave New World", "author": "Aldous Huxley", "release_date": "1932-06-01", "page_count": 268}
{ "index" : { "_index" : "books" } }
{"name": "The Handmaids Tale", "author": "Margaret Atwood", "release_date": "1985-06-01", "page_count": 311}
```

You should receive a response indicating there were no errors.

:::{dropdown} Example response

```console-result
{
  "errors": false,
  "took": 29,
  "items": [
    {
      "index": {
        "_index": "books",
        "_id": "QklI2IsBaSa7VYx_Qkh-",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 2,
          "successful": 2,
          "failed": 0
        },
        "_seq_no": 1,
        "_primary_term": 1,
        "status": 201
      }
    },
    {
      "index": {
        "_index": "books",
        "_id": "Q0lI2IsBaSa7VYx_Qkh-",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 2,
          "successful": 2,
          "failed": 0
        },
        "_seq_no": 2,
        "_primary_term": 1,
        "status": 201
      }
    },
    {
      "index": {
        "_index": "books",
        "_id": "RElI2IsBaSa7VYx_Qkh-",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 2,
          "successful": 2,
          "failed": 0
        },
        "_seq_no": 3,
        "_primary_term": 1,
        "status": 201
      }
    },
    {
      "index": {
        "_index": "books",
        "_id": "RUlI2IsBaSa7VYx_Qkh-",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 2,
          "successful": 2,
          "failed": 0
        },
        "_seq_no": 4,
        "_primary_term": 1,
        "status": 201
      }
    },
    {
      "index": {
        "_index": "books",
        "_id": "RklI2IsBaSa7VYx_Qkh-",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 2,
          "successful": 2,
          "failed": 0
        },
        "_seq_no": 5,
        "_primary_term": 1,
        "status": 201
      }
    }
  ]
}
```

:::
::::
::::{step} Use dynamic mapping

[Mappings](/manage-data/data-store/index-basics.md#elasticsearch-intro-documents-fields-mappings) define how data is stored and indexed in {{es}}, like a schema in a relational database.

If you use dynamic mapping, {{es}} automatically creates mappings for new fields.
The documents you've added so far have used dynamic mapping, because you didn't specify a mapping while creating the index.

To see how dynamic mapping works, add a new document to the `books` index with a field that isn't available in the existing documents.

```console
POST /books/_doc
{
  "name": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "release_date": "1925-04-10",
  "page_count": 180,
  "language": "EN" <1>
}
```

1. The new field.

View the mapping for the `books` index with the [get mapping API]({{es-apis}}operation/operation-indices-get-mapping).
The new field `language` has been added to the mapping with a `text` data type.

```console
GET /books/_mapping
```

The following response displays the mappings that were created by {{es}}.
:::{dropdown} Example response

```console-result
{
  "books": {
    "mappings": {
      "properties": {
        "author": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "name": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "language": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "page_count": {
          "type": "long"
        },
        "release_date": {
          "type": "date"
        }
      }
    }
  }
}
```
:::
::::
::::{step} Define explicit mapping

Create an index named `my-explicit-mappings-books` and specify the mappings yourself.
Pass each field's properties as a JSON object.
This object should contain the [field data type](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md) and any additional [mapping parameters](elasticsearch://reference/elasticsearch/mapping-reference/mapping-parameters.md).

```console
PUT /my-explicit-mappings-books
{
  "mappings": {
    "dynamic": false,  <1>
    "properties": {  <2>
      "name": { "type": "text" },
      "author": { "type": "text" },
      "release_date": { "type": "date", "format": "yyyy-MM-dd" },
      "page_count": { "type": "integer" }
    }
  }
}
```

1. `dynamic`: Turns off dynamic mapping for the index. If you don't define fields in the mapping, they'll still be stored in the document's `_source` field, but you can't index or search them.
2. `properties`: Defines the fields and their corresponding data types.

The following response indicates a successful operation.
:::{dropdown} Example response
```console-result
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "my-explicit-mappings-books"
}
```
:::

Explicit mappings are defined at index creation, and documents must conform to these mappings.
You can also use the [update mapping API]({{es-apis}}operation/operation-indices-put-mapping).
When an index has the `dynamic` flag set to `true`, you can add new fields to documents without updating the mapping, which allows you to combine explicit and dynamic mappings.
Learn more about [managing and updating mappings](/manage-data/data-store/mapping.md#mapping-manage-update).
::::
:::::

## Search your data [getting-started-search-data]

Indexed documents are available for search in near real-time, using the [`_search` API](/solutions/search/querying-for-search.md).

:::::{stepper}
::::{step} Search all documents

Use the following request to search all documents in the `books` index:

```console
GET books/_search
```

:::{dropdown} Example response
```console-result
{
  "took": 2, <1>
  "timed_out": false, <2>
  "_shards": { <3>
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": { <4>
    "total": { <5>
      "value": 7,
      "relation": "eq"
    },
    "max_score": 1, <6>
    "hits": [
      {
        "_index": "books", <7>
        "_id": "CwICQpIBO6vvGGiC_3Ls", <8>
        "_score": 1, <9>
        "_source": { <10>
          "name": "Brave New World",
          "author": "Aldous Huxley",
          "release_date": "1932-06-01",
          "page_count": 268
        }
      },
      ... (truncated)
    ]
  }
}
```

1. `took`: The time in milliseconds for {{es}} to execute the search
2. `timed_out`: Indicates if the search timed out
3. `_shards`: Information about the number of [shards](/reference/glossary/index.md) that the search was performed on and the number that succeeded
4. `hits`: Has the search results
5. `total`: Information about the total number of matching documents
6. `max_score`: The highest relevance score among all matching documents
7. `_index`: The index the document belongs to
8. `_id`: The document's unique identifier
9. `_score`: The relevance score of the document
10. `_source`: The original JSON object submitted during indexing

:::
::::
::::{step} Search with a match query

Use the [`match` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md) to search for documents that contain a specific value in a specific field. This is the standard query for full-text searches.

Use the following request to search the `books` index for documents containing `brave` in the `name` field:

```console
GET books/_search
{
  "query": {
    "match": {
      "name": "brave"
    }
  }
}
```

:::{tip}
This example uses [Query DSL](/explore-analyze/query-filter/languages/querydsl.md), which is the primary query language for {{es}}.
:::

:::{dropdown} Example response
```console-result
{
  "took": 9,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.6931471, <1>
    "hits": [
      {
        "_index": "books",
        "_id": "CwICQpIBO6vvGGiC_3Ls",
        "_score": 0.6931471,
        "_source": {
          "name": "Brave New World",
          "author": "Aldous Huxley",
          "release_date": "1932-06-01",
          "page_count": 268
        }
      }
    ]
  }
}
```

1. `max_score`: Score of the highest-scoring document in the results. In this case, there is only one matching document, so the `max_score` is the score of that document.
:::
::::
:::::

## Delete your indices [getting-started-delete-indices]

If you want to delete an index to start from scratch at any point, use the [delete index API]({{es-apis}}operation/operation-indices-delete).

For example, use the following request to delete the indices created in this quickstart:

```console
DELETE /books
DELETE /my-explicit-mappings-books
```

::::{warning}
Deleting an index permanently deletes its documents, shards, and metadata.

::::

## Next steps

This quickstart introduced the basics of creating indices, adding data, and performing basic searches with {{es}}.
To try out similar steps from the {{es}} Python client, go to [](/solutions/search/get-started/keyword-search-python.md).
The following resources will help you understand {{es}} concepts better and dive into the basics of query languages for searching data:

* [Fundamentals of Elasticsearch](/manage-data/data-store.md)
* [Search and filter with Query DSL](elasticsearch://reference/query-languages/query-dsl/full-text-filter-tutorial.md)
* [Search using ES|QL](elasticsearch://reference/query-languages/esql/esql-search-tutorial.md)


