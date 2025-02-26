---
navigation_title: "add_fields"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add_fields-processor.html
---

# Add fields [add_fields-processor]


The `add_fields` processor adds fields to the event. Fields can be scalar values, arrays, dictionaries, or any nested combination of these. The `add_fields` processor overwrites the target field if it already exists. By default, the fields that you specify are grouped under the `fields` sub-dictionary in the event. To group the fields under a different sub-dictionary, use the `target` setting. To store the fields as top-level fields, set `target: ''`.


## Examples [_examples_2]

This configuration:

```yaml
  - add_fields:
      target: project
      fields:
        name: myproject
        id: '574734885120952459'
```

Adds these fields to any event:

```json
{
  "project": {
    "name": "myproject",
    "id": "574734885120952459"
  }
}
```

This configuration alters the event metadata:

```yaml
  - add_fields:
      target: '@metadata'
      fields:
        op_type: "index"
```

When the event is ingested by {{es}}, the document will have `op_type: "index"` set as a metadata field.


## Configuration settings [_configuration_settings_4]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that they process the raw event data rather than the final event sent to {{es}}. For related limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `target` | No | `fields` | Sub-dictionary to put all fields into. Set `target` to `@metadata` to add values to the event metadata instead of fields. |
| `fields` | Yes |  | Fields to be added. |

