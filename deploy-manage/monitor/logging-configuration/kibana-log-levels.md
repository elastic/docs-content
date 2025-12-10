---
applies_to:
  stack: all
---

# Set global log levels for {{kib}}

{{kib}} logging supports the following log levels: `off`, `fatal`, `error`, `warn`, `info`, `debug`, `trace`, `all`.

Levels are ordered, so `off` > `fatal` > `error` > `warn` > `info` > `debug` > `trace` > `all`.

A record will be logged by the logger if its level is higher than or equal to the level of its logger. For example: If the output of an API call is configured to log at the `info` level and the parameters passed to the API call are set to `debug`, with a global logging configuration in [`kibana.yml`](/deploy-manage/stack-settings.md) set to `debug`, both the output *and* parameters are logged. If the log level is set to `info`, the debug logs are ignored, meaning that you’ll only get a record for the API output and *not* for the parameters.

To set the log level, add the `logging.root.level` setting to [`kibana.yml`](/deploy-manage/stack-settings.md), specifying the log level that you want. `logging.root.level` defaults to `info`.

In a self-managed cluster, these levels can also be specified using [CLI arguments](/deploy-manage/monitor/logging-configuration/kib-advanced-logging.md#logging-cli-migration), and different log levels can be set for various loggers. [Learn more](/deploy-manage/monitor/logging-configuration/kib-advanced-logging.md).