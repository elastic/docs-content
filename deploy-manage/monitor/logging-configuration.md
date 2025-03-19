---
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
---
# Logging configuration

% What needs to be done: Write from scratch

% GitHub issue: https://github.com/elastic/docs-projects/issues/350

⚠️ **This page is a work in progress.** ⚠️


## Logging features [ECE/ECH] [extra-logging-features]

When shipping logs to a monitoring deployment there are more logging features available to you. These features include:


### For {{es}} [extra-logging-features-elasticsearch]

* [Audit logging](/deploy-manage/security/logging-configuration/enabling-audit-logs.md) - logs security-related events on your deployment
* [Slow query and index logging](elasticsearch://reference/elasticsearch/index-settings/slow-log.md) - helps find and debug slow queries and indexing
* Verbose logging - helps debug stack issues by increasing component logs

After you’ve enabled log delivery on your deployment, you can [add the Elasticsearch user settings](/deploy-manage/deploy/cloud-enterprise/edit-stack-settings.md) to enable these features.


### For {{kib}} [extra-logging-features-kibana]

* [Audit logging](/deploy-manage/security/logging-configuration/enabling-audit-logs.md) - logs security-related events on your deployment

After you’ve enabled log delivery on your deployment, you can [add the {{kib}} user settings](/deploy-manage/deploy/cloud-enterprise/edit-stack-settings.md) to enable this feature.


### Other components [extra-logging-features-enterprise-search]

Enabling log collection also supports collecting and indexing the following types of logs from other components in your deployments:

**APM**

* `apm*.log*`

**Fleet and Elastic Agent**

* `fleet-server-json.log-*`
* `elastic-agent-json.log-*`

The `*` indicates that we also index the archived files of each type of log.

Check the respective product documentation for more information about the logging capabilities of each product.

=====


You can use {{es}}'s application logs to monitor your cluster and diagnose issues. If you run {{es}} as a service, the default location of the logs varies based on your platform and installation method:

:::::::{tab-set}

::::::{tab-item} Docker
On [Docker](../../deploy/self-managed/install-elasticsearch-with-docker.md), log messages go to the console and are handled by the configured Docker logging driver. To access logs, run `docker logs`.
::::::

::::::{tab-item} Debian (APT) and RPM
For [Debian](../../deploy/self-managed/install-elasticsearch-with-debian-package.md) and [RPM](../../deploy/self-managed/install-elasticsearch-with-rpm.md) installations, {{es}} writes logs to `/var/log/elasticsearch`.
::::::

::::::{tab-item} macOS and Linux
For [macOS and Linux `.tar.gz`](../../deploy/self-managed/install-elasticsearch-from-archive-on-linux-macos.md) installations, {{es}} writes logs to `$ES_HOME/logs`.

Files in `$ES_HOME` risk deletion during an upgrade. In production, we strongly recommend you set `path.logs` to a location outside of `$ES_HOME`. See [Path settings](../../deploy/self-managed/important-settings-configuration.md#path-settings).
::::::

::::::{tab-item} Windows .zip
For [Windows `.zip`](../../deploy/self-managed/install-elasticsearch-with-zip-on-windows.md) installations, {{es}} writes logs to `%ES_HOME%\logs`.

Files in `%ES_HOME%` risk deletion during an upgrade. In production, we strongly recommend you set `path.logs` to a location outside of `%ES_HOME%``. See [Path settings](../../deploy/self-managed/important-settings-configuration.md#path-settings).
::::::

:::::::
If you run {{es}} from the command line, {{es}} prints logs to the standard output (`stdout`).