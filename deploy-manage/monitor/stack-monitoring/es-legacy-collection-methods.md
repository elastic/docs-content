---
navigation_title: "Legacy collection methods"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/collecting-monitoring-data.html
applies_to:
  deployment:
    self: deprecated 7.16.0
---




# Legacy collection methods [collecting-monitoring-data]


::::{admonition} Deprecated in 7.16.
:class: warning

Using the {{es}} Monitoring plugin to collect and ship monitoring data is deprecated. {{agent}} and {{metricbeat}} are the recommended methods for collecting and shipping monitoring data to a monitoring cluster. If you previously configured legacy collection methods, you should migrate to using [{{agent}}](collecting-monitoring-data-with-elastic-agent.md) or [{{metricbeat}}](collecting-monitoring-data-with-metricbeat.md) collection methods.
::::


This method for collecting metrics about {{es}} involves sending the metrics to the monitoring cluster by using exporters.

Advanced monitoring settings enable you to control how frequently data is collected, configure timeouts, and set the retention period for locally-stored monitoring indices. You can also adjust how monitoring data is displayed.

To learn about monitoring in general, see [Monitor a cluster](../../monitor.md).

1. Configure your cluster to collect monitoring data:

    1. Verify that the `xpack.monitoring.elasticsearch.collection.enabled` setting is `true`, which is its default value, on each node in the cluster.

        ::::{note}
        You can specify this setting in either the `elasticsearch.yml` on each node or across the cluster as a dynamic cluster setting. If {{es}} {{security-features}} are enabled, you must have `monitor` cluster privileges to view the cluster settings and `manage` cluster privileges to change them.
        ::::


        For more information, see [Monitoring settings](elasticsearch://reference/elasticsearch/configuration-reference/monitoring-settings.md) and [Cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings).

    2. Set the `xpack.monitoring.collection.enabled` setting to `true` on each node in the cluster. By default, it is disabled (`false`).

        ::::{note}
        You can specify this setting in either the `elasticsearch.yml` on each node or across the cluster as a dynamic cluster setting. If {{es}} {{security-features}} are enabled, you must have `monitor` cluster privileges to view the cluster settings and `manage` cluster privileges to change them.
        ::::


        For example, use the following APIs to review and change this setting:

        ```console
        GET _cluster/settings
        ```
        %  TEST[warning:[xpack.monitoring.collection.enabled] setting was deprecated in Elasticsearch and will be removed in a future release.]

        ```console
        PUT _cluster/settings
        {
          "persistent": {
            "xpack.monitoring.collection.enabled": true
          }
        }
        ```

        Alternatively, you can enable this setting in {{kib}}. In the side navigation, click **Monitoring**. If data collection is disabled, you are prompted to turn it on.

        For more information, see [Monitoring settings](elasticsearch://reference/elasticsearch/configuration-reference/monitoring-settings.md) and [Cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings).

    3. Optional: Specify which indices you want to monitor.

        By default, the monitoring agent collects data from all {{es}} indices. To collect data from particular indices, configure the `xpack.monitoring.collection.indices` setting. You can specify multiple indices as a comma-separated list or use an index pattern to match multiple indices. For example:

        ```yaml
        xpack.monitoring.collection.indices: logstash-*, index1, test2
        ```

        You can prepend `-` to explicitly exclude index names or patterns. For example, to include all indices that start with `test` except `test3`, you could specify `test*,-test3`. To include system indices such as .security and .kibana, add `.*` to the list of included names. For example `.*,test*,-test3`

    4. Optional: Specify how often to collect monitoring data. The default value for the `xpack.monitoring.collection.interval` setting 10 seconds. See [Monitoring settings](elasticsearch://reference/elasticsearch/configuration-reference/monitoring-settings.md).

2. Identify where to store monitoring data.

    By default, the data is stored on the same cluster by using a [`local` exporter](es-local-exporter.md). Alternatively, you can use an [`http` exporter](es-http-exporter.md) to send data to a separate *monitoring cluster*.

    ::::{important}
    The {{es}} {{monitor-features}} use ingest pipelines, therefore the cluster that stores the monitoring data must have at least one [ingest node](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md).
    ::::


    For more information about typical monitoring architectures, see [How it works](../stack-monitoring.md).

3. If you choose to use an `http` exporter:

    1. On the cluster that you want to monitor (often called the *production cluster*), configure each node to send metrics to your monitoring cluster. Configure an HTTP exporter in the `xpack.monitoring.exporters` settings in the `elasticsearch.yml` file. For example:

        ```yaml
        xpack.monitoring.exporters:
          id1:
            type: http
            host: ["http://es-mon-1:9200", "http://es-mon-2:9200"]
        ```

    2. If the Elastic {{security-features}} are enabled on the monitoring cluster, you must provide appropriate credentials when data is shipped to the monitoring cluster:

        1. Create a user on the monitoring cluster that has the [`remote_monitoring_agent` built-in role](../../users-roles/cluster-or-deployment-auth/built-in-roles.md). Alternatively, use the [`remote_monitoring_user` built-in user](../../users-roles/cluster-or-deployment-auth/built-in-users.md).
        2. Add the user ID and password settings to the HTTP exporter settings in the `elasticsearch.yml` file and keystore on each node.<br>

            For example:

            ```yaml
            xpack.monitoring.exporters:
              id1:
                type: http
                host: ["http://es-mon-1:9200", "http://es-mon-2:9200"]
                auth.username: remote_monitoring_user
                # "xpack.monitoring.exporters.id1.auth.secure_password" must be set in the keystore
            ```

    3. If you configured the monitoring cluster to use [encrypted communications](../../security/secure-cluster-communications.md#encrypt-internode-communication), you must use the HTTPS protocol in the `host` setting. You must also specify the trusted CA certificates that will be used to verify the identity of the nodes in the monitoring cluster.

        * To add a CA certificate to an {{es}} node’s trusted certificates, you can specify the location of the PEM encoded certificate with the `certificate_authorities` setting. For example:

            ```yaml
            xpack.monitoring.exporters:
              id1:
                type: http
                host: ["https://es-mon1:9200", "https://es-mon-2:9200"]
                auth:
                  username: remote_monitoring_user
                  # "xpack.monitoring.exporters.id1.auth.secure_password" must be set in the keystore
                ssl:
                  certificate_authorities: [ "/path/to/ca.crt" ]
            ```

        * Alternatively, you can configure trusted certificates using a truststore (a Java Keystore file that contains the certificates). For example:

            ```yaml
            xpack.monitoring.exporters:
              id1:
                type: http
                host: ["https://es-mon1:9200", "https://es-mon-2:9200"]
                auth:
                  username: remote_monitoring_user
                  # "xpack.monitoring.exporters.id1.auth.secure_password" must be set in the keystore
                ssl:
                  truststore.path: /path/to/file
                  truststore.password: password
            ```

4. Configure your cluster to route monitoring data from sources such as {{kib}}, Beats, and {{ls}} to the monitoring cluster. For information about configuring each product to collect and send monitoring data, see [Monitor a cluster](../../monitor.md).
5. If you updated settings in the `elasticsearch.yml` files on your production cluster, restart {{es}}. See [*Stopping Elasticsearch*](../../maintenance/start-stop-services/start-stop-elasticsearch.md) and [*Starting Elasticsearch*](../../maintenance/start-stop-services/start-stop-elasticsearch.md).

    ::::{tip}
    You may want to temporarily [disable shard allocation](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md) before you restart your nodes to avoid unnecessary shard reallocation during the install process.
    ::::

6. Optional: [Configure the indices that store the monitoring data](../monitoring-data/configuring-data-streamsindices-for-monitoring.md).
7. [View the monitoring data in {{kib}}](kibana-monitoring-data.md).






