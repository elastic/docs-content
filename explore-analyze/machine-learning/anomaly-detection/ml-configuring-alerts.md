---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-configuring-alerts.html
---

# Generating alerts for anomaly detection jobs [ml-configuring-alerts]

{{kib}} {{alert-features}} include support for {{ml}} rules, which run scheduled checks for anomalies in one or more {{anomaly-jobs}} or check the health of the job with certain conditions. If the conditions of the rule are met, an alert is created and the associated action is triggered. For example, you can create a rule to check an {{anomaly-job}} every fifteen minutes for critical anomalies and to notify you in an email. To learn more about {{kib}} {{alert-features}}, refer to [Alerting](../../alerts/kibana.md#alerting-getting-started).

The following {{ml}} rules are available:

{{anomaly-detect-cap}} alert
:   Checks if the {{anomaly-job}} results contain anomalies that match the rule conditions.

{{anomaly-jobs-cap}} health
:   Monitors job health and alerts if an operational issue occurred that may prevent the job from detecting anomalies.

::::{tip}
If you have created rules for specific {{anomaly-jobs}} and you want to monitor whether these jobs work as expected, {{anomaly-jobs}} health rules are ideal for this purpose.
::::

In **{{stack-manage-app}} > {{rules-ui}}**, you can create both types of {{ml}} rules. In the **{{ml-app}}** app, you can create only {{anomaly-detect}} alert rules; create them from the {{anomaly-job}} wizard after you start the job or from the {{anomaly-job}} list.
