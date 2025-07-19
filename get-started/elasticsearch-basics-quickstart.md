---
applies_to:
  stack:
  serverless:
---
# Index and search data

This quick start guide is a hands-on introduction to the fundamental concepts of Elasticsearch: [indices, documents, and field type mappings](/manage-data/data-store/index-basics.md).
You'll learn how to create an index, add data as documents, work with dynamic and explicit mappings, and perform your first basic searches.

::::{tip}
The code examples in this tutorial are in [Console](/explore-analyze/query-filter/tools/console.md) syntax by default.
You can [convert into other programming languages](/explore-analyze/query-filter/tools/console.md#import-export-console-requests) in the Console UI.

::::

## Requirements [getting-started-requirements]

You can follow this guide using any {{es}} deployment.
If you do not already have a deployment up and running, refer to [choose your deployment type](/deploy-manage/deploy.md#choosing-your-deployment-type) for your options.
To get started quickly, you can spin up a cluster [locally in Docker](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md).

% TBD: List privileges required to perform these steps

## Add data to {{es}}

:::{tip}
This tutorial uses {{es}} APIs, but there are many other ways to [add data to {{es}}](/solutions/search/ingest-for-search.md).
:::

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

Submit the following indexing request to add a single document to the `books` index:

```console
POST books/_doc
{
  "name": "Snow Crash",
  "author": "Neal Stephenson",
  "release_date": "1992-06-01",
  "page_count": 470
}
```

:::{tip}
If the index didn't already exist, this request would automatically create it.
:::

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

1. The `_index` field indicates the index the document was added to.
2. The `_id` field is the unique identifier for the document.
3. The `_version` field indicates the version of the document.
4. The `result` field indicates the result of the indexing operation.
5. The `_shards` field contains information about the number of [shards](/deploy-manage/index.md) that the indexing operation was executed on and the number that succeeded.
6. The `total` field indicates the total number of shards for the index.
7. The `successful` field indicates the number of shards that the indexing operation was executed on.
8. The `failed` field indicates the number of shards that failed during the indexing operation. *0* indicates no failures.
9. The `_seq_no` field holds a monotonically increasing number incremented for each indexing operation on a shard.
10. The `_primary_term` field is a monotonically increasing number incremented each time a primary shard is assigned to a different node.

:::
::::
::::{step} Add multiple documents

Use the [`_bulk` endpoint]({{es-apis}}operation/operation-bulk) to add multiple documents in one request.
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
::::{step} Use dynamic mappings

[Mappings](/manage-data/data-store/index-basics.md#elasticsearch-intro-documents-fields-mappings) define how data is stored and indexed in {{es}}, like a schema in a relational database.

If you use dynamic mapping, {{es}} automatically creates mappings for new fields.
The documents we've added so far have used dynamic mapping, because we didn't specify a mapping when creating the index.

To see how dynamic mapping works, add a new document to the `books` index with a field that doesn't appear in the existing documents.

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
::::{step} Add explicit mappings

Create an index named `my-explicit-mappings-books` with explicit mappings. Pass each field's properties as a JSON object. This object should contain the [field data type](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md) and any additional [mapping parameters](elasticsearch://reference/elasticsearch/mapping-reference/mapping-parameters.md).

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

1. Disables dynamic mapping for the index. Fields not defined in the mapping will still be stored in the document's `_source` field, but they won't be indexed or searchable.
2. The `properties` object defines the fields and their data types for documents in this index.

:::{dropdown} Example response
```console-result
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "my-explicit-mappings-books"
}
```

:::
::::
::::{step} Combine dynamic and explicit mappings

Explicit mappings are defined at index creation, and documents must conform to these mappings. You can also use the [update mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-mapping). When an index has the `dynamic` flag set to `true`, you can add new fields to documents without updating the mapping.

This allows you to combine explicit and dynamic mappings. Learn more about [managing and updating mappings](/manage-data/data-store/mapping.md#mapping-manage-update).

::::
:::::

## Search your data

Indexed documents are available for search in near real-time, using the [`_search` API](/solutions/search/querying-for-search.md).

:::::{stepper}
::::{step} Search all documents

Run the following command to search the `books` index for all documents:

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

1. The `took` field indicates the time in milliseconds for {{es}} to execute the search
2. The `timed_out` field indicates whether the search timed out
3. The `_shards` field contains information about the number of [shards](/reference/glossary/index.md) that the search was executed on and the number that succeeded
4. The `hits` object contains the search results
5. The `total` object provides information about the total number of matching documents
6. The `max_score` field indicates the highest relevance score among all matching documents
7. The `_index` field indicates the index the document belongs to
8. The `_id` field is the document's unique identifier
9. The `_score` field indicates the relevance score of the document
10. The `_source` field contains the original JSON object submitted during indexing

:::
::::
::::{step} Try a match query

% Introduce different query languages, in this case Query DSL

You can use the [`match` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md) to search for documents that contain a specific value in a specific field.
This is the standard query for full-text searches.

Run the following command to search the `books` index for documents containing `brave` in the `name` field:

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

1. The `max_score` is the score of the highest-scoring document in the results. In this case, there is only one matching document, so the `max_score` is the score of that document.
:::
::::
:::::

## Delete your indices (optional)

When following along with examples, you might want to delete an index to start from scratch.
You can delete indices using the [delete index API]({{es-apis}}operation/operation-indices-delete).

For example, run the following command to delete the indices created in this tutorial:

```console
DELETE /books
DELETE /my-explicit-mappings-books
```

::::{warning}
Deleting an index permanently deletes its documents, shards, and metadata.
::::

% TBD: What are the recommended next steps?