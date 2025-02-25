---
navigation_title: "timestamp"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/timestamp-processor.html
---

# Timestamp [timestamp-processor]


::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::


The `timestamp` processor parses a timestamp from a field. By default the timestamp processor writes the parsed result to the `@timestamp` field. You can specify a different field by setting the `target_field` parameter. The timestamp value is parsed according to the `layouts` parameter. Multiple layouts can be specified and they will be used sequentially to attempt parsing the timestamp field.

::::{note}
The timestamp layouts used by this processor are different than the formats supported by date processors in Logstash and Elasticsearch Ingest Node.
::::


The `layouts` are described using a reference time that is based on this specific time:

```
Mon Jan 2 15:04:05 MST 2006
```
Since MST is GMT-0700, the reference time is:

```
01/02 03:04:05PM '06 -0700
```
To define your own layout, rewrite the reference time in a format that matches the timestamps you expect to parse. For more layout examples and details see the [Go time package documentation](https://godoc.org/time#pkg-constants).

If a layout does not contain a year then the current year in the specified `timezone` is added to the time value.


## Example [_example_34]

Here is an example that parses the `start_time` field and writes the result to the `@timestamp` field then deletes the `start_time` field. When the processor is loaded, it will immediately validate that the two `test` timestamps parse with this configuration.

```yaml
  - timestamp:
      field: start_time
      layouts:
        - '2006-01-02T15:04:05Z'
        - '2006-01-02T15:04:05.999Z'
        - '2006-01-02T15:04:05.999-07:00'
      test:
        - '2019-06-22T16:33:51Z'
        - '2019-11-18T04:59:51.123Z'
        - '2020-08-03T07:10:20.123456+02:00'
  - drop_fields:
      fields: [start_time]
```


## Configuration settings [_configuration_settings_40]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `field` | Yes |  | Source field containing the time to be parsed. |
| `target_field` | No | `@timestamp` | Target field for the parsed time value. The target value is always written as UTC. |
| `layouts` | Yes |  | Timestamp layouts that define the expected time value format. In addition layouts, `UNIX` and `UNIX_MS` are accepted. |
| `timezone` | No | `UTC` | IANA time zone name (for example, `America/New_York`) or fixed time offset (for example, `+0200`) to use when parsing times that do not contain a time zone. Specify `Local` to use the machine’s local time zone. |
| `ignore_missing` | No | `false` | Whether to ignore errors when the source field is missing. |
| `ignore_failure` | No | `false` | Whether to gnore all errors produced by the processor. |
| `test` | No |  | List of timestamps that must parse successfully when loading the processor. |
| `id` | No |  | Identifier for this processor instance. Useful for debugging. |

