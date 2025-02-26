---
navigation_title: "add_id"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add_id-processor.html
---

# Generate an ID for an event [add_id-processor]


The `add_id` processor generates a unique ID for an event.


## Example [_example_6]

```yaml
  - add_id: ~
```


## Configuration settings [_configuration_settings_6]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that they process the raw event data rather than the final event sent to {{es}}. For related limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `target_field` | No | `@metadata._id` | Field where the generated ID will be stored. |
| `type` | No | `elasticsearch` | Type of ID to generate. Currently only `elasticsearch` is supported. The `elasticsearch` type uses the same algorithm that {{es}} uses to auto-generate document IDs. |

