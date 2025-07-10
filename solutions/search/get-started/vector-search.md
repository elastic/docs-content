---
navigation_title: Vector search
description: An introduction to vectors and knn search in Elasticsearch.
applies_to:
  serverless: all
  stack: all
products:
  - id: elasticsearch
---
# Get started with vector search

{{es}} enables you to generate mathematical representations of your content called _embeddings_ or _vectors_.
There are two types of representation (_dense_ and _sparse_), which are suited to different types of queries and use cases (for example, finding similar images and content or storing expanded terms and weights).
In this introduction to vector search, you'll store and search for [dense vectors](/solutions/search/vector/dense-vector.md).
The primary use case for dense vectors is to find pieces of content with similar meanings by using mathematical functions, in this case an [approximate k-nearest neighbour](/solutions/search/vector/knn.md) (kNN) search.

To learn more about which type of vector is appropriate for your use case, check out [](/solutions/search/vector.md).
For an overview of the differences between semantic search and vector search, go to [](/solutions/search/ai-search/ai-search.md).

<!--
In this quickstart guide, you'll create vectors for a small set of sample data, store them in {{es}}, then run a semantic query.
By playing with a simple use case, you'll take the first steps toward understanding whether it's applicable to your own data.
-->

## Prerequisites

- If you're using [{{es-serverless}}](/solutions/search/serverless-elasticsearch-get-started.md), create a project that is optimized for vectors. To add the sample data, you must have a `developer` or `admin` predefined role or an equivalent custom role.
- If you're using [{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md) or [running {{es}} locally](/solutions/search/run-elasticsearch-locally.md), start {{es}} and {{kib}}. To add the sample data, log in with a user that has the `superuser` built-in role.
  
To learn about role-based access control, check out [](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md).

<!--
To try out vector search, [create an {{es-serverless}} project](/solutions/search/serverless-elasticsearch-get-started.md#elasticsearch-get-started-create-project) that is optimized for vectors.
-->

## Create a vector database

<!--
TBD: What type of data is ideal for vector search?
In addition, Elastic supports kNN vectors to implement similarity search on unstructured data beyond text, such as videos, images, and audio.
-->

<!-- 
When you create vectors (or _vectorize_ your data), you convert complex and nuanced documents into multidimensional numerical representations.
You can choose from many different vector embedding models. Some are extremely hardware efficient and can be run with less computational power. Others have a greater understanding of the context, can answer questions, and lead a threaded conversation.
The examples in this guide use the default Learned Sparse Encoder ([ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md)) model, which provides great relevance across domains without the need for additional fine tuning.

The way that you store vectors has a significant impact on the performance and accuracy of search results.
They must be stored in specialized data structures designed to ensure efficient similarity search and speedy vector distance calculations.
This guide uses the [semantic text field type](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md), which provides sensible defaults and automation.
-->
:::::{stepper}
::::{step} Create an index

An index is a collection of documents uniquely identified by a name or an alias.
You can follow the guided index workflow:

- If you're using {{es-serverless}}, go to **{{es}} > Home**, select the vector search workflow, and **Create a vector optimized index**.
- If you're using {{ech}} or running {{es}} locally, go to **{{es}} > Home** and click **Create API index**. Select the vector search workflow.

When you complete the workflow, you will have sample data and can skip to the steps related to exploring and searching it.
Alternatively, run the following API request in [Console](/explore-analyze/query-filter/tools/console.md):

```console
PUT /vector-index
```

:::{tip}
For an introduction to the concept of indices, check out [](/manage-data/data-store/index-basics.md).
:::
::::
::::{step} Create a dense vector field mapping

Each index has mappings that define how data is stored and indexed, like a schema in a relational database.

The following example defines two fields: a three-dimensional [dense_vector field](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) and a text field.

```console
PUT /vector-index/_mapping
{
  "properties": {
    "vector": {
      "type": "dense_vector",
      "dims": 3
    },
    "content": {
      "type": "text"
    }
  }
}
```

For a deeper dive, check out [Mapping embeddings to Elasticsearch field types: semantic_text, dense_vector, sparse_vector](https://www.elastic.co/search-labs/blog/mapping-embeddings-to-elasticsearch-field-types).
::::
::::
::::{step} Add documents

You can use the Elasticsearch bulk API to ingest an array of documents:

```console
POST /_bulk?pretty
{ "index": { "_index": "vector-index" } }
{"vector":[5.936,3.083,5.087],"content":"Yellowstone National Park is one of the largest national parks in the United States. It ranges from the Wyoming to Montana and Idaho, and contains an area of 2,219,791 acress across three different states. Its most famous for hosting the geyser Old Faithful and is centered on the Yellowstone Caldera, the largest super volcano on the American continent. Yellowstone is host to hundreds of species of animal, many of which are endangered or threatened. Most notably, it contains free-ranging herds of bison and elk, alongside bears, cougars and wolves. The national park receives over 4.5 million visitors annually and is a UNESCO World Heritage Site."}
{ "index": { "_index": "vector-index" } }
{"vector":[4.938,7.78,3.88],"content":"Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face."}
{ "index": { "_index": "vector-index" } }
{"vector":[9.863,8.919,2.368],"content":"Rocky Mountain National Park  is one of the most popular national parks in the United States. It receives over 4.5 million visitors annually, and is known for its mountainous terrain, including Longs Peak, which is the highest peak in the park. The park is home to a variety of wildlife, including elk, mule deer, moose, and bighorn sheep. The park is also home to a variety of ecosystems, including montane, subalpine, and alpine tundra. The park is a popular destination for hiking, camping, and wildlife viewing, and is a UNESCO World Heritage Site."}
```

In this example, the vectors are provided in each document.
In a real-world scenario, you could generate the vectors as you added data by using an ingest pipeline with an inference processor.
::::
<!--
::::{step} Explore the data
::::
-->
## Test vector search

<!--
When you run a semantic search, the text in your query must be turned into vectors that use the same embedding model as your vector database.
This step is performed automatically when you use `semantic_text` fields.
You therefore only need to pick a query language and a method for comparing the vectors.
-->
<!--
:::::{stepper}
::::{step} Choose a query language
::::
-->
<!--
::::{step} Choose a vector comparison method
::::
-->
Now try a query to get the documents that are closest to a vector.
For example, use a knn query with a vector `[2,6,0]`:

```console
GET vector-search/_search
{
 "knn": {
   "field": "vector",
   "k": 10,
   "num_candidates": 100,
   "query_vector": [2,6,0]
 }
}
```
<!--
::::{step} Analyze the results
::::
-->
The search results are sorted by relevance score, which measures how well each document matches the query.
For example:

```json
{
  "took": 9,
  "timed_out": false,
  "_shards": {
    "total": 3,
    "successful": 3,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 0.95106244,
    "hits": [
      {
        "_index": "search-05ro",
        "_id": "QZqVqZcBabT17nUqiiKf",
        "_score": 0.95106244,
        "_source": {
          "vector": [
            4.938,
            7.78,
            3.88
          ],
          "content": "Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face."
        }
      },
    ...
```

<!--
TBD: Provide more information about how to interpret and filter the search results.

The example in the UI is this, however model_id cannot be null so it's incomplete as-is:

```console
POST /vector-index/_search
{
  "retriever": {
    "standard": {
      "query": {
        "knn": {
          "field": "vector",
          "num_candidates": 100,
          "query_vector_builder": {
            "text_embedding": {
              "model_id": "",
              "model_text": "REPLACE WITH YOUR QUERY"
            }
          }
        }
      }
    }
  }
```
-->
<!--
When you finish your tests and no longer need the sample data set, delete the index:

```console
DELETE /semantic-index
```
-->

## Next steps

Thanks for taking the time to try out vector search.
For another dense vector example, check out [](/solutions/search/vector/bring-own-vectors.md).
For an example of using pipelines to generate text embeddings, check out [](/solutions/search/vector/dense-versus-sparse-ingest-pipelines.md).

To learn about more options, such as semantic and keyword search, go to [](/solutions/search/search-approaches.md).
For a summary of the AI-powered search use cases, go to [](/solutions/search/ai-search/ai-search.md).

<!--
Choose from several memory quantization strategies to reduce bloat.
-->
