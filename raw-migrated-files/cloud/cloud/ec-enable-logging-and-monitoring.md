# Enable logging and monitoring [ec-enable-logging-and-monitoring]

The deployment logging and monitoring feature lets you monitor your deployment in [Kibana](../../../get-started/the-stack.md) by shipping logs and metrics to a monitoring deployment. You can:

* View your deployment’s health and performance in real time and analyze past cluster, index, and node metrics.
* View your deployment’s logs to debug issues, discover slow queries, surface deprecations, and analyze access to your deployment.

Monitoring consists of two components:

* A monitoring and logging agent that is installed on each node in your deployment. The agents collect and index metrics to {{es}}, either on the same deployment or by sending logs and metrics to an external monitoring deployment. {{ech}} manages the installation and configuration of the monitoring agent for you, and you should not modify any of the settings.
* The stack monitoring application in Kibana that visualizes the monitoring metrics through a dashboard and the logs application that allows you to search and analyze deployment logs.

The steps in this section cover only the enablement of the monitoring and logging features in {{ech}}. For more information on how to use the monitoring features, refer to [Monitor a cluster](../../../deploy-manage/monitor.md).


### Before you begin [ec-logging-and-monitoring-limitations] 

Some limitations apply when you use monitoring on {{ech}}. To learn more, check the monitoring [restrictions and limitations](../../../deploy-manage/monitor/stack-monitoring/elastic-cloud-stack-monitoring.md#ec-restrictions-monitoring).


### Monitoring for production use [ec-logging-and-monitoring-production] 

For production use, you should send your deployment logs and metrics to a dedicated monitoring deployment. Monitoring indexes logs and metrics into {{es}} and these indexes consume storage, memory, and CPU cycles like any other index. By using a separate monitoring deployment, you avoid affecting your other production deployments and can view the logs and metrics even when a production deployment is unavailable.

How many monitoring deployments you use depends on your requirements:

* You can ship logs and metrics for many deployments to a single monitoring deployment, if your business requirements permit it.
* Although monitoring will work with a deployment running a single node, you need a minimum of three monitoring nodes to make monitoring highly available.
* You might need to create dedicated monitoring deployments for isolation purposes in some cases. For example:

    * If you have many deployments and some of them are much larger than others, creating separate monitoring deployments prevents a large deployment from potentially affecting monitoring performance for smaller deployments.
    * If you need to silo {{es}} data for different business departments. Deployments that have been configured to ship logs and metrics to a target monitoring deployment have access to indexing data and can manage monitoring index templates, which is addressed by creating separate monitoring deployments.


Logs and metrics that get sent to a dedicated monitoring {{es}} deployment [may not be cleaned up automatically](../../../deploy-manage/monitor/stack-monitoring/elastic-cloud-stack-monitoring.md#ec-logging-and-monitoring-retention) and might require some additional steps to remove excess data periodically.


### Retention of monitoring daily indices [ec-logging-and-monitoring-retention] 


#### Stack versions 8.0 and above [ec-logging-and-monitoring-retention-8] 

When you enable monitoring in {{ech}}, your monitoring indices are retained for a certain period by default. After the retention period has passed, the monitoring indices are deleted automatically. The retention period is configured in the `.monitoring-8-ilm-policy` index lifecycle policy. To view or edit the policy open {{kib}} **Stack management > Data > Index Lifecycle Policies**.


### Sending monitoring data to itself (self monitoring) [ec-logging-and-monitoring-retention-self-monitoring] 

$$$ec-logging-and-monitoring-retention-7$$$
When you enable self-monitoring in {{ech}}, your monitoring indices are retained for a certain period by default. After the retention period has passed, the monitoring indices are deleted automatically. Monitoring data is retained for three days by default or as specified by the [`xpack.monitoring.history.duration` user setting](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md#xpack-monitoring-history-duration).

To retain monitoring indices as is without deleting them automatically, you must disable the [cleaner service](../../../deploy-manage/monitor/stack-monitoring/es-local-exporter.md#local-exporter-cleaner) by adding a disabled local exporter in your cluster settings.

For example

```sh
PUT /_cluster/settings
{
    "persistent": {
        "xpack.monitoring.exporters.__no-default-local__": {
            "type": "local",
            "enabled": false
        }
    }
}
```


### Sending monitoring data to a dedicated monitoring deployment [ec-logging-and-monitoring-retention-dedicated-monitoring] 

When [monitoring for production use](../../../deploy-manage/monitor/stack-monitoring/elastic-cloud-stack-monitoring.md#ec-logging-and-monitoring-production), where you configure your deployments **to send monitoring data to a dedicated monitoring deployment** for indexing, this retention period does not apply. Monitoring indices on a dedicated monitoring deployment are retained until you remove them. There are three options open to you:

* To enable the automatic deletion of monitoring indices from dedicated monitoring deployments, [enable monitoring](../../../deploy-manage/monitor/stack-monitoring/elastic-cloud-stack-monitoring.md#ec-enable-logging-and-monitoring-steps) on your dedicated monitoring deployment in {{ech}} to send monitoring data to itself. When an {{es}} deployment sends monitoring data to itself, all monitoring indices are deleted automatically after the retention period, regardless of the origin of the monitoring data.
* Alternatively, you can enable the cleaner service on the monitoring deployment by creating a local exporter. You can define the retention period at the same time.

    For example

    ```sh
    PUT _cluster/settings
    {
      "persistent": {
        "xpack" : {
          "monitoring" : {
            "exporters" : {
              "found-user-defined" : {
                "type" : "local",
                "enabled" : "true"
              }
            },
            "history" : {
              "duration" : "24h"
            }
          }
        }
      }
    }
    ```

* To retain monitoring indices on a dedicated monitoring deployment as is without deleting them automatically, no additional steps are required other than making sure that you do not enable the monitoring deployment to send monitoring data to itself. You should also monitor the deployment for disk space usage and upgrade your deployment periodically, if necessary.


### Retention of logging indices [ec-logging-and-monitoring-log-retention] 

An ILM policy is pre-configured to manage log retention. The policy can be adjusted according to your requirements.


### Index management [ec-logging-and-monitoring-index-management-ilm] 

When sending monitoring data to a deployment, you can configure [Index Lifecycle Management (ILM)](../../../manage-data/lifecycle/index-lifecycle-management.md) to manage retention of your monitoring and logging indices. When sending logs to a deployment, an ILM policy is pre-configured to manage log retention and the policy can be customized to your needs.


### Enable logging and monitoring [ec-enable-logging-and-monitoring-steps] 

{{ech}} manages the installation and configuration of the monitoring agent for you. When you enable monitoring on a deployment, you are configuring where the monitoring agent for your current deployment should send its logs and metrics.

To enable monitoring on your deployment:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From your deployment menu, go to the **Logs and metrics** page.
4. Select **Enable**.
5. Choose where to send your logs and metrics. Select **Save**.

    If a deployment is not listed, make sure that it is running a compatible version. The monitoring deployment and production deployment must be on the same major version, cloud provider, and region.

    ::::{tip} 
    Remember to send logs and metrics for production deployments to a dedicated monitoring deployment, so that your production deployments are not impacted by the overhead of indexing and storing monitoring data. A dedicated monitoring deployment also gives you more control over the retention period for monitoring data.
    ::::


::::{note} 
Enabling logs and monitoring may trigger a plan change on your deployment. You can monitor the plan change progress from the deployment’s **Activity** page.
::::


::::{note} 
Enabling logs and monitoring requires some extra resource on a deployment. For production systems, we recommend sizing deployments with logs and monitoring enabled to at least 4 GB of RAM.
::::



### Access the monitoring application in Kibana [ec-access-kibana-monitoring] 

With monitoring enabled for your deployment, you can access the [logs](https://www.elastic.co/guide/en/kibana/current/observability.html) and [stack monitoring](../../../deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md) through Kibana.

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From your deployment menu, go to the **Logs and Metrics** page.
4. Select the corresponding **View** button to check the logs or metrics data.

Alternatively, you can access logs and metrics directly on the Kibana **Logs** and **Stack Monitoring** pages in the target monitoring deployment. You can also create an `elastic-cloud-logs-*` data view (formerly *index pattern*) to view your deployment’s logs in the Kibana **Discover** tab. Several fields are available for you to view logs based on key details, such as the source deployment:

| Field | Description | Example value |
| --- | --- | --- |
| `service.id` | The ID of the deployment that generated the log | `6ff525333d2844539663f3b1da6c04b6` |
| `service.name` | The name of the deployment that generated the log | `My Production Deployment` |
| `cloud.availability_zone` | The availability zone in which the instance that generated the log is deployed | `ap-northeast-1d` |
| `service.node.name` | The ID of the instance that generated the log | `instance-0000000008` |
| `service.type` | The type of instance that generated the log | `elasticsearch` |
| `service.version` | The version of the stack resource that generated the log | `8.13.1` |


### Logging features [ec-extra-logging-features] 

When shipping logs to a monitoring deployment there are more logging features available to you. These features include:


#### For {{es}}: [ec-extra-logging-features-elasticsearch] 

* [Audit logging](../../../deploy-manage/monitor/logging-configuration/enabling-audit-logs.md) - logs security-related events on your deployment
* [Slow query and index logging](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/slow-log.md) - helps find and debug slow queries and indexing
* Verbose logging - helps debug stack issues by increasing component logs

After you’ve enabled log delivery on your deployment, you can [add the Elasticsearch user settings](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) to enable these features.


#### For Kibana: [ec-extra-logging-features-kibana] 

* [Audit logging](../../../deploy-manage/monitor/logging-configuration/enabling-audit-logs.md) - logs security-related events on your deployment

After you’ve enabled log delivery on your deployment, you can [add the Kibana user settings](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) to enable this feature.


### Other components [ec-extra-logging-features-enterprise-search] 

Enabling log collection also supports collecting and indexing the following types of logs from other components in your deployments:

**APM**

* apm*.log*

**Fleet and Elastic Agent**

* fleet-server-json.log-*
* elastic-agent-json.log-*

The ˆ*ˆ indicates that we also index the archived files of each type of log.

Check the respective product documentation for more information about the logging capabilities of each product.


## Metrics features [ec-extra-metrics-features] 

With logging and monitoring enabled for a deployment, metrics are collected for Elasticsearch, Kibana, and APM with Fleet Server.


#### Enabling Elasticsearch/Kibana audit logs on your deployment [ec-enable-audit-logs] 
% Added by eedugon to audit logging in deploy and manage -> monitoring -> logging section

Audit logs are useful for tracking security events on your {{es}} and/or {{kib}} clusters. To enable {{es}} audit logs on your deployment:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From your deployment menu, go to the **Edit** page.
4. To enable audit logs in {{es}}, in the **Elasticsearch** section select **Manage user settings and extensions**. For deployments with existing user settings, you may have to expand the **Edit elasticsearch.yml** caret for each node instead.
5. To enable audit logs in {{kib}}, in the **Kibana** section select **Edit user settings**. For deployments with existing user settings, you may have to expand the **Edit kibana.yml** caret instead.
6. Add `xpack.security.audit.enabled: true` to the user settings.
7. Select **Save changes**.

A plan change will run on your deployment. When it finishes, audit logs will be delivered to your monitoring deployment.

## Restrictions and limitations [ec-restrictions-monitoring]

* To avoid compatibility issues, ensure your monitoring cluster and production cluster run on the same {{stack}} version. Monitoring clusters that use 8.x do work with production clusters that use the latest release of 7.x, but this setup should only occur when upgrading clusters to the same version.
* $$$cross-region-monitor$$$ Monitoring across regions is not supported. If you need to move your existing monitoring to the same region, you can do a reindex or create a new deployment and select the snapshot from the old deployment.
* The logs shipped to a monitoring cluster use an ILM managed data stream (elastic-cloud-logs-<version>). If you need to delete indices due to space, do not delete the current is_write_enabled: true index.
* When sending metrics to a dedicated monitoring deployment, the graph for IO Operations Rate(/s) is blank. This is due to the fact that this graph actually contains metrics from of all of the virtualized resources from the provider.


