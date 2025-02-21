---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/re-ranking-overview.html
applies_to:
  stack:
  serverless:
---

# Ranking and reranking [re-ranking-overview]

Many search systems are built on multi-stage retrieval pipelines.

Earlier stages use cheap, fast algorithms to find a broad set of possible matches.

Later stages use more powerful models, often machine learning-based, to reorder the documents. This step is called re-ranking. Because the resource-intensive model is only applied to the smaller set of pre-filtered results, this approach returns more relevant results while still optimizing for search performance and computational costs.

{{es}} supports various ranking and re-ranking techniques to optimize search relevance and performance.


## Two-stage retrieval pipelines [re-ranking-two-stage-pipeline] 


### Initial retrieval [re-ranking-first-stage-pipeline] 


#### Full-text search: BM25 scoring [re-ranking-ranking-overview-bm25] 

{{es}} ranks documents based on term frequency and inverse document frequency, adjusted for document length. [BM25](https://en.wikipedia.org/wiki/Okapi_BM25) is the default statistical scoring algorithm in {{es}}.


#### Vector search: similarity scoring [re-ranking-ranking-overview-vector] 

Vector search involves transforming data into dense or sparse vector embeddings to capture semantic meanings, and computing similarity scores for query vectors. Store vectors using `semantic_text` fields for automatic inference and vectorization or `dense_vector` and `sparse_vector` fields when you need more control over the underlying embedding model. Query vector fields with `semantic`, `knn` or `sparse_vector` queries to compute similarity scores. Refer to [semantic search](semantic-search.md) for more information.


#### Hybrid techniques [re-ranking-ranking-overview-hybrid] 

Hybrid search techniques combine results from full-text and vector search pipelines. {{es}} enables combining lexical matching (BM25) and vector search scores using the [Reciprocal Rank Fusion (RRF)](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion.md) algorithm.


### Re-ranking [re-ranking-overview-second-stage] 

When using the following advanced re-ranking pipelines, first-stage retrieval mechanisms effectively generate a set of candidates. These candidates are funneled into the re-ranker to perform more computationally expensive re-ranking tasks.


#### Semantic re-ranking [re-ranking-overview-semantic] 

[*Semantic re-ranking*](ranking/semantic-reranking.md) uses machine learning models to reorder search results based on their semantic similarity to a query. Models can be hosted directly in your {{es}} cluster, or you can use [inference endpoints](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) to call models provided by third-party services. Semantic re-ranking enables out-of-the-box semantic search capabilities on existing full-text search indices.


#### Learning to Rank (LTR) [re-ranking-overview-ltr] 

[*Learning To Rank*](ranking/learning-to-rank-ltr.md) is for advanced users. Learning To Rank involves training a machine learning model to build a ranking function for your search experience that updates over time. LTR is best suited for when you have ample training data and need highly customized relevance tuning.

