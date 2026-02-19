---
navigation_title: "{{kib}} task manager monitoring"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/task-manager-health-monitoring.html
applies_to:
  stack: preview
products:
  - id: kibana
---

# {{kib}} task manager health monitoring [task-manager-health-monitoring]


::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


The {{kib}} [Task Manager](/deploy-manage/distributed-architecture/kibana-tasks-management.md) has an internal monitoring mechanism to keep track of a variety of metrics, which can be consumed with either the health monitoring API or the {{kib}} server log.

The health monitoring API provides a reliable endpoint that can be monitored. Consuming this endpoint doesn’t cause additional load, but rather returns the latest health checks made by the system. This design enables consumption by external monitoring services at a regular cadence without additional load to the system.

Each {{kib}} instance exposes its own endpoint at:

```bash
$ curl -X GET api/task_manager/_health
```

Monitoring the `_health` endpoint of each {{kib}} instance in the cluster is the recommended method of ensuring confidence in mission critical services such as Alerting, Actions, and Reporting.


## Configuring the monitored health statistics [task-manager-configuring-health-monitoring]

The health monitoring API monitors the performance of Task Manager out of the box.  However, certain performance considerations are deployment specific and you can configure them.

A health threshold is the threshold for failed task executions.  Once a task exceeds this threshold, a status of `warn` or `error` is set on the task type execution. To configure a health threshold, use the [`xpack.task_manager.monitored_task_execution_thresholds`](kibana://reference/configuration-reference/task-manager-settings.md#task-manager-health-settings) setting.  You can apply this this setting to all task types in the system, or to a custom task type.

By default, this setting marks the health of every task type as `warning` when it exceeds 80% failed executions, and as `error` at 90%. Set this value to a number between 0 to 100. The threshold is hit when the value **exceeds** this number. To avoid a status of `error`, set the threshold at 100.  To hit `error` the moment any task fails, set the threshold to 0.

Create a custom configuration to set lower thresholds for task types you consider critical, such as alerting tasks that you want to detect sooner in an external monitoring service.

```yaml
xpack.task_manager.monitored_task_execution_thresholds:
  default: <1>
    error_threshold: 70
    warn_threshold: 50
  custom:
    "alerting:.index-threshold": <2>
      error_threshold: 50
      warn_threshold: 0
```

1. A default configuration that sets the system-wide `warn` threshold at a 50% failure rate, and `error` at 70% failure rate.
2. A custom configuration for the `alerting:.index-threshold` task type that sets a system wide `warn` threshold at 0% (which sets a `warn` status the moment any task of that type fails), and `error` at a 50% failure rate.



## Consuming health stats [task-manager-consuming-health-stats]

The health API is best consumed using the `/api/task_manager/_health` endpoint.

Additionally, there are two ways to consume these metrics:

### Debug logging
```{applies_to}
deployment:
  self:
  ece:
  eck:
```

In self-managed deployments, you can configure health stats to be logged in the {{kib}} `DEBUG` logger at a regular cadence. To enable Task Manager debug logging in your {{kib}} instance, add the following to your [`kibana.yml`](/deploy-manage/stack-settings.md):

```yaml
logging:
  loggers:
      - context: plugins.taskManager
        appenders: [console]
        level: debug
```

These stats are logged based on the number of milliseconds set in your [`xpack.task_manager.poll_interval`](kibana://reference/configuration-reference/task-manager-settings.md#task-manager-settings) setting, which could add substantial noise to your logs. Only enable this level of logging temporarily.

### Automatic logging

By default, the health API runs at a regular cadence, and each time it runs, it attempts to self evaluate its performance. If this self evaluation yields a potential problem, a message will log to the {{kib}} server log. In addition, the health API will look at how long tasks have waited to start (from when they were scheduled to start). If this number exceeds a configurable threshold ([`xpack.task_manager.monitored_stats_health_verbose_log.warn_delayed_task_start_in_seconds`](kibana://reference/configuration-reference/task-manager-settings.md#task-manager-settings)), the same message as above will log to the {{kib}} server log.

This message looks like:

```txt subs=true
Detected potential performance issue with Task Manager. Set 'xpack.task_manager.monitored_stats_health_verbose_log.enabled: true' in your {{kib}}.yml to enable debug logging`
```

If this message appears, set [`xpack.task_manager.monitored_stats_health_verbose_log.enabled`](kibana://reference/configuration-reference/task-manager-settings.md#task-manager-settings) to `true` in your [`kibana.yml`](/deploy-manage/stack-settings.md). This will start logging the health metrics at either a `warn` or `error` log level, depending on the detected severity of the potential problem.


## Making sense of Task Manager health stats [making-sense-of-task-manager-health-stats]

The health monitoring API exposes the following sections:

| Section | Description |
| --- | --- |
| Configuration | This section summarizes the current configuration of Task Manager.  This includes dynamic configurations that change over time, such as `poll_interval` and `max_workers`, which can adjust in reaction to changing load on the system. |
| Workload | This section summarizes the work load across the cluster, including the tasks in the system, their types, and current status. |
| Runtime | This section tracks execution performance of Task Manager, tracking task *drift*, worker *load*, and execution stats broken down by type, including duration and execution results. |
| Capacity Estimation | This section provides a rough estimate about the sufficiency of its capacity. As the name suggests, these are estimates based on historical data and should not be used as predictions. Use these estimations when following the Task Manager [Scaling guidance](../production-guidance/kibana-task-manager-scaling-considerations.md#task-manager-scaling-guidance). |

Each section has a `timestamp` and a `status` that indicates when the last update to this section took place and whether the health of this section was evaluated as `OK`, `Warning` or `Error`.

The root `status` indicates the `status` of the system overall.

The Runtime `status` indicates whether task executions have exceeded any of the [configured health thresholds](#task-manager-configuring-health-monitoring). An `OK` status means none of the threshold have been exceeded. A `Warning` status means that at least one warning threshold has been exceeded. An `Error` status means that at least one error threshold has been exceeded.

::::{important}
Some tasks (such as [connectors](../manage-connectors.md)) will incorrectly report their status as successful even if the task failed. The runtime and workload block will return data about success and failures and will not take this into consideration.

To get a better sense of action failures, refer to the [Event log index](../../explore-analyze/alerting/alerts/event-log-index.md) for more accurate context into failures and successes.

::::


The Capacity Estimation `status` indicates the sufficiency of the observed capacity. An `OK` status means capacity is sufficient. A `Warning` status means that capacity is sufficient for the scheduled recurring tasks, but non-recurring tasks often cause the cluster to exceed capacity. An `Error` status means that there is insufficient capacity across all types of tasks.

By monitoring the `status` of the system overall, and the `status` of specific task types of interest, you can evaluate the health of the {{kib}} Task Management system.
