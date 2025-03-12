---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-cluster-health-notifications.html
applies_to:
  deployment:
    ess: all
---

% NEEDS MERGING WITH kibana-alerts.md
% this one is written for Elastic Cloud but needs to be generic, except if it's really about Elastic cloud.

# Configure Stack monitoring alerts [ec-cluster-health-notifications]

You can configure Stack monitoring alerts to be sent to you by email when health related events occur in your deployments. To set up email notifications:

1. [Enable logging and monitoring](../stack-monitoring/elastic-cloud-stack-monitoring.md) on deployments for which you want to receive notifications. You need to enable only metrics data being shipped for the notifications to work.
2. In Kibana, configure the email connector to [send email from Elastic Cloud](kibana://reference/connectors-kibana/email-action-type.md#elasticcloud). If you want to use the preconfigured `Elastic-Cloud-SMTP` connector in Elastic Cloud, then you can skip this step.
3. From the Kibana main menu, go to **Stack Monitoring**. On this page you can find a summary of monitoring metrics for your deployment as well as any alerts.
4. Select **Enter setup mode**.
5. On any card showing available alerts, select the **alerts** indicator. Use the menu to select the type of alert for which you’d like to be notified. There are many alert types, including:

    * CPU usage threshold
    * Disk usage threshold
    * JVM memory threshold
    * Missing monitoring data
    * Thread pool rejections (search/write)
    * CCR read exceptions
    * Large shard size
    * Cluster alerting, including:

        * Elasticsearch cluster health status
        * Elasticsearch, Kibana, or Logstash version mismatches
        * Elasticsearch nodes changed

        All of these alerts are described in detail in [Kibana alerts](kibana-alerts.md). Check the documentation matching your Kibana version to find which alerts are available in that release.


    ::::{note}
    For the `Elasticsearch nodes changed` alert, if you have only one master node in your cluster, during the master node vacate no notification will be sent. Kibana needs to communicate with the master node in order to send a notification. One way to avoid this is by shipping your deployment metrics to a dedicated monitoring cluster, which you can configure when you enable logging and monitoring in Step 2.

    ::::

6. In the **Edit rule** pane, set how often to check for the condition and how often to send notifications.
7. In the **Actions** section, select **Email** as a connector type and select the email connector that you configured in Step 3 (or the preconfigured `Elastic-Cloud-SMTP` connector).
8. Configure the email contents and select **Save**. Make sure that the email address you specify is the one that you allowed in Step 1.
