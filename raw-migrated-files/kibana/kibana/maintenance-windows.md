# Maintenance windows [maintenance-windows]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


You can schedule single or recurring maintenance windows to temporarily reduce rule notifications. For example, a maintenance window prevents false alarms during planned outages.

By default, a maintenance window affects all rules in all {{kib}} apps within its space. You can refine the scope of a maintenance window by adding filters and rule categories.

Alerts continue to be generated, however notifications are suppressed as follows:

* When an alert occurs during a maintenance window, there are no notifications. When the alert recovers, there are no notifications—​even if the recovery occurs after the maintenance window ends.
* When an alert occurs before a maintenance window and recovers during or after the maintenance window, notifications are sent as usual.


## Configure access to maintenance windows [setup-maintenance-windows]

To use maintenance windows, you must have the appropriate [subscription](https://www.elastic.co/subscriptions) and {{kib}} feature privileges.

* To have full access to maintenance windows, you must have `All` privileges for the **Management > Maintenance Windows** feature.
* To have view-only access to maintenance windows, you must have `Read` privileges for the **Management > Maintenance Windows** feature.

For more details, refer to [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).


## Create and manange maintenance windows [manage-maintenance-windows]

In **Management > {{stack-manage-app}} > Maintenance Windows**, you can create, edit, and archive maintenance windows.

When you create a maintenance window, you must provide a name and a schedule. You can optionally configure it to repeat daily, monthly, yearly, or on a custom interval.

:::{image} ../../../images/kibana-create-maintenance-window.png
:alt: The Create Maintenance Window user interface in {kib}
:class: screenshot
:::

By default, maintenance windows affect all categories of rules. The category-specific maintenance window options alter this behavior. For the definitive list of rule types in each category, refer to the [get rule types API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-alerting).

If you turn on **Filter alerts**, you can use KQL to filter the alerts affected by the maintenance window:

:::{image} ../../../images/kibana-create-maintenance-window-filter.png
:alt: The Create Maintenance Window user interface in {{kib}} with alert filters turned on
:class: screenshot
:::

::::{note}
You can select only a single category when you turn on filters.
::::


A maintenance window can have any one of the following statuses:

* `Upcoming`: It will run at the scheduled date and time.
* `Running`: It is running.
* `Finished`: It ended and does not have a repeat schedule.
* `Archived`: It is archived. In a future release, archived maintenance windows will be queued for deletion.

When you [view alert details](../../../explore-analyze/alerts-cases/alerts/create-manage-rules.md#rule-details) in {{kib}}, each alert shows unique identifiers for maintenance windows that affected it.

