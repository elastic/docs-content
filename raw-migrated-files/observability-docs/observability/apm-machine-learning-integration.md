---
navigation_title: "Integrate with machine learning"
---

# Machine learning integration [apm-machine-learning-integration]


::::{important}
Using machine learning requires an [appropriate license](https://www.elastic.co/subscriptions).

::::


The Machine learning integration initiates a new job predefined to calculate anomaly scores on APM transaction durations. With this integration, you can quickly pinpoint anomalous transactions and see the health of any upstream and downstream services.

Machine learning jobs are created per environment and are based on a service’s average response time. Because jobs are created at the environment level, you can add new services to your existing environments without the need for additional machine learning jobs.

Results from machine learning jobs are shown in multiple places throughout the Applications UI:

* The **Services overview** provides a quick-glance view of the general health of all of your services.

    :::{image} ../../../images/observability-service-quick-health.png
    :alt: Example view of anomaly scores on response times in the Applications UI
    :class: screenshot
    :::

* The transaction duration chart will show the expected bounds and add an annotation when the anomaly score is 75 or above.

    :::{image} ../../../images/observability-apm-ml-integration.png
    :alt: Example view of anomaly scores on response times in the Applications UI
    :class: screenshot
    :::

* Service Maps will display a color-coded anomaly indicator based on the detected anomaly score.

    :::{image} ../../../images/observability-apm-service-map-anomaly.png
    :alt: Example view of anomaly scores on service maps in the Applications UI
    :class: screenshot
    :::



## Enable anomaly detection [create-ml-integration]

To enable machine learning anomaly detection:

1. From the Services overview, Traces overview, or Service Map tab, select **Anomaly detection**.
2. Click **Create Job**.
3. Machine learning jobs are created at the environment level. Select all of the service environments that you want to enable anomaly detection in. Anomalies will surface for all services and transaction types within the selected environments.
4. Click **Create Jobs**.

That’s it! After a few minutes, the job will begin calculating results; it might take additional time for results to appear on your service maps. To manage existing jobs, click **Manage jobs**.


## Anomaly detection warning [warning-ml-integration]

To make machine learning as easy as possible to set up, the Applications UI will warn you when filtered to an environment without a machine learning job.

:::{image} ../../../images/observability-apm-anomaly-alert.png
:alt: Example view of anomaly alert in the Applications UI
:class: screenshot
:::


## Unknown service health [unkown-ml-integration]

After enabling anomaly detection, service health may display as "Unknown". Here are some reasons why this can occur:

1. No machine learning job exists. See [Enable anomaly detection](../../../solutions/observability/apps/integrate-with-machine-learning.md#observability-apm-integrate-with-machine-learning-enable-anomaly-detection) to enable anomaly detection and create a machine learning job.
2. There is no machine learning data for the job. If you just created the machine learning job you’ll need to wait a few minutes for data to be available. Alternatively, if the service or its enviroment are new, you’ll need to wait for more trace data.
3. No "request" or "page-load" transaction type exists for this service; service health is only available for these transaction types.
