---
navigation_title: "truncate_fields"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/truncate_fields-processor.html
---

# Truncate fields [truncate_fields-processor]


The `truncate_fields` processor truncates a field to a given size. If the size of the field is smaller than the limit, the field is left as is.


## Example [_example_36]

This configuration truncates the field named `message` to five characters:

```yaml
  - truncate_fields:
      fields:
        - message
      max_characters: 5
      fail_on_error: false
      ignore_missing: true
```


## Configuration settings [_configuration_settings_42]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `fields` | Yes |  | List of fields to truncate. You can use the `@metadata.` prefix to truncate values in the event metadata instead of event fields. |
| `max_bytes` | Yes |  | Maximum number of bytes in a field. Mutually exclusive with `max_characters`. |
| `max_characters` | Yes |  | Maximum number of characters in a field. Mutually exclusive with `max_bytes`. |
| `fail_on_error` | No | `true` | If `true` and an error occurs, any changes to the event are reverted, and the original event is returned. If `false`, processing continues even if an error occurs. |
| `ignore_missing` | No | `false` | Whether to ignore events that lack the source field. If `false`, processing of the event fails if a field is missing. |

