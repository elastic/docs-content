---
navigation_title: Collecting monitoring data with {{metricbeat}}
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/configuring-metricbeat.html
applies_to:
  deployment:
    self: all
products:
  - id: elasticsearch
---



# Collecting monitoring data with Metricbeat [configuring-metricbeat]


You can use {{metricbeat}} to collect data about {{es}} and ship it to the monitoring cluster.

:::{tip}
Want to use {{agent}} instead? Refer to [Collecting monitoring data with {{agent}}](collecting-monitoring-data-with-elastic-agent.md).
:::

:::{image} /deploy-manage/images/elasticsearch-reference-metricbeat.png
:alt: Example monitoring architecture
:width: 550px
:::

1. [Install {{metricbeat}}](beats://reference/metricbeat/metricbeat-installation-configuration.md). 
   
   Ideally, install a single {{metricbeat}} instance configured with `scope: cluster` and configure `hosts` to point to an endpoint, such as a load-balancing proxy, which directs requests to the master-ineligible nodes in the cluster. 
   
   If this is not possible, then install one {{metricbeat}} instance for each {{es}} node in the production cluster and use the default `scope: node`. When {{metricbeat}} is monitoring {{es}} with `scope: node` then you must install a {{metricbeat}} instance for each {{es}} node. If you don’t, some metrics will not be collected. 
   
   {{metricbeat}} with `scope: node` collects most of the metrics from the elected master of the cluster, so you must scale up all your master-eligible nodes to account for this extra load. You should not use this mode if you have dedicated master nodes.
2. Enable the {{es}} module in {{metricbeat}} on each {{es}} node.

    For example, to enable the default configuration for the {{stack-monitor-features}} in the `modules.d` directory, run the following command:

    ```sh
    metricbeat modules enable elasticsearch-xpack
    ```

    For more information, refer to [{{es}} module](beats://reference/metricbeat/metricbeat-module-elasticsearch.md).

3. Configure the {{es}} module in {{metricbeat}} on each {{es}} node.

    The `modules.d/elasticsearch-xpack.yml` file contains the following settings:

    ```yaml
      - module: elasticsearch
        xpack.enabled: true
        period: 10s
        hosts: ["http://localhost:9200"] <1>
        #scope: node <2>
        #username: "user"
        #password: "secret"
        #ssl.enabled: true
        #ssl.certificate_authorities: ["/etc/pki/root/ca.pem"]
        #ssl.certificate: "/etc/pki/client/cert.pem"
        #ssl.key: "/etc/pki/client/cert.key"
        #ssl.verification_mode: "full"
    ```

    1. By default, the module collects {{es}} monitoring metrics from `http://localhost:9200`. If that host and port number are not correct, you must update the `hosts` setting. If you configured {{es}} to use encrypted communications, you must access it via HTTPS. For example, use a `hosts` setting like `https://localhost:9200`.
    2. By default, `scope` is set to `node` and each entry in the `hosts` list indicates a distinct node in an {{es}} cluster. If you set `scope` to `cluster` then each entry in the `hosts` list indicates a single endpoint for a distinct {{es}} cluster (for example, a load-balancing proxy fronting the cluster). You should use `scope: cluster` if the cluster has dedicated master nodes, and configure the endpoint in the `hosts` list not to direct requests to the dedicated master nodes.


    If Elastic {{security-features}} are enabled, you must also provide a user ID and password so that {{metricbeat}} can collect metrics successfully:

    1. Create a user on the production cluster that has the [`remote_monitoring_collector` built-in role](elasticsearch://reference/elasticsearch/roles.md). Alternatively, use the [`remote_monitoring_user` built-in user](elasticsearch://reference/elasticsearch/roles.md).
    2. Add the `username` and `password` settings to the {{es}} module configuration file.
    3. If TLS is enabled on the HTTP layer of your {{es}} cluster, you must either use https as the URL scheme in the `hosts` setting or add the `ssl.enabled: true` setting. Depending on the TLS configuration of your {{es}} cluster, you might also need to specify [additional ssl.*](beats://reference/metricbeat/configuration-ssl.md) settings.

4. Optional: Disable the system module in {{metricbeat}}.

    By default, the [system module](beats://reference/metricbeat/metricbeat-module-system.md) is enabled. The information it collects, however, is not shown on the **Monitoring** page in {{kib}}. Unless you want to use that information for other purposes, run the following command:

    ```sh
    metricbeat modules disable system
    ```

5. Identify where to send the monitoring data.

    ::::{tip}
    In production environments, we strongly recommend using a separate cluster (referred to as the *monitoring cluster*) to store the data. Using a separate monitoring cluster prevents production cluster outages from impacting your ability to access your monitoring data. It also prevents monitoring activities from impacting the performance of your production cluster. 

    For more information, refer to [](/deploy-manage/monitor/stack-monitoring/es-self-monitoring-prod.md).
    ::::


    For example, specify the {{es}} output information in the {{metricbeat}} configuration file (`metricbeat.yml`):

    ```yaml
    output.elasticsearch:
      # Array of hosts to connect to.
      hosts: ["<ES_MONITORING_HOST1_URL>:9200", "<ES_MONITORING_HOST2_URL>:9200"] <1>

      # Optional protocol and basic auth credentials.
      #protocol: "https"
      #username: "elastic"
      #password: "changeme"
    ```

    1. In this example, the data is stored on a monitoring cluster with nodes `es-mon-1` and `es-mon-2`.


    If you configured the monitoring cluster to use encrypted communications, you must access it via HTTPS. For example, use a `hosts` setting like `https://es-mon-1:9200`.

    ::::{important}
    The {{es}} {{monitor-features}} use ingest pipelines, therefore the cluster that stores the monitoring data must have at least one [ingest node](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md).
    ::::


    If {{es}} {{security-features}} are enabled on the monitoring cluster, you must provide a valid user ID and password so that {{metricbeat}} can send metrics successfully:

    1. Create a user on the monitoring cluster that has the [`remote_monitoring_agent` built-in role](elasticsearch://reference/elasticsearch/roles.md). Alternatively, use the [`remote_monitoring_user` built-in user](../../users-roles/cluster-or-deployment-auth/built-in-users.md).
    2. Add the `username` and `password` settings to the {{es}} output information in the {{metricbeat}} configuration file.

    For more information about these configuration options, see [Configure the {{es}} output](beats://reference/metricbeat/elasticsearch-output.md).

6. [Start {{metricbeat}}](beats://reference/metricbeat/metricbeat-starting.md) on each node.
7. [View the monitoring data in {{kib}}](kibana-monitoring-data.md).

