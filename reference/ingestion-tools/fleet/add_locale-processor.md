---
navigation_title: "add_locale"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add_locale-processor.html
---

# Add the local time zone [add_locale-processor]


The `add_locale` processor enriches each event with either the machine’s time zone offset from UTC or the name of the time zone. The processor adds the a `event.timezone` value to each event.


## Examples [_examples_4]

The configuration adds the processor with the default settings:

```yaml
  - add_locale: ~
```

This configuration adds the processor and configures it to add the time zone abbreviation to events:

```yaml
  - add_locale:
      format: abbreviation
```

::::{note}
The `add_locale` processor differentiates between daylight savings time (DST) and regular time. For example `CEST` indicates DST and and `CET` is regular time.
::::



## Configuration settings [_configuration_settings_9]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that they process the raw event data rather than the final event sent to {{es}}. For related limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `format` | No | `offset` | Whether an `offset` or time zone `abbreviation` is added to the event. |

