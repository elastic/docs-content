---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/task-manager-production-considerations.html
---

# Kibana tasks management [task-manager-production-considerations]

{{kib}} Task Manager is leveraged by features such as Alerting, Actions, and Reporting to run mission critical work as persistent background tasks. These background tasks distribute work across multiple {{kib}} instances. This has three major benefits:

* **Persistence**: All task state and scheduling is stored in {{es}}, so if you restart {{kib}}, tasks will pick up where they left off.
* **Scaling**: Multiple {{kib}} instances can read from and update the same task queue in {{es}}, allowing the work load to be distributed across instances. If a {{kib}} instance no longer has capacity to run tasks, you can increase capacity by adding additional {{kib}} instances.
* **Load Balancing**: Task Manager is equipped with a reactive self-healing mechanism, which allows it to reduce the amount of work it executes in reaction to an increased load related error rate in {{es}}. Additionally, when Task Manager experiences an increase in recurring tasks, it attempts to space out the work to better balance the load.

::::{important}
Task definitions for alerts and actions are stored in the index called `.kibana_task_manager`.

You must have at least one replica of this index for production deployments.

If you lose this index, all scheduled alerts and actions are lost.

::::

## Running background tasks [task-manager-background-tasks]

{{kib}} background tasks are managed as follows:

* An {{es}} task index is polled for overdue tasks at 3-second intervals. You can change this interval using the [`xpack.task_manager.poll_interval`](kibana://reference/configuration-reference/task-manager-settings.md#task-manager-settings) setting.
* Tasks are claimed by updating them in the {{es}} index, using optimistic concurrency control to prevent conflicts. Each {{kib}} instance can run a maximum of 10 concurrent tasks, so a maximum of 10 tasks are claimed each interval.
* Tasks are run on the {{kib}} server.
* Task Manager ensures that tasks:
  * Are only executed once
  * Are retried when they fail (if configured to do so)
  * Are rescheduled to run again at a future point in time (if configured to do so)

::::{important}
It is possible for tasks to run late or at an inconsistent schedule.

This is usually a symptom of the specific usage or scaling strategy of the cluster in question.

To address these issues, tweak the {{kib}} Task Manager settings or the cluster scaling strategy to better suit the unique use case.

For details on the settings that can influence the performance and throughput of Task Manager, see [Task Manager Settings](kibana://reference/configuration-reference/task-manager-settings.md).

For detailed troubleshooting guidance, see [Troubleshooting](../../troubleshoot/kibana/task-manager.md).

::::

{{es}} and {{kib}} instances use the system clock to determine the current time. To ensure schedules are triggered when expected, synchronize the clocks of all nodes in the cluster using a time service such as [Network Time Protocol](http://www.ntp.org/).

By default, {{kib}} polls for tasks at a rate of 10 tasks every 3 seconds. This means that you can expect a single {{kib}} instance to support up to 200 *tasks per minute* (`200/tpm`).

How you deploy {{kib}} largely depends on your use case. Predicting the throughout a deployment might require to support Task Management is difficult because features can schedule an unpredictable number of tasks at a variety of scheduled cadences.

In practice, a {{kib}} instance will only achieve the upper bound of `200/tpm` if the duration of task execution is below the polling rate of 3 seconds. For the most part, the duration of tasks is below that threshold, but it can vary greatly as {{es}} and {{kib}} usage grow and task complexity increases (such as alerts executing heavy queries across large datasets).

For more information on scaling, see [Kibana task manager scaling considerations](../../deploy-manage/production-guidance/kibana-task-manager-scaling-considerations.md).
