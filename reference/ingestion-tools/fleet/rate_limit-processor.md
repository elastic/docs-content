---
navigation_title: "rate_limit"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/rate_limit-processor.html
---

# Rate limit the flow of events [rate_limit-processor]

::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::



The `rate_limit` processor limits the throughput of events based on the specified configuration.

In the current implementation, rate-limited events are dropped. Future implementations may allow rate-limited events to be handled differently.


## Examples [_examples_9]

```yaml
- rate_limit:
   limit: "10000/m"
```

```yaml
- rate_limit:
   fields:
   - "cloudfoundry.org.name"
   limit: "400/s"
```

```yaml
- if.equals.cloudfoundry.org.name: "acme"
  then:
  - rate_limit:
      limit: "500/s"
```


## Configuration settings [_configuration_settings_34]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that your processor configurations cannot refer to fields that are created by ingest pipelines or {{ls}}. For more limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `limit` | Yes |  | The rate limit. Supported time units for the rate are `s` (per second), `m` (per minute), and `h` (per hour). |
| `fields` | No |  | List of fields. The rate limit will be applied to each distinct value derived by combining the values of these fields. |

