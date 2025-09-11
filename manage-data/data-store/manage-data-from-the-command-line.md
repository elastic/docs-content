---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-working-with-elasticsearch.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-working-with-elasticsearch.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-enterprise
---

# Manage data from the command line

Learn how to index, update, retrieve, search, and delete documents in an {{es}} cluster from the command line.

::::{tip}
If you are looking for a user interface for {{es}} and your data, head on over to [Kibana](/get-started/the-stack.md)! Not only are there amazing visualization and index management tools, Kibana includes realistic sample data sets to play with so that you can get to know what you *could* do with your data.
::::

## Before you begin [before-you-begin]

On the **Overview** page for your new cluster in the Cloud UI, copy the {{es}} endpoint URL under **Endpoints**.

These examples use the `elastic` user. If you didn’t copy down the password for the `elastic` user, you can [reset the password](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).

To use these examples, you also need to have the [curl](http://curl.haxx.se/) command installed.


## Indexing [indexing]

To index a document into {{es}}, `POST` your document:

```bash
curl -u USER:PASSWORD https://<ELASTICSEARCH_URL>/my_index/_doc -XPOST -H 'Content-Type: application/json' -d '{
    "title": "One", "tags": ["ruby"]
}'
```

To show that the operation worked, {{es}} returns a JSON response that looks like `{"_index":"my_index","_type":"_doc","_id":"0KNPhW4BnhCSymaq_3SI","_version":1,"result":"created","_shards":{"total":2,"successful":2,"failed":0},"_seq_no":0,"_primary_term":1}`.

In this example, the index `my_index` is created dynamically when the first document is inserted into it. All documents in {{es}} have a `type` and an `id`, which is echoed as `"_type":"_doc"` and `_id":"0KNPhW4BnhCSymaq_3SI` in the JSON response. If no ID is specified during indexing, a random `id` is generated.


### Bulk indexing [bulk-indexing]

To achieve the best possible performance, use the bulk API.

To index some additional documents with the bulk API:

```bash
curl -u USER:PASSWORD https://<ELASTICSEARCH_URL>/my_index/_doc/_bulk -XPOST -H 'Content-Type: application/json' -d '
{"index": {}}
{"title": "Two", "tags": ["ruby", "python"] }
{"index": {}}
{"title": "Three", "tags": ["java"] }
{"index": {}}
{"title": "Four", "tags": ["ruby", "php"] }
'
```

Elasticsearch returns a JSON response similar to this one:

```json
{"took":694,"errors":false,"items":[{"index":{"_index":"my_index","_type":"_doc","_id":"0aNqhW4BnhCSymaqFHQn","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":0,"_primary_term":1,"status":201}},{"index":{"_index":"my_index","_type":"_doc","_id":"0qNqhW4BnhCSymaqFHQn","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":1,"_primary_term":1,"status":201}},{"index":{"_index":"my_index","_type":"_doc","_id":"06NqhW4BnhCSymaqFHQn","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":2,"_primary_term":1,"status":201}}]}
```


## Updating [updating]

To update an existing document in {{es}}, `POST` the updated document to `http://ELASTICSEARCH_URL/my_index/_doc/ID`, where the ID is the `_id` of the document.

For example, to update the last document indexed from the previous example with `"_id":"06NqhW4BnhCSymaqFHQn"`:

```bash
curl -u USER:PASSWORD https://<ELASTICSEARCH_URL>/my_index/_doc/06NqhW4BnhCSymaqFHQn -XPOST -H 'Content-Type: application/json' -d '{
    "title": "Four updated", "tags": ["ruby", "php", "python"]
}'
```

The JSON response shows that the version counter for the document got incremented to `_version":2` to reflect the update.


## Retrieving documents [retrieving-documents]

To take a look at a specific document you indexed, here the last document we updated with the ID `0KNPhW4BnhCSymaq_3SI`:

```bash
curl -u USER:PASSWORD https://<ELASTICSEARCH_URL>/my_index/_doc/06NqhW4BnhCSymaqFHQn
```

This request didn’t include `GET`, as the method is implied if you don’t specify anything else. If the document you are looking for exists, {{es}} returns `found":true` along with the document as part of the JSON response. Otherwise, the JSON response contains `"found":false`.


## Searching [searching]

You issue search requests for documents with one of these {{es}} endpoints:

```bash
https://<ELASTICSEARCH_URL>/_search
https://<ELASTICSEARCH_URL>/INDEX_NAME/_search
```

Either a `GET` or a `POST` request with some URI search parameters works, or omit the method to default to `GET` request:

```bash
curl -u USER:PASSWORD https://<ELASTICSEARCH_URL>/my_index/_doc/_search?q=title:T*
```

For an explanation of the allowed parameters, check [URI Search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search).

To make {{es}} return a more human readable JSON response, add `?pretty=true` to the request:

```bash
curl -u USER:PASSWORD https://<ELASTICSEARCH_URL>/my_index/_doc/_search?pretty=true -H 'Content-Type: application/json' -d '{
    "query": {
        "query_string": {"query": "*"}
    }
}'
```

For performance reasons, `?pretty=true` is not recommended in production. You can verify the performance difference yourself by checking the `took` field in the JSON response which tells you how long Elasticsearch took to evaluate the search in milliseconds. When we tested these examples ourselves, the difference was `"took" : 4` against `"took" : 18`, a substantial difference.

For a full explanation of how the request body is structured, check [Elasticsearch Request Body documentation](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json). You can also execute multiple queries in one request with the [Multi Search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch).


## Deleting [deleting]

You delete documents from {{es}} by sending `DELETE` requests.

To delete a single document by ID from an earlier example:

```bash
curl -u USER:PASSWORD https://<ELASTICSEARCH_URL>/my_index/_doc/06NqhW4BnhCSymaqFHQn -XDELETE
```

To delete a whole index, here `my_index`:

```bash
curl -u USER:PASSWORD https://<ELASTICSEARCH_URL>/my_index -XDELETE
```

The JSON response returns `{"acknowledged":true}` to indicate that the index deletion was a  success.

