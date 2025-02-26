---
navigation_title: "decompress_gzip_field"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/decompress_gzip_field-processor.html
---

# Decompress gzip fields [decompress_gzip_field-processor]


The `decompress_gzip_field` processor specifies a field to gzip decompress.

To overwrite fields, either first rename the target field, or use the `drop_fields` processor to drop the field, and then decompress the field.


## Example [_example_20]

In this example, `field1` is decompressed in `field2`.

```yaml
  - decompress_gzip_field:
      field:
        from: "field1"
        to: "field2"
      ignore_missing: false
      fail_on_error: true
```


## Configuration settings [_configuration_settings_25]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `field` | Yes |  | Contains:<br><br>* `from: "old-key"`, where `from` is the origin<br>* `to: "new-key"`, where `to` is the target field name<br> |
| `ignore_missing` | No | `false` | Whether to ignore missing keys. If `true`, no error is logged if a key that should be decompressed is missing. |
| `fail_on_error` | No | `true` | If `true` and an error occurs, decompression of fields is stopped, and the original event is returned. If `false`, decompression continues even if an error occurs during decoding. |

See [Conditions](/reference/ingestion-tools/fleet/dynamic-input-configuration.md#conditions) for a list of supported conditions.

