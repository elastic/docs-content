---
navigation_title: Legacy collection methods
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/monitoring-kibana.html
applies_to:
  deployment:
    self: deprecated 7.16.0
products:
  - id: kibana
---




# Legacy collection methods for self-managed {{kib}} [monitoring-kibana]


If you enable the Elastic {{monitor-features}} in your cluster, you can optionally collect metrics about {{kib}}.

::::{important}
{{agent}} and {{metricbeat}} are the recommended methods for collecting and shipping monitoring data to a monitoring cluster.

If you have previously configured legacy collection methods, you should migrate to using {{agent}} or {{metricbeat}} collection. Do not use legacy collection alongside other collection methods.

For more information, refer to [](kibana-monitoring-elastic-agent.md) and [](kibana-monitoring-metricbeat.md).

::::


The following method involves sending the metrics to the production cluster, which ultimately routes them to the monitoring cluster.

To learn about monitoring in general, refer to [](/deploy-manage/monitor/stack-monitoring.md).

1. Set the `xpack.monitoring.collection.enabled` setting to `true` on each node in the production cluster. By default, it is is disabled (`false`).

    ::::{note}
    You can specify this setting in either the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) on each node or across the cluster as a dynamic cluster setting. If {{stack-security-features}} are enabled, you must have `monitor` cluster privileges to view the cluster settings and `manage` cluster privileges to change them.
    ::::


    * To update the cluster settings in {{kib}}:

        1. Open {{kib}} in your web browser.

            By default, if you are running {{kib}} locally, go to `http://localhost:5601/`.

            If {{security-features}} are enabled, log in.

        2. Go to the **Stack Monitoring** page using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). If data collection is disabled, you are prompted to turn it on.

    * From the Console or command line, set `xpack.monitoring.collection.enabled` to `true` on the production cluster.<br>

        For example, you can use the following APIs to review and change this setting:

        ```js
        GET _cluster/settings

        PUT _cluster/settings
        {
          "persistent": {
            "xpack.monitoring.collection.enabled": true
          }
        }
        ```

        For more information, see [Monitoring settings in {{es}}](elasticsearch://reference/elasticsearch/configuration-reference/monitoring-settings.md) and [Cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings).

2. Verify that `monitoring.enabled` and `monitoring.kibana.collection.enabled` are set to `true` in the [`kibana.yml`](/deploy-manage/stack-settings.md) file. These are the default values. For more information, see [Monitoring settings in {{kib}}](kibana://reference/configuration-reference/monitoring-settings.md).
3. Identify where to send monitoring data. {{kib}} automatically sends metrics to the {{es}} cluster specified in the `elasticsearch.hosts` setting in the [`kibana.yml`](/deploy-manage/stack-settings.md) file. This property has a default value of `http://localhost:9200`.<br>

    ::::{tip}
    In production environments, we strongly recommend using a separate cluster (referred to as the *monitoring cluster*) to store the data. Using a separate monitoring cluster prevents production cluster outages from impacting your ability to access your monitoring data. It also prevents monitoring activities from impacting the performance of your production cluster.

    If {{security-features}} are enabled on the production cluster, use an HTTPS URL such as `https://<your_production_cluster>:9200` in this setting.

    ::::

4. If {{security-features}} are enabled on the production cluster:

    1. Verify that there is a valid user ID and password in the `elasticsearch.username` and `elasticsearch.password` settings in the [`kibana.yml`](/deploy-manage/stack-settings.md) file. These values are used when {{kib}} sends monitoring data to the production cluster.
    2. [Configure encryption for traffic between {{kib}} and {{es}}](/deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-kibana-http).

5. [Start {{kib}}](../../maintenance/start-stop-services/start-stop-kibana.md).
6. [View the monitoring data in {{kib}}](kibana-monitoring-data.md).

