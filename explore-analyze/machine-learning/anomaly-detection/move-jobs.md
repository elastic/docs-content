---
navigation_title: Exporting and importing machine learning jobs
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/move-jobs.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Exporting and importing machine learning jobs [move-jobs]

In {{kib}}, you can export and import your {{ml}} job and {{dfeed}} configuration details in **{{stack-manage-app}} > {{ml-app}} Jobs**. For example, you can export jobs from your test environment and import them into your production environment.

The exported file contains configuration details; it does not contain the {{ml}} models. For {{anomaly-detect}}, you must import and run the job to build a model that is accurate for the new environment. For {{dfanalytics}}, trained models are portable and can be transferred between clusters as described in [Exporting and importing models](../data-frame-analytics/ml-trained-models.md#export-import).

There are some additional actions that you must take before you can successfully import and run your jobs:

1. The {{kib}} [{{data-sources}}](/explore-analyze/find-and-organize/data-views.md) that are used by {{anomaly-detect}} {{dfeeds}} and {{dfanalytics}} source indices must exist; otherwise, the import fails.
2. If your {{anomaly-jobs}} use [custom rules](ml-configuring-detector-custom-rules.md) with filter lists, the filter lists must exist; otherwise, the import fails. To create filter lists, use {{kib}} or the [create filters API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-filter).
3. If your {{anomaly-jobs}} were associated with [calendars](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md#ml-ad-calendars), you must create the calendar in the new environment and add your imported jobs to the calendar. Use {{kib}} or the [create calendars](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-calendar), [add events to calendar](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-post-calendar-events), and [add jobs to calendar](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-calendar-job) APIs.
