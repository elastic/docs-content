---
applies:
  stack:
  serverless:
---
# Hybrid search

Hybrid search combines traditional [full-text search](full-text.md) with [AI-powered search](ai-search/ai-search.md) for more powerful search experiences that serve a wider range of user needs.

The recommended way to use hybrid search in the Elastic Stack is following the `semantic_text` workflow. Check out the [hands-on tutorial](hybrid-semantic-text.md) for a step-by-step guide.

We recommend implementing hybrid search with the [reciprocal rank fusion (RRF)](https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html) algorithm. This approach merges rankings from both semantic and lexical queries, giving more weight to results that rank high in either search. This ensures that the final results are balanced and relevant.