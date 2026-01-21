---
applies_to:
  stack: ga
  serverless: ga
navigation_title: Elastic Inference
---

# Elastic {{infer-cap}}

## Overview

{{infer-cap}} is a process of using a {{ml}} trained model to make predictions or operations - such as text embedding, or reranking - on your data.
You can use {{infer}} during ingest time (for example, to create embeddings from textual data you ingest) or search time (to perform [semantic search](/solutions/search/semantic-search.md) based on the embeddings created previously).
There are several ways to perform {{infer}} in the {{stack}}, depending on the underlying {{infer}} infrastructure and the interface you use:

- **{{infer-cap}} infrastructure:**

  - [Elastic {{infer-cap}} Service](elastic-inference/eis.md): a managed service that runs {{infer}} outside your cluster resources.
  - [Trained models deployed in your cluster](machine-learning/nlp/ml-nlp-overview.md): models run on your own {{ml}} nodes

- **Access methods:**

  - [The `semantic_text` workflow](/solutions/search/semantic-search/semantic-search-semantic-text.md): a simplified method that uses the {{infer}} API behind the scenes to enable semantic search.
  - [The {{infer}} API](elastic-inference/inference-api.md): a general-purpose API that enables you to run {{infer}} using EIS, your own models, or third-party services.
