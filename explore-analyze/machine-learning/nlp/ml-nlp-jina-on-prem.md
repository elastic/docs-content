---
navigation_title: Deploy on-prem
description: Deploy Jina embedding, reranker, and reader models on your own infrastructure using jina-on-prem and connect them to Elasticsearch through inference endpoints.
applies_to:
  stack: ga
  deployment:
    self: ga
products:
  - id: machine-learning
---

# Deploy Jina models on-prem [ml-nlp-jina-on-prem]

In on-prem environments, Jina models are not available through [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md) because EIS requires external network connectivity. Instead, deploy them locally using [jina-on-prem](https://github.com/jina-ai/jina-on-prem), Elastic's toolkit for self-hosted Jina models. For deployment guides and troubleshooting, refer to the [jina-on-prem documentation](https://github.com/jina-ai/jina-on-prem/wiki).

{{infer-cap}} runs in Docker containers on your network, not on {{ml}} nodes inside the cluster. {{es}} calls the local containers through {{infer}} endpoints.

For pricing and licensing, refer to [Jina on-prem](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-pricing-on-prem) on the Jina models page.

## Prerequisites [jina-on-prem-prerequisites]

Before you deploy Jina models on-prem, ensure you have:

* Docker installed on the host that runs the models
* Access to GitHub Container Registry (GHCR) to pull prebuilt images, or a `.tar.gz` image bundle transferred to your environment
* A GitHub personal access token with `read:packages` scope if you pull images from GHCR
* (Optional) An NVIDIA GPU with CUDA 12.1+ and the NVIDIA Container Toolkit for GPU images

## Get started with jina-on-prem [jina-on-prem-getting-started]

1. On a machine with network access, pull or bundle a prebuilt Docker image. Refer to the [jina-on-prem Quick Start](https://github.com/jina-ai/jina-on-prem/wiki/Quick-Start).
2. Transfer the image to your on-prem host if required, then load and run it:

   ```bash
   docker load < jina-v5-nano.tar.gz
   docker run -d --name jina-nano -p 8080:8080 \
     ghcr.io/jina-ai/jina-on-prem/jina-embeddings-v5-text-nano:cpu
   ```

3. Create {{infer}} endpoints in {{es}} that point to the local server. Refer to [Connect {{es}} to a local jina-on-prem server](#jina-on-prem-elasticsearch-integration).

For end-to-end deployment patterns, model selection, and troubleshooting, refer to the [jina-on-prem documentation](https://github.com/jina-ai/jina-on-prem/wiki).

## Connect {{es}} to a local jina-on-prem server [jina-on-prem-elasticsearch-integration]

Create a `text_embedding` endpoint that uses the OpenAI-compatible API exposed by jina-on-prem:

```console
PUT _inference/text_embedding/jina-embed
{
  "service": "openai",
  "service_settings": {
    "url": "http://embed-host:8080/v1/embeddings",
    "model_id": "jina-embeddings-v5-text-small",
    "api_key": "not-needed"
  }
}
```

Create a `rerank` endpoint that uses the Cohere-compatible API:

```console
PUT _inference/rerank/jina-rerank
{
  "service": "cohere",
  "service_settings": {
    "url": "http://rerank-host:8081/v1/rerank",
    "model_id": "jina-reranker-v3",
    "api_key": "not-needed"
  }
}
```

The `api_key` value is required by the {{infer}} API schema but is not validated by jina-on-prem.

You can reference the `inference_id` of these endpoints in index mappings for the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type, {{infer}} processors, or search queries.

For more endpoint configuration examples, refer to the [jina-on-prem API reference](https://github.com/jina-ai/jina-on-prem/wiki/API-Reference#elasticsearch-integration).
