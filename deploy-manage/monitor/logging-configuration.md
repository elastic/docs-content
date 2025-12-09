---
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
---
# Logging

You can configure several types of logs in {{stack}} that can help you to gain insight into {{stack}} operations, diagnose issues, and track certain types of events.

The following logging features are available:

## For {{es}} [extra-logging-features-elasticsearch]

* **Application and component logging**: Logs messages related to running {{es}}.

  You can [configure the log level for {{es}}](/deploy-manage/monitor/logging-configuration/update-elasticsearch-logging-levels.md), and, in self-managed clusters, [configure underlying Log4j settings](/deploy-manage/monitor/logging-configuration/elasticsearch-log4j-configuration-self-managed.md) to customize logging behavior.
* [Deprecation logging](/deploy-manage/monitor/logging-configuration/elasticsearch-deprecation-logs.md): Deprecation logs record a message to the {{es}} log directory when you use deprecated {{es}} functionality. You can use the deprecation logs to update your application before upgrading {{es}} to a new major version.
* [Audit logging](/deploy-manage/security/logging-configuration/enabling-audit-logs.md): Logs security-related events on your deployment.
* [Slow query and index logging](/deploy-manage/monitor/logging-configuration/slow-logs.md): Helps find and debug slow queries and indexing.

## For {{kib}} [extra-logging-features-kibana]

* **Application and component logging**: Logs messages related to running {{kib}}.

  You can [configure the log level for {{kib}}](/deploy-manage/monitor/logging-configuration/kibana-log-levels.md), and, in self-managed, ECE, or ECK deployments, [configure advanced settings](/deploy-manage/monitor/logging-configuration/kib-advanced-logging.md) to customize logging behavior.

* [Audit logging](/deploy-manage/security/logging-configuration/enabling-audit-logs.md): Logs security-related events on your deployment.

## Access {{kib}} and {{es}} logs

The way that you access your logs differs depending on your deployment method.

### Orchestrated deployments

Access your logs using one of the following options:

* All orchestrated deployments: [](/deploy-manage/monitor/stack-monitoring.md)
* {{ech}}: [Preconfigured logs and metrics](/deploy-manage/monitor/cloud-health-perf.md#ec-es-health-preconfigured)
* {{ece}}: [Platform monitoring](/deploy-manage/monitor/orchestrators/ece-platform-monitoring.md)

### Self-managed deployments

#### {{kib}}

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

If you run {{kib}} from the command line, {{kib}} prints logs to the standard output (`stdout`).

You can also consume logs using [stack monitoring](/deploy-manage/monitor/stack-monitoring/kibana-monitoring-self-managed.md).

#### {{es}}

If you run {{es}} as a service, the default location of the logs varies based on your platform and installation method:

:::::::{tab-set}

::::::{tab-item} Docker
On [Docker](/deploy-manage/deploy/self-managed/install-elasticsearch-with-docker.md), log messages go to the console and are handled by the configured Docker logging driver. To access logs, run `docker logs`.
::::::

::::::{tab-item} Debian (APT) and RPM
For [Debian](/deploy-manage/deploy/self-managed/install-elasticsearch-with-debian-package.md) and [RPM](/deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm.md) installations, {{es}} writes logs to `/var/log/elasticsearch`.
::::::

::::::{tab-item} macOS and Linux
For [macOS and Linux `.tar.gz`](/deploy-manage/deploy/self-managed/install-elasticsearch-from-archive-on-linux-macos.md) installations, {{es}} writes logs to `$ES_HOME/logs`.

Files in `$ES_HOME` risk deletion during an upgrade. In production, we strongly recommend you set `path.logs` to a location outside of `$ES_HOME`. See [Path settings](/deploy-manage/deploy/self-managed/important-settings-configuration.md#path-settings).
::::::

::::::{tab-item} Windows .zip
For [Windows `.zip`](/deploy-manage/deploy/self-managed/install-elasticsearch-with-zip-on-windows.md) installations, {{es}} writes logs to `%ES_HOME%\logs`.

Files in `%ES_HOME%` risk deletion during an upgrade. In production, we strongly recommend you set `path.logs` to a location outside of `%ES_HOME%`. See [Path settings](/deploy-manage/deploy/self-managed/important-settings-configuration.md#path-settings).
::::::

:::::::

If you run {{es}} from the command line, {{es}} prints logs to the standard output (`stdout`).

You can also consume logs using [stack monitoring](/deploy-manage/monitor/stack-monitoring/elasticsearch-monitoring-self-managed.md).

## Other components [extra-logging-features-enterprise-search]

You can also collect and index the following types of logs from other components in your deployments:

[**APM**](/solutions/observability/apm/apm-server/configure-logging.md)

* `apm*.log*`

[**Fleet and Elastic Agent**](/reference/fleet/monitor-elastic-agent.md)

* `fleet-server-json.log-*`
* `elastic-agent-json.log-*`

The `*` indicates that we also index the archived files of each type of log.

In {{ech}} and {{ece}}, these types of logs are automatically ingested when [stack monitoring](/deploy-manage/monitor/stack-monitoring.md) is enabled.
