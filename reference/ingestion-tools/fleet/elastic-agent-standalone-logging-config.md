---
navigation_title: "Logging"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-standalone-logging-config.html
---

# Configure logging for standalone {{agent}}s [elastic-agent-standalone-logging-config]


The Logging section of the `elastic-agent.yml` config file contains settings for configuring the logging output. The logging system can write logs to the `syslog`, `file`, `stderr`, `eventlog`, or rotate log files. If you do not explicitly configure logging, the `stderr` output is used.

This example configures {{agent}} logging:

```yaml
agent.logging.level: info
agent.logging.to_files: true
agent.logging.files:
  path: /var/log/elastic-agent
  name: elastic-agent
  keepfiles: 7
  permissions: 0600
```


## Logging configuration settings [elastic-agent-standalone-logging-settings]

You can specify the following settings in the Logging section of the `elastic-agent.yml` config file.

Some outputs will log raw events on errors like indexing errors in the Elasticsearch output, to prevent logging raw events (that may contain sensitive information) together with other log messages, a different log file, only for log entries containing raw events, is used. It will use the same level, selectors and all other configurations from the default logger, but it will have it’s own file configuration.

Having a different log file for raw events also prevents event data from drowning out the regular log files. Use `agent.logging.event_data` to configure the events logger.

The events log file is not collected by the {{agent}} monitoring. If the events log files are needed, they can be collected with the diagnostics or directly copied from the host running {{agent}}.

|     |     |
| --- | --- |
| **Setting**<br> | **Description**<br> |
| `agent.logging.level`<br> | The minimum log level.<br><br>Possible values:<br><br>* `error`: Logs errors and critical errors.<br>* `warning`: Logs warnings, errors, and critical errors.<br>* `info`: Logs informational messages, including the number of events that are published. Also logs any warnings, errors, or critical errors.<br>* `debug`: Logs debug messages, including a detailed printout of all events flushed. Also logs informational messages, warnings, errors, and critical errors. When the log level is `debug`, you can specify a list of **selectors** to display debug messages for specific components. If no selectors are specified, the `*` selector is used to display debug messages for all components.<br><br>Default: `info`<br> |
| `agent.logging.selectors`<br> | Specify the selector tags that are used by different {{agent}} components for debugging. To debug the output for all components, use `*`. To display debug messages related to event publishing, set to `publish`. Multiple selectors can be chained.<br><br>Possible values: `[beat]`, `[publish]`, `[service]`<br> |
| `agent.logging.to_stderr`<br> | Set to `true` to write all logging output to the `stderr` output—this is equivalent to using the `-e` command line option.<br><br>Default: `true`<br> |
| `agent.logging.to_syslog`<br> | Set to `true` to write all logging output to the `syslog` output.<br><br>Default: `false`<br> |
| `agent.logging.to_eventlog`<br> | Set to `true` to write all logging output to the Windows `eventlog` output.<br><br>Default: `false`<br> |
| `agent.logging.metrics.enabled`<br> | Set to `true` for {{agent}} to periodically log its internal metrics that have changed in the last period. For each metric that changed, the delta from the value at the beginning of the period is logged. Also, the total values for all non-zero internal metrics get logged on shutdown. If set to `false`, no metrics for the agent or any of the {{beats}} running under it are logged.<br><br>Default: `true`<br> |
| `agent.logging.metrics.period`<br> | Specify the period after which to log the internal metrics. This setting is not passed to any {{beats}} running under the {{agent}}.<br><br>Default: `30s`<br> |
| `agent.logging.to_files`<br> | Set to `true` to log to rotating files. Set to `false` to disable logging to files.<br><br>Default: `true`<br> |
| `agent.logging.files.path`<br> | The directory that log files is written to. <br>Logs file names end with a date and optional number: log-date.ndjson, log-date-1.ndjson, and so on as new files are created during rotation.<br><br>macOS: `/Library/Elastic/Agent/data/elastic-agent-*/logs/elastic-agent.ndjson`<br>Linux: `/opt/Elastic/Agent/data/elastic-agent-*/logs/elastic-agent.ndjson`<br>Windows: `C:\Program Files\Elastic\Agent\data\elastic-agent-*\logs\elastic-agent.ndjson`<br>DEB: `/var/lib/elastic-agent/data/elastic-agent-*/logs/elastic-agent.ndjson`<br>RPM: `/var/lib/elastic-agent/data/elastic-agent-*/logs/elastic-agent.ndjson`|
| `agent.logging.files.name`<br> | The name of the file that logs are written to.<br><br>Default: `elastic-agent`<br> |
| `agent.logging.files.rotateeverybytes`<br> | The maximum size limit of a log file. If the limit is reached, a new log file is generated.<br><br>Default: `10485760` (10MB)<br> |
| `agent.logging.files.keepfiles`<br> | The most recent number of rotated log files to keep on disk. Older files are deleted during log rotation. The value must be in the range of `2` to `1024` files.<br><br>Default: `7`<br> |
| `agent.logging.files.permissions`<br> | The permissions mask to apply when rotating log files. The permissions option must be a valid Unix-style file permissions mask expressed in octal notation. In Go, numbers in octal notation must start with 0.<br><br>Default: `0600`<br> |
| `agent.logging.files.interval`<br> | Enable log file rotation on time intervals in addition to the size-based rotation. Intervals must be at least `1s`. Values of `1m`, `1h`, `24h`, `7*24h`, `30*24h`, and `365*24h` are boundary-aligned with minutes, hours, days, weeks, months, and years as reported by the local system clock. All other intervals get calculated from the Unix epoch.<br><br>Default: `0` (disabled)<br> |
| `agent.logging.files.rotateonstartup`<br> | Set to `true` to rotate existing logs on startup rather than to append to the existing file.<br><br>Default: `true`<br> |
| `agent.logging.event_data.to_files`<br> | Set to `true` to log to rotating files. Set to `false` to disable logging to files.<br><br>Default: `true`<br> |
| `agent.logging.event_data.path`<br> | The directory that log files is written to. <br>Logs file names end with a date and optional number: log-date.ndjson, log-date-1.ndjson, and so on as new files are created during rotation.<br><br>macOS: `/Library/Elastic/Agent/data/elastic-agent-*/logs/events/elastic-agent-event-log*.ndjson`<br>Linux: `/opt/Elastic/Agent/data/elastic-agent-*/logs/events/elastic-agent-event-log*.ndjson`<br>Windows: `C:\Program Files\Elastic\Agent\data\elastic-agent-*\logs\events\elastic-agent-event-log*.ndjson`<br>DEB: `/var/lib/elastic-agent/data/elastic-agent-*/logs/events/elastic-agent-event-log*.ndjson`<br>RPM: `/var/lib/elastic-agent/data/elastic-agent-*/logs/events/elastic-agent-event-log*.ndjson`
| `agent.logging.event_data.files.name`<br> | The name of the file that logs are written to.<br><br>Default: `elastic-agent-event-data`<br> |
| `agent.logging.event_data.files.rotateeverybytes`<br> | The maximum size limit of a log file. If the limit is reached, a new log file is generated.<br><br>Default: `5242880` (5MB)<br> |
| `agent.logging.event_data.files.keepfiles`<br> | The most recent number of rotated log files to keep on disk. Older files are deleted during log rotation. The value must be in the range of `2` to `1024` files.<br><br>Default: `2`<br> |
| `agent.logging.event_data.files.permissions`<br> | The permissions mask to apply when rotating log files. The permissions option must be a valid Unix-style file permissions mask expressed in octal notation. In Go, numbers in octal notation must start with 0.<br><br>Default: `0600`<br> |
| `agent.logging.event_data.files.interval`<br> | Enable log file rotation on time intervals in addition to the size-based rotation. Intervals must be at least `1s`. Values of `1m`, `1h`, `24h`, `7*24h`, `30*24h`, and `365*24h` are boundary-aligned with minutes, hours, days, weeks, months, and years as reported by the local system clock. All other intervals get calculated from the Unix epoch.<br><br>Default: `0` (disabled)<br> |
| `agent.logging.event_data.files.rotateonstartup`<br> | Set to `true` to rotate existing logs on startup rather than to append to the existing file.<br><br>Default: `false`<br> |
