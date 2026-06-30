---
navigation_title: API quick reference
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-dfanalytics-apis.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Data frame analytics API quick reference [ml-dfanalytics-apis]

All {{dfanalytics}} endpoints have the following base:

```js
/_ml/data_frame/analytics
```

The evaluation API endpoint has the following base:

```js
/_ml/data_frame/_evaluate
```

* [Create {{dfanalytics-jobs}}]({{es-apis}}operation/operation-ml-put-data-frame-analytics)
* [Delete {{dfanalytics-jobs}}]({{es-apis}}operation/operation-ml-delete-data-frame-analytics)
* [Evaluate {{dfanalytics}}]({{es-apis}}operation/operation-ml-evaluate-data-frame)
* [Explain {{dfanalytics}}]({{es-apis}}operation/operation-ml-explain-data-frame-analytics)
* [Get {{dfanalytics-jobs}} info]({{es-apis}}operation/operation-ml-get-data-frame-analytics)
* [Get {{dfanalytics-jobs}} statistics]({{es-apis}}operation/operation-ml-get-data-frame-analytics-stats)
* [Preview {{dfanalytics}}]({{es-apis}}operation/operation-ml-preview-data-frame-analytics)
* [Start {{dfanalytics-jobs}}]({{es-apis}}operation/operation-ml-start-data-frame-analytics)
* [Stop {{dfanalytics-jobs}}]({{es-apis}}operation/operation-ml-stop-data-frame-analytics)
* [Update {{dfanalytics-jobs}}]({{es-apis}}operation/operation-ml-update-data-frame-analytics)

For information about the APIs related to trained models, refer to [*API quick reference*](../nlp/ml-nlp-apis.md).
