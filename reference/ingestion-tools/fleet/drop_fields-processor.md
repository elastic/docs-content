---
navigation_title: "drop_fields"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/drop_fields-processor.html
---

# Drop fields from events [drop_fields-processor]


The `drop_fields` processor specifies which fields to drop if a certain condition is fulfilled. The condition is optional. If it’s missing, the specified fields are always dropped. The `@timestamp` and `type` fields cannot be dropped, even if they show up in the `drop_fields` list.


## Example [_example_24]

```yaml
  - drop_fields:
      when:
        condition
      fields: ["field1", "field2", ...]
      ignore_missing: false
```

::::{note}
If you define an empty list of fields under `drop_fields`, no fields are dropped.
::::



## Configuration settings [_configuration_settings_29]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `fields` | Yes |  | If non-empty, a list of matching field names will be removed. Any element in array can contain a regular expression delimited by two slashes (*/reg_exp/*), in order to match (name) and remove more than one field. |
| `ignore_missing` | No | `false` | If `true`, the processor ignores missing fields and does not return an error. |

See [Conditions](/reference/ingestion-tools/fleet/dynamic-input-configuration.md#conditions) for a list of supported conditions.

