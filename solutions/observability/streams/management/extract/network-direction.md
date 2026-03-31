---
applies_to:
  serverless: ga
  stack: ga 9.4+
products:
  - id: observability
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Network direction processor [streams-network-direction-processor]

The **Network direction** processor determines network traffic direction (inbound, outbound, internal, or external) based on source and destination IP addresses.

To determine network direction:

1. Select **Create** → **Create processor**.
1. Select **Network direction** from the **Processor** menu.
1. Set the **Source IP** to the field containing the source IP address.
1. Set the **Destination IP** to the field containing the destination IP address.
1. Set the internal networks using either a list of CIDR ranges or a field containing the list.

## YAML reference [streams-network-direction-yaml-reference]

In [YAML mode](../extract.md#streams-editing-yaml-mode), configure the network direction processor using the following parameters. For the complete Streamlang syntax, refer to the [Streamlang reference](../streamlang.md).

Specify exactly one of `internal_networks` or `internal_networks_field`.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `source_ip` | string | Yes | Field containing the source IP address. |
| `destination_ip` | string | Yes | Field containing the destination IP address. |
| `target_field` | string | No | Target field for the direction result. |
| `internal_networks` | string[] | One of `internal_networks` or `internal_networks_field` | List of internal network CIDR ranges. |
| `internal_networks_field` | string | One of `internal_networks` or `internal_networks_field` | Field containing the list of internal networks. |
| `ignore_missing` | boolean | No | When `true`, skip this processor if a source field is missing. |

```yaml
- action: network_direction
  source_ip: attributes.source.ip
  destination_ip: attributes.destination.ip
  target_field: attributes.network.direction
  internal_networks:
    - "10.0.0.0/8"
    - "172.16.0.0/12"
    - "192.168.0.0/16"
```
