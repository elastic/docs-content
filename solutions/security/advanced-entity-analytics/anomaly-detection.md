---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/machine-learning.html
  - https://www.elastic.co/guide/en/serverless/current/security-machine-learning.html
---

# Anomaly detection


[{{ml-cap}}](/explore-analyze/machine-learning/anomaly-detection.md) functionality is available when you have the appropriate role, subscription, are using a [cloud deployment](https://cloud.elastic.co/registration?page=docs&placement=docs-body), or are testing out a **Free Trial**. Refer to [Machine learning job and rule requirements](/solutions/security/advanced-entity-analytics/machine-learning-job-rule-requirements.md) for more information.

You can view the details of detected anomalies within the `Anomalies` table widget shown on the Hosts, Network, and associated details pages, or even narrow to the specific date range of an anomaly from the `Max anomaly score by job` field in the overview of the details pages for hosts and IPs. These interfaces also offer the ability to drag and drop details of the anomaly to Timeline, such as the `Entity` itself, or any of the associated `Influencers`.


## Manage {{ml}} jobs [manage-jobs]

If you have the appropriate role, you can use the **ML job settings** interface on the **Alerts**, **Rules**, and **Rule Exceptions** pages to view, start, and stop {{elastic-sec}} {{ml}} jobs.

:::{image} ../../../images/security-ml-ui.png
:alt: ML job settings UI on the Alerts page
:class: screenshot
:::


### Manage {{ml}} detection rules [manage-ml-rules]

You can also check the status of {{ml}} detection rules, and start or stop their associated {{ml}} jobs:

* On the **Rules** page, the **Last response** column displays the rule’s current [status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-status). An indicator icon (![Error icon from rules table](../../../images/security-rules-table-error-icon.png "")) also appears if a required {{ml}} job isn’t running. Click the icon to list the affected jobs, then click **Visit rule details page to investigate** to open the rule’s details page.

    :::{image} ../../../images/security-rules-table-ml-job-error.png
    :alt: Rules table {{ml}} job error
    :class: screenshot
    :::

* On a rule’s details page, check the **Definition** section to confirm whether the required {{ml}} jobs are running. Switch the toggles on or off to run or stop each job.

    :::{image} ../../../images/security-rules-ts-ml-job-stopped.png
    :alt: Rule details page with ML job stopped
    :class: screenshot
    :::



### Prebuilt jobs [included-jobs]

{{elastic-sec}} comes with prebuilt {{ml}} {{anomaly-jobs}} for automatically detecting host and network anomalies. The jobs are displayed in the `Anomaly Detection` interface. They are available when either:

* You ship data using [Beats](https://www.elastic.co/products/beats) or the [{{agent}}](/solutions/security/configure-elastic-defend/install-elastic-defend.md), and {{kib}} is configured with the required index patterns (such as `auditbeat-*`, `filebeat-*`, `packetbeat-*`, or `winlogbeat-*`) on the **Data Views** page. To find this page, navigate to **Data Views** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

Or

* Your shipped data is ECS-compliant, and {{kib}} is configured with the shipped data’s index patterns on the **Data Views** page.

Or

* You install one or more of the [Advanced Analytics integrations](/solutions/security/advanced-entity-analytics/behavioral-detection-use-cases.md#ml-integrations).

[Prebuilt job reference](asciidocalypse://docs/docs-content/docs/reference/security/prebuilt-jobs.md) describes all available {{ml}} jobs and lists which ECS fields are required on your hosts when you are not using {{beats}} or the {{agent}} to ship your data. For information on tuning anomaly results to reduce the number of false positives, see [Optimizing anomaly results](/solutions/security/advanced-entity-analytics/optimizing-anomaly-results.md).

::::{note}
Machine learning jobs look back and analyze two weeks of historical data prior to the time they are enabled. After jobs are enabled, they continuously analyze incoming data. When jobs are stopped and restarted within the two-week time frame, previously analyzed data is not processed again.
::::



## View detected anomalies [view-anomalies]

To view the `Anomalies` table widget and `Max Anomaly Score By Job` details, the user must have the `machine_learning_admin` or `machine_learning_user` role.

::::{note}
To adjust the `score` threshold that determines which anomalies are shown, you can modify the `securitySolution:defaultAnomalyScore` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md).
::::
