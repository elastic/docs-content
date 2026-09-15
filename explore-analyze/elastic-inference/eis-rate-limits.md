---
navigation_title: Rate limits
applies_to:
  stack: ga
  serverless: ga
description: Learn about rate limits for Elastic Inference Service (EIS) models.
---

# Rate limits [eis-rate-limits]

This page lists the rate limits that apply to Elastic {{infer-cap}} Service (EIS) models.

Exceeding a limit results in HTTP 429 responses from the server until the sliding window moves on further and parts of the limit resets.

Where both a requests-per-minute and a tokens-per-minute limit apply, whichever limit is reached first takes effect.

## Chat models [eis-rate-limits-chat]

| Model                                              | Requests/minute | Notes                   |
|----------------------------------------------------|-----------------|-------------------------|
| Elastic Managed LLMs {applies_to}`stack: ga 9.3+`  | 2,000           | No rate limit on tokens |

## Embedding models [eis-rate-limits-embeddings]

Embedding models are used for both ingest (indexing documents) and search (query-time retrieval). Limits apply independently per use.

| Model                                                  | Requests/minute (search) | Requests/minute (ingest) | Tokens/minute (search) | Tokens/minute (ingest) |
|--------------------------------------------------------|--------------------------|--------------------------|------------------------|------------------------|
| ELSER {applies_to}`stack: ga 9.0+`                     | 6,000                    | 6,000                    | 600,000                | 6,000,000              |
| Jina Embeddings v3 {applies_to}`stack: ga 9.3+`        | 6,000                    | 6,000                    | 600,000                | 6,000,000              |
| Jina Embeddings v5 Nano {applies_to}`stack: ga 9.3+`   | 60,000                   | 30,000                   | 6,000,000              | 30,000,000             |
| Jina Embeddings v5 Small {applies_to}`stack: ga 9.3+`  | 60,000                   | 30,000                   | 6,000,000              | 30,000,000             |

## Reranking models [eis-rate-limits-rerankers]

Reranking models are used at search time only.

| Model                                             | Requests/minute | Tokens/minute |
|---------------------------------------------------|-----------------|---------------|
| Jina Reranker v2 {applies_to}`stack: ga 9.3+`     | 600             | 6,000,000     |
| Jina Reranker v3 {applies_to}`stack: ga 9.3+`     | 600             | 6,000,000     |
| Jina Reranker v3.5 {applies_to}`stack: ga 9.5+`   | 600             | 6,000,000     |
