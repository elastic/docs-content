# How to set up monitoring [ec-monitoring-setup]

Learn how to configure your deployments for observability, which includes metric and log collection, troubleshooting views, and cluster alerts to automate performance monitoring.

These steps are helpful to set yourself up for success by making monitoring readily available and to automate alerts for the future.


## Before you begin [ec_before_you_begin_5]

As you manage, monitor, and troubleshoot your deployment, make sure you have an understanding of the [shared responsibilities](https://www.elastic.co/cloud/shared-responsibility) between Elastic and yourself, so you know what you need to do to keep your deployments running smoothly.

You may also consider subscribing to incident notices reported on the {{ecloud}} [status page](https://status.elastic.co).


## Enable logs and metrics [ec_enable_logs_and_metrics]

After you have created a new deployment, you should enable shipping logs and metrics to a monitoring deployment:

1. Go to the [Deployments](https://cloud.elastic.co/deployments) page in {{ecloud}}.
2. Find your deployment and go to the **Logs and Metrics** page.
3. Select **Enable**.
4. Choose where to send your logs and metrics.

    ::::{important}
    Anything used for production should go to a separate deployment you create only for monitoring. For development or testing, you can send monitoring data to the same deployment. Check [Enable logging and monitoring](../../../deploy-manage/monitor/stack-monitoring/elastic-cloud-stack-monitoring.md#ec-logging-and-monitoring-production).
    ::::

5. Select **Save**.

Optionally, turn on [audit logging](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/auding-settings.md) to capture security-related events, such as authentication failures, refused connections, and data-access events through the proxy. To turn on audit logging, [edit your deployment’s elasticsearch.yml file](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) to add these lines:

```sh
xpack.security.audit.enabled: true
# xpack.security.audit.logfile.events.include: _all
# xpack.security.audit.logfile.events.emit_request_body: true
```

The last two lines are commented out for now but left there as placeholders to easily turn on in the future. These two settings generate large logs, but can be helpful to turn on temporarily when troubleshooting traffic request bodies.


## View your deployment health [ec_view_your_deployment_health]

From the monitoring deployment, you can now view your deployment’s health in Kibana using [Stack Monitoring](/deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md):

1. Select the **Kibana** link for your monitoring deployment.
2. From the app menu or the search bar, open **Stack Monitoring**.

    ::::{tip}
    Stack monitoring comes with many out-of-the-box rules, but you need to enable them when prompted.
    ::::


To learn more about what [Elasticsearch monitoring metrics](/deploy-manage/monitor/monitoring-data/elasticsearch-metrics.md) are available, take a look at the different tabs. For example:

* The **Overview** tab includes information about the search and indexing performance of Elasticsearch and also provides log entries.
* The **Nodes** tab can help you monitor cluster CPU performance, JVM strain, and free disk space.

:::{image} ../../../images/cloud-ec-ce-monitoring-nodes.png
:alt: Node tab in Kibana under Stack Monitoring
:::

Some [performance metrics](../../../deploy-manage/monitor/monitoring-data/ec-saas-metrics-accessing.md) are also available directly in the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) and don’t require looking at your monitoring deployment. If you’re ever in a rush to determine if there is a performance problem, you can get a quick overview by going to the **Performance** page from your deployment menu:

:::{image} ../../../images/cloud-ec-ce-monitoring-performance.png
:alt: Performance page of the Elastic Cloud console
:::


## Check the logs [ec-check-logs]

If you suspect a performance issue, you can use your monitoring deployment to investigate what is going in Kibana:

* Through **Observability** > **Logs** > **Stream**: This page shows errors in real-time and is part of the same logs Elastic Support reviews when a deployment experiences issues. Check [Tail log files](/solutions/observability/logs/logs-stream.md).
* Through **Discover**: This page is a good option for investigating widespread historical patterns. Check [Discover](/explore-analyze/discover.md).

    Discover requires a quick setup in Kibana:

    1. Go to **Stack Management** > **Data Views** (formerly *Index Patterns*).
    2. Create a [data view](/explore-analyze/find-and-organize/data-views.md) for `elastic-cloud-logs*` and set **Timestamp field** to `@timestamp`:

        :::{image} ../../../images/cloud-ec-ce-monitoring-logs.png
        :alt: Create data view example in Kibana
        :::


Navigate to the **Discover** or **Stream** pages to check if you’ve misconfigured your SAML authentication setup by filtering for `WARN` and `ERROR` level logs and viewing the specific `message` fields, for example:

:::{image} ../../../images/cloud-ec-ce-monitoring-saml.png
:alt: Log error in Stream page showing failed SAML authentication
:::

You can also use this page to test how problematic proxy traffic requests show up in audit logs. To illustrate, create a spurious test request from the [Elasticsearch API console](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/ec-api-console.md):

:::{image} ../../../images/cloud-ec-ce-monitoring-api-console.png
:alt: Elasticsearch API console showing a spurious request that fails
:::

You will get this request reported as a new log. Audit logs do not currently report the HTTP response status code, but they do report a correlating `event.action` column:

:::{image} ../../../images/cloud-ec-ce-monitoring-new-log.png
:alt: New log entry that shows failed spurious request issued from the API console
:::


## Get notified [ec_get_notified]

You should take advantage of the default [Elastic Stack monitoring alerts](/deploy-manage/monitor/monitoring-data/kibana-alerts.md) that are available out-of-the-box. You don’t have to do anything other than enable shipping logs and metrics to have them made available to you (which you did earlier on).

On top of these default alerts that write to indices you can investigate, you might want to add some custom actions, such as a [connector](asciidocalypse://docs/kibana/docs/reference/connectors-kibana.md) for Slack notifications. To set up these notifications, you first configure a Slack connector and then append it to the default alerts and actions. From Kibana:

1. Go to **Stack Management** > **Rules and Connectors** > **Connectors** and create your Slack connector:

    1. Select **Slack**.
    2. [Create a Slack Webhook URL](asciidocalypse://docs/kibana/docs/reference/connectors-kibana/slack-action-type.md#configuring-slack) and paste it into the **Webhook URL** field.
    3. Select **Save**.

2. Go to **Stack Monitoring** and select **Enter setup mode**.
3. Edit an alert rule, such as [CPU usage](/deploy-manage/monitor/monitoring-data/kibana-alerts.md#kibana-alerts-cpu-threshold):

    1. Select one of the alert rule fields and select **CPU Usage**.
    2. Choose **Edit rule** and scroll down to the bottom of the screen to select **Slack**.
    3. Optional: Set up a customized message that helps you identify what the message is for.
    4. Select **Save**.

    :::{image} ../../../images/cloud-ec-ce-monitoring-connector-action.png
    :alt: Alert rule example showing settings to send a Slack notification based on CPU Usage
    :::


Now, when your CPU usage alert goes off, you will also get a Slack notification to investigate if your cluster is experiencing a traffic blip or if you need to scale out. (You can automate the latter with [deployment autoscaling](../../../deploy-manage/autoscaling.md)).


## Keep monitoring [ec_keep_monitoring]

As a managed service, {{ecloud}} is here to help you manage the maintenance and upkeep. As part of your responsibilities, you should monitor deployment health on an ongoing basis. There are two main activities to perform:

* Review the deployment logs
* Act on automated alerts

When issues come up that you need to troubleshoot, you’ll frequently start with the same queries to determine which rabbit hole to investigate further, such as [`_cluster/health`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health) to determine overall deployment health.

:::{image} ../../../images/cloud-ec-ce-monitoring-ongoing.png
:alt: Elasticsearch API console showing queries useful for monitoring
:::

You can run this query and many others from the API consoles available via:

* **Kibana** > **Dev Tools**. Check [Run Elasticsearch API requests](/explore-analyze/query-filter/tools/console.md).
* **Elastic Cloud** > **Deployment** > **Elasticsearch** > **API Console**. Check [Access the Elasticsearch API console](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/ec-api-console.md).

You can also learn more about the queries you should run for your deployment by reading our blog [Managing and Troubleshooting Elasticsearch Memory](https://www.elastic.co/blog/managing-and-troubleshooting-elasticsearch-memory).

