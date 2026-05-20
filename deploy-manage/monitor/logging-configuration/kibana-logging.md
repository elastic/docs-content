---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/logging-configuration.html
applies_to:
  stack: all
products:
  - id: kibana
---

# {{kib}} logging [logging-configuration]

$$$pattern-layout$$$
$$$time-interval-triggering-policy$$$
$$$size-limit-triggering-policy$$$
$$$logging-appenders$$$
$$$dedicated-loggers$$$

You do not need to configure any additional settings to use the logging features in {{kib}}. Logging is enabled by default.

In all deployment types, you might want to change the log level for {{kib}}. In a self-managed, ECE, or ECK deployment, you might want to further customize your logging settings to define where log messages are displayed, stored, and formatted, or provide granular settings for different loggers.

* [](/deploy-manage/monitor/logging-configuration/kibana-log-levels.md)
* [](/deploy-manage/monitor/logging-configuration/kib-advanced-logging.md)

You can also configure [{{kib}} task manager health monitoring](/deploy-manage/monitor/kibana-task-manager-health-monitoring.md) using logging settings.

:::{tip}
For additional information about the available logging settings, refer to the [{{kib}} configuration reference](kibana://reference/configuration-reference/logging-settings.md).
:::

## Access {{kib}} logs

The way that you access your logs differs depending on your deployment method.

### Orchestrated deployments

Access your logs using one of the following options: 

* All orchestrated deployments: [](/deploy-manage/monitor/stack-monitoring.md)
* {{ech}}: [Preconfigured logs and metrics](/deploy-manage/monitor/cloud-health-perf.md#ec-es-health-preconfigured)
* {{ece}}: [Platform monitoring](/deploy-manage/monitor/orchestrators/ece-platform-monitoring.md)

### Self-managed deployments

If you run {{kib}} as a service, the default location of the logs varies based on your platform and installation method:

:::::::{tab-set}

::::::{tab-item} Docker
On [Docker](/deploy-manage/deploy/self-managed/install-elasticsearch-with-docker.md), log messages go to the console and are handled by the configured Docker logging driver. To access logs, run `docker logs`.
::::::

::::::{tab-item} Debian (APT) and RPM
For [Debian](/deploy-manage/deploy/self-managed/install-elasticsearch-with-debian-package.md) and [RPM](/deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm.md) installations, {{es}} writes logs to `/var/log/kibana`.
::::::

::::::{tab-item} macOS and Linux
For [macOS and Linux `.tar.gz`](/deploy-manage/deploy/self-managed/install-elasticsearch-from-archive-on-linux-macos.md) installations, {{es}} writes logs to `$KIBANA_HOME/logs`.

Files in `$KIBANA_HOME` risk deletion during an upgrade. In production, you should configure a [different location for your logs](/deploy-manage/monitor/logging-configuration/kib-advanced-logging.md).
::::::

::::::{tab-item} Windows .zip
For [Windows `.zip`](/deploy-manage/deploy/self-managed/install-elasticsearch-with-zip-on-windows.md) installations, {{es}} writes logs to `%KIBANA_HOME%\logs`.

Files in `%KIBANA_HOME%` risk deletion during an upgrade. In production, you should configure a [different location for your logs](/deploy-manage/monitor/logging-configuration/kib-advanced-logging.md).
::::::

:::::::

If you run {{kib}} from the command line, {{es}} prints logs to the standard output (`stdout`).

You can also consume logs using [stack monitoring](/deploy-manage/monitor/stack-monitoring/kibana-monitoring-self-managed.md).
