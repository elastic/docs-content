---
navigation_title: "convert"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/convert-processor.html
---

# Convert field type [convert-processor]


The `convert` processor converts a field in the event to a different type, such as converting a string to an integer.

The supported types include: `integer`, `long`, `float`, `double`, `string`, `boolean`, and `ip`.

The `ip` type is effectively an alias for `string`, but with an added validation that the value is an IPv4 or IPv6 address.


## Example [_example_13]

```yaml
  - convert:
      fields:
        - {from: "src_ip", to: "source.ip", type: "ip"}
        - {from: "src_port", to: "source.port", type: "integer"}
      ignore_missing: true
      fail_on_error: false
```


## Configuration settings [_configuration_settings_16]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `fields` | Yes |  | List of fields to convert. The list must contain at least one item. Each item must have a `from` key that specifies the source field. The `to` key is optional and specifies where to assign the converted value. If `to` is omitted, the `from` field is updated in-place. The `type` key specifies the data type to convert the value to. If `type` is omitted, the processor copies or renames the field without any type conversion. |
| `ignore_missing` | No | `false` | Whether to ignore missing `from` keys. If `true` and the `from` key is not found in the event, the processor continues to the next field. If `false`, the processor returns an error and does not process the remaining fields. |
| `fail_on_error` | No | `true` | Whether to fail when a type conversion error occurs. If `false`, type conversion failures are ignored, and the processor continues to the next field. |
| `tag` | No |  | Identifier for this processor. Useful for debugging. |
| `mode` | No | `copy` | When both `from` and `to` are defined for a field, `mode` controls whether to `copy` or `rename` the field when the type conversion is successful. |

