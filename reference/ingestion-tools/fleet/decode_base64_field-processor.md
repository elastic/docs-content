---
navigation_title: "decode_base64_field"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/decode_base64_field-processor.html
---

# Decode Base64 fields [decode_base64_field-processor]


The `decode_base64_field` processor specifies a field to base64 decode.

To overwrite fields, either rename the target field or use the `drop_fields` processor to drop the field, and then rename the field.


## Example [_example_15]

In this example, `field1` is decoded in `field2`.

```yaml
  - decode_base64_field:
      field:
        from: "field1"
        to: "field2"
      ignore_missing: false
      fail_on_error: true
```


## Configuration settings [_configuration_settings_18]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `field` | Yes |  | Contains:<br><br>* `from: "old-key"`, where `from` is the origin<br>* `to: "new-key"`, where `to` is the target field name<br> |
| `ignore_missing` | No | `false` | Whether to ignore missing keys. If `true`, missing keys that should be base64 decoded are ignored and no error is logged. If `false`, an error is logged and the behavior of `fail_on_error` is applied. |
| `fail_on_error` | No | `true` | Whether to fail if an error occurs. If `true` and an error occurs, an error is logged and the event is dropped. If `false`, an error is logged, but the event is not modified. |

See [Conditions](/reference/ingestion-tools/fleet/dynamic-input-configuration.md#conditions) for a list of supported conditions.

