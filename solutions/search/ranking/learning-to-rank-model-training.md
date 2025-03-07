---
navigation_title: "Deploy and manage LTR models"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/learning-to-rank-model-training.html
applies_to:
  stack:
  serverless:
---



# Deploy and manage LTR models [learning-to-rank-model-training]


::::{note}
This feature was introduced in version 8.12.0 and is only available to certain subscription levels. For more information, see {{subscriptions}}.
::::



## Train and deploy a model using Eland [learning-to-rank-model-training-workflow]

Typically, the [XGBoost](https://xgboost.readthedocs.io/en/stable/) model training process uses standard Python data science tools like Pandas and scikit-learn.

We have developed an [example notebook](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/08-learning-to-rank.ipynb) available in the `elasticsearch-labs` repo. This interactive Python notebook details an end-to-end model training and deployment workflow.

We highly recommend using [eland](https://eland.readthedocs.io/) in your workflow, because it provides important functionalities for working with LTR in {{es}}. Use eland to:

* Configure feature extraction
* Extract features for training
* Deploy the model in {{es}}


### Configure feature extraction in Eland [learning-to-rank-model-training-feature-definition]

Feature extractors are defined using templated queries. [Eland](https://eland.readthedocs.io/) provides the `eland.ml.ltr.QueryFeatureExtractor` to define these feature extractors directly in Python:

```python
from eland.ml.ltr import QueryFeatureExtractor

feature_extractors=[
    # We want to use the BM25 score of the match query for the title field as a feature:
    QueryFeatureExtractor(
        feature_name="title_bm25",
        query={"match": {"title": "{{query}}"}}
    ),
    # We want to use the number of matched terms in the title field as a feature:
    QueryFeatureExtractor(
        feature_name="title_matched_term_count",
        query={
            "script_score": {
                "query": {"match": {"title": "{{query}}"}},
                "script": {"source": "return _termStats.matchedTermsCount();"},
            }
        },
    ),
    # We can use a script_score query to get the value
    # of the field rating directly as a feature:
    QueryFeatureExtractor(
        feature_name="popularity",
        query={
            "script_score": {
                "query": {"exists": {"field": "popularity"}},
                "script": {"source": "return doc['popularity'].value;"},
            }
        },
    ),
    # We extract the number of terms in the query as feature.
   QueryFeatureExtractor(
        feature_name="query_term_count",
        query={
            "script_score": {
                "query": {"match": {"title": "{{query}}"}},
                "script": {"source": "return _termStats.uniqueTermsCount();"},
            }
        },
    ),
]
```
%  NOTCONSOLE

::::{admonition} Term statistics as features
:class: note

It is very common for an LTR model to leverage raw term statistics as features. To extract this information, you can use the [term statistics feature](../../../explore-analyze/scripting/modules-scripting-fields.md#scripting-term-statistics) provided as part of the  [`script_score`](elasticsearch://reference/query-languages/query-dsl-script-score-query.md) query.

::::


Once the feature extractors have been defined, they are wrapped in an `eland.ml.ltr.LTRModelConfig` object for use in later training steps:

```python
from eland.ml.ltr import LTRModelConfig

ltr_config = LTRModelConfig(feature_extractors)
```
%  NOTCONSOLE


### Extracting features for training [learning-to-rank-model-training-feature-extraction]

Building your dataset is a critical step in the training process. This involves extracting relevant features and adding them to your judgment list. We recommend using Eland’s `eland.ml.ltr.FeatureLogger` helper class for this process.

```python
from eland.ml.ltr import FeatureLogger

# Create a feature logger that will be used to query {{es}} to retrieve the features:
feature_logger = FeatureLogger(es_client, MOVIE_INDEX, ltr_config)
```

The FeatureLogger provides an `extract_features` method which enables you to extract features for a list of specific documents from your judgment list. At the same time, you can pass query parameters to the feature extractors defined earlier:

```python
feature_logger.extract_features(
    query_params={"query": "foo"},
    doc_ids=["doc-1", "doc-2"]
)
```
%  NOTCONSOLE

Our [example notebook](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/08-learning-to-rank.ipynb) explains how to use the `FeatureLogger` to build a training dataset, by adding features to a judgment list.


#### Notes on feature extraction [learning-to-rank-model-training-feature-extraction-notes]

* We strongly advise against implementing feature extraction on your own. It’s crucial to maintain consistency in feature extraction between the training environment and inference in {{es}}. By using eland tooling, which is developed and tested in tandem with {{es}}, you can ensure that they function together consistently.
* Feature extraction is performed by executing queries on the {{es}} server. This could put a lot of stress on your cluster, especially when your judgment list contains a lot of examples or you have many features. Our feature logger implementation is designed to minimize the number of search requests sent to the server and reduce load. However, it might be best to build your training dataset using an {{es}} cluster that is isolated from any user-facing, production traffic.


### Deploy your model into {{es}} [learning-to-rank-model-deployment]

Once your model is trained you will be able to deploy it in your {{es}} cluster. You can use Eland’s `MLModel.import_ltr_model method`:

```python
from eland.ml import MLModel

LEARNING_TO_RANK_MODEL_ID="ltr-model-xgboost"

MLModel.import_ltr_model(
    es_client=es_client,
    model=ranker,
    model_id=LEARNING_TO_RANK_MODEL_ID,
    ltr_model_config=ltr_config,
    es_if_exists="replace",
)
```
%  NOTCONSOLE

This method will serialize the trained model and the Learning To Rank configuration (including feature extraction) in a format that {{es}} can understand. The model is then deployed to {{es}} using the [Create Trained Models API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-trained-model).

The following types of models are currently supported for LTR with {{es}}:

* [`DecisionTreeRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html)
* [`RandomForestRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)
* [`LGBMRegressor`](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMRegressor.html)
* [`XGBRanker`](https://xgboost.readthedocs.io/en/stable/python/python_api.html#xgboost.XGBRanker)
* [`XGBRegressor`](https://xgboost.readthedocs.io/en/stable/python/python_api.html#xgboost.XGBRegressor)

More model types will be supported in the future.


## Learning To Rank model management [learning-to-rank-model-management]

Once your model is deployed in {{es}} you can manage it using the [trained model APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ml-trained-model). You’re now ready to work with your LTR model as a rescorer at [search time](learning-to-rank-search-usage.md).

