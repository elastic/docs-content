---
navigation_title: "drop_event"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/drop_event-processor.html
---

# Drop events [drop_event-processor]


The `drop_event` processor drops the entire event if the associated condition is fulfilled. The condition is mandatory, because without one, all the events are dropped.


## Example [_example_23]

```yaml
  - drop_event:
      when:
        condition
```

See [Conditions](/reference/ingestion-tools/fleet/dynamic-input-configuration.md#conditions) for a list of supported conditions.

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that they process the raw event data rather than the final event sent to {{es}}. For related limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


