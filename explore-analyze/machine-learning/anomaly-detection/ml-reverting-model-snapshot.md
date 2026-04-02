---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-reverting-model-snapshot.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Reverting to a model snapshot [ml-reverting-model-snapshot]

[Snapshots of the {{ml}} model](ml-ad-run-jobs.md#ml-ad-model-snapshots) for each {{anomaly-job}} are saved frequently to an internal {{es}} index to ensure resilience. It makes it possible to reset the model to a previous state in case of a system failure or if the model changed significantly due to a one-off event.

1. Navigate to the **Anomaly Detection Jobs** page in the main menu, or use the [global search field](../../find-and-organize/find-apps-and-objects.md). 
2. Locate the {{anomaly-job}} whose model you want to revert in the job table.
3. Open the job details and navigate to the **Model Snapshots** tab.
   :::{image} /explore-analyze/images/machine-learning-anomaly-job-model-snapshots.jpg
   :alt: A screenshot of a job with the Model Snapshots tab opened
   :screenshot:
   :::

4. Select a snapshot from the list and click the **Revert** icon under **Actions**.
5. Optional: Select if you want to replay the analysis based on the data in your index after the revert has been applied. If you don’t select this option, there will be no {{anomaly-detect}} results after the snapshot was taken and the job results end at the point in time of the snapshot. If you select this option, you can then optionally select one or both of the next two options:
   * You can select whether you want the job to continue running in real time after the replay, or to just replay existing data after the snapshot.
   * You can select a time range you want to avoid during the replay by declaring a calendar event. This way, you can skip any problematic time frame that you want the {{anomaly-job}} to avoid.
   :::{image} /explore-analyze/images/machine-learning-revert-model-snapshot.jpg
   :alt: A screenshot of a revert model snapshot flyout
   :screenshot:
   :::

6. Click **Apply**.

::::{tip}
You can use [custom rules](ml-ad-run-jobs.md#ml-ad-rules) to avoid a model being updated in case of a known event you want to exclude from the analysis. Using custom rules might help you to avoid situations where you need to revert to a snapshot.
::::

Alternatively, you can use the [revert model snapshots](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-revert-model-snapshot) API. In this case, you need to manually close the corresponding job before reverting to the saved snapshot.

::::{note}

* By default, when you revert to a snapshot, all {{anomaly-detect}} results are deleted for the corresponding job after the point when the snapshot was saved. If you replay the analysis, results will be re-generated based on your configuration.
* Reverting to a snapshot does not change the `data_counts` values of the {{anomaly-job}}, these values are not reverted to the earlier state.

::::
