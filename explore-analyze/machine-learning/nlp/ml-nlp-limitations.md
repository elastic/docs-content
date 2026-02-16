---
navigation_title: Limitations
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-limitations.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# NLP limitations [ml-nlp-limitations]

The following limitations and known problems apply to the Elastic {{nlp}} trained models feature.

## Document size limitations when using `semantic_text` fields [ml-nlp-large-documents-limit-10k-10mb]

When using semantic text to ingest documents, chunking takes place automatically. The number of chunks is limited by the [`index.mapping.nested_objects.limit`](elasticsearch://reference/elasticsearch/index-settings/mapping-limit.md) cluster setting, which defaults to 10k. Documents that are too large will cause errors during ingestion. To avoid this issue, split your documents into roughly 1MB parts before ingestion.

## ELSER semantic search is limited to 512 tokens per field that inference is applied to [ml-nlp-elser-v1-limit-512]

When you use ELSER for semantic search, only the first 512 extracted tokens from each field of the ingested documents that ELSER is applied to are taken into account for the search process. If your data set contains long documents, divide them into smaller segments before ingestion if you need the full text to be searchable.
