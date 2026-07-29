---
navigation_title: Multimodal search with Jina embeddings
description: Step-by-step tutorial for multimodal search with the semantic field type and Jina embeddings in Elasticsearch, from mapping through indexing to cross-modal queries.
applies_to:
  stack: planned
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
type: tutorial
---

# Multimodal search with Jina embeddings [multimodal-search-tutorial]

Multimodal search lets you retrieve content by meaning across text, images, and other media types in one index. This tutorial walks you through a recommended workflow that uses the [`semantic`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field.md) field type with [Jina multimodal embedding models](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-multimodal-embeddings) on [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md).

By the end, you will be able to:

- Map a `semantic` field to a Jina multimodal {{infer}} endpoint
- Index text and image content that {{es}} embeds automatically
- Run text and image queries against the same vector space

:::{tip}
Jina multimodal models are the recommended path for multimodal search in {{es}}. For deployment options (EIS, external {{infer}}, and on-prem) and an overview of the workflow, refer to [Multimodal search](../multimodal-search.md).

If you work with text only, use [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) instead. To compare the two field types, refer to [Should I use `semantic_text` or `semantic`?](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field.md#should-i-use-semantictext-or-semantic).
:::

## How this workflow fits together [multimodal-tutorial-overview]

A multimodal embedding model maps different content types into one shared vector space. After you embed catalog items with that model:

- A text query such as "red running shoes" can return product images
- An image query can return related product descriptions or similar images

The `semantic` field type handles embedding generation, text chunking, and vector storage for you. You must provide an {{infer}} endpoint that uses the `embedding` task type. Use the same endpoint for ingest and search so similarity scores stay meaningful.

This tutorial uses the preconfigured `.jina-embeddings-v5-omni-small` endpoint. For lower cost or smaller deployments, you can substitute `.jina-embeddings-v5-omni-nano` or create your own endpoint for `jina-embeddings-v5-omni-nano`.

## Requirements [multimodal-tutorial-requirements]

- A running {{es}} cluster that supports the `semantic` field type. For the fastest start, [create a serverless project](/deploy-manage/deploy/elastic-cloud/create-serverless-project.md).
- Access to [Elastic {{infer-cap}} Service](/explore-analyze/elastic-inference/eis.md). EIS is available on {{ech}} and {{serverless-short}}. You can also [connect a self-managed cluster to EIS](/explore-analyze/elastic-inference/connect-self-managed-cluster-to-eis.md).
- Sample image bytes encoded as a base64 data URI when you try the image examples. Use a small PNG or JPEG from your own files.

:::{tip}
To run the `curl` examples in this tutorial, set the following environment variables:
```bash
export ELASTICSEARCH_URL="your-elasticsearch-url"
export API_KEY="your-api-key"
```
To generate API keys, search for `API keys` in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md). [Learn more about finding your endpoint and credentials](/solutions/elasticsearch-solution-project/search-connection-details.md).
:::

## Create the index mapping [multimodal-tutorial-index-mapping]

Create an index with a `semantic` field that points at a Jina multimodal endpoint. Unlike text-only workflows, a `semantic` field has no default {{infer}} endpoint. You must set `inference_id` to an endpoint that uses the `embedding` task type.

```console
PUT multimodal-catalog
{
  "mappings": {
    "properties": {
      "title": {
        "type": "keyword"
      },
      "modality": {
        "type": "keyword"
      },
      "content": {
        "type": "semantic",
        "inference_id": ".jina-embeddings-v5-omni-small"
      }
    }
  }
}
```

1. Metadata fields help you filter results after retrieval.
2. The `semantic` field stores the input and its embeddings.
3. `.jina-embeddings-v5-omni-small` is the preconfigured EIS endpoint for the Jina omni small model. The endpoint determines which input modalities the field supports.

:::{dropdown} Example response
```console-result
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "multimodal-catalog"
}
```
:::

:::{note}
To create a custom endpoint instead of using the preconfigured ID, refer to [Jina multimodal models on EIS](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-omni-getting-started), then set `inference_id` to your endpoint ID.
:::

## Index text [multimodal-tutorial-index-text]

Index documents with text in the `semantic` field. {{es}} sends the field value to the {{infer}} endpoint, generates embeddings, and stores them.

```console
POST _bulk
{ "index": { "_index": "multimodal-catalog", "_id": "text-1" } }
{ "title": "Trail runner", "modality": "text", "content": "Lightweight red running shoes designed for rocky trails and long distance training." }
{ "index": { "_index": "multimodal-catalog", "_id": "text-2" } }
{ "title": "City sneaker", "modality": "text", "content": "Minimal white sneakers for everyday walking and travel." }
{ "index": { "_index": "multimodal-catalog", "_id": "text-3" } }
{ "title": "Kitchen guide", "modality": "text", "content": "How to cook ramen noodles with a miso broth and soft boiled eggs." }
```

When indexing finishes, the embeddings are already stored. You do not need an ingest pipeline or {{infer}} processor.

## Index images [multimodal-tutorial-index-images]

Index image content in the same `semantic` field. Provide non-text input as an object with `type`, `format`, and a base64 data URL in `value`. The multimodal model embeds the image into the same vector space as the text documents.

```console
PUT multimodal-catalog/_doc/img-1
{
  "title": "red-running-shoes.png",
  "modality": "image",
  "content": {
    "type": "image",
    "format": "base64",
    "value": "data:image/png;base64,<BASE64_IMAGE_DATA>"
  }
}
```

Replace `<BASE64_IMAGE_DATA>` with your image bytes. Keep the `data:image/png;base64,` prefix, or use `data:image/jpeg;base64,` for JPEG files.

:::{tip}
The same object shape works for other modalities supported by the model. Set `type` to `audio`, `video`, or `pdf`, and use the matching data URL media type. For more input examples, refer to [Multimodal embedding models on EIS](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-omni-getting-started). Prefer short video clips over long videos so each embedding represents a focused piece of content.
:::

## Search across modalities [multimodal-tutorial-search]

You now have text and image embeddings produced by the same model and stored through the same `semantic` field. That shared space is what makes cross-modal search possible.

### Text query [multimodal-tutorial-text-query]

Search with a `match` query on the `semantic` field. A text query can retrieve both text documents and images that are close in meaning.

```console
GET multimodal-catalog/_search
{
  "query": {
    "match": {
      "content": {
        "query": "red running shoes for trails"
      }
    }
  }
}
```

The trail runner text document and the red running shoes image should rank above the ramen guide, even when the query does not share many exact keywords with the indexed content.

### Image query [multimodal-tutorial-image-query]

For image-to-image or image-to-text search, use a `knn` query with an `embedding` query vector builder. {{es}} uses the {{infer}} endpoint from the `semantic` field mapping to embed the query image.

```console
GET multimodal-catalog/_search
{
  "query": {
    "knn": {
      "field": "content",
      "k": 5,
      "num_candidates": 50,
      "query_vector_builder": {
        "embedding": {
          "input": {
            "type": "image",
            "format": "base64",
            "value": "data:image/png;base64,<BASE64_IMAGE_DATA>"
          }
        }
      }
    }
  }
}
```

Replace `<BASE64_IMAGE_DATA>` with the image you want to search with.

:::{tip}
For a fuller image-focused walkthrough with sample NASA images, text, image, and PDF queries, refer to [Build multimodal search with a `semantic` field](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field-quickstart.md).
:::

## Combine filters with multimodal retrieval [multimodal-tutorial-filters]

Vector similarity alone can return items outside the scope the user can buy or view. Add structured filters on metadata fields such as category, license, or modality.

```console
GET multimodal-catalog/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "content": {
              "query": "red running shoes for trails"
            }
          }
        }
      ],
      "filter": [
        {
          "term": {
            "modality": "image"
          }
        }
      ]
    }
  }
}
```

This example keeps only image documents while still ranking them by multimodal similarity to the text query.

## Next steps [multimodal-tutorial-next-steps]

- [Multimodal search](../multimodal-search.md): Concepts, deployment options, and recommended Jina models
- [`semantic` field type](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field.md): Mapping reference, parameters, and limitations
- [Should I use `semantic_text` or `semantic`?](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field.md#should-i-use-semantictext-or-semantic): Choose the right inference field type
- [Jina models](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md): Full model catalog and input examples
- [Optimize dense vector storage](../vector/vector-storage-for-semantic-search.md): Quantization options such as BBQ for large multimodal catalogs
