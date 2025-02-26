---
navigation_title: "add_labels"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add_labels-processor.html
---

# Add labels [add_labels-processor]


The `add_labels` processors adds a set of key-value pairs to an event. The processor flattens nested configuration objects like arrays or dictionaries into a fully qualified name by merging nested names with a dot (`.`). Array entries create numeric names starting with 0. Labels are always stored under the Elastic Common Schema compliant `labels` sub-dictionary.


## Example [_example_7]

This configuration:

```yaml
  - add_labels:
      labels:
        number: 1
        with.dots: test
        nested:
          with.dots: nested
        array:
          - do
          - re
          - with.field: mi
```

Adds these fields to every event:

```json
{
  "labels": {
    "number": 1,
    "with.dots": "test",
    "nested.with.dots": "nested",
    "array.0": "do",
    "array.1": "re",
    "array.2.with.field": "mi"
  }
}
```


## Configuration settings [_configuration_settings_8]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that they process the raw event data rather than the final event sent to {{es}}. For related limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `labels` | Yes |  | Dictionaries of labels to be added. |

