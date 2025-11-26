---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maintenance-windows.html
  - https://www.elastic.co/guide/en/serverless/current/maintenance-windows.html
applies_to:
  stack: preview 9.0, ga 9.2
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
description: Instructions for scheduling maintenance windows to suppress rule notifications during planned outages.
---

# Maintenance windows [maintenance-windows]

This content applies to: [![Observability](/explore-analyze/images/serverless-obs-badge.svg "")](../../../solutions/observability.md) [![Security](/explore-analyze/images/serverless-sec-badge.svg "")](../../../solutions/security.md)


You can schedule single or recurring maintenance windows to temporarily suppress rule notifications during planned outages or maintenance periods. Alerts continue to be generated, but notifications are suppressed according to the maintenance window schedule.

By default, a maintenance window affects all rules in all {{kib}} apps within its space. You can refine the scope of a maintenance window by adding filters and rule categories.

Alerts continue to be generated, however notifications are suppressed as follows:

* When an alert occurs during a maintenance window, there are no notifications. When the alert recovers, there are no notifications—even if the recovery occurs after the maintenance window ends.
* When an alert occurs before a maintenance window and recovers during or after the maintenance window, notifications are sent as usual.

## Configure access to maintenance windows [setup-maintenance-windows]

To use maintenance windows, you must have the appropriate [subscription](https://www.elastic.co/subscriptions) and {{kib}} feature privileges.

* To have full access to maintenance windows, you must have `All` privileges for the **Management > Maintenance Windows** feature.
* To have view-only access to maintenance windows, you must have `Read` privileges for the **Management > Maintenance Windows** feature.

For more details, refer to [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

## Create and manange maintenance windows [manage-maintenance-windows]

In **Management > {{stack-manage-app}} > Maintenance Windows** or **{{project-settings}} > {{manage-app}} > {{maint-windows-app}}** in Serverless, you can create, edit, cancel, and archive maintenance windows. 

{applies_to}`stack: ga 9.1` In {{stack}} 9.1.0 and later, you can also delete maintenance windows that are running, canceled, or archived. Be aware that you can't recover maintenance windows once you delete them.

When you create a maintenance window, you must provide a name and a schedule. You can optionally configure it to repeat daily, monthly, yearly, or on a custom interval.

:::{image} /explore-analyze/images/kibana-create-maintenance-window.png
:alt: The Create Maintenance Window user interface in {{kib}}
:screenshot:
:::

By default, maintenance windows affect all categories of rules. The category-specific maintenance window options alter this behavior. For the definitive list of rule types in each category, refer to the [get rule types API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-alerting).

::::{note}

{applies_to}`stack: removed 9.2` {applies_to}`serverless: removed` The option to specify rule categories for a maintenance window is no longer available. Maintenance windows apply to all rule types.

Note that existing maintenance windows are still applied to rule categories that were specified. However, if you edit a maintenance window after upgrading or using the latest version of {{serverless-short}}, specified rule categories are removed and the maintenance window will be applied to all rules types.


::::

If you turn on **Filter alerts**, you can use KQL to filter the alerts affected by the maintenance window:

:::{image} /explore-analyze/images/kibana-create-maintenance-window-filter.png
:alt: The Create Maintenance Window user interface in {{kib}} with alert filters turned on
:screenshot:
:::

::::{note}

* {applies_to}`stack: removed 9.2` {applies_to}`serverless: removed` You can select only a single category when you turn on filters.
* Some rules are not affected by maintenance window filters because their alerts do not contain requisite data. In particular, [{{stack-monitor-app}}](../../../deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md), [tracking containment](../../../explore-analyze/alerts-cases/alerts/geo-alerting.md), [{{anomaly-jobs}} health](../../../explore-analyze/machine-learning/anomaly-detection/ml-configuring-alerts.md), and [transform health](../../../explore-analyze/transforms/transform-alerts.md) rules are not affected by the filters.

::::

A maintenance window can have any one of the following statuses:

* `Upcoming`: It will run at the scheduled date and time.
* `Running`: It is running.
* `Finished`: It ended and does not have a repeat schedule.
* `Archived`: It is archived. In a future release, archived maintenance windows will be queued for deletion.

When you [view alert details](../../../explore-analyze/alerts-cases/alerts/create-manage-rules.md#rule-details) in {{kib}}, each alert shows unique identifiers for maintenance windows that affected it.
