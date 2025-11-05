---
navigation_title: ML-nodes vs EIS
applies_to:
  stack: ga
  serverless: ga
  deployment:
    self: unavailable
---

# Using ML-nodes or Elastic {{infer-cap}} Service (EIS) [ml-nodes-vs-eis]

## When to use EIS?

The Elastic Inference Service (EIS) requires zero setup or management. It's always-on, has excellent ingest throughput, and uses simple token-based billing.

Use EIS if you're getting started with [semantic search](./solutions/search/semantic-search.md) or [hybrid search](./solutions/search/hybrid-search-md) and want a smooth experience. Under the hood, EIS uses GPUs for ML {{infer}}, which are more efficient and allow a faster, more cost-effective experience for most usecases.

## When to use {{ml}} nodes?

ML nodes are a more configurable solution than EIS where you can set up specific nodes using CPUs to execute [ML {{infer}}]((./explore-analyze/elastic-inference/inference-api.md)). {{ml-cap}} nodes tend to incur higher costs but give more control.

Use ML nodes if you want to decide how your models run, you want to run custom models, or you have a self-managed setup.

## How do I switch from using ML nodes to EIS on an existing index?

```{applies_to}
stack: ga 9.3
serverless: ga
```

```console
PUT /my-ml-node-index/_mapping
{
  "properties": {
    "text": {
      "type": "semantic_text",
      "inference_id": ".elser-2-elastic"
    }
  }
}
```

You can also switch an EIS-based index to use ML nodes:

```console
PUT /my-eis-index/_mapping
{
  "properties": {
    "text": {
      "type": "semantic_text",
      "inference_id": ".elser-2-elasticsearch"
    }
  }
}
```
