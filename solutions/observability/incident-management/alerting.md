---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/create-alerts.html
  - https://www.elastic.co/guide/en/serverless/current/observability-alerting.html
---

# Alerting [observability-alerting]

Alerting enables you to define *rules*, which detect complex conditions within different apps and trigger actions when those conditions are met. Alerting provides a set of built-in connectors and rules for you to use. This page describes all of these elements and how they operate together.


## Important concepts [observability-alerting-important-concepts]

Alerting works by running checks on a schedule to detect conditions defined by a rule. You can define rules at different levels (service, environment, transaction) or use custom KQL queries. When a condition is met, the rule tracks it as an *alert* and responds by triggering one or more *actions*.

Actions typically involve interaction with Elastic services or third-party integrations. [Connectors](../../../deploy-manage/manage-connectors.md) enable actions to talk to these services and integrations.

Once you’ve defined your rules, you can monitor any alerts triggered by these rules in real time, with detailed dashboards that help you quickly identify and troubleshoot any issues that may arise. You can also extend your alerts with notifications via services or third-party incident management systems.


## Alerts page [observability-alerting-alerts-page]

On the **Alerts** page, the Alerts table provides a snapshot of alerts occurring within the specified time frame. The table includes the alert status, when it was last updated, the reason for the alert, and more.

:::{image} ../../../images/serverless-observability-alerts-overview.png
:alt: Summary of Alerts
:class: screenshot
:::

You can filter this table by alert status or time period, customize the visible columns, and search for specific alerts (for example, alerts related to a specific service or environment) using KQL. Select **View alert detail** from the **More actions** menu ![action menu](../../../images/serverless-boxesHorizontal.svg ""), or click the Reason link for any alert to [view alert](../../../solutions/observability/incident-management/view-alerts.md) in detail, and you can then either **View in app** or **View rule details**.


## Next steps [observability-alerting-next-steps]

* [Create and manage rules](../../../solutions/observability/incident-management/create-manage-rules.md)
* [View alerts](../../../solutions/observability/incident-management/view-alerts.md)