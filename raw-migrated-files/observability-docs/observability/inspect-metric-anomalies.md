# Detect metric anomalies [inspect-metric-anomalies]

When the {{anomaly-detect}} features of {{ml}} are enabled, you can create {{ml}} jobs to detect and inspect memory usage and network traffic anomalies for hosts and Kubernetes pods.

You can model system memory usage, along with inbound and outbound network traffic across hosts or pods. You can detect unusual increases in memory usage and unusually high inbound or outbound traffic across hosts or pods.


## Enable {{ml}} jobs for hosts or Kubernetes pods [ml-jobs-hosts]

Create a {{ml}} job to detect anomalous memory usage and network traffic automatically.

Once you create {{ml}} jobs, you can not change the settings. You can recreate these jobs later. However, you will remove any previously detected anomalies.

1. To open **Infrastructure inventory**, find **Infrastructure** in the main menu or use the [global search field](../../../get-started/the-stack.md#kibana-navigation-search).
2. Click the **Anomaly detection** link at the top of the page.
3. You’ll be prompted to create a {{ml}} job for **Hosts** or **Kubernetes Pods**. Click **Enable**.
4. Choose a start date for the {{ml}} analysis.

    {{ml-cap}} jobs analyze the last four weeks of data and continue to run indefinitely.

5. Select a partition field.

    ::::{note}
    By default, the Kubernetes partition field `kubernetes.namespace` is selected.

    ::::


    Partitions allow you to create independent models for different groups of data that share similar behavior. For example, you may want to build separate models for machine type or cloud availability zone so that anomalies are not weighted equally across groups.

6. By default, {{ml}} jobs analyze all of your metric data, and the results are listed under the **Anomalies** tab. You can filter this list to view only the jobs or metrics that you are interested in. For example, you can filter by job name and node name to view specific {{anomaly-detect}} jobs for that host.
7. Click **Enable jobs**.
8. You’re now ready to explore your metric anomalies. Click **Anomalies**.

    :::{image} ../../../images/observability-metrics-ml-jobs.png
    :alt: Infrastructure {{ml-app}} anomalies
    :class: screenshot
    :::

    The **Anomalies** table displays a list of each single metric {{anomaly-detect}} job for the specific host or Kubernetes pod. By default, anomaly jobs are sorted by time to show the most recent job.

    Along with each anomaly job and the node name, detected anomalies with a severity score equal to 50 or higher are listed. These scores represent a severity of "warning" or higher in the selected time period. The **summary** value represents the increase between the actual value and the expected ("typical") value of the metric in the anomaly record result.

    To drill down and analyze the metric anomaly, select **Actions → Open in Anomaly Explorer** to view the [Anomaly Explorer in {{ml-app}}](https://www.elastic.co/guide/en/machine-learning/current/ml-getting-started.html#sample-data-results). You can also select **Actions → Show in Inventory** to view the host or Kubernetes pods Inventory page, filtered by the specific metric.

    ::::{note}
    These predefined {{anomaly-jobs}} use [custom rules](https://www.elastic.co/guide/en/machine-learning/current/ml-ad-run-jobs.html#ml-ad-rules). To update the rules in the [Anomaly Explorer](https://www.elastic.co/guide/en/machine-learning/current/ml-getting-started.html#sample-data-results), select **actions → Configure rules**. The changes only take effect for new results. If you want to apply the changes to existing results, clone and rerun the job.

    ::::



## History chart [history-chart]

On the **Inventory** page, click **Show history** to view the metric values within the selected time frame. Detected anomalies with an anomaly score equal to 50, or higher, are highlighted in red. To examine the detected anomalies, use the [Anomaly Explorer](https://www.elastic.co/guide/en/machine-learning/current/ml-getting-started.html#sample-data-results).

:::{image} ../../../images/observability-metrics-history-chart.png
:alt: History
:class: screenshot
:::
