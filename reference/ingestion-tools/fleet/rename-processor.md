---
navigation_title: "rename"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/rename-processor.html
---

# Rename fields from events [rename-processor]


The `rename` processor specifies a list of fields to rename. This processor cannot be used to overwrite fields. To overwrite fields, either first rename the target field, or use the `drop_fields` processor to drop the field, and then rename the field.

::::{tip}
You can rename fields to resolve field name conflicts. For example, if an event has two fields, `c` and `c.b` (where `b` is a subfield of `c`), assigning scalar values results in an {{es}} error at ingest time. The assignment `{"c": 1,"c.b": 2}` would result in an error because `c` is an object and cannot be assigned a scalar value. To prevent this conflict, rename `c` to `c.value` before assigning values.
::::



## Example [_example_31]

```yaml
  - rename:
      fields:
        - from: "a.g"
          to: "e.d"
      ignore_missing: false
      fail_on_error: true
```


## Configuration settings [_configuration_settings_36]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `fields` | Yes |  | Contains:<br><br>* `from: "old-key"`, where `from` is the original field name. You can use the `@metadata.` prefix in this field to rename keys in the event metadata instead of event fields.<br>* `to: "new-key"`, where `to` is the target field name.<br> |
| `ignore_missing` | No | `false` | Whether to ignore missing keys. If `true`, no error is logged when a key that should be renamed is missing. |
| `fail_on_error` | No | `true` | Whether to fail renaming if an error occurs. If `true` and an error occurs, the renaming of fields is stopped, and the original event is returned. If `false`, renaming continues even if an error occurs during renaming. |

See [Conditions](/reference/ingestion-tools/fleet/dynamic-input-configuration.md#conditions) for a list of supported conditions.

You can specify multiple `rename` processors under the `processors` section.

