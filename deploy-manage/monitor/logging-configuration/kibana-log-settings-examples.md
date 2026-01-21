---
navigation_title: Examples
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/log-settings-examples.html
applies_to:
  deployment:
    self: all
products:
  - id: kibana
---

# Examples of {{kib}} logging configurations [log-settings-examples]

Here are some configuration examples for the most common logging use cases:


## Log to a file [log-to-file-example]

Log the default log format to a file instead of to stdout (the default).

```yaml
logging:
  appenders:
    file:
      type: file
      fileName: /var/log/kibana.log
      layout:
        type: pattern
  root:
    appenders: [file]
```


## Log in JSON format [log-in-json-ECS-example]

Log the default log format to JSON layout instead of pattern (the default). With `json` layout, log messages will be formatted as JSON strings in [ECS format](ecs://reference/index.md) that includes a timestamp, log level, logger, message text and any other metadata that may be associated with the log message itself.

```yaml
logging:
  appenders:
    json-layout:
      type: console
      layout:
        type: json
  root:
    appenders: [json-layout]
```


## Log with meta to stdout [log-with-meta-to-stdout]

Include `%meta` in your pattern layout:

```yaml
logging:
  appenders:
    console-meta:
      type: console
      layout:
        type: pattern
        pattern: "[%date] [%level] [%logger] [%meta] %message"
  root:
    appenders: [console-meta]
```


## Log {{es}} queries [log-elasticsearch-queries]

```yaml
logging:
  appenders:
    console_appender:
      type: console
      layout:
        type: pattern
        highlight: true
  root:
    appenders: [console_appender]
    level: warn
  loggers:
    - name: elasticsearch.query
      level: debug
```


## Change overall log level [change-overall-log-level]

```yaml
logging:
  root:
    level: debug
```


## Customize specific log records [customize-specific-log-records]

Here is a detailed configuration example that can be used to configure *loggers*, *appenders* and *layouts*:

```yaml
logging:
  appenders:
    console:
      type: console
      layout:
        type: pattern
        highlight: true
    file:
      type: file
      fileName: /var/log/kibana.log
    custom:
      type: console
      layout:
        type: pattern
        pattern: "[%date][%level] %message"
    json-file-appender:
      type: file
      fileName: /var/log/kibana-json.log
      layout:
        type: json

  root:
    appenders: [console, file]
    level: error

  loggers:
    - name: plugins
      appenders: [custom]
      level: warn
    - name: plugins.myPlugin
      level: info
    - name: server
      level: fatal
    - name: optimize
      appenders: [console]
    - name: telemetry
      appenders: [json-file-appender]
      level: all
    - name: metrics.ops
      appenders: [console]
      level: debug
```

Here is what we get with the config above:

| Context name | Appenders | Level |
| --- | --- | --- |
| root | console, file | error |
| plugins | custom | warn |
| plugins.myPlugin | custom | info |
| server | console, file | fatal |
| optimize | console | error |
| telemetry | json-file-appender | all |
| metrics.ops | console | debug |

