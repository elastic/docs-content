# Monitoring your deployment [ec-monitoring]

::::{admonition}
If you’re using Elastic Cloud Hosted, then you can use AutoOps to monitor your cluster. AutoOps significantly simplifies cluster management with performance recommendations, resource utilization visibility, real-time issue detection and resolution paths. AutoOps is [rolling out](../../../deploy-manage/monitor/autoops/ec-autoops-regions.md) in phases across Elastic Cloud Hosted regions and CSP. It will be automatically activated for your deployment, with no installation required. For more information, check [Monitor with AutoOps](../../../deploy-manage/monitor/autoops.md).

::::


Keeping on top of the health of your deployments is a key part of the [shared responsibilities](https://www.elastic.co/cloud/shared-responsibility) between Elastic and yourself. Elastic Cloud provides out of the box tools for monitoring the health of your deployment and resolving health issues when they arise. If you are ready to set up a deployment for production use cases, make sure you check the recommendations and best practices for [production readiness](../../../deploy-manage/production-guidance/plan-for-production-elastic-cloud.md).

A deployment on Elastic Cloud is a combination of an Elasticsearch cluster, a Kibana instance and potentially an APM server instance, and an Integration Server instance. The health of an Elastic Cloud deployment comprises the health of the various components that are part of the deployment.

The most important of these is the {{es}} cluster, because it is the heart of the system for searching and indexing data.

This section provides some best practices to help you monitor and understand the ongoing state of your deployments and their resources.

* [{{es}} cluster health](../../../deploy-manage/monitor/stack-monitoring.md#ec-es-cluster-health)
* [{{es}} cluster performance](../../../deploy-manage/monitor/stack-monitoring.md#ec-es-cluster-performance)
* [Health warnings](../../../deploy-manage/monitor/stack-monitoring.md#ec-es-health-warnings)
* [Preconfigured logs and metrics](../../../deploy-manage/monitor/stack-monitoring.md#ec-es-health-preconfigured)
* [Dedicated logs and metrics](../../../deploy-manage/monitor/stack-monitoring.md#ec-es-health-dedicated)
* [Understanding deployment health](../../../deploy-manage/monitor/stack-monitoring.md#ec-health-best-practices)


## {{es}} cluster health [ec-es-cluster-health]

Health is reported based on the following areas: Shard availability, master node health, Snapshot Lifecycle Management (SLM), Index Lifecycle Management (ILM), and repository integrity.

For {{stack}} versions 8.3 and below, the deployment **Health** page is limited. Health issues are displayed in a banner with no details on impacts and troubleshooting steps. Follow [these steps](../../../deploy-manage/upgrade/deployment-or-cluster.md) if you want to perform a version upgrade.

For {{stack}} versions 8.4 and later, the deployment **Health** page provides detailed information on health issues, impacted areas, and troubleshooting support.

To view the health for a deployment:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Deployments** page, select your deployment.
3. In your deployment menu, select **Health**.

The **Health** page provides the following information:

* Health issues for Kibana, Enterprise Search, APM and plan changes are reported in the health banner.
* Health issues for {{es}} clusters are broken down into a table with more details on Severity, Description and Affected capabilities.

:::{image} ../../../images/cloud-es-health-page.png
:alt: {{es}} Health page
:::

**Severity**: A critical issue impacts operations such as search and ingest and should be addressed as soon as possible. Warnings don’t impact the cluster immediately but might lead to more critical issues over time such as a corrupted repository might lead to no backups being available in the future.

**Description**: For most issues, you can click the description to get more details page on the specific issue and on how to fix it.

**Affected capabilities**: Each of these areas might impact Search, Ingest, Backups or Deployment Management capabilities.

You can also search and filter the table based on affected resources, such as indices, repositories, nodes, or SLM policies. Individual issues can be further expanded to get more details and guided troubleshooting.

:::{image} ../../../images/cloud-es-health-page-table.png
:alt: {{es}} Health page with details and troubleshooting
:::

For each issue you can either use a troubleshooting link or get a suggestion to contact support, in case you need help. The [troubleshooting documentation](../../../troubleshoot/elasticsearch/elasticsearch.md) for {{es}} provides more details on specific errors.


## {{es}} cluster performance [ec-es-cluster-performance]

The deployment **Health** page does not include information on cluster performance. If you observe issues on search and ingest operations in terms of increased latency or throughput for queries, these might not be directly reported on the **Health** page, unless they are related to shard health or master node availability. The performance page and the out-of-the-box logs allow you to monitor your cluster performance, but for production applications we strongly recommend setting up a dedicated monitoring cluster. Check [Understanding deployment health](../../../deploy-manage/monitor/stack-monitoring.md#ec-health-best-practices), for more guidelines on how to monitor you cluster performance.


## Health warnings [ec-es-health-warnings]

In the normal course of using your {{ech}} deployments, health warnings and errors might appear from time to time. Following are the most common scenarios and methods to resolve them.

Health warning messages
:   Health warning messages will sometimes appear on the main page for one of your deployments, as well as on the **Logs and metrics** page.

    A single warning is rarely cause for concern, as often it just reflects ongoing, routine maintenance activity occurring on {{ecloud}}.


Configuration change failures
:   In more serious cases, your deployment may be unable to restart. The failure can be due to a variety of causes, the most frequent of these being invalid secure settings, expired plugins or bundles, or out of memory errors. The problem is often not detected until an attempt is made to restart the deployment following a routine configuration change, such as a deployment resizing.

Out of memory errors
:   Out of memory errors (OOMs) may occur during your deployment’s normal operations, and these can have a very negative impact on performance. Common causes of memory shortages are oversharding, data retention oversights, and the overall request volume.

    On your deployment page, you can check the [JVM memory pressure indicator](../../../deploy-manage/monitor/monitoring-data/ec-memory-pressure.md) to get the current memory usage of each node of your deployment. You can also review the [common causes of high JVM memory usage](../../../deploy-manage/monitor/monitoring-data/ec-memory-pressure.md#ec-memory-pressure-causes) to help diagnose the source of unexpectedly high memory pressure levels. To learn more, check [How does high memory pressure affect performance?](../../../troubleshoot/monitoring/high-memory-pressure.md).



## Preconfigured logs and metrics [ec-es-health-preconfigured]

In a non-production environment, you may choose to rely on the logs and metrics that are available for your deployment by default. The deployment **Logs and metrics** page displays any current deployment health warnings, and from there you can also view standard log files from the last 24 hours.

The logs capture any activity related to your deployments, their component resources, snapshotting behavior, and more. You can use the search bar to filter the logs by, for example, a specific instance (`instance-0000000005`), a configuration file (`roles.yml`), an operation type (`snapshot`, `autoscaling`), or a component (`kibana`, `ent-search`).

In a production environment, we highly recommend storing your logs and metrics in another cluster. This gives you the ability to retain your logs and metrics over longer periods of time and setting custom alerts and watches.


## Dedicated logs and metrics [ec-es-health-dedicated]

In a production environment, it’s important set up dedicated health monitoring in order to retain the logs and metrics that can be used to troubleshoot any health issues in your deployments. In the event of that you need to [contact our support team](../../../troubleshoot/index.md), they can use the retained data to help diagnose any problems that you may encounter.

You have the option of sending logs and metrics to a separate, specialized monitoring deployment, which ensures that they’re available in the event of a deployment outage. The monitoring deployment also gives you access to Kibana’s stack monitoring features, through which you can view health and performance data for all of your deployment resources.

As part of health monitoring, it’s also a best practice to [configure alerting](../../../deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md), so that you can be notified right away about any deployment health issues.

Check the guide on [how to set up monitoring](../../../deploy-manage/monitor/stack-monitoring/elastic-cloud-stack-monitoring.md) to learn more.


## Understanding deployment health [ec-health-best-practices]

We’ve compiled some guidelines to help you ensure the health of your deployments over time. These can help you to better understand the available performance metrics, and to make decisions involving performance and high availability.

[Why is my node(s) unavailable?](../../../troubleshoot/monitoring/unavailable-nodes.md)
:   Learn about common symptoms and possible actions that you can take to resolve issues when one or more nodes become unhealthy or unavailable.

[Why are my shards unavailable?](../../../troubleshoot/monitoring/unavailable-shards.md)
:   Provide instructions on how to troubleshoot issues related to unassigned shards.

[Why is performance degrading over time?](../../../troubleshoot/monitoring/performance.md)
:   Address performance degradation on a smaller size Elasticsearch cluster.

[Is my cluster really highly available?](../../../troubleshoot/monitoring/high-availability.md)
:   High availability involves more than setting multiple availability zones (although that’s really important!). Learn how to assess performance and workloads to determine if your deployment has adequate resources to mitigate a potential node failure.

[How does high memory pressure affect performance?](../../../troubleshoot/monitoring/high-memory-pressure.md)
:   Learn about typical memory usage patterns, how to assess when the deployment memory usage levels are problematic, how this impacts performance, and how to resolve memory-related issues.

[Why are my cluster response times suddenly so much worse?](../../../troubleshoot/monitoring/cluster-response-time.md)
:   Learn about the common causes of increased query response times and decreased performance in your deployment.

[Why did my node move to a different host?](../../../troubleshoot/monitoring/node-moves-outages.md)
:   Learn about why we may, from time to time, relocate your {{ech}} deployments across hosts.

