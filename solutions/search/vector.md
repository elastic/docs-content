# Vector search

:::{tip}
Looking for a minimal configuration approach? The `semantic_text` field type provides an abstraction over these vector search implementations with sensible defaults and automatic model management. It's the recommended approach for most users. [Learn more about semantic_text](semantic-search/semantic-search-semantic-text.md).
:::

Elasticsearch's vector search capabilities enable finding content based on meaning and similarity, instead of keyword or exact term matches. Vector search is an important component of most modern [semantic search](semantic-search.md) implementations.
Vector search can also be used independently for various similarity matching use cases.

This guide explores the more manual technical implementation of vector search approaches, that **do not** use the `semantic_text` workflow.

## Vector queries and field types [choosing-vector-query]

Which query you use and which field you target in your queries depends on your chosen workflow. If you’re using the `semantic_text` workflow it’s quite simple. If not, it depends on which type of embeddings you’re working with.

If you want {{es}} to generate embeddings at both index and query time, use the `semantic_text` field and the `semantic` query. If you want to bring your own embeddings, use the `sparse_vector` or `dense_vector` field type and the associated query depending on the NLP model you used to generate the embeddings.

| Vector type | Field type      | Query type      | Use case                                           |
| ----------- | --------------- | --------------- | -------------------------------------------------- |
| Dense       | `dense_vector`  | `knn`           | Semantic similarity matching via neural embeddings  |
| Sparse      | `sparse_vector` | `sparse_vector` | Enhanced text search with semantic term expansion  |
|Dense or sparse |  [`semantic_text`](https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-text.html) | [`semantic`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-semantic-query.html) | The `semantic_text` field handles generating embeddings for you at index time and query time. |

## Dense vector vs. sparse vector

### Dense vector

Dense neural embeddings capture semantic meaning by translating content into a vector space. Fixed-length vectors of floating-point numbers represent the content's meaning, with similar content mapped to nearby points in the vector space.
When you need to find related items, these vectors work with distance metrics to identify semantic similarity. This is ideal for when you want to capture "what this content is about" rather than just what words it contains.

Dense vectors are well-suited for:
- Finding semantically similar content ("more like this")
- Matching questions with answers
- Image similarity search
- Recommendations based on content similarity

To implement dense vector search, you'll need to:
1. Generate document embeddings using a neural model (locally or in {{es}})
2. Configure your vector similarity settings
3. Generate query embeddings at search time
4. Use the `knn` query for searches

[Learn more about dense vector search implementation](vector/dense-vector.md)

### Sparse vector (ELSER)

While dense vectors capture overall meaning, sparse vectors excel at intelligent vocabulary expansion. The model enriches each key concept with closely related terms and ideas, creating semantic connections that go beyond simple word-level substitutions.

Using [Elastic's learned sparse encoder model (ELSER)](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md), both queries and documents get expanded into weighted terms. The result is powerful search that is also transparent - you can see exactly why matches occur. This contrasts with the "black-box" nature of dense vector matching, where similarity is based on abstract vector distances.

Sparse vectors are ideal for:

- Enhanced keyword search with semantic understanding
- Cases where you need explainable search results
- Scenarios requiring precise term matching with semantic awareness
- Domain-specific search where vocabulary relationships matter

To implement sparse vector search with ELSER manually, you'll need to:
1. Configure ELSER to embed your content
2. Configure ELSER to embed your queries
3. Use the `sparse_vector` query for searches

[Learn more about implementing sparse vector search](vector/sparse-vector-elser.md)

### Key considerations

If you've chosen to implement vector search manually rather than using the guided `semantic_text` workflow, consider:

1. **Data characteristics**
   - **Text length:** Dense vectors work best with shorter texts like product descriptions or chat messages. For longer content like articles or documentation, sparse vectors handle length better.
   - **Domain specificity:** For specialized content (medical literature, legal documents, technical documentation), sparse vectors preserve domain-specific terminology. Dense vectors can miss nuanced technical terms.
   - **Update frequency:** If your content changes frequently, dense vectors require recomputing embeddings for each update. Sparse vectors handle incremental updates more efficiently.

2. **Performance requirements**
   - **Query latency:** Dense vectors with HNSW offer fast search times for moderate-sized datasets. Sparse vectors have higher but consistent latency across dataset sizes.
   - **Memory footprint:** Dense vectors' size is determined by their chosen dimensionality, while sparse vectors' size varies with content complexity.
   - **Resource needs:** Dense vectors benefit significantly from GPU acceleration. Sparse vectors perform well on CPU-only setups.

3. **Explainability needs**
   - **Transparency is important:** For transparency and relevance debugging, sparse vectors show exactly which terms contributed.
   - **Transparency isn't important:** For recommendations and "more like this" features, dense vectors work well.

4. **Implementation complexity**
   - **Dense vector setup:** More complex due to wide range of embedding models to choose from, configure, and manage.
   - **Sparse vector setup:** Simpler since ELSER is Elastic's standard sparse encoding model and is available out-of-the-box.

## Implementation tutorials

TODO

- [](semantic-search/bring-own-vectors.md)
- [Sparse vector search with ELSER](vector/sparse-vector-elser.md)
- [Semantic search with a model deployed in {{es}}](semantic-search/semantic-search-deployed-nlp-model.md)
- [Semantic search with the msmarco-MiniLM-L-12-v3 sentence-transformer model](../../explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md)

## Additional resources

T