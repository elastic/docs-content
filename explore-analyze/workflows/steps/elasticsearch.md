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
| `elasticsearch.delete` | `DELETE /<index>/_doc/<id>` ([Delete a document]({{es-apis}}operation/operation-delete)) |
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

### Example: Delete a document

The `elasticsearch.delete` action deletes a single document by its ID. The `index` and `id` parameters are used to construct the API path.

```yaml
steps:
  - name: delete_a_doc
    type: elasticsearch.delete
    with:
      index: "my-index"
      id: "document_id_123"
```

### Example: Bulk indexing

The `elasticsearch.bulk` action performs multiple indexing or delete operations in a single request. The `body` parameter must be a string containing the bulk operations in newline-delimited JSON (NDJSON) format. Each operation requires an action/metadata line followed by an optional source document line.

```yaml
steps:
  - name: bulk_index_data
    type: elasticsearch.bulk
    with:
      index: "national-parks-data"
      body: |
        { "index": { "_id": "1" } } <1>
        { "name": "Yellowstone National Park", "category": "geothermal" } <2>
        { "index": { "_id": "2" } } <1>
        { "name": "Grand Canyon National Park", "category": "canyon" } <2>
```
1. **Action/metadata line**: Specifies the action and document ID
2. **Source document line**: The document data 

## Generic request actions

For advanced use cases or for accessing [{{es}} APIs]({{es-apis}}) that do not have a named action, use the generic `elasticsearch.request` type. This gives you full control over the HTTP request.

::::{note}
We recommend using named actions whenever possible. They are more readable and provide a stable interface for common operations.
::::

Use the following parameters in the `with` block to configure the request:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `method` | No (defaults to `GET`) | The HTTP method (`GET`, `POST`, `PUT`, or `DELETE`) |
| `path` | Yes | The API endpoint path (for example, `/_search`, `/_cluster/health`) |
| `body` | No | The JSON request body |
| `query` | No | An object representing URL query string parameters |

### Example: Get cluster health

This example uses the generic request to call the `GET /_cluster/health` endpoint ([Get cluster health]({{es-apis}}operation/operation-health-report)).

```yaml
steps:
  - name: get_cluster_health
    type: elasticsearch.request
    with:
      method: GET
      path: /_cluster/health
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
        type: elasticsearch.delete
        with:
          # The 'item' variable holds the current document from the loop
          index: "{{ item._index }}"
          id: "{{ item._id }}"
```

Key concepts in this example:

* [Data flow](/explore-analyze/workflows/data.md#workflows-data-flow): The output of the `search_for_docs` step is available to subsequent steps at `steps.search_for_docs.output`.
* [Foreach loop](/explore-analyze/workflows/steps/foreach.md): The `foreach` step iterates over the `hits.hits` array from the search results.
* [Item variable](/explore-analyze/workflows/data/templating.md): Inside the loop, the `item` variable holds the current document being processed, allowing you to access its fields such as `item._index` and `item._id`.
