---
navigation_title: Multimodal search
description: Search images with text and run cross-modal retrieval in Elasticsearch using multimodal embeddings, Jina models, and the semantic field type.
applies_to:
  stack: planned
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---
# Multimodal search [multimodal-search]

Multimodal search finds results by meaning across more than one content type. Common use cases include text-to-image product search, finding similar images, searching media libraries by natural language, and retrieving screenshots or document pages with text or image queries.

Multimodal search builds on [vector search](vector.md). A multimodal embedding model maps each supported input into a dense vector so content with similar meaning is nearby in vector space, even when the media types differ.

:::{tip}
For a hands-on walkthrough, refer to [Build multimodal search with a semantic field](multimodal-search/multimodal-search-tutorial.md).
:::

## How it works [how-multimodal-search-works]

Multimodal embedding models map different media types into a **shared vector space**. Text, images, and other supported modalities (such as audio, video, or PDF, depending on the model) become dense vectors that live in the same space. That shared space is what makes cross-modal retrieval possible: a text query can match an image embedding, and an image query can match text or other images.

Use the same model (and compatible endpoint settings) at ingest and at search time. Mixing models breaks similarity comparisons because the vector spaces are not interchangeable.

In {{es}}, the model is exposed through an {{infer}} endpoint that uses the `embedding` task type. The endpoint determines which modalities you can index and query.

:::{note}
The `embedding` task type does not guarantee that every endpoint supports every modality. Check the model and service documentation to determine the modalities supported. Refer to [Multimodal embedding models](#multimodal-embedding-models) for the list of multimodal embedding models supported by {{es}}.
:::

## Use cases [multimodal-search-use-cases]

Common multimodal search use cases include:

**Product and catalog visual search**
:   Shoppers describe an item in natural language ("leather crossbody bag with gold zipper") and retrieve matching product photos, even when titles and tags are incomplete. Combine with [filters](multimodal-search/multimodal-search-tutorial.md#multimodal-tutorial-filters) for price, brand, or availability.

**Similar-image and reverse image search**
:   A user uploads a photo or selects an existing asset and finds visually similar products, duplicates, or near-duplicates in a catalog or media library.

**Digital asset management**
:   Search large image and media collections by meaning instead of filenames or manual tags. For example, find campaign assets that match a brief written in plain language.

**Multilingual text-to-image search**
:   Query an image index in one language and retrieve the same visual results you would get in another, when the embedding model is trained for multilingual text-image matching.

**PDF and document-page search**
:   Embed document pages (or PDFs) so queries can match layout and visual content (diagrams, tables, scanned pages), not only extracted plain text.

**Multimodal retrieval for RAG**
:   Retrieve images, charts, or document pages alongside text passages so a downstream generative model can ground answers in visual evidence as well as prose.


## Multimodal embedding models [multimodal-embedding-models]

Compare the multimodal embedding models available with {{es}}:

| Model | Channel | Modalities | Dimensions | Context / input limit | Task type | Best for |
| --- | --- | --- | --- | --- | --- | --- |
| [`jina-embeddings-v5-omni-small`](https://jina.ai/models/jina-embeddings-v5-omni-small/) | EIS (also Jina API / marketplaces / on-prem) | Text, image, video, audio, PDF/file | 1024 | Up to 32K tokens | `embedding` | Default multimodal retrieval across media types; preconfigured as `.jina-embeddings-v5-omni-small` |
| [`jina-embeddings-v5-omni-nano`](https://jina.ai/models/jina-embeddings-v5-omni-nano/) | EIS (also Jina API / marketplaces / on-prem) | Text, image, video, audio, PDF/file | 768 | Up to 8K tokens | `embedding` | Lower-cost / lower-resource multimodal workloads |
| [`jina-clip-v2`](https://jina.ai/models/jina-clip-v2/) | EIS (also Jina API / marketplaces / on-prem) | Text, image | 1024 | Up to 8K tokens | `embedding` | Focused text↔image search, including multilingual text-to-image |
| [`jina-embeddings-v4`](https://jina.ai/models/jina-embeddings-v4/) | External JinaAI / marketplaces / on-prem (not on EIS) | Text, image, PDF | 2048 (default; optional `dimensions` via JinaAI service settings) | Up to 32K tokens | `embedding` | External or self-hosted multimodal embeddings when you connect through the JinaAI service |

For the full Jina catalog, deployment matrix, and input examples, refer to [Jina models](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md). For EIS availability by stack version, refer to [Supported models on EIS](/explore-analyze/elastic-inference/eis-supported-models.md).

You can deploy or access Jina multimodal models in these ways:

- **[Elastic {{infer-cap}} Service (EIS)](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-omni-getting-started)**: Elastic hosts the model. Use this when you want managed {{infer}} without provisioning ML nodes.
- **[Jina API](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-external)**: The model runs on the hosted Jina platform. Use this when you want Jina-hosted {{infer}} outside EIS.
- **[On-prem](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-on-prem)**: You run the model in Docker on your own infrastructure. Use this for air-gapped, offline, or compliance scenarios.

## Use the `semantic` field type [semantic-field-for-multimodal-search]

The `semantic` field type is the simplest way to run multimodal search in {{es}}. For field parameters, defaults, supported input types, and limitations, refer to the [`semantic` field documentation](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field.md).

The `semantic` field type simplifies semantic and multimodal search across text, images, audio, video, and PDF files. With a compatible multimodal embedding model, you can search from any supported input type to any other supported input type. The field automatically:

- Generates embeddings when you index field values, without an ingest pipeline or inference processor.
- Splits long text into smaller passages, called chunks.
- Indexes the generated embeddings using default index options that optimize for common use cases.
- Searches the embeddings generated for each value or text chunk.

Here's an example using the Jina Embeddings v5 Omni Small endpoint:

```json
PUT my-multimodal-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "semantic",
        "inference_id": ".jina-embeddings-v5-omni-small"
      }
    }
  }
}
```

Multiple `semantic` fields can share one {{infer}} endpoint. For example, one field for images and another for descriptions; you can then search either field or both.


## Next steps [multimodal-search-next-steps]

- [Build multimodal search with a `semantic` field](multimodal-search/multimodal-search-tutorial.md): Index images and search them with text, image, and PDF input
- [`semantic` field type](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field.md): Mapping overview and comparison guidance
- [Jina models](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md): Model catalog, deployment options, and input formats
- [Elastic {{infer-cap}} Service](/explore-analyze/elastic-inference/eis.md): Hosted {{infer}} without managing ML nodes
- [{{infer}} API](/explore-analyze/elastic-inference/inference-api.md): Create and manage {{infer}} endpoints
