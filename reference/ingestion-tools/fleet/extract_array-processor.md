---
navigation_title: "extract_array"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/extract_array-processor.html
---

# Extract array [extract_array-processor]


::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


The `extract_array` processor populates fields with values read from an array field.


## Example [_example_25]

The following example populates `source.ip` with the first element of the `my_array` field, `destination.ip` with the second element, and `network.transport` with the third.

```yaml
  - extract_array:
      field: my_array
      mappings:
        source.ip: 0
        destination.ip: 1
        network.transport: 2
```


## Configuration settings [_configuration_settings_30]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `field` | Yes |  | The array field whose elements are to be extracted. |
| `mappings` | Yes |  | Maps each field name to an array index. Use 0 for the first element in the array. Multiple fields can be mapped to the same array element. |
| `ignore_missing` | No | `false` | Whether to ignore events where the array field is missing. If `false`, processing of an event fails if the specified field does not exist. |
| `overwrite_keys` | No | `false` | Whether to overwrite target fields specified in the mapping if the fields already exist. If `false`, processing fails if a target field already exists. |
| `fail_on_error` | No | `true` | If `true` and an error occurs, any changes to the event are reverted, and the original event is returned. If `false`, processing continues despite errors. |
| `omit_empty` | No | `false` | Whether empty values are extracted from the array. If `true`, instead of the target field being set to an empty value, it is left unset. The empty string (`""`), an empty array (`[]`), or an empty object (`{}`) are considered empty values. |

