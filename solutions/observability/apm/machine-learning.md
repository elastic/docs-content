---
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

# Integrate with machine learning [observability-apm-integrate-with-machine-learning]

::::{important}
Using machine learning requires an [appropriate license](https://www.elastic.co/subscriptions).

::::

The {{ml}} integration initiates a new job predefined to calculate anomaly scores on {{product.apm}} transaction durations. With this integration, you can quickly pinpoint anomalous transactions and identify services with active anomalies across your architecture.

{{ml}} jobs are created per environment and are based on a service’s average response time. Because jobs are created at the environment level, you can add new services to your existing environments without the need for additional {{ml}} jobs.

Results from {{ml}} jobs are shown in multiple places throughout the Applications UI:

* The **Services** inventory highlights services with active anomalies so you can quickly identify problem areas.
* The transaction duration chart shows the expected bounds and adds an annotation when the anomaly score is 75 or above.
* Service Maps display a color-coded anomaly indicator on each service node based on the detected anomaly score.
* Alert detail pages for {{product.apm}} anomaly alerts show RED metric charts and the service map, along with a severity-colored callout identifying the anomaly type. For more information, refer to [View alerts](/solutions/observability/incident-management/view-alerts.md).

    :::{image} /solutions/images/observability-apm-service-map-anomaly.png
    :alt: Example view of anomaly scores on service maps in the Applications UI
    :screenshot:
    :::

## Enable anomaly detection [observability-apm-integrate-with-machine-learning-enable-anomaly-detection]

To enable machine learning anomaly detection:

1. In your {{obs-serverless}} project or {{kib}}, go to any **Applications** page.
2. Click **Anomaly detection**.
3. Click **Create Job**.
4. Machine learning jobs are created at the environment level. Select all of the service environments that you want to enable anomaly detection in. Anomalies will surface for all services and transaction types within the selected environments.
5. Click **Create Jobs**.

That’s it! After a few minutes, the job will begin calculating results; it might take additional time for results to appear on your service maps. To manage existing jobs, click **Manage jobs** (or go to **Machine learning** → **Jobs**).

## Anomaly detection warning [observability-apm-integrate-with-machine-learning-anomaly-detection-warning]

To make machine learning as easy as possible to set up, Elastic will warn you when filtered to an environment without a machine learning job.

## No anomaly data showing [observability-apm-integrate-with-machine-learning-unknown-service-health]

After enabling {{anomaly-detect}}, anomaly indicators may not appear for a service. Here are some reasons why this can occur:

1. No {{ml}} job exists. See [Enable {{anomaly-detect}}](/solutions/observability/apm/machine-learning.md#observability-apm-integrate-with-machine-learning-enable-anomaly-detection) to enable {{anomaly-detect}} and create an {{ml}} job.
2. There is no {{ml}} data for the job. If you just created the {{ml}} job you’ll need to wait a few minutes for data to be available. Alternatively, if the service or its environment are new, you’ll need to wait for more trace data.
3. No "request" or "page-load" transaction type exists for this service; {{anomaly-detect}} is only available for these transaction types.