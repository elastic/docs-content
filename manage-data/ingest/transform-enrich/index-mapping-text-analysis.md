---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Index mapping and text analysis

As part of planning how your incoming data might be transformed and enriched as it is ingested, you may want to customize how the data should be organized inside {{es}} and how text fields should be analyzed.

Refer to [Mapping](/manage-data/data-store/mapping.md) to learn about the dynamic mapping rules that Elasticsearch runs by default to identify the data types in your data and to store it in matching fields. You can also configure your own custom mappings to take full control over how your data is organized in the documents in an {{es}} index.

Refer to [Text analysis](/manage-data/data-store/text-analysis.md) to learn how to configure an analyzer to run on incoming text, in order to ensure that relevant documents are retrieved from text-based queries. You can opt to use one of several built-in analyzers, or create a custom analyzer for your specific use cases.
