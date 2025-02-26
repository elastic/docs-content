---
navigation_title: "copy_fields"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/copy_fields-processor.html
---

# Copy fields [copy_fields-processor]


The `copy_fields` processor takes the value of a field and copies it to a new field.

You cannot use this processor to replace an existing field. If the target field already exists, you must [drop](/reference/ingestion-tools/fleet/drop_fields-processor.md) or [rename](/reference/ingestion-tools/fleet/rename-processor.md) the field before using `copy_fields`.


## Example [_example_14]

This configuration:

```yaml
  - copy_fields:
      fields:
        - from: message
          to: event.original
      fail_on_error: false
      ignore_missing: true
```

Copies the original `message` field to `event.original`:

```json
{
  "message": "my-interesting-message",
  "event": {
      "original": "my-interesting-message"
  }
}
```


## Configuration settings [_configuration_settings_17]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `fields` | Yes |  | List of `from` and `to` pairs to copy from and to. You can use the `@metadata.` prefix to copy values from or to event metadata. |
| `fail_on_error` | No | `true` | Whether to fail if an error occurs. If `true` and an error occurs, any changes are reverted, and the original is returned. If `false`, processing continues even if an error occurs. |
| `ignore_missing` | No | `false` | Whether to ignore events that lack the source field. If `false`, the processing of an event will fail if a field is missing. |

