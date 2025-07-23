---
applies_to:
  stack: ga
  serverless: ga
navigation_title: Elastic Inference
---

# Elastic {{infer-cap}}

## Overview

{{infer-cap}} is a process of using an LLM or a {{ml}} trained model to make predictions or operations - such as text embedding, completion, or reranking - on your data.
You can use {{infer}} during ingest time (for example, to create embeddings from textual data you ingest) or search time (to perform [semantic search](/solutions/search/semantic-search.md)).
There are several ways to perform {{infer}} in the {{stack}}:

* [Using the Elastic {{infer-cap}} Service](/elastic-inference/eis.md)
* [Using `semantic_text` if you want to perform semantic search](/solutions/search/semantic-search/semantic-search-semantic-text.md)
* [Using the {{infer}} API](elastic-inference/inference-api.md)
* [Trained models deployed in your cluster](machine-learning/nlp/ml-nlp-overview.md)
