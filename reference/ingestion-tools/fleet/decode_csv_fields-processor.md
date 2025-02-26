---
navigation_title: "decode_csv_fields"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/decode_csv_fields-processor.html
---

# Decode CSV fields [decode_csv_fields-processor]


::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


The `decode_csv_fields` processor decodes fields containing records in comma-separated format (CSV). It will output the values as an array of strings.

::::{note}
This processor only works with log inputs.
::::



## Example [_example_17]

```yaml
  - decode_csv_fields:
      fields:
        message: decoded.csv
      separator: ","
      ignore_missing: false
      overwrite_keys: true
      trim_leading_space: false
      fail_on_error: true
```


## Configuration settings [_configuration_settings_20]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `fields` | Yes |  | A mapping from the source field containing the CSV data to the destination field to which the decoded array will be written. |
| `separator` | No | comma character (`,`) | Character to use as a column separator. To use a TAB character, set this value to "\t". |
| `ignore_missing` | No | `false` | Whether to ignore events that lack the source field. If `false`, events missing the source field will fail processing. |
| `overwrite_keys` | No | `false` | Whether the target field is overwritten if it already exists. If `false`, processing of an event fails if the target field already exists. |
| `trim_leading_space` | No | `false` | Whether extra space after the separator is trimmed from values. This works even if the separator is also a space. |
| `fail_on_error` | No | `true` | Whether to fail if an error occurs. If `true` and an error occurs, any changes to the event are reverted, and the original event is returned. If `false`, processing continues even if an error occurs. |

