---
navigation_title: Semantic search
description: An introduction to semantic search in Elasticsearch.
applies_to:
  serverless: all
  stack: all
products:
  - id: elasticsearch
---
# Get started with semantic search

_Semantic search_ is a type of AI-powered search that enables you to use natural language in your queries.
It returns results that match the meaning of a query, as opposed to literal keyword matches.
For example, if you want to search for workplace guidelines on a second income, you could search for "side hustle", which is not a term you're likely to see in a formal HR document.

Semantic search uses {{es}} [vector database](https://www.elastic.co/what-is/vector-database) and [vector search](https://www.elastic.co/what-is/vector-search) technology.
Each _vector_ (or _vector embedding_) is an array of numbers that represent different characteristics of the text, such as sentiment, context, and syntactics.
These numeric representations make vector comparisons very efficient.

In this quickstart guide, you'll create vectors for a small set of sample data, store them in {{es}}, then run a semantic query.
By playing with a simple use case, you'll take the first steps toward understanding whether it's applicable to your own data.

## Prerequisites

- If you're using [{{es-serverless}}](/solutions/search/serverless-elasticsearch-get-started.md), create a project that is optimized for vectors. To add the sample data, you must have a `developer` or `admin` predefined role or an equivalent custom role.
- If you're [running {{es}} locally](/solutions/search/run-elasticsearch-locally.md), start {{es}} and {{kib}}. To add the sample data, log in with a user that has the `superuser` built-in role, such as `elastic`.
  
To learn about role-based access control, check out [](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md).

<!--
TBD: What is the impact of this "optimized for vectors" option?
-->

## Create a vector database

When you create vectors (or _vectorize_ your data), you convert complex and nuanced documents into multidimensional numerical representations.
You can choose from many different vector embedding models. Some are extremely hardware efficient and can be run with less computational power. Others have a greater understanding of the context, can answer questions, and lead a threaded conversation.
The examples in this guide use the default Learned Sparse Encoder ([ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md)) model, which provides great relevance across domains without the need for additional fine tuning.

The way that you store vectors has a significant impact on the performance and accuracy of search results.
They must be stored in specialized data structures designed to ensure efficient similarity search and speedy vector distance calculations.
This guide uses the [semantic text field type](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md), which provide sensible defaults and automation.

Try vectorizing a small set of documents.
You can follow the guided index workflow:

- If you're using {{es-serverless}}, go to **{{es}} > Home**, select the semantic search workflow, and click **Create a semantic optimized index**.
- If you're running {{es}} locally, go to **{{es}} > Home** and click **Create API index**. Select the semantic search workflow.

Alternatively, run the following API requests in the [Console](/explore-analyze/query-filter/tools/console.md):

:::::{stepper}
::::{step} Create a semantic_text field mapping

The following example creates a mapping for a single field ("content"):

```console
PUT /semantic-index/_mapping
{
  "properties": {
    "content": {
      "type": "semantic_text"
    }
  }
}
```

When you use `semantic_text` fields, the type of vector is determined by the vector embedding model.
In this case, the default ELSER model will be used to create sparse vectors.

For a deeper dive, check out [Mapping embeddings to Elasticsearch field types: semantic_text, dense_vector, sparse_vector](https://www.elastic.co/search-labs/blog/mapping-embeddings-to-elasticsearch-field-types).
::::

::::{step} Add documents

You can use the Elasticsearch bulk API to ingest an array of documents:

```console
POST /_bulk?pretty
{ "index": { "_index": "semantic-index" } }
{"content":"Yellowstone National Park is one of the largest national parks in the United States. It ranges from the Wyoming to Montana and Idaho, and contains an area of 2,219,791 acress across three different states. Its most famous for hosting the geyser Old Faithful and is centered on the Yellowstone Caldera, the largest super volcano on the American continent. Yellowstone is host to hundreds of species of animal, many of which are endangered or threatened. Most notably, it contains free-ranging herds of bison and elk, alongside bears, cougars and wolves. The national park receives over 4.5 million visitors annually and is a UNESCO World Heritage Site."}
{ "index": { "_index": "semantic-index" } }
{"content":"Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face."}
{ "index": { "_index": "semantic-index" } }
{"content":"Rocky Mountain National Park  is one of the most popular national parks in the United States. It receives over 4.5 million visitors annually, and is known for its mountainous terrain, including Longs Peak, which is the highest peak in the park. The park is home to a variety of wildlife, including elk, mule deer, moose, and bighorn sheep. The park is also home to a variety of ecosystems, including montane, subalpine, and alpine tundra. The park is a popular destination for hiking, camping, and wildlife viewing, and is a UNESCO World Heritage Site."}
```

The bulk ingestion might take longer than the default request timeout.
If it times out, wait for the ELSER model to load (typically 1-5 minutes) then retry it.
::::
:::::

What just happened? The content was transformed into sparse vectors, which involves two main steps.
First, the content was divided into smaller, manageable chunks to ensure that meaningful segments can be more effectively processed and searched.
Then each chunk of text was transformed into a sparse vector representation using text expansion techniques.

![Semantic search chunking](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt9bbe5e260012b15d/67ffffc8165067d96124b586/animated-gif-semantic-search-chunking.gif)

With a few vectors stored in {{es}}, semantic search can now occur.

## Explore the data

To familiarize yourself with this data set, open [Discover](/explore-analyze/discover.md) from the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

In **Discover**, you can click the expand icon ![double arrow icon to open a flyout with the document details](/explore-analyze/images/kibana-expand-icon-2.png "") to show details about documents in the table.

:::{image} /solutions/images/serverless-discover-semantic.png
:screenshot:
:alt: Discover table view with document expanded
:::

For more tips, check out [](/explore-analyze/discover/discover-get-started.md).

## Test semantic search

{{es}} provides a variety of query languages for interacting with your data.
For an overview of their features and use cases, check out [](/explore-analyze/query-filter/languages.md).

You can search data that is stored in `semantic_text` fields by using a specific subset of queries, including  `knn`, `match`, `semantic`, and `sparse_vector`.
The query is translated automatically into the appropriate vector representation to run against the contents of the semantic text field.
The search results include a relevance score, which measures how well each document matches the query.

Let's test a semantic search query in [Elasticsearch Query Language](/explore-analyze/query-filter/languages/esql.md) (ES|QL).
Go to **Discover** and select **Try ES|QL** from the application menu bar.
Think of some queries that are relevant to the documents you explored, such as finding the biggest park or the best for rappelling.
For example, copy the following query:

```esql
FROM semantic-index METADATA _score <1>
  | WHERE content: "what's the biggest park?" <2>
  | KEEP content, _score <3>
  | SORT _score DESC <4>
  | LIMIT 1000 <5>
```

1. The FROM source command returns a table of data. Each row in the table represents a document. The `METADATA` clause provides access to the query relevance score, which is a [metadata field](elasticsearch://reference/query-languages/esql/esql-metadata-fields.md).
2. A simplified syntax for the [match](elasticsearch://reference/query-languages/esql/functions-operators/search-functions.md#esql-match) search function, this command performs a semantic query on the specified field.
3. The KEEP processing command affects the columns and their order in the results table.
4. The results are sorted in descending order based on the `_score`.
5. This optional command defines the maximum number of rows to return.

After you click **▶Run**, the results appear in a table.
In this example, the first row in the table is the document related to Yellowstone National Park, which had the highest relevance score for the query.

:::{image} /solutions/images/serverless-discover-esql.png
:screenshot:
:alt: Run an ES|QL semantic query in Discover
:::

<!--
TBD: Run the same query in Console
-->

To learn more, check out [](/explore-analyze/discover/try-esql.md) and [](/solutions/search/esql-for-search.md).

## Next steps

Thanks for taking the time to try out semantic search in {{es-serverless}}.
For a deeper dive, go to [](/solutions/search/semantic-search.md).

If you want to extend this example, try an index with more fields.
For example, if you have both a `text` field and a `semantic_text` field, you can combine the strengths of traditional keyword search and advanced semantic search.
A [hybrid search](/solutions/search/hybrid-semantic-text.md) provides comprehensive search capabilities to find relevant information based on both the raw text and its underlying meaning.

To learn about more options, such as vector and keyword search, go to [](/solutions/search/search-approaches.md).
For a summary of the AI-powered search use cases, go to [](/solutions/search/ai-search/ai-search.md).
