---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-limitations.html
---

# Limitations [ml-nlp-limitations]

The following limitations and known problems apply to the 9.0.0-beta1 release of the Elastic {{nlp}} trained models feature.

## Document size limitations when using `semantic_text` fields [ml-nlp-large-documents-limit-10k-10mb]

When using semantic text to ingest documents, chunking takes place automatically. The number of chunks is limited by the [`index.mapping.nested_objects.limit`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/mapping-limit-settings.md) cluster setting, which defaults to 10k. Documents that are too large will cause errors during ingestion. To avoid this issue, please split your documents into roughly 1MB parts before ingestion.

## ELSER semantic search is limited to 512 tokens per field that inference is applied to [ml-nlp-elser-v1-limit-512]

When you use ELSER for semantic search, only the first 512 extracted tokens from each field of the ingested documents that ELSER is applied to are taken into account for the search process. If your data set contains long documents, divide them into smaller segments before ingestion if you need the full text to be searchable.
