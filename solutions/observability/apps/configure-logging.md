---
navigation_title: "Logging"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-configuration-logging.html
---



# Configure logging [apm-configuration-logging]


::::{admonition}
![supported deployment methods](../../../images/observability-binary-yes-fm-no.svg "")

These configuration options are only relevant to APM Server binary users. Fleet-managed users should see [View {{agent}} logs](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/monitor-elastic-agent.md) to learn how to view logs and change the logging level of {{agent}}.

::::


The `logging` section of the `apm-server.yml` config file contains options for configuring the logging output.

The logging system can write logs to the syslog or rotate log files. If logging is not explicitly configured the file output is used.

```yaml
logging.level: info
logging.to_files: true
logging.files:
  path: /var/log/apm-server
  name: apm-server
  keepfiles: 7
  permissions: 0640
```

::::{tip}
In addition to setting logging options in the config file, you can modify the logging output configuration from the command line. See [Command reference](apm-server-command-reference.md).
::::


::::{warning}
When APM Server is running on a Linux system with systemd, it uses by default the `-e` command line option, that makes it write all the logging output to stderr so it can be captured by journald. Other outputs are disabled. See [APM Server and systemd](apm-server-systemd.md) to know more and learn how to change this.
::::



## Configuration options [_configuration_options_2]

You can specify the following options in the `logging` section of the `apm-server.yml` config file:


### `logging.to_stderr` [_logging_to_stderr]

When true, writes all logging output to standard error output. This is equivalent to using the `-e` command line option.


### `logging.to_syslog` [_logging_to_syslog]

When true, writes all logging output to the syslog.

::::{note}
This option is not supported on Windows.
::::



### `logging.to_eventlog` [_logging_to_eventlog]

When true, writes all logging output to the Windows Event Log.


### `logging.to_files` [_logging_to_files]

When true, writes all logging output to files. The log files are automatically rotated when the log file size limit is reached.

::::{note}
APM Server only creates a log file if there is logging output. For example, if you set the log [`level`](#apm-level) to `error` and there are no errors, there will be no log file in the directory specified for logs.
::::



### `logging.level` [apm-level]

Minimum log level. One of `debug`, `info`, `warning`, or `error`. The default log level is `info`.

`debug`
:   Logs debug messages, including a detailed printout of all events flushed. Also logs informational messages, warnings, errors, and critical errors. When the log level is `debug`, you can specify a list of [`selectors`](#apm-selectors) to display debug messages for specific components. If no selectors are specified, the `*` selector is used to display debug messages for all components.

`info`
:   Logs informational messages, including the number of events that are published. Also logs any warnings, errors, or critical errors.

`warning`
:   Logs warnings, errors, and critical errors.

`error`
:   Logs errors and critical errors.


### `logging.selectors` [apm-selectors]

The list of debugging-only selector tags used by different APM Server components. Use `*` to enable debug output for all components. Use `publisher` to display debug messages related to event publishing.

::::{tip}
The list of available selectors may change between releases, so avoid creating tests that depend on specific selectors.

To see which selectors are available, run APM Server in debug mode (set `logging.level: debug` in the configuration). The selector name appears after the log level and is enclosed in brackets.

::::


To configure multiple selectors, use the following [YAML list syntax](asciidocalypse://docs/beats/docs/reference/ingestion-tools/beats-libbeat/config-file-format.md):

```yaml
logging.selectors: [ harvester, input ]
```

To override selectors at the command line, use the `-d` global flag (`-d` also sets the debug log level). For more information, see [Command reference](apm-server-command-reference.md).


### `logging.metrics.enabled` [_logging_metrics_enabled]

By default, APM Server periodically logs its internal metrics that have changed in the last period. For each metric that changed, the delta from the value at the beginning of the period is logged. Also, the total values for all non-zero internal metrics are logged on shutdown. Set this to false to disable this behavior. The default is true.

Here is an example log line:

```shell
2017-12-17T19:17:42.667-0500    INFO    [metrics]       log/log.go:110  Non-zero metrics in the last 30s: beat.info.uptime.ms=30004 beat.memstats.gc_next=5046416
```

Note that we currently offer no backwards compatible guarantees for the internal metrics and for this reason they are also not documented.


### `logging.metrics.period` [_logging_metrics_period]

The period after which to log the internal metrics. The default is `30s`.


### `logging.files.path` [_logging_files_path]

The directory that log files are written to. The default is the logs path. See the [Installation layout](installation-layout.md) section for details.


### `logging.files.name` [_logging_files_name]

The name of the file that logs are written to. The default is *apm-server*.


### `logging.files.rotateeverybytes` [_logging_files_rotateeverybytes]

The maximum size of a log file. If the limit is reached, a new log file is generated. The default size limit is 10485760 (10 MB).


### `logging.files.keepfiles` [_logging_files_keepfiles]

The number of most recent rotated log files to keep on disk. Older files are deleted during log rotation. The default value is 7. The `keepfiles` options has to be in the range of 2 to 1024 files.


### `logging.files.permissions` [_logging_files_permissions]

The permissions mask to apply when rotating log files. The default value is 0600. The `permissions` option must be a valid Unix-style file permissions mask expressed in octal notation. In Go, numbers in octal notation must start with *0*.

The most permissive mask allowed is 0640. If a higher permissions mask is specified via this setting, it will be subject to an umask of 0027.

Examples:

* 0640: give read and write access to the file owner, and read access to members of the group associated with the file.
* 0600: give read and write access to the file owner, and no access to all others.


### `logging.files.interval` [_logging_files_interval]

Enable log file rotation on time intervals in addition to size-based rotation. Intervals must be at least `1s`. Values of `1m`, `1h`, `24h`, `7*24h`, `30*24h`, and `365*24h` are boundary-aligned with minutes, hours, days, weeks, months, and years as reported by the local system clock. All other intervals are calculated from the Unix epoch. Defaults to disabled.


### `logging.files.rotateonstartup` [_logging_files_rotateonstartup]

If the log file already exists on startup, immediately rotate it and start writing to a new file instead of appending to the existing one. Defaults to true.


### `logging.files.redirect_stderr` [preview] [_logging_files_redirect_stderr]

When true, diagnostic messages printed to APM Server’s standard error output will also be logged to the log file. This can be helpful in situations were APM Server terminates unexpectedly because an error has been detected by Go’s runtime but diagnostic information is not present in the log file. This feature is only available when logging to files (`logging.to_files` is true). Disabled by default.


## Logging format [_logging_format]

The logging format is generally the same for each logging output. The one exception is with the syslog output where the timestamp is not included in the message because syslog adds its own timestamp.

Each log message consists of the following parts:

* Timestamp in ISO8601 format
* Level
* Logger name contained in brackets (Optional)
* File name and line number of the caller
* Message
* Structured data encoded in JSON (Optional)

Below are some samples:

`2017-12-17T18:54:16.241-0500	INFO	logp/core_test.go:13	unnamed global logger`

`2017-12-17T18:54:16.242-0500	INFO	[example]	logp/core_test.go:16	some message`

`2017-12-17T18:54:16.242-0500	INFO	[example]	logp/core_test.go:19	some message	{"x": 1}`

