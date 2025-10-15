---
navigation_title: Manage background tasks
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/task-manager-production-considerations.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
products:
  - id: kibana
---

# {{kib}} task manager: performance and scaling guide [task-manager-production-considerations]

{{kib}} Task Manager is leveraged by features such as [alerting](/explore-analyze/alerts-cases/alerts.md), [actions](/explore-analyze/alerts-cases/alerts.md#rules-actions), and [reporting](/explore-analyze/report-and-share.md) to run mission critical work as persistent background tasks. These background tasks distribute work across multiple {{kib}} instances. This has three major benefits:

- **Persistence**: All task state and scheduling is stored in {{es}}, so if you restart {{kib}}, tasks will pick up where they left off.
- **Scaling**: Multiple {{kib}} instances can read from and update the same task queue in {{es}}, allowing the work load to be distributed across instances. If a {{kib}} instance no longer has capacity to run tasks, you can increase capacity by adding additional {{kib}} instances.
- **Load Balancing**: Task Manager is equipped with a reactive self-healing mechanism, which allows it to reduce the amount of work it executes in reaction to an increased load related error rate in {{es}}. Additionally, when Task Manager experiences an increase in recurring tasks, it attempts to space out the work to better balance the load.

::::{important}
Task definitions for alerts and actions are stored in the index called `.kibana_task_manager`.

You must have at least one replica of this index for production deployments.

If you lose this index, all scheduled alerts and actions are lost.
::::

## Running background tasks [task-manager-background-tasks]

{{kib}} background tasks are managed as follows:

- An {{es}} task index is polled for overdue tasks at 500-millisecond intervals. You can change this interval using the [`xpack.task_manager.poll_interval`](kibana://reference/configuration-reference/task-manager-settings.md#task-manager-settings) setting.
- Tasks are claimed by updating them in the {{es}} index, using optimistic concurrency control to prevent conflicts. Each {{kib}} instance can run a maximum of 10 concurrent tasks, so a maximum of 10 tasks are claimed each interval.
- Tasks are run on the {{kib}} server.
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

## Deployment considerations [_deployment_considerations]

{{es}} and {{kib}} instances use the system clock to determine the current time. To ensure schedules are triggered when expected, synchronize the clocks of all nodes in the cluster using a time service such as [Network Time Protocol](http://www.ntp.org/).

## Scaling guidance [task-manager-scaling-guidance]

How you deploy {{kib}} largely depends on your use case. Predicting the throughput a deployment requires to support Task Management is difficult because features can schedule an unpredictable number of tasks at a variety of scheduled cadences.

However, there is a relatively straight forward method you can follow to produce a rough estimate based on your expected usage.

### Default scale [task-manager-default-scaling]

By default, {{kib}} polls for tasks at a rate of 10 tasks every 500 milliseconds. This means that you can expect a single {{kib}} instance to support up to 1200 _tasks per minute_ (`1200/tpm`).

- As of v8.15 a new task claim strategy was introduced: `mget`. And as of v8.18, `mget` has been made the default strategy -as part of some performance improvement efforts-, with a default polling interval of 500 milliseconds. Since these changes offers a better task execution performance, It is highly recommended you to upgrade to v8.18.

- Maximum number of concurrent tasks can be changed by using `xpack.task_manager.capacity`, The default value is 10, the minimum and maximum values are 5 and 50 respectively.

In practice, a {{kib}} instance will only achieve the upper bound of `1200/tpm` if the duration of task execution is below the polling rate of 500 milliseconds. But for the most part, the duration of tasks is above that threshold, it can vary greatly as {{es}} and {{kib}} usage grow and task complexity increases (such as alerts executing heavy queries across large datasets). Therefore you should find your the average execution time of your tasks to estimate the number of {{kib}} instances you need.

By [estimating a rough throughput requirement](#task-manager-rough-throughput-estimation), you can estimate the number of {{kib}} instances required to reliably execute tasks in a timely manner. An appropriate number of {{kib}} instances can be estimated to match the required scale.

For details on monitoring the health of {{kib}} Task Manager, follow the guidance in [Health monitoring](../monitor/kibana-task-manager-health-monitoring.md).

### Scaling horizontally [task-manager-scaling-horizontally]

At times, the sustainable approach might be to expand the throughput of your cluster by provisioning additional {{kib}} instances. By default, each additional {{kib}} instance will add an additional 10 tasks that your cluster can run concurrently, but you can also scale each {{kib}} instance vertically, if your diagnosis indicates that they can handle the additional workload.

### Scaling vertically [task-manager-scaling-vertically]

Other times it, might be preferable to increase the throughput of individual {{kib}} instances.

Tweak the capacity with the [`xpack.task_manager.capacity`](kibana://reference/configuration-reference/task-manager-settings.md#task-manager-settings) setting, which enables each {{kib}} instance to pull a higher number of tasks per interval. This setting can impact the performance of each instance as the workload will be higher.

Tweak the poll interval with the [`xpack.task_manager.poll_interval`](kibana://reference/configuration-reference/task-manager-settings.md#task-manager-settings) setting, which enables each {{kib}} instance to pull scheduled tasks at a higher rate. This setting can impact the performance of the {{es}} cluster as the workload will be higher.

### Choosing a scaling strategy [task-manager-choosing-scaling-strategy]

Each scaling strategy comes with its own considerations, and the appropriate strategy largely depends on your use case.

Scaling {{kib}} instances vertically causes higher resource usage in each {{kib}} instance, as it will perform more concurrent work. Scaling {{kib}} instances horizontally requires a higher degree of coordination, which can impact overall performance.

A recommended strategy is to follow these steps:

1. Produce a [rough throughput estimate](#task-manager-rough-throughput-estimation) as a guide to provisioning as many {{kib}} instances as needed. Include any growth in tasks that you predict experiencing in the near future, and a buffer to better address ad-hoc tasks.
2. After provisioning a deployment, assess whether the provisioned {{kib}} instances achieve the required throughput by evaluating the [Health monitoring](../monitor/kibana-task-manager-health-monitoring.md) as described in [Insufficient throughput to handle the scheduled workload](../../troubleshoot/kibana/task-manager.md#task-manager-theory-insufficient-throughput).
3. If the throughput is insufficient, and {{kib}} instances exhibit low resource usage, incrementally scale vertically while [monitoring](../monitor/monitoring-data/kibana-page.md) the impact of these changes.
4. If the throughput is insufficient, and {{kib}} instances are exhibiting high resource usage, incrementally scale horizontally by provisioning new {{kib}} instances and reassess.

Task Manager, like the rest of the {{stack}}, is designed to scale horizontally. Take advantage of this ability to ensure mission critical services, such as Alerting, Actions, and Reporting, always have the capacity they need.

Scaling horizontally requires a higher degree of coordination between {{kib}} instances. One way Task Manager coordinates with other instances is by delaying its polling schedule to avoid conflicts with other instances. By using [health monitoring](../monitor/kibana-task-manager-health-monitoring.md) to evaluate the [date of the `last_polling_delay`](../../troubleshoot/kibana/task-manager.md#task-manager-health-evaluate-the-runtime) across a deployment, you can estimate the frequency at which Task Manager resets its delay mechanism. A higher frequency suggests {{kib}} instances conflict at a high rate, which you can address by scaling vertically rather than horizontally, reducing the required coordination.

### Rough throughput estimation [task-manager-rough-throughput-estimation]

Predicting the required throughput a deployment might need to support Task Management is difficult, as features can schedule an unpredictable number of tasks at a variety of scheduled cadences. However, a rough lower bound can be estimated, which is then used as a guide.

Throughput is best thought of as a measurements in tasks per minute.

A default {{kib}} instance can support up to `1200/tpm`.

#### Automatic estimation [_automatic_estimation]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::

As demonstrated in [Evaluate your capacity estimation](../../troubleshoot/kibana/task-manager.md#task-manager-health-evaluate-the-capacity-estimation), the Task Manager [health monitoring](../monitor/kibana-task-manager-health-monitoring.md) performs these estimations automatically.

These estimates are based on historical data and should not be used as predictions, but can be used as a rough guide when scaling the system.

We recommend provisioning enough {{kib}} instances to ensure a buffer between the observed maximum throughput (as estimated under `observed.max_throughput_per_minute`) and the average required throughput (as estimated under `observed.avg_required_throughput_per_minute`). Otherwise there might be insufficient capacity to handle spikes of ad-hoc tasks. How much of a buffer is needed largely depends on your use case, but keep in mind that estimated throughput takes into account recent spikes and, as long as they are representative of your system’s behavior, shouldn’t require much of a buffer.

We recommend provisioning at least as many {{kib}} instances as proposed by `proposed.provisioned_kibana`, but keep in mind that this number is based on the estimated required throughput, which is based on average historical performance, and cannot accurately predict future requirements.

::::{warning}
Automatic capacity estimation is performed by each {{kib}} instance independently. This estimation is performed by observing the task throughput in that instance, the number of {{kib}} instances executing tasks at that moment in time, and the recurring workload in {{es}}.

If a {{kib}} instance is idle at the moment of capacity estimation, the number of active {{kib}} instances might be miscounted and the available throughput miscalculated.

When evaluating the proposed {{kib}} instance number under `proposed.provisioned_kibana`, we highly recommend verifying that the `observed.observed_kibana_instances` matches the number of provisioned {{kib}} instances.

::::

#### Manual estimation [_manual_estimation]

By [evaluating the workload](../../troubleshoot/kibana/task-manager.md#task-manager-health-evaluate-the-workload), you can make a rough estimate as to the required throughput as a _tasks per minute_ measurement.

For example, suppose your current workload reveals a required throughput of `1920/tpm`. You can address this scale by provisioning 2 {{kib}} instances, with an upper throughput of `2400/tpm`. This scale would provide approximately 25% additional capacity to handle ad-hoc non-recurring tasks and potential growth in recurring tasks.

Given a deployment of 600 recurring tasks, estimating the required throughput depends on the scheduled cadence. Suppose you expect to run 300 tasks at a cadence of `10s`, the other 300 tasks at `20m`. In addition, you expect a couple dozen non-recurring tasks every minute.

A non-recurring task requires a single execution, which means that a single {{kib}} instance could execute all 100 tasks in less than a minute, using only half of its capacity. As these tasks are only executed once, the {{kib}} instance will sit idle once all tasks are executed. For that reason, don’t include non-recurring tasks in your _tasks per minute_ calculation. Instead, include a buffer in the final _lower bound_ to incur the cost of ad-hoc non-recurring tasks.

A recurring task requires as many executions as its cadence can fit in a minute. A recurring task with a `10s` schedule will require `6/tpm`, as it will execute 6 times per minute. A recurring task with a `20m` schedule only executes 3 times per hour and only requires a throughput of `0.05/tpm`, a number so small it that is difficult to take it into account.

For this reason, we recommend grouping tasks by _tasks per minute_ and _tasks per hour_, as demonstrated in [Evaluate your workload](../../troubleshoot/kibana/task-manager.md#task-manager-health-evaluate-the-workload), averaging the _per hour_ measurement across all minutes.

It is highly recommended that you maintain at least 20% additional capacity, beyond your expected workload, as spikes in ad-hoc tasks is possible at times of high activity (such as a spike in actions in response to an active alert).

Given the predicted workload, you can estimate a lower bound throughput of `2175/tpm` (`6/tpm` \* 300 + `0.05/tph` \* 300 + 20% buffer). As a default, a {{kib}} instance provides a throughput of `1200/tpm`. A good starting point for your deployment is to provision 2 {{kib}} instances. You could then monitor their performance and reassess as the required throughput becomes clearer.

Although this is a _rough_ estimate, the _tasks per minute_ provides the lower bound needed to execute tasks on time.

Once you estimate _tasks per minute_ , add a buffer for non-recurring tasks. How much of a buffer is required largely depends on your use case. Ensure enough of a buffer is provisioned by [evaluating your workload](../../troubleshoot/kibana/task-manager.md#task-manager-health-evaluate-the-workload) as it grows and tracking the ratio of recurring to non-recurring tasks by [evaluating your runtime](../../troubleshoot/kibana/task-manager.md#task-manager-health-evaluate-the-runtime).
