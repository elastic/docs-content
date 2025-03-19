::::{tip}
By default, the monitoring metrics are stored in local indices. In production, we strongly recommend using a [separate monitoring cluster](/deploy-manage/monitor/stack-monitoring.md#production-architecture). Using a separate monitoring cluster prevents production cluster outages from impacting your ability to access your monitoring data. It also prevents monitoring activities from impacting the performance of your production cluster. For the same reason, we also recommend using a separate {{kib}} instance for viewing the monitoring data.
::::
