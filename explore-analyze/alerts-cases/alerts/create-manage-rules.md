---
navigation_title: Create and manage rules
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/create-and-manage-rules.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Create and manage alerting rules with {{kib}} [create-and-manage-rules]

The **{{stack-manage-app}}** > **{{rules-ui}}** UI provides a cross-app view of alerting. Different {{kib}} apps like [**{{observability}}**](../../../solutions/observability/incident-management/alerting.md), [**Security**](detection-rules://index.md), [**Maps**](geo-alerting.md) and [**{{ml-app}}**](../../machine-learning/machine-learning-in-kibana.md) can offer their own rules.

You can find **Rules** in **Stack Management** > **Alerts and insights** > **Rules** in {{kib}} or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

![Rules page navigation](/explore-analyze/images/kibana-stack-management-rules.png "")

**{{rules-ui}}** provides a central place to:

* [Create and edit](#create-edit-rules) rules
* [Manage rules](#controlling-rules) including enabling/disabling, muting/unmuting, and deleting
* Drill down to [rule details](#rule-details)
* Configure rule settings

For more information on alerting concepts and the types of rules and connectors available, go to [Alerting](../alerts.md).

## Required permissions [_required_permissions]

Access to rules is granted based on your {{alert-features}} privileges. For more information, go to [Security](alerting-setup.md#alerting-security).

## Create and edit rules [create-edit-rules]

Some rules must be created within the context of a {{kib}} app like [Metrics](/solutions/observability/infra-and-hosts.md), [**APM**](/solutions/observability/apm/index.md), or [Uptime](/solutions/observability/uptime/index.md), but others are generic. Generic rule types can be created in **{{rules-ui}}** by clicking the **Create rule** button. This will launch a flyout that guides you through selecting a rule type and configuring its conditions and actions.

After a rule is created, you can open the action menu (…) and select **Edit rule** to re-open the flyout and change the rule properties.

::::{tip}
You can also manage rules as resources with the [Elasticstack provider](https://registry.terraform.io/providers/elastic/elasticstack/latest) for Terraform. For more details, refer to the [elasticstack_kibana_alerting_rule](https://registry.terraform.io/providers/elastic/elasticstack/latest/docs/resources/kibana_alerting_rule) resource.
::::

### Rule type and conditions [defining-rules-type-conditions]

Depending on the {{kib}} app and context, you might be prompted to choose the type of rule to create. Some apps will preselect the type of rule for you.

Each rule type provides its own way of defining the conditions to detect, but an expression formed by a series of clauses is a common pattern. For example, in an {{es}} query rule, you specify an index, a query, and a threshold, which uses a metric aggregation operation (`count`, `average`, `max`, `min`, or `sum`):

:::{image} /explore-analyze/images/kibana-rule-types-es-query-conditions.png
:alt: UI for defining rule conditions in an {{es}} query rule
:screenshot:
:::

All rules must have a check interval, which defines how often to evaluate the rule conditions. Checks are queued; they run as close to the defined value as capacity allows.

For details on what types of rules are available and how to configure them, refer to [*Rule types*](rule-types.md).

### Alert flapping [defining-rules-flapping-details]

You can modify the criteria for changing an alert's status to [flapping](view-alerts.md#alert-status) by configuring the **Alert flapping detection** settings, which are turned on by default. When configuring flapping settings, you must set a look back window and threshold for alert status changes. For example, you can specify that alerts with at least 6 status changes in the last 10 runs are `flapping`.   

{applies_to}`stack: ga 9.3+` Modify the flapping settings for a specific rule while creating or editing it. You can also modify the flapping settings for all rules in your {{kib}} space or {{serverless-short}} project. To do this, go to the **Rules** page (use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) or find the **Rules** page from the main management menu), click **Settings**, then go to the **Alert flapping detection** settings.

{applies_to}`stack: ga 9.0-9.2` You can only modify the global flapping settings for rules your {{kib}} space or {{serverless-short}} project.

### Actions [defining-rules-actions-details]

You can add one or more actions to your rule to generate notifications when its conditions are met and when they are no longer met.

Each action uses a connector, which provides connection information for a {{kib}} service or third party integration, depending on where you want to send the notifications.

{applies_to}`stack: preview` {applies_to}`serverless: preview` Some connectors that perform actions within {{kib}}, such as the [Cases connector](kibana://reference/connectors-kibana/cases-action-type.md), require less configuration. For example, you do not need to set the action frequency or variables.

After you select a connector, set the action frequency. You can choose to create a summary of alerts on each check interval or on a custom interval. Alternatively, you an choose to run actions for each alert (at each check interval, only when the alert status changes, or at a custom interval).

::::{note}
If you choose a custom action interval, it cannot be shorter than the rule’s check interval.
::::

For example, if you create an {{es}} query rule, you can send notifications that summarize the new, ongoing, and recovered alerts on a custom interval:

:::{image} /explore-analyze/images/kibana-es-query-rule-action-summary.png
:alt: UI for defining alert summary action in an {{es}} query rule
:screenshot:
:::

When you choose to run actions for each alert, you must specify an action group. Each rule type has a set of valid action groups, which affect when an action runs. For example, you can set **Run when** to `Query matched` or `Recovered` for the {{es}} query rule:

:::{image} /explore-analyze/images/kibana-es-query-rule-recovery-action.png
:alt: UI for defining a recovery action
:screenshot:
:::

Connectors have unique behavior for each action group. For example, you can have actions that create an {{opsgenie}} alert when rule conditions are met and recovery actions that close the {{opsgenie}} alert. For more information about connectors, refer to [*Connectors*](../../../deploy-manage/manage-connectors.md).

::::{tip}
:name: alerting-concepts-suppressing-duplicate-notifications

If you are not using alert summaries, actions are generated per alert and a rule can end up generating a large number of actions. Take the following example where a rule is monitoring three servers every minute for CPU usage > 0.9, and the action frequency is `On check intervals`:

* Minute 1: server X123 > 0.9. *One email* is sent for server X123.
* Minute 2: X123 and Y456 > 0.9. *Two emails* are sent, one for X123 and one for Y456.
* Minute 3: X123, Y456, Z789 > 0.9. *Three emails* are sent, one for each of X123, Y456, Z789.

In this example, three emails are sent for server X123 in the span of 3 minutes for the same rule. Often, it’s desirable to suppress these re-notifications. If you set the action frequency to `On custom action intervals` with an interval of 5 minutes, you reduce noise by getting emails only every 5 minutes for servers that continue to exceed the threshold:

* Minute 1: server X123 > 0.9. *One email* will be sent for server X123.
* Minute 2: X123 and Y456 > 0.9. *One email* will be sent for Y456.
* Minute 3: X123, Y456, Z789 > 0.9. *One email* will be sent for Z789.

To get notified only once when a server exceeds the threshold, you can set the action frequency to `On status changes`. Alternatively, consider using alert summaries to reduce the volume of notifications.

::::

### Action variables [defining-rules-actions-variables]

You can pass rule values to an action at the time a condition is detected. To view the list of variables available for your rule, click the "add rule variable" button:

:::{image} /explore-analyze/images/kibana-es-query-rule-action-variables.png
:alt: Passing rule values to an action
:screenshot:
:::

For more information about common action variables, refer to [*Rule action variables*](rule-action-variables.md).

## Snooze and disable rules [controlling-rules]

The rule listing enables you to quickly snooze, disable, enable, or delete individual rules. For example, you can change the state of a rule:

![Use the rule status dropdown to enable or disable an individual rule](/explore-analyze/images/kibana-individual-enable-disable.png "")

If there are rules that are not currently needed, disable them to stop running checks and reduce the load on your cluster.

When you snooze a rule, the rule checks continue to run on a schedule but alerts will not generate actions. You can snooze for a specified period of time, indefinitely, or schedule single or recurring downtimes:

![Snooze notifications for a rule](/explore-analyze/images/kibana-snooze-panel.png "")

When a rule is in a snoozed state, you can cancel or change the duration of this state.

{applies_to}`stack: preview` {applies_to}`serverless: preview` To temporarily suppress notifications for rules, you can also create a [maintenance window](maintenance-windows.md).

## View rule details [rule-details]

You can determine the health of a rule by looking at the **Last response** in **{{stack-manage-app}}** > **{{rules-ui}}**. A rule can have one of the following responses:

`failed`
:   The rule ran with errors.

`succeeded`
:   The rule ran without errors.

`warning`
:   The rule ran with some non-critical errors.

Click the rule name to access a rule details page:

:::{image} /explore-analyze/images/kibana-rule-details-alerts-active.png
:alt: Rule details page with multiple alerts
:screenshot:
:::

In this example, the rule detects when a site serves more than a threshold number of bytes in a 24 hour period. Four sites are above the threshold. These are called alerts - occurrences of the condition being detected - and the alert name, status, time of detection, and duration of the condition are shown in this view. Alerts come and go from the list depending on whether the rule conditions are met. For more information about alerts, go to [*View alerts*](view-alerts.md).

If there are rule actions that failed to run successfully, you can see the details on the **History** tab. In the **Message** column, click the warning or expand icon ![double arrow icon to open a flyout with the document details](/explore-analyze/images/kibana-expand-icon-2.png "") or click the number in the **Errored actions** column to open the **Errored Actions** panel. In this example, the action failed because the [`xpack.actions.email.domain_allowlist`](kibana://reference/configuration-reference/alerting-settings.md#action-config-email-domain-allowlist) setting was updated and the action’s email recipient is no longer included in the allowlist:

:::{image} /explore-analyze/images/kibana-rule-details-errored-actions.png
:alt: Rule histor page with alerts that have errored actions
:screenshot:
:::

## Import and export rules [importing-and-exporting-rules]

To import and export rules, use [saved objects](../../find-and-organize/saved-objects.md).

::::{note}
Some rule types cannot be exported through this interface:

**Security rules** can be imported and exported using the [Security UI](../../../solutions/security/detect-and-alert/manage-detection-rules.md#import-export-rules-ui).

**Stack monitoring rules** are [automatically created](../../../deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md) for you and therefore cannot be managed in **Saved Objects**.

::::

Rules are disabled on export. You are prompted to re-enable the rule on successful import.

:::{image} /explore-analyze/images/kibana-rules-imported-banner.png
:alt: Rules import banner
:screenshot:
:::
