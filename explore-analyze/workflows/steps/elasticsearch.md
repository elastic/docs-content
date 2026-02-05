---
navigation_title: Elasticsearch
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn about Elasticsearch action steps for searching, indexing, and managing data in workflows.
---

# {{es}} action steps

{{es}} actions are built-in steps that allow your workflows to interact directly with {{es}} APIs. You can search, index, update, and delete documents, manage indices, and perform any other operation supported by the {{es}} REST API.

All {{es}} actions are automatically authenticated using the permissions or API key of the user executing the workflow.

There are two ways to use {{es}} actions:

* [Named actions](#named-actions): Structured actions that map directly to specific {{es}} API endpoints
* [Generic request actions](#generic-request-actions): Actions that provide full control over the HTTP request for advanced use cases

## Named actions

Named actions provide a structured way to call specific {{es}} endpoints. The action type maps directly to the {{es}} API. 

To view the available named actions, click **Actions menu** and select **{{es}}**. For operations that are not available as a named action, use the [generic request action](#generic-request-actions).

The following table shows some examples:

| Action type | {{es}} operation |
|-------------|--------------|
| `elasticsearch.search` | `POST /<index>/_search` ([Run a search]({{es-apis}}operation/operation-search)) |
| `elasticsearch.update` | `POST /<index>/_update/<id>` ([Update a document]({{es-apis}}operation/operation-delete)) |
| `elasticsearch.indices.create` | `PUT /<index>` ([Create an index]({{es-apis}}operation/operation-indices-create))  |

The parameters you provide in the `with` block are passed as the body or query parameters of the API request. The following examples demonstrate common use cases.

### Example: Search for documents

The `elasticsearch.search` action searches for documents in the specified index. The `query` parameter is passed directly to the [Run a search API]({{es-apis}}operation/operation-search).

```yaml
steps:
  - name: search_for_alerts
    type: elasticsearch.search
    with:
      index: ".alerts-security.attack.discovery*"
      query:
        bool:
          filter:
            - term:
                kibana.alert.severity: "critical"
```

### Example: Update a document

The `elasticsearch.update` action partially updates a document by its ID. The `doc` parameter specifies the fields to add or modify.

```yaml
steps:
  - name: addMetadata
    type: elasticsearch.update
    with:
      index: national-parks-index
      id: "{{ foreach.item._id }}"
      doc:
        last_processed: "{{ execution.startedAt }}"
        workflow_run: "{{ execution.id }}"
        category_uppercase: "{{ foreach.item._source.category | upcase }}"
```

### Example: Create an index

The `elasticsearch.indices.create` action creates a new index with optional settings and mappings.

```yaml
  - name: create_parks_index
    type: elasticsearch.indices.create
    with:
      index: "{{ consts.indexName }}"
      mappings:
        properties:
          name: { type: text }
          category: { type: keyword }
          description: { type: text }
```

## Generic request actions

For advanced use cases or for accessing [{{es}} APIs]({{es-apis}}) that do not have a named action, use the generic `elasticsearch.request` type. This gives you full control over the HTTP request.

::::{note}
We recommend using named actions whenever possible. They are more readable and provide a stable interface for common operations.
::::

Use the following parameters in the `with` block to configure the request:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `method` | No (defaults to `GET`) | The HTTP method (`GET`, `POST`, `PUT`, or `DELETE`) |
| `path` | Yes | The API endpoint path (for example, `/_search`, `/_data_stream/<name>`) |
| `body` | No | The JSON request body |
| `query` | No | An object representing URL query string parameters |

### Example: Get data stream

This example uses the generic request to call the `GET /_data_stream/<name>` endpoint ([Get data stream]({{es-apis}}operation/operation-indices-get-data-stream)).

```yaml
steps:
  - name: get_data_stream
    type: elasticsearch.request
    with:
      method: GET
      path: /_data_stream/my-data-stream
```

### Example: Delete documents by query

This example uses the generic request to call the `POST /<index>/_delete_by_query` endpoint ([Delete documents]({{es-apis}}operation/operation-delete-by-query)).

```yaml
steps:
  - name: delete_old_documents
    type: elasticsearch.request
    with:
      method: POST
      path: /my-index/_delete_by_query
      body:
        query:
          range:
            "@timestamp":
              lt: "now-30d"
```

## Combine actions

The following example demonstrates how to combine multiple {{es}} actions in a workflow. It searches for documents and then iterates over the results to delete each one.

```yaml
name: Search and Delete Documents
triggers:
  - type: manual
steps:
  - name: search_for_docs
    type: elasticsearch.search
    with:
      index: ".alerts-security.attack.discovery.alerts-default"
      query:
        term:
          host.name: "compromised-host"

  - name: delete_found_docs
    type: foreach
    # The search results are in steps.search_for_docs.output
    foreach: steps.search_for_docs.output.hits.hits
    steps:
      - name: delete_each_doc
        type: elasticsearch.request
        with:
          method: DELETE
          # The 'item' variable holds the current document from the loop
          path: "/{{ item._index }}/_doc/{{ item._id }}"
```

Key concepts in this example:

* [Data flow](/explore-analyze/workflows/data.md#workflows-data-flow): The output of the `search_for_docs` step is available to subsequent steps at `steps.search_for_docs.output`.
* [Foreach loop](/explore-analyze/workflows/steps/foreach.md): The `foreach` step iterates over the `hits.hits` array from the search results.
* [Item variable](/explore-analyze/workflows/data/templating.md): Inside the loop, the `item` variable holds the current document being processed, allowing you to access its fields such as `item._index` and `item._id`.
