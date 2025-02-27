---
navigation_title: "add_network_direction"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add_network_direction-processor.html
---

# Add network direction [add_network_direction-processor]


The `add_network_direction` processor attempts to compute the perimeter-based network direction when given a source and destination IP address and a list of internal networks.


## Example [_example_8]

```yaml
  - add_network_direction:
      source: source.ip
      destination: destination.ip
      target: network.direction
      internal_networks: [ private ]
```


## Configuration settings [_configuration_settings_10]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that they process the raw event data rather than the final event sent to {{es}}. For related limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `source` | Yes |  | Source IP. |
| `destination` | Yes |  | Destination IP. |
| `target` | Yes |  | Target field where the network direction will be written. |
| `internal_networks` | Yes |  | List of internal networks. The value can contain either CIDR blocks or a list of special values enumerated in the network section of [Conditions](/reference/ingestion-tools/fleet/dynamic-input-configuration.md#conditions). |

