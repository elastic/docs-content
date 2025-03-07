---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Index action"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/actions-index.html
---

# Index action [actions-index]

Use the `index` action to index data into Elasticsearch. See [Index action attributes](#index-action-attributes) for the supported attributes.

## Configuring index actions [_configuring_index_actions]

The following snippet shows a simple `index` action definition:

```js
"actions" : {
  "index_payload" : { <1>
    "condition": { ... }, <2>
    "transform": { ... }, <3>
    "index" : {
      "index" : "my-index-000001", <4>
      "doc_id": "my-id" <5>
    }
  }
}
```

1. The id of the action
2. An optional [condition](condition.md) to restrict action execution
3. An optional [transform](transform.md) to transform the payload and prepare the data that should be indexed
4. The index, alias, or data stream to which the data will be written
5. An optional `_id` for the document
%  NOTCONSOLE

## Index action attributes [index-action-attributes]

| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `index` | yes* | - | The index, alias, or data stream to index into. Date math expressions like `<my-index-{now/d}>` are also supported.<br><br>*If you dynamically set an `_index` value, this parameter isn’t required. See [Multi-document support](#anatomy-actions-index-multi-doc-support).<br> |
| `doc_id` | no | - | The optional `_id` of the document. |
| `op_type` | no | `index` | The [op_type](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-create) for the index operation.                                                      Must be one of either `index` or `create`. Must be `create` if                                                      `index` is a data stream. |
| `execution_time_field` | no | - | The field that will store/index the watch execution                                                      time. |
| `timeout` | no | 60s | The timeout for waiting for the index api call to                                                      return. If no response is returned within this time,                                                      the index action times out and fails. This setting                                                      overrides the default timeouts. |
| `refresh` | no | - | Optional setting of the [refresh policy](elasticsearch://reference/elasticsearch/rest-apis/refresh-parameter.md)                                                      for the write request |

## Multi-document support [anatomy-actions-index-multi-doc-support]

Like with all other actions, you can use a [transform](transform.md) to replace the current execution context payload with another and by that change the document that will end up indexed.

The index action plays well with transforms with its support for the special `_doc` payload field.

When resolving the document to be indexed, the index action first looks up for a `_doc` field in the payload. When not found, the payload is indexed as a single document.

When a `_doc` field exists, if the field holds an object, it is extracted and indexed as a single document. If the field holds an array of objects, each object is treated as a document and the index action indexes all of them in a bulk.

An `_index`, or `_id` value can be added per document to dynamically set the index and ID of the indexed document.

The following snippet shows a multi-document `index` action definition:

```js
"actions": {
  "index_payload": {
    "transform": {
      "script": """
      def documents = ctx.payload.hits.hits.stream()
        .map(hit -> [
          "_index": "my-index-000001", <1>
          "_id": hit._id, <2>
          "severity": "Sev: " + hit._source.severity <3>
        ])
        .collect(Collectors.toList());
      return [ "_doc" : documents]; <4>
      """
    },
    "index": {} <5>
  }
}
```

1. The document’s index
2. An optional `_id` for the document
3. A new `severity` field derived from the original document
4. The payload `_doc` field which is an array of documents
5. Since the `_index` was informed per document this should be empty
%  NOTCONSOLE