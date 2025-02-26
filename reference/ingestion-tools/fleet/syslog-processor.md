---
navigation_title: "syslog"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/syslog-processor.html
---

# Syslog [syslog-processor]


The syslog processor parses RFC 3146 and/or RFC 5424 formatted syslog messages that are stored in a field. The processor itself does not handle receiving syslog messages from external sources. This is done through an input, such as the TCP input. Certain integrations, when enabled through configuration, will embed the syslog processor to process syslog messages, such as Custom TCP Logs and Custom UDP Logs.


## Example [_example_33]

```yaml
  - syslog:
      field: message
```

```json
{
  "message": "<165>1 2022-01-11T22:14:15.003Z mymachine.example.com eventslog 1024 ID47 [exampleSDID@32473 iut=\"3\" eventSource=\"Application\" eventID=\"1011\"][examplePriority@32473 class=\"high\"] this is the message"
}
```

Will produce the following output:

```json
{
  "@timestamp": "2022-01-11T22:14:15.003Z",
  "log": {
    "syslog": {
      "priority": 165,
      "facility": {
        "code": 20,
        "name": "local4"
      },
      "severity": {
        "code": 5,
        "name": "Notice"
      },
      "hostname": "mymachine.example.com",
      "appname": "eventslog",
      "procid": "1024",
      "msgid": "ID47",
      "version": 1,
      "structured_data": {
        "exampleSDID@32473": {
          "iut":         "3",
          "eventSource": "Application",
          "eventID":     "1011"
        },
        "examplePriority@32473": {
          "class": "high"
        }
      }
    }
  },
  "message": "this is the message"
}
```


## Configuration settings [_configuration_settings_39]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `field` | Yes | `message` | Source field containing the syslog message. |
| `format` | No | `auto` | Syslog format to use: `rfc3164` or `rfc5424`. To automatically detect the format from the log entries, set this option to `auto`. |
| `timezone` | No | `Local` | IANA time zone name (for example, `America/New York`) or a fixed time offset (for example, `+0200`) to use when parsing syslog timestamps that do not contain a time zone. Specify `Local` to use the machine’s local time zone. |
| `overwrite_keys` | No | `true` | Whether keys that already exist in the event are overwritten by keys from the syslog message. |
| `ignore_missing` | No | `false` | Whether to ignore missing fields. If `true` the processor does not return an error when a specified field does not exist. |
| `ignore_failure` | No | `false` | Whether to ignore all errors produced by the processor. |
| `tag` | No |  | An identifier for this processor. Useful for debugging. |


## Timestamps [_timestamps]

The RFC 3164 format accepts the following forms of timestamps:

* Local timestamp (`Mmm dd hh:mm:ss`):

    * `Jan 23 14:09:01`

* RFC-3339*:

    * `2003-10-11T22:14:15Z`
    * `2003-10-11T22:14:15.123456Z`
    * `2003-10-11T22:14:15-06:00`
    * `2003-10-11T22:14:15.123456-06:00`


::::{note}
The local timestamp (for example, `Jan 23 14:09:01`) that accompanies an RFC 3164 message lacks year and time zone information. The time zone will be enriched using the `timezone` configuration option, and the year will be enriched using the system’s local time (accounting for time zones). Because of this, it is possible for messages to appear in the future. For example, this might happen if logs generated on December 31 2021 are ingested on January 1 2022. The logs would be enriched with the year 2022 instead of 2021.
::::


The RFC 5424 format accepts the following forms of timestamps:

* RFC-3339:

    * `2003-10-11T22:14:15Z`
    * `2003-10-11T22:14:15.123456Z`
    * `2003-10-11T22:14:15-06:00`
    * `2003-10-11T22:14:15.123456-06:00`


Formats with an asterisk (*) are a non-standard allowance.


## Structured Data [_structured_data]

For RFC 5424-formatted logs, if the structured data cannot be parsed according to RFC standards, the original structured data text will be prepended to the message field, separated by a space.

