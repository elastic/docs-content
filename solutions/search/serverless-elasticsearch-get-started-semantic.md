---
navigation_title: Semantic search
applies_to:
  serverless:
products:
  - id: cloud-serverless
---
# Build an AI-powered search experience in {{es-serverless}}

<!--
As you ramp up on Elastic, you'll use the Elasticsearch Relevance Engine™ (ESRE), designed to power AI search applications. With ESRE, you can take advantage of a suite of developer tools including Elastic's textual search, vector database, and our proprietary transformer model for semantic search.
-->

Elastic offers a variety of search techniques, starting with BM25, the industry standard for textual search.
It provides precise matching for specific searches, matching exact keywords, and it improves with tuning.

<!--
As you get started on vector search, keep in mind there are two forms of vector search: “dense” (aka, kNN vector search) and “sparse."
TBD: Which type is implemented when you use semantic_text field?
-->

Elastic also offers an out-of-the-box Learned Sparse Encoder model for semantic search.
This model outperforms on a variety of data sets, such as financial data, weather records, and question-answer pairs, among others.
The model is built to provide great relevance across domains, without the need for additional fine tuning.

<!--
Check out this interactive demo to see how search results are more relevant when you test Elastic's Learned Sparse Encoder model against Elastic's textual BM25 algorithm.

In addition, Elastic also supports dense vectors to implement similarity search on unstructured data beyond text, such as videos, images, and audio.
-->

The advantage of [AI-powered search](/solutions/search/ai-search/ai-search.md) is that these technologies enable you to use intuitive language in your search queries.
For example, if you want to search for workplace guidelines on a second income, you could search for "side hustle", which is not a term you're likely to see in a formal HR document.

To try it out, [create an {{es-serverless}} project](/solutions/search/serverless-elasticsearch-get-started.md#elasticsearch-get-started-create-project) that is optimized for vectors.

% TBD: It seems like semantic search fields exist in all, so what is the value of this option?

## Add data

% TBD: What type of data is ideal for semantic search?

There are some simple data sets that you can use for learning purposes.
For example, if you follow the [guided index flow](/solutions/search/serverless-elasticsearch-get-started.md#elasticsearch-follow-guided-index-flow), you can choose the semantic search option.
Follow the instructions to install an {{es}} client and define field mappings or try out the API requests in the [Console](/explore-analyze/query-filter/tools/console.md):

```console
PUT /my-index/_mapping
{
  "properties": {
    "text": {
      "type": "semantic_text"
    }
  }
}
```

By default, thee [semantic_text](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type provides vector search capabilities using the ELSER model.
% TBD: Confirm "Elser model" vs ".elser-2-elasticsearch, a preconfigured endpoint for the elasticsearch service".

Next, use the Elasticsearch bulk API to ingest an array of documents into the index.
The initial bulk ingestion request could take longer than the default request timeout.
If the following request times out, allow time for the machine learning model loading to complete (typically 1-5 minutes) then retry it:

<!--
TBD: Describe where to look for the downloaded model in Trained Models?
-->

```console
POST /_bulk?pretty
{ "index": { "_index": "my-index" } }
{"text":"Yellowstone National Park is one of the largest national parks in the United States. It ranges from the Wyoming to Montana and Idaho, and contains an area of 2,219,791 acress across three different states. Its most famous for hosting the geyser Old Faithful and is centered on the Yellowstone Caldera, the largest super volcano on the American continent. Yellowstone is host to hundreds of species of animal, many of which are endangered or threatened. Most notably, it contains free-ranging herds of bison and elk, alongside bears, cougars and wolves. The national park receives over 4.5 million visitors annually and is a UNESCO World Heritage Site."}
{ "index": { "_index": "my-index" } }
{"text":"Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face."}
{ "index": { "_index": "my-index" } }
{"text":"Rocky Mountain National Park  is one of the most popular national parks in the United States. It receives over 4.5 million visitors annually, and is known for its mountainous terrain, including Longs Peak, which is the highest peak in the park. The park is home to a variety of wildlife, including elk, mule deer, moose, and bighorn sheep. The park is also home to a variety of ecosystems, including montane, subalpine, and alpine tundra. The park is a popular destination for hiking, camping, and wildlife viewing, and is a UNESCO World Heritage Site."}
```

What just happened? The content was transformed into a sparse vector inside the `text` field.
This transformation involves two main steps.
First, the content is divided into smaller, manageable chunks to ensure that meaningful segments can be more effectively processed and searched. Next, each chunk of text is transformed into a sparse vector representation using text expansion techniques.
This step leverages ELSER (Elastic Search Engine for Relevance) to convert the text into a format that captures the semantic meaning, enabling more accurate and relevant search results.

## Test a semantic search query

Now try a semantic query:

```console
GET my-index/_search
{
  "query": {
    "semantic": {
      "field": "text",
      "query": "best parks for rappelling"
    }
  }
}
```

The query is translated automatically into a vector representation and runs against the contents of the semantic text field.
The search results are sorted by relevance score, which measures how well each document matches the query.
For example:

```json
{
  "took": 249,
  "timed_out": false,
  "_shards": {
    "total": 3,
    "successful": 3,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 6,
      "relation": "eq"
    },
    "max_score": 12.118624,
    "hits": [
      {
        "_index": "search-0lxc",
        "_id": "0lGtpJcB7hfWuB0FGC06",
        "_score": 12.118624,
        "_source": {
          "text": "Rocky Mountain National Park  is one of the most popular national parks in the United States. It receives over 4.5 million visitors annually, and is known for its mountainous terrain, including Longs Peak, which is the highest peak in the park. The park is home to a variety of wildlife, including elk, mule deer, moose, and bighorn sheep. The park is also home to a variety of ecosystems, including montane, subalpine, and alpine tundra. The park is a popular destination for hiking, camping, and wildlife viewing, and is a UNESCO World Heritage Site."
        }
      },
    ...
```

% TBD: Provide more information about how to interpret and filter the search results.

## Next steps

Thanks for taking the time to try out semantic search in {{es-serverless}}.
For another semantic search example, check out [](/solutions/search/semantic-search/semantic-search-semantic-text.md).

If you want to extend this example, try an index with more fields.
For example, if you have both a `text` field and a `semantic_text` field, you can combine the strengths of traditional keyword search and advanced semantic search.
A [hybrid search](/solutions/search/hybrid-semantic-text.md) provides comprehensive search capabilities to find relevant information based on both the raw text and its underlying meaning.

To learn about more options, such as vector and keyword search, check out [](/solutions/search/search-approaches.md).

