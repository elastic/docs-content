---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/playground-context.html
applies_to:
  stack: preview 9.0, beta 9.1
  serverless: beta
products:
  - id: kibana
---

# Optimize model context [playground-context]

::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::


Context is the information you provide to the LLM, to optimize the relevance of your query results. Without additional context, an LLM will generate results solely based on its training data. In Playground, this additional context is the information contained in your {{es}} indices.

There are a few ways to optimize this context for better results. Some adjustments can be made directly in the Playground UI. Others require refining your indexing strategy, and potentially reindexing your data.

::::{note} 
{applies_to}`stack: preview 9.0` Currently you can only select **one field** to be provided as context to the LLM.

::::



## Edit context in UI [playground-context-ui]
```{applies_to}
stack: preview 9.0.0
```

Use the **Playground context** section in the Playground UI to adjust the number of documents and fields sent to the LLM.

If you’re hitting context length limits, try the following:

* Limit the number of documents retrieved
* Pick a field with less tokens, reducing the context length


## Other context optimizations [playground-context-index] 

This section covers additional context optimizations that you won’t be able to make directly in the UI.


### Chunking large documents [playground-context-index-chunking] 

If you’re working with large fields, you may need to adjust your indexing strategy. Consider breaking your documents into smaller chunks, such as sentences or paragraphs.

If you don’t yet have a chunking strategy, start by chunking your documents into passages.

Otherwise, consider updating your chunking strategy, for example, from sentence based to paragraph based chunking.

Refer to the following Python notebooks for examples of how to chunk your documents:

* [JSON documents](https://github.com/elastic/elasticsearch-labs/tree/main/notebooks/ingestion-and-chunking/json-chunking-ingest.ipynb)
* [PDF document](https://github.com/elastic/elasticsearch-labs/tree/main/notebooks/ingestion-and-chunking/pdf-chunking-ingest.ipynb)
* [Website content](https://github.com/elastic/elasticsearch-labs/tree/main/notebooks/ingestion-and-chunking/website-chunking-ingest.ipynb)


### Optimizing context for cost and performance [playground-context-balance] 

The following recommendations can help you balance cost, latency, and result quality when working with different context sizes:

Optimize context length
:   Determine the optimal context length through empirical testing. Start with a baseline and adjust incrementally to find a balance that optimizes both response quality and system performance.

Implement token pruning for ELSER model
:   If you’re using our ELSER model, consider implementing token pruning to reduce the number of tokens sent to the model. Refer to these relevant blog posts:

    * [Optimizing retrieval with ELSER v2](https://www.elastic.co/search-labs/blog/introducing-elser-v2-part-2)
    * [Improving text expansion performance using token pruning](https://www.elastic.co/search-labs/blog/text-expansion-pruning)

Monitor and adjust
:   Continuously monitor the effects of context size changes on performance and adjust as necessary.

