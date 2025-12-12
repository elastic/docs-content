---
navigation_title: Collect monitoring data with {{metricbeat}}
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/monitoring-metricbeat.html
applies_to:
  deployment:
    self: all
products:
  - id: kibana
---



# Collect monitoring data with Metricbeat [monitoring-metricbeat]


You can use {{metricbeat}} to collect data about {{kib}} and ship it to the monitoring cluster.

To learn about monitoring in general, refer to [](/deploy-manage/monitor/stack-monitoring.md).

:::{image} /deploy-manage/images/kibana-metricbeat.png
:alt: Example monitoring architecture
:width: 450px
:::


1. Disable the default collection of {{kib}} monitoring metrics.

    Add the following setting in the {{kib}} configuration file ([`kibana.yml`](/deploy-manage/stack-settings.md)):

    ```yaml
    monitoring.kibana.collection.enabled: false
    ```

    Leave the `monitoring.enabled` set to its default value (`true`). For more information, see [Monitoring settings in {{kib}}](kibana://reference/configuration-reference/monitoring-settings.md).

2. [Start {{kib}}](../../maintenance/start-stop-services/start-stop-kibana.md).
3. Set the `xpack.monitoring.collection.enabled` setting to `true` on each node in the production cluster. By default, it is disabled (`false`).

    ::::{note}
    You can specify this setting in either the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) on each node or across the cluster as a dynamic cluster setting. If {{es}} {{security-features}} are enabled, you must have `monitor` cluster privileges to view the cluster settings and `manage` cluster privileges to change them.
    ::::


    * In {{kib}}:

        1. Open {{kib}} in your web browser.

            If you are running {{kib}} locally, go to `http://localhost:5601/`.

            If the Elastic {{security-features}} are enabled, log in.

        2. In the side navigation, click **Stack Monitoring**. If data collection is disabled, you are prompted to turn it on.

    * From the Console or command line, set `xpack.monitoring.collection.enabled` to `true` on the production cluster.<br>

        For example, you can use the following APIs to review and change this setting:

        ```console
        GET _cluster/settings
        ```

        ```console
        PUT _cluster/settings
        {
          "persistent": {
            "xpack.monitoring.collection.enabled": true
          }
        }
        ```

        For more information, see [Monitoring settings in {{es}}](elasticsearch://reference/elasticsearch/configuration-reference/monitoring-settings.md) and [the Cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings).

4. [Install {{metricbeat}}](beats://reference/metricbeat/metricbeat-installation-configuration.md) on the same server as {{kib}}.
5. Enable the {{kib}} X-Pack module in {{metricbeat}}.<br>

    For example, to enable the default configuration in the `modules.d` directory, run the following command:

    ```sh
    metricbeat modules enable kibana-xpack
    ```

    For more information, see [Specify which modules to run](beats://reference/metricbeat/configuration-metricbeat.md) and [{{kib}} module](beats://reference/metricbeat/metricbeat-module-kibana.md).

6. Configure the {{kib}} X-Pack module in {{metricbeat}}.<br>

    The `modules.d/kibana-xpack.yml` file contains the following settings:

    ```yaml
    - module: kibana
      metricsets:
        - stats
      period: 10s
      hosts: ["localhost:5601"]
      #basepath: ""
      #username: "user"
      #password: "secret"
      xpack.enabled: true
    ```

    By default, the module collects {{kib}} monitoring metrics from `localhost:5601`. If that host and port number are not correct, you must update the `hosts` setting. If you configured {{kib}} to use encrypted communications, you must access it via HTTPS. For example, use a `hosts` setting like `https://localhost:5601`.

    If the Elastic {{security-features}} are enabled, you must also provide a user ID and password so that {{metricbeat}} can collect metrics successfully:

    1. Create a user on the production cluster that has the `remote_monitoring_collector` [built-in role](elasticsearch://reference/elasticsearch/roles.md#built-in-roles-remote-monitoring-collector). Alternatively, use the `remote_monitoring_user` [built-in user](../../users-roles/cluster-or-deployment-auth/built-in-users.md).
    2. Add the `username` and `password` settings to the {{kib}} module configuration file.

7. Optional: Disable the system module in {{metricbeat}}.

    By default, the [system module](beats://reference/metricbeat/metricbeat-module-system.md) is enabled. The information it collects, however, is not shown on the **Monitoring** page in {{kib}}. Unless you want to use that information for other purposes, run the following command:

    ```sh
    metricbeat modules disable system
    ```

8. Identify where to send the monitoring data.<br>

    ::::{tip}
    In production environments, we strongly recommend using a separate cluster (referred to as the *monitoring cluster*) to store the data. Using a separate monitoring cluster prevents production cluster outages from impacting your ability to access your monitoring data. It also prevents monitoring activities from impacting the performance of your production cluster.

    For more information, refer to [](/deploy-manage/monitor/stack-monitoring/es-self-monitoring-prod.md).
    ::::


    For example, specify the {{es}} output information in the {{metricbeat}} configuration file (`metricbeat.yml`):

    ```yaml
    output.elasticsearch:
      # Array of hosts to connect to.
      hosts: ["<ES_MONITORING_HOST1_URL>:9200", "http://es-mon2:9200"] <1>

      # Optional protocol and basic auth credentials.
      #protocol: "https"
      #username: "elastic"
      #password: "changeme"
    ```

    1. In this example, the data is stored on a monitoring cluster with nodes `es-mon-1` and `es-mon-2`.


    If you configured the monitoring cluster to use encrypted communications, you must access it via HTTPS. For example, use a `hosts` setting like `https://es-mon-1:9200`.

    ::::{important}
    The {{es}} {{monitor-features}} use ingest pipelines. The cluster that stores the monitoring data must have at least one node with the `ingest` role.
    ::::


    If the {{es}} {{security-features}} are enabled on the monitoring cluster, you must provide a valid user ID and password so that {{metricbeat}} can send metrics successfully:

    1. Create a user on the monitoring cluster that has the `remote_monitoring_agent` [built-in role](elasticsearch://reference/elasticsearch/roles.md#built-in-roles-remote-monitoring-collector). Alternatively, use the `remote_monitoring_user` [built-in user](../../users-roles/cluster-or-deployment-auth/built-in-users.md).
    2. Add the `username` and `password` settings to the {{es}} output information in the {{metricbeat}} configuration file.

    For more information about these configuration options, see [Configure the {{es}} output](beats://reference/metricbeat/elasticsearch-output.md).

9. [Start {{metricbeat}}](beats://reference/metricbeat/metricbeat-starting.md).
10. [View the monitoring data in {{kib}}](/deploy-manage/monitor/stack-monitoring/kibana-monitoring-data.md).

