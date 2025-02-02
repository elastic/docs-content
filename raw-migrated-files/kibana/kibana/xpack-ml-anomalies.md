# {{anomaly-detect-cap}} [xpack-ml-anomalies]

The Elastic {{ml}} {anomaly-detect} feature automatically models the normal behavior of your time series data — learning trends, periodicity, and more — in real time to identify anomalies, streamline root cause analysis, and reduce false positives. {{anomaly-detect-cap}} runs in and scales with {{es}}, and includes an intuitive UI on the {{kib}} **Machine Learning** page for creating {{anomaly-jobs}} and understanding results.

If you have a license that includes the {{ml-features}}, you can create {{anomaly-jobs}} and manage jobs and {{dfeeds}} from the **Job Management** pane:

:::{image} ../../../images/kibana-ml-job-management.png
:alt: Job Management
:class: screenshot
:::

You can use the **Settings** pane to create and edit calendars and the filters that are used in custom rules:

:::{image} ../../../images/kibana-ml-settings.png
:alt: Calendar Management
:class: screenshot
:::

The **Anomaly Explorer** and **Single Metric Viewer** display the results of your {{anomaly-jobs}}. For example:

:::{image} ../../../images/kibana-ml-single-metric-viewer.png
:alt: Single Metric Viewer
:class: screenshot
:::

You can optionally add annotations by drag-selecting a period of time in the **Single Metric Viewer** and adding a description. For example, you can add an explanation for anomalies in that time period or provide notes about what is occurring in your operational environment at that time:

:::{image} ../../../images/kibana-ml-annotations-list.png
:alt: Single Metric Viewer with annotations
:class: screenshot
:::

In some circumstances, annotations are also added automatically. For example, if the {{anomaly-job}} detects that there is missing data, it annotates the affected time period. For more information, see [Handling delayed data](../../../explore-analyze/machine-learning/anomaly-detection/ml-delayed-data-detection.md). The **Job Management** pane shows the full list of annotations for each job.

::::{note}
The {{kib}} {ml-features} use pop-ups. You must configure your web browser so that it does not block pop-up windows or create an exception for your {{kib}} URL.
::::


For more information about the {{anomaly-detect}} feature, see [{{ml-cap}} in the {{stack}}](https://www.elastic.co/what-is/elastic-stack-machine-learning) and [{{ml-cap}} {anomaly-detect}](../../../explore-analyze/machine-learning/anomaly-detection.md).

