---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/playground-query.html
applies_to:
  stack: preview 9.0, beta 9.1
  serverless: beta
products:
  - id: kibana
---

# View and modify queries [playground-query]

Once you’ve set up your chat interface, you can start chatting with the model. Playground will automatically generate {{es}} queries based on your questions, and retrieve the most relevant documents from your {{es}} indices. The Playground UI enables you to view and modify these queries.

* Select the **Query** tab to open the visual query editor.
* Modify the query by selecting fields to query per index.

::::{tip}
The `{{query}}` variable represents the user’s question, rewritten as an {{es}} query.

::::


The following screenshot shows the query editor in the Playground UI. In this simple example, the `books` index has two fields: `author` and `name`. Selecting a field adds it to the `fields` array in the query.

:::{image} /solutions/images/kibana-query-interface.png
:alt: View and modify queries
:screenshot:
:::

Certain fields in your documents may be hidden. Learn more about [hidden fields](#playground-hidden-fields).


## Improving relevance [playground-query-relevance]

The fields you select in the query editor determine the relevance of the retrieved documents.

Remember that the next step in the workflow is to send the retrieved documents to the LLM to answer the question. Context length is an important factor in ensuring the model has enough information to generate a relevant answer. Refer to [Optimize context](playground-context.md) for more information.

[Troubleshooting](playground-troubleshooting.md) provides tips on how to diagnose and fix relevance issues.

::::{note}
Playground uses the [`retriever`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-retriever) syntax for {{es}} queries. Retrievers make it easier to compose and test different retrieval strategies in your search pipelines. Refer to [documentation](/solutions/search/querying-for-search.md) for a high level overview of retrievers.

::::



## Hidden fields [playground-hidden-fields]

The query editor shows fields which make sense for the user to search on, but not all fields in your documents are visible from the editor.

Available field types:

* Semantic fields like `sparse_vector` or `dense_vector` fields where the embeddings have been created from a inference processor
* `text` fields

Hidden Field Types:

* non `text` fields like `keyword` fields
* fields that are not indexed
* semantic fields where the embeddings have not been created from a inference processor
* nested fields

