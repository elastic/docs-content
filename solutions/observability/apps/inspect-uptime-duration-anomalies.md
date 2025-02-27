---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/inspect-uptime-duration-anomalies.html
applies_to:
  stack: all
---

# Inspect uptime duration anomalies [inspect-uptime-duration-anomalies]

Each monitor location is modeled, and when a monitor runs for an unusual amount of time, at a particular time, an anomaly is recorded and highlighted on the **Monitor duration** chart.


## Enable uptime duration {{anomaly-detect}} [uptime-anomaly-detection]

Create a {{ml}} job to detect anomalous monitor duration rates automatically.

1. To access this page, go to **Observability > Uptime > Monitors**, and then click a monitor to view its the details.
2. In the **Monitor duration** panel, click **Enable anomaly detection**.

    ::::{note}
    If {{anomaly-detect}} is already enabled, click **Anomaly detection** and select to view duration anomalies directly in the [{{ml-app}} app](/explore-analyze/machine-learning/anomaly-detection/ml-getting-started.md#sample-data-results), enable an [anomaly rule](../incident-management/create-an-uptime-duration-anomaly-rule.md), or disable the {{anomaly-detect}}.

    ::::

3. You are prompted to create a [response duration anomaly rule](../incident-management/create-an-uptime-duration-anomaly-rule.md) for the {{ml}} job which will carry out the analysis, and you can configure which severity level to create the rule for.

When an anomaly is detected, the duration is displayed on the **Monitor duration** chart, along with the duration times. The colors represent the criticality of the anomaly: red (critical) and yellow (minor).

:::{image} ../../../images/observability-inspect-uptime-duration-anomalies.png
:alt: inspect uptime duration anomalies
:class: screenshot
:::

