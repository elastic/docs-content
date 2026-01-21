---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-cluster-health-notifications.html
  - https://www.elastic.co/guide/en/kibana/current/kibana-alerts.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
products:
  - id: cloud-hosted
  - id: kibana
---

# Stack monitoring alerts [kibana-alerts]

The {{stack}} {{monitor-features}} provide [Alerting rules](../../../explore-analyze/alerts-cases/alerts.md) out-of-the box to notify you of potential issues in the {{stack}}. These rules are preconfigured based on the best practices recommended by Elastic. However, you can tailor them to meet your specific needs.

:::{image} /deploy-manage/images/kibana-monitoring-kibana-alerting-notification.png
:alt: {{kib}} alerting notifications in {{stack-monitor-app}}
:screenshot:
:::

::::{note}
The default {{watcher}} based "cluster alerts" for {{stack-monitor-app}} have been recreated as rules in {{kib}} {{alert-features}}. For this reason, the existing {{watcher}} email action `monitoring.cluster_alerts.email_notifications.email_address` no longer works. The default action for all {{stack-monitor-app}} rules is to write to {{kib}} logs and display a notification in the UI.
::::

## Create default rules [_create_default_rules]

When you open **{{stack-monitor-app}}** for the first time, you will be asked to allow {{kib}} to create the default set of rules. They are initially configured to detect and notify on various conditions across your monitored clusters. You can view notifications for **Cluster health**, **Resource utilization**, and **Errors and exceptions** for {{es}} in real time.

If you denied creation of the default rules initially, or to recreate any deleted rules, then you can trigger {{kib}} to create the rules by going to **Alerts and rules** > **Create default rules**.

To receive external notifications for these alerts, you need to [configure a connector](/deploy-manage/manage-connectors.md) and modify the relevant rule to use the connector. If you're using {{ech}}, then you can use the default `Elastic-Cloud-SMTP` email connector or configure your own.

::::{note}
Some action types are subscription features, while others are free. For a comparison of the Elastic subscription levels, see the alerting section of the [Subscriptions page](https://www.elastic.co/subscriptions).
::::

## Modify rules

To review and modify existing **{{stack-monitor-app}}** rules, click **Enter setup mode** on the **Cluster overview** page. Cards with alerts configured are annotated with an indicator.

:::{tip}
Alternatively, to manage all rules, including create and delete functionality, find the **{{rules-ui}}** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
:::

1. On any card showing available alerts, select the **alerts** indicator. Use the menu to select the type of alert for which you’d like to be notified.
2. In the **Edit rule** pane, set how often to check for the condition and how often to send notifications.
3. In the **Actions** section, select the connector that you'd like to use for notifications.
4. Configure the connector message contents and select **Save**.

## Default rules

The following rules are [preconfigured](#_create_default_rules) for stack monitoring.

:::{dropdown} CPU usage threshold

$$$kibana-alerts-cpu-threshold$$$

This rule checks for {{es}} nodes that run a consistently high CPU load.

By default, the condition is set at 85% or more averaged over the last 5 minutes. The default rule checks on a schedule time of 1 minute with a re-notify interval of 1 day.
:::

:::{dropdown} Disk usage threshold

$$$kibana-alerts-disk-usage-threshold$$$

This rule checks for {{es}} nodes that are nearly at disk capacity.

By default, the condition is set at 80% or more averaged over the last 5 minutes. The default rule checks on a schedule time of 1 minute with a re-notify interval of 1 day.
:::

:::{dropdown} JVM memory threshold

$$$kibana-alerts-jvm-memory-threshold$$$

This rule checks for {{es}} nodes that use a high amount of JVM memory.

By default, the condition is set at 85% or more averaged over the last 5 minutes. The default rule checks on a schedule time of 1 minute with a re-notify interval of 1 day.
:::

:::{dropdown} Missing monitoring data

$$$kibana-alerts-missing-monitoring-data$$$

This rule checks for {{es}} nodes that stop sending monitoring data.

By default, the condition is set to missing for 15 minutes looking back 1 day. The default rule checks on a schedule time of 1 minute with a re-notify interval of 6 hours.
:::

:::{dropdown} Thread pool rejections (search/write)

$$$kibana-alerts-thread-pool-rejections$$$

This rule checks for {{es}} nodes that experience thread pool rejections.

By default, the condition is set at 300 or more over the last 5 minutes. The default rule checks on a schedule time of 1 minute with a re-notify interval of 1 day. Thresholds can be set independently for `search` and `write` type rejections.
:::

:::{dropdown} CCR read exceptions

$$$kibana-alerts-ccr-read-exceptions$$$

This rule checks for read exceptions on any of the replicated {{es}} clusters.

The condition is met if 1 or more read exceptions are detected in the last hour. The default rule checks on a schedule time of 1 minute with a re-notify interval of 6 hours.
:::

:::{dropdown} Large shard size

$$$kibana-alerts-large-shard-size$$$

This rule checks for a large average shard size (across associated primaries) on any of the specified data views in an {{es}} cluster.

The condition is met if an index’s average shard size is 55gb or higher in the last 5 minutes. The default rule matches the pattern of `-.*` by running checks on a schedule time of 1 minute with a re-notify interval of 12 hours.
:::

::::{dropdown} Cluster alerting

$$$kibana-alerts-cluster-alerts$$$

These rules check the current status of your {{stack}}. You can drill down into the metrics to view more information about your cluster and specific nodes, instances, and indices.

An action is triggered if any of the following conditions are met within the last minute:

* {{es}} cluster health status is yellow (missing at least one replica) or red (missing at least one primary).
* {{es}} version mismatch. You have {{es}} nodes with different versions in the same cluster.
* {{kib}} version mismatch. You have {{kib}} instances with different versions running against the same {{es}} cluster.
* Logstash version mismatch. You have Logstash nodes with different versions reporting stats to the same monitoring cluster.
* {{es}} nodes changed. You have {{es}} nodes that were recently added or removed.
* {{es}} license expiration. The cluster’s license is about to expire.

    If you do not preserve the data directory when upgrading a {{kib}} or Logstash node, the instance is assigned a new persistent UUID and shows up as a new instance.

* Subscription license expiration. When the expiration date approaches, you will get notifications with a severity level relative to how soon the expiration date is:

    * 60 days: Informational alert
    * 30 days: Low-level alert
    * 15 days: Medium-level alert
    * 7 days: Severe-level alert

  The 60-day and 30-day thresholds are skipped for Trial licenses, which are only valid for 30 days.

:::{note}
For the `Elasticsearch nodes changed` alert, if you have only one master node in your cluster, during the master node vacate no notification will be sent. {{kib}} needs to communicate with the master node in order to send a notification. One way to avoid this is by shipping your deployment metrics to a dedicated monitoring cluster.
:::
::::