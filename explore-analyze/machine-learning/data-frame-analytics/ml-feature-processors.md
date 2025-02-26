---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Feature processors"
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-feature-processors.html
---

# Feature processors [ml-feature-processors]

{{dfanalytics-cap}} automatically includes a [Feature encoding](ml-feature-encoding.md) phase, which transforms categorical features into numerical ones. If you want to have more control over the encoding methods that are used for specific fields, however, you can define  feature processors. If there are any remaining categorical features after your processors run, they are addressed in the automatic feature encoding phase.

The feature processors that you defined are the part of the analytics process, when data comes through the aggregation or pipeline, the processors run against the new data. The resulting features are ephemeral; they are not stored in the index. This provides a mechanism to create features that can be used at search and ingest time and don’t take up space in the index.

Refer to the `feature_processors` property of the [Create {{dfanalytics-job}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-data-frame-analytics) to learn more.

Available feature processors:

* [Frequency encoding](https://www.elastic.co/guide/en/machine-learning/current/frequency-encoding.html)
* [Multi encoding](https://www.elastic.co/guide/en/machine-learning/current/multi-encoding.html)
* [n-gram encoding](https://www.elastic.co/guide/en/machine-learning/current/ngram-encoding.html)
* [One hot encoding](https://www.elastic.co/guide/en/machine-learning/current/one-hot-encoding.html)
* [Target mean encoding](https://www.elastic.co/guide/en/machine-learning/current/target-mean-encoding.html)
