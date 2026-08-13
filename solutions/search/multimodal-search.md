---
navigation_title: Multimodal search
description: Search images with text and run cross-modal retrieval in Elasticsearch using multimodal embeddings, Jina models, and the semantic field type.
applies_to:
  stack: ga
  serverless: ga
---
# Multimodal search in {{es}} [multimodal-search]

Multimodal search finds results by meaning across more than one content type. Common use cases include text-to-image product search, finding similar images, searching media libraries by natural language, and retrieving screenshots or document pages with text or image queries.

Multimodal search builds on [vector search](vector.md). A multimodal embedding model maps each supported input into a dense vector so content with similar meaning is nearby in vector space, even when the media types differ.

:::{tip}
For a hands-on tutorial, refer to [Tutorial: Build multimodal search with a `semantic` field](multimodal-search/multimodal-search-tutorial.md).
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

:::{include} /explore-analyze/machine-learning/nlp/_snippets/jina-multimodal-embedding-models.md
:::

For the full Jina catalog, deployment matrix, and input examples, refer to [Jina models](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md). For EIS availability by stack version, refer to [Supported models on EIS](/explore-analyze/elastic-inference/eis-supported-models.md).

:::{include} /explore-analyze/machine-learning/nlp/_snippets/jina-deploy-and-access-options.md
:::

## The `semantic` field type [semantic-field-for-multimodal-search]

```{applies_to}
stack: preview 9.5+
serverless: preview
```

:::{important}
The `semantic` field type is in technical preview and is not recommended for production use. This functionality may be changed or removed in a future release. Features in technical preview are not subject to the support SLA of official GA features.
:::

The `semantic` field type simplifies semantic and multimodal search across text, images, audio, video, and PDF files. With a compatible multimodal embedding model, you can search from any supported input type to any other supported input type. The field automatically:

- Generates embeddings when you index field values, without an ingest pipeline or inference processor.
- Splits long text into smaller passages, called chunks.
- Indexes the generated embeddings using default index options that optimize for common use cases.
- Searches the embeddings generated for each value or text chunk.

For field parameters, defaults, supported input types, and limitations, refer to the [`semantic` field documentation](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field.md).

Here's an example using the Jina Embeddings v5 Omni Small endpoint:

```console
PUT my-multimodal-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "semantic",
        "inference_id": ".jina-embeddings-v5-omni-small" <1>
      }
    }
  }
}
```

1. Required. A `semantic` field has no default {{infer}} endpoint. You must specify an `embedding` endpoint ID.

## Next steps [multimodal-search-next-steps]

- [Tutorial: Build multimodal search with a `semantic` field](multimodal-search/multimodal-search-tutorial.md): Index images and search them with text, image, and PDF input
- [`semantic` field type](elasticsearch://reference/elasticsearch/mapping-reference/semantic-field.md): Review the mapping reference of the `semantic` field tpye.

## Related pages [multimodal-search-related-pages]

- [Jina models](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md): Learn about Jina models, how to deploy them, and how to structure multimodal input payloads.
- [Elastic {{infer-cap}} Service](/explore-analyze/elastic-inference/eis.md): Learn how to use hosted {{infer}} without managing ML nodes.
- [{{infer-cap}} API](/explore-analyze/elastic-inference/inference-api.md): Learn how to create and manage {{infer}} endpoints.
