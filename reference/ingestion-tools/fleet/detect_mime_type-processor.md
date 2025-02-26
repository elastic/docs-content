---
navigation_title: "detect_mime_type"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/detect_mime_type-processor.html
---

# Detect mime type [detect_mime_type-processor]


The `detect_mime_type` processor attempts to detect a mime type for a field that contains a given stream of bytes.


## Example [_example_21]

In this example, `http.request.body.content` is used as the source, and `http.request.mime_type` is set to the detected mime type.

```yaml
  - detect_mime_type:
      field: http.request.body.content
      target: http.request.mime_type
```


## Configuration settings [_configuration_settings_26]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `field` | Yes |  | Field used as the data source. |
| `target` | Yes |  | Field to populate with the detected type. You can use the `@metadata.` prefixto set the value in the event metadata instead of fields. |

See [Conditions](/reference/ingestion-tools/fleet/dynamic-input-configuration.md#conditions) for a list of supported conditions.

