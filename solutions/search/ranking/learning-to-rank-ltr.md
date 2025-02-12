---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/learning-to-rank.html
applies:
  stack:
  serverless:
---

# Learning To Rank (LTR) [learning-to-rank]

::::{note}
This feature was introduced in version 8.12.0 and is only available to certain subscription levels. For more information, see {{subscriptions}}.
::::


Learning To Rank (LTR) uses a trained machine learning (ML) model to build a ranking function for your search engine. Typically, the model is used as a second stage re-ranker, to improve the relevance of search results returned by a simpler, first stage retrieval algorithm. The LTR function takes a list of documents and a search context and outputs ranked documents:

:::{image} ../../../images/elasticsearch-reference-learning-to-rank-overview.png
:alt: Learning To Rank overview
:title: Learning To Rank overview
:name: learning-to-rank-overview-diagram
:::


## Search context [learning-to-rank-search-context]

In addition to the list of documents to sort, the LTR function also requires a search context. Typically, this search context includes at least the search terms provided by the user (`text_query` in the example above). The search context can also provide additional information used in the ranking mode. This could be information about the user doing the search (such as demographic data, geolocation, or age); about the query (such as query length); or document in the context of the query (such as score for the title field).


## Judgment list [learning-to-rank-judgement-list]

The LTR model is usually trained on a judgment list, which is a set of queries and documents with a relevance grade. Judgment lists can be human or machine generated: they’re commonly populated from behavioural analytics, often with human moderation. Judgment lists determine the ideal ordering of results for a given search query. The goal of LTR is to fit the model to the judgment list rankings as closely as possible for new queries and documents.

The judgment list is the main input used to train the model. It consists of a dataset that contains pairs of queries and documents, along with their corresponding relevance labels. The relevance judgment is typically either a binary (relevant/irrelevant) or a more granular label, such as a grade between 0 (completely irrelevant) to 4 (highly relevant). The example below uses a graded relevance judgment.

:::{image} ../../../images/elasticsearch-reference-learning-to-rank-judgment-list.png
:alt: Judgment list example
:title: Judgment list example
:name: learning-to-rank-judgment-list-example
:::


### Notes on judgment lists [judgment-list-notes]

While a judgment list can be created manually by humans, there are techniques available to leverage user engagement data, such as clicks or conversions, to construct judgment lists automatically.

The quantity and the quality of your judgment list will greatly influence the overall performance of the LTR model. The following aspects should be considered very carefully when building your judgment list:

* Most search engines can be searched using different query types. For example, in a movie search engine, users search by title but also by actor or director. It’s essential to maintain a balanced number of examples for each query type in your judgment list. This prevents overfitting and allows the model to generalize effectively across all query types.
* Users often provide more positive examples than negative ones. By balancing the number of positive and negative examples, you help the model learn to distinguish between relevant and irrelevant content more accurately.


## Feature extraction [learning-to-rank-feature-extraction]

Query and document pairs alone don’t provide enough information to train the ML models used for LTR. The relevance scores in judgment lists depend on a number of properties or *features*. These features must be extracted to determine how the various components combine to determine document relevance. The judgment list plus the extracted features make up the training dataset for an LTR model.

These features fall into one of three main categories:

* **Document features**: These features are derived directly from document properties. Example: product price in an eCommerce store.
* **Query features**: These features are computed directly from the query submitted by the user. Example: the number of words in the query.
* **Query-document features**: Features used to provide information about the document in the context of the query. Example: the BM25 score for the `title` field.

To prepare the dataset for training, the features are added to the judgment list:

:::{image} ../../../images/elasticsearch-reference-learning-to-rank-feature-extraction.png
:alt: Judgment list with features
:title: Judgment list with features
:name: learning-to-rank-judgement-feature-extraction
:::

To do this in {{es}}, use templated queries to extract features when building the training dataset and during inference at query time. Here is an example of a templated query:

```js
[
  {
    "query_extractor": {
      "feature_name": "title_bm25",
      "query": { "match": { "title": "{{query}}" } }
    }
  }
]
```


## Models [learning-to-rank-models]

The heart of LTR is of course an ML model. A model is trained using the training data described above in combination with an objective. In the case of LTR, the objective is to rank result documents in an optimal way with respect to a judgment list, given some ranking metric such as [nDCG](https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval)#Discounted_cumulative_gain) or [MAP](https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval)#Mean_average_precision). The model relies solely on the features and relevance labels from the training data.

The LTR space is evolving rapidly and many approaches and model types are being experimented with. In practice {{es}} relies specifically on gradient boosted decision tree ([GBDT](https://en.wikipedia.org/wiki/Gradient_boosting#Gradient_tree_boosting)) models for LTR inference.

Note that {{es}} supports model inference but the training process itself must happen outside of {{es}}, using a GBDT model. Among the most popular LTR models used today, [LambdaMART](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/MSR-TR-2010-82.pdf) provides strong ranking performance with low inference latencies. It relies on GBDT models and is therefore a perfect fit for LTR in {{es}}.

[XGBoost](https://xgboost.readthedocs.io/en/stable/) is a well known library that provides an [implementation](https://xgboost.readthedocs.io/en/stable/tutorials/learning_to_rank.md) of LambdaMART, making it a popular choice for LTR. We offer helpers in [eland](https://eland.readthedocs.io/) to facilitate the integration of a trained [XBGRanker](https://xgboost.readthedocs.io/en/stable/python/python_api.md#xgboost.XGBRanker) model as your LTR model in {{es}}.

::::{tip}
Learn more about training in [Train and deploy a LTR model](learning-to-rank-model-training.md), or check out our [interactive LTR notebook](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/08-learning-to-rank.ipynb) available in the `elasticsearch-labs` repo.

::::



## LTR in the Elastic stack [learning-to-rank-in-the-elastic-stack]

In the next pages of this guide you will learn to:

* [Train and deploy a LTR model using `eland`](learning-to-rank-model-training.md)
* [Search using LTR model as a rescorer](learning-to-rank-search-usage.md)



