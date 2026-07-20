---
navigation_title: Get started
description: >-
  Create an Elasticsearch Vector Database project on Elastic Cloud Serverless,
  ingest embeddings, and run your first vector or semantic searches.
applies_to:
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Get started with the {{es}} Vector Database project type

The {{es}} Vector Database project type on {{serverless-full}} is built for AI-powered vector retrieval. Use this guide to create a project, add embeddings, and run similarity or semantic searches from your application.

:::{note}
Not sure whether this project type is right for you? Refer to [When to use this project type](/solutions/vector-database.md#when-to-use-this-project-type).

If you're looking for an introduction to the {{stack}} or the {{es}} product, go to [](/get-started/index.md) or [](/manage-data/data-store.md).
:::

::::::{stepper}
:::::{step} Create an {{es}} Vector Database {{serverless-short}} project

There are two options to create serverless projects:

* If you're a new user, [sign up for a free 14-day trial](https://cloud.elastic.co/serverless-registration). For more information about {{ecloud}} trials, check out [Trial information](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#general-sign-up-trial-what-is-included-in-my-trial).
* If you're an existing customer, [log in to {{ecloud}}](https://cloud.elastic.co/login) and do the following:
  1. Select **Create project** from the **Serverless projects** panel.
  2. Select **Next** from the **Vector Database** panel.
  3. Name your project.
  4. Select a cloud provider and region. For available regions, refer to [Regions](/deploy-manage/deploy/elastic-cloud/regions.md).
  5. Select **Create project**. It takes a few minutes to create your project.
  6. When the project is ready, select **Continue** to open it (you might need to log in to {{ecloud}} again).

:::{note}
You need the `admin` predefined role or an equivalent custom role to create projects. For more information, refer to [User roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md).
:::

After you've created your project, note the {{es}} endpoint and API key from the project connection details. You'll use these to index data and run searches. New indices in this project type use [vector index mode](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-vectordb-document-mode) automatically.
:::::

:::::{step} (Optional) Follow the in-product setup guides

When you create a new Vector Database project, the **Set up your Elasticsearch Vector Database** page includes two guided paths you can follow. Each path walks you through ingest and then search examples, with sample scripts you can run in a client of your choosing or run the examples directly in the Console.

The following setup guides are available in {{kib}}:

| Guide | When to use | What you do |
| --- | --- | --- |
| Generate embeddings from your content | You want {{es}} to create embeddings for you | Ingest content into a `semantic_text` field, then run a semantic or hybrid query |
| Store your existing embeddings | You already have vectors from your own model | Index pre-generated embeddings into a `dense_vector` field, then run a semantic or hybrid query |

You can also skip the setup guide and continue with the steps below.
:::::

:::::{step} Ingest your data
Use the approach that matches how you create embeddings.

::::{dropdown} Generate embeddings from your content
Create an index with a [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field, then ingest documents so {{es}} generates embeddings automatically. The default model is [`jina-embeddings-v3`](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-embeddings-v3), integrated through the {{es}} {{infer}} pipeline.

::::

::::{dropdown} Store your existing embeddings
Create an index with a [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) field, and any other text or metadata fields you might need, then index your pre-generated vectors.

To walk through indexing sample embeddings and running a kNN search, follow [Bring your own dense vectors to {{es}}](/solutions/search/vector/bring-own-vectors.md).
::::

Use a language [client](/reference/elasticsearch-clients/index.md) or the [Bulk]({{es-serverless-apis}}operation/operation-bulk) API to load data. If you're not ready to use your own content, follow the [semantic search quickstart](/solutions/search/get-started/semantic-search.md).
:::::

:::::{step} Search your data
Use the approach that matches how you ingested embeddings.

::::{dropdown} Search embeddings generated from your content
Query with natural language. {{es}} embeds the query and returns the most relevant matches. You can also run a hybrid query that combines semantic and lexical ranking.

To walk through hybrid search with `semantic_text`, follow [Hybrid search with `semantic_text`](/solutions/search/hybrid-semantic-text.md). For query and retrieval options, see [Search and retrieve `semantic_text` fields](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-search-retrieval.md).
::::

::::{dropdown} Search your existing embeddings
Run a kNN search against your `dense_vector` field, or combine kNN with lexical search for hybrid retrieval.

Queries need to be converted into vectors the same way your documents were. Specify the model you used to generate your embeddings so {{es}} can apply it to your queries too.

To walk through kNN search, follow [kNN search in {{es}}](/solutions/search/vector/knn.md). For combining vector and lexical ranking, see [Hybrid search](/solutions/search/hybrid-search.md).
::::

For more query options, see [Querying for search](/solutions/search/querying-for-search.md) and the [{{es-serverless}} API documentation]({{es-serverless-apis}}).
:::::
::::::

## Next steps

After you've learned how to ingest embeddings and return relevant results, dig deeper into how vector search works, improve ranking for your use case, and tune project settings for latency and cost. Review the following: 

* [Vector search in {{es}}](/solutions/search/vector.md): Concepts, field types, quantization, and query options
* [Ranking and reranking](/solutions/search/ranking.md): Improve relevance after you have a baseline
* [RAG](/solutions/search/rag.md): Patterns for grounding LLMs on retrieved context
* [Vector search use cases](/solutions/search/vector/vector-search-use-cases.md): RAG, recommendations, multimodal search, and more
* [Search Power](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) and [billing dimensions](/deploy-manage/cloud-organization/billing/vector-database-billing-dimensions.md): Balance latency and cost for your project
* [{{es}} Vector Database overview](/solutions/vector-database.md): When to choose this project type versus the general-purpose {{es}} project
* [{{es}} solution](/solutions/elasticsearch-solution-project.md): General-purpose project type and search application UI tools
