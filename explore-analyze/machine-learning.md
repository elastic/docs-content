---
applies:
  stack:
  serverless:
navigation_title: Machine learning
mapped_urls:
  - https://www.elastic.co/guide/en/machine-learning/current/index.html
  - https://www.elastic.co/guide/en/machine-learning/current/machine-learning-intro.html
  - https://www.elastic.co/guide/en/serverless/current/machine-learning.html
---

# What is Elastic Machine Learning? [machine-learning-intro]

{{ml-cap}} features analyze your data and generate models for its patterns of behavior. The type of analysis that you choose depends on the questions or problems you want to address and the type of data you have available.

## Unsupervised {{ml}} [machine-learning-unsupervised]

There are two types of analysis that can deduce the patterns and relationships within your data without training or intervention: *{{anomaly-detect}}* and *{{oldetection}}*.

[{{anomaly-detect-cap}}](machine-learning/anomaly-detection.md) requires time series data. It constructs a probability model and can run continuously to identify unusual events as they occur. The model evolves over time; you can use its insights to forecast future behavior.

[{{oldetection-cap}}](machine-learning/data-frame-analytics/ml-dfa-finding-outliers.md) does not require time series data. It is a type of {{dfanalytics}} that identifies unusual points in a data set by analyzing how close each data point is to others and the density of the cluster of points around it. It does not run continuously; it generates a copy of your data set where each data point is annotated with an {{olscore}}. The score indicates the extent to which a data point is an outlier compared to other data points.

## Supervised {{ml}} [machine-learning-supervised]

There are two types of {{dfanalytics}} that require training data sets: *{{classification}}* and *{{regression}}*.

In both cases, the result is a copy of your data set where each data point is annotated with predictions and a trained model, which you can deploy to make predictions for new data. For more information, refer to [Introduction to supervised learning](machine-learning/data-frame-analytics/ml-dfa-overview.md#ml-supervised-workflow).

[{{classification-cap}}](machine-learning/data-frame-analytics/ml-dfa-classification.md) learns relationships between your data points in order to predict discrete categorical values, such as whether a DNS request originates from a malicious or benign domain.

[{{regression-cap}}](machine-learning/data-frame-analytics/ml-dfa-regression.md) learns relationships between your data points in order to predict continuous numerical values, such as the response time for a web request.

## Feature availability by project type [machine-learning-serverless-availability]

The {{ml-features}} that are available vary by project type:

* {{es-serverless}} projects have trained models.
* {{observability}} projects have {{anomaly-jobs}}.
* {{elastic-sec}} projects have {{anomaly-jobs}}, {{dfanalytics-jobs}}, and trained models.

## Synchronize saved objects [machine-learning-synchronize-saved-objects]

Before you can view your {{ml}} {dfeeds}, jobs, and trained models in {{kib}}, they must have saved objects. For example, if you used APIs to create your jobs, wait for automatic synchronization or go to the **{{ml-app}}** page and click **Synchronize saved objects**.

## Export and import jobs [machine-learning-export-and-import-jobs]

You can export and import your {{ml}} job and {{dfeed}} configuration details on the **{{ml-app}}** page. For example, you can export jobs from your test environment and import them in your production environment.

The exported file contains configuration details; it does not contain the {{ml}} models. For {{anomaly-detect}}, you must import and run the job to build a model that is accurate for the new environment. For {{dfanalytics}}, trained models are portable; you can import the job then transfer the model to the new cluster. Refer to [Exporting and importing {{dfanalytics}} trained models](machine-learning/data-frame-analytics/ml-trained-models.md#export-import).

There are some additional actions that you must take before you can successfully import and run your jobs:

* The {{data-sources}} that are used by {{anomaly-detect}} {dfeeds} and {{dfanalytics}} source indices must exist; otherwise, the import fails.
* If your {{anomaly-jobs}} use custom rules with filter lists, the filter lists must exist; otherwise, the import fails.
* If your {{anomaly-jobs}} were associated with calendars, you must create the calendar in the new environment and add your imported jobs to the calendar.