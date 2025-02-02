# {{ml-cap}} [machine-learning]

This content applies to:  [![Elasticsearch](../../../images/serverless-es-badge.svg "")](../../../solutions/search.md) [![Observability](../../../images/serverless-obs-badge.svg "")](../../../solutions/observability.md) [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md)

To view your {{ml}} resources, go to **{{project-settings}} → {{manage-app}} → {{ml-app}}**:

:::{image} ../../../images/serverless-ml-security-management.png
:alt: Anomaly detection job management
:class: screenshot
:::

The {{ml-features}} that are available vary by project type:

* {{es-serverless}} projects have trained models.
* {{observability}} projects have {{anomaly-jobs}}.
* {{elastic-sec}} projects have {{anomaly-jobs}}, {{dfanalytics-jobs}}, and trained models.

For more information, go to [{{anomaly-detect-cap}}](../../../explore-analyze/machine-learning/anomaly-detection.md), [{{dfanalytics-cap}}](../../../explore-analyze/machine-learning/data-frame-analytics.md) and [Natural language processing](../../../explore-analyze/machine-learning/nlp.md).


## Synchronize saved objects [machine-learning-synchronize-saved-objects]

Before you can view your {{ml}} {dfeeds}, jobs, and trained models in {{kib}}, they must have saved objects. For example, if you used APIs to create your jobs, wait for automatic synchronization or go to the **{{ml-app}}** page and click **Synchronize saved objects**.


## Export and import jobs [machine-learning-export-and-import-jobs]

You can export and import your {{ml}} job and {{dfeed}} configuration details on the **{{ml-app}}** page. For example, you can export jobs from your test environment and import them in your production environment.

The exported file contains configuration details; it does not contain the {{ml}} models. For {{anomaly-detect}}, you must import and run the job to build a model that is accurate for the new environment. For {{dfanalytics}}, trained models are portable; you can import the job then transfer the model to the new cluster. Refer to [Exporting and importing {{dfanalytics}} trained models](../../../explore-analyze/machine-learning/data-frame-analytics/ml-trained-models.md#export-import).

There are some additional actions that you must take before you can successfully import and run your jobs:

* The {{data-sources}} that are used by {{anomaly-detect}} {dfeeds} and {{dfanalytics}} source indices must exist; otherwise, the import fails.
* If your {{anomaly-jobs}} use custom rules with filter lists, the filter lists must exist; otherwise, the import fails.
* If your {{anomaly-jobs}} were associated with calendars, you must create the calendar in the new environment and add your imported jobs to the calendar.
