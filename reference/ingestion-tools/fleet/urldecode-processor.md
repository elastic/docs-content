---
navigation_title: "urldecode"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/urldecode-processor.html
---

# URL Decode [urldecode-processor]


The `urldecode` processor specifies a list of fields to decode from URL encoded format.


## Example [_example_37]

In this example, `field1` is decoded in `field2`.

```yaml
  - urldecode:
      fields:
        - from: "field1"
          to: "field2"
      ignore_missing: false
      fail_on_error: true
```


## Configuration settings [_configuration_settings_43]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `fields` | Yes |  | Contains:<br><br>* `from: "source-field"`, where `from` is the source field name<br>* `to: "target-field"`, where `to` is the target field name (defaults to the `from` value)<br> |
| `ignore_missing` | No | `false` | Whether to ignore missing keys. If `true`, no error is logged if a key that should be URL-decoded is missing. |
| `fail_on_error` | No | `true` | Whether to fail if an error occurs. If `true` and an error occurs, the URL-decoding of fields is stopped, and the original event is returned. If `false`, decoding continues even if an error occurs during decoding. |

See [Conditions](/reference/ingestion-tools/fleet/dynamic-input-configuration.md#conditions) for a list of supported conditions.

