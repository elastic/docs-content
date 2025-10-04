---
navigation_title: Optimize alerting performance
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/alerting-production-considerations.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
products:
  - id: kibana
---

# {{kib}} alerting: performance and scaling [alerting-production-considerations]

Alerting runs both rule checks and actions as persistent background tasks managed by the Task Manager.

When relying on rules and actions as mission critical services, make sure you follow the [production considerations](kibana-task-manager-scaling-considerations.md) for Task Manager.

## Running background rule checks and actions [alerting-background-tasks]

{{kib}} uses background tasks to run rules and actions, distributed across all {{kib}} instances in the cluster.

By default, each {{kib}} instance polls for work at 500-millisecond intervals, and can run a maximum of ten concurrent tasks. These tasks are then run on the {{kib}} server.

Rules are recurring background tasks which are rescheduled according to the check interval on completion. Actions are non-recurring background tasks which are deleted on completion.

For more details on Task Manager, see [Running background tasks](../distributed-architecture/kibana-tasks-management.md#task-manager-background-tasks).

::::{important}
Rule and action tasks can run late or at an inconsistent schedule. This is typically a symptom of the specific usage of the cluster in question.

You can address such issues by tweaking the [Task Manager settings](kibana://reference/configuration-reference/task-manager-settings.md) or scaling the deployment to better suit your use case.

For detailed guidance, see [Alerting Troubleshooting](../../explore-analyze/alerts-cases/alerts/alerting-troubleshooting.md).

::::

## Scaling guidance [alerting-scaling-guidance]

As rules and actions leverage background tasks to perform the majority of work, scaling Alerting is possible by following the [Task Manager Scaling Guidance](kibana-task-manager-scaling-considerations.md#task-manager-scaling-guidance).

When estimating the required task throughput, keep the following in mind:

- Each rule uses a single recurring task that is scheduled to run at the cadence defined by its check interval.
- Each action uses a single task. However, because actions are taken per instance, alerts can generate a large number of non-recurring tasks.

It is difficult to predict how much throughput is needed to ensure all rules and actions are executed at consistent schedules. By counting rules as recurring tasks and actions as non-recurring tasks, a rough throughput [can be estimated](kibana-task-manager-scaling-considerations.md#task-manager-rough-throughput-estimation) as a _tasks per minute_ measurement.

Predicting the buffer required to account for actions depends heavily on the rule types you use, the amount of alerts they might detect, and the number of actions you might choose to assign to action groups. With that in mind, regularly [monitor the health](../monitor/kibana-task-manager-health-monitoring.md) of your Task Manager instances.

## Event log index lifecycle management [event-log-ilm]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::

Alerts and actions log activity in a set of "event log" data streams, one per {{kib}} version, named `.kibana-event-log-{{VERSION}}`. These data streams are configured with a lifecycle data retention of 90 days. This can be updated to other values via the standard data stream lifecycle APIs. Note that the event log data contains the data shown in the alerting pages in {{kib}}, so reducing the data retention period will result in less data being available to view.

For more information on data stream lifecycle management, see: [Data stream lifecycle](../../manage-data/lifecycle/data-stream.md).

## Circuit breakers [alerting-circuit-breakers]

There are several scenarios where running alerting rules and actions can start to negatively impact the overall health of a {{kib}} instance either by clogging up Task Manager throughput or by consuming so much CPU/memory that other operations cannot complete in a reasonable amount of time. There are several [configurable](kibana://reference/configuration-reference/alerting-settings.md#alert-settings) circuit breakers to help minimize these effects.

### Rules with very short intervals [_rules_with_very_short_intervals]

Running large numbers of rules at very short intervals can quickly clog up Task Manager throughput, leading to higher schedule drift. Use `xpack.alerting.rules.minimumScheduleInterval.value` to set a minimum schedule interval for rules. The default (and recommended) value for this configuration is `1m`. Use `xpack.alerting.rules.minimumScheduleInterval.enforce` to specify whether to strictly enforce this minimum. While the default value for this setting is `false` to maintain backwards compatibility with existing rules, set this to `true` to prevent new and updated rules from running at an interval below the minimum.

Another related setting is `xpack.alerting.rules.maxScheduledPerMinute`, which limits the number of rules that can run per minute. For example if it’s set to `400`, you can have 400 rules with one minute check intervals or 2,000 rules with 5 minute check intervals. You cannot create or edit a rule if its check interval would cause this setting to be exceeded. To stay within this limit, delete or disable some rules or update the check intervals so that your rules run less frequently. Default value of this config is 32,000, you should change this if you want to run more than 32,000 rules per minute.

### Rules that run for a long time [_rules_that_run_for_a_long_time]

Rules that run for a long time typically do so because they are issuing resource-intensive {{es}} queries or performing CPU-intensive processing. This can block the event loop, making {{kib}} inaccessible while the rule runs. By default, rule processing is cancelled after `5m` but this can be overridden using the `xpack.alerting.rules.run.timeout` configuration. This value can also be configured per rule type using `xpack.alerting.rules.run.ruleTypeOverrides`. For example, the following configuration sets the global timeout value to `1m` while allowing **Index Threshold** rules to run for `10m` before being cancelled.

```yaml
xpack.alerting.rules.run:
  timeout: "1m"
  ruleTypeOverrides:
    - id: ".index-threshold"
      timeout: "10m"
```

When a rule run is cancelled, any alerts and actions that were generated during the run are discarded. This behavior is controlled by the `xpack.alerting.cancelAlertsOnRuleTimeout` configuration, which defaults to `true`. Set this to `false` to receive alerts and actions after the timeout, although be aware that these may be incomplete and possibly inaccurate.

### Rules that spawn too many actions [_rules_that_spawn_too_many_actions]

Rules that spawn too many actions can quickly clog up Task Manager throughput. This can occur if:

- A rule configured with a single action generates many alerts. For example, if a rule configured to run a single email action generates 100,000 alerts, then 100,000 actions will be scheduled during a run.
- A rule configured with multiple actions generates alerts. For example, if a rule configured to run an email action, a server log action and a webhook action generates 30,000 alerts, then 90,000 actions will be scheduled during a run.

Use `xpack.alerting.rules.run.actions.max` to limit the maximum number of actions a rule can generate per run. This value can also be configured by connector type using `xpack.alerting.rules.run.actions.connectorTypeOverrides`. For example, the following config sets the global maximum number of actions to 100 while allowing rules with **Email** actions to generate up to 200 actions.

```yaml
xpack.alerting.rules.run:
  actions:
    max: 100
    connectorTypeOverrides:
      - id: ".email"
        max: 200
```
