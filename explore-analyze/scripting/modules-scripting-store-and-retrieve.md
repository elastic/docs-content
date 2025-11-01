---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Store and retrieve scripts [script-stored-scripts]

You can store and retrieve scripts from the cluster state using the [stored script APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-script). Stored scripts allow you to reference shared scripts for operations like scoring, aggregating, filtering, and reindexing. Instead of embedding scripts inline in each query, you can reference these shared operations.

Stored scripts can also reduce request payload size. Depending on script size and request frequency, this can help lower latency and data transfer costs.

::::{note}
Unlike regular scripts, stored scripts require that you specify a script language using the `lang` parameter.
::::


To create a script, use the [create stored script API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-put-script). For example, the following request creates a stored script named `calculate-score`.

```console
POST _scripts/calculate-score
{
  "script": {
    "lang": "painless",
    "source": "Math.log(_score * 2) + params['my_modifier']"
  }
}
```

You can retrieve that script by using the [get stored script API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-get-script).

```console
GET _scripts/calculate-score
```

To use the stored script in a query, include the script `id` in the `script` declaration:

```console
GET my-index-000001/_search
{
  "query": {
    "script_score": {
      "query": {
        "match": {
            "message": "some message"
        }
      },
      "script": {
        "id": "calculate-score", <1>
        "params": {
          "my_modifier": 2
        }
      }
    }
  }
}
```

1. `id` of the stored script


To delete a stored script, submit a [delete stored script API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-delete-script) request.

```console
DELETE _scripts/calculate-score
```
