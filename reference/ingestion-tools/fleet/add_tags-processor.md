---
navigation_title: "add_tags"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add_tags-processor.html
---

# Add tags [add_tags-processor]


The `add_tags` processor adds tags to a list of tags. If the target field already exists, the tags are appended to the existing list of tags.


## Example [_example_12]

This configuration:

```yaml
  - add_tags:
      tags: [web, production]
      target: "environment"
```

Adds the `environment` field to every event:

```json
{
  "environment": ["web", "production"]
}
```


## Configuration settings [_configuration_settings_14]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that they process the raw event data rather than the final event sent to {{es}}. For related limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `tags` | Yes |  | List of tags to add. |
| `target` | No | `tags` | Field the tags will be added to. Setting tags in `@metadata` is not supported. |

