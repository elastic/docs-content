---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/_cli_configuration.html
applies:
  stack: all
---

# Cli configuration [_cli_configuration]


## Logging configuration via CLI [logging-cli-migration] 

As is the case for any of Kibana’s config settings, you can specify your logging configuration via the CLI. For convenience, the `--verbose` and `--silent` flags exist as shortcuts and will continue to be supported beyond v7.

If you wish to override these flags, you can always do so by passing your preferred logging configuration directly to the CLI. For example, with the following configuration:

```yaml
logging:
  appenders:
    custom:
      type: console
      layout:
        type: pattern
        pattern: "[%date][%level] %message"
  root:
    level: warn
    appenders: [custom]
```

you can override the root logging level with:

| legacy logging | {{kib}} Platform logging | cli shortcuts |
| --- | --- | --- |
| --verbose | --logging.root.level=debug | --verbose |
| --silent | --logging.root.level=off | --silent |

