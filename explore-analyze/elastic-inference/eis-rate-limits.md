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

| Model                                             | Request/minute  | Tokens/minute (ingest)  | Tokens/minute (search)  | Notes                    |
|---------------------------------------------------|-----------------|-------------------------|-------------------------|--------------------------|
| Elastic Managed LLMs {applies_to}`stack: ga 9.3+` | 2000            | -                       | -                       | No rate limit on tokens  |
| ELSER {applies_to}`stack: ga 9.0+`                | 6,000           | 6,000,000               | 600,000                 | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
| Jina Embeddings v5 Nano {applies_to}`stack: ga 9.3+`   | 6,000           | 6,000,000               | 600,000                 | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
| Jina Embeddings v5 Small {applies_to}`stack: ga 9.3+`   | 6,000           | 6,000,000               | 600,000                 | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
| Jina Embeddings v3 {applies_to}`stack: ga 9.3+`   | 6,000           | 6,000,000               | 600,000                 | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
| Jina Embeddings v5 (Small) {applies_to}`stack: ga 9.3+`   | 6,000           | 6,000,000               | 600,000                 | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
| Jina Embeddings v5 (Nano) {applies_to}`stack: ga 9.3+`   | 6,000           | 6,000,000               | 600,000                 | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
| Jina Reranker v2 {applies_to}`stack: ga 9.3+`     | 600             | -                       | 6,000,000               | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
| Jina Reranker v3 {applies_to}`stack: ga 9.3+`     | 600             | -                       | 6,000,000               | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
