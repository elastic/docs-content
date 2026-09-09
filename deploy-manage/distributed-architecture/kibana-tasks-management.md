---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/task-manager-production-considerations.html
applies_to:
  stack:
products:
  - id: kibana
---

# {{kib}} task management [task-manager-production-considerations]

{{kib}} Task Manager is used by features such as Alerting, Actions, and Reporting to run mission critical work as persistent background tasks. These background tasks distribute work across multiple {{kib}} instances. This has three major benefits:

- **Persistence**: All task state and scheduling is stored in {{es}}, so if you restart {{kib}}, tasks will pick up where they left off.
- **Scaling**: Multiple {{kib}} instances can read from and update the same task queue in {{es}}, allowing the work load to be distributed across instances. If a {{kib}} instance no longer has capacity to run tasks, you can increase capacity by adding additional {{kib}} instances. For more information on scaling, see [{{kib}} task manager scaling considerations](../../deploy-manage/production-guidance/kibana-task-manager-scaling-considerations.md#task-manager-scaling-guidance).
- **Load Balancing**: Task Manager is equipped with a reactive self-healing mechanism, which allows it to reduce the amount of work it executes in reaction to an increased load related error rate in {{es}}. Additionally, when Task Manager experiences an increase in recurring tasks, it attempts to space out the work to better balance the load.

::::{important}
Task definitions for alerts and actions are stored in the index called `.kibana_task_manager`.

You must have at least one replica of this index for production deployments.

If you lose this index, all scheduled alerts and actions are lost.

::::

## How background tasks are managed [task-manager-background-tasks]

{{kib}} background tasks are managed as follows:

- An {{es}} task index is polled for overdue tasks at 500-millisecond intervals. You can change this interval using the [`xpack.task_manager.poll_interval`](kibana://reference/configuration-reference/task-manager-settings.md#task-manager-settings) setting.
- Tasks are claimed by updating them in the {{es}} index, using optimistic concurrency control to prevent conflicts. Each {{kib}} instance can run a maximum of 10 concurrent tasks, so a maximum of 10 tasks are claimed each interval.
- {{es}} and {{kib}} instances use the system clock to determine the current time. To ensure schedules are triggered when expected, synchronize the clocks of all nodes in the cluster using a time service such as [Network Time Protocol](http://www.ntp.org/).
- Tasks are run on the {{kib}} server. In large deployments with high background task and user traffic workloads, it is recommended to run tasks on dedicated {{kib}} nodes to prevent resource contention. Refer to [Dedicated background task nodes](#task-manager-dedicated-task-nodes).
- Task Manager ensures that tasks:
  - Are only executed once
  - Are retried when they fail (if configured to do so)
  - Are rescheduled to run again at a future point in time (if configured to do so)
    ::::{important}
    It is possible for tasks to run late or at an inconsistent schedule.

This is usually a symptom of the specific usage or scaling strategy of the cluster in question.

To address these issues, tweak the {{kib}} Task Manager settings or the cluster scaling strategy to better suit the unique use case.

For details on the settings that can influence the performance and throughput of Task Manager, see [Task Manager Settings](kibana://reference/configuration-reference/task-manager-settings.md).

For detailed troubleshooting guidance, see [Troubleshooting](../../troubleshoot/kibana/task-manager.md).

::::

## Dedicated background task nodes [task-manager-dedicated-task-nodes]

Because tasks run on the {{kib}} server, heavy background workloads can compete with user traffic for resources. To avoid this, it is recommended to run background tasks on dedicated {{kib}} nodes:

- On self-managed and {{eck}} deployments, set `node.roles: ["background_tasks"]` in [`kibana.yml`](/deploy-manage/stack-settings.md) to dedicate a {{kib}} instance to background tasks.
- On {{ech}} and {{ece}} deployments, when {{kib}} is allocated more than 8 GB of RAM, it is automatically split into multiple instances with specialized roles: UI nodes, which serve user requests, and background task nodes, which run Task Manager tasks.

To identify a node's type on {{ech}} and {{ece}} deployments, check the node's instance name in the `kibana_status.json` file included in the [{{kib}} diagnostic bundle](/troubleshoot/kibana/capturing-diagnostics.md). A UI node's instance name contains `- UI`.

On {{ech}} and {{ece}} deployments, API requests, including health and monitoring APIs such as `GET api/task_manager/_health`, are always served by UI nodes, so their responses don't reflect task execution state. On self-managed and {{eck}} deployments, the same applies to any request served by a node without the `background_tasks` role. To retrieve complete Task Manager health data, refer to [Retrieve health data when {{kib}} uses separate task nodes](/troubleshoot/kibana/task-manager.md#task-manager-health-multi-node).
