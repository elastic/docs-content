---
navigation_title: "Fleet-managed"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-monitor-apm-self-install.html
applies_to:
  stack: all
---



# Monitor a Fleet-managed APM Server [apm-monitor-apm-self-install]


::::{note}
This guide assumes you are already ingesting APM data into the {{stack}}.
::::


In 8.0 and later, you can use {{metricbeat}} to collect data about APM Server and ship it to a monitoring cluster. To collect and ship monitoring data:

1. [Configure {{agent}} to send monitoring data](#apm-configure-ea-monitoring-data)
2. [Install and configure {{metricbeat}} to collect monitoring data](#apm-install-config-metricbeat)


## Configure {{agent}} to send monitoring data [apm-configure-ea-monitoring-data]

::::{admonition}
Before you can monitor APM, you must have monitoring data for the {{es}} production cluster. To learn how, see [Collect {{es}} monitoring data with {{metricbeat}}](../../../deploy-manage/monitor/stack-monitoring/collecting-monitoring-data-with-metricbeat.md). Alternatively, open the **{{stack-monitor-app}}** app in {{kib}} and follow the in-product guide.

::::


1. Enable monitoring of {{agent}} by adding the following settings to your `elastic-agent.yml` configuration file:

    ```yaml
    agent.monitoring:
      http:
        enabled: true <1>
        host: localhost <2>
        port: 6791 <3>
    ```

    1. Enable monitoring
    2. The host to expose logs/metrics on
    3. The port to expose logs/metrics on

2. Enroll {{agent}}

    After editing `elastic-agent.yml`, you must re-enroll {{agent}} for the changes to take effect.

    To enroll the {{agent}} in {{fleet}}:

    ```shell
    elastic-agent enroll --url <string>
                         --enrollment-token <string>
                         [--ca-sha256 <string>]
                         [--certificate-authorities <string>]
                         [--daemon-timeout <duration>]
                         [--delay-enroll]
                         [--elastic-agent-cert <string>]
                         [--elastic-agent-cert-key <string>]
                         [--elastic-agent-cert-key-passphrase <string>]
                         [--force]
                         [--header <strings>]
                         [--help]
                         [--insecure ]
                         [--proxy-disabled]
                         [--proxy-header <strings>]
                         [--proxy-url <string>]
                         [--staging <string>]
                         [--tag <string>]
                         [global-flags]
    ```


See the [{{agent}} command reference](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/agent-command-reference.md) for more information on the enroll command.


## Install and configure {{metricbeat}} to collect monitoring data [apm-install-config-metricbeat]

1. Install {{metricbeat}} on the same server as {{agent}}. To learn how, see [Get started with {{metricbeat}}](asciidocalypse://docs/beats/docs/reference/metricbeat/metricbeat-installation-configuration.md). If you already have {{metricbeat}} installed, skip this step.
2. Enable the `beat-xpack` module in {{metricbeat}}.

    For example, to enable the default configuration in the `modules.d` directory, run the following command, using the correct command syntax for your OS:

    ```sh
    metricbeat modules enable beat-xpack
    ```

    For more information, see [Configure modules](asciidocalypse://docs/beats/docs/reference/metricbeat/configuration-metricbeat.md) and [beat module](asciidocalypse://docs/beats/docs/reference/metricbeat/metricbeat-module-beat.md).

3. Configure the `beat-xpack` module in {{metricbeat}}.

    When complete, your `modules.d/beat-xpack.yml` file should look similar to this:

    ```yaml
    - module: beat
      xpack.enabled: true
      period: 10s
      hosts: ["http://localhost:6791"]
      basepath: "/processes/apm-server-default"
      username: remote_monitoring_user
      password: your_password
    ```

    1. Do not change the  `module` name or `xpack.enabled` boolean; these are required for stack monitoring. We recommend accepting the default `period` for now.
    2. Set the `hosts` to match the host:port configured in your `elastic-agent.yml` file. In this example, that’s `http://localhost:6791`.

        To monitor multiple APM Server instances running in multiple {{agent}}s, specify a list of hosts, for example:

        ```yaml
        hosts: ["http://localhost:5066","http://localhost:5067","http://localhost:5068"]
        ```

        If you configured {{agent}} to use encrypted communications, you must access it via HTTPS. For example, use a `hosts` setting like `https://localhost:5066`.

    3. APM Server metrics are exposed at `/processes/apm-server-default`. Add this location as the `basepath`.
    4. Set the `username` and `password` settings as required by your environment. If Elastic {{security-features}} are enabled, you must provide a username and password so that {{metricbeat}} can collect metrics successfully:

        1. Create a user on the {{es}} cluster that has the `remote_monitoring_collector` [built-in role](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md). Alternatively, if it’s available in your environment, use the `remote_monitoring_user` [built-in user](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).
        2. Add the `username` and `password` settings to the beat module configuration file.

4. Optional: Disable the system module in the {{metricbeat}}.

    By default, the [system module](asciidocalypse://docs/beats/docs/reference/metricbeat/metricbeat-module-system.md) is enabled. The information it collects, however, is not shown on the **{{stack-monitor-app}}** page in {{kib}}. Unless you want to use that information for other purposes, run the following command:

    ```sh
    metricbeat modules disable system
    ```

5. Identify where to send the monitoring data.<br>

    ::::{tip}
    In production environments, you should send your deployment logs and metrics to a dedicated monitoring deployment (referred to as the *monitoring cluster*). Monitoring indexes logs and metrics into {{es}} and these indexes consume storage, memory, and CPU cycles like any other index. By using a separate monitoring deployment, you avoid affecting your other production deployments and can view the logs and metrics even when a production deployment is unavailable.
    ::::


    For example, specify the {{es}} output information in the {{metricbeat}} configuration file (`metricbeat.yml`):

    ```yaml
    output.elasticsearch:
      # Array of hosts to connect to.
      hosts: ["http://es-mon-1:9200", "http://es-mon2:9200"] <1>

      # Optional protocol and basic auth credentials.
      #protocol: "https"
      #api_key:  "id:api_key" <2>
      #username: "elastic"
      #password: "changeme"
    ```

    1. In this example, the data is stored on a monitoring cluster with nodes `es-mon-1` and `es-mon-2`.
    2. Specify one of `api_key` or `username`/`password`.


    If you configured the monitoring cluster to use encrypted communications, you must access it via HTTPS. For example, use a `hosts` setting like `https://es-mon-1:9200`.

    ::::{important}
    The {{es}} {{monitor-features}} use ingest pipelines, therefore the cluster that stores the monitoring data must have at least one ingest node.
    ::::


    If the {{es}} {{security-features}} are enabled on the monitoring cluster, you must provide a valid user ID and password so that {{metricbeat}} can send metrics successfully:

    1. Create a user on the monitoring cluster that has the `remote_monitoring_agent` [built-in role](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md). Alternatively, if it’s available in your environment, use the `remote_monitoring_user` [built-in user](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).
    2. Add the `username` and `password` settings to the {{es}} output information in the {{metricbeat}} configuration file.

    For more information about these configuration options, see [Configure the {{es}} output](asciidocalypse://docs/beats/docs/reference/metricbeat/elasticsearch-output.md).

6. [Start {{metricbeat}}](asciidocalypse://docs/beats/docs/reference/metricbeat/metricbeat-starting.md) to begin collecting APM monitoring data.
7. [View the monitoring data in {{kib}}](../../../deploy-manage/monitor/stack-monitoring/kibana-monitoring-data.md).
