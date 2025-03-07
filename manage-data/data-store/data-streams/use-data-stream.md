---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/use-a-data-stream.html
applies_to:
  stack: ga
  serverless: ga
---

# Use a data stream [use-a-data-stream]

After you [set up a data stream](set-up-data-stream.md), you can do the following:

- [Use a data stream \[use-a-data-stream\]](#use-a-data-stream-use-a-data-stream)
  - [Add documents to a data stream \[add-documents-to-a-data-stream\]](#add-documents-to-a-data-stream-add-documents-to-a-data-stream)
  - [Search a data stream \[search-a-data-stream\]](#search-a-data-stream-search-a-data-stream)
  - [Get statistics for a data stream \[get-stats-for-a-data-stream\]](#get-statistics-for-a-data-stream-get-stats-for-a-data-stream)
  - [Manually roll over a data stream \[manually-roll-over-a-data-stream\]](#manually-roll-over-a-data-stream-manually-roll-over-a-data-stream)
  - [Open closed backing indices \[open-closed-backing-indices\]](#open-closed-backing-indices-open-closed-backing-indices)
  - [Reindex with a data stream \[reindex-with-a-data-stream\]](#reindex-with-a-data-stream-reindex-with-a-data-stream)
  - [Update documents in a data stream by query \[update-docs-in-a-data-stream-by-query\]](#update-documents-in-a-data-stream-by-query-update-docs-in-a-data-stream-by-query)
  - [Delete documents in a data stream by query \[delete-docs-in-a-data-stream-by-query\]](#delete-documents-in-a-data-stream-by-query-delete-docs-in-a-data-stream-by-query)
  - [Update or delete documents in a backing index \[update-delete-docs-in-a-backing-index\]](#update-or-delete-documents-in-a-backing-index-update-delete-docs-in-a-backing-index)


## Add documents to a data stream [add-documents-to-a-data-stream]

To add an individual document, use the [index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-create). [Ingest pipelines](../../ingest/transform-enrich/ingest-pipelines.md) are supported.

```console
POST /my-data-stream/_doc/
{
  "@timestamp": "2099-03-08T11:06:07.000Z",
  "user": {
    "id": "8a4f500d"
  },
  "message": "Login successful"
}
```

You cannot add new documents to a data stream using the index API’s `PUT /<target>/_doc/<_id>` request format. To specify a document ID, use the `PUT /<target>/_create/<_id>` format instead. Only an [`op_type`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-create#docs-index-api-op_type) of `create` is supported.

To add multiple documents with a single request, use the [bulk API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk). Only `create` actions are supported.

```console
PUT /my-data-stream/_bulk?refresh
{"create":{ }}
{ "@timestamp": "2099-03-08T11:04:05.000Z", "user": { "id": "vlb44hny" }, "message": "Login attempt failed" }
{"create":{ }}
{ "@timestamp": "2099-03-08T11:06:07.000Z", "user": { "id": "8a4f500d" }, "message": "Login successful" }
{"create":{ }}
{ "@timestamp": "2099-03-09T11:07:08.000Z", "user": { "id": "l7gk7f82" }, "message": "Logout successful" }
```


## Search a data stream [search-a-data-stream]

The following search APIs support data streams:

* [Search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search)
* [Async search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit)
* [Multi search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch)
* [Field capabilities](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-field-caps)
* [EQL search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-eql-search)


## Get statistics for a data stream [get-stats-for-a-data-stream]

Use the [data stream stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-data-streams-stats-1) to get statistics for one or more data streams:

```console
GET /_data_stream/my-data-stream/_stats?human=true
```


## Manually roll over a data stream [manually-roll-over-a-data-stream]

Use the [rollover API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover) to manually [roll over](../data-streams.md#data-streams-rollover) a data stream. You have two options when manually rolling over:

1. To immediately trigger a rollover:

    ```console
    POST /my-data-stream/_rollover/
    ```

2. Or to postpone the rollover until the next indexing event occurs:

    ```console
    POST /my-data-stream/_rollover?lazy
    ```

    Use the second to avoid having empty backing indices in data streams that do not get updated often.



## Open closed backing indices [open-closed-backing-indices]

You cannot search a [closed](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-close) backing index, even by searching its data stream. You also cannot [update](#update-docs-in-a-data-stream-by-query) or [delete](#delete-docs-in-a-data-stream-by-query) documents in a closed index.

To re-open a closed backing index, submit an [open index API request](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-open) directly to the index:

```console
POST /.ds-my-data-stream-2099.03.07-000001/_open/
```
%  TEST[setup:my_index]
%  TEST[s/.ds-my-data-stream-2099.03.07-000001/my-index-000001/]

To re-open all closed backing indices for a data stream, submit an open index API request to the stream:

```console
POST /my-data-stream/_open/
```


## Reindex with a data stream [reindex-with-a-data-stream]

Use the [reindex API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) to copy documents from an existing index, alias, or data stream to a data stream. Because data streams are [append-only](../data-streams.md#data-streams-append-only), a reindex into a data stream must use an `op_type` of `create`. A reindex cannot update existing documents in a data stream.

```console
POST /_reindex
{
  "source": {
    "index": "archive"
  },
  "dest": {
    "index": "my-data-stream",
    "op_type": "create"
  }
}
```
%  TEST[continued]


## Update documents in a data stream by query [update-docs-in-a-data-stream-by-query]

Use the [update by query API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update-by-query) to update documents in a data stream that match a provided query:

```console
POST /my-data-stream/_update_by_query
{
  "query": {
    "match": {
      "user.id": "l7gk7f82"
    }
  },
  "script": {
    "source": "ctx._source.user.id = params.new_id",
    "params": {
      "new_id": "XgdX0NoX"
    }
  }
}
```


## Delete documents in a data stream by query [delete-docs-in-a-data-stream-by-query]

Use the [delete by query API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-delete-by-query) to delete documents in a data stream that match a provided query:

```console
POST /my-data-stream/_delete_by_query
{
  "query": {
    "match": {
      "user.id": "vlb44hny"
    }
  }
}
```


## Update or delete documents in a backing index [update-delete-docs-in-a-backing-index]

If needed, you can update or delete documents in a data stream by sending requests to the backing index containing the document. You’ll need:

* The [document ID](elasticsearch://reference/elasticsearch/mapping-reference/mapping-id-field.md)
* The name of the backing index containing the document
* If updating the document, its [sequence number and primary term](elasticsearch://reference/elasticsearch/rest-apis/optimistic-concurrency-control.md)

To get this information, use a [search request](#search-a-data-stream):

```console
GET /my-data-stream/_search
{
  "seq_no_primary_term": true,
  "query": {
    "match": {
      "user.id": "yWIumJd7"
    }
  }
}
```

Response:

```console-result
{
  "took": 20,
  "timed_out": false,
  "_shards": {
    "total": 3,
    "successful": 3,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.2876821,
    "hits": [
      {
        "_index": ".ds-my-data-stream-2099.03.08-000003",      <1>
        "_id": "bfspvnIBr7VVZlfp2lqX",              <2>
        "_seq_no": 0,                               <3>
        "_primary_term": 1,                         <4>
        "_score": 0.2876821,
        "_source": {
          "@timestamp": "2099-03-08T11:06:07.000Z",
          "user": {
            "id": "yWIumJd7"
          },
          "message": "Login successful"
        }
      }
    ]
  }
}
```

1. Backing index containing the matching document
2. Document ID for the document
3. Current sequence number for the document
4. Primary term for the document
%  TESTRESPONSE[s/"took": 20/"took": $body.took/]
%  TESTRESPONSE[s/"max_score": 0.2876821/"max_score": $body.hits.max_score/]
%  TESTRESPONSE[s/"_index": ".ds-my-data-stream-2099.03.08-000003"/"_index": $body.hits.hits.0._index/]
%  TESTRESPONSE[s/"_score": 0.2876821/"_score": $body.hits.hits.0._score/]

To update the document, use an [index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-create) request with valid `if_seq_no` and `if_primary_term` arguments:

```console
PUT /.ds-my-data-stream-2099-03-08-000003/_doc/bfspvnIBr7VVZlfp2lqX?if_seq_no=0&if_primary_term=1
{
  "@timestamp": "2099-03-08T11:06:07.000Z",
  "user": {
    "id": "8a4f500d"
  },
  "message": "Login successful"
}
```
%  TEST[setup:my_index]
%  TEST[s/.ds-my-data-stream-2099.03.08-000003/my-index-000001/]
%  TEST[s/bfspvnIBr7VVZlfp2lqX/1/]
%  TEST[s/if_seq_no=0/if_seq_no=1/]

To delete the document, use the [delete API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-delete):

```console
DELETE /.ds-my-data-stream-2099.03.08-000003/_doc/bfspvnIBr7VVZlfp2lqX
```
%  TEST[setup:my_index]
%  TEST[s/.ds-my-data-stream-2099.03.08-000003/my-index-000001/]
%  TEST[s/bfspvnIBr7VVZlfp2lqX/1/]

To delete or update multiple documents with a single request, use the [bulk API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk)'s `delete`, `index`, and `update` actions. For `index` actions, include valid [`if_seq_no` and `if_primary_term`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk#bulk-optimistic-concurrency-control) arguments.

```console
PUT /_bulk?refresh
{ "index": { "_index": ".ds-my-data-stream-2099.03.08-000003", "_id": "bfspvnIBr7VVZlfp2lqX", "if_seq_no": 0, "if_primary_term": 1 } }
{ "@timestamp": "2099-03-08T11:06:07.000Z", "user": { "id": "8a4f500d" }, "message": "Login successful" }
```
%  TEST[setup:my_index]
%  TEST[s/.ds-my-data-stream-2099.03.08-000003/my-index-000001/]
%  TEST[s/bfspvnIBr7VVZlfp2lqX/1/]

