---
navigation_title: "include_fields"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/include_fields-processor.html
---

# Keep fields from events [include_fields-processor]


The `include_fields` processor specifies which fields to export if a certain condition is fulfilled. The condition is optional. If it’s missing, the specified fields are always exported. The `@timestamp`, `@metadata`, and `type` fields are always exported, even if they are not defined in the `include_fields` list.


## Example [_example_27]

```yaml
  - include_fields:
      when:
        condition
      fields: ["field1", "field2", ...]
```

See [Conditions](/reference/ingestion-tools/fleet/dynamic-input-configuration.md#conditions) for a list of supported conditions.

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


You can specify multiple `include_fields` processors under the `processors` section.

::::{note}
If you define an empty list of fields under `include_fields`, only the required fields, `@timestamp` and `type`, are exported.
::::


