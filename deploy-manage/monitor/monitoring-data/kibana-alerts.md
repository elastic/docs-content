---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/kibana-alerts.html
applies:
  hosted: all
  ece: all
  eck: all
  stack: all
---

% NEEDS TO BE MERGED WITH configure-stack-monitoring-alerts.md

# Kibana alerts [kibana-alerts]

The {{stack}} {monitor-features} provide [Alerting rules](../../../explore-analyze/alerts/kibana.md) out-of-the box to notify you of potential issues in the {{stack}}. These rules are preconfigured based on the best practices recommended by Elastic. However, you can tailor them to meet your specific needs.

:::{image} ../../../images/kibana-monitoring-kibana-alerting-notification.png
:alt: {{kib}} alerting notifications in {stack-monitor-app}
:class: screenshot
:::

When you open **{{stack-monitor-app}}** for the first time, you will be asked to acknowledge the creation of these default rules. They are initially configured to detect and notify on various conditions across your monitored clusters. You can view notifications for: **Cluster health**, **Resource utilization**, and **Errors and exceptions** for {{es}} in real time.

::::{note}
The default {{watcher}} based "cluster alerts" for {{stack-monitor-app}} have been recreated as rules in {{kib}} {alert-features}. For this reason, the existing {{watcher}} email action `monitoring.cluster_alerts.email_notifications.email_address` no longer works. The default action for all {{stack-monitor-app}} rules is to write to {{kib}} logs and display a notification in the UI.
::::


To review and modify existing **{{stack-monitor-app}}** rules, click **Enter setup mode** on the **Cluster overview** page. Alternatively, to manage all rules, including create and delete functionality go to **{{stack-manage-app}} > {{rules-ui}}**.


## CPU usage threshold [kibana-alerts-cpu-threshold]

This rule checks for {{es}} nodes that run a consistently high CPU load. By default, the condition is set at 85% or more averaged over the last 5 minutes. The default rule checks on a schedule time of 1 minute with a re-notify interval of 1 day.


## Disk usage threshold [kibana-alerts-disk-usage-threshold]

This rule checks for {{es}} nodes that are nearly at disk capacity. By default, the condition is set at 80% or more averaged over the last 5 minutes. The default rule checks on a schedule time of 1 minute with a re-notify interval of 1 day.


## JVM memory threshold [kibana-alerts-jvm-memory-threshold]

This rule checks for {{es}} nodes that use a high amount of JVM memory. By default, the condition is set at 85% or more averaged over the last 5 minutes. The default rule checks on a schedule time of 1 minute with a re-notify interval of 1 day.


## Missing monitoring data [kibana-alerts-missing-monitoring-data]

This rule checks for {{es}} nodes that stop sending monitoring data. By default, the condition is set to missing for 15 minutes looking back 1 day. The default rule checks on a schedule time of 1 minute with a re-notify interval of 6 hours.


## Thread pool rejections (search/write) [kibana-alerts-thread-pool-rejections]

This rule checks for {{es}} nodes that experience thread pool rejections. By default, the condition is set at 300 or more over the last 5 minutes. The default rule checks on a schedule time of 1 minute with a re-notify interval of 1 day. Thresholds can be set independently for `search` and `write` type rejections.


## CCR read exceptions [kibana-alerts-ccr-read-exceptions]

This rule checks for read exceptions on any of the replicated {{es}} clusters. The condition is met if 1 or more read exceptions are detected in the last hour. The default rule checks on a schedule time of 1 minute with a re-notify interval of 6 hours.


## Large shard size [kibana-alerts-large-shard-size]

This rule checks for a large average shard size (across associated primaries) on any of the specified data views in an {{es}} cluster. The condition is met if an index’s average shard size is 55gb or higher in the last 5 minutes. The default rule matches the pattern of `-.*` by running checks on a schedule time of 1 minute with a re-notify interval of 12 hours.


## Cluster alerting [kibana-alerts-cluster-alerts]

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



## Alerts and rules [_alerts_and_rules]


### Create default rules [_create_default_rules]

This option can be used to create default rules in this Kibana space. This is useful for scenarios when you didn’t choose to create these default rules initially or anytime later if the rules were accidentally deleted.

::::{note}
Some action types are subscription features, while others are free. For a comparison of the Elastic subscription levels, see the alerting section of the [Subscriptions page](https://www.elastic.co/subscriptions).
::::


