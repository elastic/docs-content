---
navigation_title: "decode_cef"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/decode_cef-processor.html
---

# Decode CEF [decode_cef-processor]


The `decode_cef` processor decodes Common Event Format (CEF) messages.

::::{note}
This processor only works with log inputs.
::::



## Example [_example_16]

In this example, the `message` field is decoded as CEF after it is renamed to `event.original`. It is best to rename `message` to `event.original` because the decoded CEF data contains its own `message` field.

```yaml
  - rename:
      fields:
        - {from: "message", to: "event.original"}
  - decode_cef:
      field: event.original
```


## Configuration settings [_configuration_settings_19]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `field` | No | `message` | Source field containing the CEF message to be parsed. |
| `target_field` | No | `cef` | Target field where the parsed CEF object will be written. |
| `ecs` | No | `true` | Whether to generate Elastic Common Schema (ECS) fields from the CEF data. Certain CEF header and extension values will be used to populate ECS fields. |
| `timezone` | No | `UTC` | IANA time zone name (for example, `America/New_York`) or fixed time offset (for example, `+0200`) to use when parsing times that do not contain a time zone. Specify `Local` to use the machine’s local time zone. |
| `ignore_missing` | No | `false` | Whether to ignore errors when the source field is missing. |
| `ignore_failure` | No | false | Whether to ignore failures when the source field does not contain a CEF message. |
| `id` | No |  | Identifier for this processor instance. Useful for debugging. |

