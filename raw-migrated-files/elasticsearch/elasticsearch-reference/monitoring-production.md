# Monitoring in a production environment [monitoring-production]

In production, you should send monitoring data to a separate *monitoring cluster* so that historical data is available even when the nodes you are monitoring are not.

::::{important}
{{agent}} and {{metricbeat}} are the recommended methods for collecting and shipping monitoring data to a monitoring cluster.

If you have previously configured legacy collection methods, you should migrate to using [{{agent}}](../../../deploy-manage/monitor/stack-monitoring/collecting-monitoring-data-with-elastic-agent.md) or [{{metricbeat}}](../../../deploy-manage/monitor/stack-monitoring/collecting-monitoring-data-with-metricbeat.md) collection. Do not use legacy collection alongside other collection methods.

::::


If you have at least a Gold Subscription, using a dedicated monitoring cluster also enables you to monitor multiple clusters from a central location.

To store monitoring data in a separate cluster:

1. Set up the {{es}} cluster you want to use as the monitoring cluster. For example, you might set up a two host cluster with the nodes `es-mon-1` and `es-mon-2`.

    ::::{important}
    * Ideally the monitoring cluster and the production cluster run on the same {{stack}} version. However, a monitoring cluster on the latest release of 9.x also works with production clusters that use the same major version. Monitoring clusters that use 9.x also work with production clusters that use the latest release of 8.x.
    * There must be at least one [ingest node](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md) in the monitoring cluster; it does not need to be a dedicated ingest node.

    ::::


    1. (Optional) Verify that the collection of monitoring data is disabled on the monitoring cluster. By default, the `xpack.monitoring.collection.enabled` setting is `false`.

        For example, you can use the following APIs to review and change this setting:

        ```console
        GET _cluster/settings

        PUT _cluster/settings
        {
          "persistent": {
            "xpack.monitoring.collection.enabled": false
          }
        }
        ```

    2. If the {{es}} {{security-features}} are enabled on the monitoring cluster, create users that can send and retrieve monitoring data:

        ::::{note}
        If you plan to use {{kib}} to view monitoring data, username and password credentials must be valid on both the {{kib}} server and the monitoring cluster.
        ::::


        * If you plan to use {{agent}}, create a user that has the `remote_monitoring_collector` [built-in role](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md#built-in-roles-remote-monitoring-agent) and that the monitoring related [integration assets have been installed](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/install-uninstall-integration-assets.md#install-integration-assets) on the remote monitoring cluster.
        * If you plan to use {{metricbeat}}, create a user that has the `remote_monitoring_collector` built-in role and a user that has the `remote_monitoring_agent` [built-in role](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md#built-in-roles-remote-monitoring-agent). Alternatively, use the `remote_monitoring_user` [built-in user](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).
        * If you plan to use HTTP exporters to route data through your production cluster, create a user that has the `remote_monitoring_agent` [built-in role](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md#built-in-roles-remote-monitoring-agent).

            For example, the following request creates a `remote_monitor` user that has the `remote_monitoring_agent` role:

            ```console
            POST /_security/user/remote_monitor
            {
              "password" : "changeme",
              "roles" : [ "remote_monitoring_agent"],
              "full_name" : "Internal Agent For Remote Monitoring"
            }
            ```

            Alternatively, use the `remote_monitoring_user` [built-in user](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).

2. Configure your production cluster to collect data and send it to the monitoring cluster:

    * [{{agent}} collection methods](../../../deploy-manage/monitor/stack-monitoring/collecting-monitoring-data-with-elastic-agent.md)
    * [{{metricbeat}} collection methods](../../../deploy-manage/monitor/stack-monitoring/collecting-monitoring-data-with-metricbeat.md)
    * [Legacy collection methods](../../../deploy-manage/monitor/stack-monitoring/es-legacy-collection-methods.md)

3. (Optional) [Configure {{ls}} to collect data and send it to the monitoring cluster](asciidocalypse://docs/logstash/docs/reference/ingestion-tools/logstash/monitoring-logstash-legacy.md).
4. (Optional) Configure the {{beats}} to collect data and send it to the monitoring cluster. Skip this step for {{beats}} that are managed by {{agent}}.

    * [Auditbeat](asciidocalypse://docs/beats/docs/reference/ingestion-tools/beats-auditbeat/monitoring.md)
    * [Filebeat](asciidocalypse://docs/beats/docs/reference/ingestion-tools/beats-filebeat/monitoring.md)
    * [Heartbeat](asciidocalypse://docs/beats/docs/reference/ingestion-tools/beats-heartbeat/monitoring.md)
    * [Metricbeat](asciidocalypse://docs/beats/docs/reference/ingestion-tools/beats-metricbeat/monitoring.md)
    * [Packetbeat](asciidocalypse://docs/beats/docs/reference/ingestion-tools/beats-packetbeat/monitoring.md)
    * [Winlogbeat](asciidocalypse://docs/beats/docs/reference/ingestion-tools/beats-winlogbeat/monitoring.md)

5. (Optional) [Configure APM Server monitoring](/solutions/observability/apps/monitor-apm-server.md)
6. (Optional) Configure {{kib}} to collect data and send it to the monitoring cluster:

    * [{{agent}} collection methods](../../../deploy-manage/monitor/stack-monitoring/kibana-monitoring-elastic-agent.md)
    * [{{metricbeat}} collection methods](../../../deploy-manage/monitor/stack-monitoring/kibana-monitoring-metricbeat.md)
    * [Legacy collection methods](../../../deploy-manage/monitor/stack-monitoring/kibana-monitoring-legacy.md)

7. (Optional) Create a dedicated {{kib}} instance for monitoring, rather than using a single {{kib}} instance to access both your production cluster and monitoring cluster.

    ::::{note}
    If you log in to {{kib}} using SAML, Kerberos, PKI, OpenID Connect, or token authentication providers, a dedicated {{kib}} instance is **required**. The security tokens that are used in these contexts are cluster-specific; therefore you cannot use a single {{kib}} instance to connect to both production and monitoring clusters.
    ::::


    1. (Optional) Disable the collection of monitoring data in this {{kib}} instance. Set the `xpack.monitoring.kibana.collection.enabled` setting to `false` in the `kibana.yml` file. For more information about this setting, see [Monitoring settings in {{kib}}](asciidocalypse://docs/kibana/docs/reference/configuration-reference/monitoring-settings.md).

8. [Configure {{kib}} to retrieve and display the monitoring data](../../../deploy-manage/monitor/stack-monitoring/kibana-monitoring-data.md).

