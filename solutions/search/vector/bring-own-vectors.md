---
navigation_title: Bring your own dense vectors
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bring-your-own-vectors.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
description: An introduction to vectors and knn search in Elasticsearch.
---

# Bring your own dense vectors [bring-your-own-vectors]

{{es}} enables you store and search mathematical representations of your content called _embeddings_ or _vectors_, which help machines understand and process your data more effectively.
There are two types of representation (_dense_ and _sparse_), which are suited to different types of queries and use cases (for example, finding similar images and content or storing expanded terms and weights).

In this introduction to [vector search](/solutions/search/vector.md), you'll store and search for dense vectors.
You'll also learn the syntax for searching these documents using a [k-nearest neighbour](/solutions/search/vector/knn.md) (kNN) query.

## Prerequisites

- If you're using {{es-serverless}}, create a project with the general purpose configuration. To add the sample data, you must have a `developer` or `admin` predefined role or an equivalent custom role.
- If you're using {{ech}} or a self-managed cluster, start {{es}} and {{kib}}. The simplest method to complete the steps in this guide is to log in with a user that has the `superuser` built-in role.
  
To learn about role-based access control, check out [](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md).

## Create a vector database

When you create vectors (or _vectorize_ your data), you convert complex and nuanced content (such as text, videos, images, or audio) into multidimensional numerical representations.
They must be stored in specialized data structures designed to ensure efficient similarity search and speedy vector distance calculations.

In this quide, you'll use documents that already have dense vector embeddings.
To deploy a vector embedding model in {{es}} and generate vectors while ingesting and searching your data, refer to the links in [Learn more](#bring-your-own-vectors-learn-more).

::::{tip}
This is an advanced use case that uses the `dense_vector` field type. Refer to [](/solutions/search/semantic-search.md) for an overview of your options for semantic search with {{es}}.
To learn about the differences between semantic search and vector search, go to [](/solutions/search/ai-search/ai-search.md).
::::

:::::{stepper}
::::{step} Create an index with dense vector field mappings

Each document in our simple data set will have:

* A review: stored in a `review_text` field
* An embedding of that review: stored in a `review_vector` field, which is defined as a [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) data type.

:::{tip}
The `dense_vector` type automatically uses `int8_hnsw` quantization by default to reduce the memory footprint required when searching float vectors. Learn more about balancing performance and accuracy in [Dense vector quantization](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization).
:::

The following API request defines the `review_text` and `review_vector` fields:

```console
PUT /amazon-reviews
{
  "mappings": {
    "properties": {
      "review_vector": {
        "type": "dense_vector",
        "dims": 8, <1>
        "index": true, <2>
        "similarity": "cosine" <3>
      },
      "review_text": {
        "type": "text"
      }
    }
  }
}
```

1. The `dims` parameter must match the length of the embedding vector. If not specified, `dims` will be dynamically calculated based on the first indexed document.
2. The `index` parameter is set to `true` to enable the use of the `knn` query.
3. The `similarity` parameter defines the similarity function used to compare the query vector to the document vectors. `cosine` is the default similarity function for `dense_vector` fields in {{es}}.

Here we're using an 8-dimensional embedding for readability.
The vectors that neural network models work with can have several hundreds or even thousands of dimensions that represent a point in a multi-dimensional space.
Each vector dimension represents a _feature_ or a characteristic of the unstructured data.
::::
::::{step} Add documents with embeddings

First, index a single document to understand the document structure:

```console
PUT /amazon-reviews/_doc/1
{
  "review_text": "This product is lifechanging! I'm telling all my friends about it.",
  "review_vector": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8] <1>
}
```

1. The size of the `review_vector` array is 8, matching the `dims` count specified in the mapping.

In a production scenario, you'll want to index many documents at once using the [`_bulk` endpoint]({{es-apis}}operation/operation-bulk).
Here's an example of indexing multiple documents in a single `_bulk` request:

```console
POST /_bulk
{ "index": { "_index": "amazon-reviews", "_id": "2" } }
{ "review_text": "This product is amazing! I love it.", "review_vector": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8] }
{ "index": { "_index": "amazon-reviews", "_id": "3" } }
{ "review_text": "This product is terrible. I hate it.", "review_vector": [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1] }
{ "index": { "_index": "amazon-reviews", "_id": "4" } }
{ "review_text": "This product is great. I can do anything with it.", "review_vector": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8] }
{ "index": { "_index": "amazon-reviews", "_id": "5" } }
{ "review_text": "This product has ruined my life and the lives of my family and friends.", "review_vector": [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1] }
```

::::
:::::

## Test vector search [bring-your-own-vectors-search-documents]

Now you can query these document vectors using a [`knn` retriever](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md#knn-retriever).
`knn` is a type of vector search, which finds the `k` most similar documents to a query vector.
Here we're using a raw vector for the query text for demonstration purposes:

```console
POST /amazon-reviews/_search
{
  "retriever": {
    "knn": {
      "field": "review_vector",
      "query_vector": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], <1>
      "k": 2, <2>
      "num_candidates": 5 <3>
    }
  }
}
```

1. A raw vector serves as the query text in this example. In a real-world scenario, you'll need to generate vectors for queries using an embedding model.
2. The `k` parameter specifies the number of results to return.
3. The `num_candidates` parameter is optional. It limits the number of candidates returned by the search node. This can improve performance and reduce costs.

## Next steps

If you want to try a similar set of steps from an {{es}} client, check out the guided index workflow:

- If you're using Elasticsearch Serverless, go to **{{es}} > Home**, select the vector search workflow, and **Create a vector optimized index**.
- If you're using {{ech}} or a self-managed cluster, go to **Elasticsearch > Home** and click **Create API index**. Select the vector search workflow.

When you finish your tests and no longer need the sample data set, delete the index:

```console
DELETE /amazon-reviews
```

## Learn more [bring-your-own-vectors-learn-more]

In these simple examples, we're sending a raw vector for the query text.
In a real-world scenario you won't know the query text ahead of time.
You'll need to generate query vectors, on the fly, using the same embedding model that generated the document vectors.
For this you'll need to deploy a text embedding model in {{es}} and use the [`query_vector_builder` parameter](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md#knn-query-top-level-parameters).
Alternatively, you can generate vectors client-side and send them directly with the search request.

For an example of using pipelines to generate text embeddings, check out [](/solutions/search/vector/dense-versus-sparse-ingest-pipelines.md).

To learn about more search options, such as semantic, full-text, and hybrid, go to [](/solutions/search/search-approaches.md).
