# {{maint-windows-cap}} [maintenance-windows]

This content applies to: [![Observability](../../../images/serverless-obs-badge.svg "")](../../../solutions/observability.md) [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md)

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


You can schedule single or recurring {{maint-windows}} to temporarily reduce rule notifications. For example, a maintenance window prevents false alarms during planned outages.

Alerts continue to be generated, however notifications are suppressed as follows:

* When an alert occurs during a maintenance window, there are no notifications. When the alert recovers, there are no notifications—​even if the recovery occurs after the maintenance window ends.
* When an alert occurs before a maintenance window and recovers during or after the maintenance window, notifications are sent as usual.


## Create and manage {{maint-windows}} [maintenance-windows-create-and-manage-maint-windows]

In **{{project-settings}} → {{manage-app}} → {{maint-windows-app}}** you can create, edit, and archive {{maint-windows}}.

When you create a maintenance window, you must provide a name and a schedule. You can optionally configure it to repeat daily, monthly, yearly, or on a custom interval.

:::{image} ../../../images/serverless-create-maintenance-window.png
:alt: The Create Maintenance Window user interface in {kib}
:class: screenshot
:::

If you turn on **Filter alerts**, you can use KQL to filter the alerts affected by the maintenance window. For example, you can suppress notifications for alerts from specific rules:

:::{image} ../../../images/serverless-create-maintenance-window-filter.png
:alt: The Create Maintenance Window user interface in {{kib}} with a filter
:class: screenshot
:::

::::{note}
* You can select only a single category when you turn on filters.
* Some rules are not affected by maintenance window filters because their alerts do not contain requisite data. In particular, [{{stack-monitor-app}}](../../../deploy-manage/monitor/monitoring-data/kibana-alerts.md), [tracking containment](../../../explore-analyze/alerts-cases/alerts/geo-alerting.md), [{{anomaly-jobs}} health](../../../explore-analyze/machine-learning/anomaly-detection/ml-configuring-alerts.md), and [transform health](../../../explore-analyze/transforms/transform-alerts.md) rules are not affected by the filters.

::::


A maintenance window can have any one of the following statuses:

* `Upcoming`: It will run at the scheduled date and time.
* `Running`: It is running.
* `Finished`: It ended and does not have a repeat schedule.
* `Archived`: It is archived. In a future release, archived {{maint-windows}} will be queued for deletion.

When you view alert details in {{kib}}, each alert shows unique identifiers for {{maint-windows}} that affected it.
