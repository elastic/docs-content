---
navigation_title: Enable on ECH and ECE
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-enable-logging-and-monitoring.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-restrictions-monitoring.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-monitoring.html
  - https://www.elastic.co/guide/en/cloud/current/ec-monitoring-setup.html
  - https://www.elastic.co/guide/en/cloud/current/ec-enable-logging-and-monitoring.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-enable-logging-and-monitoring.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-monitoring-setup.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-restrictions-monitoring.html
applies_to:
  deployment:
    ece: all
    ess: all
products:
  - id: cloud-enterprise
  - id: cloud-hosted
---

# Enable stack monitoring on ECH and ECE deployments

The deployment logging and monitoring feature lets you monitor your deployment in {{kib}} by shipping logs and metrics to a monitoring deployment. You can:

* View your deployment’s health and performance in real time and analyze past cluster, index, and node metrics.
* View your deployment’s logs to debug issues, discover slow queries, surface deprecations, and analyze access to your deployment.

Monitoring consists of two components:

* A monitoring and logging agent that is installed on each node in your deployment. The agents collect and index metrics to {{es}}, either on the same deployment or by sending logs and metrics to an external monitoring deployment. Elastic manages the installation and configuration of the monitoring agent for you, and you should not modify any of the settings.
* The stack monitoring application in {{kib}} that visualizes the monitoring metrics through a dashboard, and the logs application that allows you to search and analyze deployment logs.

With logging and monitoring enabled for a deployment, metrics are collected for {{es}}, {{kib}}, and APM with Fleet Server.

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::

## Before you begin [logging-and-monitoring-limitations]

* Some limitations apply when you use monitoring on ECH or ECE. To learn more, check the monitoring [restrictions and limitations](#restrictions-monitoring).
* Enabling logs and monitoring requires additional resources. For production systems where these features are enabled, we recommend allocating at least 4 GB of RAM per {{es}} instance. Review [Minimum size recommendations for production use](../../deploy/elastic-cloud/elastic-cloud-hosted-planning.md#ec-minimum-recommendations) for more details.

## Monitoring for production use [logging-and-monitoring-production]

For production use, you should send your deployment logs and metrics to a dedicated monitoring deployment. Monitoring indexes logs and metrics into {{es}} and these indexes consume storage, memory, and CPU cycles like any other index. By using a separate monitoring deployment, you avoid affecting your other production deployments and can view the logs and metrics even when a production deployment is unavailable.

How many monitoring deployments you use depends on your requirements:

* You can ship logs and metrics for many deployments to a single monitoring deployment, if your business requirements permit it.
* Although monitoring will work with a deployment running a single node, you need a minimum of three monitoring nodes to make monitoring highly available.
* You might need to create dedicated monitoring deployments for isolation purposes in some cases. For example:

    * If you have many deployments and some of them are much larger than others, creating separate monitoring deployments prevents a large deployment from potentially affecting monitoring performance for smaller deployments.
    * If you need to silo {{es}} data for different business departments. Deployments that have been configured to ship logs and metrics to a target monitoring deployment have access to indexing data and can manage monitoring index templates, which is addressed by creating separate monitoring deployments.

Logs and metrics that get sent to a dedicated monitoring {{es}} deployment [may not be cleaned up automatically](#logging-and-monitoring-retention) and might require some additional steps to remove excess data periodically.

## Retention of logging and monitoring indices [logging-and-monitoring-retention]

When sending monitoring and logging data to a deployment, an ILM policy is pre-configured to control data retention. To view or edit the policies, Go to the **Index Lifecycle Policies** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

For monitoring indices, the retention period is configured in the `.monitoring-8-ilm-policy` index lifecycle policy.

## Enable logging and monitoring [enable-logging-and-monitoring-steps]

Elastic manages the installation and configuration of the monitoring agent for you. When you enable monitoring on a deployment, you are configuring where the monitoring agent for your current deployment should send its logs and metrics.

**Before you start**

- Enabling logging and monitoring increases the resource consumption of the deployment. For production systems, we recommend sizing deployments with logging and monitoring enabled to at least 4 GB of RAM on each {{es}} instance.
- Enabling logging and monitoring can trigger a plan change on your deployment. You can monitor the plan change progress from the deployment's **Activity** page.

:::{tip}
The monitoring deployment and production deployment must be on the same major version, cloud provider, and region.
:::

To enable monitoring on your deployment:

:::{include} /deploy-manage/_snippets/find-manage-deployment-ech-and-ece.md
:::

3. Under the deployment's name in the navigation menu, select **Logs and metrics**.
4. Under **Ship to a deployment**, select **Enable**.
5. Choose where to send your logs and metrics. Select **Save**.

    If a deployment is not listed, make sure that it is running a compatible version. The monitoring deployment and production deployment must be on the same major version, cloud provider, and region.

    ::::{tip}
    Remember to send logs and metrics for production deployments to a dedicated monitoring deployment, so that your production deployments are not impacted by the overhead of indexing and storing monitoring data. A dedicated monitoring deployment also gives you more control over the retention period for monitoring data.
    ::::

## Access the monitoring application in {{kib}} [access-kibana-monitoring]

With monitoring enabled for your deployment, you can access the [logs](//solutions/observability.md) and [stack monitoring](../monitoring-data/visualizing-monitoring-data.md) through {{kib}}.

:::{include} /deploy-manage/monitor/stack-monitoring/_snippets/cloud-monitoring-access.md
:::

You can also create an `elastic-cloud-logs-*` data view (formerly *index pattern*) to view your deployment’s logs in the {{kib}} **Discover** tab.

Several fields are available for you to view logs based on key details, such as the source deployment:

| Field | Description | Example value |
| --- | --- | --- |
| `service.id` | The ID of the deployment that generated the log | `6ff525333d2844539663f3b1da6c04b6` |
| `service.name` | The name of the deployment that generated the log | `My Production Deployment` |
| `cloud.availability_zone` | The availability zone in which the instance that generated the log is deployed | `ap-northeast-1d` |
| `service.node.name` | The ID of the instance that generated the log | `instance-0000000008` |
| `service.type` | The type of instance that generated the log | `elasticsearch` |
| `service.version` | The version of the stack resource that generated the log | `9.0.0` |

## Logging features [extra-logging-features]

When shipping logs to a monitoring deployment there are more logging features available to you. These features include:


### For {{es}} [extra-logging-features-elasticsearch]

* [Audit logging](/deploy-manage/security/logging-configuration/enabling-audit-logs.md) - logs security-related events on your deployment
* [Slow query and index logging](/deploy-manage/monitor/logging-configuration/slow-logs.md) - helps find and debug slow queries and indexing
* Verbose logging - helps debug stack issues by increasing component logs

After you’ve enabled log delivery on your deployment, you can [add the {{es}} user settings](/deploy-manage/deploy/cloud-enterprise/edit-stack-settings.md) to enable these features.


### For {{kib}} [extra-logging-features-kibana]

* [Audit logging](/deploy-manage/security/logging-configuration/enabling-audit-logs.md) - logs security-related events on your deployment

After you’ve enabled log delivery on your deployment, you can [add the {{kib}} user settings](/deploy-manage/deploy/cloud-enterprise/edit-stack-settings.md) to enable this feature.


### Other components [extra-logging-features-enterprise-search]

Enabling log collection also supports collecting and indexing the following types of logs from other components in your deployments:

**APM**

* `apm*.log*`

**Fleet and Elastic Agent**

* `fleet-server-json.log-*`
* `elastic-agent-json.log-*`

The `*` indicates that we also index the archived files of each type of log.

Check the respective product documentation for more information about the logging capabilities of each product.

## Restrictions and limitations [restrictions-monitoring]
* The monitoring deployment and production deployment must be on the same major version, cloud provider, and region.
* To avoid compatibility issues, ensure your monitoring cluster and production cluster run on the same {{stack}} version. Monitoring clusters that use 9.x do work with production clusters that use the latest release of 8.x, but this setup should only occur when upgrading clusters to the same version.
* $$$cross-region-monitor$$$ Monitoring across regions is not supported. If you need to move your existing monitoring to the same region, you can do a reindex or create a new deployment and select the snapshot from the old deployment.
* The logs shipped to a monitoring cluster use an ILM managed data stream (`elastic-cloud-logs-<version>`). If you need to delete indices due to space, do not delete the current `is_write_enabled: true` index.
* When sending metrics to a dedicated monitoring deployment, the graph for IO Operations Rate(/s) is blank. This is due to the fact that this graph actually contains metrics from of all of the virtualized resources from the provider.
