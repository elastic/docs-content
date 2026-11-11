---
navigation_title: Integrate with Machine Learning
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-machine-learning-integration.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-integrate-with-machine-learning.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Integrate Elastic APM with {{ml}} [observability-apm-integrate-with-machine-learning]

::::{important}
Using {{ml}} requires an [appropriate license](https://www.elastic.co/subscriptions).

::::

The {{ml}} integration creates predefined jobs to detect anomalies in {{product.apm}} transaction metrics. With this integration, you can quickly pinpoint anomalous transactions and identify services with active anomalies across your architecture.

{{ml}} jobs are created per environment, so you can add services to an existing environment without creating additional jobs.

Results from {{ml}} jobs are shown in multiple places throughout the Applications UI:

* The **Services** inventory provides a quick-glance view of the general health of all of your services. {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` Services are color coded to show services with active anomalies so you can quickly identify problem areas.
* The transaction duration chart shows the expected bounds and adds an annotation when the anomaly score is 75 or above.
* Service Maps display a color-coded anomaly indicator on each service node based on the detected anomaly score.
* {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` Alert detail pages for {{product.apm}} anomaly alerts show RED metric charts and the service map, along with [a severity-colored callout](/solutions/observability/apm/service-map.md#service-maps-legend-anomaly-colors) identifying the anomaly type. For more information, refer to [View alerts](/solutions/observability/incident-management/view-alerts.md).

:::{image} /solutions/images/observability-apm-service-map-anomaly-scores.png
:alt: Service map showing color-coded anomaly score indicators on service nodes, with yellow and red borders indicating degraded or unhealthy services
:screenshot:
:::

## Enable {{anomaly-detect}} [observability-apm-integrate-with-machine-learning-enable-anomaly-detection]

To enable {{ml}} {{anomaly-detect}}:

1. In your {{obs-serverless}} project or {{kib}}, go to any **Applications** page.
2. Click **{{anomaly-detect-cap}}**.
3. Click **Create Job**.
4. {{ml-jobs-cap}} are created at the environment level. Select all of the service environments that you want to enable {{anomaly-detect}} in. Anomalies will surface for all services and transaction types within the selected environments.
5. Click **Create Jobs**.

After a few minutes, the job will begin calculating results; it might take additional time for results to appear on your service maps. To manage existing jobs, click **Manage jobs** (or go to **{{ml-cap}}** → **Jobs**).

## Detect low transaction counts [apm-ml-low-transaction-count]
```{applies_to}
stack: ga 9.6+
serverless: ga
```

New {{product.apm}} transaction {{ml}} jobs include four detectors: latency, throughput, failed transaction rate, and low transaction count. The `low_count` detector identifies unusually low transaction counts, including drops to zero. This helps detect when traffic stops reaching a service, even when there are no transactions from which to calculate latency or failed transaction rate.

Existing jobs retain the detectors they were created with, which means that upgrading {{kib}} doesn't add the low-count detector to them. To use it, [recreate jobs that lack the detector](#apm-ml-recreate-existing-jobs).

## Add low-count detection to existing jobs [apm-ml-recreate-existing-jobs]
```{applies_to}
stack: ga 9.6+
serverless: ga
```

Because a job's detectors are fixed at creation, the only way to add low-count detection is to delete the environment's {{product.apm}} transaction job and create a new one, which includes all four detectors. Your {{product.apm}} anomaly rules survive the deletion, but the environment's anomaly history and model are lost.

Use this procedure for each environment whose {{product.apm}} transaction job lacks the `low_count` detector.

To check a job, open its configuration in **{{ml-app}}** → **Anomaly Detection** → **Jobs**, or use the [get job configuration API]({{es-apis}}operation/operation-ml-get-jobs) and inspect `analysis_config.detectors`. If the `low_count` detector is already present, you do not need to recreate the job.

### Before you delete a job

:::{warning}
Deleting a job permanently deletes its anomaly results and model snapshots. The replacement job analyzes the last four weeks of available data with a new model. Older anomaly history is lost, and scores in the reanalyzed period can differ. Other environments' jobs are not affected.
:::

Anomaly charts and badges for the environment have no results until the replacement job produces them. {{product.apm}} anomaly rules cannot detect new anomalies for that environment during this gap. Existing active alerts recover, and anomalies from the replacement job create new alerts. Alert history remains available.

Deleting a job also removes its automatically generated annotations. User-created annotations are deleted only if you enable **Delete annotations** in the deletion dialog.

### Recreate the job and update rules

1. In **{{ml-app}}** → **Anomaly Detection** → **Jobs**, find the environment's {{product.apm}} transaction job. Its ID has the form `apm-<environment>-<four-character suffix>-apm_tx_metrics`.
2. Delete the job. Because these jobs are managed by {{product.apm}}, deleting one also deletes its {{dfeed}}. Leave **Delete alerting rules** off if the option appears. Wait for the job to disappear from the list.
3. In **Applications**, open **Settings** → **{{anomaly-detect-cap}}**. Click **Create job**, select the same environment, and click **Create Jobs**. The {{dfeed}} starts automatically with a four-week lookback.
4. Wait until the job is open and has finished analyzing the lookback period.
5. Edit each existing [{{product.apm}} anomaly rule](/solutions/observability/incident-management/create-an-apm-anomaly-rule.md#apm-anomaly-low-transaction-count) that should detect traffic drops. Under **Detector types**, select **low transaction count** and save the rule.

Closing the old job is not enough: {{product.apm}} skips creation while the existing {{product.apm}} transaction job for the environment remains, including a closed job.

You do not need to recreate {{product.apm}} anomaly rules. They look up the job for the environment on each run, and the ML job deletion dialog does not delete them. {{rules-ui}} retain their saved detector selections, so check that **low transaction count** is selected. The other selected detectors resume alerting once the new job has finalized results.

## {{anomaly-detect-cap}} warning [observability-apm-integrate-with-machine-learning-anomaly-detection-warning]

To make {{ml}} as easy as possible to set up, Elastic will warn you when filtered to an environment without a {{ml}} job.

## No anomaly data showing [observability-apm-integrate-with-machine-learning-unknown-service-health]

After enabling {{anomaly-detect}}, anomaly indicators might not appear for a service. Here are some reasons why this can occur:

1. No {{ml}} job exists. Refer to [Enable {{anomaly-detect}}](/solutions/observability/apm/machine-learning.md#observability-apm-integrate-with-machine-learning-enable-anomaly-detection) to enable {{anomaly-detect}} and create an {{ml}} job.
2. There is no {{ml}} data for the job. If you just created the {{ml}} job you’ll need to wait a few minutes for data to be available. Alternatively, if the service or its environment are new, you’ll need to wait for more trace data.
3. No "request" or "page-load" transaction type exists for this service; {{anomaly-detect}} is only available for these transaction types.