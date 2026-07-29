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

Multimodal search finds results by meaning across more than one content type. In {{es}}, a common use case is **text-to-image search**: you index product photos, screenshots, or media assets, then retrieve matching images with a natural-language query such as "red running shoes on a white background" from a single index.

You can also query with an image to find related text or visually similar images, when the model and endpoint support those inputs.

Multimodal search builds on [vector search](vector.md). A multimodal embedding model maps each supported input into a dense vector so content with similar meaning is nearby in vector space, even when the media types differ.

:::{tip}
For a hands-on walkthrough, refer to [Multimodal search with Jina embeddings](multimodal-search/multimodal-search-tutorial.md) or the [`semantic` field quickstart](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field-quickstart.md).
:::

## How it works [how-multimodal-search-works]

Multimodal embedding models map different media types into a **shared vector space**. Text, images, and other supported modalities (such as audio, video, or PDF, depending on the model) become dense vectors that live in the same space. That shared space is what makes cross-modal retrieval possible: a text query can match an image embedding, and an image query can match text or other images.

At a high level:

1. At **ingest**, each piece of content is embedded with a multimodal model and the resulting vectors are stored in {{es}}.
2. At **search**, the query is embedded with the **same model**, then nearest-neighbor / semantic retrieval returns documents whose vectors are closest to the query vector.

Use the same model (and compatible endpoint settings) at ingest and at search time. Mixing models breaks similarity comparisons because the vector spaces are not interchangeable.

In {{es}}, the model is exposed through an {{infer}} endpoint that uses the `embedding` task type. The endpoint determines which modalities you can index and query.

:::{note}
The `embedding` task type does not guarantee that every endpoint supports every modality. Check the model and service documentation to determine the modalities supported.
:::

## Use cases [multimodal-search-use-cases]

These are common multimodal search patterns users build with {{es}}:

**Product and catalog visual search**
:   Shoppers describe an item in natural language ("leather crossbody bag with gold zipper") and retrieve matching product photos, even when titles and tags are incomplete. Combine with filters for price, brand, or availability.

**Similar-image and reverse image search**
:   A user uploads a photo or selects an existing asset and finds visually similar products, duplicates, or near-duplicates in a catalog or media library.

**Digital asset management**
:   Search large image and media collections by meaning instead of filenames or manual tags. For example, find campaign assets that match a brief written in plain language.

**Screenshot and visual document retrieval**
:   Index screenshots, slides, charts, or UI captures, then retrieve them with text queries (or related images). Typical apps include support tickets, runbooks, design systems, and internal knowledge bases.

**Multilingual text-to-image search**
:   Query an image index in one language and retrieve the same visual results you would get in another, when the embedding model is trained for multilingual text-image matching.

**PDF and document-page search**
:   Embed document pages (or PDFs) so queries can match layout and visual content (diagrams, tables, scanned pages), not only extracted plain text.

**Multimodal retrieval for RAG**
:   Retrieve images, charts, or document pages alongside text passages so a downstream generative model can ground answers in visual evidence as well as prose.

## Ways to perform multimodal search in Elastic [ways-to-perform-multimodal-search]

To run multimodal search, you need:

1. A **model with multimodal embedding capability** for the media types you want to index and query
2. A way to **deploy or access that model** from {{es}} (EIS, external {{infer}}, or on-prem)
3. A mapping path that stores and queries the embeddings. The [`semantic`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field.md) field type is the simplest managed option (covered in the next section).

Elastic recommends [Jina multimodal embedding models](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-multimodal-embeddings) for this workflow. They are available through Elastic {{infer-cap}} Service (EIS) for managed hosting, and through the JinaAI external {{infer}} service or on-prem containers when you need another deployment path.

### Deployment channels [multimodal-deployment-channels]

#### Elastic {{infer-cap}} Service (EIS)

Elastic hosts selected multimodal models on managed GPUs. You create an {{infer}} endpoint with `"service": "elastic"` (or use a preconfigured endpoint) without managing ML nodes.

- [Elastic {{infer-cap}} Service](/explore-analyze/elastic-inference/eis.md)
- [Supported models on EIS](/explore-analyze/elastic-inference/eis-supported-models.md)
- [Jina multimodal models on EIS](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-omni-getting-started)

#### External {{infer}}

The model runs outside your cluster (for example on the hosted Jina API). You connect {{es}} with an {{infer}} endpoint that calls that service. For multimodal inputs (image, PDF, and other non-text modalities), use an endpoint that supports the `embedding` task type **and** non-text content. In the create-{{infer}}-endpoint API, the [JinaAI]({{es-apis}}operation/operation-inference-put-jinaai) service documents multimodal `embedding` (including a `multimodal_model` setting). The [OpenAI]({{es-apis}}operation/operation-inference-put-openai) service also lists an `embedding` task type, but that path is for text embeddings compatible with the `embedding` task; it does not accept non-text inputs for multimodal search.

- [{{infer}} API](/explore-analyze/elastic-inference/inference-api.md)
- [Create an {{infer}} endpoint]({{es-apis}}operation/operation-inference-put)
- [Create a JinaAI {{infer}} endpoint]({{es-apis}}operation/operation-inference-put-jinaai)
- [Jina API and external {{infer}}](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-external)

#### On-prem

You can run Jina models in Docker on your own infrastructure for air-gapped, offline, or compliance scenarios. Multimodal models can run on-prem through the Jina API schemas exposed by the container. **Native {{es}} {{infer}} integration on-prem is currently limited to text embedding models.** For multimodal models, call the on-prem Jina API from your application or pipeline, then index the resulting vectors in {{es}} (or use another supported access path).

- [Jina on-prem](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-on-prem)
- [Jina model overview](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-model-overview)

### Multimodal embedding models [multimodal-embedding-models]

The following table lists multimodal **embedding** options documented for use with {{es}}. Specs (dimensions, context limits, modalities) come from the Jina model catalog and EIS supported-models docs.

Among external {{infer}} integrations, the services that list an `embedding` task type include [JinaAI]({{es-apis}}operation/operation-inference-put-jinaai) and [OpenAI]({{es-apis}}operation/operation-inference-put-openai). **Multimodal (non-text) embedding through external {{infer}} is documented for JinaAI** (for example `jina-embeddings-v4` with multimodal request format). OpenAI's `embedding` task type is text-oriented: it does not accept image or other non-text inputs for cross-modal search. Other providers in the [create {{infer}} endpoint]({{es-apis}}operation/operation-inference-put) list typically expose `text_embedding` only. Some vendors offer multimodal models outside {{es}}; to use their vectors today you typically embed outside {{es}} and [bring your own dense vectors](vector/bring-own-vectors.md), or use a Jina / EIS multimodal endpoint with a `semantic` field.

| Model | Channel | Modalities | Dimensions | Context / input limit | Task type | Best for |
| --- | --- | --- | --- | --- | --- | --- |
| [`jina-embeddings-v5-omni-small`](https://jina.ai/models/jina-embeddings-v5-omni-small/) | EIS (also Jina API / marketplaces / on-prem) | Text, image, video, audio, PDF/file | 1024 | Up to 32K tokens | `embedding` | Default multimodal retrieval across media types; preconfigured as `.jina-embeddings-v5-omni-small` |
| [`jina-embeddings-v5-omni-nano`](https://jina.ai/models/jina-embeddings-v5-omni-nano/) | EIS (also Jina API / marketplaces / on-prem) | Text, image, video, audio, PDF/file | 768 | Up to 8K tokens | `embedding` | Lower-cost / lower-resource multimodal workloads |
| [`jina-clip-v2`](https://jina.ai/models/jina-clip-v2/) | EIS (also Jina API / marketplaces / on-prem) | Text, image | 1024 | Up to 8K tokens | `embedding` | Focused text↔image search, including multilingual text-to-image |
| [`jina-embeddings-v4`](https://jina.ai/models/jina-embeddings-v4/) | External JinaAI / marketplaces / on-prem (not on EIS) | Text, image, PDF | 2048 (default; optional `dimensions` via JinaAI service settings) | Up to 32K tokens | `embedding` | External or self-hosted multimodal embeddings when you connect through the JinaAI service |

For the full Jina catalog, deployment matrix, and input examples, refer to [Jina models](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md). For EIS availability by stack version, refer to [Supported models on EIS](/explore-analyze/elastic-inference/eis-supported-models.md).

## Use the `semantic` field type [semantic-field-for-multimodal-search]

The [`semantic`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field.md) field type is the simplest way to run multimodal search in {{es}}. Map a `semantic` field to an `embedding` {{infer}} endpoint; the field then:

- Generates embeddings when you index field values (no ingest pipeline or {{infer}} processor required)
- Splits long **text** into chunks
- Indexes embeddings with defaults that suit common use cases
- Searches those embeddings at query time

`inference_id` is **required**. There is no default endpoint. The ID must reference an endpoint that uses the `embedding` task type. That endpoint determines which modalities the field accepts.

Example using the preconfigured Jina Embeddings v5 Omni Small endpoint:

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

:::{note}
For a comparison with text-only inference fields, refer to [Should I use `semantic_text` or `semantic`?](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field.md#should-i-use-semantictext-or-semantic).
:::

Further reading on the `semantic` field:

- [Multimodal search quickstart](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field-quickstart.md)
- [Parameters for `semantic` fields](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field-reference.md#semantic-params)
- [Inference endpoint requirements](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field-reference.md#semantic-inference-endpoint)
- [Supported input types](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field-reference.md#semantic-input)
- [Limitations](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field-reference.md#semantic-limitations)
- [`semantic` field reference](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field-reference.md)

## Next steps [multimodal-search-next-steps]

- [Multimodal search with Jina embeddings](multimodal-search/multimodal-search-tutorial.md): End-to-end tutorial for mapping, indexing, and cross-modal queries
- [Build multimodal search with a `semantic` field](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field-quickstart.md): Image-focused quickstart with text, image, and PDF queries
- [`semantic` field type](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field.md): Mapping overview and comparison guidance
- [Jina models](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md): Model catalog, deployment options, and input formats
- [Elastic {{infer-cap}} Service](/explore-analyze/elastic-inference/eis.md): Hosted {{infer}} without managing ML nodes
- [{{infer}} API](/explore-analyze/elastic-inference/inference-api.md): Create and manage {{infer}} endpoints
