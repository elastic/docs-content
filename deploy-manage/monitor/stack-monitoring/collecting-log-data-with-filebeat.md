---
navigation_title: "Collecting log data with {{filebeat}}"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/configuring-filebeat.html
applies:
  stack: all
---



# Collecting log data with Filebeat [configuring-filebeat]


You can use {{filebeat}} to monitor the {{es}} log files, collect log events, and ship them to the monitoring cluster. Your recent logs are visible on the **Monitoring** page in {{kib}}.

::::{important} 
If you’re using {{agent}}, do not deploy {{filebeat}} for log collection. Instead, configure the {{es}} integration to collect logs.
::::


1. Verify that {{es}} is running and that the monitoring cluster is ready to receive data from {{filebeat}}.

    ::::{tip} 
    In production environments, we strongly recommend using a separate cluster (referred to as the *monitoring cluster*) to store the data. Using a separate monitoring cluster prevents production cluster outages from impacting your ability to access your monitoring data. It also prevents monitoring activities from impacting the performance of your production cluster. See [*Monitoring in a production environment*](elasticsearch-monitoring-self-managed.md).
    ::::

2. Identify which logs you want to monitor.

    The {{filebeat}} {es} module can handle [audit logs](../logging-configuration/logfile-audit-output.md), [deprecation logs](../logging-configuration/elasticsearch-log4j-configuration-self-managed.md#deprecation-logging), [gc logs](https://www.elastic.co/guide/en/elasticsearch/reference/current/advanced-configuration.html#gc-logging), [server logs](../logging-configuration/elasticsearch-log4j-configuration-self-managed.md), and [slow logs](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-slowlog.html). For more information about the location of your {{es}} logs, see the [path.logs](../../deploy/self-managed/important-settings-configuration.md#path-settings) setting.

    ::::{important} 
    If there are both structured (`*.json`) and unstructured (plain text) versions of the logs, you must use the structured logs. Otherwise, they might not appear in the appropriate context in {{kib}}.
    ::::

3. [Install {{filebeat}}](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation-configuration.html) on the {{es}} nodes that contain logs that you want to monitor.
4. Identify where to send the log data.

    For example, specify {{es}} output information for your monitoring cluster in the {{filebeat}} configuration file (`filebeat.yml`):

    ```yaml
    output.elasticsearch:
      # Array of hosts to connect to.
      hosts: ["http://es-mon-1:9200", "http://es-mon-2:9200"] <1>

      # Optional protocol and basic auth credentials.
      #protocol: "https"
      #username: "elastic"
      #password: "changeme"
    ```

    1. In this example, the data is stored on a monitoring cluster with nodes `es-mon-1` and `es-mon-2`.


    If you configured the monitoring cluster to use encrypted communications, you must access it via HTTPS. For example, use a `hosts` setting like `https://es-mon-1:9200`.

    ::::{important} 
    The {{es}} {monitor-features} use ingest pipelines, therefore the cluster that stores the monitoring data must have at least one [ingest node](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md).
    ::::


    If {{es}} {security-features} are enabled on the monitoring cluster, you must provide a valid user ID and password so that {{filebeat}} can send metrics successfully.

    For more information about these configuration options, see [Configure the {{es}} output](https://www.elastic.co/guide/en/beats/filebeat/current/elasticsearch-output.html).

5. Optional: Identify where to visualize the data.

    {{filebeat}} provides example {{kib}} dashboards, visualizations and searches. To load the dashboards into the appropriate {{kib}} instance, specify the `setup.kibana` information in the {{filebeat}} configuration file (`filebeat.yml`) on each node:

    ```yaml
    setup.kibana:
      host: "localhost:5601"
      #username: "my_kibana_user"
      #password: "YOUR_PASSWORD"
    ```

    ::::{tip} 
    In production environments, we strongly recommend using a dedicated {{kib}} instance for your monitoring cluster.
    ::::


    If {{security-features}} are enabled, you must provide a valid user ID and password so that {{filebeat}} can connect to {{kib}}:

    1. Create a user on the monitoring cluster that has the [`kibana_admin` built-in role](../../users-roles/cluster-or-deployment-auth/built-in-roles.md) or equivalent privileges.
    2. Add the `username` and `password` settings to the {{es}} output information in the {{filebeat}} configuration file. The example shows a hard-coded password, but you should store sensitive values in the [secrets keystore](https://www.elastic.co/guide/en/beats/filebeat/current/keystore.html).

    See [Configure the {{kib}} endpoint](https://www.elastic.co/guide/en/beats/filebeat/current/setup-kibana-endpoint.html).

6. Enable the {{es}} module and set up the initial {{filebeat}} environment on each node.

    For example:

    ```sh
    filebeat modules enable elasticsearch
    filebeat setup -e
    ```

    For more information, see [{{es}} module](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-elasticsearch.html).

7. Configure the {{es}} module in {{filebeat}} on each node.

    If the logs that you want to monitor aren’t in the default location, set the appropriate path variables in the `modules.d/elasticsearch.yml` file. See [Configure the {{es}} module](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-elasticsearch.html#configuring-elasticsearch-module).

    ::::{important} 
    If there are JSON logs, configure the `var.paths` settings to point to them instead of the plain text logs.
    ::::

8. [Start {{filebeat}}](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-starting.html) on each node.

    ::::{note} 
    Depending on how you’ve installed {{filebeat}}, you might see errors related to file ownership or permissions when you try to run {{filebeat}} modules. See [Config file ownership and permissions](https://www.elastic.co/guide/en/beats/libbeat/current/config-file-permissions.html).
    ::::

9. Check whether the appropriate indices exist on the monitoring cluster.

    For example, use the [cat indices](https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-indices.html) command to verify that there are new `filebeat-*` indices.

    ::::{tip} 
    If you want to use the **Monitoring** UI in {{kib}}, there must also be `.monitoring-*` indices. Those indices are generated when you collect metrics about {{stack}} products. For example, see [Collecting monitoring data with {{metricbeat}}](collecting-monitoring-data-with-metricbeat.md).
    ::::

10. [View the monitoring data in {{kib}}](kibana-monitoring-data.md).

