---
navigation_title: Add semantic search to an existing index
description: Two paths for adding semantic search capability to an existing BM25 index — semantic reranking without reindexing, and adding semantic fields via reindex with an alias swap for zero downtime.
applies_to:
  stack: ga
  serverless:
    elasticsearch: ga
---

# Add semantic search to an existing Elasticsearch index

If you have an existing Elasticsearch index running full-text search, you can add semantic search capability without starting over. There are two paths depending on what you need:

- **Semantic reranking**: no reindexing required. Add a cross-encoder reranking step on top of your existing BM25 queries. This is the lowest-friction option and often produces an immediate relevance improvement.
- **Semantic fields via reindex**: add a `semantic_text` field to a new index version, reindex your data, and swap the alias. This enables native semantic retrieval and hybrid search, but requires reprocessing your corpus.

This page covers both paths. For guidance on choosing between them, refer to [Choose a hybrid and reranking strategy](/solutions/search/vector/choose-hybrid-reranking-strategy.md). For guidance on which semantic implementation to use once you have decided to reindex, refer to [Choose a semantic search implementation](/solutions/search/semantic-search/choose-semantic-implementation.md).

## Path A: Add semantic reranking without reindexing [reranking-path]

Semantic reranking works on top of any existing retrieval step, including BM25. You do not need to add vector fields or reindex your data. The reranker reads the original text field at query time and scores candidates against the query using a cross-encoder model.

This path is appropriate when:

- You want to improve result quality immediately without a reindex operation
- Your existing BM25 results include the right documents but in the wrong order
- You want to validate whether semantic relevance improves results before committing to a full migration

**Steps:**

**1. Create a reranking inference endpoint.** Elastic Rerank is available as a preconfigured endpoint in your cluster. Refer to [Semantic reranking](/solutions/search/ranking/semantic-reranking.md) for the current endpoint name and setup instructions. Third-party reranking services are also supported via the inference API.

**2. Wrap your existing query in a `text_similarity_reranker` retriever:**

```json
GET my-existing-index/_search
{
  "retriever": {
    "text_similarity_reranker": {
      "retriever": {
        "standard": {
          "query": {
            "match": {
              "body": "{{query_text}}"
            }
          }
        }
      },
      "field": "body",
      "inference_id": "my-reranker",
      "inference_text": "{{query_text}}",
      "rank_window_size": 50
    }
  }
}
```

The `rank_window_size` controls how many BM25 candidates are passed to the reranker. A value of 50–100 is a reasonable starting point. The reranker scores those candidates and returns the top `size` results in semantic order.

No changes to your index mapping or existing documents are required.

## Path B: Add semantic fields via reindex [reindex-path]

To enable native semantic retrieval — semantic queries, hybrid search with RRF, or the `semantic_text` field type — you need to add vector fields to your index. Because field types cannot be changed in an existing mapping, this requires creating a new index version and reindexing your data.

The steps below use an index alias to achieve zero downtime during the migration. Your existing queries continue serving from the current index while the new index is being built.

### Step 1: Create an inference endpoint [step-inference-endpoint]

Create the inference endpoint you will use to generate embeddings at index time. The `semantic_text` field type manages inference automatically once an endpoint is configured.

For ELSER (sparse vectors, recommended for general domain search without a labelled dataset), create a sparse embedding inference endpoint using the current ELSER model ID for your platform. Refer to [Semantic search with ELSER](/solutions/search/semantic-search/semantic-search-elser-ingest-pipelines.md) for the current model ID and deployment instructions.

For dense vector models, refer to [Semantic search with the inference API](/solutions/search/semantic-search/semantic-search-inference.md).

### Step 2: Create the new index with a semantic field [step-new-index]

Create a new index that includes your existing field mappings alongside a new `semantic_text` field. Copy your original field mappings exactly — you will use these to serve queries during the transition.

```json
PUT my-index-v2
{
  "mappings": {
    "properties": {
      "body": {
        "type": "text"
      },
      "title": {
        "type": "text"
      },
      "body_semantic": {
        "type": "semantic_text",
        "inference_id": "my-elser-endpoint"
      }
    }
  }
}
```

Add the `semantic_text` field alongside the original `text` field rather than replacing it. This lets you run hybrid search (BM25 on `body` + semantic on `body_semantic`) and makes it straightforward to fall back to BM25 queries during testing.

For dense vector index options such as quantization, refer to [Tune vector search performance and relevance](/solutions/search/vector/tune-vector-search.md) and configure `index_options` on the `semantic_text` field accordingly before reindexing.

### Step 3: Set up an alias with write routing [step-alias]

If your index receives live writes, configure an alias so that new documents are written to the new index while the reindex is running. This prevents a gap where newly indexed documents are missing from the new index.

If you are not already using an alias, create one pointing to the current index:

```json
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "my-index",
        "alias": "my-search",
        "is_write_index": true
      }
    }
  ]
}
```

Then add the new index to the alias and set it as the write target:

```json
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "my-index-v2",
        "alias": "my-search",
        "is_write_index": true
      }
    },
    {
      "add": {
        "index": "my-index",
        "alias": "my-search",
        "is_write_index": false
      }
    }
  ]
}
```

From this point, new documents go to `my-index-v2` and receive embeddings on ingest. Read queries via the `my-search` alias hit both indices and merge results. The reindex step below backfills the older documents.

:::{note}
If your index does not receive writes during the migration window — for example, it contains a static corpus — you can skip the alias write routing and do a simple reindex followed by a final alias swap at the end.
:::

### Step 4: Reindex the existing data [step-reindex]

Reindex from the original index to the new one. Set `size` to a small batch value (10–50) during initial testing so you can catch inference errors early. The `semantic_text` field type triggers the inference endpoint automatically during reindex.

```json
POST _reindex?wait_for_completion=false
{
  "source": {
    "index": "my-index",
    "size": 50
  },
  "dest": {
    "index": "my-index-v2"
  }
}
```

The call returns a task ID immediately. Use it to monitor progress:

```json
GET _tasks/<task_id>
```

**Throttle the reindex to protect your ML nodes.** Inference is CPU- and memory-intensive. Running a large reindex at full speed can starve query-serving allocations. Use the `requests_per_second` parameter to limit throughput:

```json
POST _reindex?wait_for_completion=false&requests_per_second=100
{
  "source": { "index": "my-index", "size": 50 },
  "dest": { "index": "my-index-v2" }
}
```

Adjust `requests_per_second` based on observed ML node load. You can also increase inference throughput by adding allocations to the inference endpoint if ML node capacity allows.

Large reindex operations can take hours or days for large corpora. Plan accordingly and monitor the task before treating the migration as complete.

### Step 5: Verify the new index [step-verify]

Before removing the old index from the alias, verify that the new index contains the expected document count and that semantic queries return reasonable results:

```json
GET my-index-v2/_count

GET my-index-v2/_search
{
  "query": {
    "semantic": {
      "field": "body_semantic",
      "query": "a representative query from your application"
    }
  }
}
```

If you have a judgment set, run `_rank_eval` against the new index before completing the cutover. Refer to [Evaluate retrieval quality](/solutions/search/ranking/evaluate-retrieval-quality.md).

### Step 6: Swap the alias [step-alias-swap]

Once the reindex is complete and verified, remove the old index from the alias in a single atomic operation:

```json
POST _aliases
{
  "actions": [
    {
      "remove": {
        "index": "my-index",
        "alias": "my-search"
      }
    }
  ]
}
```

The alias now points only to `my-index-v2`. The old index remains in place until you have confirmed the migration is stable. Delete it once you are satisfied.

### Step 7: Update your queries [step-update-queries]

With the new index in place, update your application queries to use the semantic field. The simplest change is to add a semantic query alongside your existing BM25 query using the `rrf` retriever:

```json
GET my-search/_search
{
  "retriever": {
    "rrf": {
      "retrievers": [
        {
          "standard": {
            "query": {
              "match": {
                "body": "{{query_text}}"
              }
            }
          }
        },
        {
          "standard": {
            "query": {
              "semantic": {
                "field": "body_semantic",
                "query": "{{query_text}}"
              }
            }
          }
        }
      ]
    }
  }
}
```

This hybrid query gives you the precision of BM25 alongside the recall of semantic search, combined using RRF. You can also run pure semantic queries, or add a reranking step on top. Refer to [Choose a hybrid and reranking strategy](/solutions/search/vector/choose-hybrid-reranking-strategy.md).

## Next steps [next-steps]

- [Evaluate retrieval quality](/solutions/search/ranking/evaluate-retrieval-quality.md)
- [Tune vector search performance and relevance](/solutions/search/vector/tune-vector-search.md)
- [Choose a hybrid and reranking strategy](/solutions/search/vector/choose-hybrid-reranking-strategy.md)
- [Semantic reranking](/solutions/search/ranking/semantic-reranking.md)
- [Aliases](/manage-data/data-store/aliases.md)
