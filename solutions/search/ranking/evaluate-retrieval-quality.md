---
navigation_title: Measure quality
description: Build a judgment set, choose the right metric, and use the rank evaluation API to measure and compare retrieval pipeline performance in Elasticsearch.
applies_to:
  stack: ga
  serverless:
    elasticsearch: ga
---

# Evaluate retrieval quality

Measuring retrieval quality lets you make evidence-based decisions when tuning your pipeline. Without measurement, it is not possible to know whether a change — a different quantization level, an added reranking step, or a modified query — actually improved results.

This page covers how to build a judgment set, choose an evaluation metric, and run the `_rank_eval` API against your pipeline. For tuning parameters like `num_candidates` and rescoring, refer to [Tune vector search performance and relevance](/solutions/search/vector/tune-vector-search.md). For guidance on when to add reranking or switch retrieval strategies, refer to [Choose a hybrid and reranking strategy](/solutions/search/vector/choose-hybrid-reranking-strategy.md).

## Step 1: Build a judgment set [judgment-set]

A judgment set is a collection of queries paired with relevance ratings for specific documents. It is the input the `_rank_eval` API requires.

Each entry in a judgment set contains:

- A query that is representative of real user queries in your application
- A list of `(document_id, rating)` pairs that express the relevance of specific documents for that query

Relevance ratings can be binary (0 = irrelevant, 1 = relevant) or graded (for example, 0–3). Use graded ratings when you need a metric that rewards ranking highly relevant documents above marginally relevant ones, such as NDCG.

**How to source your query set:**

- Use query logs from your existing search system if available. Filter to queries with sufficient volume and diverse enough coverage of your use cases.
- For new applications without logs, write queries by hand that represent the key use cases you are building for. Aim for at least 20–50 queries to get a stable metric; more is better.

**How to source ratings:**

- Manual human annotation is the most reliable method. Annotators review the top-k results for each query and assign ratings.
- For applications with user interaction data, implicit signals such as click-through rate can supplement or replace manual ratings, but they are noisy and require careful interpretation.
- For RAG or question-answering applications, you can generate candidate ratings programmatically using an LLM as a judge. For guidance on LLM-based evaluation, refer to the [Elastic Search Labs blog](https://www.elastic.co/search-labs).

Keep your judgment set in source control. It is the baseline you compare all future pipeline changes against.

## Step 2: Choose a metric [metrics]

The `_rank_eval` API supports five metrics. Choose based on what matters most in your application.

**Precision@k** measures what fraction of the top-k results are relevant. Use it when every result shown to the user should be relevant — for example, in a product search or document retrieval UI where false positives are costly.

**Recall@k** measures what fraction of all relevant documents appear in the top-k results. Use it when missing a relevant result is the main failure mode — for example, in a RAG pipeline where leaving out a critical passage degrades the generated answer.

**Mean Reciprocal Rank (MRR)** measures how highly the first relevant result is ranked. Use it for applications where the user is looking for a single correct answer and position of that answer matters — for example, a question-answering interface or navigational search.

**Discounted Cumulative Gain (DCG) / NDCG** rewards placing highly relevant documents earlier in the ranking, using graded relevance scores. NDCG normalizes DCG against an ideal ranking. Use it when you have graded ratings and want a metric that captures ranking quality across all top-k positions.

**Expected Reciprocal Rank (ERR)** is a position-based metric that models a user who stops reading once they find a satisfactory result. It is useful when higher-rated documents are disproportionately more valuable than lower-rated ones.

For most retrieval evaluation tasks, start with **NDCG@10** or **Precision@10**. Both are widely understood and cover the typical top-10 result window.

## Step 3: Run the rank evaluation API [run-rank-eval]

The `_rank_eval` API takes your judgment set and returns the chosen metric score across all queries in the set.

A minimal request using NDCG:

```json
GET my-index/_rank_eval
{
  "requests": [
    {
      "id": "what is elasticsearch",
      "request": {
        "query": {
          "semantic": {
            "field": "content",
            "query": "what is elasticsearch"
          }
        }
      },
      "ratings": [
        { "_index": "my-index", "_id": "doc-1", "rating": 3 },
        { "_index": "my-index", "_id": "doc-2", "rating": 1 },
        { "_index": "my-index", "_id": "doc-5", "rating": 0 }
      ]
    }
  ],
  "metric": {
    "dcg": {
      "k": 10,
      "normalize": true
    }
  }
}
```

The response includes a `metric_score` across all queries, per-query scores in the `details` section, and an `unrated_docs` list for documents that appeared in results but had no rating in your judgment set. Use `unrated_docs` to identify gaps in your judgment set and expand it over time.

The `request.query` field accepts any valid Elasticsearch Query DSL query. Use a `semantic` query to evaluate a semantic retrieval pipeline, a `match` query for BM25, or a `bool` query to combine them. The `_rank_eval` API does not support the `retriever` syntax — evaluate the query layer directly.

For the full API reference, refer to the Elasticsearch reference documentation.

## Step 4: Compare configurations [compare]

The value of `_rank_eval` comes from running it repeatedly against the same judgment set as you make changes. A single score in isolation is not meaningful; a score relative to a baseline is.

A practical workflow:

1. Establish a baseline score using your current pipeline configuration.
2. Make one change — for example, adjust `num_candidates`, add a reranking step, or switch from RRF to linear combination.
3. Run `_rank_eval` with the same judgment set and compare the new score to the baseline.
4. Keep the change if the score improves; revert if it does not.

Run this loop for each tuning decision. Changes that appear intuitive sometimes reduce metric scores; changes that seem minor sometimes produce meaningful gains.

:::{tip}
When comparing configurations, hold the judgment set constant. Changing the queries or ratings between runs makes results incomparable. If you need to expand the judgment set, rerun the baseline configuration against the updated set before comparing.
:::

## Limitations of offline evaluation [limitations]

The `_rank_eval` API performs offline evaluation: it measures retrieval quality against a static judgment set that you define in advance. Offline evaluation is fast, reproducible, and easy to automate in a CI pipeline. It is the right starting point for most teams.

Offline evaluation has limits:

- It cannot capture user satisfaction directly. A document rated relevant by an annotator may not be the one a user clicks on.
- Judgment sets go stale as your corpus and user queries evolve. Review and update your judgment set periodically.
- For RAG pipelines, retrieval quality is necessary but not sufficient. Whether good retrieved documents lead to good generated answers requires end-to-end evaluation beyond `_rank_eval`. For LLM-based evaluation approaches, refer to the [Elastic Search Labs blog](https://www.elastic.co/search-labs).

## Next steps [next-steps]

- [Tune vector search performance and relevance](/solutions/search/vector/tune-vector-search.md)
- [Choose a hybrid and reranking strategy](/solutions/search/vector/choose-hybrid-reranking-strategy.md)
