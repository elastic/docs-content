---
navigation_title: EIS model catalogue
applies_to:
  stack: ga
  serverless: ga
  deployment:
    self: unavailable
---

# EIS model catalogue [eis-model-catalogue]

| Model | Type | Request/minute  | Tokens/minute (ingest)  | Tokens/minute (search)  | Notes                    |
|-------|------|-----------------|-------------------------|-------------------------|--------------------------|
| Claude Sonnet 3.7 {applies_to}`stack: ga 9.3+`| LLM | 400     | -                       | -                       | No rate limit on tokens  |
| Elastic Managed LLM {applies_to}`stack: ga 9.0-9.2`| LLM | 400     | -                       | -                       | No rate limit on tokens. Renamed to *Claude Sonnet 3.7* in later versions  |
| Claude Sonnet 4.5 {applies_to}`stack: ga 9.3+`| LLM | 400                   | -                   | -                       | No rate limit on tokens  |
| ELSER | Embedding | 6,000           | 6,000,000               | 600,000                 | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
| `jina-embeddings-v3` {applies_to}`stack: preview 9.3`  | Embedding | 6,000           | 6,000,000               | 600,000                 | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |